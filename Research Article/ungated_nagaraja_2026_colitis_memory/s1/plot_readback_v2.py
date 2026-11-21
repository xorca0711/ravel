"""Render the S1 source tables in the paper's black-text, grayscale figure style."""
import csv
import json
import sys
from pathlib import Path

import pymupdf
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def draw_figure(out, mice, primary, motifs, genes):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"pdf.fonttype":42,"text.color":"black",
                         "axes.labelcolor":"black","axes.titlecolor":"black","xtick.color":"black",
                         "ytick.color":"black","legend.labelcolor":"black",
                         "axes.spines.top":False,"axes.spines.right":False})
    fig=plt.figure(figsize=(13.2,8.4),facecolor="white")
    fig.text(.045,.955,"Colonic epithelial recovery after colitis",fontsize=21,weight="bold",color="black")
    fig.text(.045,.917,"Nagaraja et al. 2026   /   Mouse colon   /   Figure 1 readback",fontsize=11,color="black")
    fig.text(.045,.85,"A   FOS protein in CD44-positive crypt cells",fontsize=14,weight="bold",color="black")
    fig.text(.045,.816,
             f"Early recovery minus control: {primary['recovered_minus_control_pp']:+.2f} percentage points"
             "  ·  3 mice per group",fontsize=10,color="black")
    ax=fig.add_axes([.342,.146,.193,.607])
    table=fig.add_axes([.045,.146,.29,.607])
    table.axis("off")
    ax.set_xlim(-4,102)
    ax.set_xticks([0,25,50,75,100])
    ax.set_xlabel("FOS⁺ cells among CD44⁺ cells (%)",fontsize=9)
    ax.set_yticks([])
    ax.spines[["left","bottom"]].set_visible(False)
    ax.tick_params(axis="x",length=0,labelsize=9)
    ax.grid(axis="x",color="#dedede",linewidth=.7)
    ax.set_axisbelow(True)
    for x,t in [(0,"Stage and protocol day"),(.64,"Mouse"),(.82,"Double⁺ / CD44⁺")]:
        table.text(x,1.025,t,transform=table.transAxes,fontsize=8.5,weight="bold",color="black")
    groups=list(dict.fromkeys(r["stage"] for r in mice))
    y=0
    for stage in groups:
        group=[r for r in mice if r["stage"]==stage]
        mid=y+(len(group)-1)/2
        day=group[0]["protocol_day"]
        stage_label=stage.replace("d recovery","-day recovery")
        table.text(0,mid-.16,f"{stage_label}  (n={len(group)})",fontsize=9.6,weight="bold",va="center",color="black")
        cycle=group[0]["withdrawal_cycle"]
        description=f"Protocol d{day}"
        if cycle:
            description+=f"  ·  +{group[0]['days_after_referenced_withdrawal']} d, cycle {cycle}"
        table.text(0,mid+.44,description,fontsize=8,va="center",color="black")
        for row in group:
            table.text(.68,y,str(row["replicate"]),fontsize=8.7,va="center",color="black")
            table.text(.83,y,f"{row['FOS_CD44_double_positive']} / {row['CD44_positive']}",
                       fontsize=8.8,va="center",color="black")
            marker = "s" if stage in ("Acute injury","Chronic injury") else "o"
            ax.scatter(row["percent_double_positive"],y,s=38,marker=marker,zorder=3,
                       facecolor="white" if stage=="Control" else "#4c4c4c",
                       edgecolor="black",linewidth=.8,clip_on=False)
            y+=1
        if stage!=groups[-1]:
            for panel in (ax,table):
                panel.axhline(y-.23,color="#e5e5e5",linewidth=.7)
        y+=.55
    for panel in (ax,table):
        panel.set_ylim(y-.8,-.7)
    table.set_xlim(0,1)
    fig.text(.045,.078,"Each mark is one mouse. Counts are FOS⁺CD44⁺ / CD44⁺.",color="black",fontsize=9)
    fig.text(.045,.050,"+d gives days since the indicated DSS cycle ended. No mouse is followed across stages.",
             color="black",fontsize=8.5)

    fig.text(.608,.85,"B   Fos-family motif accessibility",fontsize=14,weight="bold",color="black")
    fig.text(.608,.816,"Deposited stage mean minus control mean (chromVAR score)",fontsize=9.7,color="black")
    states=["stem_prog","AE_inter","AE_diff"]
    stages=["Colitis_acute","Colitis_chronic","Colitis_recovered"]
    source={(r["epithelial_state"],r["stage"]):r["delta"] for r in motifs}
    values=[[source[k,s] for s in stages] for k in states]
    limit=max(abs(v) for line in values for v in line) or 1.
    cmap=LinearSegmentedColormap.from_list("positive_delta",["#ffffff","#d6d6d6","#a9a9a9"])
    heat=fig.add_axes([.726,.598,.238,.163])
    heat.imshow(values,aspect="auto",cmap=cmap,vmin=0,vmax=limit)
    heat.set_xticks(range(3),["Acute","Chronic","Early recovery"],fontsize=8.5)
    heat.xaxis.tick_top()
    heat.set_yticks(range(3),["Stem/progenitor","Intermediate AE","Differentiated AE"],fontsize=9)
    heat.tick_params(length=0,pad=6)
    heat.spines[:].set_visible(False)
    for i,r in enumerate(values):
        for j,value in enumerate(r):
            heat.text(j,i,f"{value:+.2f}",ha="center",va="center",fontsize=11,weight="bold",
                      color="black")
    fig.text(.608,.56,"AE = absorptive enterocyte. The deltas use mean scores across mice.",fontsize=8.5)
    fig.text(.608,.533,"Sequencing cohorts for B and C: 9 control, 4 acute, 5 chronic, 5 recovered mice.",fontsize=8.3)

    fig.text(.608,.463,"C   Transcription in stem cells",fontsize=14,weight="bold",color="black")
    fig.text(.608,.427,f"Genes meeting the upregulation threshold within the {genes[0]['injury_union']}-gene injury union",
             fontsize=9.4,color="black")
    bars=fig.add_axes([.705,.20,.205,.16])
    bars.barh([2,1,0],[r["union_up"] for r in genes],height=.4,color="#bcbcbc",edgecolor="#222222",linewidth=.7)
    bars.set_yticks([2,1,0],["Acute","Chronic","Early recovery"],fontsize=9)
    bars.set_xlim(0,genes[0]["injury_union"])
    bars.set_xticks([0,50,100,150,200,250])
    for h,r in zip([2,1,0],genes):
        bars.text(r["union_up"]+genes[0]["injury_union"]*.025,h,str(r["union_up"]),va="center",fontsize=10,color="black")
    bars.set_xlabel("Upregulated genes",fontsize=9)
    bars.spines[["left","bottom"]].set_visible(False)
    bars.tick_params(length=0)
    bars.grid(axis="x",linewidth=.65,color="#e5e5e5")
    bars.set_axisbelow(True)
    fig.text(.608,.103,"Released Table 1 calls: adjusted P < 0.05 and positive log₂ fold change.",fontsize=8.3,color="black")
    recovered = genes[-1]
    fig.text(.608,.078,f"Recovery: {recovered['union_unavailable_padj']} union genes lack adjusted P; "
             f"{recovered['union_absent']} are absent.",fontsize=8.5)
    fig.savefig(out/"fig1_recovery_v2.png",dpi=170)
    fig.savefig(out/"fig1_recovery_v2.pdf",metadata={"CreationDate":None,"ModDate":None})
    plt.close(fig)


def read_table(source, name):
    with (source/name).open(encoding="utf-8",newline="") as handle:
        return list(csv.DictReader(handle,delimiter="\t"))


def verify_render(out):
    with pymupdf.open(out/"fig1_recovery_v2.pdf") as document:
        assert len(document)==1
        page=document[0]
        spans=[s for b in page.get_text("dict")["blocks"] for line in b.get("lines",[]) for s in line["spans"]]
        families={s["font"] for s in spans}
        assert families and all(f.startswith("DejaVuSans") for f in families), families
        assert all(s["color"]==0 for s in spans)
        assert all(page.rect.contains(pymupdf.Rect(s["bbox"])) for s in spans)
        assert all(s["size"]>=7.9 for s in spans)
        result={"fonts":sorted(families),"text_spans":len(spans),"all_text_black":True,
                "all_text_on_page":True,"minimum_text_pt":min(s["size"] for s in spans)}
    (out/"render_checks.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    source=Path("analysis/research/runs/ng26_s1_v1")
    out=Path(sys.argv[1])
    mice=read_table(source,"fos_mice.tsv")
    for row in mice:
        row["percent_double_positive"]=float(row["percent_double_positive"])
        if row["withdrawal_cycle"]=="NA":
            row["withdrawal_cycle"]=None
    primary=read_table(source,"fos_primary.tsv")[0]
    primary["recovered_minus_control_pp"]=float(primary["recovered_minus_control_pp"])
    motifs=read_table(source,"fos_motif_by_state.tsv")
    for row in motifs:
        row["delta"]=float(row["delta"])
    genes=read_table(source,"rna_stages.tsv")
    for row in genes:
        for k in ("injury_union","union_up"):
            row[k]=int(row[k])
    draw_figure(out,mice,primary,motifs,genes)
    verify_render(out)
