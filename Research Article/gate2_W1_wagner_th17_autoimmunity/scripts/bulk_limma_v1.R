# Source-aligned, outcome-exposed reconstruction; not the authors' exact pipeline.
args <- commandArgs(trailingOnly=TRUE); out <- args[1]
suppressPackageStartupMessages({library(limma);library(edgeR);library(jsonlite)})
stopifnot(as.character(packageVersion('limma'))=='3.68.5',as.character(packageVersion('edgeR'))=='4.10.5')
write_tsv <- function(x,name) { con <- if(grepl('gz$',name)) gzfile(file.path(out,name),'wt') else file.path(out,name); write.table(x,con,sep='\t',row.names=FALSE,quote=FALSE); if(inherits(con,'connection'))close(con) }
meta <- read.delim('analysis/research/runs/wg_bulk_qualification_v1/library_design.tsv',check.names=FALSE)
map <- read.delim('analysis/research/runs/wg_bulk_qualification_v1/source_sample_map.tsv',check.names=FALSE)
all_results <- list(); summaries <- list(); partitions <- list(); pcs <- list(); animal_programs <- list(); inventories <- list()
for(series in c('GSE162300','GSE162382')) {
 stem <- if(series=='GSE162300')'DFMO_RNA' else 'DFMO_JMJD3'
 raw <- read.csv(gzfile(paste0('raw_data/wagner_r3_20261004/',series,'_',stem,'_est_counts.csv.gz')),row.names=1,check.names=FALSE)
 m <- meta[meta$series==series,];m <- m[order(m$library_id),]; sm <- map[map$series==series,]
 counts <- sapply(m$library_id,function(id) rowSums(raw[,sm$source_title[sm$library_id==id],drop=FALSE]))
 rownames(counts)<-rownames(raw);stopifnot(all(is.finite(counts)),all(counts>=0),all(colSums(counts)>0))
 # Fixed abundance screen, independent of treatment effects: >=1 CPM in >=3 libraries.
 keep <- rowSums(cpm(counts)>=1)>=3
 y <- normLibSizes(DGEList(counts[keep,,drop=FALSE]),method='TMM')
 animals <- sort(unique(m$animal_id));cells <- sort(unique(m$cell_type)); genos <- sort(unique(m$genotype))
 design <- sapply(animals,function(a)as.numeric(m$animal_id==a));colnames(design)<-paste0('animal_',animals)
 for(g in genos)for(c in setdiff(cells,'Th17n')) { n<-paste('baseline',g,c,sep='_');design<-cbind(design,as.numeric(m$genotype==g & m$cell_type==c));colnames(design)[ncol(design)]<-n }
 for(g in genos)for(c in cells) { n<-paste('DFMO',g,c,sep='_');design<-cbind(design,as.numeric(m$genotype==g & m$cell_type==c & m$treatment=='DFMO'));colnames(design)[ncol(design)]<-n }
 stopifnot(qr(design)$rank==ncol(design),nrow(design)>ncol(design));rownames(design)<-m$library_id
 v <- voom(y,design,plot=FALSE,save.plot=TRUE)
 vectors <- list()
 cv <- function(...) { z<-setNames(rep(0,ncol(design)),colnames(design));a<-list(...);for(n in names(a))z[n]<-a[[n]];z }
 for(g in genos)for(c in cells) { n<-paste('DFMO',g,c,sep='_');z<-cv();z[n]<-1;vectors[[n]]<-z }
 if(series=='GSE162300') {
  vectors[['baseline_Th17n_minus_iTreg']]<-cv(baseline_WT_iTreg=-1)
  vectors[['baseline_Th17p_minus_iTreg']]<-cv(baseline_WT_Th17p=1,baseline_WT_iTreg=-1)
  vectors[['baseline_Th17p_minus_Th17n']]<-cv(baseline_WT_Th17p=1)
  vectors[['baseline_pooledTh17_minus_iTreg']]<-cv(baseline_WT_Th17p=.5,baseline_WT_iTreg=-1)
 } else {
  for(c in cells) {z<-cv();z[paste('DFMO_JMJD3_KO',c,sep='_')]<-1;z[paste('DFMO_WT',c,sep='_')]<--1;vectors[[paste0('interaction_KO_minus_WT_',c)]]<-z}
  vectors[['baseline_WT_Th17n_minus_iTreg']]<-cv(baseline_WT_iTreg=-1)
  vectors[['baseline_KO_Th17n_minus_iTreg']]<-cv(baseline_JMJD3_KO_iTreg=-1)
  vectors[['baseline_equalGenotype_Th17n_minus_iTreg']]<-cv(baseline_WT_iTreg=-.5,baseline_JMJD3_KO_iTreg=-.5)
 }
 C<-do.call(cbind,vectors); results<-list()
 for(n in colnames(C)) {
  # Reparameterization makes each contrast an exact coefficient despite gene-specific voom weights.
  dc<-contrastAsCoef(design,C[,n,drop=FALSE]);fit<-eBayes(lmFit(v,dc$design),trend=FALSE,robust=FALSE);k<-dc$coef[1]
  se<-fit$stdev.unscaled[,k]*sqrt(fit$s2.post); t<-fit$t[,k];p<-fit$p.value[,k];q<-p.adjust(p,'BH');fc<-fit$coefficients[,k]
  tab<-data.frame(series=series,contrast=n,gene=rownames(v$E),log2FC=fc,moderated_SE=se,t=t,df=fit$df.total,p=p,q=q,lower=fc-qt(.975,fit$df.total)*se,upper=fc+qt(.975,fit$df.total)*se,s2_post=fit$s2.post,DE=q<=.05 & abs(fc)>=log2(1.5))
  results[[n]]<-tab
  summaries[[paste(series,n)]]<-data.frame(series=series,contrast=n,tested=nrow(tab),up=sum(tab$DE & fc>0),down=sum(tab$DE & fc<0))
 }
 getprogram<-function(n) {t<-results[[n]];ifelse(t$DE,ifelse(t$log2FC>0,'Th17','Treg'),'NS')}
 primary <- if(series=='GSE162300')'baseline_pooledTh17_minus_iTreg' else 'baseline_equalGenotype_Th17n_minus_iTreg'
 prog <- getprogram(primary)
 sensitivity <- getprogram(if(series=='GSE162300')'baseline_Th17n_minus_iTreg' else 'baseline_WT_Th17n_minus_iTreg')
 five <- rep('not_applicable',length(prog))
 if(series=='GSE162300') {
  a<-results[['baseline_Th17p_minus_iTreg']];b<-results[['baseline_Th17n_minus_iTreg']];pn<-results[['baseline_Th17p_minus_Th17n']]
  five<-ifelse(prog=='Treg' & a$DE & a$log2FC<0 & b$DE & b$log2FC<0,'Treg',ifelse(prog!='Treg' & a$DE & a$log2FC>0 & pn$DE & pn$log2FC>0,'Th17p',ifelse(prog!='Treg' & b$DE & b$log2FC>0 & pn$DE & pn$log2FC<0,'Th17n',ifelse(prog=='Th17','Th17','NS'))))
  selected<-a$DE | b$DE | pn$DE
  if(sum(selected)>=2) {pc<-prcomp(t(v$E[selected,,drop=FALSE]),center=TRUE,scale.=FALSE);pcd<-cbind(m,PC1=pc$x[,1],PC2=pc$x[,2],PC1_percent=100*pc$sdev[1]^2/sum(pc$sdev^2),PC2_percent=100*pc$sdev[2]^2/sum(pc$sdev^2),selected_genes=sum(selected));pcs[[series]]<-pcd}
 }
 partitions[[series]]<-data.frame(series=series,gene=rownames(v$E),primary_program=prog,sensitivity_program=sensitivity,five_way=five,primary_contrast=primary)
 # Same-data selected programs: descriptive paired animal summaries, never independent validation.
 for(g in genos)for(c in cells)for(a in animals[m$genotype[match(animals,m$animal_id)]==g]) {
  i<-which(m$animal_id==a & m$cell_type==c & m$treatment=='control');j<-which(m$animal_id==a & m$cell_type==c & m$treatment=='DFMO');stopifnot(length(i)==1,length(j)==1)
  for(pn in c('Th17','Treg')) {z<-prog==pn;animal_programs[[length(animal_programs)+1]]<-data.frame(series=series,genotype=g,cell_type=c,animal_id=a,program=pn,genes=sum(z),mean_delta=if(any(z))mean(v$E[z,j]-v$E[z,i]) else NA_real_)}
 }
 all_results[[series]]<-do.call(rbind,results)
 write_tsv(data.frame(library_id=m$library_id,design,check.names=FALSE),paste0(series,'_design.tsv'))
 write_tsv(data.frame(term=rownames(C),C,check.names=FALSE),paste0(series,'_contrasts.tsv'))
 write_tsv(data.frame(gene=rownames(v$E),v$E,check.names=FALSE),paste0(series,'_voom_E.tsv.gz'))
 colnames(v$weights)<-colnames(v$E)
 write_tsv(data.frame(gene=rownames(v$E),v$weights,check.names=FALSE),paste0(series,'_voom_weights.tsv.gz'))
 write_tsv(data.frame(m,y$samples,check.names=FALSE),paste0(series,'_libraries.tsv'))
 inventories[[series]]<-list(input_genes=nrow(counts),filtered_genes=nrow(v$E),excluded_genes=sum(!keep),libraries=ncol(counts),design_rank=qr(design)$rank,residual_df=nrow(design)-ncol(design),animals=animals,program_counts=as.list(table(prog)),primary_vs_sensitivity_changed=sum(prog!=sensitivity),maximum_library_ratio=max(colSums(counts))/min(colSums(counts)))
}
write_tsv(do.call(rbind,all_results),'all_contrasts.tsv.gz');write_tsv(do.call(rbind,summaries),'contrast_summary.tsv');write_tsv(do.call(rbind,partitions),'gene_programs.tsv');write_tsv(do.call(rbind,pcs),'selected_PCA.tsv');write_tsv(do.call(rbind,animal_programs),'animal_program_changes.tsv')
write_json(list(scope='exposed source-aligned limma reconstruction; author settings and supplement concordance unavailable',series=inventories,R=R.version.string,packages=sapply(c('limma','edgeR','jsonlite'),function(p)as.character(packageVersion(p)))),file.path(out,'model_summary.json'),pretty=TRUE,auto_unbox=TRUE)
writeLines(capture.output(sessionInfo()),file.path(out,'R_session.txt'))
