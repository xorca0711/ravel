"""S4 plots with individual mice, lesion distributions and two spatial sections."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

COLORS={"Control":"#28729a","Recovered":"#c06421"}


def save(fig,out,stem):
    for ext in ("png","pdf"):
        fig.savefig(out/f"{stem}.{ext}",dpi=190,facecolor="white")
    plt.close(fig)


def cloud(ax,groups,rng,level):
    labels=[]
    for i,(h,t,series) in enumerate(groups):
        x=np.asarray(series)
        marker="D" if t=="T5224" else "o"
        shift=np.linspace(-.15,.15,len(x)) if level=="mouse" else rng.uniform(-.20,.20,len(x))
        ax.scatter(i+shift,x,c=COLORS[h],s=32 if level=="mouse" else 12,alpha=.88 if level=="mouse" else .45,
                   marker=marker,linewidth=0)
        mid=x.mean() if level=="mouse" else np.median(x)
        ax.hlines(mid,i-.24,i+.24,lw=1.8,color="black")
        labels.append((h if t=="none" else ("Veh." if t=="vehicle" else "Drug"))+f"\nn={len(x)}")
    ax.set_xticks(range(len(labels)),labels,fontsize=8.5)
    ax.set_xlim(-.48,len(groups)-.52)


def render(out,gross,micro,lesions,summaries,points):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"pdf.fonttype":42,
                         "axes.spines.top":False,"axes.spines.right":False,"text.color":"black",
                         "axes.labelcolor":"black","xtick.color":"black","ytick.color":"black"})
    rng=np.random.default_rng(340)
    fig,axes=plt.subplots(1,4,figsize=(12,4))
    fig.subplots_adjust(left=.057,right=.985,bottom=.24,top=.72,wspace=.47)
    fig.suptitle("Adenoma number, size fraction and tissue burden by mouse",x=.043,y=.975,ha="left",
                 fontsize=15,fontweight="bold")
    fig.text(.043,.86,"Each point is one mouse. Black bars show equal-mouse means. Gross and microscopic panels use separate cohorts.",fontsize=9.5)
    specs=[(gross,"count","A   Gross count","Visible adenomas"),
           (gross,"large_fraction_pct","B   Gross size fraction","Adenomas >1 mm (%)"),
           (micro,"count","C   Microscopic count","Lesions in assessed tissue"),
           (micro,"area_fraction_pct","D   Microscopic burden","Tissue area occupied (%)")]
    for ax,(data,col,title,ylab) in zip(axes,specs):
        cloud(ax,[(h,"none",data.loc[data.history.eq(h),col]) for h in COLORS],rng,"mouse")
        ax.set_title(title,loc="left",fontsize=10,fontweight="bold")
        ax.set_ylabel(ylab);ax.set_ylim(bottom=0)
    fig.text(.057,.055,"Panel C uses raw counts. The worksheet lacks each mouse’s assessed tissue area for calculating lesion density.",fontsize=8.5)
    save(fig,out,"mouse_adenoma_burden")

    fig,axes=plt.subplots(1,3,figsize=(11.3,4.35),gridspec_kw={"width_ratios":[.9,1.22,1]})
    fig.subplots_adjust(left=.076,right=.985,top=.73,bottom=.24,wspace=.46)
    fig.suptitle("Microscopic lesion size and spatial P20 expression",x=.043,y=.97,ha="left",
                 fontsize=15,fontweight="bold")
    fig.text(.043,.86,"One point per released area or published P20 symbol. Bars show medians. Colors identify control and recovered histories.",fontsize=9)
    for ax,panel,title in [(axes[0],"4e","A   Microscopic area"),(axes[1],"4l","B   History and inhibitor")]:
        subset=lesions[lesions.panel.eq(panel)]
        groups=[(h,arm,subset.loc[subset.history.eq(h)&subset.arm.eq(arm),"value"]) for h in COLORS for arm in
                (["none"] if panel=="4e" else ["vehicle","T5224"])]
        cloud(ax,groups,rng,"lesion")
        ax.set_yscale("log");ax.yaxis.set_major_formatter(FuncFormatter(lambda y,pos: f"{y:,.0f}"))
        ax.set_ylabel("Lesion area (µm², log scale)");ax.set_title(title,loc="left",fontsize=10.5,fontweight="bold")
    cloud(axes[2],[(h,"none",points.loc[points.history.eq(h),"plot_P20_score"]) for h in COLORS],rng,"lesion")
    axes[2].axhline(3,color=".45",ls="--",lw=.8)
    axes[2].set_ylabel("P20 score read from Fig. 4j")
    axes[2].set_title("C   One section per history",loc="left",fontsize=10.5,fontweight="bold")
    fig.text(.076,.055,"In B, circles show vehicle and diamonds show T-5224. In C, the dashed line marks the published high-score threshold.",fontsize=8.5)
    save(fig,out,"lesion_areas_and_p20")
