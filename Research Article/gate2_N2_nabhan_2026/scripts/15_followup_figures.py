"""Paper-style figures for frozen Nb3 follow-up diagnostics and enrichment."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
RUN = HERE / "runs/followup_v1"


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, default=HERE/"figures/followup_v1")
    out = parser.parse_args().output.resolve()
    if out.exists(): raise SystemExit("Refusing to overwrite follow-up figure package")
    (out/"source_data").mkdir(parents=True)
    palette_path = ROOT/"analysis/config/palette.json"
    p = json.loads(palette_path.read_text()); c = list(p["categorical"].values())
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":8, "axes.labelsize":8, "axes.titlesize":9,
        "xtick.labelsize":7, "ytick.labelsize":7, "legend.fontsize":7,
        "figure.facecolor":p["surface"], "axes.facecolor":p["surface"], "savefig.facecolor":p["surface"],
        "text.color":p["ink"], "axes.labelcolor":p["ink"], "axes.edgecolor":p["axis"],
        "xtick.color":p["ink_2"], "ytick.color":p["ink_2"], "axes.linewidth":.6,
        "axes.spines.top":False, "axes.spines.right":False, "pdf.fonttype":42, "svg.fonttype":"none",
        "svg.hashsalt":"Nb3-followup-v1", "figure.constrained_layout.use":True,
        "figure.constrained_layout.w_pad":.06, "figure.constrained_layout.h_pad":.085})
    inputs = {str(palette_path.relative_to(ROOT)).replace("\\", "/"):sha(palette_path)}
    def read(name):
        path=RUN/(name+".tsv"); inputs[path.relative_to(ROOT).as_posix()]=sha(path)
        return pd.read_csv(path, sep="\t")
    def data(name, d): d.to_csv(out/"source_data"/(name+".tsv"), sep="\t", index=False, float_format="%.12g", lineterminator="\n")
    def title(ax, letter, label): ax.set_title(f"{letter}   {label}", loc="left", fontsize=9, fontweight="bold", pad=9)
    def save(fig, name):
        for ext in ["png", "pdf", "svg"]:
            kw={"metadata":{"CreationDate":None,"ModDate":None}} if ext=="pdf" else {}
            fig.savefig(out/f"{name}.{ext}", dpi=300, **kw)
        plt.close(fig)
    s=read("panel_sensitivities"); depth=read("focal_depth_effects"); a=read("paired_depth_associations")
    fig,axes=plt.subplots(2,2,figsize=(7.2,7.4))
    all_plot=[]
    selections=[("NKX21",[("mouse","AT2_figure3","AT2"),("human","chemokines_figure4","Chemokines"),("human","wound_figure4","Wound")]),
                ("SLC34A2",[("mouse","transition_figure3","Transition"),("mouse","AT2_figure3","AT2"),("mouse","AT1_maintext","AT1")])]
    variants=[("combined","Both controls"),("TIGIT_only","TIGIT only"),("tdTomato_only","tdTomato only"),("omit_gene","Omit a gene"),("omit_target_well","Omit a well")]
    for j,(target,selection) in enumerate(selections):
        ax=axes[0,j]; ticks=[]; labels=[]
        for g,(species,program,label) in enumerate(selection):
            for k,(variant,vlab) in enumerate(variants):
                d=s[(s.target==target)&(s.species==species)&(s.program==program)&(s.variant==variant)&(s.status=="technical_descriptive")]
                assert len(d)>0
                y=g*6+k; ticks.append(y);labels.append(f"{label} · {vlab}" if k==0 else vlab)
                lo,hi=d.effect.min(),d.effect.max()
                color=c[0] if species=="mouse" else c[1]
                ax.plot([lo,hi],[y,y],color=color,lw=1.5)
                ax.scatter(d.effect, np.full(len(d),y),color=color,s=15 if k<3 else 8,marker="o",linewidth=0)
                all_plot.append(d)
        ax.set_yticks(ticks,labels);ax.set_ylim(17,-1);ax.axvline(0,color=p["muted"],lw=.7)
        ax.set_xlabel("Marker-panel contrast\n(points/ranges across specifications)")
        title(ax,"AB"[j],target+" sensitivity")
    data("F07_panel_sensitivities",pd.concat(all_plot))
    ax=axes[1,0];d=depth[depth.target=="NKX21"]
    data("F07_NKX21_depth",d)
    for j,species in enumerate(["mouse","human"]):
        for k,variant in enumerate(["paired_baseline","paired_depth"]):
            r=d[(d.species==species)&(d.variant==variant)].iloc[0];y=j*3+k
            ax.errorbar(r.effect,y,xerr=[[r.effect-r.ci_low],[r.ci_high-r.effect]],fmt="os"[k],color=c[j],ms=4,capsize=2,lw=.9)
    ax.set_yticks([0,1,3,4],["AT2 · paired","AT2 · +read depths","Chemokines · paired","Chemokines · +read depths"])
    ax.set_ylim(5,-1);ax.axvline(0,color=p["muted"],lw=.7)
    ax.set_xlabel("Contrast (95% technical interval)");title(ax,"C","NKX21 paired-depth sensitivity")
    ax=axes[1,1]
    for j,pop in enumerate(["common_estimable","common_without_NKX21"]):
        d=a[a.population==pop].set_index("variant").loc[["paired_baseline","paired_depth"]]
        ax.plot(d.spearman,[j,j],color=p["muted"],lw=.9)
        for k,r in enumerate(d.itertuples()):ax.scatter(r.spearman,j,color=c[k],marker="os"[k],s=25)
    data("F07_depth_associations",a)
    ax.set_yticks([0,1],["All common targets (195)","Without NKX21 (194)"]);ax.set_ylim(1.8,-.7);ax.set_xlim(0,.26)
    ax.set_xlabel("AT2–chemokine Spearman ρ")
    ax.legend(handles=[Line2D([0],[0],marker="o",color=c[0],linestyle="none",label="Paired baseline"),Line2D([0],[0],marker="s",color=c[1],linestyle="none",label="Both read depths")],frameon=False,loc="lower left")
    title(ax,"D","Cross-target association")
    fig.supxlabel("RNA contrasts: mean log$_2$(TMM CPM + 0.5) · A–B ranges are sensitivity ranges, not confidence intervals",fontsize=7)
    save(fig,"Nb3_F07_followup_sensitivity")

    h=read("hallmark_camera")
    joined=h[h.intergene_correlation==.01].merge(h[h.intergene_correlation==.05],on=["species","target","pathway"],suffixes=("_01","_05"),validate="one_to_one")
    spec_path=HERE/"config/Nb3_followup_v1.json";inputs[spec_path.relative_to(ROOT).as_posix()]=sha(spec_path)
    targets=json.loads(spec_path.read_text())["targets"]
    # A thematic view of the existing v1 questions, not a significance-selected set.
    short=[("INTERFERON_ALPHA_RESPONSE","IFN α"),("INTERFERON_GAMMA_RESPONSE","IFN γ"),("TNFA_SIGNALING_VIA_NFKB","TNF/NF-κB"),("INFLAMMATORY_RESPONSE","Inflammatory"),("HYPOXIA","Hypoxia"),("TGF_BETA_SIGNALING","TGF-β"),("WNT_BETA_CATENIN_SIGNALING","Wnt/β-catenin"),("EPITHELIAL_MESENCHYMAL_TRANSITION","EMT"),("E2F_TARGETS","E2F"),("G2M_CHECKPOINT","G2M"),("OXIDATIVE_PHOSPHORYLATION","OXPHOS"),("UNFOLDED_PROTEIN_RESPONSE","UPR")]
    selected=["HALLMARK_"+name for name,_ in short]
    fig=plt.figure(figsize=(7.2,7.2));grid=fig.add_gridspec(2,2,height_ratios=[1.3,1])
    for j,species in enumerate(["mouse","human"]):
        ax=fig.add_subplot(grid[0,j]);d=joined[(joined.species==species)&joined.pathway.isin(selected)]
        assert len(d)==len(targets)*len(selected)
        for row in d.itertuples():
            x=targets.index(row.target);y=selected.index(row.pathway)
            color=c[1] if row.Direction_01=="Up" else c[0]
            size=9+3*min(-np.log10(max(row.FDR_global_01,1e-30)),10)
            ax.scatter(x,y,s=size,facecolor=color if row.FDR_global_01<.05 else "none",edgecolor=color,linewidth=.5,alpha=1 if row.FDR_global_01<.05 else .5)
            if row.FDR_global_05<.05:ax.scatter(x,y,s=size+18,facecolor="none",edgecolor=p["ink"],linewidth=.7)
        ax.set_xticks(range(len(targets)),targets,rotation=90);ax.set_yticks(range(len(short)),[label for _,label in short] if j==0 else [])
        ax.set_xlim(-.6,len(targets)-.4);ax.set_ylim(len(short)-.4,-.6);ax.tick_params(length=0)
        title(ax,"AB"[j],"Mouse Hallmark context" if j==0 else "Human Hallmark context")
        data(f"F08_{species}_thematic",d)
    ax=fig.add_subplot(grid[1,0]);x=-np.log10(joined.FDR_global_01);y=-np.log10(joined.FDR_global_05)
    robust=(joined.FDR_global_01<.05)&(joined.FDR_global_05<.05)
    ax.scatter(x[~robust],y[~robust],s=8,color=p["muted"],alpha=.45,linewidth=0)
    ax.scatter(x[robust],y[robust],s=15,color=c[1],alpha=.8,linewidth=.3,edgecolor=p["ink"])
    ax.axvline(-np.log10(.05),color=p["muted"],ls="--",lw=.7);ax.axhline(-np.log10(.05),color=p["muted"],ls="--",lw=.7)
    ax.set_xlabel("−log$_{10}$(global q), correlation = 0.01");ax.set_ylabel("−log$_{10}$(global q), correlation = 0.05")
    title(ax,"C","Intergene-correlation sensitivity")
    data("F08_all_enrichment_comparisons",joined)
    ax=fig.add_subplot(grid[1,1]);ax.axis("off")
    handles=[Line2D([0],[0],marker="o",linestyle="none",color=c[1],label="Up-ranked"),Line2D([0],[0],marker="o",linestyle="none",color=c[0],label="Down-ranked"),Line2D([0],[0],marker="o",linestyle="none",color=p["muted"],markerfacecolor="none",label="Open: q ≥ 0.05 at 0.01"),Line2D([0],[0],marker="o",linestyle="none",color=p["ink"],markerfacecolor="none",markersize=9,label="Black ring: q < 0.05 at 0.05")]
    ax.legend(handles=handles,loc="upper left",frameon=False,handlelength=1)
    ax.text(.02,.47,"Size: −log₁₀(q) at 0.01, capped at 10\nFilled: q < 0.05 at correlation 0.01\n\n1,486 eligible tests per specification\n251 pass at 0.01; 6 pass at 0.05\nAll 50 sets retained in source tables",transform=ax.transAxes,va="top",fontsize=7,linespacing=1.6)
    fig.supxlabel("Rank-based cameraPR · BH across species × target × eligible set · exploratory RNA context",fontsize=7)
    save(fig,"Nb3_F08_hallmark_context")
    writer=PdfWriter()
    for path in sorted(out.glob("Nb3_F*.pdf")):
        r=PdfReader(path);assert len(r.pages)==1;writer.add_page(r.pages[0])
    with (out/"Nb3_followup_atlas.pdf").open("wb") as f:writer.write(f)
    record={"schema":"Nb3-followup-figures/v1","script_sha256":sha(Path(__file__)),"inputs":inputs,
        "display_selection":"F07: named v1 focal contrasts; F08: 12 v1-relevant Hallmark themes including null Wnt results, not selected by q. All 50 sets retained in complete tables.",
        "limits":"A-B sensitivity ranges are not CIs; depth may be downstream; fixed-correlation enrichment is exploratory and assumption-sensitive",
        "outputs":{p.relative_to(out).as_posix():sha(p) for p in sorted(out.rglob("*")) if p.is_file()}}
    (out/"render_record.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps({"figures":2,"output":str(out)}))


if __name__=="__main__":main()
