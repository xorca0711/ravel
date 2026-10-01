"""Resolve target labels to S2 gene IDs using plate/position, without exporting guide sequences."""
from pathlib import Path
import hashlib
import json
import re
import pandas as pd
import openpyxl

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parents[1]

def main():
    out=HERE/"runs/00_v1"
    if out.exists(): raise SystemExit("Refusing to overwrite target identity audit")
    source=ROOT/"raw_data/nabhan_2026_sources/pnas.2606113123.sd02.xlsx"
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest=="59b69b5db53139f9b75183b91739e7b22d3666ac1df728028461548bd0ff399e"
    wb=openpyxl.load_workbook(source,read_only=True,data_only=True)
    rows=[]
    for sheet in wb:
        iterator=sheet.iter_rows(values_only=True); next(iterator)
        for row in iterator:
            if not any(row): continue
            if len(row)<4: raise ValueError("Nonblank source row has fewer than four identity fields")
            position,name,species,gene=row[:4]
            if not position or not name: continue
            match=re.fullmatch(r"([A-Z])(\d+)",str(position))
            if not match: raise ValueError(f"Unexpected position {position}")
            rows.append(dict(plate=sheet.title,position=f"{match[1]}{int(match[2]):02d}",source_gene_name=name,source_species=species,source_gene_id=gene))
    wb.close()
    design=pd.DataFrame(rows)
    assert not design.duplicated(["plate","position"]).any()
    crosswalk=pd.read_csv(ROOT/"raw_data/GSE307112/Nb3_v1/crosswalk.tsv",sep="\t")
    joined=crosswalk[["library","target","plate","position"]].merge(design,on=["plate","position"],how="left",validate="many_to_one")
    normalized=lambda s: re.sub(r"[^A-Z0-9]","",str(s).upper())
    mapped=joined.source_gene_id.notna()
    assert (joined.loc[mapped,"target"].map(normalized)==joined.loc[mapped,"source_gene_name"].map(normalized)).all()
    assert set(joined.loc[~mapped,"target"])=={"TDTOMATO"}
    features=pd.read_csv(ROOT/"raw_data/GSE307112/Nb3_v1/mouse_genes.tsv",sep="\t").rename(columns={"ID":"source_gene_id","symbol":"count_gene_symbol","type":"count_gene_type"})
    joined=joined.merge(features,on="source_gene_id",how="left",validate="many_to_one")
    assert joined.loc[mapped,"count_gene_symbol"].notna().all()
    joined["interpretation"]=joined.target.map(lambda t:"source activating edit; not a simple knockout" if t=="CTNNB1" else ("reference label; no S2 guide row" if t=="TDTOMATO" else "source target label; RNA is not protein-editing validation"))
    out.mkdir()
    joined.to_csv(out/"library_target_identity.tsv",sep="\t",index=False)
    joined.drop(columns="library").drop_duplicates().to_csv(out/"target_identity.tsv",sep="\t",index=False)
    record={"analysis_id":"Nb3_00","source_sha256":digest,"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "libraries":len(joined),"mapped_libraries":int(mapped.sum()),"missing_design_libraries":int((~mapped).sum()),
      "target_labels":joined.target.nunique(),"unique_target_gene_pairs":len(joined[["target","source_gene_id"]].drop_duplicates()),
      "all_mapped_labels_agree_after_punctuation_normalization":True,"all_mapped_mouse_gene_IDs_present":True,
      "implementation_history":"Initial parse stopped before writing outputs on empty trailing Excel rows; corrected to skip completely blank rows only"}
    (out/"run_record.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps(record))

if __name__=="__main__": main()
