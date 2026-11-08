suppressPackageStartupMessages({library(Matrix);library(SeuratObject);library(jsonlite)})
options(digits=17,warn=1)
args=commandArgs(trailingOnly=TRUE);cfg=fromJSON(args[1]);out=args[2]
markers=fromJSON(cfg$marker_manifest)
obj=readRDS(cfg$rds_path)
meta=slot(obj,'meta.data');counts=slot(slot(obj,'assays')[['RNA']],'counts');rna=slot(slot(obj,'assays')[['RNA']],'data')
stopifnot(inherits(counts,'dgCMatrix'),inherits(rna,'dgCMatrix'),identical(dimnames(counts),dimnames(rna)),identical(colnames(counts),rownames(meta)))
rm(obj);gc()
condition=as.character(meta$orig.ident);annotation=as.character(meta$Celltype)
libtotal=Matrix::colSums(counts)
selected=which(condition %in% cfg$conditions & annotation %in% c('Microglia','T_cells'))
stopifnot(!anyNA(condition[selected]),!anyNA(annotation[selected]),!anyDuplicated(selected))
gzm=match('Gzmb',rownames(counts));stopifnot(!is.na(gzm))
positive=rep(NA_integer_,length(selected));tc=which(annotation[selected]=='T_cells')
positive[tc]=as.integer(as.numeric(counts[gzm,selected[tc]])>0)
denom=data.frame(cell_index=selected,condition=condition[selected],celltype=annotation[selected],
  library_total=unname(libtotal[selected]),gzmb_positive=positive,stringsAsFactors=FALSE)
write.table(denom,file.path(out,'cell_denominators.tsv'),sep='\t',row.names=FALSE,quote=TRUE,na='NA')
genes=list(Microglia=c(markers$vectors$il10$genes,markers$vectors$ifng$genes),T_cells=markers$vectors$tcell_primary$genes)
availability=list();summaries=list();audit=gzfile(file.path(out,'selected_entries.tsv.gz'),'wt')
writeLines('cell_index\tcondition\tcelltype\tgene\traw_count\tnormalized\tlibrary_total',audit)
for(type in names(genes)) {
  cells=selected[annotation[selected]==type]
  for(gene in genes[[type]]) {
    family=if(type=='T_cells')'T_cell_primary' else if(gene %in% markers$vectors$il10$genes)'IL10_related_mixed_direction' else 'IFN_related'
    gi=match(gene,rownames(counts));present=!is.na(gi)
    availability[[length(availability)+1L]]=data.frame(scope=type,family=family,gene=gene,present=present)
    raw=if(present)as.numeric(counts[gi,cells]) else rep(NA_real_,length(cells))
    value=if(present)as.numeric(rna[gi,cells]) else rep(NA_real_,length(cells))
    if(present) {
      stopifnot(all(is.finite(value)),all(value>=0),all(value[raw==0]==0))
      nz=which(raw>0)
      if(length(nz))write.table(data.frame(cell_index=cells[nz],condition=condition[cells[nz]],celltype=type,gene=gene,
        raw_count=raw[nz],normalized=value[nz],library_total=unname(libtotal[cells[nz]])),audit,sep='\t',row.names=FALSE,col.names=FALSE,quote=FALSE)
    }
    for(group in cfg$conditions) {
      ii=which(condition[cells]==group);n=length(ii);det=if(present)sum(raw[ii]>0) else NA_integer_
      summaries[[length(summaries)+1L]]=data.frame(scope=type,family=family,gene=gene,condition=group,gene_present=present,
        n_cells=n,n_detected=det,sum_normalized=if(present)sum(value[ii]) else NA_real_,total_raw=if(present)sum(raw[ii]) else NA_real_,
        mean_log_expression=if(present&&n>0)mean(value[ii]) else NA_real_,detection_fraction=if(present&&n>0)det/n else NA_real_,
        mean_log_expression_positive=if(present&&det>0)mean(value[ii][raw[ii]>0]) else NA_real_,
        n_all_T=if(type=='T_cells')n else NA_integer_,gzmb_positive_fraction_all_T=NA_real_,stringsAsFactors=FALSE)
      if(type=='T_cells'&&gene=='Gzmb') {
        pos=ii[raw[ii]>0];np=length(pos)
        summaries[[length(summaries)+1L]]=data.frame(scope='T_cells_Gzmb_positive',family='T_cell_conditional',gene=gene,condition=group,gene_present=present,
          n_cells=np,n_detected=np,sum_normalized=sum(value[pos]),total_raw=sum(raw[pos]),
          mean_log_expression=if(np>0)mean(value[pos]) else NA_real_,detection_fraction=if(np>0)1 else NA_real_,
          mean_log_expression_positive=if(np>0)mean(value[pos]) else NA_real_,n_all_T=n,
          gzmb_positive_fraction_all_T=if(n>0)np/n else NA_real_,stringsAsFactors=FALSE)
      }
    }
  }
}
close(audit)
summary=do.call(rbind,summaries);available=do.call(rbind,availability)
write.table(summary,file.path(out,'summaries_R.tsv'),sep='\t',row.names=FALSE,quote=TRUE,na='NA')
write.table(available,file.path(out,'marker_availability.tsv'),sep='\t',row.names=FALSE,quote=TRUE,na='NA')
contrasts=list()
for(k in seq_len(nrow(cfg$contrasts))) {
  contrast=cfg$contrasts[k,]
  left=summary[summary$condition==contrast$left,];right=summary[summary$condition==contrast$right,]
  key=function(x)paste(x$scope,x$gene,sep='|');right=right[match(key(left),key(right)),]
  stopifnot(identical(key(left),key(right)))
  contrasts[[k]]=data.frame(scope=left$scope,family=left$family,gene=left$gene,contrast=contrast$id,
    left=contrast$left,right=contrast$right,n_left=left$n_cells,n_right=right$n_cells,
    mean_log_difference=left$mean_log_expression-right$mean_log_expression,
    detection_fraction_difference=left$detection_fraction-right$detection_fraction,
    gzmb_positive_fraction_all_T_difference=left$gzmb_positive_fraction_all_T-right$gzmb_positive_fraction_all_T)
}
write.table(do.call(rbind,contrasts),file.path(out,'contrasts_R.tsv'),sep='\t',row.names=FALSE,quote=TRUE,na='NA')
capture.output(sessionInfo(),file=file.path(out,'R_session.txt'))
write_json(list(conditions=cfg$conditions,excluded_expression_aliases=c('WT50','Mut50'),
  original_broad_annotations=TRUE,normalization='RNA LogNormalize, scale 10000',
  no_reclustering=TRUE,no_downsampling=TRUE,no_population_inference=TRUE,
  R_loaded_once=TRUE,unneeded_assays_released_before_summaries=TRUE),file.path(out,'description_scope.json'),pretty=TRUE,auto_unbox=TRUE)
