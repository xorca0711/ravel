#!/usr/bin/env python
"""Wp-R0: qualify the Wang 2025 (PGAM) deposited sources before any reanalysis.

Metadata recovery only. The script reads GEO records and the headers of the
deposited matrices, verifies them against the recorded acquisition hashes, and
writes an inventory plus a per-stage eligibility table. It never reads an
expression value, computes a score or tests a hypothesis.

Standard library only, so the governed runner needs no scientific stack.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path


SERIES = {
    "GSE289733": "single-cell RNA-seq, Th17n/Th17p at 25 mM and 1 mM glucose",
    "GSE290297": "population RNA-seq, Th17n/Th17p with EGCG, DHEA and solvent controls",
    "GSE138266": "human MS/control blood and CSF leukocytes, reused by the source paper",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_soft_samples(text: str) -> list[dict]:
    """Return one record per ^SAMPLE block, keeping repeated keys as lists."""
    samples: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        if line.startswith("^SAMPLE"):
            current = {"gsm": line.split("=", 1)[1].strip()}
            samples.append(current)
        elif current is not None and line.startswith("!Sample_"):
            key, _, value = line[len("!Sample_"):].partition(" = ")
            current.setdefault(key.strip(), []).append(value.strip())
    return samples


def characteristics(sample: dict) -> dict:
    fields = {}
    for item in sample.get("characteristics_ch1", []):
        key, _, value = item.partition(": ")
        fields[key.strip().lower()] = value.strip()
    return fields


def first(sample: dict, key: str) -> str:
    values = sample.get(key, [])
    return values[0] if values else ""


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True,
                        help="Directory holding acquisition_v1.json and the recorded GEO files")
    parser.add_argument("--output", required=True, help="Run directory supplied by the runner")
    args = parser.parse_args()
    data_root = Path(args.data_root)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    manifest = json.loads((data_root / "acquisition_v1.json").read_text(encoding="utf-8"))
    verified = []
    for record in manifest["files"]:
        path = data_root / record["file"]
        digest = sha256(path)
        verified.append({"file": record["file"], "url": record["url"], "bytes": record["bytes"],
                         "recorded_sha256": record["sha256"], "observed_sha256": digest,
                         "match": digest == record["sha256"] and path.stat().st_size == record["bytes"]})
    if not all(item["match"] for item in verified):
        raise SystemExit("Input hash or size mismatch; stop before any qualification claim")

    # --- single-cell series -------------------------------------------------
    sc_text = (data_root / "GSE289733_samples.soft.txt").read_text(encoding="utf-8", errors="replace")
    sc_samples = parse_soft_samples(sc_text)
    sc_rows = []
    for sample in sc_samples:
        fields = characteristics(sample)
        sc_rows.append({
            "series_order": str(len(sc_rows) + 1),
            "gsm": sample["gsm"], "title": first(sample, "title"),
            "cell_type": fields.get("cell type", ""), "animal_id": fields.get("animal id", ""),
            "glucose": fields.get("glucose concentration", ""),
            "instrument": first(sample, "instrument_model"),
            "sample_supplementary_files": "; ".join(v for v in sample.get("supplementary_file", []) if v != "NONE"),
        })
    write_csv(output / "scrna_sample_inventory.csv", sc_rows,
              ["series_order", "gsm", "title", "cell_type", "animal_id", "glucose",
               "instrument", "sample_supplementary_files"])

    with gzip.open(data_root / "GSE289733_filtered_feature_bc_matrix_barcodes.tsv.gz", "rt") as handle:
        barcodes = [line.strip() for line in handle if line.strip()]
    suffixes = Counter(barcode.rsplit("-", 1)[1] for barcode in barcodes)
    suffix_rows = [{"aggr_suffix": key, "n_barcodes": value,
                    "declared_gsm": "", "mapping_status": "unresolved_in_deposit"}
                   for key, value in sorted(suffixes.items(), key=lambda item: int(item[0]))]
    write_csv(output / "scrna_library_suffix_inventory.csv", suffix_rows,
              ["aggr_suffix", "n_barcodes", "declared_gsm", "mapping_status"])

    with gzip.open(data_root / "GSE289733_filtered_feature_bc_matrix_features.tsv.gz", "rt") as handle:
        features = [line.rstrip("\n").split("\t") for line in handle if line.strip()]
    feature_types = Counter(row[2] for row in features if len(row) > 2)

    # --- bulk series --------------------------------------------------------
    bulk_text = (data_root / "GSE290297_samples.soft.txt").read_text(encoding="utf-8", errors="replace")
    bulk_samples = parse_soft_samples(bulk_text)
    bulk_rows = []
    for sample in bulk_samples:
        fields = characteristics(sample)
        title = first(sample, "title")
        parts = title.split("_")
        bulk_rows.append({
            "gsm": sample["gsm"], "title": title,
            "matrix_column": parts[0],
            "sequencing_id": parts[1] if len(parts) > 1 else "",
            "cell_type": fields.get("cell type", ""), "treatment": fields.get("treatment", ""),
            "divisions": fields.get("divisions", ""),
            "animal_id": fields.get("animal id", fields.get("mouse", "")),
            "library_name": "; ".join(sample.get("description", [])),
        })
    write_csv(output / "bulk_sample_inventory.csv", bulk_rows,
              ["gsm", "title", "matrix_column", "sequencing_id", "cell_type",
               "treatment", "divisions", "animal_id", "library_name"])

    with gzip.open(data_root / "GSE290297_collected_inhibitors_tpm_4geo.csv.gz", "rt") as handle:
        header = handle.readline().rstrip("\n").split(",")
        n_genes = sum(1 for _ in handle)
    matrix_columns = header[1:]
    declared = {row["matrix_column"]: row for row in bulk_rows}
    join_rows = []
    for column in matrix_columns:
        row = declared.get(column)
        join_rows.append({"matrix_column": column, "gsm": row["gsm"] if row else "",
                          "title": row["title"] if row else "",
                          "join_status": "matched" if row else "unmatched_matrix_column"})
    for column, row in sorted(declared.items()):
        if column not in matrix_columns:
            join_rows.append({"matrix_column": column, "gsm": row["gsm"], "title": row["title"],
                              "join_status": "sample_without_matrix_column"})
    write_csv(output / "bulk_matrix_column_join.csv", join_rows,
              ["matrix_column", "gsm", "title", "join_status"])

    design = Counter((row["cell_type"], row["treatment"], row["divisions"]) for row in bulk_rows)
    design_rows = [{"cell_type": key[0], "treatment": key[1], "divisions": key[2], "n_libraries": value}
                   for key, value in sorted(design.items())]
    write_csv(output / "bulk_design_counts.csv", design_rows,
              ["cell_type", "treatment", "divisions", "n_libraries"])

    # --- human reuse series -------------------------------------------------
    human_text = (data_root / "GSE138266_samples.soft.txt").read_text(encoding="utf-8", errors="replace")
    human_samples = parse_soft_samples(human_text)
    human_rows = []
    for sample in human_samples:
        fields = characteristics(sample)
        title = first(sample, "title")
        donor, _, tissue_suffix = title.rpartition("_")
        human_rows.append({
            "gsm": sample["gsm"], "title": title,
            "donor_code_from_title": donor, "tissue_from_title": tissue_suffix,
            "disease": fields.get("disease condition", ""),
            "source_name": first(sample, "source_name_ch1"),
            "declared_characteristics": "; ".join(sample.get("characteristics_ch1", [])),
            "supplementary_files": "; ".join(v for v in sample.get("supplementary_file", []) if v != "NONE"),
        })
    write_csv(output / "human_sample_inventory.csv", human_rows,
              ["gsm", "title", "donor_code_from_title", "tissue_from_title", "disease",
               "source_name", "declared_characteristics", "supplementary_files"])
    human_design = Counter((row["disease"], row["source_name"]) for row in human_rows)

    donors: dict[str, dict] = {}
    for row in human_rows:
        entry = donors.setdefault(row["donor_code_from_title"],
                                  {"donor_code_from_title": row["donor_code_from_title"],
                                   "disease": row["disease"], "tissues": set(), "gsms": []})
        entry["tissues"].add(row["tissue_from_title"])
        entry["gsms"].append(row["gsm"])
    donor_rows = [{"donor_code_from_title": key, "disease": value["disease"],
                   "tissues": "+".join(sorted(value["tissues"])),
                   "n_samples": len(value["gsms"]), "gsms": "; ".join(sorted(value["gsms"])),
                   "donor_id_source": "sample title only; no declared donor characteristic field"}
                  for key, value in sorted(donors.items())]
    write_csv(output / "human_donor_pairing.csv", donor_rows,
              ["donor_code_from_title", "disease", "tissues", "n_samples", "gsms", "donor_id_source"])

    paired_donors = sum(1 for row in donor_rows if row["n_samples"] > 1)
    donors_per_disease = Counter(row["disease"] for row in donor_rows)

    # --- eligibility --------------------------------------------------------
    animal_labels = sorted({row["animal_id"] for row in sc_rows if row["animal_id"]})
    bulk_animal_labels = sorted({row["animal_id"] for row in bulk_rows if row["animal_id"]})
    unmatched = [row for row in join_rows if row["join_status"] != "matched"]
    per_sample_matrices = sum(1 for row in sc_rows if row["sample_supplementary_files"])
    eligibility = [
        {"stage": "Wp-R1", "target": "single-cell signature and state reproduction",
         "status": "eligible_descriptive" if len(suffix_rows) == len(sc_rows) else "blocked",
         "reason": (f"the aggregated matrix carries {len(suffix_rows)} suffixes for {len(sc_rows)} declared "
                    f"libraries and {per_sample_matrices} per-sample matrices; the deposit states no "
                    f"suffix-to-GSM order, so condition labels must be re-derived. Animal labels present: "
                    f"{', '.join(animal_labels) if animal_labels else 'none'}")},
        {"stage": "Wp-R2", "target": "Compass reaction scores",
         "status": "blocked_external",
         "reason": ("Compass needs a solver licence, and the published run used scVI-imputed input with "
                    "lambda 0 and no meta-reactions; neither the fitted model nor the imputed matrix is deposited")},
        {"stage": "Wp-R3", "target": "bulk EGCG and DHEA contrasts",
         "status": "eligible_descriptive" if not unmatched else "blocked",
         "reason": (f"{len(matrix_columns)} matrix columns against {len(bulk_rows)} sample records with "
                    f"{len(unmatched)} unmatched; the deposit supplies TPM only and "
                    f"{'no animal field' if not bulk_animal_labels else 'animal labels ' + ', '.join(bulk_animal_labels)}, "
                    "so the library is the only verifiable unit")},
        {"stage": "Wp-R4", "target": "human MS signature transport",
         "status": "eligible_descriptive",
         "reason": (f"{len(human_rows)} sample records resolve to {len(donor_rows)} donor codes recovered from "
                    f"sample titles ({paired_donors} with both tissues); donors are the unit, but CD4 identity, "
                    "pseudobulk construction and any clinical covariate must be re-derived or remain unknown")},
        {"stage": "Wp-R5", "target": "flow cytometry, 13C tracing, Legendplex, EAE and histology",
         "status": "blocked_no_deposit",
         "reason": "no numerical assay values are deposited for these panels; only figure images exist"},
    ]
    write_csv(output / "stage_eligibility.csv", eligibility, ["stage", "target", "status", "reason"])

    results = {
        "schema": "wp_r0_source_qualification/v1",
        "series": SERIES,
        "inputs_verified": verified,
        "single_cell": {
            "n_sample_records": len(sc_rows),
            "animal_labels": animal_labels,
            "conditions": sorted({row["cell_type"] + "|" + row["glucose"] for row in sc_rows}),
            "per_sample_supplementary_matrices": per_sample_matrices,
            "n_barcodes_in_aggregated_matrix": len(barcodes),
            "n_unique_barcodes": len(set(barcodes)),
            "n_aggr_suffixes": len(suffix_rows),
            "barcodes_per_suffix": {row["aggr_suffix"]: row["n_barcodes"] for row in suffix_rows},
            "n_features": len(features),
            "feature_types": dict(feature_types),
            "suffix_to_gsm_mapping": "not stated in the deposit",
        },
        "bulk": {
            "n_sample_records": len(bulk_rows),
            "n_matrix_columns": len(matrix_columns),
            "n_genes_in_matrix": n_genes,
            "unmatched_joins": unmatched,
            "design_counts": {"|".join(key): value for key, value in sorted(design.items())},
            "animal_labels": bulk_animal_labels,
            "value_scale": "TPM as deposited; no estimated or raw counts",
        },
        "human": {
            "n_sample_records": len(human_rows),
            "design_counts": {"|".join(key): value for key, value in sorted(human_design.items())},
            "n_donor_codes": len(donor_rows),
            "donors_per_disease": dict(sorted(donors_per_disease.items())),
            "donors_with_both_tissues": paired_donors,
            "donor_id_source": "recovered from sample titles; the deposit declares no donor characteristic field",
        },
        "stage_eligibility": eligibility,
        "interpretation_limit": (
            "Source identity and design inventory only. Nothing here establishes independent biological "
            "replication, metabolic flux, protein-level effects or agreement with the published figures."),
    }
    (output / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
