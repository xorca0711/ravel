"""Use every BGZF row for a library denominator and retain panel-overlapping rows."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import csv
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

SRC=Path("raw_data/nagaraja_s0")
CACHE=Path("raw_data/nagaraja_jf1")
HERE=Path(__file__).resolve().parent

def compress(source,target):
    with source.open("rb") as src, target.open("wb") as dest:
        with gzip.GzipFile(fileobj=dest,filename="",mode="wb",mtime=0,compresslevel=5) as packed:
            shutil.copyfileobj(src,packed,length=1<<20)

def main(out):
    with TemporaryDirectory(dir=CACHE) as tmp:
        root=Path(tmp)
        exe=(root/("scan.exe" if os.name=="nt" else "scan")).resolve()
        rustc=subprocess.check_output(["rustc","-Vv"],text=True)
        subprocess.run(["rustc","--edition=2021","-O",str(HERE/"scan_fragments.rs"),"-o",str(exe)],check=True)
        bed=root/"targets.bed"
        with (SRC/"code/7_inVitroFootprinting/Regions.csv").open() as handle:
            rows=list(csv.DictReader(handle))
        assert len(rows)==63
        bed.write_text("".join(f"{r['Chromosome']}\t{r['amplicon_start']}\t{r['amplicon_end']}\n" for r in rows))
        def scan(entry):
            label,series=entry
            meta=json.loads((SRC/(series+".json")).read_bytes())
            item,=[f for f in meta["files"] if f["content_type"]=="fragments"]
            path=CACHE/Path(item["s3_uri"]).name
            assert path.stat().st_size==item["file_size"]
            depth=root/(label+"_depth.tsv")
            panel=root/(label+"_panel.tsv")
            with subprocess.Popen([str(exe),str(bed),str(depth),str(panel)],stdin=subprocess.PIPE) as worker:
                with gzip.open(path,"rb") as stream:
                    shutil.copyfileobj(stream,worker.stdin,length=4<<20)
                worker.stdin.close()
                if worker.wait()!=0: raise RuntimeError("fragment scanner failed for "+label)
            for p in [depth,panel]:
                compress(p,out/(p.name+".gz"))
            return {"export":label,"series":series,"file":item["accession"],"assembly":item["assembly"],
                    "md5":item["md5sum"],"bytes":item["file_size"],"public_uri":item["s3_uri"]}
        with ThreadPoolExecutor(2) as workers:
            info=list(workers.map(scan,[("extended","IGVFDS0502QEQJ"),("main","IGVFDS0237MRDL")]))
        (out/"scan_provenance.json").write_text(json.dumps({"compiler":rustc,"sources":info,"panel_loci":63,
                "input_scope":"complete BGZF exports, all chromosomes, source row read support retained separately"},indent=2)+"\n")

if __name__=="__main__":
    main(Path(sys.argv[1]))
