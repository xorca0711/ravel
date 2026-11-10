suppressPackageStartupMessages({library(Matrix);library(SeuratObject);library(jsonlite)})
options(digits=17,warn=1)
args=commandArgs(trailingOnly=TRUE);cfg=fromJSON(args[1]);out=args[2]
obj=readRDS(cfg$rds_path)
meta=slot(obj,'meta.data');counts=slot(slot(obj,'assays')[['RNA']],'counts');rna=slot(slot(obj,'assays')[['RNA']],'data')
stopifnot(inherits(counts,'dgCMatrix'),inherits(rna,'dgCMatrix'),identical(dimnames(counts),dimnames(rna)),identical(colnames(counts),rownames(meta)),ncol(counts)==51176,nrow(counts)==31053)
rm(obj);gc()
condition=as.character(meta$orig.ident);annotation=as.character(meta$Celltype)
totals=Matrix::colSums(counts)
selected=which(condition %in% cfg$conditions & annotation %in% cfg$celltypes)
stopifnot(!anyNA(condition[selected]),!anyNA(annotation[selected]),!anyDuplicated(selected),all(totals[selected]>0))
write.table(data.frame(cell_index=selected,barcode=colnames(counts)[selected],condition=condition[selected],celltype=annotation[selected],library_total=unname(totals[selected])),file.path(out,'cell_denominators.tsv'),sep='\t',row.names=FALSE,quote=TRUE)
audit=gzfile(file.path(out,'selected_entries.tsv.gz'),'wt');writeLines('cell_index\tgene\traw_count\tnormalized',audit)
summaries=list();available=list()
for(gene in cfg$genes) {
 gi=match(gene,rownames(counts));present=!is.na(gi)
 available[[length(available)+1]]=data.frame(gene=gene,present=present)
 raw=if(present)as.numeric(counts[gi,selected]) else rep(NA_real_,length(selected))
 value=if(present)as.numeric(rna[gi,selected]) else rep(NA_real_,length(selected))
 if(present) {
  stopifnot(all(is.finite(value)),all(value>=0),all(value[raw==0]==0))
  nz=which(raw>0)
  if(length(nz))write.table(data.frame(cell_index=selected[nz],gene=gene,raw_count=raw[nz],normalized=value[nz]),audit,sep='\t',row.names=FALSE,col.names=FALSE,quote=FALSE)
 }
 for(type in cfg$celltypes)for(cond in cfg$conditions) {
  ii=which(annotation[selected]==type & condition[selected]==cond);n=length(ii)
  summaries[[length(summaries)+1]]=data.frame(celltype=type,condition=cond,gene=gene,present=present,n_cells=n,
   total_raw=if(present)sum(raw[ii]) else NA_real_,n_detected=if(present)sum(raw[ii]>0) else NA_integer_,
   mean_log_expression=if(present&&n>0)mean(value[ii]) else NA_real_,
   detection_fraction=if(present&&n>0)sum(raw[ii]>0)/n else NA_real_)
 }
}
close(audit)
write.table(do.call(rbind,summaries),file.path(out,'summaries_R.tsv'),sep='\t',row.names=FALSE,quote=TRUE,na='NA')
write.table(do.call(rbind,available),file.path(out,'marker_availability.tsv'),sep='\t',row.names=FALSE,quote=TRUE,na='NA')
capture.output(sessionInfo(),file=file.path(out,'R_session.txt'))
