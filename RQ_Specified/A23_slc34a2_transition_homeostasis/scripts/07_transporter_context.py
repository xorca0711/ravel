"""Descriptive human transporter RNA context; never a compensatory flux test."""
import csv
import datetime
import hashlib
import json
import platform
from pathlib import Path
import h5py
import numpy as np
import scipy
from scipy.sparse import csc_matrix
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[3]
RQ = ROOT / "RQ_Specified/A23_slc34a2_transition_homeostasis"
RUN = "transporter_context_v1"


def digest(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1048576), b""):
            h.update(b)
    return h.hexdigest()


def rows(p):
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write(p, rr):
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rr[0]), delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(rr)


def correlation(x, y):
    if np.std(x) < 1e-12 or np.std(y) < 1e-12:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def rank_association(x, y, total, ngenes):
    a, b = rankdata(x), rankdata(y)
    c = np.column_stack([np.ones(len(a)), rankdata(total), rankdata(ngenes)])
    residual = lambda v: v - c @ np.linalg.lstsq(c, v, rcond=None)[0]
    return dict(spearman=correlation(a, b), partial_rank=correlation(residual(a), residual(b)), x_depth=correlation(a, rankdata(total)), y_depth=correlation(b, rankdata(total)), x_ngenes=correlation(a, rankdata(ngenes)), y_ngenes=correlation(b, rankdata(ngenes)))


def run():
    contract = RQ / "config/transporter_context_v1.json"
    cfg = json.loads(contract.read_text())
    for r in cfg["inputs"]:
        if digest(ROOT/r["path"]) != r["sha256"]:
            raise ValueError("Changed input " + r["path"])
    out, meta = RQ/"tables"/RUN, RQ/"metadata"/RUN
    if out.exists() or meta.exists():
        raise FileExistsError("Preserve archived runs")
    published = rows(RQ/"tables/published_cell_audit_v1/cell_selection.tsv")
    candidate = rows(RQ/"tables/external_pilot_v2/cell_selection.tsv")
    matrices = json.loads((RQ/"metadata/external_acquisition_v1/raw_matrices.json").read_text())
    genes = cfg["new_readouts"] + cfg["context_readouts"]
    coverage, summaries, associations, mapping = [], [], [], []
    raw_inputs = []
    for rec in matrices:
        lib = rec["library"]; path = ROOT/rec["path"]
        if digest(path) != rec["sha256"]:
            raise ValueError("Changed raw source")
        raw_inputs.append(dict(path=rec["path"],sha256=rec["sha256"]))
        groups = {}
        for group in cfg["selections"]:
            if group.startswith("published_"):
                col = group.replace("published_", "")
                rr = [r for r in published if r["library"] == lib and r[col] == "True"]
            else:
                qc = group.rsplit("_", 1)[1]
                rr = [r for r in candidate if r["library"] == lib and r["qc"] == qc and r["AT2_candidate"] == "True"]
            lookup = {r["barcode"]: r for r in rr}
            if len(lookup) != len(rr):
                raise ValueError("Duplicate selection barcode")
            groups[group] = lookup
        union = set().union(*(set(v) for v in groups.values()))
        with h5py.File(path,"r") as f:
            g=f["hg19"]
            names=[v.decode() for v in g["gene_names"][:]]; ids=[v.decode() for v in g["genes"][:]]
            barcodes=[v.decode() for v in g["barcodes"][:]]
            if len(set(barcodes)) != len(barcodes):
                raise ValueError("Duplicate raw barcode")
            jj=[i for i,b in enumerate(barcodes) if b in union]; kept=[barcodes[i] for i in jj]
            if set(kept) != union:
                raise ValueError("Unrecovered archived selection")
            x=csc_matrix((g["data"][:],g["indices"][:],g["indptr"][:]),shape=tuple(g["shape"][:]))[:,jj].tocsr()
        x.sum_duplicates(); x.eliminate_zeros()
        total=np.asarray(x.sum(axis=0)).ravel(); ng=np.asarray((x>0).sum(axis=0)).ravel()
        vectors={}
        for gene in genes:
            ix=[i for i,n in enumerate(names) if n == gene]
            mapping.append(dict(library=lib,gene=gene,features=len(ix),stable_ids=";".join(ids[i] for i in ix),status="unique" if len(ix)==1 else "unavailable"))
            vectors[gene]=x[ix[0]].toarray().ravel() if len(ix)==1 else None
        for group, lookup in groups.items():
            mask=np.array([b in lookup for b in kept]); n=int(mask.sum())
            for i in np.flatnonzero(mask):
                if int(lookup[kept[i]]["umi"]) != total[i] or int(lookup[kept[i]]["n_genes"]) != ng[i]:
                    raise ValueError("Archived QC mismatch")
            coverage.append(dict(library=lib,group=group,n=n,median_umi=float(np.median(total[mask])) if n else "",median_genes=float(np.median(ng[mask])) if n else ""))
            for gene in genes:
                v=vectors[gene]; available=v is not None and n>0
                summaries.append(dict(library=lib,group=group,gene=gene,n=n,status="available" if available else "missing",n_detected=int((v[mask]>0).sum()) if available else "",fraction_detected=float((v[mask]>0).mean()) if available else "",mean_log1p_10k=float(np.log1p(v[mask]*10000/total[mask]).mean()) if available else "",sum_count_cpm=float(v[mask].sum()*1e6/total[mask].sum()) if available else ""))
            for a in cfg["new_readouts"]:
                for b in ["KRT8","SPRR1A","CLU"]:
                    va,vb=vectors[a],vectors[b]
                    da=int((va[mask]>0).sum()) if va is not None else 0
                    db=int((vb[mask]>0).sum()) if vb is not None else 0
                    valid=va is not None and vb is not None and n>=50 and min(da,db)>=20 and min(da,db)>=.05*n
                    result=dict.fromkeys(["spearman","partial_rank","x_depth","y_depth","x_ngenes","y_ngenes"], "")
                    if valid:
                        result=rank_association(np.log1p(va[mask]*10000/total[mask]),np.log1p(vb[mask]*10000/total[mask]),total[mask],ng[mask])
                        if result["partial_rank"] is None:
                            valid=False
                    associations.append(dict(library=lib,group=group,transporter=a,state_marker=b,n=n,transporter_detected=da,marker_detected=db,status="descriptive" if valid else "not_estimable",reason="" if valid else "missing_feature_low_detection_or_constant",**result))
    differences=[]
    for group in cfg["selections"]:
        for gene in genes:
            a=next(r for r in summaries if (r["library"],r["group"],r["gene"])==(cfg["primary_comparison"][0],group,gene))
            b=next(r for r in summaries if (r["library"],r["group"],r["gene"])==(cfg["primary_comparison"][1],group,gene))
            valid=a["status"]==b["status"]=="available" and min(a["n"],b["n"])>=50
            differences.append(dict(group=group,gene=gene,pam_n=a["n"],control_n=b["n"],status="descriptive" if valid else "not_estimable",mean_log1p_difference=a["mean_log1p_10k"]-b["mean_log1p_10k"] if valid else "",detection_percentage_point_difference=100*(a["fraction_detected"]-b["fraction_detected"]) if valid else "",sum_count_cpm_difference=a["sum_count_cpm"]-b["sum_count_cpm"] if valid else ""))
    out.mkdir(parents=True);meta.mkdir(parents=True)
    for name,rr in [("gene_mapping",mapping),("coverage",coverage),("summaries",summaries),("differences",differences),("associations",associations)]:
        write(out/(name+".tsv"),rr)
    inputs=cfg["inputs"]+raw_inputs+[dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p)) for p in [contract,Path(__file__)]]
    outputs=[dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p)) for p in sorted(out.glob("*.tsv"))]
    rec=dict(status="completed descriptive transporter RNA context",completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,h5py=h5py.__version__,inputs=inputs,outputs=outputs)
    (meta/"run_record.json").write_text(json.dumps(rec,indent=2)+"\n")
    for r in differences:
        if r["gene"] in cfg["new_readouts"]:
            print(r["group"],r["gene"],r["mean_log1p_difference"])
    print("Estimable associations",sum(r["status"]=="descriptive" for r in associations),"of",len(associations))


if __name__=="__main__":
    run()
