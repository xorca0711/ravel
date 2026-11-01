args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args) == 2)
.libPaths(c(args[2], .libPaths()))
stopifnot(requireNamespace("edgeR", quietly=TRUE))
stopifnot(as.character(packageVersion("edgeR")) == "4.10.5")
x <- as.matrix(read.csv(args[1], row.names=1, check.names=FALSE))
stopifnot(all(is.finite(x)), all(x >= 0), all(x == floor(x)), !anyDuplicated(rownames(x)))
libraries <- c("PBS_1","PBS_2","LH5_1","LH5_2","LH30_1","LH30_2")
stopifnot(identical(colnames(x), libraries))
views <- c("full", paste0("omit_", libraries))
result <- list()
for (view in views) {
  omitted <- if (view == "full") "" else sub("^omit_", "", view)
  keep <- libraries != omitted
  y <- edgeR::DGEList(counts=x[,keep,drop=FALSE])
  y <- edgeR::calcNormFactors(y, method="TMM", refColumn=NULL,
                             logratioTrim=0.3, sumTrim=0.05,
                             doWeighting=TRUE, Acutoff=-1e10)
  result[[view]] <- data.frame(view=view, library=colnames(y),
    library_size=y$samples$lib.size, tmm_factor=y$samples$norm.factors,
    effective_library_size=y$samples$lib.size*y$samples$norm.factors,
    R_version=as.character(getRversion()), edgeR_version=as.character(packageVersion("edgeR")))
}
write.csv(do.call(rbind,result), stdout(), row.names=FALSE, quote=FALSE)
