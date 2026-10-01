"""Shorten a clipped S3 title, preserving every numerical value and prior export."""
from pathlib import Path
import hashlib
import json
import importlib.util
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from pypdf import PdfReader, PdfWriter

HERE=Path(__file__).resolve().parents[1]; ROOT=HERE.parents[1]
OUT=HERE/"figures/publication_v1/S03_layout_v2"


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    if OUT.exists():raise SystemExit("Refusing to overwrite S03 layout revision")
    OUT.mkdir()
    spec=importlib.util.spec_from_file_location("nb3_base", HERE/"scripts/13_publication_figures.py")
    base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    palette=ROOT/"analysis/config/palette.json";p=json.loads(palette.read_text());c=list(p["categorical"].values())
    base.P=p;base.DIV=LinearSegmentedColormap.from_list("repo_signed",[c[0],p["surface"],c[1]])
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8,"axes.labelsize":8,"xtick.labelsize":7,"ytick.labelsize":7,"legend.fontsize":7,
        "figure.facecolor":p["surface"],"axes.facecolor":p["surface"],"savefig.facecolor":p["surface"],"text.color":p["ink"],"axes.labelcolor":p["ink"],
        "xtick.color":p["ink_2"],"ytick.color":p["ink_2"],"axes.edgecolor":p["axis"],"axes.linewidth":.6,"axes.spines.top":False,"axes.spines.right":False,
        "pdf.fonttype":42,"svg.fonttype":"none","svg.hashsalt":"Nb3-S03-v2","figure.constrained_layout.use":True,
        "figure.constrained_layout.w_pad":.065,"figure.constrained_layout.h_pad":.085})
    paths=[HERE/"figures/publication_v1/source_data"/name for name in ["S03_depth_diagnostics.tsv","S03_leave_target_out.tsv","S03_associations.tsv"]]
    depth,loo,assoc=[pd.read_csv(x,sep="\t") for x in paths]
    parts=[]
    for species in ["mouse","human"]:
        d=depth[depth.depth_species==species].set_index("key")
        parts.append(d[["spearman","plate_residual_spearman"]].rename(columns={"spearman":species+" raw","plate_residual_spearman":species+" residual"}))
    mat=pd.concat(parts,axis=1).loc[["mouse__"+x for x in base.MOUSE]+["human__"+x for x in base.HUMAN]]
    mat.index=["M · "+base.LABEL[x] for x in base.MOUSE]+["H · "+base.LABEL[x] for x in base.HUMAN]
    fig,axes=plt.subplots(1,2,figsize=(7.2,5.4),gridspec_kw={"width_ratios":[1.25,1]})
    im=base.heat(axes[0],mat,1,decimals=2,labels=["Mouse\nraw","Mouse\nresidual","Human\nraw","Human\nresidual"])
    base.title(axes[0],"A","Control score–depth associations")
    axes[0].set_xlabel("Read-depth compartment and adjustment")
    fig.colorbar(im,ax=axes[0],location="bottom",pad=.04,aspect=30,label="Spearman ρ · 99 paired control wells")
    ax=axes[1]
    for j,left in enumerate(["mouse__AT2_figure3","growth_coverage"]):
        a=assoc[assoc.left==left].iloc[0];d=loo[loo.left==left];y=3*j
        ax.scatter([a.spearman],[y],color=c[0],s=24,marker="o")
        if pd.notna(a.growth_residual_spearman):ax.scatter([a.growth_residual_spearman],[y+.6],color=c[1],s=24,marker="s")
        ax.scatter(d.spearman,np.full(len(d),y+1.2),s=16,marker="|",color=p["muted"])
        r=d[d.omitted=="NKX21"].iloc[0];ax.scatter([r.spearman],[y+1.2],s=30,facecolor="none",edgecolor=p["ink"],zorder=4)
    ax.set_yticks([0,.6,1.2,3,4.2],["AT2 · raw","AT2 · growth residual","AT2 · omit one","Coverage · raw","Coverage · omit one"])
    ax.set_ylim(5.4,-.7);ax.set_xlim(0,.28);ax.set_xlabel("Spearman ρ with chemokine contrast")
    ax.legend(handles=[Line2D([0],[0],marker="|",linestyle="none",color=p["muted"],label="16 focal omissions"),Line2D([0],[0],marker="o",linestyle="none",markerfacecolor="none",color=p["ink"],label="Omit NKX21")],frameon=False,loc="lower left")
    base.title(ax,"B","Target influence")
    fig.supxlabel("M: mouse marker panel; H: human marker panel · residual correlations do not identify causality",fontsize=7)
    for ext in ["png","pdf","svg"]:
        kwargs={"metadata":{"CreationDate":None,"ModDate":None}} if ext=="pdf" else {}
        fig.savefig(OUT/f"Nb3_S03_depth_and_influence.{ext}",dpi=300,**kwargs)
    # Check title bounding boxes against the saved page width after final layout.
    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    for axis in axes:
        bbox=axis._left_title.get_window_extent(renderer)
        assert bbox.x0>=0 and bbox.x1<=fig.bbox.width
    plt.close(fig)
    figures=sorted(list((HERE/"figures/publication_v1").glob("Nb3_F0[1-8]*.pdf"))+list((HERE/"figures/followup_v1").glob("Nb3_F0[1-8]*.pdf"))+list((HERE/"figures/publication_v1").glob("Nb3_S0[12]*.pdf"))+[OUT/"Nb3_S03_depth_and_influence.pdf"],key=lambda p:p.stem)
    assert len(figures)==11
    writer=PdfWriter()
    for f in figures:writer.add_page(PdfReader(f).pages[0])
    writer.add_metadata({"/Title":"Nb3 complete figures (S03 title layout corrected)","/Author":"Nb3 analysis"})
    atlas=HERE/"figures/Nb3_complete_figure_atlas_v2.pdf"
    assert not atlas.exists()
    with atlas.open("wb") as handle:writer.write(handle)
    record={"change":"Shortened S03 titles after full-page PDF inspection found right-edge clipping. No numerical, axis, selection or inference change; prior exports and initial atlas retained.",
        "implementation_history":"Initial atlas-selection assertion stopped before writing the atlas/record: Windows case-insensitive glob also selected atlas PDFs. Restricted to numbered figure names; draft exports preserved in ignored tmp.",
        "script_sha256":sha(Path(__file__)),"helper_sha256":sha(HERE/"scripts/13_publication_figures.py"),"palette_sha256":sha(palette),
        "source_data":{p.relative_to(HERE).as_posix():sha(p) for p in paths},"title_bounds":"PASS", "atlas_pages":len(PdfReader(atlas).pages),
        "outputs":{p.relative_to(HERE).as_posix():sha(p) for p in list(OUT.glob("Nb3_*"))+[atlas]},
        "atlas_input_PDFs":{p.relative_to(HERE).as_posix():sha(p) for p in figures}}
    (OUT/"layout_revision.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps({"title_bounds":"PASS","atlas_pages":11}))


if __name__=="__main__":main()
