"""Post-hoc audit of unexpected human S5 discordance; no relabeling or refitting."""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import openpyxl

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parents[1]
CACHE=ROOT/"raw_data/GSE307112/Nb3_v1"
OUT=HERE/"runs/concordance_audit_v1"
NS="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

def cell_value(cell):
    value=cell.find(NS+"v")
    if value is not None: return value.text
    return "".join(x.text or "" for x in cell.iter(NS+"t"))

def main():
    if OUT.exists(): raise SystemExit("Refusing to overwrite concordance audit")
    summaries, examples=[],[]
    focal=["NKX21","MET","ACOXL","TRP53","ERBB3"]
    reconstructed={target:pd.read_csv(CACHE/f"DE/human/{target}.tsv.gz",sep="\t").set_index("ID").logFC for target in focal}
    summary_signs={target:{"target":target,"compared":0,"matches":0,"missing_gene":0} for target in focal}
    for species,number in [("mouse","04"),("human","05")]:
        source=ROOT/f"raw_data/nabhan_2026_sources/pnas.2606113123.sd{number}.xlsx"
        workbook=openpyxl.load_workbook(source,read_only=True,data_only=True)
        rows=workbook.active.iter_rows(values_only=True); header=list(next(rows))
        indices={name:i for i,name in enumerate(header)}
        counts={"listed_direction_pairs":0,"direction_matches":0,"direction_conflicts":0,"missing_numeric":0,"summary_count_mismatches":0,"gene_rows":0}
        for row in rows:
            if not any(row): continue
            counts["gene_rows"]+=1
            for direction,field,nfield in [(1,"whichKOs_up","nbKOs_up"),(-1,"whichKOs_down","nbKOs_down")]:
                value=row[indices[field]]
                targets=str(value).split(",") if value else []
                if len(targets)!=int(row[indices[nfield]]): counts["summary_count_mismatches"]+=1
                for target in targets:
                    counts["listed_direction_pairs"]+=1
                    coef=row[indices[f"{target}_logFC"]]
                    if coef is None: counts["missing_numeric"]+=1; continue
                    match=np.sign(float(coef))==direction
                    counts["direction_matches" if match else "direction_conflicts"]+=1
                    if species=="human" and target in reconstructed:
                        identifier=row[indices["gene"]]
                        if identifier in reconstructed[target].index:
                            summary_signs[target]["compared"]+=1
                            summary_signs[target]["matches"]+=int(np.sign(reconstructed[target].loc[identifier])==direction)
                        else: summary_signs[target]["missing_gene"]+=1
                    if not match and (row[indices["symbol"]] in ["RGS5","CCL2","CXCL1","CXCL2","CXCL3","CXCL8","PLIN2","CTGF","ACTA2"] or len(examples)<5):
                        examples.append(dict(species=species,gene=row[indices["gene"]],symbol=row[indices["symbol"]],target=target,
                            listed_direction="up" if direction==1 else "down",numeric_logFC=coef,numeric_padj=row[indices[f"{target}_padj"]]))
        workbook.close()
        summaries.append(dict(species=species,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),**counts))
        print(species,counts,flush=True)
    # Does a simple target-column swap explain the human discrepancy? Keep
    # this diagnostic separate; never apply the best-looking labels as a fix.
    source=np.load(CACHE/"source_DE_human.npz")
    centered=source["logfc"]-source["logfc"].mean(axis=0)
    swaps=[]
    for target in focal:
        values=reconstructed[target].reindex(source["gene"]).to_numpy()
        values=values-values.mean()
        correlations=(values[:,None]*centered).sum(axis=0)/np.sqrt((values*values).sum()*(centered*centered).sum(axis=0))
        best=int(np.argmax(correlations))
        swaps.append(dict(reconstructed_target=target,best_source_target=source["targets"][best],maximum_pearson=float(correlations[best]),source_targets_checked=len(correlations)))
    # Independent XML parser verifies complete count rows for three affected
    # human markers, including every library, against the extracted binary.
    genes=pd.read_csv(CACHE/"human_genes.tsv",sep="\t")
    libraries=pd.read_csv(CACHE/"human_libraries.tsv",sep="\t").library.tolist()
    matrix=np.memmap(CACHE/"human_counts.bin",dtype="<i4",mode="r",shape=(len(genes),len(libraries)))
    # Exact S5 stable IDs: RGS5 also labels an antisense feature in the counts.
    selected=genes[genes.ID.isin(["ENSG00000143248","ENSG00000169429","ENSG00000147872"])]
    wanted={row.ID:(int(index),row.symbol) for index,row in selected.iterrows()}
    assert len(wanted)==3
    seen=[]; header_map=None
    with zipfile.ZipFile(ROOT/"raw_data/GSE307112/GSE307112_gene_counts.xlsx") as archive, archive.open("xl/worksheets/sheet2.xml") as handle:
        for _,element in ET.iterparse(handle,events=("end",)):
            if element.tag!=NS+"row": continue
            cells={re.sub(r"\d","",c.attrib["r"]):cell_value(c) for c in element}
            if header_map is None:
                header_map={name:column for column,name in cells.items()}
            else:
                identifier=cells.get(header_map["ID"])
                if identifier in wanted:
                    index,symbol=wanted[identifier]
                    values=np.array([int(float(cells.get(header_map[library],0) or 0)) for library in libraries],dtype="<i4")
                    assert np.array_equal(values,matrix[index]),f"Independent XML count check failed: {identifier}"
                    assert cells[header_map["symbol"]]==symbol
                    seen.append(dict(gene=identifier,symbol=symbol,libraries_checked=len(libraries),counts_and_symbol_match=True))
            element.clear()
            if len(seen)==len(wanted): break
    assert len(seen)==3
    OUT.mkdir()
    pd.DataFrame(summaries).to_csv(OUT/"source_internal_consistency.tsv",sep="\t",index=False)
    pd.DataFrame(examples).to_csv(OUT/"source_direction_conflicts.tsv",sep="\t",index=False)
    pd.DataFrame(swaps).to_csv(OUT/"target_swap_diagnostic.tsv",sep="\t",index=False)
    pd.DataFrame(summary_signs.values()).to_csv(OUT/"source_summary_vs_reconstructed_signs.tsv",sep="\t",index=False)
    pd.DataFrame(seen).to_csv(OUT/"independent_count_checks.tsv",sep="\t",index=False)
    record={"analysis_id":"Nb3_R2","timing":"Post-hoc audit triggered by near-zero labeled S5 concordance; not a new biological endpoint",
      "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "source_summary":summaries,"independent_count_entries_checked":sum(x["libraries_checked"] for x in seen),
      "implementation_history":"Initial count spot-check selection stopped before writing outputs because RGS5 also labels an antisense feature; corrected to the three exact S5 stable IDs, without altering extraction or any endpoint",
      "interpretation":"Retain original labels and both results. Internal source-table conflicts do not establish how the source table was produced; request source mapping/code before treating human DE as reproduced.",
      "relabeling_or_endpoint_refitting":False}
    record["output_sha256"]={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob("*.tsv")}
    (OUT/"run_record.json").write_text(json.dumps(record,indent=2)+"\n")
    print("Independent human XML count rows matched; source labels remain unchanged",flush=True)

if __name__=="__main__": main()
