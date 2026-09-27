args <- commandArgs(TRUE)
stopifnot(length(args)==3)
input <- args[1]; out <- args[2]; cache <- args[3]
suppressPackageStartupMessages(library(Matrix))
dir.create(out, recursive=TRUE, showWarnings=FALSE)
dir.create(cache, recursive=TRUE, showWarnings=FALSE)
stopifnot(!file.exists(file.path(out,'object_inventory.txt')))
cat('Reading RDS\n'); flush.console()
o <- readRDS(input)
inv <- capture.output({
 cat('Class:',class(o),'\nAttributes:',names(attributes(o)),'\n')
 cat('Object bytes:',as.numeric(object.size(o)),'\n')
})
m <- attr(o,'meta.data')
stopifnot(is.data.frame(m),!anyDuplicated(rownames(m)))
write.table(cbind(cell_id=rownames(m),m),gzfile(file.path(cache,'cell_metadata.tsv.gz')),sep='\t',quote=FALSE,row.names=FALSE)
inv <- c(inv,paste('Cells:',nrow(m)),paste('Metadata fields:',paste(names(m),collapse=', ')))
lev <- do.call(rbind,lapply(names(m),function(k){v<-unique(as.character(m[[k]]));data.frame(field=k,class=class(m[[k]])[1],n_unique=length(v),n_missing=sum(is.na(m[[k]])),values=if(length(v)<=100)paste(sort(v),collapse=' | ') else '<high cardinality>')}))
write.table(lev,file.path(out,'metadata_fields.tsv'),sep='\t',quote=FALSE,row.names=FALSE)
assays <- attr(o,'assays')
inv <- c(inv,paste('Assays:',paste(names(assays),collapse=', ')))
rows <- list()
for(an in names(assays)) {
 a<-assays[[an]]
 inv<-c(inv,paste('Assay',an,'class',class(a),'attributes',paste(names(attributes(a)),collapse=', ')))
 for(sn in intersect(c('counts','data','scale.data'),names(attributes(a)))) {
  mat<-attr(a,sn); dims<-dim(mat)
  rows[[length(rows)+1]]<-data.frame(assay=an,slot=sn,class=class(mat)[1],n_genes=dims[1],n_cells=dims[2])
  if(an=='RNA' && sn=='counts') {
   stopifnot(identical(colnames(mat),rownames(m)))
   write.table(data.frame(gene_id=rownames(mat)),file.path(out,'rna_gene_index.tsv'),sep='\t',quote=FALSE,row.names=FALSE)
   v<-attr(mat,'x'); stopifnot(!is.null(v))
   nonfinite<-0; negative<-0; noninteger<-0
   for(start in seq.int(1,length(v),by=1000000)) {
    q<-v[start:min(length(v),start+999999)]
    nonfinite<-nonfinite+sum(!is.finite(q)); negative<-negative+sum(q<0,na.rm=TRUE)
    noninteger<-noninteger+sum(abs(q-round(q))>1e-8,na.rm=TRUE)
   }
   inv<-c(inv,paste('RNA stored values:',length(v)),paste('RNA nonfinite:',nonfinite),paste('RNA negative:',negative),paste('RNA noninteger:',noninteger),paste('RNA range:',paste(range(v),collapse=' ')),paste('RNA duplicated genes:',sum(duplicated(rownames(mat)))))
   totals<-Matrix::colSums(mat)
   write.table(data.frame(cell_id=names(totals),RNA_UMIs=as.numeric(totals)),gzfile(file.path(cache,'cell_rna_totals.tsv.gz')),sep='\t',quote=FALSE,row.names=FALSE)
  }
 }
}
write.table(do.call(rbind,rows),file.path(out,'assays.tsv'),sep='\t',quote=FALSE,row.names=FALSE)
writeLines(inv,file.path(out,'object_inventory.txt'))
writeLines(capture.output(sessionInfo()),file.path(out,'R_session.txt'))
cat(paste(inv,collapse='\n'),'\n')
