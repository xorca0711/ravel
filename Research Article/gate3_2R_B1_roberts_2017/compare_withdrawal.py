"""Render the two release-84 contrasts from their checked source-value tables."""
import argparse
import csv
from pathlib import Path

from replay import WITHDRAWAL, plot, table


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source_values, effects, rows = [], [], []
    for number, path in enumerate((args.first, args.second), start=1):
        with path.open() as handle:
            result = list(csv.DictReader(handle, delimiter="\t"))
        if [x["symbol"] for x in result] != list(WITHDRAWAL) or any(x["experiment"] != str(number) for x in result):
            raise ValueError(f"Unexpected withdrawal results: {path}")
        for field in ("ex_vivo_tpm", "culture_1_tpm", "culture_2_tpm"):
            source_values.append({row["symbol"]: float(row[field]) for row in result})
        effects.append({row["symbol"]: float(row["log2_difference"]) for row in result})
        rows.extend((row["experiment"], row["symbol"], row["ex_vivo_tpm"], row["culture_1_tpm"], row["culture_2_tpm"], row["log2_difference"]) for row in result)
    plot(args.output, source_values, effects)
    table(args.output / "withdrawal_comparison.tsv", ("experiment", "symbol", "ex_vivo_tpm", "culture_1_tpm", "culture_2_tpm", "log2_difference"), rows)


if __name__ == "__main__":
    main()
