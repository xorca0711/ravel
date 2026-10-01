"""Acquire small public GEO SOFT records and audit context eligibility; no patient raw data."""
from pathlib import Path
from urllib.request import Request, urlopen
import gzip
import hashlib
import json
import csv
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
SERIES = ("GSE307128", "GSE215824", "GSE122960")

def fetch(series):
    folder = ROOT / "raw_data/Nb3_context_metadata"
    folder.mkdir(exist_ok=True)
    url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{series[:-3]}nnn/{series}/soft/{series}_family.soft.gz"
    path = folder / f"{series}_family.soft.gz"
    if not path.exists():
        with urlopen(Request(url, headers={"User-Agent": "Nb3-reproducibility-audit/1.0"}), timeout=90) as response:
            data = response.read(15_000_001)
        if len(data) > 15_000_000:
            raise ValueError("Unexpectedly large metadata; stop rather than download expression tables")
        gzip.decompress(data)
        path.write_bytes(data)
    data = path.read_bytes()
    lines = gzip.decompress(data).decode("utf-8").splitlines()
    samples, record, header = [], None, []
    keys = ("!Sample_title", "!Sample_source_name_ch1", "!Sample_characteristics_ch1", "!Sample_treatment_protocol_ch1", "!Sample_data_processing", "!Sample_supplementary_file", "!Sample_relation")
    for line in lines:
        if line.startswith("^SAMPLE = "):
            if record: samples.append(record)
            record = {"gsm": line.split(" = ", 1)[1]}
        elif line.startswith("!Series_"):
            if any(line.startswith(x) for x in ("!Series_title", "!Series_summary", "!Series_overall_design", "!Series_supplementary_file", "!Series_pubmed_id")):
                header.append(line)
        elif record and line.startswith(keys):
            key, value = line.split(" = ", 1)
            record.setdefault(key.removeprefix("!Sample_"), []).append(value)
    if record: samples.append(record)
    return {"series": series, "url": url, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "series_metadata": header, "samples": samples}

def main():
    out = HERE / "runs/R5_v1"
    if out.exists():
        raise SystemExit("Refusing to overwrite context metadata audit")
    with ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(fetch, SERIES))
    out.mkdir()
    for record in records:
        (out / f'{record["series"]}_metadata.json').write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({r["series"]: len(r["samples"]) for r in records}))

if __name__ == "__main__":
    main()
