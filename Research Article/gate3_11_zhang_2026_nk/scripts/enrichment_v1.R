args <- commandArgs(trailingOnly=TRUE); out <- args[[1]]
library(fgsea); library(msigdbr)
stopifnot(as.character(packageVersion('fgsea'))=='1.26.0',as.character(packageVersion('msigdbr'))=='7.5.1')
gs <- rbind(msigdbr(species='Mus musculus',category='H'),msigdbr(species='Mus musculus',category='C2',subcategory='CP:KEGG'))
gs$gene_symbol <- toupper(gs$gene_symbol)
members <- unique(gs[,c('gs_name','gene_symbol')])
members <- members[order(members$gs_name,members$gene_symbol),]
write.csv(members,file.path(out,'gene_sets.csv'),row.names=FALSE)
pathways <- split(members$gene_symbol,members$gs_name)
coverage <- list()
for(contrast in c('itdt_vs_pbs','itdt_acd4_vs_itdt')) {
  df <- read.csv(file.path('analysis/research/runs/zh26_s1_reproduction_v1',paste0(contrast,'_nk.csv')),row.names=1,check.names=FALSE)
  symbols <- toupper(rownames(df));stopifnot(!anyDuplicated(symbols))
  rownames(df) <- symbols;df <- df[df$AveExpr > 1,,drop=FALSE]
  df <- df[order(-df$logFC),,drop=FALSE]
  ranks <- setNames(df$logFC,rownames(df))
  write.csv(data.frame(symbol=names(ranks),statistic=unname(ranks)),file.path(out,paste0('ranks_',contrast,'.csv')),row.names=FALSE)
  for(p in names(pathways)) coverage[[length(coverage)+1]] <- data.frame(contrast=contrast,pathway=p,source_members=length(pathways[[p]]),retained_members=sum(pathways[[p]] %in% names(ranks)),ranked_genes=length(ranks))
  set.seed(42)
  # Explicit serial backend is a recorded portability adaptation; source backend is unreported.
  result <- fgsea(pathways=pathways,stats=ranks,gseaParam=1,scoreType='std',minSize=0,maxSize=Inf,nPermSimple=3000,BPPARAM=BiocParallel::SerialParam())
  result$leadingEdge <- vapply(result$leadingEdge,paste,collapse=',',FUN.VALUE=character(1))
  result <- result[order(result$padj),]
  write.csv(as.data.frame(result),file.path(out,paste0('gsea_',contrast,'.csv')),row.names=FALSE)
}
write.csv(do.call(rbind,coverage),file.path(out,'coverage.csv'),row.names=FALSE)
capture.output(sessionInfo(),file=file.path(out,'R_session.txt'))
writeLines(c('CLI_NO_THREAD=true disables only cli progress tick thread (Windows ARM workaround).',
  'BiocParallel::SerialParam; seed=42 for each contrast; source parallel backend not reported.',
  paste('babelgene',packageVersion('babelgene'))),file.path(out,'runtime_settings.txt'))
