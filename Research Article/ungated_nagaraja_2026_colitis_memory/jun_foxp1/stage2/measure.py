"""Compute the frozen per-locus measures from the qualified public sources."""
from pathlib import Path
from zipfile import ZipFile
import io
import sys

import numpy as np
import pandas as pd

from plot import draw


RUNS = Path("analysis/research/runs")
METH = RUNS / "ng26_jf_methylation_v1"
ATAC = RUNS / "ng26_jf_atac_eligibility_v1"
WINDOWS = ("amplicon", "left_flank", "right_flank", "scored_motif")
MODELS = {"organoid_history": "P4 organoid", "tissue_vehicle_history": "whole colon"}


def read(path, **kw):
    return pd.read_csv(path, sep="\t", **kw)


def save(df, out, name):
    df.to_csv(out / name, sep="\t", index=False, float_format="%.15g", na_rep="NA",
              compression={"method": "gzip", "mtime": 0} if name.endswith(".gz") else None)


def coordinates(value):
    return [] if pd.isna(value) else [int(v) for v in value.split("|")]


def biochemistry(panel):
    with ZipFile("raw_data/nagaraja_s0/moesm5.zip") as archive:
        name, = [n for n in archive.namelist() if "Table6_" in n and n.endswith(".xlsx")]
        raw = pd.read_excel(io.BytesIO(archive.read(name)), sheet_name="Raw in vitro binding score")
    result = panel.copy()
    for protein in ("JUN", "JUNFOXP1"):
        rows = raw.iloc[result[protein + "_excel_row"].to_numpy() - 2].reset_index(drop=True)
        assert rows.TF.eq(protein).all()
        assert (rows.Chromosome == result.chrom).all() and (rows.Start == result.scored_start).all()
        assert (rows.End == result.scored_end).all()
        result[protein + "_raw"] = rows.meanfootprintscore
    jun, pair = result.JUN_raw, result.JUNFOXP1_raw
    assert np.isfinite(jun).all() and np.isfinite(pair).all()
    result["increment"] = pair - jun
    result["raw_ratio"] = pair / jun.where(jun.ne(0))
    result["ratio_status"] = np.select([jun.eq(0), jun.lt(0) | pair.lt(0)],
                                       ["zero denominator", "signed scale"], default="fold eligible")
    result["fold_ratio"] = result.raw_ratio.where(result.ratio_status.eq("fold eligible"))
    stats = []
    for label, g in result.groupby("motif_class"):
        stats.append(dict(motif_class=label, loci=len(g), median_JUN_raw=g.JUN_raw.median(),
                          median_JUNFOXP1_raw=g.JUNFOXP1_raw.median(), median_increment=g.increment.median(),
                          positive=int(g.increment.gt(0).sum()), zero=int(g.increment.eq(0).sum()),
                          negative=int(g.increment.lt(0).sum()), defined_ratios=int(g.raw_ratio.count()),
                          signed_scale=int(g.ratio_status.eq("signed scale").sum()),
                          zero_denominators=int(g.JUN_raw.eq(0).sum()), fold_eligible=int(g.fold_ratio.count()),
                          median_fold_ratio=g.fold_ratio.median()))
    return result, pd.DataFrame(stats)


def accessibility(amp):
    counts = read(ATAC / "atac_sample_windows.tsv.gz", dtype={"time": str})
    depth = read(ATAC / "atac_donor_depth.tsv", dtype={"time": str})
    keys = ["export", "time", "specimen", "donor", "condition", "min_autosomal_per_barcode"]
    select = counts.export.eq("extended") & counts.min_autosomal_per_barcode.eq(300) & counts.window.eq("amplicon")
    mice = counts.loc[select].merge(depth[keys + ["source_alias", "barcodes", "autosomal_unique"]],
                                    on=keys, validate="many_to_one")
    mice = mice.merge(amp, on="locus", validate="many_to_one")
    assert (mice.autosomal_denominator == mice.autosomal_unique).all()
    valid = mice.autosomal_denominator.gt(0)
    assert mice.unique_fragment_overlaps.notna().equals(valid)
    assert mice.loc[~valid, "specimen"].unique().tolist() == ["IGVFSM0940ZCKQ"]
    assert not mice.duplicated(["time", "donor", "locus"]).any()
    mice["status"] = np.select([~valid, mice.unique_fragment_overlaps.eq(0)],
                               ["held identity; no denominator", "measured zero"], default="measured")
    mice["CPM"] = 1e6 * mice.unique_fragment_overlaps / mice.autosomal_denominator.where(valid)
    mice["CPM_per_kb"] = 1000 * mice.CPM / mice.width_bp
    rows = []
    for (day, locus), g in mice[mice.time.isin(["50", "102"])].groupby(["time", "locus"], sort=False):
        c, r = (g.loc[g.condition.eq(k), "CPM"] for k in ("control", "colitis"))
        assert c.count() == len(c) == 2 and r.count() == len(r) == {"50": 2, "102": 4}[day]
        width = int(g.width_bp.iloc[0])
        delta = r.mean() - c.mean()
        rows.append(dict(time=day, locus=locus, width_bp=width, control_n=len(c), recovered_n=len(r),
                         control_mean_CPM=c.mean(), recovered_mean_CPM=r.mean(), delta_CPM=delta,
                         delta_CPM_per_kb=1000 * delta / width))
    assert len(rows) == 126 and len(mice) == 63 * 13
    return mice, pd.DataFrame(rows)


def regional_methylation(panel, geom):
    sources = read(METH / "methylation_sources.tsv")
    sources = sources[~sources.arm.str.contains("T5224")]
    coverage = read(METH / "methylation_contrast_coverage.tsv", dtype={"common_plus_C": "string"})
    coverage = coverage[coverage.contrast.isin(MODELS) & coverage.window.isin(WINDOWS)].copy()
    coverage = coverage.merge(geom[["locus", "window", "chrom", "start", "end", "width_bp", "CpGs_per_100bp"]],
                              on=["locus", "window"], validate="many_to_one")
    coverage["model"] = coverage.contrast.map(MODELS)
    index = panel.set_index("locus").amplicon_row
    sites, values = [], []
    with ZipFile(METH / "stage1_sources.zip") as archive:
        for (model, locus), windows in coverage.groupby(["model", "locus"], sort=False):
            selected = sources[sources.model.eq(model)]
            assert len(selected) == 6 and selected.mouse.nunique() == 6
            for s in selected.itertuples():
                arm = "control" if s.arm.startswith("Control") else "recovered"
                base = dict(model=model, locus=locus, gsm=s.gsm, mouse=s.mouse, source_arm=s.arm, arm=arm)
                native = {}
                for line in archive.read(f"methylation/{s.gsm}/{index[locus]}.bedGraph").decode().splitlines():
                    chrom, start, end, frac = line.split()
                    assert chrom == windows.chrom.iloc[0] and 0 <= float(frac) <= 1
                    for pos in range(int(start), int(end)):
                        assert pos not in native
                        native[pos] = float(frac)
                for w in windows.itertuples():
                    coords = coordinates(w.common_plus_C)
                    assert len(coords) == w.common_CpGs and len(set(coords)) == len(coords)
                    fractions = [native[pos] for pos in coords]
                    values.append(dict(**base, window=w.window, width_bp=w.width_bp,
                                       reference_CpGs=w.reference_CpGs, common_CpGs=w.common_CpGs,
                                       mean_fraction=np.mean(fractions) if coords else np.nan))
                    if w.window == "amplicon":
                        sites.extend(dict(**base, chrom=w.chrom, plus_C=pos, fraction=native[pos]) for pos in coords)
    specimen = pd.DataFrame(values)
    groups = specimen.groupby(["model", "locus", "window", "arm"]).mean_fraction.agg(
        ["size", "count", "mean"]).unstack("arm")
    groups.columns = [f"{arm}_{stat}" for stat, arm in groups.columns]
    groups = groups.rename(columns={f"{arm}_{s}": f"{arm}_{label}" for arm in ("recovered", "control")
                                     for s, label in (("size", "n_nominal"), ("count", "n_usable"),
                                                      ("mean", "mean_fraction"))})
    history = coverage.merge(groups.reset_index(), on=["model", "locus", "window"], validate="one_to_one")
    history["delta_pp"] = 100 * (history.recovered_mean_fraction - history.control_mean_fraction)
    assert len(history) == 504 and len(sites) == 6684 and len(specimen) == 3024
    for arm in ("control", "recovered"):
        assert history[f"{arm}_n_nominal"].eq(3).all()
        assert (history[f"{arm}_n_usable"] == 3 * history.common_CpGs.gt(0)).all()
    return pd.DataFrame(sites), specimen, history


def main(out):
    panel = read(METH / "binding_panel.tsv")
    assert len(panel) == panel.locus.nunique() == 63
    geom = read(METH / "mm10_windows.tsv")
    geom = geom[geom.window.isin(WINDOWS)].copy()
    geom[["start", "end"]] = geom[["start", "end"]].astype(int)
    geom["width_bp"] = geom.end - geom.start
    geom["CpGs_per_100bp"] = 100 * geom.reference_CpGs / geom.width_bp
    amp = geom.loc[geom.window.eq("amplicon"), ["locus", "width_bp", "reference_CpGs", "CpGs_per_100bp"]]
    binding, classes = biochemistry(panel)
    mice, atac = accessibility(amp)
    sites, lines, meth = regional_methylation(panel, geom)
    integrated = binding.merge(amp, on="locus", validate="one_to_one")
    for day, g in atac.groupby("time"):
        sub = g.drop(columns=["time", "width_bp"]).set_index("locus").add_prefix(f"d{day}_")
        integrated = integrated.join(sub, on="locus", validate="one_to_one")
    for (model, window), g in meth.groupby(["model", "window"]):
        prefix = ("P4" if model == "P4 organoid" else "tissue_vehicle") + "_" + window + "_"
        cols = ["width_bp", "reference_CpGs", "common_CpGs", "control_n_usable", "recovered_n_usable",
                "control_mean_fraction", "recovered_mean_fraction", "delta_pp"]
        integrated = integrated.join(g.set_index("locus")[cols].add_prefix(prefix), on="locus", validate="one_to_one")
    for df, name in ((binding, "biochemical_loci.tsv"), (classes, "binding_by_class.tsv"),
                     (mice, "atac_specimens.tsv"), (atac, "atac_history.tsv"),
                     (sites, "methylation_sites.tsv.gz"), (lines, "methylation_specimens.tsv.gz"),
                     (meth, "methylation_history.tsv"), (integrated, "locus_measurements.tsv")):
        save(df, out, name)
    draw(binding, atac, meth, lines, out)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
