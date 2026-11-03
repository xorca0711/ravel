"""Original A12 index components plus five fixed IL-1-context transcripts."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd

OLD = Path("docs/roadmap_runs/2026-09-27-followthrough")
META = Path("Research Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_niche/unc20_pooled_units.csv")
RAW = Path("raw_data/A12_COMPONENTS_v1/unc20_pooled_triad_counts.csv.gz")
GENES = ["IL1R1","IL1RAP","IL1R2","IL1RN","SIGIRR","MYD88","IRAK1","IRAK4","NFKBIA","TNFAIP3"]
WEIGHTS = dict(zip(GENES,[.5,.5,-1/3,-1/3,-1/3,0,0,0,0,0]))


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True)
    out=Path(parser.parse_args().output);out.mkdir(parents=True,exist_ok=True)
    original=pd.read_csv(OLD/"A12_model_inputs.csv",dtype={"patient":str})
    original=original[original.uncertainty.eq(.2)&original.cell_floor.eq(50)].copy()
    if len(original)!=24 or original.duplicated(["patient","recipient"]).any():raise ValueError("Primary roster conflict")
    groups=original.groupby("recipient").patient.apply(set)
    if set(groups.index)!={"AT2","Alveolar fibroblasts"} or len(groups.iloc[0])!=12 or groups.iloc[0]!=groups.iloc[1]:raise ValueError("Patient cohort conflict")
    units=sorted(set(original.recipient_normal_unit)|set(original.recipient_LUAD_unit))
    if len(units)!=48:raise ValueError("Original unit ID conflict")
    meta=pd.read_csv(META,dtype={"patient":str}).set_index("unit_id",drop=False)
    if not meta.index.is_unique:raise ValueError("Duplicated metadata IDs")
    meta=meta.loc[units].copy()
    if not meta.cells.ge(50).all():raise ValueError("Original support failure")
    sums=np.zeros(len(units),dtype=np.int64);parts=[];seen=set()
    for chunk in pd.read_csv(RAW,usecols=["gene"]+units,chunksize=500):
        names=chunk.gene.tolist()
        if len(set(names))!=len(names) or seen.intersection(names):raise ValueError("Duplicated source genes")
        seen.update(names);values=chunk[units].to_numpy()
        if not (np.isfinite(values).all() and (values>=0).all() and (values==np.floor(values)).all()):raise ValueError("Invalid unit counts")
        sums+=values.sum(axis=0,dtype=np.int64)
        parts.append(chunk[chunk.gene.isin(GENES)].set_index("gene")[units])
    if not np.array_equal(sums,meta.full_library_sum.to_numpy()) or (sums<=0).any():raise ValueError("Full-library parity failure")
    counts=pd.concat(parts).loc[GENES]
    if not counts.index.is_unique or len(counts)!=10:raise ValueError("Target feature conflict")
    logs=np.log2(1+counts.div(meta.full_library_sum,axis="columns")*1e6)
    response=set(json.loads((OLD/"A12_pilot_specification.json").read_text())["response"]["genes"])
    if set(GENES)&response!={"NFKBIA","TNFAIP3"}:raise ValueError("Original response overlap changed")
    primitives=[];scalar_errors=[]
    for unit in units:
        m=meta.loc[unit]
        for gene in GENES:
            value=float(logs.loc[gene,unit]);raw=int(counts.loc[gene,unit]);total=int(m.full_library_sum)
            error=abs(value-math.log2(1+raw/total*1e6));scalar_errors.append(error)
            if error>1e-10:raise ValueError("Independent log-CPM parity failure")
            primitives.append(dict(unit_id=unit,patient=m.patient,recipient=m.label,histology=m.histology,n_cells=int(m.cells),full_library_sum=total,gene=gene,gene_count=raw,log2_1_plus_cpm=value,index_weight=WEIGHTS[gene],weighted_contribution=value*WEIGHTS[gene],overlaps_old_response=gene in response))
    pd.DataFrame(primitives).to_csv(out/"unit_gene_primitives.tsv",sep="\t",index=False)
    paired=[];parity=[]
    for row in original.sort_values(["recipient","patient"]).itertuples(index=False):
        normal,luad=row.recipient_normal_unit,row.recipient_LUAD_unit
        for unit,hist in [(normal,"normal"),(luad,"LUAD")]:
            m=meta.loc[unit]
            if (m.patient,m.label,m.histology)!=(row.patient,row.recipient,hist):raise ValueError("Unit/patient/recipient mapping conflict")
        total_delta=0.0
        for gene in GENES:
            nv,lv=float(logs.loc[gene,normal]),float(logs.loc[gene,luad]);delta=lv-nv
            total_delta+=WEIGHTS[gene]*delta
            paired.append(dict(patient=row.patient,recipient=row.recipient,gene=gene,normal_unit=normal,LUAD_unit=luad,source_normal_unit=row.source_normal_unit,source_LUAD_unit=row.source_LUAD_unit,normal_log2cpm=nv,LUAD_log2cpm=lv,delta_log2cpm=delta,index_weight=WEIGHTS[gene],weighted_delta=WEIGHTS[gene]*delta,overlaps_old_response=gene in response))
        error=abs(total_delta-row.recipient_index)
        if error>1e-10:raise ValueError("Original index reconstruction failure")
        parity.append(dict(patient=row.patient,recipient=row.recipient,original_index_delta=row.recipient_index,reconstructed_index_delta=total_delta,absolute_error=error))
    paired=pd.DataFrame(paired);paired.to_csv(out/"paired_gene_components.tsv",sep="\t",index=False)
    pd.DataFrame(parity).to_csv(out/"original_index_parity.tsv",sep="\t",index=False)
    summaries=[]
    for recipient in ["AT2","Alveolar fibroblasts"]:
        for gene in GENES:
            group=paired[paired.recipient.eq(recipient)&paired.gene.eq(gene)]
            if len(group)!=12:raise ValueError("Incomplete paired summary")
            summaries.append(dict(recipient=recipient,gene=gene,n_patients=12,mean_paired_delta_log2cpm=float(group.delta_log2cpm.mean()),mean_index_contribution=float(group.weighted_delta.mean()),overlaps_old_response=gene in response))
    pd.DataFrame(summaries).to_csv(out/"component_summary.tsv",sep="\t",index=False)
    result=dict(ok=True,patients=12,patient_recipient_pairs=24,recipient_units=len(units),genes=10,primitive_rows=len(primitives),paired_rows=len(paired),full_library_checks=len(units),scalar_log_checks=len(scalar_errors),max_scalar_log_error=max(scalar_errors),original_index_checks=len(parity),max_index_error=max(r["absolute_error"] for r in parity),response_overlap=sorted(set(GENES)&response),limit="Original candidate labels and unfavorable fibroblast prediction retained; no new index, refit, response correlation, causal specificity or protein activity claim.")
    (out/"verification.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8");print(json.dumps(result))


if __name__=="__main__":main()
