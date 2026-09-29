# Nb2 bulk v1: limma/voom adaptation under the source's unverified replicate assumption.
# Effects are library-level; p-values/intervals are explicitly conditional diagnostics.
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==3)
study <- normalizePath(args[1],winslash="/")
.libPaths(c(args[2], .libPaths()))
suppressPackageStartupMessages(library(limma))
suppressPackageStartupMessages(library(edgeR))
suppressPackageStartupMessages(library(jsonlite))
out <- file.path(study,"trials/bulk_v1")
contract <- fromJSON(file.path(out,"contract.json"),simplifyVector=FALSE)
stopifnot(!file.exists(file.path(out,"run_complete.json")))
dir.create(file.path(out,"tables"),showWarnings=FALSE)
dir.create(file.path(out,"figures"),showWarnings=FALSE)
tab <- function(x,name) write.table(x,file.path(out,"tables",name),sep="\t",row.names=FALSE,quote=FALSE,na="NA")
m <- read.delim(file.path(study,"metadata/samples.tsv"),check.names=FALSE)
x <- as.matrix(read.csv(gzfile(file.path(study,"raw/bulk_counts.csv.gz")),row.names=1,check.names=FALSE))
stopifnot(identical(colnames(x),m$accession),all(x>=0),all(x==floor(x)))
map <- read.delim(file.path(study,"raw/gene_mapping.tsv"),check.names=FALSE,na.strings="")
stopifnot(identical(rownames(x),map$gene_id))
labels <- unlist(contract$condition_labels)
m$arm <- factor(unname(labels[m$condition]),levels=c("withdraw48","withdraw24","Wnt","CHIR","Fzd5","Fzd6"))
design <- model.matrix(~0+arm,m);colnames(design)<-levels(m$arm)
stopifnot(qr(design)$rank==6)
keep <- rowSums(x>=10)>=3
d <- DGEList(x[keep,,drop=FALSE]);d<-calcNormFactors(d,method="TMM")
pdf(file.path(out,"figures/voom_diagnostic.pdf"));v<-voom(d,design,plot=TRUE);dev.off()
fit <- lmFit(v,design)
specs <- contract$contrasts
cm <- sapply(specs,function(z) {a<-rep(0,6);names(a)<-colnames(design);a[z[[1]]]<-1;a[z[[2]]]<- -1;a})
colnames(cm)<-names(specs)
fc <- eBayes(contrasts.fit(fit,cm),trend=FALSE,robust=FALSE)
annotation<-map[match(rownames(v$E),map$gene_id),]
effects<-do.call(rbind,lapply(seq_len(ncol(cm)),function(j){
 se<-sqrt(fc$s2.post)*fc$stdev.unscaled[,j];crit<-qt(.975,fc$df.total)
 data.frame(gene_id=rownames(v$E),symbol=annotation$symbol,contrast=colnames(cm)[j],
            log2FC=fc$coefficients[,j],SE=se,CI_low=fc$coefficients[,j]-crit*se,
            CI_high=fc$coefficients[,j]+crit*se,t=fc$t[,j],P=fc$p.value[,j],
            FDR=p.adjust(fc$p.value[,j],"BH"),mean_log2CPM=fc$Amean,
            inference="conditional_on_source_independence_assumption")
}))
effects$FDR_all_contrasts<-p.adjust(effects$P,"BH")
con<-gzfile(file.path(out,"tables/gene_effects.tsv.gz"),"wt")
write.table(effects,con,sep="\t",row.names=FALSE,quote=FALSE,na="NA");close(con)
summaries<-do.call(rbind,lapply(split(effects,effects$contrast),function(z){
 do.call(rbind,lapply(c(1,2),function(th){data.frame(contrast=z$contrast[1],absolute_log2FC_gt=th,
 up=sum(z$log2FC>th & z$FDR<.05),down=sum(z$log2FC< -th & z$FDR<.05),
 caption_raw_p001=sum(z$P<.001),caption_FDR001=sum(z$FDR<.001),tested_genes=nrow(z))}))
}));tab(summaries,"threshold_reconciliation.tsv")
normalization<-cbind(m,d$samples[,c("lib.size","norm.factors")]);tab(normalization,"normalization.tsv")
tab(data.frame(gene_id=rownames(v$E),symbol=annotation$symbol,v$E,check.names=FALSE),"normalized_log2CPM.tsv")
panels<-read.delim(file.path(study,"metadata/source_panel_membership.tsv"),check.names=FALSE)
panel_rows<-list();source_rows<-list();index<-1
for(p in unique(panels$panel)) {
 pp<-panels[panels$panel==p & panels$status=="resolved",];idx<-match(pp$gene_id,rownames(v$E));stopifnot(!anyNA(idx))
 e<-v$E[idx,,drop=FALSE];z<-t(scale(t(e)))
 for(i in seq_len(nrow(m))) {
  panel_rows[[index]]<-data.frame(panel=p,accession=m$accession[i],arm=m$arm[i],
     n_genes=nrow(e),mean_log2CPM=mean(e[,i]),mean_gene_z=mean(z[,i]));index<-index+1
 }
 source_rows[[p]]<-do.call(rbind,lapply(seq_len(nrow(e)),function(g) data.frame(panel=p,
    source_symbol=pp$source_symbol[g],gene_id=rownames(e)[g],accession=m$accession,
    arm=m$arm,log2CPM=as.numeric(e[g,]),gene_z=as.numeric(z[g,]))))
}
panel_scores<-do.call(rbind,panel_rows);tab(panel_scores,"panel_sample_scores.tsv")
tab(do.call(rbind,source_rows),"source_panel_expression.tsv")
source_ids<-panels$gene_id[panels$status=="resolved"]
leads<-c("Tgfb2","Zbtb16","Car2","Ca2","Crim1","Axin2","Il1r1","Fzd1","Fzd5","Fzd6","Lrp5","Lrp6")
tab(effects[effects$gene_id %in% source_ids | effects$symbol %in% leads,],"source_and_lead_effects.tsv")
tab(do.call(rbind,lapply(split(effects,effects$contrast),function(z) head(z[order(z$P,-abs(z$log2FC),z$gene_id),],100))),"top100_per_contrast.tsv")
# Four-gene source panel and Birc5-excluded sensitivity are separate measurements.
ix<-match(panels$gene_id[panels$panel=="Wnt" & panels$source_symbol!="Birc5"],rownames(v$E))
tab(data.frame(accession=m$accession,arm=m$arm,Wnt_without_Birc5_mean_log2CPM=colMeans(v$E[ix,,drop=FALSE])),"wnt_specificity_sensitivity.tsv")
# Transparent library-level uncertainty summaries, without treating genes as replicates.
panel_effects<-do.call(rbind,lapply(unique(panel_scores$panel),function(p){
 z<-panel_scores[panel_scores$panel==p,]
 do.call(rbind,lapply(names(specs),function(n){c<-specs[[n]];a<-z$mean_log2CPM[z$arm==c[[1]]];b<-z$mean_log2CPM[z$arm==c[[2]]]
 data.frame(panel=p,contrast=n,mean_difference=mean(a)-mean(b),min_pair_difference=min(outer(a,b,"-")),max_pair_difference=max(outer(a,b,"-")),n_first=length(a),n_second=length(b))}))
}));tab(panel_effects,"panel_effects.tsv")
# GO/Hallmark annotation: expressed unique-symbol universe, CAMERA accounts for gene correlation.
read_gmt<-function(path){z<-strsplit(readLines(path),"\t",fixed=TRUE);setNames(lapply(z,function(r)unique(r[-c(1,2)])),vapply(z,`[[`,"",1))}
sets<-c(read_gmt(file.path(args[3],"mh.all.v2024.1.Mm.symbols.gmt")),read_gmt(file.path(args[3],"m5.go.bp.v2024.1.Mm.symbols.gmt")))
ok<-tolower(as.character(annotation$symbol_unique))=="true" & !is.na(annotation$symbol);ev<-v$E[ok,,drop=FALSE];wv<-v$weights[ok,,drop=FALSE]
rownames(ev)<-rownames(wv)<-annotation$symbol[ok]
idx<-ids2indices(sets,rownames(ev),remove.empty=FALSE);idx<-idx[lengths(idx)>=15 & lengths(idx)<=500]
gene_sets<-do.call(rbind,lapply(seq_len(ncol(cm)),function(j){
 ans<-camera(ev,idx,design,contrast=cm[,j],weights=wv,inter.gene.cor=.01,sort=FALSE)
 data.frame(set=rownames(ans),contrast=colnames(cm)[j],ans,universe=nrow(ev),row.names=NULL)
}));gene_sets$FDR_all_contrasts<-p.adjust(gene_sets$PValue,"BH")
con<-gzfile(file.path(out,"tables/camera_all_sets.tsv.gz"),"wt");write.table(gene_sets,con,sep="\t",row.names=FALSE,quote=FALSE);close(con)
tab(do.call(rbind,lapply(split(gene_sets,gene_sets$contrast),function(z)head(z[order(z$PValue,z$set),],25))),"camera_top25_per_contrast.tsv")
# Independent predefined Hallmark panels: sensitivity to estimated residual correlation.
hall<-idx[grepl("^HALLMARK_",names(idx))]
sens<-do.call(rbind,lapply(seq_len(ncol(cm)),function(j){ans<-camera(ev,hall,design,contrast=cm[,j],weights=wv,inter.gene.cor=NA,sort=FALSE);data.frame(set=rownames(ans),contrast=colnames(cm)[j],ans,row.names=NULL)}))
tab(sens,"hallmark_estimated_correlation.tsv")
pc<-prcomp(t(v$E[order(apply(v$E,1,var),decreasing=TRUE)[seq_len(min(2000,nrow(v$E)))],]),center=TRUE,scale.=FALSE)
tab(data.frame(accession=m$accession,arm=m$arm,PC1=pc$x[,1],PC2=pc$x[,2]),"pca_coordinates.tsv")
record<-list(finished_utc=format(Sys.time(),tz="UTC",usetz=TRUE),R=R.version.string,
 limma=as.character(packageVersion("limma")),edgeR=as.character(packageVersion("edgeR")),
 input_genes=nrow(x),tested_genes=nrow(v$E),design_rank=qr(design)$rank,residual_df=nrow(design)-qr(design)$rank,
 gene_sets=length(idx),source_panel_resolved=19,source_panel_unresolved="Crim2",
 interpretation="Adapted assay reproduction; model inference conditional on unverified source replicate independence; not equivalence or functional validation",
 pca_variance=pc$sdev[1:2]^2/sum(pc$sdev^2))
write_json(record,file.path(out,"run_complete.json"),pretty=TRUE,auto_unbox=TRUE)
cat("Bulk v1 complete:",nrow(v$E),"genes;",ncol(cm),"contrasts;",length(idx),"GO/Hallmark sets\n")
