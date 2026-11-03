args<-commandArgs(TRUE)
source(args[1])
setClass("MetadataFixture",slots=c(meta.data="data.frame",assays="list",misc="list"))
meta<-data.frame(group=factor(c("PBS","BLM","PBS","BLM","PBS","BLM")),depth=c(0,2,NA,8,16,32),label=c("AT1","AT2","AM1",NA,"fibroblast","mu"),keep=c(TRUE,FALSE,NA,TRUE,FALSE,TRUE),stringsAsFactors=FALSE)
rownames(meta)<-paste0("cell_",seq_len(6))
x<-new("MetadataFixture",meta.data=meta,assays=list(counts=matrix(as.double(1:120),20,6),integers=as.integer(1:120),complex=complex(real=1:120),raw=as.raw(rep(1,120))),misc=list(symbols=alist(a=x,b=x),seq=1:6,empty=NULL,nested=list(meta)))
for(v in c(2L,3L)) {
  src<-rawConnection(serialize(x,NULL,version=v),"rb");dst<-rawConnection(raw(),"wb")
  st<-filter_xdr(src,dst,1000L);out<-rawConnectionValue(dst);close(src);close(dst)
  stopifnot(identical(out,serialize(x,NULL,version=v)),identical(unserialize(out),x))
  src<-rawConnection(serialize(x,NULL,version=v),"rb");dst<-rawConnection(raw(),"wb")
  st<-filter_xdr(src,dst,80L);out<-rawConnectionValue(dst);close(src);close(dst)
  z<-unserialize(out)
  stopifnot(identical(attr(z,"meta.data"),meta),identical(attr(z,"misc"),attr(x,"misc")),length(st$omitted)>=3L)
}
# Truncation and unsupported type fail closed.
for(b in list(head(serialize(x,NULL),-1),c(charToRaw("X\n"),as.raw(c(0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,99))))) {
 src<-rawConnection(b,"rb");dst<-rawConnection(raw(),"wb")
 result<-try(filter_xdr(src,dst),silent=TRUE);close(src);close(dst)
 stopifnot(inherits(result,"try-error"))
}
# A nested gzip source is passed through native gz connections, not parsed in Python.
f1<-tempfile();f2<-tempfile();saveRDS(x,f1,version=2,compress="gzip")
c1<-file(f1,"rb");c2<-gzfile(f2,"wb");writeBin(readBin(c1,"raw",file.info(f1)$size),c2);close(c1);close(c2)
src<-gzcon(gzfile(f2,"rb"));dst<-rawConnection(raw(),"wb");filter_xdr(src,dst,80L);z<-unserialize(rawConnectionValue(dst));close(src);close(dst)
stopifnot(identical(attr(z,"meta.data"),meta));unlink(c(f1,f2))
cat("PASS: byte-identical passthrough v2/v3; native metadata/order parity; factors, data frames, S4, symbols/references, atomic vectors, ALTREP, nested gzip; fail-closed truncation/type\n")
