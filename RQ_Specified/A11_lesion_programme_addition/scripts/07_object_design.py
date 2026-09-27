"""C1, object half: the explant design as the count object records it, with AT2 depth.

Reads only the cell metadata the inspection step cached, not the count matrices, so it runs in
a few seconds and needs no memory headroom. It writes the donor by arm by medium design with
author-annotated AT2 counts, and the medium-matched pair inventory that C2 would have to
choose a contrast from.

It chooses nothing. Arm selection is C2's, and this table exists so that selection can be
justified on coverage and protocol matching before any programme value is computed. No
expression is read here and no score is produced.

Standard library only. Refuses to overwrite.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OUTPUTS = ["object_explant_design.tsv", "object_crosswalk_run.json"]
ARMS = ["control", "H3N2", "SCoV1", "SCoV2", "MERS"]
INFECTED = ["H3N2", "SCoV1", "SCoV2", "MERS"]
MEDIA = ["BSA", "FCS"]
AT2_LABEL = "AT2"          # the author cluster label
FLOORS = [20, 50]


def sha256(path: Path) -> str:
    d = hashlib.sha256()
    with path.open("rb") as h:
        for b in iter(lambda: h.read(1 << 24), b""):
            d.update(b)
    return d.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    existing = [n for n in OUTPUTS if (out / n).exists()]
    if existing:
        raise SystemExit("Refusing to overwrite: %s" % existing)

    with gzip.open(args.metadata, "rt", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    explant = [r for r in rows if r["origin"] == "explant"]
    donors = sorted({r["donor"] for r in explant})

    cells: dict[tuple, int] = {}
    at2: dict[tuple, int] = {}
    for r in explant:
        key = (r["donor"], r["infect"], r["protocol"])
        cells[key] = cells.get(key, 0) + 1
        if r["cluster"] == AT2_LABEL:
            at2[key] = at2.get(key, 0) + 1

    table = []
    for d in donors:
        for a in ARMS:
            for p in MEDIA:
                n = cells.get((d, a, p), 0)
                if not n:
                    continue
                table.append({"donor": d, "arm": a, "medium": p, "cells": n,
                              "at2_cells": at2.get((d, a, p), 0)})
    with open(out / OUTPUTS[0], "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(table[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in table:
            w.writerow(r)

    pairs = {}
    for a in INFECTED:
        found = []
        for d in donors:
            for p in MEDIA:
                if cells.get((d, a, p)) and cells.get((d, "control", p)):
                    smaller = min(at2.get((d, a, p), 0), at2.get((d, "control", p), 0))
                    found.append({"donor": d, "medium": p,
                                  "at2_infected": at2.get((d, a, p), 0),
                                  "at2_control": at2.get((d, "control", p), 0),
                                  "at2_smaller_side": smaller})
        pairs[a] = {
            "medium_matched_pairs": len(found),
            "pairs": found,
            "pairs_at_floor": {str(f): sum(1 for x in found if x["at2_smaller_side"] >= f) for f in FLOORS},
        }

    record = {
        "task": "C1, object half",
        "scope": "cached cell metadata only; no count matrix and no expression is read, and no score is produced",
        "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script": "RQ_Specified/A11_lesion_programme_addition/scripts/07_object_design.py",
        "script_sha256": sha256(Path(__file__).resolve()),
        "input": {"path": str(args.metadata).replace("\\", "/"), "sha256": sha256(args.metadata)},
        "explant_cells": len(explant),
        "explant_donors": donors,
        "autopsy_cells": len(rows) - len(explant),
        "medium_is_recorded_per_cell": "yes, in the protocol field, for infected and control libraries alike",
        "at2_label_used": "the author cluster label %r" % AT2_LABEL,
        "at2_explant_cells": sum(at2.values()),
        "pair_inventory": pairs,
        "donor_label_mismatch": {
            "object_labels": donors,
            "series_single_cell_explant_donors": ["102C", "1169Z", "218V", "219V", "700D", "89C"],
            "status": "six against six, but the mapping is not stated anywhere in either source",
            "partially_constrained_by_arms": "the donor carrying only a control and an influenza arm, and the two donors carrying both control media, are each identifiable as a group, which narrows the mapping without resolving any individual pair",
        },
        "selection_not_made_here": "C2 chooses the arm. This table exists so the choice rests on matched-control availability and AT2 depth, both counted before any programme value.",
        "scores_computed": False,
    }
    (out / OUTPUTS[1]).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print("explant cells %d across donors %s; author AT2 %d"
          % (len(explant), donors, sum(at2.values())))
    print()
    for a in INFECTED:
        p = pairs[a]
        print("  %-6s matched pairs %d, at AT2 floor 20 -> %s, at 50 -> %s"
              % (a, p["medium_matched_pairs"], p["pairs_at_floor"]["20"], p["pairs_at_floor"]["50"]))


if __name__ == "__main__":
    main()
