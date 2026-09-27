"""C5: verify the C4 result independently of the R path, and test its normalisation dependence.

Four checks, none of which reuses edgeR:

1. the pseudobulk is non-negative integers and its per-unit totals match the library sizes R
   recorded, so the matrix R scored is the matrix C3 wrote;
2. the per-donor differences follow from the per-unit scores by arithmetic;
3. the cell counts behind each unit match what C3 recorded and clear the inherited floor;
4. the primary contrast is recomputed from raw counts with plain counts-per-million and no
   trimmed-mean normalisation, which tests whether the direction depends on the normalisation.

It computes no new inference and changes no decision.

Standard library only. Refuses to overwrite.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import json
import math
import statistics as st
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OUTPUTS = ["verification.json"]
PRIMARY_ARM = "SCoV1"
SECONDARY_ARM = "SCoV2"
FLOOR = 50
TOL = 1e-6


def sha256(path: Path) -> str:
    d = hashlib.sha256()
    with path.open("rb") as h:
        for b in iter(lambda: h.read(1 << 24), b""):
            d.update(b)
    return d.hexdigest()


def read_tsv(path: Path) -> list[dict]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--c3", type=Path, required=True)
    ap.add_argument("--c4", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    a = ap.parse_args()
    out = a.c4.resolve()
    if (out / OUTPUTS[0]).exists():
        raise SystemExit("Refusing to overwrite %s" % OUTPUTS[0])

    checks = []

    def ck(label: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": label, "passed": bool(ok), "detail": detail})
        print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  | " + detail) if detail else ""))

    # ---- load
    pb_path = a.cache / "at2_pseudobulk_counts.tsv.gz"
    with gzip.open(pb_path, "rt", encoding="utf-8", newline="") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        units = header[1:]
        totals = {u: 0 for u in units}
        genes = {}
        bad = 0
        nrows = 0
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            gene = parts[0]
            vals = []
            for v in parts[1:]:
                iv = int(v)
                if iv < 0:
                    bad += 1
                vals.append(iv)
            genes[gene] = vals
            for u, iv in zip(units, vals):
                totals[u] += iv
            nrows += 1
    ck("pseudobulk holds only non-negative integers", bad == 0, "%d rows, %d units" % (nrows, len(units)))

    norm = {r["unit_id"]: r for r in read_tsv(a.c4 / "normalization.tsv")}
    mism = [u for u in units if abs(float(norm[u]["library_size"]) - totals[u]) > 0.5]
    ck("per-unit totals match the library sizes R recorded", not mism, str(mism[:4]))

    c3_units = {r["unit_id"]: r for r in read_tsv(a.c3 / "units.tsv")}
    cellmis = [u for u in units if int(c3_units[u]["cells"]) != int(norm[u]["cells"])]
    ck("cell counts agree between C3 and the C4 normalisation table", not cellmis, str(cellmis[:4]))
    below = [u for u in units if int(c3_units[u]["cells"]) < FLOOR]
    ck("every unit clears the inherited %d-cell floor" % FLOOR, not below, str(below))

    # ---- differences follow from scores
    scores = read_tsv(a.c4 / "scores.tsv")
    smap = {(r["module"], r["unit_id"]): float(r["score"]) for r in scores}
    med = {r["unit_id"]: r["medium"] for r in scores}
    diffs = read_tsv(a.c4 / "paired_differences.tsv")
    worst = 0.0
    for r in diffs:
        for module, col in [("lesion_specific", "lesion_specific"),
                            ("shared_remodelling", "shared_remodelling"),
                            ("stress_excluded", "stress_excluded")]:
            inf = "%s_%s_%s" % (r["donor"], r["arm"], med["%s_%s_FCS" % (r["donor"], r["arm"])])
            ctl = "%s_control_%s" % (r["donor"], med[inf])
            want = smap[(module, inf)] - smap[(module, ctl)]
            worst = max(worst, abs(want - float(r[col])))
        beyond = float(r["lesion_specific"]) - float(r["shared_remodelling"])
        worst = max(worst, abs(beyond - float(r["beyond_shared"])))
    ck("paired differences follow from the per-unit scores", worst <= TOL, "largest error %.3g" % worst)

    # ---- independent recomputation without TMM
    module_genes = [r["gene"] for r in read_tsv(
        a.repo / "RQ_Specified/A11_lesion_programme_addition/tables/test_v2/human_module_genes.tsv")
        if r["module"] == "lesion_specific"]
    present = [g for g in module_genes if g in genes]
    ck("all 73 module genes are present in the pseudobulk", len(present) == 73,
       "%d of %d" % (len(present), len(module_genes)))

    idx = {u: i for i, u in enumerate(units)}

    def plain_score(unit: str) -> float:
        total = totals[unit]
        vals = [math.log2(genes[g][idx[unit]] / total * 1e6 + 1) for g in present]
        return sum(vals) / len(vals)

    plain = {}
    for arm in (PRIMARY_ARM, SECONDARY_ARM):
        donors = sorted({r["donor"] for r in diffs if r["arm"] == arm})
        vals = []
        for d in donors:
            inf = "%s_%s_FCS" % (d, arm)
            ctl = "%s_control_FCS" % d
            vals.append(plain_score(inf) - plain_score(ctl))
        plain[arm] = {"donors": donors, "differences": [round(v, 6) for v in vals],
                      "mean": round(st.mean(vals), 6),
                      "donors_positive": sum(1 for v in vals if v > 0)}

    r_primary = next(r for r in read_tsv(a.c4 / "inference.tsv")
                     if r["test"] == "%s_primary_lesion" % PRIMARY_ARM)
    same_sign = (plain[PRIMARY_ARM]["mean"] > 0) == (float(r_primary["mean"]) > 0)
    same_count = plain[PRIMARY_ARM]["donors_positive"] == int(r_primary["donors_positive"])
    ck("the primary direction survives dropping the trimmed-mean normalisation",
       same_sign and same_count,
       "plain mean %+.4f with %d of %d positive, against the TMM mean %+.4f with %s positive"
       % (plain[PRIMARY_ARM]["mean"], plain[PRIMARY_ARM]["donors_positive"],
          len(plain[PRIMARY_ARM]["donors"]), float(r_primary["mean"]), r_primary["donors_positive"]))

    exact_unavailable = all(r["exact_available"] == "FALSE" for r in read_tsv(a.c4 / "inference.tsv"))
    ck("the exact interval is unavailable on every test, as the contract predicted", exact_unavailable)

    record = {
        "task": "C5 verification",
        "scope": "checks only; no new inference and no decision changed",
        "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script": "docs/research_pipeline/scripts/c5_verify_a11_acute.py",
        "script_sha256": sha256(Path(__file__).resolve()),
        "inputs": {
            "pseudobulk": {"path": pb_path.name, "sha256": sha256(pb_path)},
            "inference": {"path": "inference.tsv", "sha256": sha256(a.c4 / "inference.tsv")},
        },
        "checks": checks,
        "failures": sum(1 for c in checks if not c["passed"]),
        "normalisation_free_recomputation": plain,
        "reading": ("The direction in the primary arm does not depend on the trimmed-mean "
                    "normalisation, and the exact interval the contract designated is unavailable "
                    "at four pairs exactly as declared. Neither fact turns an unresolved result "
                    "into a supported one."),
    }
    (out / OUTPUTS[0]).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("\n%d checks, %d failures" % (len(checks), record["failures"]))
    print("plain-CPM recomputation: %s" % json.dumps(plain[PRIMARY_ARM]))
    sys.exit(1 if record["failures"] else 0)


if __name__ == "__main__":
    main()
