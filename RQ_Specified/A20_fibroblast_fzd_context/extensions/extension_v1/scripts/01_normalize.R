args <- commandArgs(trailingOnly=TRUE)
base <- args[1]
suppressPackageStartupMessages(library(edgeR))
x <- read.delim(file.path(base, "cache/ng2019_expression.tsv"), check.names=FALSE)
counts <- as.matrix(x[,-1]); rownames(counts) <- x[[1]]
stopifnot(ncol(counts)==16, nrow(counts)==32734, !anyDuplicated(rownames(counts)), all(counts>=0), all(counts==floor(counts)))
y <- DGEList(counts=counts); y <- calcNormFactors(y, method="TMM")
effective <- y$samples$lib.size*y$samples$norm.factors
logvalue <- log2(cpm(y, normalized.lib.sizes=TRUE)+1)
write.table(data.frame(probe=rownames(logvalue),logvalue,check.names=FALSE),file.path(base,"cache/TMM_log2CPM.tsv"),sep="\t",quote=FALSE,row.names=FALSE)
write.table(data.frame(sample=colnames(counts),library_size=y$samples$lib.size,TMM_factor=y$samples$norm.factors,effective_library_size=effective),file.path(base,"tables/normalization.tsv"),sep="\t",quote=FALSE,row.names=FALSE)
sink(file.path(base,"reports/R_session.txt"));sessionInfo();sink()
cat("TMM normalized 32734 genes across 16 libraries; no treatment-effect fit.\n")
