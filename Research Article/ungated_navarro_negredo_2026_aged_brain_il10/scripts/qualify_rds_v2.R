suppressPackageStartupMessages({library(Matrix);library(SeuratObject);library(jsonlite)})
args <- commandArgs(trailingOnly=TRUE)
cfg <- fromJSON(args[1],simplifyVector=FALSE)
out <- args[2]
options(digits=17)
writej <- function(x,name) write_json(x,file.path(out,name),pretty=TRUE,auto_unbox=TRUE,digits=17,null='null',na='null')
writet <- function(x,name) write.table(x,file.path(out,name),sep='\t',row.names=FALSE,quote=TRUE,na='NA')
slots <- function(x) setdiff(names(attributes(x)),'class')
getslot <- function(x,n) if(n %in% slots(x)) slot(x,n) else NULL
simple <- function(x) {
  if(is.null(x)) return(NULL)
  if(inherits(x,'numeric_version')) return(as.character(x))
  if(is.function(x) || is.environment(x)) return(list(class=class(x),content='not serialized'))
  if(is.matrix(x) || inherits(x,'Matrix')) return(list(class=class(x),dim=dim(x)))
  if(is.list(x)) return(lapply(x,simple))
  if(length(x)>200) return(list(length=length(x),head=head(as.character(x),10)))
  if(inherits(x,'POSIXt')) return(as.character(x))
  if(is.factor(x)) return(as.character(x))
  if(isS4(x)) return(list(class=class(x),slots=slots(x)))
  x
}
writej(list(phase='before_readRDS',input=cfg$rds_path,R=R.version.string),'load_status.json')
obj <- readRDS(cfg$rds_path)
writej(list(phase='loaded',object_class=class(obj),R=R.version.string),'load_status.json')
stopifnot(isS4(obj),'meta.data' %in% slots(obj),'assays' %in% slots(obj))
meta <- slot(obj,'meta.data')
assays <- slot(obj,'assays')
inventory <- list(object_class=class(obj),object_slots=slots(obj),object_version=simple(getslot(obj,'version')),
                 default_assay=getslot(obj,'active.assay'),assays=list(),metadata_columns=list(),commands=list())
for(n in names(assays)) {
  assay <- assays[[n]]
  desc <- list(class=class(assay),slots=slots(assay),matrices=list())
  for(s in intersect(c('counts','data','scale.data'),slots(assay))) {
    m <- slot(assay,s)
    desc$matrices[[s]] <- list(class=class(m),dim=dim(m),sparse=inherits(m,'sparseMatrix'),
      stored_entries=if('x' %in% slots(m)) length(m@x) else length(m))
  }
  if('layers' %in% slots(assay)) desc$layers <- lapply(slot(assay,'layers'),function(m)list(class=class(m),dim=dim(m)))
  inventory$assays[[n]] <- desc
}
for(n in names(meta)) {
  v <- meta[[n]]
  u <- unique(v)
  desc <- list(class=class(v),missing=sum(is.na(v)),unique_values=length(u),
               levels=if(is.factor(v)) levels(v) else if(!is.numeric(v)&&length(u)<=100) as.character(u) else NULL)
  if(is.numeric(v)) desc$quantiles <- quantile(v,probs=c(0,.25,.5,.75,1),na.rm=TRUE,names=TRUE)
  inventory$metadata_columns[[n]] <- desc
}
commands <- getslot(obj,'commands')
for(n in names(commands)) {
  v <- commands[[n]]
  inventory$commands[[n]] <- list(class=class(v),name=simple(getslot(v,'name')),
      assay_used=simple(getslot(v,'assay.used')),call=simple(getslot(v,'call.string')),params=simple(getslot(v,'params')))
}
inventory$donor_resembling_fields <- grep('donor|mouse|animal|sample|hash|demux|orig|batch',names(meta),value=TRUE,ignore.case=TRUE)
inventory$donor_assignment_provenance <- 'A column name, pool size, barcode prefix or orig.ident is not individual mouse assignment; source S1 says no multiplexing.'
writej(inventory,'object_inventory.json')
stopifnot('RNA' %in% names(assays))
rna <- assays[['RNA']]
stopifnot(all(c('counts','data') %in% slots(rna)))
counts <- slot(rna,'counts'); normalized <- slot(rna,'data')
stopifnot(inherits(counts,'dgCMatrix'),inherits(normalized,'dgCMatrix'))
stopifnot(cfg$condition_field %in% names(meta),cfg$annotation_field %in% names(meta))
condition <- as.character(meta[[cfg$condition_field]])
annotation <- as.character(meta[[cfg$annotation_field]])
alignment <- list(counts_normalized_dim_equal=identical(dim(counts),dim(normalized)),
  counts_normalized_genes_identical=identical(rownames(counts),rownames(normalized)),
  counts_normalized_cells_identical=identical(colnames(counts),colnames(normalized)),
  counts_metadata_cells_identical=identical(colnames(counts),rownames(meta)),
  unique_barcodes=anyDuplicated(rownames(meta))==0,unique_genes=anyDuplicated(rownames(counts))==0,
  missing_condition=sum(is.na(condition)|condition==''),missing_annotation=sum(is.na(annotation)|annotation==''))
writej(alignment,'alignment.json')
stopifnot(all(unlist(alignment[1:6])),alignment$missing_condition==0,alignment$missing_annotation==0)
recovery <- as.data.frame(table(condition,annotation),stringsAsFactors=FALSE)
names(recovery) <- c('condition','celltype','cells')
totals <- table(condition)
recovery$condition_total <- as.numeric(totals[recovery$condition])
recovery$fraction_of_recovered_condition <- recovery$cells/recovery$condition_total
writet(recovery,'recovery.tsv')
prefix <- sub('_.*$','',rownames(meta))
prefix_table <- as.data.frame(table(condition,prefix),stringsAsFactors=FALSE)
names(prefix_table)<-c('condition','barcode_prefix','cells')
writet(prefix_table[prefix_table$cells>0,],'barcode_prefixes.tsv')
library_totals <- Matrix::colSums(counts)
feature_counts <- integer(ncol(counts));count_zero=count_negative=count_noninteger=count_nonfinite=0L
for(j in seq_len(ncol(counts))) {
  begin=counts@p[j]+1L;end=counts@p[j+1L]
  x=if(begin<=end) counts@x[begin:end] else numeric()
  feature_counts[j]=sum(x>0)
  count_zero=count_zero+sum(x==0);count_negative=count_negative+sum(x<0)
  count_noninteger=count_noninteger+sum(x!=floor(x));count_nonfinite=count_nonfinite+sum(!is.finite(x))
}
qc <- list(cells=nrow(meta),genes=nrow(counts),conditions=as.list(totals),celltypes=as.list(table(annotation)),
  sparse_counts=list(explicit_zeros=count_zero,negative=count_negative,noninteger=count_noninteger,nonfinite=count_nonfinite),
  zero_library_totals=sum(library_totals<=0),
  nCount_matches=if('nCount_RNA'%in%names(meta))max(abs(library_totals-meta$nCount_RNA)) else NULL,
  nFeature_matches=if('nFeature_RNA'%in%names(meta))max(abs(feature_counts-meta$nFeature_RNA)) else NULL,
  thresholds=list(nCount_RNA_gt_1000=if('nCount_RNA'%in%names(meta))sum(meta$nCount_RNA<=1000) else NULL,
                  nFeature_RNA_gt_500=if('nFeature_RNA'%in%names(meta))sum(meta$nFeature_RNA<=500) else NULL,
                  percent_mt_lt_10=if('percent.mt'%in%names(meta))sum(meta$percent.mt>=10) else NULL),
  broad_Remove_cells=sum(annotation=='Remove'),downstream_Micro_types_present='Micro_types'%in%names(meta),
  WT50_present='WT50'%in%condition,Mut50_present='Mut50'%in%condition,
  true_mouse_assignment_established=FALSE,
  source_pooling='One pool/library per main condition. Old vehicle one mouse; other reported main libraries two pooled mice; no multiplexing.')
writej(qc,'qc.json')
stopifnot(count_negative==0,count_noninteger==0,count_nonfinite==0,all(library_totals>0))
norm_names <- grep('NormalizeData',names(commands),value=TRUE)
candidate_commands <- Filter(function(n) {
  a <- getslot(commands[[n]],'assay.used')
  identical(a,'RNA') || grepl('RNA',n,fixed=TRUE)
},norm_names)
norm_params <- if(length(candidate_commands)==1)getslot(commands[[candidate_commands]],'params') else list()
method <- norm_params[['normalization.method']]
scale <- norm_params[['scale.factor']]
if(is.null(method))method <- cfg$normalization_candidate$method
if(is.null(scale))scale <- cfg$normalization_candidate$scale_factor
stopifnot(method=='LogNormalize',is.numeric(scale),length(scale)==1,scale>0)
idx <- unlist(lapply(sort(unique(condition)),function(g) {
  w=which(condition==g);w[unique(round(seq(1,length(w),length.out=min(cfg$cells_per_condition,length(w)))))]
}))
uniform_rows <- unique(round(seq(1,nrow(counts),length.out=min(cfg$uniform_genes,nrow(counts)))))
rows <- vector('list',length(idx))
for(k in seq_along(idx)) {
  j=idx[k];begin=counts@p[j]+1L;end=counts@p[j+1L]
  nonzero=if(begin<=end)counts@i[begin:end]+1L else integer()
  nonzero=nonzero[unique(round(seq(1,length(nonzero),length.out=min(cfg$nonzero_genes,length(nonzero)))))]
  ii=sort(unique(c(uniform_rows,nonzero)))
  raw=as.numeric(counts[ii,j]);stored=as.numeric(normalized[ii,j]);reconstructed=log1p(scale*raw/library_totals[j])
  rows[[k]]=data.frame(cell=colnames(counts)[j],condition=condition[j],celltype=annotation[j],
    gene=rownames(counts)[ii],raw_count=raw,library_total=library_totals[j],stored=stored,
    reconstructed=reconstructed,absolute_error=abs(stored-reconstructed),stringsAsFactors=FALSE)
}
sampled=do.call(rbind,rows)
writet(sampled,'normalization_samples.tsv')
normcheck <- list(method=method,scale_factor=scale,stored_command_names=candidate_commands,
  parameters_recorded=length(candidate_commands)==1,formula='log1p(raw_count / RNA library_total * scale_factor)',
  sample_cells=length(idx),sample_entries=nrow(sampled),sample_nonzero=sum(sampled$raw_count>0),sample_zero=sum(sampled$raw_count==0),
  max_absolute_error=max(sampled$absolute_error),tolerance=cfg$normalization_tolerance,
  reconstruction_passed=max(sampled$absolute_error)<=cfg$normalization_tolerance,
  qualification='Sampled arithmetic validation, not whole-matrix equality and not biological replication.')
writej(normcheck,'normalization.json')
capture.output(sessionInfo(),file=file.path(out,'R_session.txt'))
writej(list(metadata_qualification_completed=TRUE,normalization_reconstruction_passed=normcheck$reconstruction_passed,
           biological_population_inference_allowed=FALSE,actual_object_loaded=TRUE), 'metadata_stage_status.json')
