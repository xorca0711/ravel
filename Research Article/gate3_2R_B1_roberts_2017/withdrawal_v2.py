"""Compare one explicitly qualified baseline and its two culture libraries."""
import argparse
import math
from pathlib import Path
from statistics import mean

from replay import RAW, WITHDRAWAL, gene_index, plt, read_sample, table


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--experiment", type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    index, genes = gene_index()
    panel = {symbol: genes[symbol] for symbol in WITHDRAWAL}
    start = 2968 if args.experiment == 1 else 2971
    accessions = [f"GSM246{i}" for i in range(start, start + 3)]
    values, qc, sources, results = [], [], [], []
    for accession in accessions:
        if args.experiment == 1:
            path = RAW / "requant" / accession / "abundance.tsv.gz"
        else:
            path, = RAW.glob(f"{accession}_*.txt.gz")
        by_gene, targets, mapped, total = read_sample(path, index, panel)
        qc.append((accession, targets, mapped, targets - mapped, total))
        row = []
        for symbol, gene in panel.items():
            parts = by_gene[gene]
            if not parts:
                raise ValueError(f"Missing {symbol} for {accession}")
            gene_tpm = math.fsum(parts)
            row.append(gene_tpm)
            sources.append((accession, symbol, gene, len(parts), gene_tpm, gene_tpm < 1))
        values.append(row)

    fig, (signal, effect) = plt.subplots(2, 1, figsize=(8, 5), sharex=True, layout="constrained")
    for i, (symbol, (baseline, first, second)) in enumerate(zip(panel, zip(*values))):
        log_baseline, log_first, log_second = [math.log2(1 + x) for x in (baseline, first, second)]
        delta = mean((log_first, log_second)) - log_baseline
        results.append((args.experiment, symbol, baseline, first, second, delta))
        signal.scatter(i - 0.16, log_baseline, color="#19728a", marker="s", label="Ex vivo" if i == 0 else None)
        signal.scatter([i, i + 0.16], [log_first, log_second], facecolors="none", edgecolors="#9d471e", label="60 h libraries" if i == 0 else None)
        effect.scatter(i, delta, color="#263041")
    signal.set_title(f"Roberts niche withdrawal · Experiment {args.experiment}")
    signal.set_ylabel("log₂(TPM + 1)")
    signal.legend(frameon=False)
    effect.axhline(0, color="0.6", linewidth=1)
    effect.set_ylabel("60 h − ex vivo\n(log₂ scale)")
    effect.set_xticks(range(len(WITHDRAWAL)), WITHDRAWAL)
    fig.savefig(args.output / "withdrawal.png", dpi=180)
    table(args.output / "mapping_qc.tsv", ("gsm", "targets", "mapped", "unmapped", "total_tpm"), qc)
    table(args.output / "gene_tpm.tsv", ("gsm", "symbol", "gene_id", "indexed_transcripts", "tpm", "below_1_tpm"), sources)
    table(args.output / "withdrawal.tsv", ("experiment", "symbol", "ex_vivo_tpm", "culture_1_tpm", "culture_2_tpm", "log2_difference"), results)


if __name__ == "__main__":
    main()
