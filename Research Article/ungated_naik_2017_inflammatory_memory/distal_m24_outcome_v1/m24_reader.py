"""Exact primary-record and per-base audit for the frozen mouse M24 intervals."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from contextlib import ExitStack
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
GSMS = ("GSM9034861", "GSM9034862", "GSM9034863", "GSM9034864")
CLASSES = ("Memory", "Resolved")


def read_rows(path):
    with path.open(encoding="utf8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_rows(path, rows):
    with path.open("x", encoding="utf8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, value):
    with path.open("x", encoding="utf8", newline="\n") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def inputs_by_name(contract):
    return {Path(a["path"]).name: ROOT / a["path"] for a in contract["inputs"]}


def load_cohort(paths):
    regions = [r for r in read_rows(paths["regions.tsv"]) if r["primary"] == "1"]
    samples = read_rows(paths["samples.tsv"])
    if Counter(r["source_class"] for r in regions) != Counter(Memory=791, Resolved=784):
        raise ValueError("Frozen primary class counts differ")
    coords = [(r["chromosome"], int(r["start0"]), int(r["end0"])) for r in regions]
    if len(set(coords)) != len(regions) or len({r["s2_excel_row"] for r in regions}) != len(regions):
        raise ValueError("Duplicated primary region")
    for row, (_, start, end) in zip(regions, coords, strict=True):
        if row["distal"] != "1" or end-start != int(row["width_bp"]) or start < 0 or end <= start:
            raise ValueError("Invalid frozen region")
    if [(s["gsm"], s["history"]) for s in samples] != list(zip(GSMS, ("naive","naive","post_IMQ","post_IMQ"))):
        raise ValueError("Frozen pool identities or histories differ")
    return regions, samples


def audit_interval(handle, chrom, start, end):
    """Use masks distinct from signal. Values agree exactly after widening stored floats."""
    width = end-start
    if width <= 0:
        raise ValueError("Nonpositive interval width")
    diag = dict(width_bp=width, records=0, stored_bp=0, explicit_zero_bp=0, absent_bp=0,
                overlap_bp=0, conflict_bp=0, nonfinite_record_bp=0, negative_record_bp=0,
                nonfinite_fetch_stored_bp=0, disagreement_bp=0, invalid_record=0,
                fetch_bp="", wrong_fetch_length=0, out_of_bounds=0, read_error="", status="held", mean_cpm="")
    if chrom not in handle.chromsizes or start < 0 or end > handle.chromsizes[chrom]:
        diag["out_of_bounds"] = 1
        return diag
    seen = np.zeros(width, dtype=bool)
    overlaps = seen.copy()
    conflicts = seen.copy()
    nonfinite = seen.copy()
    negative = seen.copy()
    stored = np.full(width, np.nan)
    for name, a, b, score in handle.fetch_intervals(chrom, start, end, iterator=True):
        diag["records"] += 1
        lo, hi = max(a,start)-start, min(b,end)-start
        if name != chrom or a < 0 or b > handle.chromsizes[chrom] or not 0 <= lo < hi <= width:
            diag["invalid_record"] += 1
            continue
        sl = slice(lo,hi)
        overlaps[sl] |= seen[sl]
        conflicts[sl] |= seen[sl] & (stored[sl] != score)
        nonfinite[sl] |= not np.isfinite(score)
        negative[sl] |= score < 0
        stored[sl] = score
        seen[sl] = True
    diag.update(stored_bp=int(seen.sum()), explicit_zero_bp=int(np.sum(seen & (stored == 0))),
                absent_bp=int((~seen).sum()), overlap_bp=int(overlaps.sum()), conflict_bp=int(conflicts.sum()),
                nonfinite_record_bp=int(nonfinite.sum()), negative_record_bp=int(negative.sum()))
    fetched = np.asarray(handle.fetch(chrom,start,end,bins=-1,missing=np.nan,oob=np.inf), dtype=np.float64)
    diag["fetch_bp"] = int(fetched.size)
    if fetched.shape != (width,):
        diag["wrong_fetch_length"] = 1
        return diag
    diag["nonfinite_fetch_stored_bp"] = int(np.sum(seen & ~np.isfinite(fetched)))
    diag["disagreement_bp"] = int(np.sum((seen & (stored != fetched)) | (~seen & ~np.isnan(fetched))))
    if any(diag[k] for k in ("absent_bp","overlap_bp","conflict_bp","nonfinite_record_bp",
                              "negative_record_bp","nonfinite_fetch_stored_bp","disagreement_bp","invalid_record")):
        return diag
    diag.update(status="valid", mean_cpm=float(np.sum(stored, dtype=np.float64)/width))
    return diag


def audit_all(handles, regions, output):
    records = []
    for gsm, handle in handles.items():
        for r in regions:
            start, end = int(r["start0"]), int(r["end0"])
            try:
                fields = audit_interval(handle, r["chromosome"], start, end)
            except Exception as exc:
                # Unknown coverage after an I/O failure must stay unknown, not appear as zero.
                fields = dict(width_bp=end-start, read_error=f"{type(exc).__name__}: {exc}",status="held",mean_cpm="")
            records.append(dict(gsm=gsm,s2_excel_row=r["s2_excel_row"],source_class=r["source_class"],
                chromosome=r["chromosome"],start0=start,end0=end,**fields))
    # First or every read can fail. Preserve a consistent diagnostic schema in that case.
    columns = dict.fromkeys(k for row in records for k in row)
    write_rows(output/"intervals.tsv", [dict.fromkeys(columns,"") | r for r in records])
    held = [r for r in records if r["status"] != "valid"]
    write_json(output/"coverage.json", dict(records=len(records),held=len(held),complete=len(records)-len(held),
               by_pool={g:sum(r["gsm"]==g and r["status"]!="valid" for r in records) for g in handles},
               aggregation="held" if held else "eligible"))
    if held:
        raise ValueError(f"{len(held)} interval-library records held. Coverage diagnostics saved; aggregation stopped.")


def extract(contract, output):
    import bbi
    paths = inputs_by_name(contract)
    regions, samples = load_cohort(paths)
    structure = json.loads(paths["track_structure.json"].read_bytes())
    if bbi.__version__ != structure["reader"]["pybbi"] or np.__version__ != structure["reader"]["numpy"]:
        raise ValueError("Reader version differs from the qualified runtime")
    with ExitStack() as stack:
        handles = {}
        try:
            for sample in samples:
                gsm = sample["gsm"]
                path = paths[sample["file_url"].rsplit("/",1)[1]]
                with path.open("rb") as stream:
                    file_hash = hashlib.file_digest(stream,"sha256").hexdigest()
                if path.stat().st_size != int(sample["bytes"]) or file_hash != sample["sha256"]:
                    raise ValueError(f"Complete binary identity failed for {gsm}")
                handle = stack.enter_context(bbi.open(str(path)))
                if handle.chromsizes != structure["tracks"][gsm]["chromosome_sizes"]:
                    raise ValueError(f"Chromosome dictionary changed for {gsm}")
                handles[gsm] = handle
        except Exception as exc:
            write_json(output/"coverage.json",dict(aggregation="held",stage="file_header",error=str(exc)))
            raise
        audit_all(handles,regions,output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    extract(json.loads(args.contract.read_bytes()), args.output)
