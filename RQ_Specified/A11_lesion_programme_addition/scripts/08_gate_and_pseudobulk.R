## C3: gate the frozen A11 contract against this object, then build the type 2 pseudobulk.
##
## Applies the gates the contract names before any score exists: module gene coverage in this
## object's RNA index, and a recomputation of the eligible pair list that refuses on any
## disagreement with the contract. Then sums raw counts over author-annotated type 2 explant
## cells, per donor and arm and medium, across all genes because the normalisation needs the
## whole library.
##
## No score is computed here. No gene list is derived from this cohort.
##
## Usage: Rscript c3_gate_and_pseudobulk.R <repo> <data_root> <rds> <out> <cache>

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
if (file.exists(file.path(out, "gate_report.json"))) stop("Refusing to overwrite the C3 gate")

contract_path <- file.path(repo, "RQ_Specified/A11_lesion_programme_addition/config/gse198864_acute_injury_contract.json")
stopifnot(file.exists(contract_path))
contract_text <- paste(readLines(contract_path, warn = FALSE), collapse = "\n")
## Read the few fields we need without a JSON package.
grab_num <- function(key) as.numeric(sub(sprintf('.*"%s"\\s*:\\s*([0-9.]+).*', key), "\\1", contract_text))
CELL_FLOOR <- grab_num("cell_floor_per_arm")
UNIT_FLOOR <- grab_num("unit_floor")
COVERAGE_GATE <- grab_num("gene_coverage_gate")
stopifnot(CELL_FLOOR == 50, UNIT_FLOOR == 3, COVERAGE_GATE == 0.7)

modules_path <- file.path(repo, "RQ_Specified/A11_lesion_programme_addition/tables/test_v2/human_module_genes.tsv")
g <- read.delim(modules_path, stringsAsFactors = FALSE)
modules <- split(g$gene, g$module)
needed <- c("lesion_specific", "stress_excluded", "shared_remodelling")
stopifnot(all(needed %in% names(modules)))

cat("Reading the object\n"); flush.console()
o <- readRDS(rds)
m <- attr(o, "meta.data")
assays <- attr(o, "assays")
counts <- attr(assays[["RNA"]], "counts")
stopifnot(is.data.frame(m), identical(colnames(counts), rownames(m)))

## ---- gate 1: module gene coverage in this object -------------------------------------------
index <- rownames(counts)
cov <- do.call(rbind, lapply(names(modules), function(k) {
  present <- intersect(modules[[k]], index)
  data.frame(module = k, genes = length(modules[[k]]), present = length(present),
             fraction = length(present) / length(modules[[k]]), stringsAsFactors = FALSE)
}))
write.table(cov, file.path(out, "module_coverage.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
primary_cov <- cov$fraction[cov$module == "lesion_specific"]
cat(sprintf("lesion_specific coverage: %d of %d = %.4f\n",
            cov$present[cov$module == "lesion_specific"],
            cov$genes[cov$module == "lesion_specific"], primary_cov)); flush.console()

## ---- gate 2: recompute the eligible pairs --------------------------------------------------
ex <- m$origin == "explant"
at2 <- ex & m$cluster == "AT2"
key <- paste(m$donor, m$infect, m$protocol, sep = "|")
at2_counts <- table(key[at2])
cellcount <- function(d, a, p) {
  k <- paste(d, a, p, sep = "|")
  if (k %in% names(at2_counts)) as.integer(at2_counts[[k]]) else 0L
}
donors <- sort(unique(m$donor[ex]))
arms <- c("SCoV1", "SCoV2", "MERS", "H3N2")
elig <- list()
for (a in arms) for (d in donors) for (p in c("BSA", "FCS")) {
  ni <- cellcount(d, a, p); nc <- cellcount(d, "control", p)
  if (ni > 0 && nc > 0) {
    elig[[length(elig) + 1]] <- data.frame(arm = a, donor = d, medium = p,
      at2_infected = ni, at2_control = nc, smaller = min(ni, nc),
      eligible = min(ni, nc) >= CELL_FLOOR, stringsAsFactors = FALSE)
  }
}
elig <- do.call(rbind, elig)
write.table(elig, file.path(out, "pair_eligibility.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
tally <- tapply(elig$eligible, elig$arm, sum)
cat("eligible pairs by arm:", paste(sprintf("%s=%d", names(tally), as.integer(tally)), collapse = " "), "\n")
expected <- c(SCoV1 = 4L, SCoV2 = 3L, MERS = 2L, H3N2 = 1L)
got <- sapply(names(expected), function(a) as.integer(sum(elig$eligible[elig$arm == a])))
if (!identical(got, expected)) {
  write.table(data.frame(arm = names(expected), contract = as.integer(expected), recomputed = got),
              file.path(out, "eligibility_disagreement.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
  stop("Eligible pair counts disagree with the frozen contract; refusing to build the pseudobulk")
}
if (primary_cov < COVERAGE_GATE) stop(sprintf("lesion_specific coverage %.4f below the %.2f gate", primary_cov, COVERAGE_GATE))

## ---- build the pseudobulk over all genes ---------------------------------------------------
primary_arm <- "SCoV1"; secondary_arm <- "SCoV2"
wanted <- elig[elig$eligible & elig$arm %in% c(primary_arm, secondary_arm), ]
units <- unique(rbind(
  data.frame(donor = wanted$donor, arm = wanted$arm, medium = wanted$medium, stringsAsFactors = FALSE),
  data.frame(donor = wanted$donor, arm = "control", medium = wanted$medium, stringsAsFactors = FALSE)))
units$unit_id <- paste(units$donor, units$arm, units$medium, sep = "_")
units <- units[order(units$unit_id), ]
mat <- matrix(0L, nrow = nrow(counts), ncol = nrow(units),
              dimnames = list(index, units$unit_id))
units$cells <- NA_integer_
for (i in seq_len(nrow(units))) {
  sel <- at2 & m$donor == units$donor[i] & m$infect == units$arm[i] & m$protocol == units$medium[i]
  stopifnot(sum(sel) > 0)
  mat[, i] <- as.integer(round(Matrix::rowSums(counts[, sel, drop = FALSE])))
  units$cells[i] <- sum(sel)
}
stopifnot(all(mat >= 0), !any(is.na(mat)))
gz <- gzfile(file.path(cache, "at2_pseudobulk_counts.tsv.gz"), "wt")
write.table(cbind(gene = rownames(mat), mat), gz, sep = "\t", row.names = FALSE, quote = FALSE)
close(gz)
write.table(units, file.path(out, "units.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

report <- c(
  sprintf('{"task":"C3","scope":"gates and pseudobulk only; no score computed",'),
  sprintf('"contract_sha_note":"read from %s",', "RQ_Specified/A11_lesion_programme_addition/config/gse198864_acute_injury_contract.json"),
  sprintf('"rds":"%s",', basename(rds)),
  sprintf('"genes_in_index":%d,', length(index)),
  sprintf('"lesion_specific_present":%d,"lesion_specific_fraction":%.6f,',
          cov$present[cov$module == "lesion_specific"], primary_cov),
  sprintf('"coverage_gate":%.2f,"coverage_gate_passed":%s,', COVERAGE_GATE, tolower(as.character(primary_cov >= COVERAGE_GATE))),
  sprintf('"eligible_pairs":{"SCoV1":%d,"SCoV2":%d,"MERS":%d,"H3N2":%d},', got[["SCoV1"]], got[["SCoV2"]], got[["MERS"]], got[["H3N2"]]),
  sprintf('"eligibility_matches_contract":true,'),
  sprintf('"primary_arm":"%s","secondary_arm":"%s",', primary_arm, secondary_arm),
  sprintf('"pseudobulk_units":%d,"pseudobulk_genes":%d,', nrow(units), nrow(mat)),
  sprintf('"total_at2_cells_used":%d,', sum(units$cells)),
  sprintf('"scores_computed":false}'))
writeLines(paste(report, collapse = "\n"), file.path(out, "gate_report.json"))
writeLines(trimws(capture.output(sessionInfo()), which = "right"), file.path(out, "R_session.txt"))
cat("units:", nrow(units), " genes:", nrow(mat), " AT2 cells used:", sum(units$cells), "\n")
print(units, row.names = FALSE)
