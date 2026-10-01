# Nb3 source-informed bulk read-count reconstruction. Launched by 05_run_expression.py.
args <- commandArgs(trailingOnly = TRUE)
source(args[[1]])
suppressPackageStartupMessages(library(edgeR))
suppressPackageStartupMessages(library(limma))
dir.create(de_dir, recursive = TRUE, showWarnings = FALSE)
write_tsv <- function(x, path) write.table(x, path, sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
meta <- read.delim(file.path(cache, "crosswalk.tsv"), check.names = FALSE)
qc <- read.delim(file.path(out, "library_qc.tsv"), check.names = FALSE)
panels <- read.delim(panel_file, check.names = FALSE)
summaries <- list()
for (species in c("mouse", "human")) {
  message("Starting ", species)
  genes <- read.delim(file.path(cache, paste0(species, "_genes.tsv")), check.names = FALSE)
  libs <- read.delim(file.path(cache, paste0(species, "_libraries.tsv")), check.names = FALSE)$library
  n <- nrow(genes) * length(libs)
  con <- file(file.path(cache, paste0(species, "_counts.bin")), "rb")
  counts <- readBin(con, integer(), n = n, size = 4, endian = "little", signed = TRUE)
  close(con)
  stopifnot(length(counts) == n, !anyDuplicated(genes$ID), !anyDuplicated(libs))
  counts <- matrix(counts, nrow = nrow(genes), byrow = TRUE, dimnames = list(genes$ID, libs))
  m <- meta[match(libs, meta$library), ]
  q <- qc[qc$species == species, ]
  q <- q[match(libs, q$library), ]
  stopifnot(identical(m$library, libs), identical(q$library, libs), all(colSums(counts) == q$total_reads))
  keep <- q$detected_genes >= detection_cutoffs[[species]]
  m <- m[keep, ]
  counts <- counts[, keep, drop = FALSE]
  nonzero <- rowSums(counts) > 0
  genes <- genes[nonzero, ]
  y <- calcNormFactors(DGEList(counts[nonzero, , drop = FALSE]), method = "TMM")
  rm(counts); gc(verbose = FALSE)
  write_tsv(data.frame(species = species, library = m$library, target = m$target,
      plate = m$plate, total_reads = y$samples$lib.size, norm_factor = y$samples$norm.factors,
      effective_library_size = y$samples$lib.size * y$samples$norm.factors),
      file.path(out, paste0(species, "_normalization.tsv")))
  # Score only fixed source panels. Sum duplicated symbols on the CPM scale first.
  selected <- panels[panels$species == species, ]
  selected_rows <- genes$symbol %in% selected$gene
  symbol_cpm <- rowsum(cpm(y, log = FALSE)[selected_rows, , drop = FALSE],
      group = genes$symbol[selected_rows], reorder = FALSE)
  score_rows <- list(); availability <- list()
  for (program in unique(selected$program)) {
    required <- selected$gene[selected$program == program]
    present <- required %in% rownames(symbol_cpm)
    availability[[program]] <- data.frame(species = species, program = program,
        required_genes = paste(required, collapse = ";"), missing_genes = paste(required[!present], collapse = ";"), eligible = all(present))
    if (all(present)) score_rows[[program]] <- data.frame(species = species, library = m$library,
        target = m$target, plate = m$plate, program = program,
        score = colMeans(log2(symbol_cpm[required, , drop = FALSE] + panel_pseudocount)))
  }
  write_tsv(do.call(rbind, availability), file.path(out, paste0(species, "_panel_eligibility.tsv")))
  write_tsv(do.call(rbind, score_rows), file.path(out, paste0(species, "_panel_scores.tsv")))
  write_tsv(data.frame(gene = rownames(symbol_cpm), symbol_cpm, check.names = FALSE),
      file.path(cache, paste0(species, "_selected_symbol_cpm.tsv")))
  rm(symbol_cpm); gc(verbose = FALSE)
  targets <- sort(setdiff(unique(m$target), controls))
  species_summaries <- list()
  species_dir <- file.path(de_dir, species)
  dir.create(species_dir, showWarnings = FALSE)
  for (i in seq_along(targets)) {
    target <- targets[[i]]
    target_plates <- unique(m$plate[m$target == target])
    use <- m$target == target | (m$target %in% controls & m$plate %in% target_plates)
    design_data <- data.frame(plate = droplevels(factor(m$plate[use])), is_target = as.numeric(m$target[use] == target))
    nt <- sum(design_data$is_target); nc <- sum(1 - design_data$is_target)
    design <- if (nlevels(design_data$plate) > 1) model.matrix(~plate + is_target, design_data) else model.matrix(~is_target, design_data)
    df <- nrow(design) - qr(design)$rank
    eligible <- nt >= min_target && nc >= min_control && df >= min_df && qr(design)$rank == ncol(design)
    record <- data.frame(species = species, target = target, n_target = nt, n_control = nc,
      plates = paste(sort(target_plates), collapse = ";"), residual_df = df, eligible = eligible,
      fitted_genes = nrow(y), expression_pass_genes = NA_integer_, diagnostic_DE_genes = NA_integer_)
    if (eligible) {
      v <- voom(y[, use, keep.lib.sizes = TRUE], design, normalize.method = "none", plot = FALSE)
      fit <- eBayes(lmFit(v, design))
      tab <- topTable(fit, coef = "is_target", number = Inf, sort.by = "none", adjust.method = "BH")
      stopifnot(identical(rownames(tab), rownames(y)))
      tab <- data.frame(ID = rownames(tab), symbol = genes$symbol, tab[, c("logFC", "AveExpr", "t", "P.Value", "adj.P.Val")], row.names = NULL)
      record$expression_pass_genes <- sum(tab$AveExpr > min_AveExpr)
      record$diagnostic_DE_genes <- sum(tab$AveExpr > min_AveExpr & tab$adj.P.Val < diagnostic_fdr)
      dest <- gzfile(file.path(species_dir, paste0(target, ".tsv.gz")), "wt", compression = 1)
      write_tsv(tab, dest); close(dest)
    }
    species_summaries[[i]] <- record
    if (i %% 25 == 0) message(species, ": ", i, "/", length(targets), " targets")
  }
  summaries[[species]] <- do.call(rbind, species_summaries)
  write_tsv(summaries[[species]], file.path(out, paste0(species, "_DE_summary.tsv")))
  rm(y); gc(verbose = FALSE)
}
write_tsv(do.call(rbind, summaries), file.path(out, "DE_summary.tsv"))
capture.output(sessionInfo(), file = file.path(out, "R_session.txt"))
message("Nb3 expression reconstruction completed")
