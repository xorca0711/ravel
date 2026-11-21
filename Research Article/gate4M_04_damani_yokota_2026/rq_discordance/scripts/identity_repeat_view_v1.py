"""A3/DY1 fixed six-target view of frozen WT source-average contrasts."""
import argparse
import csv
import gzip
import json
import math
from pathlib import Path

TARGETS = ("Stat6", "Egr2", "Pparg", "Rxra", "Irf4", "Arg1")
COLUMNS = ("WT_ctrl_0h", "WT_ctrl_3h_IL4", "WT_IL4_pre_0h", "WT_IL4_pre_3h_IL4")
OFFSETS = (1.0, 0.5)
RAW = Path("raw_data/DY1_P02_temporal_source_v1/GSE115504_memory_averaged.cpm.table.tsv.gz")
FROZEN = Path("analysis/research/runs/DY1_P02_source_average_response_v1/source_average_contrasts.tsv.gz")


def read_unique(path, id_column):
    with gzip.open(path, "rt", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        selected, seen = {}, set()
        for row in reader:
            key = (row[id_column], float(row["offset"])) if "offset" in row else row[id_column]
            if key in seen:
                raise ValueError(f"Duplicate source key: {key}")
            seen.add(key)
            if row[id_column] in TARGETS:
                selected[key] = row
    return selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    out = Path(parser.parse_args().output)
    out.mkdir(parents=True, exist_ok=True)
    raw, frozen = read_unique(RAW, "ORF"), read_unique(FROZEN, "source_row_id")
    if set(raw) != set(TARGETS) or len(frozen) != 12:
        raise ValueError("Missing target/offset rows")
    rows, checks, errors = [], 0, []
    for gene in TARGETS:
        values = [float(raw[gene][column]) for column in COLUMNS]
        if not all(math.isfinite(v) and v >= 0 for v in values):
            raise ValueError("Invalid source average")
        for offset in OFFSETS:
            first = math.log2((values[1]+offset)/(values[0]+offset))
            second = math.log2((values[3]+offset)/(values[2]+offset))
            expected = dict(first_stage_log_ratio=first, second_stage_log_ratio=second,
                            second_minus_first=second-first,
                            baseline_log_ratio=math.log2((values[2]+offset)/(values[0]+offset)))
            saved = frozen[(gene, offset)]
            row = dict(gene=gene, role="separate_effector" if gene=="Arg1" else "identity_context",
                       offset=offset, **dict(zip(COLUMNS, values)))
            for endpoint, value in expected.items():
                old = float(saved[endpoint]); error = abs(old-value)
                checks += 1; errors.append(error)
                if error > 1e-10:
                    raise ValueError(f"Frozen parity failure: {gene}/{offset}/{endpoint}")
                row[endpoint] = old
                row[endpoint+"_parity_error"] = error
            if (saved["any_nonzero_source_average"].lower()=="true") != any(v>0 for v in values):
                raise ValueError("Nonzero flag conflict")
            row["any_nonzero_source_average"] = any(v>0 for v in values)
            rows.append(row)
    with (out/"target_source_average_view.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader(); writer.writerows(rows)
    verification = dict(ok=True, targets=6, rows=len(rows), scalar_parity_checks=checks,
                        max_absolute_error=max(errors), offsets=list(OFFSETS),
                        method="Read frozen target rows; independently compare scalar log2 ratios of four original WT source averages.",
                        limit="Numerical verification of the same source, not biological replication; no individual variance/n or causal interaction.")
    (out/"verification.json").write_text(json.dumps(verification, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(ok=True, rows=len(rows), checks=checks, max_error=max(errors))))


if __name__ == "__main__":
    main()
