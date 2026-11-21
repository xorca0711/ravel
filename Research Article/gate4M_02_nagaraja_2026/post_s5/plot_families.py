"""Show original native scales and changes under donor-conditional comparison."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


def render(out, leaders, stability):
    plt.rcParams.update({"font.size":9,"text.color":"black","axes.labelcolor":"black",
                         "xtick.color":"black","ytick.color":"black","pdf.fonttype":42,
                         "axes.spines.top":False,"axes.spines.right":False})
    fig, (ax,bx) = plt.subplots(1,2,figsize=(10.6,4.7),gridspec_kw={"width_ratios":[1,1.1]})
    fig.subplots_adjust(top=.79,bottom=.25,left=.084,right=.98,wspace=.40)
    exact = leaders.dropna(subset=["tissue_delta","organ_aligned","org_fdr"])
    palette = {"Both":"#7b488c","Tissue":"#b8701e","Organoid":"#25708d","Neither":"#a6adb3"}
    for group, color in palette.items():
        a = exact.tissue_status.isin(["gain","loss"])
        b = exact.organ_status.eq("tighter")
        mask = {"Both":a&b,"Tissue":a&~b,"Organoid":~a&b,"Neither":~a&~b}[group]
        x = exact.loc[mask]
        ax.scatter(x.tissue_delta,x.organ_aligned,s=29 if group!="Neither" else 17,
                   color=color,alpha=.9,zorder=3,label=group)
    for axis in (ax,bx):
        axis.axvline(0,color="#b2b2b2",lw=.8,zorder=0)
    ax.axhline(0,color="#b2b2b2",lw=.8,zorder=0)
    ax.set(xlabel="Recovered − control chromVAR score",ylabel="Null − observed clone variance")
    ax.set_title("A   Published exact-name comparison",loc="left",fontweight="bold",fontsize=11,pad=13)
    ax.legend(loc="upper center",bbox_to_anchor=(.52,-.24),ncol=4,frameon=False,columnspacing=.7,
              handletextpad=.1,fontsize=8)
    markers = [("organ_aligned","Published","o","#414e56"),("line_qualified_aligned","Line-qualified","^","#bb752f"),
               ("clean_exclusive_aligned","Exclusive","s","#459281"),("within_line_aligned","Within line","D","#825998")]
    names = ["Fos","Etv2","Ctcf","Hnf4g","Hmga2"]
    offsets = [.21,.07,-.07,-.21]
    for j,name in enumerate(names):
        y=len(names)-1-j
        for (col,label,mark,color),dy in zip(markers,offsets):
            x=leaders.at[name,col]
            bx.scatter(x,y+dy,marker=mark,color=color,s=26,zorder=3)
        q=stability.loc[stability.design.eq("keep50") & stability.feature.eq(name)]
        if len(q):
            bx.plot([q.p05.iloc[0],q.p95.iloc[0]],[y+offsets[-1]]*2,color=markers[-1][3],lw=1.4)
    bx.set_yticks(np.arange(len(names))[::-1],names)
    bx.set(xlabel="Null − observed clone variance",ylim=(-.5,len(names)-.5))
    bx.set_title("B   Changing the clone comparison",loc="left",fontweight="bold",fontsize=11,pad=13)
    handles = [Line2D([],[],ls="",marker=mark,color=color,label=label,ms=5) for _,label,mark,color in markers]
    bx.legend(handles=handles,loc="upper center",bbox_to_anchor=(.5,-.24),ncol=4,frameon=False,
              columnspacing=.55,handletextpad=.15,fontsize=8)
    fig.suptitle("Which tissue motif differences also appear in organoid clones?",fontsize=14,
                 x=.06,ha="left",y=.96,fontweight="bold")
    for ext in ("png","pdf"):
        fig.savefig(out/f"family_evidence.{ext}",dpi=210,facecolor="white")
    plt.close(fig)
