"""S3 figures built directly from the deposited endpoint tables."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

COLORS={"Control":"#28729a","Colitis":"#c06421"}
CLASSES={"AP1 only":"#357895","AP1 + Fox":"#a34177"}


def save(out,fig,name):
    for ext in ("png","pdf"):
        fig.savefig(out/f"{name}.{ext}",dpi=190,facecolor="white")
    plt.close(fig)


def draw(out,data,groups,binding,libs):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.titlesize":11,
                         "axes.titleweight":"bold","pdf.fonttype":42,"text.color":"black",
                         "axes.labelcolor":"black","xtick.color":"black","ytick.color":"black",
                         "legend.labelcolor":"black","axes.spines.right":False,"axes.spines.top":False})
    fig,axes=plt.subplots(1,3,figsize=(12.2,4.65),gridspec_kw={"width_ratios":[1,1,.95]})
    fig.subplots_adjust(left=.065,right=.99,top=.77,bottom=.23,wspace=.43)
    fig.suptitle("Organoid proliferation, size after washout and Thbs1 methylation",
                 x=.045,y=.97,ha="left",fontsize=15,fontweight="bold")
    fig.text(.045,.865,"Control-derived cultures are blue and colitis-derived cultures are orange. Each panel has its own sampling unit.",fontsize=10)
    order=[(h,t) for h in COLORS for t in ("DMSO","T5224")]
    rng=np.random.default_rng(920)
    for ax,endpoint,title,ylabel in zip(axes[:2],["EdU_pct","diameter_um"],
            ["A   Drug exposure · 24 h","B   After washout · 20 days"],["EdU-positive cells (%)","Individual organoid diameter (µm)"]):
        labels=[]
        for i,(h,t) in enumerate(order):
            x=data.loc[data.endpoint.eq(endpoint)&data.history.eq(h)&data.exposure.eq(t),"value"]
            s=groups.loc[groups.endpoint.eq(endpoint)&groups.history.eq(h)&groups.exposure.eq(t)].iloc[0]
            ax.scatter(i+rng.uniform(-.16,.16,len(x)),x,color=COLORS[h],alpha=.75 if endpoint=="EdU_pct" else .41,
                       s=31 if endpoint=="EdU_pct" else 12,marker="o" if t=="DMSO" else "D",lw=0)
            middle=s["mean"] if endpoint=="EdU_pct" else s["median"]
            ax.hlines(middle,i-.22,i+.22,color="black",lw=1.8)
            labels.append(("Veh." if t=="DMSO" else "Drug")+f"\nn={len(x)}")
        ax.set_xticks(range(4),labels,fontsize=8.5)
        ax.set(ylabel=ylabel,xlim=(-.5,3.5));ax.set_title(title,loc="left")
        ax.set_ylim(bottom=0)
    axes[1].axhline(200,color=".48",lw=.8,ls="--")
    ax=axes[2]
    for i,h in enumerate(COLORS):
        sub=libs.loc[libs.history.eq(h)].sort_values("mouse_label")
        ys=100*sub.common_site_mean_fraction.to_numpy()
        ax.scatter(i+np.linspace(-.12,.12,len(ys)),ys,s=36,c=COLORS[h],linewidths=0)
        ax.hlines(ys.mean(),i-.22,i+.22,color="black",lw=1.8)
    ax.set_xticks([0,1],["Control\nn=3","Colitis\nn=3"],fontsize=8.5)
    ax.set(xlim=(-.55,1.55),ylabel="Mean methylation at shared CpGs (%)",ylim=(0,100))
    ax.set_title("C   Thbs1 · six libraries",loc="left")
    fig.text(.065,.07,"Bars show means in A and C and medians in B. Dashed line marks 200 µm. Vehicle is DMSO and drug is T-5224.",fontsize=8.5)
    save(out,fig,"organoid_phenotypes_and_thbs1")

    order=["Control_1","Control_2","FOS","JUN","FOXA1","FOXP1","FOSFOXA1","FOSFOXP1",
           "JUNFOXA1","JUNFOXP1","JUNFOS","JUNFOSFOXA1","JUNFOSFOXP1"]
    labels=["No TF, library 1","No TF, library 2","FOS","JUN","FOXA1","FOXP1","FOS + FOXA1","FOS + FOXP1",
            "JUN + FOXA1","JUN + FOXP1","JUN + FOS","JUN + FOS + FOXA1","JUN + FOS + FOXP1"]
    fig,ax=plt.subplots(figsize=(8.8,6.25));fig.subplots_adjust(left=.26,right=.97,top=.81,bottom=.16)
    fig.suptitle("Defined-protein binding at AP-1 motif sites",x=.045,y=.97,ha="left",fontsize=15,fontweight="bold")
    fig.text(.045,.897,"Footprint score of each condition divided by the JUN + FOS score at the same locus",fontsize=10)
    y=np.arange(len(order))
    for cl,dy,m,lab in [("AP1 only",-.16,"o","AP-1 only · 29 loci"),("AP1 + Fox",.16,"D","AP-1/FOX composite · 34 loci")]:
        t=binding.loc[binding.motif_class.eq(cl)].set_index("condition").loc[order]
        ax.errorbar(t["mean"],y+dy,xerr=t["sem"],fmt=m,color=CLASSES[cl],ms=4.8,
                    capsize=2,elinewidth=1.1,label=lab)
    ax.axvline(1,color=".45",lw=1,ls="--")
    ax.set_yticks(y,labels,fontsize=9);ax.invert_yaxis()
    ax.set_xlabel("Mean relative footprint score across loci (± s.e.m.)")
    ax.legend(frameon=False,ncol=2,fontsize=9,loc="lower right",bbox_to_anchor=(1.015,1.01))
    fig.text(.045,.045,"Each named protein condition has one deposited library. Error bars describe variation across loci.",fontsize=9)
    save(out,fig,"fig3i_defined_protein")
