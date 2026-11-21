"""Index Supplementary Tables 2–4 without collapsing distinct assay leaders."""
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd

CACHE = Path("raw_data/nagaraja_s0")
RUNS = Path("analysis/research/runs")


def read_tables():
    with ZipFile(CACHE / "moesm5.zip") as archive:
        def table(index):
            name, = [name for name in archive.namelist() if f"SupplementalTable{index}_" in name]
            return pd.read_excel(BytesIO(archive.read(name)))
        catalog, tissue, organoid = [table(i) for i in (2, 3, 4)]
    tissue = tissue.loc[tissue["sample"].eq("Colitis_recovered") & tissue.cell_type.eq("stem_prog")].copy()
    assert (len(catalog), len(tissue), len(organoid)) == (361, 50, 299)
    assert all(series.is_unique for series in (catalog.leader, tissue.bag_leader, organoid.bag_leader))
    return catalog, tissue, organoid


def inventory():
    catalog, tissue, organoid = read_tables()
    tissue = tissue.set_index("bag_leader")
    organoid = organoid.set_index("bag_leader")
    lookup = {}
    catalog_rows = []
    for bag, raw in catalog.itertuples(index=False):
        members = set(raw.split(",")) | {bag}
        for motif in members:
            if motif in lookup:
                raise ValueError(f"Overlapping Table 2 group for {motif}")
            lookup[motif] = bag
        tr = sorted(members.intersection(tissue.index))
        oe = sorted(members.intersection(organoid.index))
        catalog_rows.append(dict(table2_leader=bag, members=raw, tissue_reporters="|".join(tr),
                                 organoid_reporters="|".join(oe), n_tissue=len(tr), n_organoid=len(oe)))
    t = tissue[["delta", "pval", "padj"]].add_prefix("tissue_")
    o = organoid.add_prefix("org_")
    leaders = t.join(o, how="outer")
    leaders.index.name = "feature"
    leaders["table2_leader"] = [lookup.get(x, "") for x in leaders.index]
    leaders["organ_aligned"] = leaders.org_shuf_median_var - leaders.org_clone_median_var
    leaders["tissue_status"] = np.select(
        [leaders.tissue_padj.isna(), leaders.tissue_padj.lt(.05) & leaders.tissue_delta.gt(0),
         leaders.tissue_padj.lt(.05) & leaders.tissue_delta.lt(0)],
        ["unreported", "gain", "loss"], default="tested nonhit")
    leaders["organ_status"] = np.select(
        [leaders.org_fdr.isna(), leaders.org_fdr.lt(.05) & leaders.organ_aligned.gt(0),
         leaders.org_fdr.lt(.05) & leaders.organ_aligned.lt(0)],
        ["unevaluable", "tighter", "wider"], default="tested nonhit")
    prior = pd.read_csv(RUNS / "ng26_s2_v1/dispersion.tsv", sep="\t")
    for label, frame in prior.groupby("variant"):
        vals = frame.set_index("feature")[["observed", "null_mean", "fdr"]].copy()
        vals["aligned"] = vals.null_mean - vals.observed
        leaders = leaders.join(vals.add_prefix(label + "_"))
    pairs = []
    for tname in sorted(tissue.index):
        for oname in sorted(organoid.index):
            exact = tname == oname
            if exact or (lookup.get(tname) is not None and lookup[tname] == lookup.get(oname)):
                pairs.append(dict(tissue_feature=tname, organoid_feature=oname,
                                  table2_leader=lookup.get(tname, ""), match="exact" if exact else "member proxy",
                                  tissue_delta=leaders.at[tname,"tissue_delta"], tissue_q=leaders.at[tname,"tissue_padj"],
                                  tissue_status=leaders.at[tname,"tissue_status"], organ_aligned=leaders.at[oname,"organ_aligned"],
                                  organ_q=leaders.at[oname,"org_fdr"], organ_status=leaders.at[oname,"organ_status"]))
    return pd.DataFrame(catalog_rows), leaders, pd.DataFrame(pairs)


def exclusive_matrix(features):
    cells = pd.read_csv(RUNS / "ng26_s5_v1/exclusive_cells.tsv", sep="\t")
    cells = cells.sort_values(["organoid_line", "clone", "atac_cell"]).reset_index(drop=True)
    keys = ["atac_cell", "clone", "sample"]
    assert cells.atac_cell.is_unique and cells.organoid_line.nunique() == cells.mouse_donor.nunique() == 6
    blocks = []
    for part in pd.read_csv(CACHE / "moesm4.txt", sep="\t", chunksize=125000):
        part = part.loc[part.feature.isin(features)]
        blocks.append(part.merge(cells[keys], how="inner", on=keys, validate="many_to_one"))
    scores = pd.concat(blocks).pivot(index="atac_cell", columns="feature", values="score")
    scores = scores.reindex(index=cells.atac_cell, columns=sorted(features))
    for name in ("Fos", "Hnf4g"):
        np.testing.assert_allclose(scores[name], cells[name], rtol=1e-10, atol=1e-10)
    return cells, scores
