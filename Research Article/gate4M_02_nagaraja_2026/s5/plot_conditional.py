"""Show conditional dispersion, cell selection and leave-one-mouse sensitivity."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SCHEMES=("global","line","line_hnf4g")
LABELS=("Global","Within mouse line","Within line and Hnf4g band")
COLORS=("#337a9a","#b55d27","#79578c")


def render(out,t,lines):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"pdf.fonttype":42,
                         "axes.spines.top":False,"axes.spines.right":False,"text.color":"black",
                         "axes.labelcolor":"black","xtick.color":"black","ytick.color":"black"})
    fig,(ax,bx)=plt.subplots(1,2,figsize=(10.7,4.7),gridspec_kw={"width_ratios":[1,1.15]})
    fig.subplots_adjust(left=.11,right=.98,bottom=.24,top=.75,wspace=.40)
    fig.suptitle("How much Fos-family resemblance remains within mouse lines?",x=.045,y=.97,ha="left",fontsize=15,fontweight="bold")
    fig.text(.045,.865,"Exclusive clone assignments · 5,000 shuffles of individual cells per comparison · lower values indicate closer resemblance",fontsize=9.5)
    full=t.loc[t.omitted_line.eq("none")]
    for i,(sch,label,color) in enumerate(zip(SCHEMES,LABELS,COLORS)):
        xy=full.loc[full.scheme.eq(sch)].set_index("min_clone_size")
        ax.plot([i-.11,i+.11],xy.loc[[2,5],"observed_minus_null"],color=color,lw=1)
        ax.scatter(i-.11,xy.loc[2,"observed_minus_null"],marker="o",s=53,c=color,zorder=3)
        ax.scatter(i+.11,xy.loc[5,"observed_minus_null"],marker="D",s=43,facecolor="white",edgecolor=color,zorder=3)
        loo=t.loc[t.min_clone_size.eq(2)&t.omitted_line.ne("none")&t.scheme.eq(sch)].set_index("omitted_line")
        bx.scatter(np.arange(6)+(i-1)*.15,loo.loc[lines,"observed_minus_null"],s=30,color=color,marker=["o","s","^"][i],label=label)
    for axis in (ax,bx):
        axis.axhline(0,color=".45",ls="--",lw=.8)
        axis.set_ylabel("Observed − mean null variance")
    ax.set_xticks(range(3),["Global","Within\nline","Within line +\nHnf4g band"],fontsize=9)
    ax.set_title("A   Clone-size sensitivity",loc="left",fontsize=11,fontweight="bold")
    bx.set_xticks(range(6),[line.rsplit("-",1)[1] for line in lines])
    bx.set_xlabel("Mouse line omitted");bx.set_title("B   Leave one of six lines out",loc="left",fontsize=11,fontweight="bold")
    bx.legend(frameon=False,loc="upper left",bbox_to_anchor=(-.02,-.24),ncol=2,fontsize=8,handlelength=.9,columnspacing=.8)
    fig.text(.08,.07,"Filled circles include clones with ≥2 cells.\nOpen diamonds require ≥5 cells.",fontsize=8.5)
    for ext in ("png","pdf"):
        fig.savefig(out/("fos_conditional_dispersion."+ext),dpi=190,facecolor="white")
    plt.close(fig)
