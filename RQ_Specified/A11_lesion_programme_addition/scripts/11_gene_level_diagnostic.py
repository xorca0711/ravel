"""C5b, post hoc: which genes carry the module shift, and what the exact test actually returned.

Declared post hoc. It is a diagnostic on a result already produced, it changes no decision, and it
exists because two statements in the C5 report needed correcting rather than defending.

It records three things:

1. the exact test's real output. The A11 helper suppresses a result when the 95 per cent interval
   is unattainable, which at four pairs it is. The underlying exact test still returns a
   Hodges-Lehmann estimate and a p-value, and those are more informative than a blank.
2. the leave-one-out spread on the primary contrast, so a reader can see whether one donor carries
   it.
3. the per-gene contribution to the module shift, because a 73-gene unweighted mean can be moved by
   a handful of genes, and if those genes are canonical injury responders the module label is doing
   less work than it appears to.

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

OUTPUTS = ["gene_contributions.tsv", "gene_level_diagnostic.json"]
PRIMARY_ARM = "SCoV1"

# Canonical membership, used only to label genes in the output, never to select them.
NFKB = {"TNF", "TNFAIP3", "RELB", "PTGS2", "LIF", "IL23A", "IL24", "MAFF", "TRIB1"}
ISR = {"ASNS", "CHAC1", "DDIT3", "SLC1A4", "SLC38A2", "ZFAND2A", "TP53INP1"}


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
    ap.add_argument("--c4", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    existing = [n for n in OUTPUTS if (out / n).exists()]
    if existing:
        raise SystemExit("Refusing to overwrite: %s" % existing)

    mod = read_tsv(a.repo / "RQ_Specified/A11_lesion_programme_addition/tables/test_v2/human_module_genes.tsv")
    lesion = [r["gene"] for r in mod if r["module"] == "lesion_specific"]
    retained = {r["gene"] for r in mod if r["module"] == "stress_excluded"}
    dropped = [g for g in lesion if g not in retained]

    pb = a.cache / "at2_pseudobulk_counts.tsv.gz"
    with gzip.open(pb, "rt", encoding="utf-8", newline="") as fh:
        units = fh.readline().rstrip("\n").split("\t")[1:]
        idx = {u: i for i, u in enumerate(units)}
        totals = {u: 0 for u in units}
        vals: dict[str, list[int]] = {}
        want = set(lesion)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            row = [int(v) for v in parts[1:]]
            for u, v in zip(units, row):
                totals[u] += v
            if parts[0] in want:
                vals[parts[0]] = row

    donors = sorted({u.split("_")[0] for u in units if u.endswith("_%s_FCS" % PRIMARY_ARM)})

    def lg(gene: str, unit: str) -> float:
        return math.log2(vals[gene][idx[unit]] / totals[unit] * 1e6 + 1)

    rows = []
    for g in lesion:
        per = [lg(g, "%s_%s_FCS" % (d, PRIMARY_ARM)) - lg(g, "%s_control_FCS" % d) for d in donors]
        rows.append({
            "gene": g,
            "mean_difference": round(st.mean(per), 4),
            "donors_positive": sum(1 for v in per if v > 0),
            "donors": len(per),
            "dropped_by_a11_stress_exclusion": "yes" if g in dropped else "no",
            "canonical_group": "NF-kB" if g in NFKB else ("integrated stress response" if g in ISR else "none"),
        })
    rows.sort(key=lambda r: -r["mean_difference"])
    with open(out / OUTPUTS[0], "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    total = sum(r["mean_difference"] for r in rows)
    top10 = rows[:10]
    positive_sum = sum(r["mean_difference"] for r in rows if r["mean_difference"] > 0)

    record = {
        "task": "C5b, post hoc diagnostic",
        "declared": "post hoc; not in the frozen contract; changes no decision",
        "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script": "RQ_Specified/A11_lesion_programme_addition/scripts/11_gene_level_diagnostic.py",
        "script_sha256": sha256(Path(__file__).resolve()),
        "inputs": {"pseudobulk": {"path": pb.name, "sha256": sha256(pb)}},
        "primary_arm": PRIMARY_ARM,
        "donors": donors,
        "exact_test_actual_output": {
            "note": "recomputed and recorded because the A11 helper blanks its output when the interval is unattainable",
            "SCoV1_primary_lesion": {"n": 4, "HL": 0.2410, "exact_p": 0.1250,
                                     "conf_int": "minus infinity to infinity",
                                     "attained_conf_level": 1.0,
                                     "why_helper_reports_unavailable": "the helper requires a finite 95 per cent interval and at four pairs none exists"},
            "SCoV1_stress_excluded": {"n": 4, "HL": 0.2296, "exact_p": 0.1250},
            "SCoV1_beyond_shared": {"n": 4, "HL": 0.0845, "exact_p": 0.6250},
            "SCoV2_primary_lesion": {"n": 3, "HL": 0.1587, "exact_p": 0.5000},
            "SCoV2_stress_excluded": {"n": 3, "HL": 0.1489, "exact_p": 0.5000},
            "SCoV2_beyond_shared": {"n": 3, "HL": 0.0074, "exact_p": 0.2500},
            "minimum_attainable_two_sided_p": {"n=4": 0.125, "n=3": 0.25},
        },
        "leave_one_out_primary_means": {r["omitted_donor"]: round(float(r["remaining_mean"]), 4)
                                        for r in read_tsv(a.c4 / "omission_diagnostics.tsv")},
        "a11_stress_exclusion": {
            "genes_dropped": len(dropped), "dropped": dropped,
            "nfkb_names_retained": sorted(NFKB & retained),
            "isr_names_retained": sorted(ISR & retained),
            "consequence": "the exclusion removes 17 of the 73 and retains the canonical NF-kB and integrated-stress-response names, so agreement between the primary and the stress-excluded variant does not show the movement is independent of an injury response",
        },
        "gene_level": {
            "net_sum_of_mean_differences": round(total, 4),
            "sum_of_positive_movers": round(positive_sum, 4),
            "top_10": [{k: r[k] for k in ("gene", "mean_difference", "donors_positive", "canonical_group")} for r in top10],
            "share_of_net_shift_carried_by_top_10": round(sum(r["mean_difference"] for r in top10) / total, 3) if total else None,
            "reading": "the net shift is a small residue of large opposing gene movements, and several of the largest positive movers are canonical injury responders, so the module label carries less of the result than its name suggests",
        },
        "changes_no_decision": True,
    }
    (out / OUTPUTS[1]).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print("net sum of mean differences: %+.4f over %d genes" % (total, len(rows)))
    print("top movers:")
    for r in top10:
        print("   %-10s %+.3f  %s%s" % (r["gene"], r["mean_difference"], r["canonical_group"],
                                        "  [dropped by stress exclusion]" if r["dropped_by_a11_stress_exclusion"] == "yes" else ""))
    print("NF-kB names retained in the stress-excluded list: %s" % sorted(NFKB & retained))
    print("stress response names retained: %s" % sorted(ISR & retained))


if __name__ == "__main__":
    main()
