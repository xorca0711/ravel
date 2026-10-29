"""Bounded source-label and feature-identifier audit; no count matrices are read."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re

from verify_sources_v2 import verify

RAW = Path("raw_data/nam_memory_2026")
REFERENCES = {
    "GSM9964564": "1", "GSM9964565": "2",
    "GSM9964566": "5", "GSM9964567": "6",
}
FEATURES = {
    "GSM9964560": "1", "GSM9964561": "2",
    "GSM9964562": "6", "GSM9964563": "5",
}
REFERENCE_FIELDS = ["reference_file", "reference_accession", "tag_id", "name",
                    "feature_type", "condition_label"]
TAG_FIELDS = ["feature_file", "library_accession", "tag_id", "name", "feature_type"]
PRESENCE_FIELDS = ["feature_file", "reference_file", "tag_id", "present"]


def parse_reference(stream):
    """Trim headers/values; refuse missing/ambiguous fields instead of blank labels."""
    reader = csv.DictReader(stream)
    original_headers = reader.fieldnames
    if not original_headers:
        raise ValueError("Missing CSV header")
    headers = [header.strip() for header in original_headers]
    if any(not header for header in headers) or len(set(headers)) != len(headers):
        raise ValueError("Empty or duplicate normalized CSV header")
    required = {"id", "name", "feature_type", "multiplexed_sample"}
    if not required.issubset(headers):
        raise ValueError("Missing required CSV header: " + ", ".join(sorted(required - set(headers))))
    reader.fieldnames = headers
    rows, seen = [], set()
    for raw in reader:
        if None in raw or any(value is None for value in raw.values()):
            raise ValueError(f"Missing or extra CSV field at line {reader.line_num}")
        row = {key: value.strip() for key, value in raw.items()}
        if any(not row[key] for key in required):
            raise ValueError(f"Blank required CSV field at line {reader.line_num}")
        if row["id"] in seen:
            raise ValueError("Duplicate reference tag: " + row["id"])
        seen.add(row["id"])
        rows.append(row)
    if not rows:
        raise ValueError("Reference has no data rows")
    return original_headers, headers, rows


def parse_features(stream):
    counts, tags, seen = Counter(), [], set()
    for line_number, fields in enumerate(csv.reader(stream, delimiter="\t"), 1):
        if len(fields) != 3 or any(not field.strip() for field in fields):
            raise ValueError(f"Missing or malformed feature field at line {line_number}")
        identifier, name, kind = [field.strip() for field in fields]
        counts[kind] += 1
        if kind != "Gene Expression" or re.fullmatch(r"CMO\d+", identifier):
            if identifier in seen:
                raise ValueError("Duplicate tag feature: " + identifier)
            seen.add(identifier)
            tags.append({"tag_id": identifier, "name": name, "feature_type": kind})
    if not counts:
        raise ValueError("Feature table has no rows")
    return dict(sorted(counts.items())), tags


def parse_accession(path, accession):
    fields = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith(("!Sample_geo_accession =", "!Sample_title =")):
            key, value = line.split("=", 1)
            key = key.strip().removeprefix("!Sample_")
            if key in fields:
                raise ValueError("Duplicate accession metadata: " + key)
            fields[key] = value.strip()
    if fields.get("geo_accession") != accession or not fields.get("title"):
        raise ValueError("Missing/mismatched accession identity or title: " + accession)
    return {"accession": accession, "title": fields["title"], "source_file": path.as_posix()}


def write_tsv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def audit(out):
    reference_rows, reference_summary, tag_rows, feature_summary = [], [], [], []
    source_files = []
    for accession, suffix in REFERENCES.items():
        path = RAW / f"{accession}_feature_reference.csv"
        source_files.extend([path, RAW / f"{accession}_feature_reference_{suffix}.csv.gz"])
        with path.open(newline="", encoding="utf-8-sig") as stream:
            original, normalized, rows = parse_reference(stream)
        for row in rows:
            reference_rows.append({
                "reference_file": path.name, "reference_accession": accession,
                "tag_id": row["id"], "name": row["name"],
                "feature_type": row["feature_type"], "condition_label": row["multiplexed_sample"],
            })
        reference_summary.append({"file": path.name, "original_headers": original,
                                  "normalized_headers": normalized,
                                  "labels": sorted({row["multiplexed_sample"] for row in rows}),
                                  "tag_ids": sorted(row["id"] for row in rows)})
    for accession, suffix in FEATURES.items():
        path = RAW / f"{accession}_count{suffix}_features.tsv.gz"
        source_files.append(path)
        with gzip.open(path, "rt", newline="", encoding="utf-8-sig") as stream:
            counts, tags = parse_features(stream)
        tag_rows.extend(dict(feature_file=path.name, library_accession=accession, **tag) for tag in tags)
        feature_summary.append({"file": path.name, "rows": sum(counts.values()),
                                "feature_type_rows": counts,
                                "cmo_tag_ids": sorted(tag["tag_id"] for tag in tags
                                                      if re.fullmatch(r"CMO\d+", tag["tag_id"]))})
    accession_rows = []
    for accession in sorted(set(REFERENCES) | set(FEATURES)):
        path = RAW / f"{accession}.txt"
        source_files.append(path)
        accession_rows.append(parse_accession(path, accession))
    presence = []
    for feature in feature_summary:
        identifiers = {row["tag_id"] for row in tag_rows if row["feature_file"] == feature["file"]}
        for reference in reference_rows:
            presence.append({"feature_file": feature["file"], "reference_file": reference["reference_file"],
                             "tag_id": reference["tag_id"], "present": str(reference["tag_id"] in identifiers).lower()})
    write_tsv(out / "reference_labels.tsv", REFERENCE_FIELDS, reference_rows)
    write_tsv(out / "feature_tags.tsv", TAG_FIELDS, tag_rows)
    write_tsv(out / "reference_presence.tsv", PRESENCE_FIELDS, presence)
    manifest = []
    for path in sorted(source_files):
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        manifest.append({"path": path.as_posix(), "sha256": digest, "bytes": path.stat().st_size})
    result = {
        "analysis": "metadata correction only", "analysis_id": "DY1-P01.source_v2",
        "supersedes": {"analysis_id": "DY1-P01.source_v1",
                       "output": "analysis/research/runs/DY1_source_v1/source_qualification.json",
                       "fields": ["cmo_references: GSM9964564 labels", "scRNA_condition_batch"],
                       "scope": "Only these interpretations are corrected; v1 artifacts remain unchanged."},
        "corrections": [
            "Whitespace-normalized CSV headers recover the reference label Naive for CMO301-303 in GSM9964564.",
            "Condition/library confounding is unresolved. Feature-row presence cannot establish assigned cells, condition support or absence of confounding.",
        ],
        "accession_records": accession_rows, "cmo_references": reference_summary,
        "feature_tables": feature_summary, "input_manifest": manifest,
        "join_semantics": "All reference-file/tag-ID by feature-file membership checks, including negative matches; neither pairing nor cell assignment. Tag identifiers are local to their source record.",
        "scRNA_condition_batch": "unresolved; no cell assignments or count matrices inspected",
        "animal_pool_identity": "unknown", "animal_independence": "unknown",
        "biological_acceptance": "not_assessed",
        "stage_status": "Stage 0 metadata correction only; stages 1-8 remain unexecuted in this task.",
        "interpretation_limit": "Labels describe reference records; feature identifiers describe available rows. Neither identifies animals, pools, cell conditions, biological effects or mechanisms.",
    }
    (out / "source_qualification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    verification = verify(RAW, out)
    (out / "verification.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(verification))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    audit(parser.parse_args().output)
