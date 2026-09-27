"""A13 coverage: count complete macrophage, fibroblast and epithelial triads.

Obeys config/a13_triad_coverage_spec.json, committed before this produced a count. It
reads deposited annotation only, fits nothing and estimates nothing.

It first reproduces the earlier trial's per-donor flags for both IPF cohorts at all three
floors, and refuses to report its new counts if any flag disagrees. Then it counts the Kim
lung adenocarcinoma cohort, which the gate has never counted, per sample and per patient as
a complete paired triad.

Standard library only. Hash-verified inputs. Refuses to overwrite.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
OUT = HERE / "tables"
SPEC = HERE / "config/a13_triad_coverage_spec.json"
PRIOR_TABLE = ROOT / "Research Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_liana_robustness/complete_triad_coverage.csv"
OUTPUTS = ["a13_triad_counts.tsv", "a13_reproduction_check.tsv", "a13_coverage_run.json"]
FLOORS = [30, 50, 100]


def sha256(path: Path) -> str:
    d = hashlib.sha256()
    with path.open("rb") as h:
        for b in iter(lambda: h.read(1 << 24), b""):
            d.update(b)
    return d.hexdigest()


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def open_text(path: Path):
    return gzip.open(path, "rt", encoding="utf-8-sig", newline="") if path.suffix == ".gz" \
        else open(path, "r", encoding="utf-8-sig", newline="")


def read_rows(path: Path, delimiter: str) -> list[dict]:
    with open_text(path) as fh:
        return list(csv.DictReader(fh, delimiter=delimiter))


def classify(label: str, mapping: dict) -> str | None:
    for compartment, labels in mapping.items():
        if label in labels:
            return compartment
    return None


def count_cells(rows: list[dict], label_col: str, unit_col: str, mapping: dict) -> dict:
    """Per unit, the cell count of every label that belongs to a compartment."""
    counts: dict[str, dict[str, dict[str, int]]] = {}
    for r in rows:
        compartment = classify(r[label_col], mapping)
        if compartment is None:
            continue
        unit = r[unit_col]
        counts.setdefault(unit, {"epithelial": {}, "fibroblast": {}, "myeloid": {}})
        per_label = counts[unit][compartment]
        per_label[r[label_col]] = per_label.get(r[label_col], 0) + 1
    return counts


def largest(per_label: dict) -> int:
    return max(per_label.values()) if per_label else 0


def pooled(per_label: dict) -> int:
    return sum(per_label.values())


def complete(c: dict, floor: int, rule: str) -> bool:
    """The earlier gate required one single label to reach the floor. Pooling is a sensitivity."""
    size = largest if rule == "single_label" else pooled
    return all(size(c[k]) >= floor for k in ("epithelial", "fibroblast", "myeloid"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", type=Path, default=ROOT)
    data_root = ap.parse_args().data_root.resolve()

    OUT.mkdir(exist_ok=True)
    existing = [n for n in OUTPUTS if (OUT / n).exists()]
    if existing:
        raise SystemExit("Refusing to overwrite: %s" % existing)
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    if spec["counts_produced_at_declaration"] is not False:
        raise SystemExit("the spec must assert that no count existed at declaration")
    floor_primary = spec["definition_of_a_complete_triad"]["floors"]["primary"]

    paths = {
        "GSE136831": data_root / "raw_data/GSE136831/GSE136831_AllCells.Samples.CellType.MetadataTable.txt.gz",
        "GSE135893": data_root / "raw_data/GSE135893/GSE135893_IPF_metadata.csv.gz",
        "GSE131907": data_root / "raw_data/GSE131907/GSE131907_Lung_Cancer_cell_annotation.txt.gz",
    }
    for name, p in paths.items():
        if not p.exists():
            raise SystemExit("missing %s for %s" % (p, name))

    reused = spec["compartment_labels"]["reused_verbatim_from_the_earlier_trial"]
    rows_out = []
    check_rows = []

    # ---------------------------------------------------------------- the two IPF cohorts
    ipf_counts = {}
    for cohort in ["GSE136831", "GSE135893"]:
        cfg = reused[cohort]
        mapping = {"epithelial": cfg["epithelial"], "fibroblast": cfg["fibroblast"], "myeloid": cfg["myeloid"]}
        delim = "\t" if paths[cohort].name.endswith(".txt.gz") else ","
        rows = read_rows(paths[cohort], delim)
        rows = [{k: (v.strip('"') if isinstance(v, str) else v) for k, v in r.items()} for r in rows]
        counts = count_cells(rows, cfg["label_column"], cfg["patient_column"], mapping)
        disease = {}
        for r in rows:
            disease[r[cfg["patient_column"]]] = r[cfg["disease_column"]]
        ipf_counts[cohort] = (counts, disease)
        for unit, c in sorted(counts.items()):
            for floor in FLOORS:
                for rule in ("single_label", "pooled"):
                    size = largest if rule == "single_label" else pooled
                    rows_out.append({"cohort": cohort, "unit": unit, "unit_kind": "donor",
                                     "group": disease.get(unit, ""), "floor": floor, "rule": rule,
                                     "epithelial": size(c["epithelial"]),
                                     "fibroblast": size(c["fibroblast"]),
                                     "myeloid": size(c["myeloid"]),
                                     "complete_triad": complete(c, floor, rule),
                                     "epithelial_definition": "primary"})
        print("%s: %d donors counted" % (cohort, len(counts)), flush=True)

    # ---------------------------------------------------------------- reproduction check
    prior = read_rows(PRIOR_TABLE, ",")
    mine = {(r["cohort"], r["unit"], int(r["floor"])): bool(r["complete_triad"])
            for r in rows_out
            if r["cohort"] in ("GSE136831", "GSE135893") and r["rule"] == "single_label"}
    disagreements = 0
    for p in prior:
        key = (p["cohort"], p["donor"], int(p["floor"]))
        want = p["complete_triad"] == "True"
        got = mine.get(key)
        agree = got is not None and got == want
        if not agree:
            disagreements += 1
        check_rows.append({"cohort": p["cohort"], "donor": p["donor"], "floor": p["floor"],
                           "earlier_trial": want, "recomputed": "missing" if got is None else got,
                           "agrees": agree})
    print("reproduction check: %d prior rows, %d disagreements" % (len(prior), disagreements), flush=True)
    with open(OUT / OUTPUTS[1], "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(check_rows[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in check_rows:
            w.writerow(r)
    if disagreements:
        raise SystemExit("STOP: this script does not reproduce the earlier triad flags; "
                         "new counts are not reported. See %s" % OUTPUTS[1])

    # ---------------------------------------------------------------- the new cohort
    cfg = spec["compartment_labels"]["declared_here_for_the_new_cohort"]["GSE131907"]
    rows = read_rows(paths["GSE131907"], "\t")
    rows = [r for r in rows if r["Sample_Origin"] in cfg["origins_in_scope"]]
    pat = re.compile(r"^LUNG_([NT])(\d+)$")
    for r in rows:
        m = pat.match(r["Sample"])
        r["_patient"] = m.group(2) if m else ""
        r["_origin"] = {"N": "normal", "T": "tumour"}.get(m.group(1), "") if m else ""
    unmapped = sum(1 for r in rows if not r["_patient"])
    if unmapped:
        raise SystemExit("%d cells have a sample name the patient rule does not match" % unmapped)

    kim = {}
    for variant, epi in [("primary", cfg["epithelial_primary"]), ("sensitivity", cfg["epithelial_sensitivity"])]:
        mapping = {"epithelial": epi, "fibroblast": cfg["fibroblast"], "myeloid": cfg["myeloid"]}
        per_sample: dict[tuple, dict] = {}
        for r in rows:
            compartment = classify(r[cfg["label_column"]], mapping)
            if compartment is None:
                continue
            key = (r["_patient"], r["_origin"])
            per_sample.setdefault(key, {"epithelial": {}, "fibroblast": {}, "myeloid": {}})
            per_label = per_sample[key][compartment]
            label = r[cfg["label_column"]]
            per_label[label] = per_label.get(label, 0) + 1
        for (patient, origin), c in sorted(per_sample.items()):
            for floor in FLOORS:
                for rule in ("single_label", "pooled"):
                    size = largest if rule == "single_label" else pooled
                    rows_out.append({"cohort": "GSE131907", "unit": "%s_%s" % (patient, origin),
                                     "unit_kind": "sample", "group": origin, "floor": floor,
                                     "rule": rule,
                                     "epithelial": size(c["epithelial"]),
                                     "fibroblast": size(c["fibroblast"]),
                                     "myeloid": size(c["myeloid"]),
                                     "complete_triad": complete(c, floor, rule),
                                     "epithelial_definition": variant})
        patients = sorted({p for p, _ in per_sample})
        paired: dict[str, dict[int, list]] = {"single_label": {}, "pooled": {}}
        for rule in ("single_label", "pooled"):
            for floor in FLOORS:
                both = [p for p in patients
                        if all((p, o) in per_sample and complete(per_sample[(p, o)], floor, rule)
                               for o in ("tumour", "normal"))]
                paired[rule][floor] = both
                for p in patients:
                    rows_out.append({"cohort": "GSE131907", "unit": p,
                                     "unit_kind": "patient_paired",
                                     "group": "tumour_and_normal", "floor": floor, "rule": rule,
                                     "epithelial": "", "fibroblast": "", "myeloid": "",
                                     "complete_triad": p in both,
                                     "epithelial_definition": variant})
        kim[variant] = {
            "patients_seen": len(patients),
            "patients_with_both_samples": len([p for p in patients
                                               if (p, "tumour") in per_sample
                                               and (p, "normal") in per_sample]),
            "complete_paired_triads_single_label": {str(f): len(v) for f, v in paired["single_label"].items()},
            "complete_paired_triads_pooled": {str(f): len(v) for f, v in paired["pooled"].items()},
            "paired_patients_at_primary_floor_single_label": paired["single_label"][floor_primary],
        }
        print("GSE131907 %s epithelial definition: paired triads single-label %s, pooled %s"
              % (variant, {f: len(v) for f, v in paired["single_label"].items()},
                 {f: len(v) for f, v in paired["pooled"].items()}), flush=True)

    with open(OUT / OUTPUTS[0], "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_out[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows_out:
            w.writerow(r)

    primary = kim["primary"]["complete_paired_triads_single_label"][str(floor_primary)]
    gate = spec["question"]["joint_model_floor_patients"]
    verdict = ("gate met: %d patients hold a complete paired triad at the %d-cell floor, at or above the %d-patient floor"
               % (primary, floor_primary, gate) if primary >= gate else
               "gate not met: %d patients hold a complete paired triad at the %d-cell floor, below the %d-patient floor"
               % (primary, floor_primary, gate))

    record = {
        "stage": "A13 coverage",
        "scope": "counts only; nothing fitted",
        "governed_by": {"file": rel(SPEC), "sha256": sha256(SPEC)},
        "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script": rel(Path(__file__).resolve()),
        "script_sha256": sha256(Path(__file__).resolve()),
        "inputs": {rel(p): sha256(p) for p in paths.values()},
        "prior_table": {"path": rel(PRIOR_TABLE), "sha256": sha256(PRIOR_TABLE),
                        "rows": len(prior), "disagreements": disagreements},
        "floors": FLOORS,
        "primary_floor": floor_primary,
        "primary_rule": "one single cell label at or above the floor; pooling is a declared sensitivity",
        "ipf_cohorts_at_primary_floor_single_label": {
            cohort: {
                group: sum(1 for r in rows_out
                           if r["cohort"] == cohort and r["floor"] == floor_primary
                           and r["rule"] == "single_label" and r["complete_triad"]
                           and str(r["group"]).lower().startswith(group.lower()))
                for group in ["IPF", "Control"]
            } for cohort in ["GSE136831", "GSE135893"]
        },
        "kim_cohort": kim,
        "joint_model_floor_patients": gate,
        "verdict": verdict,
        "nothing_fitted": True,
    }
    (OUT / OUTPUTS[2]).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("\nVERDICT: %s" % verdict)
    print("wrote %s" % OUTPUTS)


if __name__ == "__main__":
    main()
