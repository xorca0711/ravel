"""Resolve annotation overlap found during visual QA; preserve the initial export."""
from pathlib import Path
import hashlib
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parents[1]
OUT=HERE/"figures"

def main():
    stem="Nb3_E1_E8_associations_v2"
    if (OUT/f"{stem}.png").exists(): raise SystemExit("Refusing to overwrite revised figure")
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"pdf.fonttype":42,"savefig.facecolor":"white"})
    effects=pd.read_csv(HERE/"runs/R4_v1/fixed_panel_effects.tsv",sep="\t")
    effects["key"]=effects.species+"__"+effects.program
    wide=effects.pivot(index="target",columns="key",values="effect")
    imaging=pd.read_csv(HERE/"runs/R1_v1/imaging_effects.tsv",sep="\t")
    growth=imaging[(imaging.variant=="all_wells_scaling")&(imaging.day=="day14")&(imaging.endpoint=="organoids_area_prop")].set_index("target").effect
    fig,axes=plt.subplots(1,2,figsize=(11,5.7),sharey=True)
    offsets=[{"NKX21":(-5,9,"right"),"TRP53":(-5,13,"right"),"BECN1":(7,-15,"left"),"KEAP1":(5,-15,"left")},
             {"NKX21":(5,9,"left"),"TRP53":(-5,13,"right"),"BECN1":(7,8,"left"),"KEAP1":(5,-15,"left")}]
    for i,(ax,x,title) in enumerate([(axes[0],growth,"Growth contrast"),(axes[1],wide["mouse__AT2_figure3"],"AT2 marker contrast")]):
        pair=pd.concat([x.rename("x"),wide["human__chemokines_figure4"].rename("y")],axis=1).dropna()
        ax.scatter(pair.x,pair.y,s=15,c="#acbac2",alpha=.65,linewidth=0)
        for target,(dx,dy,align) in offsets[i].items():
            row=pair.loc[target]; ax.scatter(row.x,row.y,s=32,c="#9c3d10")
            ax.annotate(target,(row.x,row.y),xytext=(dx,dy),textcoords="offset points",fontsize=8,ha=align,
                        arrowprops={"arrowstyle":"-","color":"0.6","linewidth":.5})
        ax.axhline(0,color="0.8",linewidth=.8); ax.axvline(0,color="0.8",linewidth=.8)
        ax.set_title(title); ax.set_xlabel("Coverage effect (SD units)" if i==0 else "AT2 panel effect (mean log2 CPM units)")
    axes[0].set_ylabel("Fibroblast chemokine panel effect\n(mean log2 CPM units)")
    fig.suptitle("Nb3 E1/E8 | Paired target-associated contrasts",fontsize=14,y=.98)
    fig.text(.5,.02,"Each point is an eligible target. Associations do not identify an independent identity effect or immune recruitment.",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,.065,1,.94])
    fig.savefig(OUT/f"{stem}.png",dpi=170); fig.savefig(OUT/f"{stem}.pdf"); plt.close(fig)
    record={"reason":"Visual QA found overlapping TRP53/BECN1 annotations; fixed label offsets only, no new selection or fitting",
      "initial_version_preserved":True,"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "files":{f"{stem}.{suffix}":hashlib.sha256((OUT/f"{stem}.{suffix}").read_bytes()).hexdigest() for suffix in ("png","pdf")}}
    (OUT/"layout_revision.json").write_text(json.dumps(record,indent=2)+"\n")
    print("Revised association labels; initial figure and numerical outputs preserved")

if __name__=="__main__": main()
