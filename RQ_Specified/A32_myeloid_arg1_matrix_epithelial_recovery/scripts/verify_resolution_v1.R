# Independent native-R arithmetic from original YoungD14 MatrixMarket counts.
suppressPackageStartupMessages(library(Matrix))
a<-commandArgs(TRUE);stopifnot(length(a)==3L)
rawdir<-a[1];out<-a[2];metadata<-a[3]
prefix<-file.path(rawdir,"GSM7454030_YoungD14_")
x<-readMM(gzfile(paste0(prefix,"matrix.mtx.gz")))
bc<-sub("-.*","",read.delim(gzfile(paste0(prefix,"barcodes.tsv.gz")),header=FALSE)[[1]])
ft<-read.delim(gzfile(paste0(prefix,"features.tsv.gz")),header=FALSE)
m<-read.delim(metadata,check.names=FALSE,stringsAsFactors=FALSE)
e<-read.delim(file.path(out,"mouse_expression.tsv"),check.names=FALSE,stringsAsFactors=FALSE)
c<-read.delim(file.path(out,"condition_contrasts.tsv"),check.names=FALSE,stringsAsFactors=FALSE)
m<-m[grepl("^Young_D14\\.",m$cell_id),]; rawbc<-sub("^Young_D14\\.","",m$cell_id)
col<-match(rawbc,bc);stopifnot(!anyNA(col),!anyDuplicated(col))
ct<-as.numeric(colSums(x));stopifnot(identical(ct[col],as.numeric(m$nCount_RNA)))
y<-e[e$capture=="YoungD14",];checked<-0L
for(i in seq_len(nrow(y))) {
 r<-y[i,];state<-if(r$state=="AM_all") c("AM1","AM2","AM3","Prolif. AM") else r$state
 ix<-col[m$mice==r$mouse & m$celltype %in% state]
 gi<-which(ft[[2]]==r$gene);stopifnot(length(gi)==1L)
 stopifnot(sum(x[gi,ix,drop=FALSE])==r$gene_UMI,sum(ct[ix])==r$total_RNA_UMI,length(ix)==r$n_cells,sum(x[gi,ix,drop=FALSE]>0)==r$positive_cells)
 if(length(ix)>=10L) stopifnot(abs(log2(1+1e6*r$gene_UMI/sum(ct[ix]))-r$log2_CPM_plus1)<1e-10)
 else stopifnot(is.na(r$log2_CPM_plus1))
 checked<-checked+1L
}
ci_checked<-0L
for(i in seq_len(nrow(c))) {
 r<-c[i,];z<-e[e$capture==r$capture & e$state==r$state & e$gene==r$gene & e$n_cells>=10L,]
 v1<-z$log2_CPM_plus1[z$condition=="Bleo"];v0<-z$log2_CPM_plus1[z$condition=="PBS"]
 ok<-length(v1)==3L && length(v0)==3L
 stopifnot(ok==as.logical(r$estimated),length(v1)==r$n_BLM,length(v0)==r$n_PBS)
 if(ok) {
  est<-mean(v1)-mean(v0)
  stopifnot(abs(est-r$effect_log2CPM)<1e-10)
  if(var(v1)+var(v0)==0) stopifnot(is.na(r$lower95),is.na(r$upper95),is.na(r$welch_df),r$interval_status=="unestimated: zero observed variance")
  else {
   ci<-as.numeric(t.test(v1,v0,var.equal=FALSE)$conf.int)
   stopifnot(max(abs(ci-c(r$lower95,r$upper95)))<1e-9)
  }
  ci_checked<-ci_checked+1L
 } else stopifnot(is.na(r$effect_log2CPM))
}
writeLines(c("PASS",paste("YoungD14 original-matrix gene/state/mouse rows",checked),paste("All-capture Welch intervals",ci_checked),paste("All planned contrast eligibility rows",nrow(c)),"Original source MatrixMarket read by native R/Matrix; all YoungD14 retained-cell UMI totals exact.","Same-data numerical verification, not biological replication."),file.path(out,"independent_verification.txt"))
cat("Independent R verification passed:",checked,"original-matrix rows;",ci_checked,"intervals\n")
