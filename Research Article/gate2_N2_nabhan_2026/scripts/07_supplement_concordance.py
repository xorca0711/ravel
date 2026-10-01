"""Compare reconstructed DE with S4/S5 on their selected gene universe only."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import pandas as pd
import openpyxl
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
CACHE = ROOT / "raw_data/GSE307112/Nb3_v1"
OUT = HERE / "runs/R2_v1"

def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()

def prepare():
    schema = {x["dataset"]: x for x in json.loads((HERE / "reports/supplement_schema.json").read_text())["datasets"]}
    for species, key in (("mouse", "S4"), ("human", "S5")):
        dest = CACHE / f"source_DE_{species}.npz"
        record_file = CACHE / f"source_DE_{species}.json"
        source = ROOT / schema[key]["path"]
        source_sha = sha(source)
        assert source_sha == schema[key]["sha256"]
        if dest.exists():
            record = json.loads(record_file.read_text())
            assert record["source_sha256"] == source_sha and record["cache_sha256"] == sha(dest)
            continue
        wb = openpyxl.load_workbook(source, read_only=True, data_only=True)
        rows = wb.active.iter_rows(values_only=True)
        header = list(next(rows))
        table = pd.DataFrame(rows, columns=header)
        wb.close()
        assert table.gene.is_unique and table.gene.notna().all()
        targets = [x.removesuffix("_logFC") for x in header if x.endswith("_logFC")]
        logfc = table[[f"{x}_logFC" for x in targets]].to_numpy(dtype=float)
        padj = table[[f"{x}_padj" for x in targets]].to_numpy(dtype=float)
        np.savez_compressed(dest, gene=table.gene.to_numpy(dtype=str), targets=np.array(targets), logfc=logfc, padj=padj)
        record_file.write_text(json.dumps({"source_sha256": source_sha, "cache_sha256": sha(dest),
            "genes": len(table), "targets": len(targets), "selection": "source-selected genes, not full tested universe"}, indent=2) + "\n")
        print(f"{species}: {len(table)} source-selected genes, {len(targets)} targets", flush=True)

def compare():
    if (OUT / "source_concordance.tsv").exists():
        raise SystemExit("Refusing to overwrite source concordance")
    run = json.loads((OUT / "expression_record.json").read_text())
    assert run["status"] == "completed"
    manifest = {str(path.relative_to(CACHE)).replace("\\", "/"): sha(path) for path in sorted((CACHE / "DE").glob("*/*.tsv.gz"))}
    (OUT / "DE_manifest.json").write_text(json.dumps({"files": manifest, "count": len(manifest)}, indent=2) + "\n")
    rows, focal_gene_tables = [], []
    spec = json.loads((HERE / "config/Nb3_execution_v1.json").read_text())
    spec["programs"]["mouse"].update(json.loads((HERE / "config/Nb3_panel_amendment_v1.json").read_text())["replace_programs_mouse"])
    focal = {"NKX21", *spec["R4_extensions"]["comparison_targets"]}
    for species in ("mouse", "human"):
        source = np.load(CACHE / f"source_DE_{species}.npz")
        for i, target in enumerate(source["targets"]):
            path = CACHE / "DE" / species / f"{target}.tsv.gz"
            if not path.exists():
                rows.append(dict(species=species, target=target, status="no_eligible_reconstruction"))
                continue
            ours = pd.read_csv(path, sep="\t").set_index("ID")
            if target in focal:
                markers = {gene for panel in spec["programs"][species].values() for gene in panel}
                markers.update(("Egfr", "Erbb2", "Erbb3", "Erbb4", "Nkx2-1") if species == "mouse" else ("EGFR", "ERBB2", "ERBB3", "ERBB4"))
                selected_markers = ours[ours.symbol.isin(markers)].reset_index()
                selected_markers.insert(0, "target", target)
                selected_markers.insert(0, "species", species)
                focal_gene_tables.append(selected_markers)
            original = pd.DataFrame({"source_logFC": source["logfc"][:, i], "source_padj": source["padj"][:, i]}, index=source["gene"])
            paired = original.join(ours[["logFC", "adj.P.Val", "AveExpr"]], how="inner").dropna()
            x, y = paired.source_logFC, paired.logFC
            selected = paired.source_padj < .05
            rows.append(dict(species=species, target=target, status="source_selected_comparison", source_genes=len(original), common_genes=len(paired),
                pearson_logFC=x.corr(y), spearman_logFC=float(spearmanr(x,y).statistic),
                sign_agreement=float((np.sign(x) == np.sign(y)).mean()), median_abs_logFC_difference=float((x-y).abs().median()),
                source_q05_in_common=int(selected.sum()), both_q05_AveExpr_pass=int((selected & (paired["adj.P.Val"] < .05) & (paired.AveExpr > 1.5)).sum())))
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "source_concordance.tsv", sep="\t", index=False)
    pd.concat(focal_gene_tables, ignore_index=True).to_csv(OUT / "focal_gene_DE.tsv", sep="\t", index=False)
    (OUT / "source_concordance_record.json").write_text(json.dumps({"analysis_id": "Nb3_R2", "script_sha256": sha(Path(__file__)),
        "selection_warning": "Concordance is conditional on S4/S5 source-selected genes; this is not independent validation or exact source pipeline recovery",
        "species_summary": table.groupby("species")[["pearson_logFC", "spearman_logFC", "sign_agreement"]].median().to_dict(),
        "table_sha256": sha(OUT / "source_concordance.tsv")}, indent=2) + "\n")
    print(table.groupby("species")[["pearson_logFC", "spearman_logFC", "sign_agreement"]].median().round(3).to_string())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    prepare()
    if not args.prepare_only:
        compare()
