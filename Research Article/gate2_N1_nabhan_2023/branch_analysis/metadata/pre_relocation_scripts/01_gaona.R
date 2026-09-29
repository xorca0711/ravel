args<-commandArgs(trailingOnly=TRUE);stopifnot(length(args)==2)
root<-normalizePath(args[1],winslash='/');.libPaths(c(args[2],.libPaths()))
suppressPackageStartupMessages(library(edgeR));suppressPackageStartupMessages(library(limma));suppressPackageStartupMessages(library(jsonlite))
out<-file.path(root,'trials/extension_v1');stopifnot(file.exists(file.path(out,'contract.json')),!file.exists(file.path(out,'gaona_complete.json')))
repo<-dirname(dirname(root));paper<-file.path(repo,'Research Article/gate2_N1_nabhan_2023')
x<-read.csv(gzfile(file.path(paper,'raw/GSE327565_raw_counts_GEO_YapTaz.csv.gz')),check.names=FALSE)
meta<-fromJSON(file.path(repo,'RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE327565.json'),simplifyVector=FALSE)
m<-do.call(rbind,lapply(meta$samples,function(s){
 col<-sub('Column name in raw_counts_GEO_YapTaz.csv: ','',unlist(s$description)[2])
 data.frame(accession=s$accession,column=col,genotype=if(grepl('^WT',col)) 'WT' else 'YT',medium=if(grepl('A',col)) 'ADM' else 'SFFFM',source_unit='source-reported mouse; cross-media identity unresolved')
}))
counts<-as.matrix(x[,m$column]);rownames(counts)<-x$ID
stopifnot(!anyDuplicated(x$ID),all(counts>=0),all(counts==floor(counts)))
keep<-rowSums(counts>=10)>=3
tab<-function(x,n)write.table(x,file.path(out,'tables',n),sep='\t',row.names=FALSE,quote=FALSE,na='NA')
tab(m,'gaona_samples.tsv');all<-list();norm<-list();qc<-list()
for(med in c('SFFFM','ADM')) {
 mm<-m[m$medium==med,];d<-DGEList(counts[keep,mm$column,drop=FALSE]);d<-normLibSizes(d,method='TMM')
 design<-model.matrix(~factor(mm$genotype,levels=c('WT','YT')))
 v<-voom(d,design,plot=FALSE);fit<-eBayes(lmFit(v,design))
 tt<-topTable(fit,coef=2,number=Inf,sort.by='none',confint=TRUE)
 all[[med]]<-data.frame(gene_id=rownames(tt),symbol=x$Gene.name[match(rownames(tt),x$ID)],medium=med,tt,check.names=FALSE)
 norm[[med]]<-data.frame(gene_id=rownames(v$E),symbol=x$Gene.name[match(rownames(v$E),x$ID)],v$E,check.names=FALSE)
 qc[[med]]<-data.frame(mm,d$samples,check.names=FALSE)
}
tab(do.call(rbind,all),'gaona_gene_effects.tsv.gz.tmp')
# Explicit gzip for portable readers; never leave a misleading .gz extension.
con<-gzfile(file.path(out,'tables/gaona_gene_effects.tsv.gz'),'wt');write.table(do.call(rbind,all),con,sep='\t',row.names=FALSE,quote=FALSE);close(con)
unlink(file.path(out,'tables/gaona_gene_effects.tsv.gz.tmp'))
tab(merge(norm[[1]],norm[[2]],by=c('gene_id','symbol'),sort=FALSE),'gaona_log2CPM.tsv')
tab(do.call(rbind,qc),'gaona_normalization.tsv')
write_json(list(finished_utc=format(Sys.time(),tz='UTC',usetz=TRUE),input_genes=nrow(x),kept_genes=sum(keep),samples=nrow(m),R=R.version.string,limma=as.character(packageVersion('limma')),edgeR=as.character(packageVersion('edgeR')),scope='two separate within-medium contrasts; source-reported mouse independence'),file.path(out,'gaona_complete.json'),auto_unbox=TRUE,pretty=TRUE)
cat('Gaona:',sum(keep),'genes; separate 3v3 and 4v4 contrasts\n')
