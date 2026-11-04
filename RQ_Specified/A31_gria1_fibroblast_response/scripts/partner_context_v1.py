"""Nine prespecified A31 partner-context transcripts, original source strata."""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
import pandas as pd

GENES=["GRIA1","GRIA2","GRIA3","GRIA4","CNIH2","CNIH3","CACNG2","CACNG3","CACNG8"]
LABELS=["Alveolar Fibroblast","Adventitial Fibroblast","Schwann_nonmyelinating","Schwann_Myelinating","NAF_endoneurial","NAF_epineurial"]
KEYS=["cohort","assay","donor","region","protocol","cell_type"]
CACHE=Path("raw_data/travaglini_nabhan_2020")
LEGACY=Path("analysis/portfolio_extensions/2026-10-07/g2_niche/sensory_v1.py")
OLD=Path("analysis/research/runs/nb4_p09_expression_specificity_v1_20261007")


def cells():
    spec=importlib.util.spec_from_file_location("a31_legacy_reader",LEGACY)
    reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    # Reuse only the hash-bound read-only reader, never its historical main/output path.
    reader.GENES=GENES
    meta=pd.read_csv(CACHE/"prepared/cell_metadata.tsv",sep="\t")
    parts=[]
    for assay,name in reader.FILES:
        ids,values,totals,obs,mapping=reader.read_counts(CACHE/name)
        if assay!="Madissoon":
            m=meta[meta.assay.eq(assay)].reset_index(drop=True)
            if list(m.cell_id)!=list(ids):raise ValueError("Source order mismatch")
            data=pd.DataFrame(dict(cell=ids,cohort="Travaglini",assay=assay,donor=m.donor_id,region=m.anatomical_region,protocol=assay,cell_type=m.author_cell_type))
            keep=m.tissue.eq("lung").to_numpy()
        else:
            data=pd.DataFrame(dict(cell=ids,cohort="Madissoon",assay=["Madissoon "+str(x) for x in obs["suspension_type"]],donor=obs["donor_id"],region=obs["Location_long"],protocol=[str(a)+"|"+str(b) for a,b in zip(obs["assay_ontology_term_id"],obs["Protocol_plot"])],cell_type=obs["Celltypes"]))
            keep=(np.asarray(obs["disease"])=="normal")&(np.asarray(obs["Location_long"])!="Mix")
            data.cell_type=data.cell_type.replace({"Fibro_alveolar":"Alveolar Fibroblast","Fibro_adventitial":"Adventitial Fibroblast"})
        data["library"]=totals
        for i,gene in enumerate(GENES):data[gene]=values[:,i]
        data["count_unit"]="reads" if assay=="SS2" else "UMIs" if assay=="10x" else "source_counts"
        parts.append(data[keep & data.cell_type.isin(LABELS)].copy())
    data=pd.concat(parts,ignore_index=True)
    if data[KEYS].isna().any().any() or data.duplicated(["cohort","assay","cell"]).any():raise ValueError("Missing/duplicate source identity")
    return data


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True)
    out=Path(parser.parse_args().output);out.mkdir(parents=True,exist_ok=True)
    data=cells();data.to_csv(out/"cell_partner_counts.tsv.gz",sep="\t",index=False,compression={"method":"gzip","mtime":0})
    gene_rows=[];joint_rows=[]
    for keys,group in data.groupby(KEYS,sort=True):
        common=dict(zip(KEYS,keys));total=int(group.library.sum());n=len(group)
        common.update(count_unit=group.count_unit.iloc[0])
        for gene in GENES:
            value=int(group[gene].sum());detected=int(group[gene].gt(0).sum())
            gene_rows.append(dict(common,gene=gene,n_cells=n,library=total,sum_count=value,n_detected=detected,fraction_detected=detected/n,log2cpm=float(np.log2(1+1e6*value/total))))
        ordered=group.sort_values(["library","cell"])
        for depth,block in [("all_depth",group),("low_half",ordered.iloc[:n//2]),("high_half",ordered.iloc[n//2:])]:
            if block.empty:continue
            a=block.GRIA1.gt(0)
            for partner in GENES[1:]:
                b=block[partner].gt(0);both=int((a&b).sum());nn=len(block);na=int(a.sum());nb=int(b.sum())
                if not max(0,na+nb-nn)<=both<=min(na,nb):raise ValueError("Co-detection set-bound failure")
                joint_rows.append(dict(common,depth=depth,partner=partner,n_cells=nn,library=int(block.library.sum()),n_gria1=na,n_partner=nb,n_both=both,fraction_both=both/nn,stratum_support_ge20=nn>=20))
    genes=pd.DataFrame(gene_rows);joint=pd.DataFrame(joint_rows)
    genes.to_csv(out/"stratum_gene.tsv",sep="\t",index=False);joint.to_csv(out/"partner_codetection.tsv",sep="\t",index=False)
    old=pd.read_csv(OLD/"stratum_gene.tsv",sep="\t",keep_default_na=False)
    old=old[old.sensitivity.eq("all")&old.depth.eq("all_depth")&old.gene.eq("GRIA1")&old.cell_type.isin(LABELS)]
    check=genes[genes.gene.eq("GRIA1")].merge(old,on=KEYS+["gene"],how="outer",suffixes=("_new","_old"),indicator=True,validate="one_to_one")
    if not check._merge.eq("both").all():raise ValueError("GRIA1 stratum roster conflict")
    errors=[]
    for name in ["n_cells","library","sum_count","n_detected","fraction_detected","log2cpm"]:
        error=float(np.abs(check[name+"_new"]-check[name+"_old"]).max());errors.append(error)
        if error>1e-10:raise ValueError("GRIA1 primitive/endpoint parity failure")
    check.to_csv(out/"gria1_stratum_parity.tsv",sep="\t",index=False)
    use=genes[((genes.cohort.eq("Travaglini"))&genes.region.eq("distal")) | (genes.cohort.eq("Madissoon")&genes.region.isin(["Lower Left Lobe","Upper left lobe"]))]
    use=use[use.cell_type.isin(LABELS[:2])];pairs=[]
    for keys,group in use.groupby(KEYS[:-1]+["gene"],sort=True):
        row=dict(zip(KEYS[:-1]+["gene"],keys));v=group.set_index("cell_type");a=LABELS[0];b=LABELS[1]
        na=int(v.loc[a,"n_cells"]) if a in v.index else 0;nb=int(v.loc[b,"n_cells"]) if b in v.index else 0
        eligible=na>=20 and nb>=20
        row.update(n_alveolar=na,n_adventitial=nb,eligible=eligible,status="estimated" if eligible else "unestimated_support",delta_log2cpm=float(v.loc[a,"log2cpm"]-v.loc[b,"log2cpm"]) if eligible else np.nan,delta_detection=float(v.loc[a,"fraction_detected"]-v.loc[b,"fraction_detected"]) if eligible else np.nan)
        pairs.append(row)
    pairs=pd.DataFrame(pairs);pairs.to_csv(out/"paired_strata.tsv",sep="\t",index=False)
    donor_keys=["cohort","assay","donor","gene"]
    donors=pairs[pairs.eligible].groupby(donor_keys,as_index=False).agg(delta_log2cpm=("delta_log2cpm","mean"),delta_detection=("delta_detection","mean"),n_strata=("eligible","size"))
    donors.to_csv(out/"donor_effects.tsv",sep="\t",index=False)
    olddonor=pd.read_csv(OLD/"donor_effects.tsv",sep="\t",keep_default_na=False)
    olddonor=olddonor[olddonor.sensitivity.eq("all")&olddonor.floor.eq(20)&olddonor.gene.eq("GRIA1")]
    parity=donors[donors.gene.eq("GRIA1")].merge(olddonor,on=donor_keys,how="outer",suffixes=("_new","_old"),indicator=True,validate="one_to_one")
    if not parity._merge.eq("both").all():raise ValueError("GRIA1 donor roster conflict")
    for name in ["delta_log2cpm","delta_detection","n_strata"]:
        error=float(abs(parity[name+"_new"]-parity[name+"_old"]).max());errors.append(error)
        if error>1e-10:raise ValueError("GRIA1 donor parity failure")
    parity.to_csv(out/"gria1_donor_parity.tsv",sep="\t",index=False)
    result=dict(ok=True,genes=GENES,cells=len(data),strata=len(check),gene_rows=len(genes),joint_rows=len(joint),attempted_pairs=len(pairs),estimated_pairs=int(pairs.eligible.sum()),unestimated_pairs=int((~pairs.eligible).sum()),donor_gene_rows=len(donors),gria1_donor_rows=len(parity),max_gria1_parity_error=max(errors),limit="Nine-gene sentinel RNA only; SS2 reads differ from UMIs; depth halves are within-stratum relative-depth sensitivity, not cross-label depth matching; source/assay donors overlap.")
    (out/"verification.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8");print(json.dumps(result))


if __name__=="__main__":main()
