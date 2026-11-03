"""Fixed six-gene A9 recipient context; original donor and subtype gates."""
import argparse,json,math
from pathlib import Path
import anndata as ad
import h5py
import numpy as np
import pandas as pd
from scipy import sparse

GENES=["EGFR","ERBB2","ERBB3","ERBB4","ERRFI1","LRIG1"]
LABELS=["Fibroblast","Myofibroblast"]
PRE=Path("docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A9_INPUT_MAP_V1.json")


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);out=Path(ap.parse_args().output);out.mkdir(parents=True,exist_ok=True)
    spec=json.loads(PRE.read_text());donors=spec["donors"]
    with h5py.File(spec["path"],"r") as h:
        obs=ad.io.read_elem(h["obs"]);names=h["var/_index"].asstr()[:]
        positions=[np.flatnonzero(names==g) for g in GENES]
        if any(len(x)!=1 for x in positions):raise ValueError("Target mapping changed")
        positions=[int(x[0]) for x in positions]
        if {g:[i] for g,i in zip(GENES,positions)}!=spec["feature_map"]:raise ValueError("Feature-index map changed")
        if not obs.index.is_unique:raise ValueError("Duplicate cell IDs")
        eligible=[]
        for donor,group in obs.groupby("donor",observed=True):
            if group.category.eq("Epithelial").sum()>=50 and group.celltype.isin(LABELS).sum()>=50:eligible.append(str(donor))
        if set(eligible)!=set(donors) or len(donors)!=22:raise ValueError("Original donor roster changed")
        m=h["X"];shape=tuple(m.attrs["shape"])
        if m.attrs["encoding-type"]!="csr_matrix" or list(shape)!=spec["shape"]:raise ValueError("Source layer/shape changed")
        counts=np.zeros((len(obs),6),dtype=np.int64);totals=np.zeros(len(obs),dtype=np.int64)
        for start in range(0,len(obs),1000):
            end=min(start+1000,len(obs));ptr=m["indptr"][start:end+1];lo,hi=int(ptr[0]),int(ptr[-1]);values=m["data"][lo:hi]
            if not (np.isfinite(values).all() and (values>=0).all() and (values==np.floor(values)).all()):raise ValueError("Source is not integer counts")
            block=sparse.csr_matrix((values.astype(np.int64),m["indices"][lo:hi],ptr-ptr[0]),shape=(end-start,len(names)))
            totals[start:end]=np.asarray(block.sum(axis=1)).ravel();counts[start:end]=block[:,positions].toarray()
    keep=obs.donor.isin(donors)&obs.celltype.isin(LABELS);idx=np.flatnonzero(keep.to_numpy())
    frame=obs.loc[keep,["donor","disease","celltype"]].copy().rename(columns={"celltype":"recipient"});frame.insert(0,"cell",frame.index.astype(str));frame["library"]=totals[idx]
    if not frame.library.gt(0).all():raise ValueError("Zero source library")
    scalar_error=0.0;scalar_checks=0
    for j,g in enumerate(GENES):
        frame[g]=counts[idx,j];v=np.log1p(1e4*frame[g].to_numpy()/frame.library.to_numpy());frame[g+"_log1p_cp10k"]=v
        expected=np.asarray([math.log1p(1e4*int(k)/int(n)) for k,n in zip(frame[g],frame.library)])
        error=float(np.max(abs(v-expected)));scalar_error=max(scalar_error,error);scalar_checks+=len(v)
        if error>1e-10:raise ValueError("Cell-log scalar parity failed")
    frame.to_csv(out/"cell_receptor_primitives.tsv.gz",sep="\t",index=False,compression={"method":"gzip","mtime":0})
    support=[];rows=[];joint=[]
    for donor in donors:
        for label in LABELS:
            b=frame[frame.donor.eq(donor)&frame.recipient.eq(label)];n=len(b);ok=n>=10
            expected=next(r for r in spec["recipient_support"] if r["donor"]==donor and r["recipient"]==label)
            if n!=expected["n_cells"] or ok!=expected["eligible_subtype"]:raise ValueError("Original subtype support changed")
            support.append(dict(donor=donor,recipient=label,n_cells=n,eligible=ok))
            for g in GENES:
                rows.append(dict(donor=donor,recipient=label,gene=g,n_cells=n,eligible=ok,full_library_sum=int(b.library.sum()),sum_count=int(b[g].sum()),n_detected=int(b[g].gt(0).sum()),fraction_detected=float(b[g].gt(0).mean()) if ok else np.nan,mean_log1p_cp10k=float(b[g+"_log1p_cp10k"].mean()) if ok else np.nan))
            na=int(b.EGFR.gt(0).sum());nb=int(b.ERBB2.gt(0).sum());both=int((b.EGFR.gt(0)&b.ERBB2.gt(0)).sum())
            if not max(0,na+nb-n)<=both<=min(na,nb):raise ValueError("Co-detection set-bound failure")
            joint.append(dict(donor=donor,recipient=label,n_cells=n,eligible=ok,n_egfr=na,n_erbb2=nb,n_both=both,fraction_both=both/n if ok else np.nan))
    pd.DataFrame(support).to_csv(out/"recipient_support.tsv",sep="\t",index=False)
    rows=pd.DataFrame(rows);rows.to_csv(out/"recipient_gene_profiles.tsv",sep="\t",index=False);pd.DataFrame(joint).to_csv(out/"egfr_erbb2_codetection.tsv",sep="\t",index=False)
    pairs=[]
    for donor in donors:
        for gene in GENES:
            b=rows[rows.donor.eq(donor)&rows.gene.eq(gene)].set_index("recipient");ok=bool(b.eligible.all())
            pairs.append(dict(donor=donor,gene=gene,eligible=ok,status="estimated" if ok else "unestimated_subtype_support",delta_mean_log1p_cp10k=float(b.loc[LABELS[1],"mean_log1p_cp10k"]-b.loc[LABELS[0],"mean_log1p_cp10k"]) if ok else np.nan,delta_detection=float(b.loc[LABELS[1],"fraction_detected"]-b.loc[LABELS[0],"fraction_detected"]) if ok else np.nan))
    pairs=pd.DataFrame(pairs);pairs.to_csv(out/"within_donor_recipient_pairs.tsv",sep="\t",index=False)
    result=dict(ok=True,donors=22,recipient_rows=44,eligible_recipients=sum(x["eligible"] for x in support),cells=len(frame),genes=GENES,scalar_log_checks=scalar_checks,max_scalar_log_error=scalar_error,attempted_gene_pairs=len(pairs),estimated_gene_pairs=int(pairs.eligible.sum()),unestimated_gene_pairs=int((~pairs.eligible).sum()),limit="Mean cell-logCP10k receptor/context RNA; old7/22complex failure unchanged; ERBB3/4 family context not directAREG receptors; feedbackRNA not effective inhibition.")
    (out/"verification.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8");print(json.dumps(result))


if __name__=="__main__":main()
