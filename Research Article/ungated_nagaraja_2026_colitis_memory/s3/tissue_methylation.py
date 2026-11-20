"""Read the two printed ED6e windows from the GSE316762 tissue tracks."""
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SOURCE=Path(__file__).resolve().parent/"source"
LOCI={"Dcaf5":("chr12",80433160,80433600),"Rbm27":("chr18",42347000,42347400)}
ARMS=["Control vehicle","Recovered vehicle","Recovered T5224","Control T5224"]


def write(out,name,table):
    table.to_csv(out/(name+".tsv"),index=False,sep="\t",lineterminator="\n",na_rep="NA",float_format="%.15g")


def read_locus(gene,src,rows):
    chrom,start,end=LOCI[gene]
    dna=(SOURCE/(gene+"_reference.txt")).read_text().strip()
    assert len(dna)==end-start+2
    pos=[start-1+i for i in range(1,len(dna)-1) if dna[i:i+2]=="CG"]
    sites=pd.DataFrame(index=pd.Index(pos,name="mm10_plus_C_0based"))
    for gsm,g in rows.groupby("gsm"):
        values={}
        for item in g.itertuples():
            assert item.chrom==chrom and start<=item.start<item.end<=end and 0<=item.fraction<=1
            for bp in range(item.start,item.end):
                assert bp not in values
                values[bp]=item.fraction
        sites[gsm]=pd.Series(values)
    assert set(sites)==set(src.gsm)
    primary=sites.notna().all(axis=1)
    nine=src.loc[src.arm.ne("Control T5224"),"gsm"]
    display=sites[nine].notna().all(axis=1)
    assert primary.any() and display.any()
    summary=src[["gsm","arm","mouse"]].copy().set_index("gsm")
    summary["n_reference_sites"]=len(sites)
    summary["n_observed_sites"]=sites.count()
    summary["mean_all_observed_fraction"]=sites.mean()
    summary["n_common_all_arms"]=int(primary.sum())
    summary["mean_common_fraction"]=sites.loc[primary].mean()
    summary["n_common_three_displayed_arms"]=int(display.sum())
    summary["displayed_arm_sensitivity_fraction"]=sites.loc[display,nine].mean()
    summary["locus"]=gene
    sites["common_all_arms"]=primary
    sites["common_three_displayed_arms"]=display
    sites.insert(0,"locus",gene)
    return summary.reset_index(),sites.reset_index()


def draw(out,result):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"pdf.fonttype":42,
                         "axes.spines.right":False,"axes.spines.top":False,"text.color":"black",
                         "axes.labelcolor":"black","xtick.color":"black","ytick.color":"black"})
    fig,axes=plt.subplots(1,2,figsize=(9.5,4.2),sharey=True)
    fig.subplots_adjust(left=.085,right=.98,bottom=.24,top=.74,wspace=.22)
    fig.suptitle("Whole-colon methylation after recovery and AP-1 inhibition",x=.045,y=.97,ha="left",
                 fontsize=15,fontweight="bold")
    fig.text(.045,.865,"Each point is one mouse. Bars show the arm mean, with three mice per arm.",fontsize=10)
    for ax,gene in zip(axes,LOCI):
        t=result.loc[result.locus.eq(gene)]
        for i,arm in enumerate(ARMS):
            obs=t.loc[t.arm.eq(arm)].sort_values("mouse").mean_common_fraction.to_numpy()*100
            ax.scatter(i+np.linspace(-.12,.12,len(obs)),obs,s=37,color="#28729a" if "Control" in arm else "#c06421",
                       marker="D" if "T5224" in arm else "o",lw=0)
            ax.hlines(obs.mean(),i-.22,i+.22,color="black",lw=1.6)
        ax.set_title(f"{gene} · {t.n_common_all_arms.iloc[0]} common CpGs",loc="left",fontsize=11,fontweight="bold")
        ax.set_xticks(range(4),["Control\nvehicle","Recovered\nvehicle","Recovered\nT-5224","Control\nT-5224"],fontsize=8.5)
        ax.set(xlim=(-.4,3.4),ylim=(0,100))
    axes[0].set_ylabel("Mean methylation at shared CpGs (%)")
    fig.text(.085,.065,"Regions follow the printed Extended Data Fig. 6e coordinates. Each shared reference CpG receives equal weight.",fontsize=8.5)
    for ext in ["png","pdf"]:
        fig.savefig(out/("ed6e_tissue_methylation."+ext),dpi=190,facecolor="white")
    plt.close(fig)


def main(out):
    src=pd.read_csv(SOURCE/"ed6_tissue_sources.tsv",sep="\t")
    assert src.gsm.nunique()==src.mouse.nunique()==len(src)==12 and src.groupby("arm").size().eq(3).all()
    intervals=pd.read_csv(SOURCE/"ed6_tissue_slices.tsv",sep="\t")
    samples=[];cpgs=[]
    for gene in LOCI:
        s,c=read_locus(gene,src,intervals.loc[intervals.locus.eq(gene)])
        samples.append(s);cpgs.append(c)
    sample=pd.concat(samples,ignore_index=True)
    write(out,"tissue_libraries",sample)
    write(out,"tissue_cpg_fractions",pd.concat(cpgs,ignore_index=True))
    means=sample.groupby(["locus","arm"],as_index=False).agg(n_mice=("mouse","size"),
          mean_fraction=("mean_common_fraction","mean"),min_fraction=("mean_common_fraction","min"),
          max_fraction=("mean_common_fraction","max"))
    write(out,"tissue_arms",means)
    contrasts=[]
    for gene,g in means.groupby("locus"):
        indexed=g.set_index("arm").mean_fraction
        for left,right in [("Recovered vehicle","Control vehicle"),("Recovered T5224","Recovered vehicle"),
                           ("Recovered T5224","Control vehicle"),("Control T5224","Control vehicle")]:
            contrasts.append(dict(locus=gene,left=left,right=right,difference_pp=100*(indexed[left]-indexed[right])))
    write(out,"tissue_contrasts",pd.DataFrame(contrasts))
    draw(out,sample)


if __name__=="__main__":
    main(Path(sys.argv[1]))
