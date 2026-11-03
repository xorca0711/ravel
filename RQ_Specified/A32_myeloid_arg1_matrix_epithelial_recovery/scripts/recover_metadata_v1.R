# Metadata-only XDR stream filter; never use stripped assays as expression.
# Format reference: R Internals Serialization Formats; R Core serialize.c.
# Unsupported constructs fail closed. Native R performs final deserialization.
filter_xdr <- function(src, dst, threshold=1000000L) {
  pos <- 0; omitted <- list(); nodes <- 0L
  bytes <- function(n, keep=TRUE) {
    if (!is.finite(n) || n < 0 || n > 1e11) stop("Invalid byte count")
    while (n > 0) {
      k <- min(n,1048576); b <- readBin(src,"raw",k)
      if (length(b)!=k) stop("Truncated stream at ",pos)
      if (keep) writeBin(b,dst)
      pos <<- pos+k; n <- n-k
    }
  }
  number <- function(keep=TRUE) {
    b <- readBin(src,"raw",4L)
    if (length(b)!=4L) stop("Truncated integer at ",pos)
    pos <<- pos+4
    if (keep) writeBin(b,dst)
    readBin(b,"integer",1L,size=4,endian="big")
  }
  put <- function(n) writeBin(as.integer(n),dst,size=4,endian="big")
  item <- function(depth=0L) {
    if (depth>200L) stop("Excessive nesting")
    nodes <<- nodes+1L
    if (nodes>30000000L) stop("Excessive node count")
    flags <- number(); kind <- bitwAnd(flags,255L)
    att <- bitwAnd(flags,512L)!=0L; tag <- bitwAnd(flags,1024L)!=0L
    child <- function() item(depth+1L)
    if (kind %in% c(0L,254L,253L,252L,251L,250L,242L,241L)) return(invisible(NULL))
    if (kind==255L) { if (bitwShiftR(flags,8L)==0L) number(); return(invisible(NULL)) }
    if (kind==238L) { child();child();child();return(invisible(NULL)) }
    if (kind==1L) { child();return(invisible(NULL)) }
    if (kind==4L) { number();child();child();child();child();return(invisible(NULL)) }
    if (kind %in% c(2L,3L,5L,6L,17L)) {
      if(att) child()
      if(tag) child()
      child();child();return(invisible(NULL))
    }
    if (kind %in% c(7L,8L,9L)) {
      n <- number()
      if (n < -1L || (n == -1L && kind!=9L)) stop("Invalid string length")
      if(n>=0L) bytes(n)
    } else if (kind %in% c(10L,13L,14L,15L,24L)) {
      start <- pos; n <- number(FALSE)
      if(n<0L) stop("Long/invalid atomic vector unsupported")
      size <- if(kind==24L) 1L else if(kind==14L) 8L else if(kind==15L) 16L else 4L
      drop <- n>threshold
      put(if(drop) 0L else n); bytes(as.double(n)*size,!drop)
      if(drop) omitted[[length(omitted)+1L]] <<- c(offset=start,type=kind,length=n,bytes=as.double(n)*size)
    } else if (kind %in% c(16L,19L,20L)) {
      n <- number()
      if(n<0L || n>1000000L) stop("Unsupported list/string-vector length")
      if(n>0L) for(i in seq_len(n)) child()
    } else if (kind==22L) {
      child();child()
    } else if (!kind %in% c(23L,25L)) {
      stop("Unsupported serialization type ",kind," at ",pos-4)
    }
    if(att) child()
    invisible(NULL)
  }
  magic <- readBin(src,"raw",2L);pos<-2
  if(!identical(magic,charToRaw("X\n"))) stop("Only XDR serialization supported")
  writeBin(magic,dst)
  version<-number();number();number()
  if(!version %in% c(2L,3L)) stop("Unsupported serialization version")
  if(version==3L) { n<-number();bytes(n) }
  item()
  if(length(readBin(src,"raw",1L))) stop("Trailing stream data")
  list(serialization_version=version,input_bytes=pos,nodes=nodes,omitted=omitted)
}

recover_metadata <- function(input, output) {
  dir.create(output,recursive=TRUE,showWarnings=FALSE)
  temp <- file.path(output,"metadata_only_INVALID_ASSAYS.rds")
  if(file.exists(temp)) stop("Refuse existing temporary output")
  # GEO applies gzip around an already gzip-compressed RDS.
  src <- gzcon(gzfile(input,"rb"));dst<-file(temp,"wb")
  stats <- tryCatch(filter_xdr(src,dst),finally={close(src);close(dst)})
  on.exit(unlink(temp),add=TRUE)
  obj <- readRDS(temp)
  if(!identical(as.character(class(obj)),"Seurat")) stop("Unexpected source class")
  meta<-attr(obj,"meta.data",exact=TRUE)
  if(!is.data.frame(meta)||nrow(meta)!=45311L||anyDuplicated(rownames(meta))) stop("Invalid metadata")
  if(any(lengths(meta)!=nrow(meta))) stop("Inconsistent metadata columns")
  # Threshold exceeds every per-cell column length; verify the exclusion explicitly.
  stopifnot(all(vapply(stats$omitted,function(z) z['length']>nrow(meta),logical(1))))
  write.table(cbind(cell_id=rownames(meta),meta),file.path(output,"source_metadata.tsv"),sep="\t",quote=TRUE,row.names=FALSE,na="NA")
  write.table(do.call(rbind,stats$omitted),file.path(output,"stripped_numeric_payloads.tsv"),sep="\t",quote=FALSE,row.names=FALSE)
  info <- c(paste("class",class(obj)),paste("cells",nrow(meta)),paste("columns",paste(names(meta),collapse=",")),paste("input_bytes",stats$input_bytes),paste("nodes",stats$nodes),paste("stripped_arrays",length(stats$omitted)),"Expression source: original GEO RAW.tar only; stripped arrays are invalid.")
  writeLines(info,file.path(output,"recovery.txt"))
  rm(obj);gc()
  message("Recovered ",nrow(meta)," metadata rows; stripped ",length(stats$omitted)," large arrays")
}
if(sys.nframe()==0L) {
  a<-commandArgs(TRUE)
  if(length(a)!=2L) stop("Usage: input_double_gzip_RDS output_dir")
  recover_metadata(a[1],a[2])
}
