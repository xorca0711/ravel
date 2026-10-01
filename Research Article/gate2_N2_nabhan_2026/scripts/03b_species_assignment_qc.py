"""Audit deposited Xenome partitions without inferring unrecorded host/graft species."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parents[1]

def main():
    dest=HERE/"runs/R2_v1/xenome_QC.tsv"
    if dest.exists(): raise SystemExit("Refusing to overwrite Xenome audit")
    source=ROOT/"raw_data/GSE307112/GSE307112_xenome_stats.csv.gz"
    source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
    assert source_sha=="045b9da623db54a59948f1e8e6b68c1587fa4786a6838a51a890dfe59064edf5"
    x=pd.read_csv(source).rename(columns={"library name":"library","crispr_target":"target"})
    x.target=x.target.str.upper()
    assert len(x)==886 and x.library.is_unique
    columns=[f"xenome_numReads{k}" for k in ("Graft","Host","Ambiguous","Both","Neither")]
    assert (x[columns]>=0).all().all() and (x[columns].sum(axis=1)==x.xenome_numReadsInput).all()
    crosswalk=pd.read_csv(ROOT/"raw_data/GSE307112/Nb3_v1/crosswalk.tsv",sep="\t")
    joined=x.merge(crosswalk[["library","target","plate"]],on="library",validate="one_to_one",suffixes=("","_crosswalk"))
    assert len(joined)==886 and (joined.target==joined.target_crosswalk).all() and (joined.plate==joined.plate_crosswalk).all()
    for category in ("Graft","Host","Ambiguous","Both","Neither"):
        x[f"fraction_{category.lower()}"]=x[f"xenome_numReads{category}"]/x.xenome_numReadsInput
    x["fraction_unambiguous"]=x.fraction_graft+x.fraction_host
    output=x[["library","target","plate"]+[c for c in x if c.startswith("fraction_")]]
    output.to_csv(dest,sep="\t",index=False)
    record={"analysis_id":"Nb3_R2","source_sha256":source_sha,"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "all_886_partitions_sum_to_input":True,"all_library_target_plate_joins_exact":True,
      "fraction_quantiles":output.select_dtypes(include="number").quantile([0,.25,.5,.75,1]).to_dict(),
      "scope":"QC diagnostics only; no additional exclusions applied after outcome inspection",
      "host_graft_species":"Retain deposited labels; do not equate them with a species without explicit source mapping"}
    (dest.parent/"xenome_QC_record.json").write_text(json.dumps(record,indent=2)+"\n")
    print(output.select_dtypes(include="number").median().round(3).to_json())

if __name__=="__main__": main()
