"""S4 mouse burdens, released lesion areas and figure-derived spatial P20 scores."""
import gzip
from pathlib import Path
import re
import sys

import numpy as np
import pandas as pd
import pymupdf

from plot_tumours import render

CACHE=Path("raw_data/nagaraja_s0")
CTRL="Control"
REC="Recovered"


def write(out,name,table):
    table.to_csv(out/(name+".tsv"),index=False,sep="\t",na_rep="NA",float_format="%.15g",lineterminator="\n")


def history(label):
    if label.startswith("Control"):
        return CTRL
    if label.lower().startswith("colitis"):
        return REC
    raise ValueError(label)


def mouse_readback(out):
    frac=pd.read_excel(CACHE/"moesm9.xlsx",sheet_name="Fig. 4c")
    frac.columns=["source_label","large_fraction"]
    totals=pd.read_excel(CACHE/"moesm11.xlsx",sheet_name="Ext. Data Fig. 9d")
    totals.columns=["source_label","count"]
    g=frac.merge(totals,on="source_label",validate="one_to_one",how="outer",indicator=True)
    assert len(g)==9 and g._merge.eq("both").all()
    g=g.drop(columns="_merge")
    prior=pd.read_csv("analysis/research/runs/ng26_s0_v2/gross_sample_join.tsv",sep="\t").set_index("source_label")
    audit=prior.loc[g.source_label]
    assert np.allclose(g.large_fraction,audit.figure4c_fraction,atol=1e-14,rtol=0)
    assert np.array_equal(g["count"],audit.ed9d_count)
    g["large_count"]=np.rint(g.large_fraction*g["count"]).astype(int)
    assert np.allclose(g.large_count,g.large_fraction*g["count"],rtol=0,atol=1e-10)
    g["large_fraction_pct"]=100*g.large_fraction
    g["history"]=g.source_label.map(history)
    assert g.history.value_counts().to_dict()=={CTRL:4,REC:5}
    m=pd.read_excel(CACHE/"moesm11.xlsx",sheet_name="Ext. Data Fig. 9g,h")
    m.columns=["source_label","count","area_fraction"]
    m["history"]=m.source_label.map(history)
    assert m.source_label.is_unique and m.history.value_counts().to_dict()=={CTRL:7,REC:10}
    assert m.area_fraction.between(0,1).all() and m["count"].ge(0).all()
    m["area_fraction_pct"]=100*m.area_fraction
    write(out,"gross_mice",g);write(out,"microscopic_mice",m)
    sums=[]
    for series,frame,fields in [("gross",g,["count","large_fraction_pct","large_count"]),
                                ("microscopic",m,["count","area_fraction_pct"])]:
        for field in fields:
            def diff(f):
                means=f.groupby("history")[field].mean()
                return means[REC]-means[CTRL]
            leave=[diff(frame.drop(i)) for i in frame.index]
            c=frame.loc[frame.history.eq(CTRL),field];h=frame.loc[frame.history.eq(REC),field]
            sums.append(dict(series=series,endpoint=field,n_control=len(c),n_recovered=len(h),
                             control_mean=c.mean(),recovered_mean=h.mean(),control_median=c.median(),
                             recovered_median=h.median(),recovered_minus_control=diff(frame),
                             leave_one_mouse_min=min(leave),leave_one_mouse_max=max(leave)))
    write(out,"mouse_contrasts",pd.DataFrame(sums))
    return g,m


def lesion_readback(out,gross,micro):
    records=[];summary=[]
    panels=[("ED9a","moesm11.xlsx","Ext. Data Fig. 9a","diameter_mm",1),
            ("4e","moesm9.xlsx","Fig. 4e","area_um2",20000),
            ("4l","moesm9.xlsx","Fig. 4l","area_um2",20000)]
    legends={"4e":{(CTRL,"none"):(88,7),(REC,"none"):(256,10)},
             "4l":{(CTRL,"vehicle"):(48,6),(CTRL,"T5224"):(43,5),
                   (REC,"vehicle"):(95,7),(REC,"T5224"):(163,7)}}
    for panel,book,sheet,unit,cutoff in panels:
        f=pd.read_excel(CACHE/book,sheet_name=sheet)
        f.columns=["source_label","value"];f["sheet_row"]=np.arange(2,len(f)+2)
        assert np.isfinite(f.value).all() and f.value.gt(0).all()
        f["history"]=f.source_label.map(history)
        f["arm"]=f.source_label.map(lambda x:"vehicle" if "DMSO" in x else "T5224" if "T5224" in x else "none")
        f["panel"]=panel;f["unit"]=unit;records.append(f)
        for (h,t),group in f.groupby(["history","arm"]):
            x=group.value
            denominator,animals=legends.get(panel,{}).get((h,t),(np.nan,np.nan))
            matching=np.nan;large=np.nan
            if panel in ("ED9a","4e"):
                mice=gross if panel=="ED9a" else micro
                sub=mice.loc[mice.history.eq(h)]
                matching=int(sub["count"].sum())
                assert matching==len(x)
                if panel=="ED9a":
                    large=int(sub.large_count.sum())
            summary.append(dict(panel=panel,history=h,arm=t,unit=unit,released_rows=len(x),
                                legend_lesions=denominator,legend_mice=animals,
                                legend_minus_release=denominator-len(x),matching_mouse_count_sum=matching,
                                mean=x.mean(),median=x.median(),q25=x.quantile(.25),q75=x.quantile(.75),
                                min=x.min(),max=x.max(),strict_cutoff=cutoff,above_cutoff=x.gt(cutoff).sum(),
                                pct_above_cutoff=x.gt(cutoff).mean()*100,mouse_implied_large_count=large))
    allrows=pd.concat(records,ignore_index=True);summary=pd.DataFrame(summary)
    write(out,"lesion_measurements",allrows);write(out,"lesion_distributions",summary)
    return allrows,summary


def spatial(out):
    # Foreground fill distinguishes one mark per lesion from the second PDF paint layer.
    pdf=pymupdf.open(CACHE/"article.pdf")
    page=pdf[7]; bounds=pymupdf.Rect(39,302,138,422)
    drawn=[d for d in page.get_drawings() if bounds.contains(d["rect"])]
    ticks=sorted(d["rect"].y0 for d in drawn if d["type"]=="s" and
                 abs(d["rect"].x1-65.44)<.03 and abs(d["rect"].width-1.67)<.03)
    assert len(ticks)==4
    zero=ticks[2];scale=(ticks[-1]-ticks[0])/12
    pts=[]
    for d in drawn:
        if d["type"]!="fs" or [item[0] for item in d["items"]]!=["c"]*4:
            continue
        color=np.asarray(d["fill"])
        if np.linalg.norm(color-[.75,.75,.75])<.035:
            h=CTRL
        elif np.linalg.norm(color-[.79,.12,.27])<.035:
            h=REC
        else:
            continue
        rect=d["rect"];x=(rect.x0+rect.x1)/2;y=(rect.y0+rect.y1)/2
        assert (70<x<90 if h==CTRL else 95<x<115) and 2.1<rect.width<2.4
        pts.append(dict(history=h,pdf_x_pt=x,pdf_y_pt=y,plot_P20_score=(zero-y)/scale))
    points=pd.DataFrame(pts)
    assert points.history.value_counts().to_dict()=={CTRL:117,REC:137}
    summaries=[]
    for h,g in points.groupby("history"):
        x=g.plot_P20_score
        summaries.append(dict(history=h,sections=1,plotted_lesions=len(x),median=x.median(),
                              mean=x.mean(),q25=x.quantile(.25),q75=x.quantile(.75),
                              scored_above_three=x.gt(3).sum(),percent_above_three=100*x.gt(3).mean(),
                              within_0p05_of_threshold=x.sub(3).abs().le(.05).sum()))
    write(out,"p20_plotted_points",points);write(out,"p20_plotted_summary",pd.DataFrame(summaries))
    text=gzip.open(CACHE/"GSE316618_family.soft.gz","rt").read();files=[]
    for section in re.split(r"(?=\^SAMPLE = )",text):
        if not section.startswith("^SAMPLE"):
            continue
        gsm=section.splitlines()[0].split(" = ")[1]
        title=re.search(r"^!Sample_title = (.+)$",section,re.M)[1]
        for url in re.findall(r"^!Sample_supplementary_file_\d+ = (.+)$",section,re.M):
            files.append(dict(gsm=gsm,title=title,file=url.rsplit("/",1)[1],url=url.replace("ftp://","https://")))
    manifest=pd.DataFrame(files);assert manifest.gsm.nunique()==2
    write(out,"spatial_file_inventory",manifest)
    return points


if __name__=="__main__":
    out=Path(sys.argv[1]);g,m=mouse_readback(out)
    lesions,summaries=lesion_readback(out,g,m)
    points=spatial(out)
    render(out,g,m,lesions,summaries,points)
