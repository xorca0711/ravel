"""Resolve S0 line aliases using observed barcode evidence and independently check memberships."""
import csv
import gzip
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

CACHE = Path("raw_data/nagaraja_s0")
FIRST = Path("analysis/research/runs/ng26_s0_v2")


def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def write(path, fields, records):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(records)


def reconcile(out):
    specimens = {r["specimen"]:r for r in rows(FIRST/"specimen_key.tsv")}
    clean = set()
    for row in rows(CACHE/"code/ref/mouse_organoids.cleaned_clone_calls.txt"):
        clean.update((row["atac_cell"], clone) for clone in row["clone"].split(","))
    scored, fos, nonfinite, feature_names = set(), set(), Counter(), set()
    for row in rows(CACHE/"moesm4.txt"):
        key = (row["atac_cell"],row["clone"],row["sample"])
        scored.add(key)
        feature_names.add(row["feature"])
        value = float("nan") if row["score"] == "NA" else float(row["score"])
        if not math.isfinite(value):
            nonfinite[row["feature"]] += 1
        elif row["feature"] == "Fos":
            if key in fos:
                raise ValueError("Duplicate Fos row")
            fos.add(key)

    resolved, keys, line_sets = [], set(), defaultdict(set)
    clean_counts, score_counts = Counter(), Counter()
    lines_by_clone, history_sizes = defaultdict(Counter), Counter()
    per_line_scored = defaultdict(set)
    for row in rows(FIRST/"organoid_memberships.tsv"):
        cell, clone, line = row["atac_cell"],row["clone"],row["replicate"]
        key = (cell,clone)
        assert key in clean and key not in keys
        keys.add(key)
        accession = row["barcode_map_specimen"]
        spec = specimens[accession]
        donor = spec["donor"]
        assert donor and "|" not in donor
        raw_history = spec["observed_map_labels"]
        history = {"DSS":"Colitis","Control":"Control"}[raw_history]
        line_sets[line].add((history,accession,spec["source_alias"],donor))
        has_score = (cell,clone,history) in scored
        assert has_score == (row["join_state"] == "both")
        assert not has_score or row["sample"] == history
        clean_counts[cell] += 1
        if has_score:
            score_counts[cell] += 1
            history_sizes[history,clone] += 1
            per_line_scored[line].add(cell)
        lines_by_clone[clone][line,"clean"] += 1
        lines_by_clone[clone][line,"scored"] += int(has_score)
        resolved.append((cell,row["barcode_cell"],clone,line,history,accession,donor,has_score))
    assert keys == clean and scored == fos
    assert sum(score_counts.values()) == len(scored)
    assert all(len(x)==1 for x in line_sets.values())
    assert len({next(iter(x))[3] for x in line_sets.values()}) == len(line_sets)
    write(out/"cell_clone_line_mouse.tsv",
          ["atac_cell","clone_assay_cell","clone_id","organoid_line","history","specimen","mouse_donor",
           "in_score_table","clean_memberships_of_cell","scored_memberships_of_cell"],
          [(*r,clean_counts[r[0]],score_counts[r[0]]) for r in resolved])
    write(out/"line_donor_key.tsv",
          ["organoid_line","history","specimen","deposited_specimen_alias","mouse_donor","scored_cells"],
          [(line,*next(iter(x)),len(per_line_scored[line])) for line,x in sorted(line_sets.items())])
    overlaps = []
    for clone, counts in sorted(lines_by_clone.items()):
        lines = sorted({line for line, _ in counts})
        if len(lines)>1:
            for line in lines:
                overlaps.append((clone,line,next(iter(line_sets[line]))[0],counts[line,"clean"],counts[line,"scored"]))
    write(out/"clone_ids_in_multiple_lines.tsv",["clone_id","line","history","clean_cells","scored_cells"],overlaps)
    write(out/"nonfinite_features.tsv",["feature","nonfinite_score_rows"],sorted(nonfinite.items()))
    denominators = []
    for history in sorted({h for h,_ in history_sizes}):
        sizes = [n for (h,_),n in history_sizes.items() if h==history]
        denominators.append((history,len(sizes),sum(n>=5 for n in sizes),min(sizes),max(sizes)))
    write(out/"fig2i_denominators.tsv",["history","distinct_deposited_clone_ids_with_finite_Fos",
          "history_clone_pairs_with_at_least_5_cells","min_cells_in_history_clone","max_cells_in_history_clone"],denominators)
    tissue = Counter()
    with gzip.open(FIRST/"barcode_lookup.tsv.gz","rt",newline="") as handle:
        for row in csv.DictReader(handle,delimiter="\t"):
            if "tissue" not in row["dataset"]:
                continue
            ids = row["specimen_matches"].split("|") if row["specimen_matches"] else []
            labels = "|".join(sorted({specimens[x]["observed_map_labels"] for x in ids}))
            tissue[row["dataset"],row["input"],row["identifier_status"],len(ids),labels] += 1
    write(out/"tissue_lookup_by_stage.tsv",["dataset","input","indexed_barcode_status","n_specimen_matches",
          "map_labels_if_observed","barcode_records"],[(*k,n) for k,n in sorted(tissue.items())])
    return len(clean),len(scored),len(feature_names)


if __name__ == "__main__":
    print("Validated clean pairs, scored memberships and features",reconcile(Path(sys.argv[1])))
