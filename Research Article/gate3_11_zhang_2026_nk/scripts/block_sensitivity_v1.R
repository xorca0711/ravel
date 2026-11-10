args <- commandArgs(trailingOnly=TRUE); out <- args[[1]]
library(limma)
stopifnot(as.character(packageVersion('limma'))=='3.58.1')
src <- 'analysis/research/runs/zh26_s1_reproduction_v1'
y <- as.matrix(read.csv(file.path(src,'logTPM.csv'),row.names=1,check.names=FALSE))
meta <- read.csv('raw_data/zhang_2026/source_v1/author/input_files/sample_info_NK.csv',row.names=1)
stopifnot(identical(colnames(y),rownames(meta)))
result <- list()
for(omit in unique(meta$replicate)) {
  take <- meta$replicate != omit
  condition <- factor(meta$condition[take],levels=c('PBS','ITDT','ITDT_aCD4'))
  replicate <- factor(meta$replicate[take])
  design <- model.matrix(~0+condition+replicate,contrasts.arg=list(replicate='contr.sum'))
  stopifnot(qr(design)$rank==4)
  fit <- lmFit(y[,take],design)
  ct <- makeContrasts(ITDTvsPBS=conditionITDT-conditionPBS,ITDTaCD4vsITDT=conditionITDT_aCD4-conditionITDT,levels=design)
  cf <- contrasts.fit(fit,ct)$coefficients
  for(i in 1:2) result[[length(result)+1]] <- data.frame(gene=rownames(cf),contrast=c('itdt_vs_pbs','itdt_acd4_vs_itdt')[i],omitted_block=omit,logFC=cf[,i],residual_df=2)
}
write.csv(do.call(rbind,result),file.path(out,'leave_one_block_out.csv'),row.names=FALSE)
capture.output(sessionInfo(),file=file.path(out,'R_session.txt'))
