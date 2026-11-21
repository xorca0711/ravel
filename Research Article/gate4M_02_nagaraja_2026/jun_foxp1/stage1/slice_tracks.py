"""Acquire unzoomed GEO track slices with the S3 UCSC executable (Linux/WSL)."""
from concurrent.futures import ThreadPoolExecutor
import csv
from pathlib import Path
import subprocess
import time

D = Path("raw_data/nagaraja_jf1")
SRC = Path("analysis/research/runs/ng26_s3_sources_v1")
REG = Path("raw_data/nagaraja_s0/code/7_inVitroFootprinting/Regions.csv")
UCSC = Path("raw_data/nagaraja_s3/bigWigToBedGraph")


def read(path, delimiter):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def main():
    tracks = read(SRC/"ed6_tissue_sources.tsv","\t") + read(SRC/"thbs1_track_sources.tsv","\t")
    regions = [(r["Chromosome"], int(r["amplicon_start"])-1, int(r["amplicon_end"])+1, str(i))
               for i,r in enumerate(read(REG,","),1)]
    def fetch(track):
        gsm = track["gsm"]
        out = D/"methylation"/gsm
        out.mkdir(parents=True,exist_ok=True)
        cache = (D/"udc"/gsm).resolve()
        cache.mkdir(parents=True,exist_ok=True)
        audit = ("chr12",80433160,80433600,"audit_Dcaf5") if "arm" in track else ("chr2",118115000,118118000,"audit_Thbs1")
        local = D/"original_tracks"/(gsm+".bw")
        source = str(local) if local.exists() else track["url"]
        for chrom, start, end, label in [audit]+regions:
            target = out/(label+".bedGraph")
            if target.exists():
                continue
            partial = target.with_suffix(".part")
            for trial in range(3):
                result = subprocess.run([str(UCSC),"-udcDir="+str(cache),"-chrom="+chrom,
                                         "-start="+str(start),"-end="+str(end),source,str(partial)],
                                        capture_output=True,text=True)
                if result.returncode == 0:
                    partial.replace(target)
                    break
                if trial == 2:
                    raise RuntimeError(f"{gsm} {label}: {result.stderr[:400]}")
                time.sleep(2**trial)
        print(gsm,"completed 63 source slices plus S3 audit window",flush=True)
    with ThreadPoolExecutor(6) as pool:
        list(pool.map(fetch,tracks))

if __name__ == "__main__":
    main()
