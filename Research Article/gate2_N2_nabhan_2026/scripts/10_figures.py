"""Export scientific figures from recorded Nb3 outputs; no refitting or re-selection."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "figures"
TARGETS = ["NKX21", "BECN1", "KEAP1", "TRP53", "CDKN2B", "CTNNB1", "CSNK2A1", "ELOVL1", "ATP6V0E", "SLC34A2", "FZD5", "PORCN", "ERBB2", "ERBB3", "EGFR", "ERBB4"]
LABELS = {"AT2_figure3":"AT2", "transition_figure3":"Transition", "IFN_figure3":"Interferon", "hypoxia_figure3":"Hypoxia", "gastric_maintext":"Gastric", "Wnt_maintext":"Wnt (S7)", "AT1_maintext":"AT1 (S7)",
          "ID_figure4":"ID genes", "OXPHOS_figure4":"Mitochondrial ND", "Hippo_figure4":"Hippo markers", "wound_figure4":"Wound markers", "chemokines_figure4":"Chemokines", "PLIN2_sentinel":"PLIN2 sentinel"}
plt.rcParams.update({"font.size":10, "axes.spines.top":False, "axes.spines.right":False, "pdf.fonttype":42, "savefig.facecolor":"white"})

def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=170)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)

def main():
    if OUT.exists():
        raise SystemExit("Refusing to overwrite Nb3 figures")
    OUT.mkdir()
    data = pd.read_csv(HERE / "runs/R1_v1/imaging_effects.tsv",sep="\t")
    data = data[(data.variant == "all_wells_scaling") & (data.day == "day14")]
    fig,axes = plt.subplots(1,3,figsize=(12,7.8),sharey=True)
    for ax,endpoint,title in zip(axes,["organoids_count","organoids_area_mean","organoids_area_prop"],["Organoid count","Mean segmented size","Bounding-box coverage"]):
        d=data[data.endpoint == endpoint].set_index("target").reindex(TARGETS)
        ax.errorbar(d.effect,np.arange(len(TARGETS)),xerr=np.vstack([d.effect-d.ci_low,d.ci_high-d.effect]),fmt="o",markersize=4,color="#276482",elinewidth=1,capsize=2)
        ax.axvline(0,color="0.65",linewidth=.8)
        ax.set_title(title); ax.set_xlabel("Effect versus TIGIT\n(within-plate SD units)")
        ax.grid(axis="x",color="0.93")
    axes[0].set_yticks(np.arange(len(TARGETS)),TARGETS); axes[0].invert_yaxis()
    fig.suptitle("Nb3 | Day-14 imaging reconstruction",fontsize=15,y=.98)
    fig.text(.5,.015,"95% intervals describe technical wells. CTNNB1 is an activating edit; size is the deposited measurement scale.",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,.045,1,.95]); save(fig,"Nb3_R1_imaging")
    effects=pd.read_csv(HERE / "runs/R4_v1/fixed_panel_effects.tsv",sep="\t")
    fig,axes=plt.subplots(1,2,figsize=(12.5,8),gridspec_kw={"width_ratios":[7,6]})
    for species,ax in zip(["mouse","human"],axes):
        columns=[c for c in LABELS if c in set(effects.loc[effects.species==species,"program"])]
        matrix=effects[effects.species==species].pivot(index="target",columns="program",values="effect").reindex(index=TARGETS,columns=columns)
        limit=max(1.,float(np.nanmax(np.abs(matrix.to_numpy()))))
        im=ax.imshow(matrix,cmap="RdBu_r",vmin=-limit,vmax=limit,aspect="auto")
        ax.set_xticks(np.arange(len(columns)),[LABELS[c] for c in columns],rotation=40,ha="right")
        ax.set_yticks(np.arange(len(TARGETS)),TARGETS)
        ax.set_title("Mouse epithelial compartment" if species=="mouse" else "Human fibroblast compartment")
        fig.colorbar(im,ax=ax,shrink=.6,label="Mean log2(CPM + 0.5) contrast")
    fig.suptitle("Nb3 | Fixed source-marker panels",fontsize=15,y=.98)
    fig.text(.5,.015,"Against in-plate TIGIT + tdTomato; separate color scales. Marker summaries are not complete pathways or cell fractions.",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,.05,1,.94]); save(fig,"Nb3_R4_fixed_panels")
    ica=pd.read_csv(HERE / "runs/R3_v1/source_ICA_activities.tsv",sep="\t").set_index("target")
    matrix=ica.reindex(TARGETS)[["ICA_05","ICA_13","ICA_17"]]
    fig,ax=plt.subplots(figsize=(6.4,8.5))
    limit=float(np.nanmax(np.abs(matrix.to_numpy())))
    im=ax.imshow(matrix,cmap="RdBu_r",vmin=-limit,vmax=limit,aspect="auto")
    ax.set_xticks(range(3),["ICA 5","ICA 13","ICA 17"]); ax.set_yticks(range(len(TARGETS)),TARGETS)
    for i in range(len(matrix)):
        for j in range(3):
            v=matrix.iloc[i,j]
            if np.isfinite(v): ax.text(j,i,f"{v:.2f}",ha="center",va="center",fontsize=8,color="white" if abs(v)>.65*limit else "black")
    ax.set_title("Nb3 | Deposited component activities\nS6 reconstruction; no new ICA fit",pad=16)
    fig.colorbar(im,ax=ax,shrink=.65,label="Source activity (source sign retained)")
    fig.text(.5,.015,"Component signs are arbitrary; compare activities with the signed gene projections.",ha="center",fontsize=8)
    fig.tight_layout(rect=[0,.05,1,1]); save(fig,"Nb3_R3_source_ICA")
    effects["key"]=effects.species+"__"+effects.program
    wide=effects.pivot(index="target",columns="key",values="effect")
    growth=data[data.endpoint=="organoids_area_prop"].set_index("target").effect
    fig,axes=plt.subplots(1,2,figsize=(11,5.7),sharey=True)
    for ax,x,title in [(axes[0],growth,"Growth contrast"),(axes[1],wide["mouse__AT2_figure3"],"AT2 marker contrast")]:
        pair=pd.concat([x.rename("x"),wide["human__chemokines_figure4"].rename("y")],axis=1).dropna()
        ax.scatter(pair.x,pair.y,s=15,c="#acbac2",alpha=.65,linewidth=0)
        for target in ["NKX21","TRP53","BECN1","KEAP1"]:
            if target in pair.index:
                row=pair.loc[target]; ax.scatter(row.x,row.y,s=32,c="#9c3d10")
                ax.annotate(target,(row.x,row.y),xytext=(4,5),textcoords="offset points",fontsize=8)
        ax.axhline(0,color="0.8",linewidth=.8); ax.axvline(0,color="0.8",linewidth=.8)
        ax.set_title(title); ax.set_xlabel("Coverage effect (SD units)" if ax==axes[0] else "AT2 panel effect (mean log2 CPM units)")
    axes[0].set_ylabel("Fibroblast chemokine panel effect\n(mean log2 CPM units)")
    fig.suptitle("Nb3 E1/E8 | Paired target-associated contrasts",fontsize=14,y=.98)
    fig.text(.5,.02,"Each point is an eligible target. Associations do not identify an independent identity effect or immune recruitment.",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,.065,1,.94]); save(fig,"Nb3_E1_E8_associations")
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir())}
    (OUT/"manifest.json").write_text(json.dumps({"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"files":manifest},indent=2)+"\n")
    print("Exported four figures as PNG and PDF")

if __name__=="__main__":
    main()
