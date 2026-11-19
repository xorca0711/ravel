"""Frozen equal-region and common-support estimators for four unpaired pools."""
import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from m24_reader import CLASSES, ROOT, inputs_by_name, load_cohort, read_rows, write_json, write_rows

COVARIATES = ("s3_D6_log2FoldChange", "width_bp")
PRIMARY = "full_mean"
MEDIAN = "full_median"
WEIGHTED = "overlap_weighted_mean"


def support(regions):
    x = np.asarray([[float(r[k]) for k in COVARIATES] for r in regions])
    classes = np.asarray([r["source_class"] for r in regions])
    if not np.isfinite(x).all() or np.any(x[:,1] <= 0) or set(classes) != set(CLASSES):
        raise ValueError("Incomplete design covariates or classes")
    cuts = np.quantile(x, [.25,.5,.75], axis=0, method="linear")
    bins = [tuple(np.searchsorted(cuts[:,j],row[j],side="right").item()+1 for j in range(2)) for row in x]
    counts = Counter(zip(bins,classes))
    strata = []
    minima = {}
    for a in range(1,5):
        for b in range(1,5):
            cell = (a,b)
            m,r = (counts[cell,k] for k in CLASSES)
            minima[cell] = min(m,r)
            strata.append(dict(D6_bin=a,width_bin=b,Memory=m,Resolved=r,overlap_units=min(m,r)))
    total = sum(minima.values())
    weights = np.asarray([minima[cell] / (total*counts[cell,k]) if total else 0.0 for cell,k in zip(bins,classes)])
    for rec in strata:
        rec["weight_per_class"] = rec["overlap_units"]/total if total else 0.0
    rows = [dict(s2_excel_row=r["s2_excel_row"],source_class=k,D6_log2FC=float(v[0]),
                 width_bp=int(v[1]),D6_bin=cell[0],width_bin=cell[1],overlap_weight=float(w))
            for r,k,v,cell,w in zip(regions,classes,x,bins,weights,strict=True)]
    summary = {}
    masks = {k:classes == k for k in CLASSES}
    for k, mask in masks.items():
        wk = weights[mask]
        if total and not np.isclose(wk.sum(),1,rtol=0,atol=1e-12):
            raise ValueError("Overlap weights failed to normalize within class")
        summary[k] = dict(full=int(mask.sum()),shared=int(np.count_nonzero(wk)),excluded=int(np.count_nonzero(wk==0)),
                          regional_Kish_ESS=float(1/np.dot(wk,wk)) if total else None)
    balance = []
    for j, field in enumerate(COVARIATES):
        series = [x[masks[k],j] for k in CLASSES]
        df = sum(len(v)-1 for v in series)
        ss = sum(float(np.sum((v-v.mean())**2)) for v in series)
        sd = float(np.sqrt(ss/df)) if df else 0.0
        for method in ([PRIMARY, WEIGHTED] if total else [PRIMARY]):
            means = [float(np.average(v,weights=weights[masks[k]] if method==WEIGHTED else None)) for k,v in zip(CLASSES,series)]
            difference=means[0]-means[1]
            balance.append(dict(covariate=field,method=method,Memory=means[0],Resolved=means[1],difference=difference,
                                full_pooled_within_class_sd=sd,standardized_difference=difference/sd if sd else None))
    design = dict(cutpoints={f:cuts[:,j].tolist() for j,f in enumerate(COVARIATES)},strata=strata,
                  total_overlap_units=total,classes=summary,balance=balance,
                  weighted_status="estimable" if total else "no_common_support")
    return rows, design


def summarize(regions, samples, intervals, weights):
    ids = [r["s2_excel_row"] for r in regions]
    if len(ids)!=len(set(ids)) or len({s["gsm"] for s in samples})!=4:
        raise ValueError("Duplicated region or incorrect pool identities")
    weights_by_id = {r["s2_excel_row"]:r["overlap_weight"] for r in weights}
    if len(weights)!=len(ids) or set(ids)!=set(weights_by_id):
        raise ValueError("Weights do not cover the frozen regions")
    classes = np.array([r["source_class"] for r in regions])
    w = np.array([weights_by_id[i] for i in ids])
    expected = {(s["gsm"],i) for s in samples for i in ids}
    by_id = {r["s2_excel_row"]:r for r in regions}
    values = {}
    for row in intervals:
        key = (row["gsm"],row["s2_excel_row"])
        if key not in expected or key in values or row["status"]!="valid":
            raise ValueError("Unexpected, repeated or held interval record")
        source = by_id[key[1]]
        if any(str(row[k])!=str(source[k]) for k in ("chromosome","start0","end0","source_class","width_bp")):
            raise ValueError("Interval identity differs from the source manifest")
        width = int(source["width_bp"])
        if int(row["stored_bp"])!=width or int(row["fetch_bp"])!=width or int(row["absent_bp"])!=0:
            raise ValueError("Interval width or coverage differs at aggregation")
        values[key] = float(row["mean_cpm"])
    if set(values)!=expected or not all(np.isfinite(v) and v>=0 for v in values.values()):
        raise ValueError("Incomplete or invalid interval output")
    methods=[PRIMARY,MEDIAN] + ([WEIGHTED] if np.any(w) else [])
    pools=[]
    for sample in samples:
        arr=np.array([values[sample["gsm"],i] for i in ids])
        for method in methods:
            result=dict(method=method,gsm=sample["gsm"],history=sample["history"],replicate=sample["replicate"])
            for k in CLASSES:
                mask=classes==k
                if method==MEDIAN:
                    value=np.median(arr[mask])
                elif method==WEIGHTED:
                    value=np.average(arr[mask],weights=w[mask])
                else:
                    value=np.mean(arr[mask])
                result[k]=float(value)
            result["gap"]=result["Memory"]-result["Resolved"]
            pools.append(result)
    changes, pairs=[],[]
    for method in methods:
        naive=[v for v in pools if v["method"]==method and v["history"]=="naive"]
        post=[v for v in pools if v["method"]==method and v["history"]=="post_IMQ"]
        if len(naive)!=2 or len(post)!=2:
            raise ValueError("Expected two unpaired pools per condition")
        metrics=("Memory","Resolved","gap")
        row={"method":method}
        for k in metrics:
            row[k]=float(np.mean([p[k] for p in post])-np.mean([n[k] for n in naive]))
        cross=[dict(method=method,post_pool=p["gsm"],naive_pool=n["gsm"],**{k:p[k]-n[k] for k in metrics})
               for p in post for n in naive]
        scale=max(1.,max(abs(v[k]) for v in naive+post for k in metrics))
        tolerance=64*np.finfo(float).eps*scale
        if abs(row["gap"]-(row["Memory"]-row["Resolved"]))>tolerance or any(
            abs(np.mean([p[k] for p in cross])-row[k])>tolerance for k in metrics):
            raise ValueError("Pool-level contrast identities disagree")
        changes.append(row)
        pairs.extend(cross)
    return pools,changes,pairs


def plot(pools,changes,pairs,output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    colors=("#007286","#b34d29")
    plotted=[m for m in (PRIMARY,WEIGHTED) if any(d["method"]==m for d in changes)]
    fig,axes=plt.subplots(len(plotted),2,figsize=(9.3,3.15*len(plotted)+0.8),squeeze=False,sharey="col",layout="constrained")
    for row,method in enumerate(plotted):
        left,right=axes[row]
        these=[p for p in pools if p["method"]==method]
        label="Full cohort" if method==PRIMARY else "D6- and width-weighted"
        for j,(k,color) in enumerate(zip(CLASSES,colors)):
            left.scatter(np.arange(len(these))+(j-.5)*.16,[p[k] for p in these],color=color,
                         marker=("o","s")[j],s=40,label=k,zorder=3)
        left.set(xticks=range(4),xticklabels=[("Naïve" if p["history"]=="naive" else "Post-IMQ")+" "+str(p["replicate"]) for p in these],
                 ylabel="Mean fragment coverage (CPM)",title=label+" · individual pools")
        cp=[p for p in pairs if p["method"]==method]
        effect=next(p for p in changes if p["method"]==method)
        for j,k in enumerate(("Memory","Resolved","gap")):
            right.scatter(j+np.linspace(-.18,.18,4),[p[k] for p in cp],facecolor="none",edgecolor="#506978",s=32,zorder=2)
            right.scatter(j,effect[k],marker="D",color="#182d38",s=35,zorder=3)
        right.axhline(0,color="#606c73",lw=.8)
        right.set(xticks=range(3),xticklabels=["Memory","Resolved","Memory − Resolved"],
                  ylabel="Post-IMQ − naïve (CPM)", title=label+" · history contrasts")
        for ax in (left,right):
            ax.spines[["right","top"]].set_visible(False)
            ax.grid(axis="y",alpha=.16)
            ax.set_axisbelow(True)
    highest=max(p[k] for p in pools if p["method"] in plotted for k in CLASSES)
    axes[0,0].set_ylim(0,highest*1.18 if highest else 1)
    axes[0,0].legend(frameon=False,ncols=2,fontsize=8)
    axes[0,1].legend(handles=[Line2D([],[],marker="o",mfc="none",mec="#506978",ls="",label="Cross-pool contrast"),
        Line2D([],[],marker="D",color="#182d38",ls="",label="Mean change")],frameon=False,fontsize=8)
    fig.suptitle("M24 epidermal accessibility at distal Memory and Resolved regions",fontsize=14)
    for ext in ("png","pdf"):
        fig.savefig(output/f"m24_distal.{ext}",dpi=300)
    plt.close(fig)


def verify_support_reference(design, reference):
    """Marginalize the already registered 3-D counts over pooled baseMean before accessing tracks."""
    source=reference["acute_covariate_support"]
    if any(design["cutpoints"][f]!=source["pooled_quartile_cuts"][f] for f in COVARIATES):
        raise ValueError("Design cutpoints differ from registered metadata")
    axes=[COVARIATES[0],"s3_baseMean",COVARIATES[1]]
    table,=[v for v in source["diagnostics"] if v["axes"]==axes]
    counts=Counter()
    for row in table["cell_counts"]:
        a,_,b=row["bin"]
        for k in CLASSES:
            counts[a,b,k]+=row[k]
    for row in design["strata"]:
        if any(row[k]!=counts[row["D6_bin"],row["width_bin"],k] for k in CLASSES):
            raise ValueError("Joint stratum counts differ from registered metadata")


def finish(regions,samples,output,prepared=None):
    coverage=json.loads((output/"coverage.json").read_bytes())
    if coverage["aggregation"]!="eligible" or coverage["held"] or coverage["complete"]!=len(regions)*len(samples):
        raise ValueError("Coverage hold prevents all class and cross-pool summaries")
    weights,design=prepared if prepared is not None else support(regions)
    pools,changes,pairs=summarize(regions,samples,read_rows(output/"intervals.tsv"),weights)
    write_rows(output/"region_weights.tsv",weights)
    write_json(output/"support.json",design)
    write_rows(output/"pool_summaries.tsv",pools)
    write_rows(output/"history_changes.tsv",changes)
    write_rows(output/"cross_pool.tsv",pairs)
    plot(pools,changes,pairs,output)


def run(contract_path,output):
    contract=json.loads(contract_path.read_bytes())
    paths=inputs_by_name(contract)
    regions,samples=load_cohort(paths)
    prepared=support(regions)
    verify_support_reference(prepared[1],json.loads(paths["region_qualification.json"].read_bytes()))
    source=Path(__file__).with_name("m24_reader.py")
    if os.name=="nt":
        wsl=["wsl.exe","-d","Ubuntu","--exec"]
        root=subprocess.check_output(wsl+["wslpath","-a",str(ROOT)],text=True).strip()
        def linux(p):
            return root+"/"+p.resolve().relative_to(ROOT).as_posix()
        command=wsl+[root+"/raw_data/naik2017_s3_runtime_v1/venv/bin/python","-B",linux(source),
                     "--contract",linux(contract_path),"--output",linux(output)]
    else:
        command=[str(ROOT/"raw_data/naik2017_s3_runtime_v1/venv/bin/python"),"-B",str(source),
                 "--contract",str(contract_path),"--output",str(output)]
    subprocess.run(command,check=True)
    finish(regions,samples,output,prepared)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    run(args.contract.resolve(),args.output.resolve())
