"""Descriptive aged-HSC count readback with all-positive median-ratio normalization."""
import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, median

from openpyxl import load_workbook

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
sheet = load_workbook("raw_data/mu2026/GSE307126_RNAseq_HSCs.xlsx",
                      read_only=True, data_only=True)["Count matrix_deseq2"]
records = sheet.values
header = next(records)
assert header == ("GeneID", "Mx1Cre_1", "Mx1Cre_2", "Mx1T3_2", "Mx1T3_3")
target = ("Cox7a2", "Ndufa6", "ND1", "ND4")
values_by_gene = {}
ratios = [[], [], [], []]
for gene, *counts in records:
    if gene is None:
        continue
    assert all(type(count) is int and count >= 0 for count in counts), gene
    if gene in target:
        assert gene not in values_by_gene
        values_by_gene[gene] = counts
    if min(counts) > 0:
        geomean = math.exp(mean(math.log(count) for count in counts))
        for sample_ratios, count in zip(ratios, counts):
            sample_ratios.append(count / geomean)
factors = [median(sample_ratios) for sample_ratios in ratios]
assert len(values_by_gene) == len(target)
with (args.output / "hsc_counts.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(["released_gene_label", *header[1:],
                     *(f"{sample}_normalized" for sample in header[1:]), "normalized_T3_minus_Cre"])
    for gene in target:
        counts = values_by_gene[gene]
        normalized = [count / factor for count, factor in zip(counts, factors)]
        writer.writerow([gene, *counts, *normalized, mean(normalized[2:]) - mean(normalized[:2])])
(args.output / "normalization.json").write_text(json.dumps({
    "all_positive_rows": len(ratios[0]),
    "size_factors": dict(zip(header[1:], factors)),
}, indent=2) + "\n")
