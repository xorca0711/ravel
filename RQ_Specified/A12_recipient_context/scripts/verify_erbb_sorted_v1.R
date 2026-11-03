args <- commandArgs(trailingOnly=TRUE)
suppressPackageStartupMessages(library(Matrix))
base <- args[1]
prefix <- 'GSM4522986_HT280pos'
genes <- read.delim(gzfile(file.path(base, paste0(prefix, '_genes.tsv.gz'))), header=FALSE, stringsAsFactors=FALSE)
barcodes <- readLines(gzfile(file.path(base, paste0(prefix, '_barcodes.tsv.gz'))))
triplet <- readMM(gzfile(file.path(base, paste0(prefix, '_matrix.mtx.gz'))))
m <- as(triplet, 'CsparseMatrix')
stopifnot(length(m@x) == length(triplet@x), all(m@x > 0), all(m@x == floor(m@x)))
rm(triplet)
invisible(gc())
stopifnot(nrow(m) == nrow(genes), ncol(m) == length(barcodes), !anyDuplicated(barcodes))
idx4 <- which(genes$V2 == 'ERBB4')
idx2 <- which(genes$V2 == 'ERBB2')
stopifnot(length(idx4) == 1, length(idx2) == 1,
 genes$V1[idx4] == 'ENSG00000178568', genes$V1[idx2] == 'ENSG00000141736')
total <- colSums(m)
features <- colSums(m > 0)
mt <- colSums(m[grepl('^MT-', genes$V2), , drop=FALSE])
qc <- total > 0 & features >= 200 & features <= 6000 & mt <= total / 10
result <- data.frame(barcode=barcodes, full_rna_umi=total, detected_features=features,
 mitochondrial_umi=mt, ERBB4_umi=as.numeric(m[idx4, ]), ERBB2_umi=as.numeric(m[idx2, ]),
 operational_qc=as.integer(qc))
write.csv(result, args[2], row.names=FALSE, quote=TRUE)
cat(R.version.string, '; Matrix ', as.character(packageVersion('Matrix')), '\n', sep='')
