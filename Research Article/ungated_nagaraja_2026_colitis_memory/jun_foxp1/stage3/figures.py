"""Gallery-style figures for the two prospective rank comparisons."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BLUE = "#23658a"
ORANGE = "#aa5422"
COLORS = {"AP1 only": BLUE, "AP1 + Fox": ORANGE}


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "pdf.fonttype": 42,
                         "text.color": "black", "axes.labelcolor": "black", "xtick.color": "black",
                         "ytick.color": "black", "axes.spines.top": False, "axes.spines.right": False})


def write(fig, out, name):
    for ext in ("pdf", "png"):
        fig.savefig(out / f"{name}.{ext}", dpi=200, facecolor="white")
    plt.close(fig)


def coef_axis(ax, count):
    ax.axvline(0, color="#999999", lw=.7, zorder=0)
    ax.set_xlim(-1.02, 1.02)
    ax.set_xticks([-1, -.5, 0, .5, 1])
    ax.set_ylim(count - .45, -.60)
    ax.set_xlabel("Rank correlation")


def binding_figure(results, points, ranges, out):
    style()
    fig, axes = plt.subplots(2, 2, figsize=(11.7, 8.0))
    fig.subplots_adjust(left=.11, bottom=.09, top=.95, right=.98, hspace=.48, wspace=.67)
    a, b, c, d = axes.flat
    dots = points[points.endpoint.eq("d102") & points.predictor.eq("increment")]
    for label, col in COLORS.items():
        g = dots[dots.motif_class.eq(label)]
        a.scatter(g.residual_x, g.residual_y, s=22, color=col, alpha=.8, edgecolor="none", label=label)
    a.axhline(0, color="#999999", lw=.6, zorder=0)
    a.axvline(0, color="#999999", lw=.6, zorder=0)
    a.set(xlabel="Binding increment (adjusted rank)", ylabel="Day-102 ΔCPM (adjusted rank)")
    a.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(.5,-.19))
    rr = results[results.check.eq("geometry_adjusted")]
    def rho(endpoint, predictor):
        return rr[rr.endpoint.eq(endpoint) & rr.predictor.eq(predictor)].rho.item()
    a.set_title(f"A   Primary day-102 association   ρ = {rho('d102','increment'):+.2f}", loc="left", fontweight="bold")
    checks = ["geometry_adjusted", "unadjusted", "within_class", "within_class", "control_only",
              "recovered_only", "coupled_control_adjustment", "per_kb"]
    groups = ["all","all","AP1 only","AP1 + Fox","all","all","all","all"]
    for off, day, color in [(-.13, "d102", BLUE), (.13, "d50", ORANGE)]:
        sub = results[results.endpoint.eq(day) & results.predictor.eq("increment")]
        vals = [sub[sub.check.eq(k) & sub.subgroup.eq(g)].rho.item() for k,g in zip(checks,groups)]
        b.scatter(vals, np.arange(len(vals)) + off, color=color, s=22, label="Day " + day[1:])
    coef_axis(b, len(checks))
    b.set_yticks(range(len(checks)), ["Adjusted", "Unadjusted", "AP1 only", "AP1 + Fox", "Control CPM",
                                     "Recovered CPM", "Control-adjusted", "Per kb"])
    b.set_title("B   Accessibility and baseline checks", loc="left", fontweight="bold")
    b.legend(frameon=False, loc="upper center", bbox_to_anchor=(.5,-.20), ncol=2)
    keys = ["P4_amplicon","P4_left_flank","P4_right_flank","vehicle_amplicon","vehicle_left_flank","vehicle_right_flank"]
    for i, (p, name, color, marker) in enumerate([("increment","Raw difference",BLUE,"o"),("fold_ratio","Paired fold",ORANGE,"D")]):
        vals = [rho(k,p) for k in keys]
        c.scatter(vals, np.arange(6) + (i-.5)*.26, color=color, marker=marker, s=23, label=name)
    coef_axis(c, 6)
    c.set_yticks(range(6), ["P4 full", "P4 left", "P4 right", "Tissue full", "Tissue left", "Tissue right"])
    c.set_title("C   Binding and regional methylation", loc="left", fontweight="bold")
    c.legend(frameon=False, loc="upper center", bbox_to_anchor=(.5,-.19), ncol=2)
    keys = ["d102", "d50", "P4_amplicon", "vehicle_amplicon"]
    for i,(typ,label,col) in enumerate([("locus","Omit one locus",BLUE),("mouse_or_line","Omit one mouse/line",ORANGE)]):
        for j,k in enumerate(keys):
            s = ranges[ranges.endpoint.eq(k) & ranges.predictor.eq("increment") & ranges.omission.eq(typ)].iloc[0]
            y = j + (i-.5)*.30
            d.plot([s.min_rho,s.max_rho],[y,y], color=col, lw=3, label=label if j==0 else None)
            d.scatter([s.full_rho],[y],s=16,color="black",zorder=3)
    coef_axis(d,4)
    d.set_yticks(range(4),["Day 102","Day 50","P4 full","Tissue full"])
    d.set_title("D   Sensitivity to omitted units",loc="left",fontweight="bold")
    d.legend(frameon=False, loc="upper center", bbox_to_anchor=(.5,-.19), ncol=2, fontsize=8)
    write(fig, out, "binding_associations")


def native_figure(results, ranges, out):
    style()
    fig, axes = plt.subplots(1, 2, figsize=(10.4,4.25), sharey=True)
    fig.subplots_adjust(left=.16, right=.98, top=.86, bottom=.23, wspace=.12)
    keys = ["P4_amplicon","P4_left_flank","P4_right_flank","vehicle_amplicon","vehicle_left_flank","vehicle_right_flank"]
    for ax,day in zip(axes,["d102","d50"]):
        sub = results[results.time.eq(day) & results.check.eq("geometry_adjusted")].set_index("methylation")
        for j,key in enumerate(keys):
            for i,(typ,label,col) in enumerate([("atac_mouse","Omit ATAC mouse",BLUE),
                                                 ("methylation_mouse_or_line","Omit methylation mouse/line",ORANGE)]):
                s = ranges[ranges.time.eq(day) & ranges.methylation.eq(key) & ranges.omission.eq(typ)].iloc[0]
                y=j+(i-.5)*.26
                ax.plot([s.min_rho,s.max_rho],[y,y],color=col,lw=3,label=label if j==0 else None)
                ax.scatter(sub.loc[key,"rho"],y,s=17,color="black",zorder=3)
        coef_axis(ax,6)
        ax.set_title("Day " + day[1:] + " epithelial accessibility",fontweight="bold",loc="left")
    axes[0].set_yticks(range(6),["P4 full (63)","P4 left (58)","P4 right (62)","Tissue full (63)","Tissue left (58)","Tissue right (62)"])
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="lower center",ncol=2,frameon=False)
    write(fig,out,"native_associations")
