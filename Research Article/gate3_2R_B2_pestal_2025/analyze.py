"""Descriptive gene-level replay of the Pestal deposits."""
import argparse
import gzip
import json
import re
from pathlib import Path

import h5py
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = Path("raw_data/pestal")
MARKERS = {
    "transfer": "Gata6 Rara Rarg Rxra Timd4 Icam2 Mafb Nt5e Lyve1".split(),
    "regulatory": "Gata6 Rara Rarb Rarg Rxra Timd4 Icam2 Mafb Bhlhe40 Cebpb Serpinb2 Hp Tgfb2".split(),
    "lung": "Car4 Perp Epcam Cpne5 Fcgr2b Mrc1 Cd74 Ctsk Itgax Siglecf Cd24a Pparg".split(),
}


def table(number):
    df = pd.read_excel(RAW / f"jem_20240379_tables{number}.xlsx")
    df = df[["Gene name", "log2FoldChange", "padj"]].dropna(subset=["Gene name"])
    df.columns = ["gene", f"S{number}_author_lfc", f"S{number}_author_padj"]
    return df.loc[~df.gene.duplicated(keep=False)].set_index("gene")


def annotation(build, feature):
    with gzip.open(RAW / f"{build}.gtf.gz", "rt") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.rstrip().split("\t")
            if fields[2] == feature:
                yield fields, dict(re.findall(r'(\w+) "([^"]+)"', fields[8]))


def expression(start, stop):
    names = {}
    for _, attrs in annotation("GRCm38", "transcript"):
        if "gene_name" in attrs:
            names[attrs["transcript_id"]] = attrs["gene_name"]
    values = {}
    provenance = []
    for path in sorted(RAW.glob("GSM*.h5")):
        accession, sample = path.stem.split("_", 1)
        if not start <= int(accession[3:]) <= stop:
            continue
        with h5py.File(path) as h:
            ids = [x.decode() for x in h["aux/ids"][:]]
            counts = h["est_counts"][:]
            length = h["aux/eff_lengths"][:]
            rate = np.divide(counts, length, out=np.zeros_like(counts), where=length > 0)
            tpm = rate * (1e6 / rate.sum())
            mapped = [names.get(x.split(".")[0]) for x in ids]
            by_gene = pd.Series(tpm, index=mapped).groupby(level=0).sum()
            values[sample] = by_gene
            provenance.append(dict(accession=accession, sample=sample, targets=len(ids),
                                   matched=sum(x is not None for x in mapped),
                                   mapped_tpm=float(by_gene.sum()),
                                   bootstrap=int(h["aux/num_bootstrap"][0]),
                                   kallisto=h["aux/kallisto_version"][0].decode(),
                                   call=h["aux/call"][0].decode()))
    return pd.DataFrame(values).sort_index(), pd.DataFrame(provenance)


def contrast(log, a, b):
    return log.filter(regex=a).mean(axis=1) - log.filter(regex=b).mean(axis=1)


def agreement(frame, n, local, summary):
    column = f"S{n}_author_lfc"
    shared = frame[[column, local]].dropna()
    keep = shared[column].abs().ge(1) & shared[local].ne(0)
    summary[f"S{n}_comparison"] = dict(
        shared=len(shared), rho=float(shared.corr(method="spearman").iloc[0, 1]),
        strong_author_nonzero_local=int(keep.sum()),
        same_sign=int((np.sign(shared.loc[keep, column]) == np.sign(shared.loc[keep, local])).sum()),
    )


def occupancy():
    peaks = pd.read_csv(RAW / "peaks.bed.gz", sep="\t", header=None,
                        names=["chrom", "start", "end", "peak", "score", "strand"],
                        dtype={"chrom": str})
    rows = []
    for f, attrs in annotation("GRCm39", "gene"):
        gene = attrs.get("gene_name")
        if gene in MARKERS["regulatory"]:
            lo, hi = int(f[3]) - 1, int(f[4])
            tss = lo if f[6] == "+" else hi - 1
            selected = peaks[(peaks.chrom == f[0]) & (peaks.start < max(hi, tss + 2001))
                             & (peaks.end > min(lo, tss - 2000))]
            rows.append(dict(gene=gene, chromosome=f[0], start=lo, end=hi, tss=tss,
                             overlap=len(selected), coordinates=";".join(
                                 f"{r.chrom}:{r.start}-{r.end}" for r in selected.itertuples())))
    return pd.DataFrame(rows).set_index("gene")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=MARKERS)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    stage, output = args.stage, args.output
    limits = {"transfer": (8763466, 8763474), "regulatory": (8763475, 8763480),
              "lung": (8763481, 8763484)}
    tpm, qc = expression(*limits[stage])
    assert len(tpm.columns) == limits[stage][1] - limits[stage][0] + 1
    qc.to_csv(output / "libraries.tsv", sep="\t", index=False)
    log = np.log2(tpm + 1)
    effect = pd.DataFrame(index=log.index)
    summary = {}
    if stage == "transfer":
        effect["WT_KO_day7"] = contrast(log, "WTday7", "KOday7")
        effect["WT_KO_day0"] = contrast(log, "WTday0", "KOday0")
        effect["day7_minus_day0"] = effect.WT_KO_day7 - effect.WT_KO_day0
        effect["WT_KO_day7_without_GSM8763472"] = contrast(log, "WTday7_[12]$", "KOday7")
        effect = effect.join(table(2), how="outer").join(table(1), how="outer")
        agreement(effect, 2, "WT_KO_day7", summary)
        for direction, label in [(1, "S1_positive"), (-1, "S1_negative")]:
            mask = effect.S1_author_lfc * direction >= 1
            mask &= effect.S1_author_padj <= 0.1
            summary[label] = {col: dict(n=int(effect.loc[mask, col].count()),
                                         median=float(effect.loc[mask, col].median()))
                              for col in ["WT_KO_day0", "WT_KO_day7", "day7_minus_day0",
                                          "WT_KO_day7_without_GSM8763472"]}
    elif stage == "regulatory":
        effect["KLF2_EV"] = contrast(log, "KLF2OE", "empty")
        effect["GATA6_EV"] = contrast(log, "GATA6OE", "empty")
        for n, local in [(3, "KLF2_EV"), (4, "GATA6_EV")]:
            effect = effect.join(table(n), how="outer")
            agreement(effect, n, local, summary)
        effect = effect.join(table(2), how="outer").join(occupancy(), how="outer")
    else:
        effect["WT_KO"] = contrast(log, "(?i)WT", "(?i)KO")
        effect = effect.join(table(5), how="outer")
        agreement(effect, 5, "WT_KO", summary)
    effect.to_csv(output / "effects.tsv", sep="\t", index_label="gene")
    marks = MARKERS[stage]
    effect.reindex(marks).join(tpm).to_csv(output / "markers.tsv", sep="\t", index_label="gene")
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    fig, ax = plt.subplots(figsize=(9, 5))
    image = ax.imshow(log.reindex(marks), aspect="auto", cmap="viridis")
    ax.set_yticks(range(len(marks)), marks)
    ax.set_xticks(range(len(log.columns)), log.columns, rotation=40, ha="right")
    fig.colorbar(image, ax=ax, label="log2(gene TPM + 1)")
    fig.tight_layout()
    fig.savefig(output / "markers.png", dpi=160)


if __name__ == "__main__":
    main()
