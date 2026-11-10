# Faithful numerical core of released limma_nk.Rmd and nk_pca.Rmd.
# Only I/O, base-R table manipulation and plotting are adapted; no model change.
args <- commandArgs(trailingOnly=TRUE)
out <- args[[1]]
library(limma)
library(edgeR)
stopifnot(as.character(packageVersion('limma')) == '3.58.1')
raw <- 'raw_data/zhang_2026/source_v1/author'
y <- as.matrix(read.csv(file.path(raw,'input_files/NK_kallisto_tpm.csv'),row.names=1,check.names=FALSE))
meta <- read.csv(file.path(raw,'input_files/sample_info_NK.csv'),row.names=1,check.names=FALSE)
stopifnot(identical(colnames(y),rownames(meta)))
keep <- rowSums(y > 1) >= 3
write.csv(data.frame(gene=rownames(y),samples_gt1=rowSums(y > 1),included=keep,
                     reason=ifelse(keep,'TPM > 1 in at least three libraries','Fails released TPM filter')),
          file.path(out,'feature_inclusion.csv'),row.names=FALSE)
x <- DGEList(counts=y[keep,,drop=FALSE])
condition <- factor(meta$condition,levels=c('PBS','ITDT','ITDT_aCD4'))
replicate <- factor(meta$replicate)
design <- model.matrix(~0 + condition + replicate,contrasts.arg=list(replicate='contr.sum'))
stopifnot(qr(design)$rank == ncol(design))
logTPM <- log2(x$counts + 0.5)
fit0 <- lmFit(logTPM,design)
contrast <- makeContrasts(ITDTvsPBS=conditionITDT-conditionPBS,
  ITDTaCD4vsPBS=conditionITDT_aCD4-conditionPBS,
  ITDTaCD4vsITDT=conditionITDT_aCD4-conditionITDT,levels=design)
fit <- eBayes(contrasts.fit(fit0,contrast),trend=TRUE)
files <- c('itdt_vs_pbs_nk.csv','itdt_acd4_vs_pbs_nk.csv','itdt_acd4_vs_itdt_nk.csv')
for(i in seq_along(files)) write.csv(topTable(fit,coef=i,number=Inf),file.path(out,files[i]))
write.csv(design,file.path(out,'design.csv'))
write.csv(logTPM,file.path(out,'logTPM.csv'))
beta <- fit0$coefficients[,startsWith(colnames(fit0$coefficients),'replicate'),drop=FALSE]
norm <- logTPM - beta %*% t(design[,startsWith(colnames(design),'replicate'),drop=FALSE])
write.csv(norm,file.path(out,'block_adjusted_logTPM.csv'))
groups <- list(PBS=c(1,4,7),ITDT=c(2,5,8),ITDT_aCD4=c(3,6,9))
avg <- sapply(groups,function(cols) rowMeans(norm[,cols,drop=FALSE]))
panels <- list(Activation=c('Icos','Fas','Klrg1','Tigit','Cd226','Cd69','Il2ra','Ly6a'),
  Cytotoxic_cargo=c('Gzmf','Gzme','Gzmg','Gzmd','Gzmc','Prf1','Gzma','Gzmb','Gzmk','Gzmm'),
  Checkpoints=c('Pdcd1','Ctla4','Lag3','Tigit','Havcr2'),Metabolism=c('Nos2','Sod2','Gys1','Pgk1'))
tt <- topTable(fit,coef=1,number=Inf)
panel_rows <- list()
for(p in names(panels)) {
  genes <- panels[[p]]
  stopifnot(all(genes %in% rownames(avg)))
  genes <- genes[order(tt[genes,'adj.P.Val'])]
  for(g in genes) {
    group_sd <- sd(avg[g,])
    for(j in seq_len(ncol(norm))) panel_rows[[length(panel_rows)+1]] <- data.frame(
      panel=p,gene=g,sample=colnames(norm)[j],condition=as.character(condition[j]),
      block=as.character(replicate[j]),log2TPM=logTPM[g,j],adjusted_log2TPM=norm[g,j],
      group_mean=avg[g,as.character(condition[j])],
      group_scaled=(avg[g,as.character(condition[j])]-mean(avg[g,]))/group_sd,
      library_scaled=(norm[g,j]-mean(avg[g,]))/group_sd)
  }
}
write.csv(do.call(rbind,panel_rows),file.path(out,'fixed_panels.csv'),row.names=FALSE)
pca <- prcomp(t(logTPM),center=TRUE,scale.=TRUE)
write.csv(data.frame(sample=rownames(pca$x),condition=condition,block=replicate,pca$x),file.path(out,'pca_scores.csv'),row.names=FALSE)
write.csv(data.frame(component=seq_along(pca$sdev),fraction=pca$sdev^2/sum(pca$sdev^2)),file.path(out,'pca_variance.csv'),row.names=FALSE)
capture.output(sessionInfo(),file=file.path(out,'R_session.txt'))
