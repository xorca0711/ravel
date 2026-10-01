"""Verify archived extension evidence without scientific dependencies; optional raw checks."""
import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
A22=ROOT/"RQ_Specified/A22_epithelial_identity_niche_response"
A23=ROOT/"RQ_Specified/A23_slc34a2_transition_homeostasis"


def rows(p):
    with p.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))


def near(a,b):
    if not math.isclose(float(a),float(b),rel_tol=1e-8,abs_tol=1e-9):
        raise AssertionError((a,b))


def verify(with_raw=False):
    checked={}
    for q,run in [(A22,"identity_amount_v1"),(A22,"identity_amount_v2"),(A23,"transporter_context_v1")]:
        folder=q/"metadata"/run
        records=[folder/"run_record.json"]
        records.extend(sorted(folder.glob("figure_record*.json")))
        for record in records:
            rec=json.loads(record.read_text())
            for r in rec["inputs"]+rec["outputs"]:
                if r["path"].startswith("raw_data/") and not with_raw:continue
                if r["path"] not in checked:
                    h=hashlib.sha256()
                    with (ROOT/r["path"]).open("rb") as f:
                        for b in iter(lambda:f.read(1048576),b""):h.update(b)
                    checked[r["path"]]=h.hexdigest()
                if checked[r["path"]]!=r["sha256"]:raise AssertionError("Changed "+r["path"])
    tab=A22/"tables/identity_amount_v2"
    members=rows(tab/"fold_membership.tsv"); folds=defaultdict(list)
    for r in members:folds[(r["variant"],r["mode"],r["fold"])].append(r)
    assignments={}
    for (variant,mode,fold),rr in folds.items():
        train={r["target"] for r in rr if r["role"]=="train"};test={r["target"] for r in rr if r["role"]=="test"}
        assert not train & test
        assert not ({"TIGIT","TDTOMATO"} & (train|test))
        if mode=="plate_shift":
            assert not {r["plate"] for r in rr if r["role"]=="train"} & {r["plate"] for r in rr if r["role"]=="test"}
        else:
            for target in test:
                if target in assignments:assert assignments[target]==fold
                assignments[target]=fold
    pred=rows(tab/"predictions.tsv"); seen=set(); groups=defaultdict(list)
    for r in pred:
        key=tuple(r[k] for k in ["variant","mode","endpoint","library"])
        assert key not in seen;seen.add(key)
        groups[key[:3]].append(r)
        memberships=folds[(r["variant"],r["mode"],r["fold"])]
        assert any(m["library"]==r["library"] and m["role"]=="test" for m in memberships)
    for r in rows(tab/"metrics.tsv"):
        rr=groups[tuple(r[k] for k in ["variant","mode","endpoint"])]
        if r["fold"]!="pooled":rr=[v for v in rr if v["fold"]==r["fold"]]
        assert len(rr)==int(r["wells"])
        bytarget=defaultdict(list)
        for v in rr:bytarget[v["target"]].append(v)
        assert len(bytarget)==int(r["targets"])
        mse={}
        for model,prefix in [("baseline","baseline"),("plus_identity","full")]:
            err=lambda v:(float(v["observed"])-float(v[model]))**2
            mse[prefix]=sum(sum(map(err,tt))/len(tt) for tt in bytarget.values())/len(bytarget)
            near(r[prefix+"_target_mse"],mse[prefix]);near(r[prefix+"_target_rmse"],math.sqrt(mse[prefix]))
            near(r[prefix+"_well_mse"],sum(map(err,rr))/len(rr))
        near(r["relative_target_mse_reduction"],1-mse["full"]/mse["baseline"])
    tab3=A23/"tables/transporter_context_v1";summ=rows(tab3/"summaries.tsv")
    lookup={(r["library"],r["group"],r["gene"]):r for r in summ}
    for r in summ:
        if r["status"]=="available":near(r["fraction_detected"],int(r["n_detected"])/int(r["n"]))
    for r in rows(tab3/"differences.tsv"):
        if r["status"]!="descriptive":continue
        a=lookup[("GSM5970468",r["group"],r["gene"])];b=lookup[("GSM5970470",r["group"],r["gene"])]
        near(r["mean_log1p_difference"],float(a["mean_log1p_10k"])-float(b["mean_log1p_10k"]))
        near(r["detection_percentage_point_difference"],100*(float(a["fraction_detected"])-float(b["fraction_detected"])))
        near(r["sum_count_cpm_difference"],float(a["sum_count_cpm"])-float(b["sum_count_cpm"]))
    for r in rows(A23/"tables/published_cell_audit_v1/marker_summaries.tsv"):
        key=(r["library"],r["group"],r["gene"])
        if key in lookup:
            for col in ["n","n_detected","mean_log1p_10k"]:near(r[col],lookup[key][col])
    assoc=rows(tab3/"associations.tsv")
    for r in assoc:
        eligible=int(r["n"])>=50 and min(int(r["transporter_detected"]),int(r["marker_detected"]))>=max(20,.05*int(r["n"]))
        assert (r["status"]=="descriptive")==eligible
        if eligible:
            for col in ["spearman","partial_rank","x_depth","y_depth","x_ngenes","y_ngenes"]:assert -1<=float(r[col])<=1
    if with_raw:verify_raw(lookup,assoc,groups)
    print("Extension verification PASS: receipts, fixed folds, no target leakage, error arithmetic, selection recovery and coverage gates"+("; independent model and raw-marker calculations" if with_raw else " (tracked inputs only)"))


def verify_raw(lookup,assoc,pred_groups):
    import h5py
    import numpy as np
    from scipy.sparse import csc_matrix
    from scipy.stats import spearmanr,rankdata
    # Independent unstandardized weighted least-squares reconstruction of one held-out fold.
    joined=rows(A22/"tables/identity_amount_v2/joined_wells.tsv")
    members=rows(A22/"tables/identity_amount_v2/fold_membership.tsv")
    mm={r["library"]:r["role"] for r in members if (r["variant"],r["mode"],r["fold"])==("primary","target_holdout","1")}
    train=[r for r in joined if mm[r["library"]]=="train"];test=[r for r in joined if mm[r["library"]]=="test"]
    counts={t:sum(r["target"]==t for r in train) for t in {r["target"] for r in train}}
    def design(rr,full):
        return np.array([[1,float(r["area07"]),float(r["area14"]),math.log1p(float(r["count07"])),math.log1p(float(r["count14"])),float(r["prop07"]),float(r["prop14"]),math.log2(float(r["mouse_reads"])),math.log2(float(r["human_reads"])),*[float(r["plate"]==p) for p in ["plate2","plate3","plate4"]],*([float(r["identity"])] if full else [])] for r in rr])
    w=np.array([counts[r["target"]]**-.5 for r in train]);y=np.array([float(r["chemokines_figure4"]) for r in train])
    saved={r["library"]:r for r in pred_groups[("primary","target_holdout","chemokines_figure4")]}
    for full,col in [(False,"baseline"),(True,"plus_identity")]:
        coef=np.linalg.pinv(design(train,full)*w[:,None])@(y*w)
        for r,value in zip(test,design(test,full)@coef):near(saved[r["library"]][col],value)
    # Read raw CSC columns by archived primary candidate barcode, independently of the generator's union/CSR reader.
    selections=rows(A23/"tables/external_pilot_v2/cell_selection.tsv")
    matrices=json.loads((A23/"metadata/external_acquisition_v1/raw_matrices.json").read_text())
    for rec in matrices:
        lib=rec["library"]
        if lib=="GSM5970469":continue
        selected={r["barcode"]:r for r in selections if r["library"]==lib and r["qc"]=="primary" and r["AT2_candidate"]=="True"}
        with h5py.File(ROOT/rec["path"],"r") as f:
            g=f["hg19"];names=[v.decode() for v in g["gene_names"][:]];barcodes=[v.decode() for v in g["barcodes"][:]]
            mat=csc_matrix((g["data"][:],g["indices"][:],g["indptr"][:]),shape=tuple(g["shape"][:]))
        jj=[j for j,b in enumerate(barcodes) if b in selected];sub=mat[:,jj]
        total=np.asarray(sub.sum(axis=0)).ravel();ng=np.asarray((sub>0).sum(axis=0)).ravel()
        normalized={}
        for gene in ["SLC20A1","SLC20A2","SLC34A2","KRT8","SPRR1A","CLU"]:
            v=sub[names.index(gene)].toarray().ravel();s=lookup[(lib,"AT2_candidate_primary",gene)]
            terms=[math.log1p(float(a)*10000/float(b)) for a,b in zip(v,total)];normalized[gene]=np.array(terms)
            near(s["mean_log1p_10k"],sum(terms)/len(terms));near(s["sum_count_cpm"],sum(v)*1e6/sum(total));assert int(s["n_detected"])==sum(a>0 for a in v)
        cov=np.column_stack([np.ones(len(total)),rankdata(total),rankdata(ng)])
        proj=np.eye(len(total))-cov@np.linalg.pinv(cov)
        for r in assoc:
            if (r["library"],r["group"],r["status"])!=(lib,"AT2_candidate_primary","descriptive"):continue
            a=normalized[r["transporter"]];b=normalized[r["state_marker"]]
            near(r["spearman"],spearmanr(a,b).statistic)
            near(r["partial_rank"],np.corrcoef(proj@rankdata(a),proj@rankdata(b))[0,1])


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--with-raw",action="store_true");verify(p.parse_args().with_raw)
