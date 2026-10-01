"""Stream both complete count sheets for Nb3; validate against archived A10 totals."""
from pathlib import Path
import csv
import hashlib
import html
import json
import re
import time
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
CONFIG = HERE / "config/Nb3_execution_v1.json"
CACHE = ROOT / "raw_data/GSE307112/Nb3_v1"
CELL = re.compile(rb'<c r="([A-Z]+)\d+"[^>]*?>(?:<v>([^<]*)</v>|<is><t>([^<]*)</t></is>)</c>')
ROW = re.compile(rb'<row [^>]*?>(.*?)</row>', re.S)


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def stream_sheet(z, species, member):
    start = time.time()
    annotations, totals, detected, column_map = [], None, None, None
    header = None
    binary = CACHE / f"{species}_counts.bin"
    with z.open(member) as handle, binary.open("xb") as output:
        buffer = b""
        while chunk := handle.read(2**23):
            buffer += chunk
            cut = buffer.rfind(b"</row>")
            if cut < 0:
                continue
            block, buffer = buffer[:cut+6], buffer[cut+6:]
            for match in ROW.finditer(block):
                data = match.group(1)
                cells = CELL.findall(data)
                if len(cells) != data.count(b"<c "):
                    raise ValueError("Unparsed Excel cells; source schema differs")
                if header is None:
                    header = {ref: html.unescape((txt or num).decode()) for ref, num, txt in cells}
                    libraries = [v for v in header.values() if re.match(r"^\d-\d_[A-Z]\d{2}_", v)]
                    lookup = {v:i for i,v in enumerate(libraries)}
                    column_map = {ref:lookup[name] for ref,name in header.items() if name in lookup}
                    ann_cols = {ref:name for ref,name in header.items() if name in ("ID", "symbol", "type")}
                    assert set(ann_cols.values()) == {"ID", "symbol", "type"}
                    assert len(libraries) == len(set(libraries)) == 886
                    totals = np.zeros(len(libraries),dtype=np.int64)
                    detected = np.zeros(len(libraries),dtype=np.int64)
                    continue
                ann, positions, numbers = {}, [], []
                for ref,num,txt in cells:
                    if ref in column_map:
                        if not num:
                            raise ValueError("Non-numeric count")
                        positions.append(column_map[ref]); numbers.append(num)
                    elif ref in ann_cols:
                        ann[ann_cols[ref]] = html.unescape((txt or num).decode())
                values = np.fromstring(b" ".join(numbers).decode(),sep=" ")
                if not (np.isfinite(values).all() and (values >= 0).all()
                        and (values == np.floor(values)).all() and (values < 2**31).all()):
                    raise ValueError("Counts are not finite nonnegative int32 values")
                vector = np.zeros(len(libraries),dtype="<i4")
                vector[positions] = values.astype("<i4")
                vector.tofile(output)
                totals += vector
                detected += vector > 0
                annotations.append(ann)
                if len(annotations)%20000 == 0:
                    print(f"{species}: {len(annotations)} genes, {time.time()-start:.0f}s",flush=True)
        if b"<row " in buffer:
            raise ValueError("Trailing unparsed row")
    ann = pd.DataFrame(annotations)
    assert ann.ID.notna().all() and ann.ID.is_unique
    ann.to_csv(CACHE/f"{species}_genes.tsv",sep="\t",index=False)
    pd.DataFrame({"library":libraries}).to_csv(CACHE/f"{species}_libraries.tsv",sep="\t",index=False)
    return pd.DataFrame({"library":libraries,"species":species,"total_reads":totals,"detected_genes":detected}), {
        "genes":len(ann),"libraries":len(libraries),"matrix_format":"little-endian int32, gene-major",
        "matrix_sha256":sha(binary),"seconds":round(time.time()-start,2)}


if __name__ == "__main__":
    out = HERE / "runs/R2_v1"
    if CACHE.exists() or out.exists():
        raise SystemExit("Refusing to overwrite Nb3_v1 extraction or R2_v1")
    config = json.loads(CONFIG.read_text())
    source = ROOT / config["inputs"]["counts"]["path"]
    assert sha(source) == config["inputs"]["counts"]["sha256"]
    CACHE.mkdir(parents=True); out.mkdir(parents=True)
    frames, records = [], {}
    with zipfile.ZipFile(source) as z:
        for index,species in enumerate(("mouse","human"),1):
            frame,records[species] = stream_sheet(z,species,f"xl/worksheets/sheet{index}.xml")
            frames.append(frame)
    qc = pd.concat(frames,ignore_index=True)
    archived = pd.read_csv(ROOT/"RQ_Specified/A10_organoid_growth_outcome/tables/library_totals.tsv",sep="\t")
    for species in ("mouse","human"):
        joined=qc[qc.species==species].merge(archived,on="library",validate="one_to_one")
        assert len(joined)==886
        assert (joined.total_reads == joined[f"{species}_total_counts"]).all(), "Archived totals disagree"
    qc["source_qc_pass"] = qc.apply(lambda row:row.detected_genes >= config["R2"]["species_gene_detection_cutoff"][row.species],axis=1)
    qc.to_csv(out/"library_qc.tsv",sep="\t",index=False)
    crosswalk=pd.read_csv(ROOT/config["inputs"]["crosswalk"],sep="\t")
    assert set(crosswalk.library)==set(qc.library)
    crosswalk.to_csv(CACHE/"crosswalk.tsv",sep="\t",index=False)
    record={"analysis_id":"Nb3_R2","config_sha256":sha(CONFIG),"script_sha256":sha(Path(__file__)),
            "input_sha256":sha(source),"archived_A10_totals_exact_match":True,"species":records,
            "source_qc_pass":qc.groupby("species").source_qc_pass.sum().astype(int).to_dict()}
    (out/"extraction_record.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps(record["source_qc_pass"]),flush=True)
