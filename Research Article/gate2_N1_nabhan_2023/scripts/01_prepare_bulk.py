"""Audit count/annotation schema and prepare a gene-ID matrix before endpoint fitting."""
from __future__ import annotations
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(2**20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    manifest = json.loads((ROOT / "metadata/count_download_manifest.json").read_text())
    meta = pd.read_csv(ROOT / "metadata/samples.tsv", sep="\t")
    matrices, audits, original = [], [], None
    for row in manifest["files"]:
        path = ROOT / row["path"]
        assert sha(path) == row["sha256"]
        tab = pd.read_csv(path, sep="\t")
        assert list(tab) == ["name", "count", "width", "rpkm"]
        assert tab.name.is_unique and tab.name.str.match(r"^ENSMUSG\d+$").all()
        assert np.isfinite(tab[["count", "width", "rpkm"]]).all().all()
        assert (tab[["count", "rpkm"]] >= 0).all().all() and (tab.width > 0).all()
        assert np.equal(tab["count"], np.floor(tab["count"])).all()
        if original is None:
            original = tab[["name", "width"]].copy()
        assert original.equals(tab[["name", "width"]]), "Gene order/width differs"
        matrices.append(tab["count"].to_numpy(np.int64))
        # RPKM denominator can include reads not assigned to these rows.
        nz = tab["count"] > 0
        implied = tab.loc[nz, "count"] * 1e9 / (tab.loc[nz, "width"] * tab.loc[nz, "rpkm"])
        audits.append({"accession": row["accession"], "gene_rows": len(tab),
                       "assigned_counts": int(tab["count"].sum()),
                       "detected_genes": int(nz.sum()),
                       "rpkm_implied_denominator_median": float(implied.median()),
                       "rpkm_denominator_relative_spread": float((implied.max()-implied.min())/implied.median())})
    accessions = [x["accession"] for x in manifest["files"]]
    assert accessions == meta.accession.tolist()
    count = pd.DataFrame(np.column_stack(matrices), index=original.name, columns=accessions)
    count.to_csv(ROOT / "raw/bulk_counts.csv.gz", index_label="gene_id")
    gtf = ROOT / "raw/Mus_musculus.GRCm38.102.gtf.gz"
    mapping = {}
    with gzip.open(gtf, "rt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.split("\t")
            if fields[2] != "gene":
                continue
            attrs = dict(re.findall(r'(\w+) "([^"]+)"', fields[8]))
            mapping[attrs["gene_id"]] = attrs.get("gene_name", "")
    gene_map = pd.DataFrame({"gene_id": count.index, "symbol": [mapping.get(g, "") for g in count.index]})
    # Ambiguous symbols are retained in ID-level DE, excluded from set enrichment.
    gene_map["symbol_unique"] = gene_map.symbol.ne("") & ~gene_map.symbol.duplicated(keep=False)
    gene_map.to_csv(ROOT / "raw/gene_mapping.tsv", sep="\t", index=False)
    qc = pd.DataFrame(audits).merge(meta[["accession", "condition", "replicate_label"]], on="accession", validate="one_to_one")
    qc.to_csv(ROOT / "metadata/bulk_schema_qc.tsv", sep="\t", index=False)
    panels = json.loads((ROOT / "config/pipeline.json").read_text())["source_panels"]
    present = set(gene_map.symbol)
    aliases = {"Cyr61": "Ccn1", "Ctgf": "Ccn2", "Cenpc": "Cenpc1"}
    panel_coverage, members = {}, []
    for panel, genes in panels.items():
        resolved = [aliases.get(g, g) for g in genes]
        panel_coverage[panel] = {"resolved": [g for g in resolved if g in present],
                                 "unresolved_source_symbols": [g for g, r in zip(genes, resolved) if r not in present]}
        for original_symbol, symbol in zip(genes, resolved):
            hits = gene_map.loc[gene_map.symbol.eq(symbol), "gene_id"].tolist()
            members.append({"panel": panel, "source_symbol": original_symbol,
                            "annotation_symbol": symbol, "gene_id": hits[0] if len(hits)==1 else "",
                            "status": "resolved" if len(hits)==1 else "unresolved"})
    pd.DataFrame(members).to_csv(ROOT / "metadata/source_panel_membership.tsv", sep="\t", index=False)
    assert sum(r["status"] == "resolved" for r in members) == 19
    assert [r["source_symbol"] for r in members if r["status"] != "resolved"] == ["Crim2"]
    record = {"schema": ["name", "count", "width", "rpkm"], "libraries": len(accessions),
              "gene_rows": len(count), "count_integrity": "finite nonnegative integers; same gene order and widths in all libraries",
              "annotation": "Ensembl release 102, GRCm38; adapter to the paper's unrecovered internal gene model",
              "annotation_sha256": sha(gtf), "gene_mapping_sha256": sha(ROOT / "raw/gene_mapping.tsv"),
              "matrix_sha256": sha(ROOT / "raw/bulk_counts.csv.gz"),
              "mapped_gene_ids": int(gene_map.symbol.ne("").sum()),
              "unique_symbol_gene_ids": int(gene_map.symbol_unique.sum()),
              "source_panel_coverage": panel_coverage,
              "preparation_map_verified": False, "pairing_verified": False,
              "endpoint_analysis_performed": False, "code_sha256": sha(__file__)}
    (ROOT / "metadata/bulk_schema_audit.json").write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({k:record[k] for k in ["libraries", "gene_rows", "mapped_gene_ids", "unique_symbol_gene_ids", "source_panel_coverage"]}))


if __name__ == "__main__":
    main()
