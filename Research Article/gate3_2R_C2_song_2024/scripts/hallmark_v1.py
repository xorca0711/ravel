"""Source-defined mouse Hallmark rank summaries and single-library sensitivity."""
import csv
import json
import statistics as st
import sys
from pathlib import Path

from openpyxl import load_workbook

SOURCE = Path("analysis/research/runs/song24_c2_S3_v2")
GMT = Path("raw_data/song_v1/mouse_hallmark_2025.1.gmt")
PANELS = {"HALLMARK_OXIDATIVE_PHOSPHORYLATION", "HALLMARK_E2F_TARGETS", "HALLMARK_G2M_CHECKPOINT"}
CONTEXTS = ["young_ex_vivo", "young_homeo", "old"]


def main(output):
    with (SOURCE / "libraries.csv").open() as handle:
        libraries = list(csv.DictReader(handle))
    with (SOURCE / "expression.csv").open() as handle:
        expression = {r["gene"]: r for r in csv.DictReader(handle)}
    sets = {}
    for line in GMT.read_text().splitlines():
        name, _, *genes = line.split("\t")
        if name in PANELS:
            sets[name] = set(genes)
    assert sets.keys() == PANELS
    observed = set(expression)
    references = {}
    workbook = load_workbook("raw_data/song_v1/m2.xlsx", read_only=True, data_only=True)
    for title in ("Tab1", "Tab3"):
        references[title] = {r[0]: r[2] for r in workbook[title].values if isinstance(r[2], (int, float))}
    results = {}
    for name, members in sorted(sets.items()):
        genes = sorted(members & observed)
        assert genes
        result = {"uncovered": sorted(members - observed), "covered": len(genes), "size": len(members)}
        for omitted in [None] + [r["gsm"] for r in libraries]:
            arm = {}
            for context in CONTEXTS:
                for genotype in ("KO", "WT"):
                    arm[context, genotype] = [r["gsm"] for r in libraries if r["group"] == context
                                              and r["genotype"] == genotype and r["gsm"] != omitted]
            values = {}
            for gene, row in expression.items():
                contrasts = [st.mean(float(row[gsm]) for gsm in arm[context, "KO"])
                             - st.mean(float(row[gsm]) for gsm in arm[context, "WT"]) for context in CONTEXTS]
                values[gene] = contrasts + [contrasts[0] - contrasts[1], contrasts[2] - contrasts[1]]
            if omitted is None:
                result["median_log2"] = [st.median(values[g][i] for g in genes) for i in range(5)]
                for i, key in enumerate(("young_stim_KO_WT", "young_fresh_KO_WT", "old_fresh_KO_WT",
                                         "stim_minus_fresh", "old_minus_young_fresh")):
                    assert max(abs(values[g][i] - float(expression[g][key])) for g in genes) < 1e-9
                rank = sorted(expression, key=lambda g: (values[g][0], g))
                percentiles = {g: i/(len(rank)-1) for i,g in enumerate(rank)}
                result["young_stim_median_rank_percentile"] = st.median(percentiles[g] for g in genes)
                result["published_median_log2"] = {t: st.median(ref[g] for g in genes if g in ref)
                                                    for t, ref in references.items()}
            else:
                result.setdefault("leave_one_library", {})[omitted] = [
                    st.median(values[g][i] for g in genes) for i in range(5)]
        results[name] = result
    (output / "hallmark.json").write_text(json.dumps({"order": CONTEXTS + [
        "young stimulated minus fresh", "old minus young fresh"], "sets": results}, indent=2)+"\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
