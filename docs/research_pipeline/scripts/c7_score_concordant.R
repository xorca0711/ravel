## C7: score the frozen contrast again on the identity-concordant pseudobulk.
##
## Same instrument, same module, same inherited floors. The only change is which cells enter each
## pseudobulk: only those where the author cluster label and the reference transfer agree. That
## restriction drops one unit below the inherited 50-cell floor, so the primary arm loses a donor and
## the test is run at three pairs.
##
## This is a sensitivity on a frozen primary, not a replacement for it. Both are reported.
##
## Usage: Rscript c7_score_concordant.R <repo> <data_root> <c6_dir> <cache> <out>

args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 5)
repo <- normalizePath(args[1], winslash = "/")
data_root <- normalizePath(args[2], winslash = "/")
c6 <- normalizePath(args[3], winslash = "/")
cache <- normalizePath(args[4], winslash = "/")
out <- args[5]
.libPaths(c(file.path(data_root, "analysis/corrections/statistics/.tools/R-library"), .libPaths()))
suppressPackageStartupMessages(library(edgeR))
source(file.path(repo, "RQ_Specified/A5_A11_shared_component_contract/scripts/paired_inference.R"))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
if (file.exists(file.path(out, "inference_concordant.tsv"))) stop("Refusing to overwrite")

units <- read.delim(file.path(c6, "units_concordant.tsv"), stringsAsFactors = FALSE)
x <- as.matrix(read.delim(gzfile(file.path(cache, "at2_concordant_pseudobulk_counts.tsv.gz")),
                          row.names = 1, check.names = FALSE))
stopifnot(identical(colnames(x), units$unit_id), all(x >= 0), !any(is.na(x)))
g <- read.delim(file.path(repo, "RQ_Specified/A11_lesion_programme_addition/tables/test_v2/human_module_genes.tsv"),
                stringsAsFactors = FALSE)
modules <- split(g$gene, g$module)

y <- calcNormFactors(DGEList(counts = x), method = "TMM")
lc <- cpm(y, log = TRUE, prior.count = 1)

sc <- list()
for (k in names(modules)) {
  present <- intersect(modules[[k]], rownames(lc))
  if (!length(present)) next
  sc[[k]] <- colMeans(lc[present, , drop = FALSE])
}

diff_for <- function(module, arm) {
  v <- sc[[module]]
  donors <- sort(units$donor[units$arm == arm])
  setNames(sapply(donors, function(d) {
    med <- units$medium[units$donor == d & units$arm == arm]
    v[[paste(d, arm, med, sep = "_")]] - v[[paste(d, "control", med, sep = "_")]]
  }), donors)
}

tests <- list(); pairs <- list()
for (arm in c("SCoV1", "SCoV2")) {
  if (!any(units$arm == arm)) next
  les <- diff_for("lesion_specific", arm)
  sh <- diff_for("shared_remodelling", arm)
  st <- diff_for("stress_excluded", arm)
  for (nm in names(les)) pairs[[length(pairs) + 1]] <- data.frame(
    arm = arm, donor = nm, lesion_specific = les[[nm]], shared_remodelling = sh[[nm]],
    stress_excluded = st[[nm]], beyond_shared = les[[nm]] - sh[[nm]], stringsAsFactors = FALSE)
  tests[[paste0(arm, "_primary_lesion")]] <- les
  tests[[paste0(arm, "_stress_excluded")]] <- st
  tests[[paste0(arm, "_beyond_shared")]] <- les - sh[names(les)]
}
z <- do.call(rbind, pairs)
write.table(z, file.path(out, "paired_differences_concordant.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

## The helper blanks its output when the 95 per cent interval is unattainable, which it is at these
## unit counts, so the exact quantities are also recorded directly.
rows <- list()
for (k in names(tests)) {
  d <- tests[[k]]
  w <- suppressWarnings(wilcox.test(d, mu = 0, exact = TRUE, conf.int = TRUE, conf.level = .95, tol.root = 1e-10))
  lt <- location_test(d)
  rows[[length(rows) + 1]] <- cbind(test = k, lt,
    exact_HL_direct = unname(w$estimate), exact_p_direct = w$p.value,
    attained_conf_level = attr(w$conf.int, "conf.level"),
    donors_positive = sum(d > 0), donors_total = length(d))
}
res <- do.call(rbind, rows)
write.table(res, file.path(out, "inference_concordant.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(cbind(units, library_size = y$samples$lib.size, TMM_factor = y$samples$norm.factors),
            file.path(out, "normalization_concordant.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
writeLines(trimws(capture.output(sessionInfo()), which = "right"), file.path(out, "R_session_c7.txt"))
print(res[, c("test", "n", "mean", "exact_HL_direct", "exact_p_direct", "donors_positive", "donors_total")],
      row.names = FALSE)
cat("\n")
print(z, row.names = FALSE)
