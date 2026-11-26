"""Replay withdrawal and challenge on a verified versioned transcript reference."""
import argparse
import csv
import gzip
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean

from replay import CHALLENGE, RAW, WITHDRAWAL, gene_index, plt, table


def reference():
    records = {}
    with gzip.open(RAW / "ensembl84.cdna.fa.gz", "rt") as handle:
        for line in handle:
            if line.startswith(">"):
                transcript = line.split()[0][1:]
                gene = re.search(r" gene:([^ .]+)", line)[1]
                if transcript in records:
                    raise ValueError(f"Duplicated reference transcript: {transcript}")
                records[transcript] = [gene, 0]
            else:
                records[transcript][1] += len(line.strip())
    if len(records) != 96626:
        raise ValueError("Incorrect release-84 cDNA target count")
    return records


def load(path, index, genes, require_order):
    signal = defaultdict(list)
    observed = set()
    value_total = 0.0
    count_total = 0.0
    with gzip.open(path, "rt") as handle:
        rdr = csv.DictReader(handle, delimiter="\t")
        for row in rdr:
            tx = row["target_id"]
            if tx not in index or tx in observed:
                raise ValueError(f"Unexpected duplicate or unmapped target {tx}")
            gene, length = index[tx]
            if int(row["length"]) != length:
                raise ValueError(f"Length mismatch for {tx}")
            observed.add(tx)
            v = float(row["tpm"])
            if not math.isfinite(v) or v < 0:
                raise ValueError(f"Invalid TPM for {tx}")
            value_total += v
            count_total += float(row["est_counts"])
            if gene in genes:
                signal[gene].append(v)
    if len(observed) != len(index) or abs(value_total - 1e6) > 50:
        raise ValueError("Incomplete reference or invalid normalization")
    if require_order:
        with gzip.open(path, "rt") as handle:
            next(handle)
            if not all(t == line.split("\t", 1)[0] for t, line in zip(index, handle, strict=True)):
                raise ValueError("Deposited target order differs from the release-84 source")
    return signal, value_total, count_total


def withdrawal(out, stage, values):
    fig, (signals, effects) = plt.subplots(2, 1, figsize=(8, 5), sharex=True, layout="constrained")
    summary = []
    for i, symbol in enumerate(WITHDRAWAL):
        baseline, first, second = [row[symbol] for row in values]
        a, b, c = [math.log2(v + 1) for v in (baseline, first, second)]
        delta = mean((b, c)) - a
        summary.append((stage, symbol, baseline, first, second, delta))
        signals.scatter(i - 0.13, a, marker="s", color="#19728a", label="Ex vivo" if i == 0 else None)
        signals.scatter([i, i + 0.13], [b, c], facecolors="none", edgecolors="#9d471e", label="60 h libraries" if i == 0 else None)
        effects.scatter(i, delta, color="#263041")
    signals.set_title(f"Roberts niche withdrawal · Experiment {stage}")
    signals.set_ylabel("log₂(TPM + 1)")
    signals.legend(frameon=False)
    effects.axhline(0, color="0.6", linewidth=1)
    effects.set_ylabel("60 h − ex vivo\n(log₂ scale)")
    effects.set_xticks(range(len(WITHDRAWAL)), WITHDRAWAL)
    fig.savefig(out / "withdrawal.png", dpi=180)
    table(out / "withdrawal.tsv", ("experiment", "symbol", "ex_vivo_tpm", "culture_1_tpm", "culture_2_tpm", "log2_difference"), summary)


def challenge(out, values):
    results = []
    for symbol in CHALLENGE:
        baseline, stimulated, deprogrammed, cargo = [mean(row[symbol] for row in values[i:i+2]) for i in range(0, 8, 2)]
        exclude = cargo > 2 * baseline
        fold = stimulated / baseline if baseline > 0 and not exclude else "NA"
        results.append((symbol, baseline, stimulated, deprogrammed, cargo, exclude, cargo > 2 * stimulated, fold, min(baseline, stimulated) < 1))
    table(out / "challenge.tsv", ("symbol", "programmed_minus_tpm", "programmed_plus_tpm", "deprogrammed_plus_tpm", "cargo_tpm", "exclude_cargo_gt_2x_minus", "cargo_gt_2x_plus", "programmed_fold", "low_tpm"), results)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("1", "2", "challenge"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--requantification", nargs=3, type=Path)
    args = parser.parse_args()
    ids = {"1": range(2968, 2971), "2": range(2971, 2974), "challenge": range(2974, 2982)}
    index = reference()
    _, named = gene_index()
    panels = WITHDRAWAL if args.stage != "challenge" else CHALLENGE
    genes = {name: named[name] for name in panels}
    accession_paths = []
    for offset, suffix in enumerate(ids[args.stage]):
        gsm = f"GSM246{suffix}"
        if args.stage == "1":
            release = args.requantification[offset]
        else:
            release, = RAW.glob(f"{gsm}_*.txt.gz")
        accession_paths.append((gsm, release))
    values, qc, sources = [], [], []
    for gsm, path in accession_paths:
        tpm, total_tpm, total_counts = load(path, index, set(genes.values()), args.stage != "1")
        qc.append((gsm, len(index), total_tpm, total_counts))
        observed = {}
        for symbol, gene in genes.items():
            parts = tpm[gene]
            if not parts:
                raise ValueError(f"Panel gene missing from reference: {gene}")
            observed[symbol] = math.fsum(parts)
            sources.append((gsm, symbol, gene, len(parts), observed[symbol], observed[symbol] < 1))
        values.append(observed)
    table(args.output / "mapping_qc.tsv", ("gsm", "exact_targets", "total_tpm", "est_counts"), qc)
    table(args.output / "gene_tpm.tsv", ("gsm", "symbol", "gene_id", "indexed_transcripts", "tpm", "below_1_tpm"), sources)
    if args.stage == "challenge":
        challenge(args.output, values)
    else:
        withdrawal(args.output, args.stage, values)


if __name__ == "__main__":
    main()
