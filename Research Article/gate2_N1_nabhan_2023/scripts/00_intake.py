"""Recover/check public design metadata; no expression analysis or inferred pairing."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def derive(raw: bytes) -> tuple[str, dict]:
    text = gzip.decompress(raw).decode("utf-8")
    rows = []
    for block in re.split(r"^\^SAMPLE = ", text, flags=re.M)[1:]:
        lines = block.splitlines()
        fields: dict[str, list[str]] = {}
        for line in lines[1:]:
            if line.startswith("^"):
                break
            if " = " in line:
                key, value = line.split(" = ", 1)
                fields.setdefault(key, []).append(value)
        title = fields["!Sample_title"][0]
        match = re.fullmatch(r"(.+), rep([123])", title)
        if match is None:
            raise ValueError(f"Unexpected sample title: {title}")
        chars = dict(x.split(": ", 1) for x in fields["!Sample_characteristics_ch1"])
        rows.append({
            "accession": lines[0].strip(), "title": title,
            "condition": match[1], "replicate_label": match[2],
            "organism": fields["!Sample_organism_ch1"][0],
            "cell_type": chars["cell type"], "treatment": chars["treatment"],
            "assay": "bulk_RNA_seq", "biological_unit_id": "unresolved",
            "pairing_id": "unresolved",
            "processed_file_url": fields["!Sample_supplementary_file_1"][0],
        })
    if not rows:
        raise ValueError("No GEO samples found")
    rows.sort(key=lambda r: r["accession"])
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    summary = {
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "n_libraries": len(rows),
        "condition_counts": dict(sorted(Counter(r["condition"] for r in rows).items())),
        "assay": "bulk_RNA_seq", "assay_basis": "P1 Figure 4 and methods p.24",
        "preparation_map_verified": False, "pairing_verified": False,
        "count_matrix_inspected": False, "biological_analysis_executed": False,
    }
    return out.getvalue(), summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Retrieve SOFT only if absent")
    parser.add_argument("--check", action="store_true", help="Check existing outputs without writing")
    args = parser.parse_args()
    if args.download and args.check:
        parser.error("Use --download or --check separately")
    manifest = json.loads((ROOT / "metadata/source_manifest.json").read_text(encoding="utf-8"))
    source = next(s for s in manifest["sources"] if s["id"] == "D1")
    path = ROOT / source["path"]
    if args.download and not path.exists():
        with urllib.request.urlopen(source["url"], timeout=30) as response:
            downloaded = response.read()
        if hashlib.sha256(downloaded).hexdigest() != source["sha256"]:
            raise ValueError("Remote metadata changed; review provenance before updating snapshot")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(downloaded)
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != source["sha256"]:
        raise ValueError("Source metadata hash mismatch")
    tsv, summary = derive(raw)
    config = json.loads((ROOT / "config/pipeline.json").read_text(encoding="utf-8"))
    expected = config["primary_deposit"]
    if summary["n_libraries"] != expected["expected_libraries"] or summary["condition_counts"] != {c: expected["libraries_per_condition"] for c in expected["conditions"]}:
        raise ValueError("Unexpected treatment design")
    outputs = {"samples.tsv": tsv, "intake_summary.json": json.dumps(summary, indent=2) + "\n"}
    for name, content in outputs.items():
        target = ROOT / "metadata" / name
        if args.check:
            if target.read_text(encoding="utf-8") != content:
                raise ValueError(f"Stale intake output: {name}")
        else:
            target.write_text(content, encoding="utf-8", newline="\n")
    print("PASS: 18 libraries / 6 conditions; bulk metadata only; preparation and pairing unresolved")


if __name__ == "__main__":
    main()
