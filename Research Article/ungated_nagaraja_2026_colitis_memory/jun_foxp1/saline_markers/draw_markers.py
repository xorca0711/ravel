"""Display the frozen eight-site screen from saved tables only."""
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymupdf


SOURCE = Path("analysis/research/runs/ng26_saline_markers_v1")
STYLE = {"GSE283386": ("#25668a", "o"), "GSE316762": ("#a45325", "D")}


def read(name):
    return pd.read_csv(SOURCE / name, sep="\t")


def main(out):
    m, g, p = (read(n) for n in ("mouse_values.tsv", "study_differences.tsv", "site_comparison.tsv"))
    assert (len(m), len(g), len(p)) == (96, 16, 8)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "pdf.fonttype": 42,
                         "text.color": "black", "axes.labelcolor": "black", "xtick.color": "black",
                         "ytick.color": "black", "axes.spines.top": False, "axes.spines.right": False})
    fig = plt.figure(figsize=(14, 7.2))
    grid = fig.add_gridspec(1, 5, width_ratios=[2.9,2.05,2.05,2.6,1.85],
                            left=.025, right=.977, top=.84, bottom=.19, wspace=.18)
    names, ext, native, effect, screen = [fig.add_subplot(grid[0,i]) for i in range(5)]
    names.set_title("Fragment and probe", loc="left", fontweight="bold")
    screen.set_title("Direction across cohorts", loc="left", fontweight="bold")
    names.set_axis_off()
    screen.set_axis_off()
    pos = {}
    row = 0.
    for fragment, subset in p.groupby("locus", sort=False):
        names.text(0,row,fragment,fontsize=9,fontweight="bold",va="center")
        row += .63
        for item in subset.itertuples():
            pos[item.probe] = row
            flank = "L" if item.flank=="left_flank" else "R"
            names.text(.045,row,f"{item.probe}   {flank}",fontsize=8.5,va="center")
            label = {"joint decrease, stable":"Joint loss · stable", "joint increase, stable":"Joint gain · stable",
                     "joint decrease, omission-sensitive":"Joint loss · sensitive",
                     "joint increase, omission-sensitive":"Joint gain · sensitive",
                     "opposite directions":"Opposite directions"}.get(item.directional_screen,item.directional_screen)
            screen.text(0,row,label,va="center",fontsize=8.5)
            row += .97
        row += .32
    for ax in (names,ext,native,effect,screen):
        ax.set_ylim(row-.85,-.62)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
    for ax,study,title in [(ext,"GSE283386","A   Day 14 · epithelium"),(native,"GSE316762","B   Day 23 · whole colon")]:
        ax.set_title(title,loc="left",fontweight="bold")
        color,_ = STYLE[study]
        for item in g[g.study.eq(study)].itertuples():
            sub=m[m.probe.eq(item.probe) & m.study.eq(study)]
            for arm,shift,mean in [("control",-.18,item.control_mean_percent),("DSS",.18,item.DSS_mean_percent)]:
                hit=sub[sub.arm.str.contains("water|Control",regex=True)] if arm=="control" else sub[sub.arm.str.contains("DSS|Recovered",regex=True)]
                assert len(hit)==3
                cy=pos[item.probe]+shift
                ax.plot([mean,mean],[cy-.105,cy+.105],color="black",lw=1.15,zorder=4)
                ax.scatter(hit.methylation_percent,cy+np.array([-.067,0,.067]),s=23,
                           facecolor="white" if arm=="control" else color,edgecolor=color,lw=.9,zorder=3)
        ax.set_xlim(-4,104)
        ax.set_xticks([0,25,50,75,100])
        ax.set_xlabel("Methylation (%)")
        ax.grid(axis="x",lw=.5,color="#dedede")
    effect.set_title("C   DSS − control",loc="left",fontweight="bold")
    for s in g.itertuples():
        color,marker=STYLE[s.study]
        y=pos[s.probe]+(-.15 if s.study=="GSE283386" else .15)
        effect.plot([s.omission_min_pp,s.omission_max_pp],[y,y],color=color,lw=2)
        effect.scatter(s.delta_pp,y,s=25,marker=marker,color=color,edgecolor="black",lw=.35,zorder=3)
    effect.axvline(0,color="#686868",lw=.8,zorder=0)
    effect.set_xlabel("Difference (percentage points)")
    effect.margins(x=.10)
    fig.text(.025,.969,"Methylation after DSS at eight flanking CpGs",fontsize=16,fontweight="bold",va="top")
    fig.text(.025,.924,"Three DSS-history mice and three controls in each cohort. Sites are grouped by their original mm10 fragment.",fontsize=10)
    fig.text(.025,.105,"A–B   Each point is one mouse. Open circles show controls, filled circles show DSS history, and black ticks mark arm means. L and R indicate flanks.",fontsize=9)
    fig.text(.025,.065,"C   Blue circles show day 14; orange diamonds show day 23. Lines span all six one-mouse omissions. Stable direction requires every omission in both cohorts to preserve the sign.",fontsize=9)
    for suffix in ("pdf","png"):
        fig.savefig(out/f"saline_markers.{suffix}",dpi=300,bbox_inches="tight",pad_inches=.20,facecolor="white")
    plt.close(fig)
    with pymupdf.open(out/"saline_markers.pdf") as doc:
        page=doc[0]
        spans=[s for b in page.get_text("dict")["blocks"] if b["type"]==0 for l in b["lines"] for s in l["spans"]]
        fonts=sorted({s["font"] for s in spans})
        assert all(s["color"]==0 and page.rect.contains(pymupdf.Rect(s["bbox"])) for s in spans)
        assert fonts==["DejaVuSans","DejaVuSans-Bold"] and all(probe in page.get_text() for probe in p.probe)
        checks=dict(all_eight_probe_labels=True,visible_text_black=True,all_text_inside_page=True,fonts=fonts,
                    pages=len(doc),mouse_points=len(m),study_site_differences=len(g))
    (out/"render_checks.json").write_text(json.dumps(checks,indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    main(Path(sys.argv[1]))
