## C4: score the frozen A11 acute-injury contrast on the type 2 pseudobulk.
##
## Reuses the A11 instrument unchanged: edgeR TMM, log CPM at prior count 1, the unweighted
## module mean, and the shared exact paired location test. It reads only the small pseudobulk
## C3 wrote, so it needs no memory headroom and never touches the count object.
##
## Module genes are intersected with this object's index and the number used is recorded, because
## coverage here is not the coverage the A11 Kim test had.
##
## Usage: Rscript c4_score_a11_acute.R <repo> <data_root> <c3_dir> <cache> <out>

args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 5)
repo <- normalizePath(args[1], winslash = "/")
data_root <- normalizePath(args[2], winslash = "/")
c3 <- normalizePath(args[3], winslash = "/")
cache <- normalizePath(args[4], winslash = "/")
out <- args[5]
.libPaths(c(file.path(data_root, "analysis/corrections/statistics/.tools/R-library"), .libPaths()))
suppressPackageStartupMessages(library(edgeR))
source(file.path(repo, "RQ_Specified/A5_A11_shared_component_contract/scripts/paired_inference.R"))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
if (file.exists(file.path(out, "inference.tsv"))) stop("Refusing to overwrite the C4 scores")

## The gate must have passed before any score exists.
gate <- paste(readLines(file.path(c3, "gate_report.json"), warn = FALSE), collapse = " ")
stopifnot(grepl('"coverage_gate_passed":true', gate), grepl('"eligibility_matches_contract":true', gate))
stopifnot(grepl('"scores_computed":false', gate))
PRIMARY_ARM <- "SCoV1"; SECONDARY_ARM <- "SCoV2"

units <- read.delim(file.path(c3, "units.tsv"), stringsAsFactors = FALSE)
x <- as.matrix(read.delim(gzfile(file.path(cache, "at2_pseudobulk_counts.tsv.gz")),
                          row.names = 1, check.names = FALSE))
stopifnot(identical(colnames(x), units$unit_id), all(x >= 0), !any(is.na(x)))

g <- read.delim(file.path(repo, "RQ_Specified/A11_lesion_programme_addition/tables/test_v2/human_module_genes.tsv"),
                stringsAsFactors = FALSE)
modules <- split(g$gene, g$module)

y <- calcNormFactors(DGEList(counts = x), method = "TMM")
lc <- cpm(y, log = TRUE, prior.count = 1)

used <- list(); scores <- list()
for (k in names(modules)) {
  present <- intersect(modules[[k]], rownames(lc))
  used[[length(used) + 1]] <- data.frame(module = k, genes = length(modules[[k]]),
                                         used = length(present),
                                         fraction = length(present) / length(modules[[k]]),
                                         stringsAsFactors = FALSE)
  if (!length(present)) next
  v <- colMeans(lc[present, , drop = FALSE])
  scores[[length(scores) + 1]] <- cbind(units, module = k, score = unname(v))
}
used <- do.call(rbind, used)
scores <- do.call(rbind, scores)
write.table(used, file.path(out, "module_genes_used.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(scores, file.path(out, "scores.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

## Per-donor paired differences, infected minus the control in the same medium.
diff_for <- function(module, arm) {
  s <- scores[scores$module == module, ]
  donors <- sort(unique(s$donor[s$arm == arm]))
  vals <- sapply(donors, function(d) {
    a <- s$score[s$donor == d & s$arm == arm]
    med <- s$medium[s$donor == d & s$arm == arm]
    b <- s$score[s$donor == d & s$arm == "control" & s$medium == med]
    stopifnot(length(a) == 1, length(b) == 1)
    a - b
  })
  setNames(as.numeric(vals), donors)
}

pairs <- list(); tests <- list()
for (arm in c(PRIMARY_ARM, SECONDARY_ARM)) {
  les <- diff_for("lesion_specific", arm)
  sh <- diff_for("shared_remodelling", arm)
  st <- diff_for("stress_excluded", arm)
  for (nm in names(les)) {
    pairs[[length(pairs) + 1]] <- data.frame(arm = arm, donor = nm,
      lesion_specific = les[[nm]], shared_remodelling = sh[[nm]],
      stress_excluded = st[[nm]], beyond_shared = les[[nm]] - sh[[nm]],
      stringsAsFactors = FALSE)
  }
  tests[[paste0(arm, "_primary_lesion")]] <- les
  tests[[paste0(arm, "_stress_excluded")]] <- st
  tests[[paste0(arm, "_beyond_shared")]] <- les - sh[names(les)]
}
z <- do.call(rbind, pairs)
write.table(z, file.path(out, "paired_differences.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

res <- do.call(rbind, lapply(names(tests), function(k) cbind(test = k, location_test(tests[[k]]))))
## The primary carries the decision; Benjamini-Hochberg covers the secondaries only.
primary_row <- paste0(PRIMARY_ARM, "_primary_lesion")
res$is_primary <- res$test == primary_row
res$q_secondary <- NA_real_
sec <- !res$is_primary
res$q_secondary[sec] <- p.adjust(ifelse(is.finite(res$p_exact[sec]), res$p_exact[sec], 1), "BH")
res$donors_positive <- sapply(names(tests), function(k) sum(tests[[k]] > 0))
res$donors_total <- sapply(names(tests), function(k) length(tests[[k]]))
write.table(res, file.path(out, "inference.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(cbind(units, library_size = y$samples$lib.size, TMM_factor = y$samples$norm.factors),
            file.path(out, "normalization.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

d <- tests[[primary_row]]
loo <- data.frame(omitted_donor = names(d), remaining_n = length(d) - 1,
                  remaining_mean = sapply(seq_along(d), function(j) mean(d[-j])))
write.table(loo, file.path(out, "omission_diagnostics.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
writeLines(trimws(capture.output(sessionInfo()), which = "right"), file.path(out, "R_session.txt"))

print(used, row.names = FALSE)
cat("\n")
print(res[, c("test", "n", "mean", "HL", "low", "high", "p_exact", "exact_available",
              "direction", "magnitude", "donors_positive", "donors_total")], row.names = FALSE)
