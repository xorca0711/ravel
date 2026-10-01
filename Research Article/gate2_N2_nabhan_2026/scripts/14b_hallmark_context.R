# Competitive rank enrichment of saved moderated t statistics; no gene DE refit.
suppressPackageStartupMessages(library(limma))
args <- commandArgs(trailingOnly=TRUE)
root <- args[1]; out <- args[2]
targets <- read.delim(file.path(out, "targets.tsv"), stringsAsFactors=FALSE)$target
results <- list(); coverage <- list(); universes <- list(); n <- 0L; k <- 0L; u <- 0L
for (species in c("mouse", "human")) {
  filename <- if (species == "mouse") "mh.all.v2024.1.Mm.symbols.gmt" else "h.all.v2024.1.Hs.symbols.gmt"
  lines <- strsplit(readLines(file.path(root, "raw_data/msigdb", filename)), "\t", fixed=TRUE)
  sets <- setNames(lapply(lines, function(z) unique(z[-c(1,2)])), vapply(lines, `[`, "", 1L))
  stopifnot(length(sets)==50L)
  for (target in targets) {
    path <- file.path(root, "raw_data/GSE307112/Nb3_v1/DE", species, paste0(target, ".tsv.gz"))
    d <- read.delim(gzfile(path), stringsAsFactors=FALSE, check.names=FALSE)
    d <- d[is.finite(d$t) & is.finite(d$AveExpr) & d$AveExpr>1.5 & !is.na(d$symbol) & nzchar(d$symbol), ]
    before <- nrow(d)
    d <- d[order(-d$AveExpr, d$ID), ]; d <- d[!duplicated(d$symbol), ]; d <- d[order(d$symbol), ]
    u <- u+1L; universes[[u]] <- data.frame(species=species, target=target, expressed_rows=before, unique_symbols=nrow(d), duplicate_rows_removed=before-nrow(d))
    index <- lapply(sets, function(s) which(d$symbol %in% s))
    cov <- data.frame(species=species, target=target, pathway=names(sets), set_genes=lengths(sets), mapped_genes=lengths(index), stringsAsFactors=FALSE)
    cov$coverage_fraction <- cov$mapped_genes/cov$set_genes
    cov$eligible <- cov$mapped_genes>=15 & cov$coverage_fraction>=0.5
    k <- k+1L; coverage[[k]] <- cov
    index <- index[cov$eligible]
    for (cor in c(0.01, 0.05)) {
      fit <- cameraPR(d$t, index=index, use.ranks=TRUE, inter.gene.cor=cor, sort=FALSE, directional=TRUE)
      n <- n+1L
      fit$pathway <- rownames(fit); fit$species <- species; fit$target <- target; fit$intergene_correlation <- cor
      fit$FDR_within_target <- fit$FDR; fit$FDR <- NULL
      results[[n]] <- fit
    }
  }
}
r <- do.call(rbind, results); rownames(r) <- NULL
r$FDR_global <- ave(r$PValue, r$intergene_correlation, FUN=function(x) p.adjust(x, method="BH"))
write.table(r, file.path(out, "hallmark_camera.tsv"), sep="\t", row.names=FALSE, quote=FALSE)
write.table(do.call(rbind, coverage), file.path(out, "hallmark_coverage.tsv"), sep="\t", row.names=FALSE, quote=FALSE)
write.table(do.call(rbind, universes), file.path(out, "hallmark_universes.tsv"), sep="\t", row.names=FALSE, quote=FALSE)
writeLines(capture.output(sessionInfo()), file.path(out, "R_session.txt"))
cat("Hallmark rows:", nrow(r), "\n")
