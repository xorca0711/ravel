"""Reconstruct deposited ICA activities/projections without claiming a new ICA fit."""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import pandas as pd
import openpyxl

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "raw_data/nabhan_2026_sources"
OUT = HERE / "runs/R3_v1"

def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()

def main():
    if OUT.exists():
        raise SystemExit("Refusing to overwrite existing component reconstruction")
    schema = json.loads((HERE / "reports/supplement_schema.json").read_text())
    sources = {x["dataset"]: x for x in schema["datasets"]}
    for key in ("S6", "S7"):
        assert sha(ROOT / sources[key]["path"]) == sources[key]["sha256"]
    spec = json.loads((HERE / "config/Nb3_execution_v1.json").read_text())
    spec["programs"]["mouse"].update(json.loads((HERE / "config/Nb3_panel_amendment_v1.json").read_text())["replace_programs_mouse"])
    activities = pd.read_csv(ROOT / sources["S6"]["path"], index_col=0)
    activities.index.name = "source_target"
    activities = activities.reset_index()
    # Punctuation normalization is used only for joins; retain original deposited label.
    crosswalk = pd.read_csv(ROOT / spec["inputs"]["crosswalk"], sep="\t")
    normalize = lambda value: "".join(c for c in str(value).upper() if c.isalnum())
    lookup = {normalize(x): x for x in crosswalk.target.unique()}
    assert len(lookup) == crosswalk.target.nunique()
    activities.insert(1, "target", activities.source_target.map(lambda x: lookup.get(normalize(x))))
    assert activities.target.notna().all() and activities.target.is_unique
    OUT.mkdir()
    activities.to_csv(OUT / "source_ICA_activities.tsv", sep="\t", index=False)
    wb = openpyxl.load_workbook(ROOT / sources["S7"]["path"], read_only=True, data_only=True)
    top, markers, dimensions = [], [], []
    for ws in wb:
        rows = ws.iter_rows(values_only=True)
        header = list(next(rows))
        columns = [header.index(x) for x in ("ID", "symbol", "gene_zscoreOfProj")]
        table = pd.DataFrame(([r[c] for c in columns] for r in rows), columns=["ID", "symbol", "projection_z"])
        assert table.ID.is_unique and np.isfinite(table.projection_z).all()
        dimensions.append({"component": ws.title, "genes": len(table)})
        table["component"] = ws.title
        top.append(table.loc[table.projection_z.abs().nlargest(200).index])
        for panel, genes in spec["programs"]["mouse"].items():
            selected = table[table.symbol.isin(genes)].copy()
            selected["program"] = panel
            markers.append(selected)
        print(f"{ws.title}: {len(table)} source projections", flush=True)
    wb.close()
    pd.concat(top, ignore_index=True).to_csv(OUT / "source_ICA_top200.tsv", sep="\t", index=False)
    pd.concat(markers, ignore_index=True).to_csv(OUT / "source_ICA_panel_projections.tsv", sep="\t", index=False)
    record = {"analysis_id": "Nb3_R3", "status": "partial_source_reconstruction",
        "script_sha256": sha(Path(__file__)), "source_sha256": {key: sources[key]["sha256"] for key in ("S6", "S7")},
        "activity_targets": len(activities), "components": dimensions,
        "target_alias_rule": "uppercase and remove punctuation for unambiguous exact crosswalk match; preserve deposited names",
        "cpca_status": "held: source alpha/implementation settings unresolved",
        "fresh_JADE_status": "held: source input settings and exact implementation unresolved",
        "interpretation": "Deposited component identities; source-table reconstruction, not independently refitted components or validation"}
    (OUT / "run_record.json").write_text(json.dumps(record, indent=2) + "\n")

if __name__ == "__main__":
    main()
