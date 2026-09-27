"""C5d, post hoc: the viral-detection table, with the field defined and the eligible donors separated.

An adversarial review found three errors in the C5 narrative: the viral-feature inventory was
miscounted and omitted the arm under test, the MERS figure was pooled over donors that are not
eligible, and the influenza figure likewise. It also asked that the virus field be described as what
it is, a detection of at least one viral read, rather than as infection status.

This emits the table those statements should have been generated from. It changes no decision.

Standard library only. Refuses to overwrite.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import json
import re
import statistics as st
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OUTPUTS = ["virus_detection.tsv", "virus_detection.json"]
VIRAL_PREFIX = re.compile(r"^(SCoV1|SCoV2|MERS|H3N2)-")
# Donors whose pair clears the inherited 50-cell floor, from the C3 eligibility table.
ELIGIBLE = {"SCoV1": ["pat1", "pat3", "pat4", "pat6"], "SCoV2": ["pat1", "pat4", "pat6"],
            "MERS": ["pat1", "pat4"], "H3N2": ["pat5"]}


def sha256(path: Path) -> str:
    d = hashlib.sha256()
    with path.open("rb") as h:
        for b in iter(lambda: h.read(1 << 24), b""):
            d.update(b)
    return d.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", type=Path, required=True)
    ap.add_argument("--gene-index", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    existing = [n for n in OUTPUTS if (out / n).exists()]
    if existing:
        raise SystemExit("Refusing to overwrite: %s" % existing)

    index = [r["gene_id"] for r in csv.DictReader(open(a.gene_index, encoding="utf-8"), delimiter="\t")]
    inventory: dict[str, list[str]] = {}
    for g in index:
        m = VIRAL_PREFIX.match(g)
        if m:
            inventory.setdefault(m.group(1), []).append(g)
    total_viral = sum(len(v) for v in inventory.values())

    with gzip.open(a.metadata, "rt", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    at2 = [r for r in rows if r["origin"] == "explant" and r["cluster"] == "AT2"]

    pct_field = {"SCoV1": "pct.SCoV1", "SCoV2": "pct.SCoV2", "MERS": "pct.MERS", "H3N2": "pct.H3N2"}
    table = []
    for arm in ["control", "SCoV1", "SCoV2", "MERS", "H3N2"]:
        for scope in ["all donors", "eligible donors only"]:
            sub = [r for r in at2 if r["infect"] == arm]
            if scope == "eligible donors only":
                if arm == "control":
                    continue
                sub = [r for r in sub if r["donor"] in ELIGIBLE[arm]]
            if not sub:
                continue
            det = sum(1 for r in sub if r["virus"] != "none")
            pcts = []
            if arm in pct_field:
                for r in sub:
                    try:
                        pcts.append(float(r[pct_field[arm]]))
                    except (ValueError, KeyError):
                        pass
            table.append({
                "arm": arm, "scope": scope, "cells": len(sub),
                "cells_with_any_viral_read": det,
                "fraction_with_any_viral_read": round(det / len(sub), 4),
                "median_viral_percent": round(st.median(pcts), 5) if pcts else "none",
                "max_viral_percent": round(max(pcts), 4) if pcts else "none",
                "cells_above_1pc_viral": sum(1 for v in pcts if v > 1) if pcts else "none",
                "donors": ",".join(sorted({r["donor"] for r in sub})),
            })
    with open(out / OUTPUTS[0], "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(table[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in table:
            w.writerow(r)

    def pick(arm: str, scope: str) -> dict:
        return next(r for r in table if r["arm"] == arm and r["scope"] == scope)

    record = {
        "task": "C5d, post hoc",
        "declared": "post hoc; corrects three narrative figures and changes no decision",
        "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script": "docs/research_pipeline/scripts/c5d_virus_table.py",
        "script_sha256": sha256(Path(__file__).resolve()),
        "inputs": {"cell_metadata": sha256(a.metadata), "gene_index": sha256(a.gene_index)},
        "virus_field_definition": "the object's virus field is a detection call, non-none when the cell carries at least one read assigned to that virus; it is not an infection assay and a droplet assay can miss low-load infected cells",
        "viral_feature_inventory": {"total": total_viral,
                                    "by_virus": {k: len(v) for k, v in sorted(inventory.items())},
                                    "features": {k: sorted(v) for k, v in sorted(inventory.items())}},
        "corrections": {
            "viral_inventory": "an earlier narrative said 34 SARS-CoV-2, 10 influenza and 9 MERS entries and omitted SARS-CoV-1, the arm under test; the counted inventory is above",
            "mers_figure": "an earlier narrative gave 309 virus-positive type 2 cells for MERS pooled over all donors; restricted to its two eligible donors the figure is %d of %d"
                           % (pick("MERS", "eligible donors only")["cells_with_any_viral_read"],
                              pick("MERS", "eligible donors only")["cells"]),
            "h3n2_figure": "an earlier narrative gave 15.6 per cent for influenza pooled over all donors; restricted to its one eligible donor the figure is %d of %d"
                           % (pick("H3N2", "eligible donors only")["cells_with_any_viral_read"],
                              pick("H3N2", "eligible donors only")["cells"]),
        },
        "primary_arm_eligible_donors": pick("SCoV1", "eligible donors only"),
        "changes_no_decision": True,
    }
    (out / OUTPUTS[1]).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print("viral features in the index: %d  %s" % (total_viral, record["viral_feature_inventory"]["by_virus"]))
    print()
    for r in table:
        print("  %-8s %-22s %5d cells, any viral read %4d (%.1f%%), median viral pct %s, cells above 1%% %s"
              % (r["arm"], r["scope"], r["cells"], r["cells_with_any_viral_read"],
                 100 * r["fraction_with_any_viral_read"], r["median_viral_percent"], r["cells_above_1pc_viral"]))


if __name__ == "__main__":
    main()
