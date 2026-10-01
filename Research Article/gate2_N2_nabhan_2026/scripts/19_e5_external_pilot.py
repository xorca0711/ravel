"""Descriptive GSE306184 pilot under the pre-reading E5 contract."""
from pathlib import Path
import gzip
import hashlib
import io
import json
import tarfile
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import openpyxl

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
OUT = HERE / "runs/E5_external_v1"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, frame):
    frame.to_csv(OUT / f"{name}.tsv", sep="\t", index=False, float_format="%.12g", lineterminator="\n")


def main():
    if OUT.exists():
        raise SystemExit("Refusing to overwrite E5_external_v1")
    config_path = HERE / "config/Nb3_E5_external_v1.json"
    spec = json.loads(config_path.read_text())
    receipt = json.loads((HERE / spec["input_receipt"]).read_text())
    for item in receipt["inputs"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    metadata = {d["GSM"]: d for d in json.loads((HERE / "runs/E5_metadata_v1/sample_metadata.json").read_text())}
    columns, library_rows, symbol_order = {}, [], None
    archive_path = ROOT / "raw_data/GSE306184/GSE306184_RAW.tar"
    with tarfile.open(archive_path) as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            gsm = Path(member.name).name.split("_", 1)[0]
            record = metadata[gsm]
            library = record["description"][0].split(": ", 1)[1]
            raw = archive.extractfile(member).read()
            if member.name.endswith(".gz"):
                raw = gzip.decompress(raw)
            wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
            rows = list(wb.worksheets[0].iter_rows(values_only=True))
            wb.close()
            assert rows[0] == ("Gene_Symbol", library+"_Read_Count"), (gsm, rows[0])
            assert len(rows)-1 == spec["expected_rows_per_workbook"]
            genes = [r[0] for r in rows[1:]]
            if symbol_order is None:
                symbol_order = genes
            assert genes == symbol_order, gsm
            values = np.asarray([r[1] for r in rows[1:]], dtype=float)
            assert np.isfinite(values).all() and (values >= 0).all(), gsm
            columns[gsm] = values
            prefix, context, repeat = library.split("_")
            target = {"1si": "EGFR", "3si": "ERBB3", "Consi": "control"}[prefix]
            assert ("EGFR" if target == "EGFR" else "Erbb3" if target == "ERBB3" else "control") in record["title"][0]
            library_rows.append(dict(GSM=gsm, library=library, target=target, context=context,
                                     source_repeat_label=repeat, integer_fraction=float(np.mean(values == np.floor(values))),
                                     input_rows=len(values)))
    assert len(columns) == spec["expected_samples"]
    counts = pd.DataFrame(columns, index=symbol_order)
    blank = counts.index.isna() | (counts.index.astype(str).str.strip() == "")
    blank_sums = counts.loc[blank].sum()
    blank_rows = int(blank.sum())
    counts = counts.loc[~blank].groupby(level=0, sort=False).sum()
    libraries = pd.DataFrame(library_rows).set_index("GSM").loc[counts.columns]
    totals = counts.sum(axis=0)
    assert (totals > 0).all()
    libraries["count_total"] = totals
    libraries["blank_symbol_count_total"] = blank_sums
    libraries["blank_symbol_rows"] = blank_rows
    libraries["unique_symbols"] = len(counts)
    libraries["duplicate_rows_collapsed"] = spec["expected_rows_per_workbook"]-blank_rows-len(counts)
    libraries["detected_symbols"] = (counts > 0).sum(axis=0)
    cpm = counts.divide(totals, axis=1)*1e6
    positive = counts.where(counts > 0)
    eligible = (counts > 0).sum(axis=1) >= 7
    geom = np.exp(np.log(positive.loc[eligible]).mean(axis=1))
    factors = positive.loc[eligible].divide(geom, axis=0).median(axis=0)
    factors = factors / np.exp(np.log(factors).mean())
    assert np.isfinite(factors).all() and (factors > 0).all()
    sensitivity = counts.divide(factors, axis=1)/np.median(totals)*1e6
    libraries["positive_median_ratio_factor"] = factors
    genes = sum(spec["genes"].values(), [])
    assert len(genes) == len(set(genes))
    missing = sorted(set(genes)-set(counts.index))
    available = [gene for gene in genes if gene in counts.index]
    long_values, effects, panels = [], [], []
    for norm, matrix in [("CPM", cpm), ("positive_median_ratio_CPM", sensitivity)]:
        logged = np.log2(matrix.loc[available]+1)
        for gene in available:
            for gsm in counts.columns:
                long_values.append(dict(normalization=norm, gene=gene, GSM=gsm,
                    normalized_abundance=float(matrix.loc[gene, gsm]), log2_abundance_plus_1=float(logged.loc[gene, gsm]),
                    detected_ge1=bool(matrix.loc[gene, gsm] >= 1)))
        for target in spec["targets"]:
            for context in spec["contexts"]:
                treatment = libraries.index[(libraries.target == target) & (libraries.context == context)]
                control = libraries.index[(libraries.target == "control") & (libraries.context == context)]
                assert len(treatment) == len(control) == 2
                effect = logged[treatment].mean(axis=1)-logged[control].mean(axis=1)
                for gene in available:
                    effects.append(dict(normalization=norm, target=target, context=context, gene=gene,
                        effect=float(effect[gene]), target_mean=float(logged.loc[gene,treatment].mean()),
                        control_mean=float(logged.loc[gene,control].mean()), target_libraries=2, control_libraries=2))
                for panel, members in spec["genes"].items():
                    if panel == "receptors":
                        continue
                    complete = set(members).issubset(available)
                    panels.append(dict(normalization=norm, target=target, context=context, panel=panel,
                        effect=float(effect.loc[members].mean()) if complete else np.nan,
                        complete=complete, genes=len(members),
                        control_genes_detected_all_libraries=int((matrix.loc[[g for g in members if g in available],control] >= 1).all(axis=1).sum())))
    effects = pd.DataFrame(effects)
    context_delta = effects.pivot(index=["normalization", "target", "gene"], columns="context", values="effect")
    context_delta["IR_minus_Cyto"] = context_delta.IR-context_delta.Cyto
    OUT.mkdir(parents=True)
    write("sample_design_qc", libraries.reset_index())
    write("selected_source_counts", counts.loc[available].rename_axis("gene").reset_index())
    write("selected_normalized_values", pd.DataFrame(long_values))
    write("gene_contrasts", effects)
    write("panel_contrasts", pd.DataFrame(panels))
    write("context_difference", context_delta.reset_index())
    summary = dict(status="descriptive_pilot_only", samples=len(libraries), unique_symbols=len(counts),
                   missing_fixed_genes=missing, total_range=[int(totals.min()), int(totals.max())],
                   all_source_values_integer=bool((libraries.integer_fraction == 1).all()),
                   independent_donors="unresolved", metadata_conflicts=spec["metadata_conflicts"],
                   no_uninjured_knockdown=True, input_hashes=receipt["inputs"], config_sha256=sha(config_path),
                   script_sha256=sha(Path(__file__)), completed_utc=datetime.now(timezone.utc).isoformat(),
                   output_sha256={p.name: sha(p) for p in sorted(OUT.glob("*.tsv"))})
    (OUT / "run_record.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps({k:summary[k] for k in ["status", "samples", "unique_symbols", "missing_fixed_genes", "total_range", "all_source_values_integer"]}))
    print(pd.DataFrame(panels).to_string(index=False))
    print(effects[(effects.normalization == "CPM") & (effects.gene == effects.target)][["target", "context", "effect"]].to_string(index=False))


if __name__ == "__main__":
    main()
