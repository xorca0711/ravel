"""Cache mm10 amplicon reference, tagged processing code and IGVF library provenance."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import csv
import gzip
import hashlib
import json
import time

import requests

S0=Path("raw_data/nagaraja_s0")
D=Path("raw_data/nagaraja_jf1")
REG=S0/"code/7_inVitroFootprinting/Regions.csv"

def get(path,url,params=None,byte_range=None):
    if path.exists():
        return path.read_bytes()
    path.parent.mkdir(parents=True,exist_ok=True)
    headers={"Range":f"bytes=0-{byte_range-1}"} if byte_range else {}
    for n in range(5):
        try:
            r=requests.get(url,params=params,headers=headers,timeout=(12,50))
            r.raise_for_status()
            data=r.content
            if byte_range and (r.status_code!=206 or len(data)!=byte_range):
                raise ValueError("incomplete or non-ranged prefix")
            tmp=path.with_suffix(path.suffix+".part")
            tmp.write_bytes(data)
            tmp.replace(path)
            return data
        except (requests.RequestException,ValueError):
            if n==4: raise
            time.sleep(2**n)

def main():
    tree=json.loads((S0/"code_tree.json").read_bytes())
    for key,name in [("7_inVitroFootprinting/01_IVFP.multiscale_plot.ipynb","ivfp.ipynb"),
                     ("1_SHAREseq_processing/01b_refilter_barcodes.ATAC.v2.2.R","refilter.R"),
                     ("1_SHAREseq_processing/02c_scATAC.getSinglet_cluster.v2.8.R","singlets.R")]:
        data=get(D/name,"https://raw.githubusercontent.com/snagaraja13/colitis_memory/v1.0.1/"+key)
        expected=next(x["sha"] for x in tree["tree"] if x["path"]==key)
        assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==expected
    with REG.open() as h: regions=list(csv.DictReader(h))
    def ref(item):
        idx,r=item
        chrom=r["Chromosome"]
        start,end=int(r["amplicon_start"])-1,int(r["amplicon_end"])+1
        data=get(D/"reference"/f"{idx}.json","https://api.genome.ucsc.edu/getData/sequence",
                 params={"genome":"mm10","chrom":chrom,"start":start,"end":end})
        obj=json.loads(data)
        assert obj["genome"]=="mm10" and obj["chrom"]==chrom and len(obj["dna"])==end-start
    with ThreadPoolExecutor(5) as workers: list(workers.map(ref,enumerate(regions,1)))
    sets={}
    for series in ["IGVFDS0502QEQJ","IGVFDS0237MRDL"]:
        for item in json.loads((S0/(series+".json")).read_bytes())["input_file_sets"]:
            sets[item["accession"]]=item["@id"]
    def measurement(arg):
        acc,uri=arg
        data=get(D/"sets"/(acc+".json"),"https://api.data.igvf.org"+uri+"?format=json")
        record=json.loads(data)
        assert record["accession"]==acc
        for f in record["files"]:
            if "barcode.fastq" in f.get("submitted_file_name","").lower():
                url=f["s3_uri"].replace("s3://igvf-public/","https://igvf-public.s3.amazonaws.com/")
                get(D/"prefix"/(f["accession"]+".64k"),url,byte_range=65536)
    with ThreadPoolExecutor(5) as workers: list(workers.map(measurement,sets.items()))
    print(f"Cached 63 mm10 reference slices and {len(sets)} measurement records",flush=True)

if __name__=="__main__":
    main()
