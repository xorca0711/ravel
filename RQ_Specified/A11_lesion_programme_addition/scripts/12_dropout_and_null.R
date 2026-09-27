## C5c, post hoc: does the module still move once the injury-responsive genes are removed, and is
## the normalisation sensitivity a change of effect or a change of baseline.
##
## Two diagnostics an adversarial review showed were missing.
##
## 1. The A11 stress exclusion retains the canonical NF-kB and integrated-stress-response names, so
##    agreement between the primary and the stress-excluded variant cannot test stress dependence.
##    The actual test is to drop those genes and see whether the remainder moves.
## 2. The earlier normalisation comparison changed the pseudocount as well as the normalisation, and
##    it compared raw scores. A module score has an arbitrary zero that moves with the normalisation,
##    so the quantity to compare is the module's displacement from an abundance-matched random
##    background computed under the same normalisation.
##
## Declared post hoc. Changes no decision. The module, the instrument and the contract are untouched.
##
## Usage: Rscript c5c_dropout_and_null.R <repo> <data_root> <cache> <c3> <out>

args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 5)
repo <- normalizePath(args[1], winslash = "/")
data_root <- normalizePath(args[2], winslash = "/")
cache <- normalizePath(args[3], winslash = "/")
c3 <- normalizePath(args[4], winslash = "/")
out <- args[5]
.libPaths(c(file.path(data_root, "analysis/corrections/statistics/.tools/R-library"), .libPaths()))
suppressPackageStartupMessages(library(edgeR))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
if (file.exists(file.path(out, "dropout_and_null.tsv"))) stop("Refusing to overwrite")

NFKB <- c("TNF", "TNFAIP3", "RELB", "PTGS2", "LIF", "IL23A", "IL24", "MAFF", "TRIB1")
ISR <- c("ASNS", "CHAC1", "DDIT3", "SLC1A4", "SLC38A2", "ZFAND2A", "TP53INP1")
ARM <- "SCoV1"
NULL_SETS <- 2000L
set.seed(20260927)

units <- read.delim(file.path(c3, "units.tsv"), stringsAsFactors = FALSE)
x <- as.matrix(read.delim(gzfile(file.path(cache, "at2_pseudobulk_counts.tsv.gz")),
                          row.names = 1, check.names = FALSE))
stopifnot(identical(colnames(x), units$unit_id))
g <- read.delim(file.path(repo, "RQ_Specified/A11_lesion_programme_addition/tables/test_v2/human_module_genes.tsv"),
                stringsAsFactors = FALSE)
lesion <- g$gene[g$module == "lesion_specific"]
lesion <- intersect(lesion, rownames(x))

donors <- sort(unique(units$donor[units$arm == ARM]))

score_matrix <- function(use_tmm) {
  y <- DGEList(counts = x)
  if (use_tmm) y <- calcNormFactors(y, method = "TMM")
  cpm(y, log = TRUE, prior.count = 1)
}

paired_mean <- function(lc, genes) {
  genes <- intersect(genes, rownames(lc))
  if (!length(genes)) return(NA_real_)
  v <- colMeans(lc[genes, , drop = FALSE])
  mean(sapply(donors, function(d)
    v[[paste(d, ARM, "FCS", sep = "_")]] - v[[paste(d, "control", "FCS", sep = "_")]]))
}
paired_signs <- function(lc, genes) {
  genes <- intersect(genes, rownames(lc))
  v <- colMeans(lc[genes, , drop = FALSE])
  sum(sapply(donors, function(d)
    v[[paste(d, ARM, "FCS", sep = "_")]] - v[[paste(d, "control", "FCS", sep = "_")]]) > 0)
}

rows <- list(); nullrows <- list()
for (tmm in c(TRUE, FALSE)) {
  lc <- score_matrix(tmm)
  ## abundance-matched random background: bin all genes by mean log CPM, draw a set matching the
  ## module's bin profile, and take the same paired mean.
  ab <- rowMeans(lc)
  ## Restrict the background pool to genes with any count, because a matrix this sparse would
  ## otherwise put most quantile breaks on identical all-zero values and the bins would collapse.
  expressed <- rownames(lc)[rowSums(x) > 0]
  ab_e <- ab[expressed]
  breaks <- unique(quantile(ab_e, probs = seq(0, 1, length.out = 21), na.rm = TRUE))
  stopifnot(length(breaks) >= 5)
  bin <- setNames(cut(ab_e, breaks, include.lowest = TRUE, labels = FALSE), expressed)
  want <- table(bin[intersect(lesion, expressed)])
  pool <- split(names(bin), bin)
  draws <- numeric(NULL_SETS)
  for (i in seq_len(NULL_SETS)) {
    pick <- unlist(lapply(names(want), function(b) {
      cand <- setdiff(pool[[b]], lesion)
      sample(cand, min(length(cand), want[[b]]))
    }), use.names = FALSE)
    draws[i] <- paired_mean(lc, pick)
  }
  null_centre <- mean(draws, na.rm = TRUE)
  module <- paired_mean(lc, lesion)
  nullrows[[length(nullrows) + 1]] <- data.frame(
    normalisation = if (tmm) "TMM" else "none",
    module_paired_mean = round(module, 4),
    null_centre = round(null_centre, 4),
    null_sd = round(sd(draws, na.rm = TRUE), 4),
    displacement_from_null = round(module - null_centre, 4),
    null_sets = NULL_SETS, stringsAsFactors = FALSE)

  variants <- list(
    full_module = lesion,
    drop_nfkb = setdiff(lesion, NFKB),
    drop_isr = setdiff(lesion, ISR),
    drop_both = setdiff(lesion, c(NFKB, ISR)),
    only_nfkb_and_isr = intersect(lesion, c(NFKB, ISR)))
  for (nm in names(variants)) {
    rows[[length(rows) + 1]] <- data.frame(
      normalisation = if (tmm) "TMM" else "none",
      variant = nm, genes = length(intersect(variants[[nm]], rownames(lc))),
      paired_mean = round(paired_mean(lc, variants[[nm]]), 4),
      donors_positive = paired_signs(lc, variants[[nm]]),
      donors = length(donors), stringsAsFactors = FALSE)
  }
}
res <- do.call(rbind, rows); nul <- do.call(rbind, nullrows)
write.table(res, file.path(out, "dropout_and_null.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(nul, file.path(out, "null_displacement.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
writeLines(trimws(capture.output(sessionInfo()), which = "right"), file.path(out, "R_session_c5c.txt"))
print(res, row.names = FALSE)
cat("\n")
print(nul, row.names = FALSE)
