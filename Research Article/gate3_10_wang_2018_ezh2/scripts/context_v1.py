"""Compare five exposed candidate directions across frozen Treg contrasts."""

import argparse
import csv
from pathlib import Path

RUNS = Path("analysis/research/runs")
WANG = RUNS / "wang18_s3_breadth_v1/gene_sensitivity.tsv"
DUPAGE = RUNS / "dupage_s2_state_contrast_v1/interaction.tsv"
PEETERS = RUNS / "dupage_candidate_followup_v1/contrasts.tsv"
PANEL = ("Tigit", "Prdm1", "Ccr2", "Igfbp4", "Areg")


def read_tsv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main(output):
    wang, dupage, peeters = map(read_tsv, (WANG, DUPAGE, PEETERS))
    table = []
    for symbol in PANEL:
        w, = [row for row in wang if row["symbol"] == symbol and row["eligible"] == "1"]
        d, = [row for row in dupage if row["gene_short_name"] == symbol]
        fresh, cultured = [
            next(row for row in peeters if (row["gene"], row["contrast"]) == (symbol, key))
            for key in ("gain_N", "gain_D4")
        ]
        table.append(dict(
            gene=symbol, wang_pooled_log2_ratio=w["primary"], wang_strict_wt_log2_ratio=w["strict_wt"],
            wang_omit_min=w["omit_library_min"], wang_omit_max=w["omit_library_max"],
            dupage_high_mean_log_fpkm_difference=d["delta_high"],
            dupage_low_mean_log_fpkm_difference=d["delta_low"],
            peeters_fresh_mean_rlog_difference=fresh["primary"],
            peeters_fresh_omit_min=fresh["sensitivity_min"], peeters_fresh_omit_max=fresh["sensitivity_max"],
            peeters_d4_mean_rlog_difference=cultured["primary"],
            peeters_d4_omit_min=cultured["sensitivity_min"], peeters_d4_omit_max=cultured["sensitivity_max"],
        ))
    with (output / "context_directions.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(table[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args().output)
