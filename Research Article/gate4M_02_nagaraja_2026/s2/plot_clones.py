"""Figures for S2; every mark is derived from a deposited result table."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

REPORTERS = {"Fos": "AP-1 · Fos", "Etv2": "ETS · Etv2", "Ctcf": "CTCF · Ctcf", "Hnf4g": "HNF4/PPAR · Hnf4g"}
HISTORY = {"Control": "#28729a", "Colitis": "#c06421"}


def setup():
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10, "axes.titlesize":11,
                         "axes.labelsize":10, "axes.titleweight":"bold", "axes.spines.top":False,
                         "axes.spines.right":False, "pdf.fonttype":42, "text.color":"black",
                         "axes.labelcolor":"black", "xtick.color":"black", "ytick.color":"black",
                         "legend.labelcolor":"black", "legend.frameon":False})


def save(fig, out, name):
    for ext in ("png", "pdf"):
        fig.savefig(out / f"{name}.{ext}", dpi=185, facecolor="white")
    plt.close(fig)


def draw(out, dispersion, clones, lines):
    setup()
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10.9, 4.55), gridspec_kw={"width_ratios":[1,1.28]})
    fig.subplots_adjust(left=.085, right=.98, bottom=.19, top=.77, wspace=.52)
    fig.suptitle("Which motif scores resemble one another within clones?", x=.06, y=.97,
                 ha="left", fontsize=15, fontweight="bold")
    fig.text(.06,.865,"Mouse colonic organoids  ·  1,000 global label permutations per motif and membership rule",fontsize=10)
    r = dispersion.loc[dispersion.variant.eq("released")]
    ax.scatter(r.delta, -np.log10(r.fdr), color="#77949e", s=16, alpha=.62, linewidth=0)
    styles = ["#b34332","#397357","#3b65a1","#945597"]
    for (key, label), color in zip(REPORTERS.items(),styles):
        row = r.loc[r.feature.eq(key)].iloc[0]
        ax.scatter(row.delta, -np.log10(row.fdr), color=color, edgecolor="black", linewidth=.5, s=42, zorder=3, label=key)
    ax.legend(loc="upper right",fontsize=8.5, handlelength=.8)
    ax.axvline(0, color=".55", lw=.8)
    ax.axhline(-np.log10(.05), color=".42", lw=.9, ls="--")
    ax.set(xlabel="Observed − null variance", ylabel="−log₁₀(BH-adjusted P)")
    ax.set_title("A   Global-label replay",loc="left")
    names=list(REPORTERS)
    specs=[("Table 4","t4_delta","released","o","#232323",-.24),
           ("Released","delta","released","s","#3696b0",-.08),
           ("Line ID","delta","line_qualified","^","#d37e26",.08),
           ("Exclusive","delta","clean_exclusive","D","#9467a9",.24)]
    for label, column, variant, marker, color, dy in specs:
        tab=dispersion.loc[dispersion.variant.eq(variant)].set_index("feature")
        bx.scatter(tab.loc[names,column], np.arange(4)+dy, marker=marker, c=color, s=37, label=label, zorder=3)
    bx.axvline(0,color=".45",lw=.9)
    bx.set_yticks(np.arange(4), REPORTERS.values()); bx.invert_yaxis()
    bx.set(xlabel="Observed − null variance")
    bx.set_title("B   Membership sensitivity",loc="left")
    bx.legend(ncol=2,loc="lower left",bbox_to_anchor=(.00,-.29),fontsize=8.5,
              handlelength=1.2,columnspacing=1.1, borderaxespad=0)
    save(fig,out,"fig2h_dispersion")

    fig,(ax,bx)=plt.subplots(1,2,figsize=(10.9,4.95),gridspec_kw={"width_ratios":[.85,1.25]})
    fig.subplots_adjust(left=.085,right=.98,top=.78,bottom=.20,wspace=.37)
    fig.suptitle("Does the AP-1 history difference span mouse lines?", x=.06,y=.97,
                 ha="left",fontsize=15,fontweight="bold")
    fig.text(.06,.87,"Fos-family motif accessibility  ·  six mouse-derived organoid lines, three per history",fontsize=10)
    r=clones.loc[clones.variant.eq("released")]
    rng=np.random.default_rng(508)
    for x,(name,color) in enumerate(HISTORY.items()):
        v=r.loc[r["sample"].eq(name),"fos_median"]
        ax.scatter(x+rng.uniform(-.19,.19,len(v)),v,s=20,alpha=.6,linewidth=0,color=color)
        ax.hlines(v.median(),x-.28,x+.28,color="black",lw=2,zorder=4)
    ax.axhline(1.25,color=".35",lw=.8,ls="--")
    ax.set_xticks([0,1],["Control\n80 clones","Colitis\n52 clones"])
    ax.set(xlim=(-.5,1.5), ylabel="Median score within each clone")
    ax.set_title("A   Released clone distribution",loc="left")
    fig.text(.085,.065,"Crossbars show group medians. Dashed line marks 1.25.",fontsize=8)
    all_lines=lines.loc[lines.variant.eq("line_qualified")].sort_values("organoid_line")
    exclusive=lines.loc[lines.variant.eq("clean_exclusive")].set_index("organoid_line")
    for x,(_,row) in enumerate(all_lines.iterrows()):
        only=exclusive.loc[row.organoid_line,"mean_clone_median"]
        color=HISTORY[row["sample"]]
        bx.plot([x-.115,x+.115],[row.mean_clone_median,only],lw=1,color=color)
        bx.scatter(x-.115,row.mean_clone_median,s=45,c=color,zorder=3)
        bx.scatter(x+.115,only,marker="D",s=35,facecolor="white",edgecolor=color,zorder=3)
    bx.axhline(0,lw=.7,color=".55")
    bx.set_xticks(np.arange(len(all_lines)),[f"{line.split('-')[-1]}\n{n} clones" for line,n in zip(all_lines.organoid_line,all_lines.n_clones)],fontsize=8)
    bx.set(xlim=(-.55,5.55), ylabel="Mean of clone medians per mouse line")
    bx.set_title("B   Each clone weighted equally within line",loc="left")
    handles=[Line2D([],[],marker="o",color="black",linestyle="",label="Line-qualified clones"),
             Line2D([],[],marker="D",color="black",markerfacecolor="white",linestyle="",label="Exclusive cells")]
    bx.legend(handles=handles,ncol=2,bbox_to_anchor=(.5,-.17),loc="upper center",fontsize=8.5)
    save(fig,out,"fig2i_history")
