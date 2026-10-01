"""Render question-owned figures from frozen extension tables."""
import csv,datetime,hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
BLUE="#2166AC";ORANGE="#B35806";GRAY="#777777"
plt.rcParams.update({"font.family":"Arial","font.size":9,"axes.titlesize":10,"axes.labelsize":9,"xtick.labelsize":8,"ytick.labelsize":8,"axes.spines.top":False,"axes.spines.right":False,"pdf.fonttype":42,"svg.fonttype":"none","savefig.dpi":300})
def read(p):
 with p.open(encoding="utf-8") as f:return list(csv.DictReader(f,delimiter="\t"))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def panel(ax,letter,title):
 ax.set_title(title,loc="left",pad=12);ax.text(-.16,1.08,letter,transform=ax.transAxes,fontweight="bold",fontsize=12)
def save(fig,q,run,name,inputs):
 out=q/"figures"/run
 if out.exists():raise FileExistsError(out)
 out.mkdir(parents=True)
 for ext in ["png","pdf","svg"]:fig.savefig(out/(name+"."+ext),bbox_inches="tight",facecolor="white")
 plt.close(fig)
 record=dict(rendered_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in inputs+[Path(__file__)]],outputs=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in sorted(out.iterdir())])
 (q/"metadata"/run/"figure_record.json").write_text(json.dumps(record,indent=2)+"\n")
def main():
 q=ROOT/"RQ_Specified/A22_epithelial_identity_niche_response";run="identity_amount_v2";path=q/"tables"/run/"metrics.tsv"
 rows=[r for r in read(path) if r["endpoint"]=="chemokines_figure4"]
 fig,axes=plt.subplots(1,3,figsize=(11.2,3.5),layout="constrained")
 for i,mode in enumerate(["target_holdout","plate_shift"]):
  r=next(r for r in rows if (r["variant"],r["mode"],r["fold"])==("primary",mode,"pooled"))
  vv=[float(r[k]) for k in ["baseline_target_rmse","full_target_rmse"]]
  axes[0].plot([i-.12,i+.12],vv,color=GRAY,lw=1)
  for xx,vv,c in zip([i-.12,i+.12],vv,[BLUE,ORANGE]):axes[0].scatter(xx,vv,color=c,s=40,zorder=3)
 axes[0].plot([],[],"o",color=BLUE,label="Amount/depth proxies")
 axes[0].plot([],[],"o",color=ORANGE,label="Proxies + identity")
 axes[0].set_xticks([0,1],["Target holdout","Plate shift"]);axes[0].set_ylabel("Equal-target RMSE (panel-score units)");axes[0].set_ylim(0,1.3);axes[0].legend(frameon=False,fontsize=7,loc="lower left");panel(axes[0],"A","Absolute held-out error")
 for ax,mode,letter,title in [(axes[1],"target_holdout","B","Target-group sensitivity"),(axes[2],"plate_shift","C","Whole-plate sensitivity")]:
  folds=sorted({r["fold"] for r in rows if r["mode"]==mode and r["fold"]!="pooled"})
  for offset,variant,c,label in [(-.09,"primary",BLUE,"All targets"),(.09,"without_NKX21",ORANGE,"Without NKX21")]:
   vv=[100*float(next(r for r in rows if (r["variant"],r["mode"],r["fold"])==(variant,mode,f))["relative_target_mse_reduction"]) for f in folds]
   ax.scatter(np.arange(len(folds))+offset,vv,color=c,s=33,label=label,zorder=3)
  ax.axhline(0,color=GRAY,lw=.8);ax.set_xticks(range(len(folds)),[f.replace("plate","P") for f in folds]);ax.set_xlabel("Held-out fold" if mode=="target_holdout" else "Held-out plate");ax.set_ylabel("Error reduction with identity (%)");ax.legend(frameon=False,fontsize=7,loc="lower left");panel(ax,letter,title)
 fig.suptitle("A22 | Concurrent RNA–imaging diagnostics: 672 wells, 201 targets",fontsize=11)
 save(fig,q,run,"F1_identity_amount",[path,q/"config"/(run+".json")])
 q=ROOT/"RQ_Specified/A23_slc34a2_transition_homeostasis";run="transporter_context_v1";tab=q/"tables"/run
 summaries=read(tab/"summaries.tsv");diff=read(tab/"differences.tsv");assoc=read(tab/"associations.tsv")
 fig,axes=plt.subplots(1,3,figsize=(12,3.6),layout="constrained")
 genes=["SLC20A1","SLC20A2"]
 for off,lib,c,label in [(-.12,"GSM5970468",ORANGE,"PAM case (2,298 AT2 candidates)"),(.12,"GSM5970470",BLUE,"Control (185 AT2 candidates)")]:
  vv=[float(next(r for r in summaries if (r["library"],r["group"],r["gene"])==(lib,"AT2_candidate_primary",g))["mean_log1p_10k"]) for g in genes]
  axes[0].scatter(np.arange(2)+off,vv,color=c,s=45,label=label)
 axes[0].set_xticks([0,1],genes);axes[0].set_ylabel("Mean ln(1 + UMI per 10,000)");axes[0].set_ylim(0,.31);axes[0].legend(frameon=False,fontsize=6.5,loc="upper right");panel(axes[0],"A","Alternative-transporter RNA")
 groups=["AT2_candidate_primary","AT2_candidate_strict","published_AT2_all","published_AT2_primary","published_AT2_strict"]
 labels=["Candidate / primary","Candidate / strict","Published / all","Published / primary","Published / strict"]
 for off,g,c in [(-.09,"SLC20A1",BLUE),(.09,"SLC20A2",ORANGE)]:
  vv=[float(next(r for r in diff if (r["group"],r["gene"])==(group,g))["mean_log1p_difference"]) for group in groups]
  axes[1].scatter(vv,np.arange(5)+off,color=c,s=30,label=g)
 axes[1].axvline(0,color=GRAY,lw=.8);axes[1].set_yticks(range(5),labels);axes[1].invert_yaxis();axes[1].set_xlim(-.22,.015);axes[1].set_xlabel("PAM − control (mean log-normalized RNA)");axes[1].legend(frameon=False,fontsize=7,loc="lower right");panel(axes[1],"B","Selection sensitivity")
 pairs=[(g,m) for g in genes for m in ["KRT8","CLU"]]
 for off,lib,group,c,marker,label in [(-.18,"GSM5970468","AT2_candidate_primary",ORANGE,"o","PAM / candidate"),(-.06,"GSM5970468","published_AT2_all",ORANGE,"s","PAM / published"),(.06,"GSM5970470","AT2_candidate_primary",BLUE,"o","Control / candidate"),(.18,"GSM5970470","published_AT2_all",BLUE,"s","Control / published")]:
  vv=[float(next(r for r in assoc if (r["library"],r["group"],r["transporter"],r["state_marker"])==(lib,group,g,m))["partial_rank"]) for g,m in pairs]
  axes[2].scatter(vv,np.arange(4)+off,color=c,marker=marker,s=23,label=label)
 axes[2].axvline(0,color=GRAY,lw=.8);axes[2].set_yticks(range(4),[g+" / "+m for g,m in pairs]);axes[2].invert_yaxis();axes[2].set_xlim(-.20,.20);axes[2].set_xlabel("Depth-conditional rank correlation");axes[2].legend(frameon=False,fontsize=6.5,loc="lower right");axes[2].set_ylim(5,-.6);panel(axes[2],"C","Within-library associations")
 fig.suptitle("A23 | One PAM case and one control; RNA does not measure transport flux",fontsize=11)
 save(fig,q,run,"F5_transporter_context",[tab/(n+".tsv") for n in ["summaries","differences","associations"]]+[q/"config"/(run+".json")])
 print("Two figures rendered as PNG, PDF and SVG.")
if __name__=="__main__":main()
