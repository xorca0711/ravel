## C6: rebuild the type 2 pseudobulk restricted to identity-concordant cells, and audit purity.
##
## An adversarial review of C5 found that the per-donor lesion difference is rank-identical to the
## per-donor shift in the share of counts coming from cells the object's own reference transfer does
## not call type 2. That confound cannot be separated from programme induction in the C4 pseudobulk,
## because C3 gated gene coverage, pair eligibility and integer counts but never cell identity.
##
## This builds a second pseudobulk over cells where the author cluster label and the reference
## transfer agree, and records per-unit purity either way. It applies the inherited 50-cell floor to
## the restricted counts, so a unit that only cleared the floor on mixed cells becomes ineligible and
## is reported as such.
##
## No score is computed here. The module and the instrument are untouched.
##
## Usage: Rscript c6_identity_concordant_pseudobulk.R <repo> <data_root> <rds> <out> <cache>

args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 5)
repo <- normalizePath(args[1], winslash = "/")
data_root <- normalizePath(args[2], winslash = "/")
rds <- normalizePath(args[3], winslash = "/")
out <- args[4]
cache <- args[5]
.libPaths(c(file.path(data_root, "analysis/corrections/statistics/.tools/R-library"), .libPaths()))
suppressPackageStartupMessages(library(Matrix))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
dir.create(cache, recursive = TRUE, showWarnings = FALSE)
if (file.exists(file.path(out, "purity.tsv"))) stop("Refusing to overwrite the C6 outputs")

CELL_FLOOR <- 50L
AUTHOR_LABEL <- "AT2"
TRANSFER_LABEL <- "Alveolar Epithelial Type 2"
ARMS <- c("SCoV1", "SCoV2")

cat("Reading the object\n"); flush.console()
o <- readRDS(rds)
m <- attr(o, "meta.data")
counts <- attr(attr(o, "assays")[["RNA"]], "counts")
stopifnot(identical(colnames(counts), rownames(m)))

ex <- m$origin == "explant"
author <- ex & m$cluster == AUTHOR_LABEL
concordant <- author & m$predicted.id == TRANSFER_LABEL

## ---- purity, per unit, on the cells C4 actually used ---------------------------------------
u <- read.delim(file.path(repo, "docs/research_pipeline/2026-09-27-execution/c3/units.tsv"),
                stringsAsFactors = FALSE)
lib <- Matrix::colSums(counts)
rows <- list()
for (i in seq_len(nrow(u))) {
  sel <- author & m$donor == u$donor[i] & m$infect == u$arm[i] & m$protocol == u$medium[i]
  con <- sel & concordant
  tot <- sum(lib[sel])
  transfer <- table(m$predicted.id[sel])
  top_foreign <- names(sort(transfer[names(transfer) != TRANSFER_LABEL], decreasing = TRUE))[1]
  rows[[length(rows) + 1]] <- data.frame(
    unit_id = u$unit_id[i], donor = u$donor[i], arm = u$arm[i], medium = u$medium[i],
    cells_author = sum(sel), cells_concordant = sum(con),
    cell_share_concordant = round(sum(con) / sum(sel), 4),
    count_share_concordant = round(sum(lib[con]) / tot, 4),
    largest_foreign_transfer_label = if (is.na(top_foreign)) "none" else top_foreign,
    clears_floor_concordant = sum(con) >= CELL_FLOOR,
    stringsAsFactors = FALSE)
}
purity <- do.call(rbind, rows)
write.table(purity, file.path(out, "purity.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
print(purity, row.names = FALSE)

## ---- the restricted pseudobulk --------------------------------------------------------------
keep <- purity[purity$clears_floor_concordant, ]
mat <- matrix(0L, nrow = nrow(counts), ncol = nrow(keep),
              dimnames = list(rownames(counts), keep$unit_id))
for (i in seq_len(nrow(keep))) {
  sel <- concordant & m$donor == keep$donor[i] & m$infect == keep$arm[i] & m$protocol == keep$medium[i]
  mat[, i] <- as.integer(round(Matrix::rowSums(counts[, sel, drop = FALSE])))
}
stopifnot(all(mat >= 0), !any(is.na(mat)))
gz <- gzfile(file.path(cache, "at2_concordant_pseudobulk_counts.tsv.gz"), "wt")
write.table(cbind(gene = rownames(mat), mat), gz, sep = "\t", row.names = FALSE, quote = FALSE)
close(gz)
units_out <- keep[, c("unit_id", "donor", "arm", "medium")]
units_out$cells <- keep$cells_concordant
write.table(units_out, file.path(out, "units_concordant.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

## which pairs survive the floor on concordant cells
surviving <- character()
for (a in ARMS) {
  for (d in unique(keep$donor)) {
    if (any(keep$arm == a & keep$donor == d) && any(keep$arm == "control" & keep$donor == d)) {
      surviving <- c(surviving, sprintf("%s:%s", a, d))
    }
  }
}
writeLines(c(
  sprintf("author-labelled type 2 explant cells: %d", sum(author)),
  sprintf("of which the reference transfer also calls type 2: %d (%.4f)", sum(concordant), sum(concordant)/sum(author)),
  sprintf("units retained at the inherited %d-cell floor on concordant cells: %d of %d", CELL_FLOOR, nrow(keep), nrow(u)),
  sprintf("units dropped: %s", paste(setdiff(u$unit_id, keep$unit_id), collapse = ", ")),
  sprintf("surviving pairs: %s", paste(surviving, collapse = ", "))),
  file.path(out, "restriction_summary.txt"))
writeLines(trimws(capture.output(sessionInfo()), which = "right"), file.path(out, "R_session.txt"))
cat("\n"); cat(readLines(file.path(out, "restriction_summary.txt")), sep = "\n"); cat("\n")
