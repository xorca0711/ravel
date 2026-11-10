args <- commandArgs(trailingOnly=TRUE);out<-args[[1]]
library(fgsea)
stopifnot(as.character(packageVersion('fgsea'))=='1.26.0')
s1<-'analysis/research/runs/zh26_s1_reproduction_v1'
s2<-'analysis/research/runs/zh26_s2_enrichment_v1'
gs<-read.csv(file.path(s2,'gene_sets.csv'))
pathways<-split(gs$gene_symbol,gs$gs_name)
for(contrast in c('itdt_vs_pbs','itdt_acd4_vs_itdt')) {
  df<-read.csv(file.path(s1,paste0(contrast,'_nk.csv')),row.names=1,check.names=FALSE)
  rownames(df)<-toupper(rownames(df));stopifnot(!anyDuplicated(rownames(df)))
  df<-df[df$AveExpr>1,,drop=FALSE];df<-df[order(-df$t),,drop=FALSE]
  ranks<-setNames(df$t,rownames(df))
  old<-read.csv(file.path(s2,paste0('ranks_',contrast,'.csv')))
  stopifnot(setequal(old$symbol,names(ranks)))
  write.csv(data.frame(symbol=names(ranks),statistic=unname(ranks)),file.path(out,paste0('ranks_',contrast,'.csv')),row.names=FALSE)
  set.seed(42)
  result<-fgsea(pathways=pathways,stats=ranks,gseaParam=1,scoreType='std',minSize=0,maxSize=Inf,nPermSimple=3000,BPPARAM=BiocParallel::SerialParam())
  result$leadingEdge<-vapply(result$leadingEdge,paste,collapse=',',FUN.VALUE=character(1))
  write.csv(as.data.frame(result[order(result$padj),]),file.path(out,paste0('gsea_t_',contrast,'.csv')),row.names=FALSE)
}
capture.output(sessionInfo(),file=file.path(out,'R_session.txt'))
