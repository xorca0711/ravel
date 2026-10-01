"""Recover fixed marker rows from both deposited S3 budding comparisons."""
from pathlib import Path
import hashlib
import json
import csv
import openpyxl

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parents[1]

def main():
    out=HERE/"runs/R3_v1/source_budding_markers.tsv"
    if out.exists(): raise SystemExit("Refusing to overwrite source budding reconstruction")
    source=ROOT/"raw_data/nabhan_2026_sources/pnas.2606113123.sd03.xlsx"
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest=="90eeb3c416a68049b90ca7fd1e54c3893f3fdf103c089a5317024f57aaf76397"
    spec=json.loads((HERE/"config/Nb3_execution_v1.json").read_text())
    spec["programs"]["mouse"].update(json.loads((HERE/"config/Nb3_panel_amendment_v1.json").read_text())["replace_programs_mouse"])
    membership={}
    for program,genes in spec["programs"]["mouse"].items():
        for gene in genes: membership.setdefault(gene,[]).append(program)
    wb=openpyxl.load_workbook(source,read_only=True,data_only=True)
    selected=[]; dimensions=[]
    for sheet in wb:
        rows=sheet.iter_rows(values_only=True); header=list(next(rows))
        keep=["ID","symbol","logFC","AveExpr","t","P.Value","adj.P.Val"]
        indices={key:header.index(key) for key in keep}
        count=0; seen=set()
        for row in rows:
            if not any(row): continue
            identifier=row[indices["ID"]]
            assert identifier and identifier not in seen
            seen.add(identifier); count+=1
            if row[indices["symbol"]] in membership:
                result={key:row[index] for key,index in indices.items()}
                result.update(comparison=sheet.title,programs=";".join(membership[result["symbol"]]))
                selected.append(result)
        dimensions.append({"comparison":sheet.title,"source_gene_rows":count})
    wb.close()
    with out.open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=["comparison","programs"]+keep,delimiter="\t")
        writer.writeheader(); writer.writerows(selected)
    record={"analysis_id":"Nb3_R3","source_sha256":digest,"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       "source_dimensions":dimensions,"selected_marker_rows":len(selected),
       "interpretation":"Published S3 contrasts and statistics, not newly fitted budding labels or independent marker validation",
       "unavailable":"Original image embeddings and exact source morphology assignments are not reconstructed"}
    (out.parent/"source_budding_record.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps({"source_dimensions":dimensions,"selected_marker_rows":len(selected)}))

if __name__=="__main__": main()
