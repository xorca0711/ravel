"""Fixed-panel descriptive replay of the deposited Roberts quantifications."""
import argparse
import csv
import gzip
import hashlib
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = Path("raw_data/roberts_2017")
WITHDRAWAL = ("Timd4", "Marco", "Olr1", "Socs3", "Dusp1", "Ptpn6", "Tlr9")
CHALLENGE = ("Tnf", "Il1a", "Il1b", "Cxcl2")


def table(path, columns, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(rows)


def gene_index():
    transcripts = defaultdict(set)
    genes = defaultdict(set)
    with gzip.open(RAW / "ensembl79.gtf.gz", "rt") as annotation:
        for line in annotation:
            if line.startswith("#"):
                continue
            fields = line.split("\t")
            if fields[2] != "transcript":
                continue
            keys = dict(re.findall(r'(\w+) "([^"]+)"', fields[8]))
            gene = keys["gene_id"]
            transcripts[keys["transcript_id"]].add(gene)
            if "gene_name" in keys:
                genes[keys["gene_name"]].add(gene)
    panel = {}
    for symbol in WITHDRAWAL + CHALLENGE:
        gene, = genes[symbol]
        panel[symbol] = gene
    index = {tx: next(iter(owners)) for tx, owners in transcripts.items() if len(owners) == 1}
    return index, panel


def read_sample(path, index, panel):
    by_gene = defaultdict(list)
    target_ids = set()
    mapped = 0
    with gzip.open(path, "rt") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != ["target_id", "length", "eff_length", "est_counts", "tpm"]:
            raise ValueError(f"Unexpected header: {path}")
        normalized_total = 0.0
        for row in reader:
            target = row["target_id"].split(".")[0]
            tpm = float(row["tpm"])
            if target in target_ids or not math.isfinite(tpm) or tpm < 0:
                raise ValueError(f"Invalid target or TPM: {path} {target}")
            target_ids.add(target)
            normalized_total += tpm
            gene = index.get(target)
            if gene is not None:
                mapped += 1
                if gene in panel.values():
                    by_gene[gene].append(tpm)
        if abs(normalized_total - 1e6) > 50:
            raise ValueError(f"Unexpected TPM total: {path} {normalized_total}")
    return by_gene, len(target_ids), mapped, normalized_total


def sample_map(out):
    entries = {}
    with gzip.open(RAW / "family.soft.gz", "rt") as source:
        for line in source:
            if line.startswith("^SAMPLE = "):
                accession = line.strip().split(" = ", 1)[1]
                entries[accession] = {"characteristics": {}}
            elif line.startswith("!Sample_title = "):
                entries[accession]["title"] = line.strip().split(" = ", 1)[1]
            elif line.startswith("!Sample_characteristics_ch1 = "):
                key, value = line.strip().split(" = ", 1)[1].split(": ", 1)
                entries[accession]["characteristics"][key] = value
    if sorted(entries) != [f"GSM246{n}" for n in range(2968, 2982)]:
        raise ValueError("Unexpected accession set")
    paths = {}
    rows = []
    for position, (accession, record) in enumerate(sorted(entries.items())):
        path, = RAW.glob(f"{accession}_*.txt.gz")
        paths[accession] = path
        group = ("withdrawal 1", "withdrawal 2")[position // 3] if position < 6 else "cargo challenge"
        role = ("baseline" if position % 3 == 0 else "60 h library") if position < 6 else "technical duplicate"
        c = record["characteristics"]
        rows.append((accession, record["title"], group, c["time in culture"], c.get("treatment", "none specified"), c["cell type"], "animal/pool unresolved", role, path.name, "transcript TPM", hashlib.sha256(path.read_bytes()).hexdigest()))
    table(out / "sample_map.tsv", ("gsm", "title", "experiment", "culture", "cargo", "sample_type", "preparation", "replicate_role", "file", "scale", "sha256"), rows)
    return paths


def plot(out, values, effects):
    fig, (ax, delta) = plt.subplots(2, 1, figsize=(8, 6), sharex=True, layout="constrained")
    for i, gene in enumerate(WITHDRAWAL):
        for j, color in enumerate(("#19728a", "#9d471e")):
            group = values[j * 3:j * 3 + 3]
            x = i + (j - 0.5) * 0.28
            ax.scatter(x - 0.055, math.log2(group[0][gene] + 1), marker="s", color=color, label=f"Experiment {j + 1} baseline" if i == 0 else None)
            ax.scatter([x + 0.025, x + 0.075], [math.log2(row[gene] + 1) for row in group[1:]], facecolors="none", edgecolors=color, label=f"Experiment {j + 1} 60 h" if i == 0 else None)
            delta.scatter(x, effects[j][gene], color=color)
    ax.set_ylabel("log₂(TPM + 1)")
    ax.legend(frameon=False, ncol=2)
    delta.axhline(0, color="0.6", linewidth=1)
    delta.set_ylabel("60 h − ex vivo\n(log₂ scale)")
    delta.set_xticks(range(len(WITHDRAWAL)), WITHDRAWAL)
    fig.savefig(out / "withdrawal.png", dpi=180)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("map", "withdrawal", "challenge"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paths = sample_map(args.output)
    if args.stage == "map":
        index, panel = gene_index()
        eligibility = []
        for accession, path in paths.items():
            with gzip.open(path, "rt") as handle:
                targets = {line.split("\t", 1)[0].split(".")[0] for line in handle}
            observed = defaultdict(int)
            for target in targets:
                observed[index.get(target)] += 1
            symbols = WITHDRAWAL if accession in list(paths)[:6] else CHALLENGE
            for symbol in symbols:
                gene = panel[symbol]
                eligibility.append((accession, symbol, gene, observed[gene], sum(owner == gene for owner in index.values())))
        table(args.output / "panel_eligibility.tsv", ("gsm", "symbol", "gene_id", "indexed_transcripts", "release79_transcripts"), eligibility)
        return
    symbols = WITHDRAWAL if args.stage == "withdrawal" else CHALLENGE
    samples = list(paths)[:6] if args.stage == "withdrawal" else list(paths)[6:]
    index, all_genes = gene_index()
    panel = {symbol: all_genes[symbol] for symbol in symbols}
    audited = []
    source = []
    values = []
    for accession in samples:
        data, targets, mapped, total = read_sample(paths[accession], index, panel)
        audited.append((accession, targets, mapped, targets - mapped, total))
        observed = {}
        for symbol, gene in panel.items():
            parts = data[gene]
            if not parts:
                raise ValueError(f"Missing panel gene {symbol} in {accession}")
            tpm = math.fsum(parts)
            observed[symbol] = tpm
            n_reference = sum(owner == gene for owner in index.values())
            source.append((accession, symbol, gene, len(parts), n_reference, tpm, tpm < 1))
        values.append(observed)
    table(args.output / "mapping_qc.tsv", ("gsm", "targets", "mapped", "unmapped", "total_tpm"), audited)
    table(args.output / "gene_tpm.tsv", ("gsm", "symbol", "gene_id", "indexed_transcripts", "release79_transcripts", "tpm", "below_1_tpm"), source)
    if args.stage == "withdrawal":
        rows = []
        effects = [{}, {}]
        for j in range(2):
            group = values[j * 3:j * 3 + 3]
            for symbol in symbols:
                baseline, first, second = (row[symbol] for row in group)
                effect = statistics.mean((math.log2(first + 1), math.log2(second + 1))) - math.log2(baseline + 1)
                effects[j][symbol] = effect
                rows.append((j + 1, symbol, baseline, first, second, effect))
        table(args.output / "withdrawal.tsv", ("experiment", "symbol", "ex_vivo_tpm", "culture_1_tpm", "culture_2_tpm", "log2_difference"), rows)
        plot(args.output, values, effects)
    else:
        rows = []
        for symbol in symbols:
            minus, plus, deprogrammed, cargo = [statistics.mean(row[symbol] for row in values[i:i + 2]) for i in range(0, 8, 2)]
            flagged = cargo > 2 * minus
            fold = plus / minus if minus > 0 and not flagged else "NA"
            rows.append((symbol, minus, plus, deprogrammed, cargo, flagged, cargo > 2 * plus, fold, min(minus, plus) < 1))
        table(args.output / "challenge.tsv", ("symbol", "programmed_minus_tpm", "programmed_plus_tpm", "deprogrammed_plus_tpm", "cargo_tpm", "exclude_cargo_gt_2x_minus", "cargo_gt_2x_plus", "programmed_fold", "low_tpm"), rows)


if __name__ == "__main__":
    main()
