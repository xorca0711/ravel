"""Preserve the exact small public inputs and regional fetch provenance in one archive."""
import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

from fetch_support import D,S0,REG
from methylation import track_manifest

def make():
    target=D/"stage1_sources.zip"
    if target.exists():
        raise FileExistsError(target)
    entries={}
    def add(key,path,url,detail):
        data=path.read_bytes()
        item=(data,url,detail)
        if key in entries: assert entries[key]==item
        entries[key]=item
    for source in ["IGVFDS0502QEQJ","IGVFDS0237MRDL"]:
        path=S0/(source+".json");ds=json.loads(path.read_bytes())
        def record(acc,p):
            d=json.loads(p.read_bytes())
            add("records/"+acc+".json",p,"https://api.data.igvf.org"+d["@id"]+"?format=json","release record")
        record(source,path)
        for pool in ds["samples"]:
            pp=S0/(pool["accession"]+".json");pr=json.loads(pp.read_bytes());record(pool["accession"],pp)
            for s in pr["multiplexed_samples"]:
                record(s["accession"],S0/"specimens"/(s["accession"]+".json"))
        for s in ds["input_file_sets"]:
            p=D/"sets"/(s["accession"]+".json");m=json.loads(p.read_bytes())
            add("sets/"+p.name,p,"https://api.data.igvf.org"+m["@id"]+"?format=json","measurement record")
            for f in m["files"]:
                if "barcode.fastq" in f.get("submitted_file_name","").lower():
                    name=f["accession"]+".64k"
                    add("prefix/"+name,D/"prefix"/name,f["s3_uri"],"compressed bytes 0-65535")
    with REG.open() as h: regions=list(csv.DictReader(h))
    for i,r in enumerate(regions,1):
        chrom,start,end=r["Chromosome"],int(r["amplicon_start"])-1,int(r["amplicon_end"])+1
        url=f"https://api.genome.ucsc.edu/getData/sequence?genome=mm10&chrom={chrom}&start={start}&end={end}"
        add(f"reference/{i}.json",D/"reference"/f"{i}.json",url,"mm10 padded amplicon")
    for t in track_manifest().itertuples(index=False):
        folder=D/"methylation"/t.gsm
        for i,r in enumerate(regions,1):
            add(f"methylation/{t.gsm}/{i}.bedGraph",folder/f"{i}.bedGraph",t.url,
                f"{r['Chromosome']}:{int(r['amplicon_start'])-1}-{int(r['amplicon_end'])+1}, exact unzoomed slice")
        audit="audit_"+t.audit+".bedGraph"
        add(f"methylation/{t.gsm}/{audit}",folder/audit,t.url,"independent repeat of S3 "+t.audit+" window")
    tag="https://raw.githubusercontent.com/snagaraja13/colitis_memory/v1.0.1/"
    for local,src in [("ivfp.ipynb","7_inVitroFootprinting/01_IVFP.multiscale_plot.ipynb"),
                      ("refilter.R","1_SHAREseq_processing/01b_refilter_barcodes.ATAC.v2.2.R"),
                      ("singlets.R","1_SHAREseq_processing/02c_scATAC.getSinglet_cluster.v2.8.R")]:
        add("code/"+local,D/local,tag+src,"tag v1.0.1, Git blob verified at acquisition")
    ledger=io.StringIO();writer=csv.writer(ledger,delimiter="\t",lineterminator="\n")
    writer.writerow(["member","bytes","sha256","source","scope"])
    with ZipFile(target.with_suffix(".tmp"),"w") as archive:
        for k,(v,url,detail) in sorted(entries.items()):
            writer.writerow([k,len(v),hashlib.sha256(v).hexdigest(),url,detail])
            info=ZipInfo(k);info.compress_type=ZIP_DEFLATED
            archive.writestr(info,v)
        info=ZipInfo("source_manifest.tsv");info.compress_type=ZIP_DEFLATED
        archive.writestr(info,ledger.getvalue().encode())
    target.with_suffix(".tmp").replace(target)
    print("Preserved",len(entries),"source slices and records in",target)

if __name__=="__main__":
    make()
