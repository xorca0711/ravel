"""S3 reporter, size, in-vitro footprint and anchored Thbs1 methylation readbacks."""
import io
import sys
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, ttest_1samp, ttest_ind

from plot_readback import draw

CACHE = Path("raw_data/nagaraja_s0")
SOURCE = Path(__file__).resolve().parent / "source"
GROUP = ["history","exposure"]


def write(out, name, frame):
    frame.to_csv(out/(name+".tsv"),sep="\t",index=False,na_rep="NA",lineterminator="\n",float_format="%.15g")


def function_panels(out):
    workbook = CACHE/"moesm8.xlsx"
    rows, summaries, contrasts = [], [], []
    pairs = [(("Control","T5224"),("Control","DMSO")), (("Colitis","T5224"),("Colitis","DMSO")),
             (("Colitis","DMSO"),("Control","DMSO")), (("Colitis","T5224"),("Control","T5224"))]
    for sheet, endpoint, expected in [("Fig. 2l","EdU_pct",[5,5,4,3]),("Fig. 2n","diameter_um",[86,87,67,71])]:
        f = pd.read_excel(workbook,sheet_name=sheet)
        f.columns=["source_label","value"]
        parsed = f.source_label.str.extract(r"^(Control|Colitis) \+ (DMSO|T5224)(?: replicate (\d+))?$")
        parsed.columns=[*GROUP,"within_arm_replicate"]
        f = f.join(parsed)
        assert f[GROUP].notna().all().all() and np.isfinite(f.value).all()
        f["sheet_row"]=np.arange(2,len(f)+2)
        f["endpoint"]=endpoint
        if endpoint=="EdU_pct":
            assert f.value.between(0,100).all() and not f.duplicated([*GROUP,"within_arm_replicate"]).any()
        else:
            assert f.value.gt(0).all() and f.within_arm_replicate.isna().all()
        rows.append(f)
        grouped = f.groupby(GROUP,sort=False).value
        counts=[len(grouped.get_group((h,t))) for h in ("Control","Colitis") for t in ("DMSO","T5224")]
        assert counts==expected
        for (h,t), x in grouped:
            summaries.append(dict(endpoint=endpoint,history=h,exposure=t,n=len(x),mean=x.mean(),
                                  median=x.median(),q25=x.quantile(.25),q75=x.quantile(.75),sd=x.std(),
                                  sem=x.sem() if endpoint=="EdU_pct" else np.nan,
                                  above_200=int(x.gt(200).sum()) if endpoint=="diameter_um" else np.nan,
                                  pct_above_200=100*x.gt(200).mean() if endpoint=="diameter_um" else np.nan))
        for left,right in pairs:
            a,b=grouped.get_group(left),grouped.get_group(right)
            contrasts.append(dict(endpoint=endpoint,left=" ".join(left),right=" ".join(right),
                                  n_left=len(a),n_right=len(b),difference_of_means=a.mean()-b.mean(),
                                  difference_of_medians=a.median()-b.median(),
                                  pctpoint_difference_above_200=100*(a.gt(200).mean()-b.gt(200).mean()) if endpoint=="diameter_um" else np.nan,
                                  welch_p=ttest_ind(a,b,equal_var=False).pvalue if endpoint=="EdU_pct" else np.nan,
                                  pooled_t_p=ttest_ind(a,b,equal_var=True).pvalue if endpoint=="EdU_pct" else np.nan,
                                  organoid_rank_sum_p=mannwhitneyu(a,b,alternative="two-sided",method="asymptotic",use_continuity=True).pvalue if endpoint=="diameter_um" else np.nan))
    data=pd.concat(rows,ignore_index=True);summary=pd.DataFrame(summaries)
    write(out,"function_measurements",data)
    write(out,"function_groups",summary);write(out,"function_contrasts",pd.DataFrame(contrasts))
    return data,summary


def binding(out):
    with ZipFile(CACHE/"moesm5.zip") as z:
        sheet,=[n for n in z.namelist() if "Table6_" in n]
        book=pd.ExcelFile(io.BytesIO(z.read(sheet)))
        raw=pd.read_excel(book,sheet_name=0);published=pd.read_excel(book,sheet_name=1)
    raw.columns=["chrom","start","end","motif_class","condition","raw_score"]
    raw["raw_score"]=pd.to_numeric(raw.raw_score,errors="raise")
    key=["chrom","start","end","motif_class"]
    regions=pd.read_csv(CACHE/"code/7_inVitroFootprinting/Regions.csv").rename(columns={
        "Chromosome":"chrom","motif_start":"start","motif_end":"end","label":"motif_class"})
    assert set(map(tuple,raw[key].values))==set(map(tuple,regions[key].values))
    assert len(raw)==819 and raw.groupby(key).condition.nunique().eq(13).all()
    wide=raw.pivot(index=key,columns="condition",values="raw_score")
    assert np.isfinite(wide.values).all() and len(wide)==63 and wide.JUNFOS.gt(0).all()
    # Preserve both no-TF runs, then check their equal-weight pooled score per locus.
    wide["Control"]=(wide.Control_1+wide.Control_2)/2
    relative=wide.div(wide.JUNFOS,axis=0)
    raw_full=wide.reset_index().melt(id_vars=key,var_name="condition",value_name="raw_score")
    norm=relative.reset_index().melt(id_vars=key,var_name="condition",value_name="fold_vs_JUNFOS")
    norm=norm.merge(raw_full,on=[*key,"condition"],validate="one_to_one")
    baseline=wide.JUNFOS.rename("JUNFOS_raw").reset_index()
    norm=norm.merge(baseline,on=key,validate="many_to_one")
    p=published.set_index("TF")
    summary=[]
    for (cl,t),g in norm.groupby(["motif_class","condition"]):
        x=g.fold_vs_JUNFOS
        orig=(p.loc[t].iloc[:3] if cl=="AP1 only" else p.loc[t].iloc[3:]) if t in p.index else [np.nan]*3
        summary.append(dict(motif_class=cl,condition=t,loci=len(x),mean=x.mean(),sd=x.std(),
                            sem=x.sem(),median=x.median(),p_vs_one=ttest_1samp(x,1).pvalue if t!="JUNFOS" else np.nan,
                            t6_mean=float(orig.iloc[0] if hasattr(orig,"iloc") else orig[0]),
                            t6_sd=float(orig.iloc[1] if hasattr(orig,"iloc") else orig[1]),
                            t6_p=float(orig.iloc[2] if hasattr(orig,"iloc") else orig[2])))
    result=pd.DataFrame(summary);write(out,"binding_loci",norm);write(out,"binding_summary",result)
    return result


def methylation(out):
    src=pd.read_csv(SOURCE/"thbs1_track_sources.tsv",sep="\t")
    intervals=pd.read_csv(SOURCE/"thbs1_track_slices.tsv",sep="\t")
    dna=(SOURCE/"thbs1_reference.txt").read_text().strip()
    assert len(dna)==3002 and intervals.chrom.eq("chr2").all() and intervals.fraction.between(0,1).all()
    assert src.gsm.nunique()==6 and src.groupby("history").size().eq(3).all()
    sites=[118114999+i for i in range(1,len(dna)-1) if dna[i:i+2]=="CG"]
    fractions=pd.DataFrame(index=pd.Index(sites,name="mm10_plus_C_0based"))
    for gsm,g in intervals.groupby("gsm"):
        values={}
        for row in g.itertuples():
            assert 118115000<=row.start<row.end<=118118000
            for position in range(row.start,row.end):
                assert position not in values
                values[position]=row.fraction
        fractions[gsm]=pd.Series(values)
    assert set(fractions.columns)==set(src.gsm)
    complete=fractions.notna().all(axis=1)
    assert complete.any()
    summary=src[["gsm","history","mouse_label","passage"]].copy().set_index("gsm")
    summary["reference_CpGs"]=len(fractions)
    summary["observed_plus_C_sites"]=fractions.count()
    summary["all_observed_mean_fraction"]=fractions.mean()
    summary["six_way_common_sites"]=int(complete.sum())
    summary["common_site_mean_fraction"]=fractions[complete].mean()
    summary["common_site_median_fraction"]=fractions[complete].median()
    summary=summary.reset_index()
    fractions["in_all_six"]=complete
    write(out,"thbs1_cpg_fractions",fractions.reset_index());write(out,"thbs1_libraries",summary)
    means=summary.groupby("history").common_site_mean_fraction.mean()
    comparison=pd.DataFrame([dict(control_libraries=3,colitis_libraries=3,common_sites=int(complete.sum()),
                        control_fraction=means.Control,colitis_fraction=means.Colitis,
                        colitis_minus_control_pp=100*(means.Colitis-means.Control))])
    write(out,"thbs1_contrast",comparison)
    return summary


if __name__=="__main__":
    out=Path(sys.argv[1])
    data,groups=function_panels(out)
    scores=binding(out)
    libs=methylation(out)
    draw(out,data,groups,scores,libs)
