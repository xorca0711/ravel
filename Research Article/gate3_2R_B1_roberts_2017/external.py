"""Read the released paired cargo-status matrix without cross-tissue pooling."""
import argparse
import gzip
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

import xlrd

from replay import RAW, WITHDRAWAL, gene_index, table


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = RAW / "external"
    records = {}
    with gzip.open(root / "external.soft.gz", "rt") as handle:
        for line in handle:
            key, _, value = line.strip().partition(" = ")
            if key == "^SAMPLE":
                record = {"gsm": value}
            elif key == "!Sample_title":
                records[value] = record
            elif key == "!Sample_characteristics_ch1":
                field, value = value.split(": ", 1)
                record[field] = value
    with gzip.open(root / "external.matrix.xls.gz", "rb") as handle:
        workbook = xlrd.open_workbook(file_contents=handle.read())
    sheet = workbook.sheet_by_index(0)
    headings = sheet.row_values(0)
    if len(records) != 18 or headings[0] != "ID" or set(headings[1:]) != set(records):
        raise ValueError("Unexpected sample mapping")
    _, genes = gene_index()
    panel = {symbol: genes[symbol] for symbol in WITHDRAWAL if symbol != "Tlr9"}
    targets = defaultdict(list)
    for idx in range(1, sheet.nrows):
        row = sheet.row_values(idx)
        if row[0] in panel.values():
            targets[row[0]].append(row[1:])
    pairs = defaultdict(dict)
    for column, name in enumerate(headings[1:]):
        sample = records[name]
        key = (sample["tissue"], sample["sample pair"], sample["library batch"])
        phenotype = sample["phenotype"]
        if phenotype in pairs[key]:
            raise ValueError(f"Duplicated phenotype in {key}")
        pairs[key][phenotype] = (column, name)
    if len(pairs) != 9:
        raise ValueError("Unexpected pairing")
    source = []
    grouped = defaultdict(list)
    for (tissue, pair, batch), roles in sorted(pairs.items()):
        positive, positive_name = roles["Engulfing"]
        negative, negative_name = roles["Non engulfing"]
        for symbol, gene in panel.items():
            matched = targets[gene]
            if len(matched) != 1:
                source.append((tissue, pair, batch, symbol, gene, positive_name, negative_name, "NA", "NA", "NA", "missing" if not matched else "ambiguous"))
                grouped[tissue, symbol].append(None)
                continue
            pos, neg = float(matched[0][positive]), float(matched[0][negative])
            if any(not math.isfinite(x) or x < 0 for x in (pos, neg)):
                raise ValueError("Invalid normalized CPM")
            change = math.log2((1 + pos) / (1 + neg))
            source.append((tissue, pair, batch, symbol, gene, positive_name, negative_name, pos, neg, change, "observed"))
            grouped[tissue, symbol].append(change)
    table(args.output / "pairs.tsv", ("tissue", "pair", "library_batch", "symbol", "gene_id", "positive_library", "negative_library", "positive_cpm", "negative_cpm", "log2_difference", "status"), source)
    summary = []
    for (tissue, symbol), effects in grouped.items():
        observed = [value for value in effects if value is not None]
        summary.append((tissue, symbol, len(observed), mean(observed) if observed else "NA", sum(x > 0 for x in observed), sum(x < 0 for x in observed), sum(x == 0 for x in observed)))
    table(args.output / "tissue_summary.tsv", ("tissue", "symbol", "pairs", "mean_paired_log2_difference", "positive", "negative", "zero"), summary)
    table(args.output / "sample_map.tsv", ("library", "gsm", "tissue", "pair", "library_batch", "phenotype"), [(name, sample["gsm"], sample["tissue"], sample["sample pair"], sample["library batch"], sample["phenotype"]) for name, sample in records.items()])


if __name__ == "__main__":
    main()
