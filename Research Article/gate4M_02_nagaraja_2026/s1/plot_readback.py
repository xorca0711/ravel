"""Display measured staining and two deposited molecular summaries on distinct axes."""
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def draw_figure(out, mice, primary, motifs, genes):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"pdf.fonttype":42,
                         "axes.spines.top":False,"axes.spines.right":False})
    fig=plt.figure(figsize=(13.2,8.4),facecolor="white")
    ink, muted, teal = "#182d36","#475a62","#09645d"
    fig.text(.045,.955,"Colonic epithelial recovery after colitis",fontsize=21,weight="bold",color=ink)
    fig.text(.045,.917,"Nagaraja et al. 2026   /   Mouse colon   /   Figure 1 readback",fontsize=11,color=muted)
    fig.text(.045,.85,"A   FOS protein in CD44-positive crypt cells",fontsize=14,weight="bold",color=ink)
    fig.text(.045,.816,
             f"Early recovery minus control: {primary['recovered_minus_control_pp']:+.2f} percentage points"
             "  ·  3 mice per group",fontsize=10,color=teal)
    ax=fig.add_axes([.342,.146,.193,.607])
    table=fig.add_axes([.045,.146,.29,.607])
    table.axis("off")
    ax.set_xlim(-4,102)
    ax.set_xticks([0,25,50,75,100])
    ax.set_xlabel("FOS⁺ cells among CD44⁺ cells (%)",fontsize=9)
    ax.set_yticks([])
    ax.spines[["left","bottom"]].set_visible(False)
    ax.tick_params(axis="x",length=0,labelsize=9)
    ax.grid(axis="x",color="#dae2e2",linewidth=.7)
    ax.set_axisbelow(True)
    for x,t in [(0,"Stage and protocol day"),(.64,"Mouse"),(.82,"FOS⁺ / CD44⁺")]:
        table.text(x,1.025,t,transform=table.transAxes,fontsize=8.5,weight="bold",color=muted)
    groups=list(dict.fromkeys(r["stage"] for r in mice))
    y=0
    for stage in groups:
        group=[r for r in mice if r["stage"]==stage]
        mid=y+(len(group)-1)/2
        day=group[0]["protocol_day"]
        stage_label=stage.replace("d recovery","-day recovery")
        table.text(0,mid-.16,f"{stage_label}  (n={len(group)})",fontsize=9.6,weight="bold",va="center",color=ink)
        cycle=group[0]["withdrawal_cycle"]
        description=f"Protocol d{day}"
        if cycle:
            description+=f"  ·  +{group[0]['days_after_referenced_withdrawal']} d, cycle {cycle}"
        table.text(0,mid+.44,description,fontsize=8,va="center",color=muted)
        for row in group:
            table.text(.68,y,str(row["replicate"]),fontsize=8.7,va="center",color=muted)
            table.text(.83,y,f"{row['FOS_CD44_double_positive']} / {row['CD44_positive']}",
                       fontsize=8.8,va="center",color=ink)
            ax.scatter(row["percent_double_positive"],y,s=41,color=teal,zorder=3,
                       edgecolor="white",linewidth=.6,clip_on=False)
            y+=1
        if stage!=groups[-1]:
            for panel in (ax,table):
                panel.axhline(y-.23,color="#e3e9e9",linewidth=.7)
        y+=.55
    for panel in (ax,table):
        panel.set_ylim(y-.8,-.7)
    table.set_xlim(0,1)
    fig.text(.045,.077,"Each dot is one mouse. +d gives days since the indicated DSS cycle ended.",color=muted,fontsize=8.5)

    fig.text(.608,.85,"B   Fos-family motif accessibility",fontsize=14,weight="bold",color=ink)
    fig.text(.608,.816,"Deposited stage mean minus control mean (chromVAR score)",fontsize=9.7,color=muted)
    states=["stem_prog","AE_inter","AE_diff"]
    stages=["Colitis_acute","Colitis_chronic","Colitis_recovered"]
    source={(r["epithelial_state"],r["stage"]):r["delta"] for r in motifs}
    values=[[source[k,s] for s in stages] for k in states]
    limit=max(abs(v) for line in values for v in line) or 1.
    cmap=LinearSegmentedColormap.from_list("signed",["#9b442d","#f7f7f1","#246c72"])
    heat=fig.add_axes([.726,.598,.238,.163])
    heat.imshow(values,aspect="auto",cmap=cmap,vmin=-limit,vmax=limit)
    heat.set_xticks(range(3),["Acute","Chronic","Early recovery"],fontsize=8.5)
    heat.xaxis.tick_top()
    heat.set_yticks(range(3),["Stem/progenitor","Intermediate AE","Differentiated AE"],fontsize=9)
    heat.tick_params(length=0,pad=6)
    heat.spines[:].set_visible(False)
    for i,r in enumerate(values):
        for j,value in enumerate(r):
            heat.text(j,i,f"{value:+.2f}",ha="center",va="center",fontsize=11,weight="bold",
                      color="white" if abs(value)>.66*limit else ink)
    fig.text(.608,.56,"AE = absorptive enterocyte. One entry per stage and state.",fontsize=8.5,color=muted)

    fig.text(.608,.463,"C   Transcription in stem cells",fontsize=14,weight="bold",color=ink)
    fig.text(.608,.427,f"Genes meeting the upregulation threshold within the {genes[0]['injury_union']}-gene injury union",
             fontsize=9.4,color=muted)
    bars=fig.add_axes([.705,.20,.205,.16])
    bars.barh([2,1,0],[r["union_up"] for r in genes],height=.4,color=["#737585","#737585",teal])
    bars.set_yticks([2,1,0],["Acute","Chronic","Early recovery"],fontsize=9)
    bars.set_xlim(0,genes[0]["injury_union"])
    for h,r in zip([2,1,0],genes):
        bars.text(r["union_up"]+genes[0]["injury_union"]*.025,h,str(r["union_up"]),va="center",fontsize=10,color=ink)
    bars.set_xlabel("Upregulated genes",fontsize=9)
    bars.spines[["left","bottom"]].set_visible(False)
    bars.tick_params(length=0)
    bars.grid(axis="x",linewidth=.65,color="#e3e9e9")
    bars.set_axisbelow(True)
    fig.text(.608,.103,"Released Table 1 calls: adjusted P < 0.05 and positive log₂ fold change.",fontsize=8.3,color=muted)
    fig.text(.608,.079,"Gene coverage and unavailable adjusted P values vary by stage.",fontsize=8.3,color=muted)
    fig.savefig(out/"fig1_recovery.png",dpi=170)
    fig.savefig(out/"fig1_recovery.pdf",metadata={"CreationDate":None,"ModDate":None})
    plt.close(fig)
