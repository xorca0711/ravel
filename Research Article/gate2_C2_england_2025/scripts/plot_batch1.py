"""Plot completed England measurements using the repository palette."""
import argparse,sys,json,hashlib
from pathlib import Path
pa=argparse.ArgumentParser();pa.add_argument('--data-root',type=Path,required=True);a=pa.parse_args();sys.path.insert(0,str(a.data_root/'.venv-x64/Lib/site-packages'))
import numpy as np
import pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,LogNorm
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1];B=HERE/'trials/batch1';OUT=B/'figures';OUT.mkdir(exist_ok=True)
pal=json.loads((ROOT/'analysis/config/palette.json').read_text());cs=list(pal['categorical'].values());cm=LinearSegmentedColormap.from_list('repo_seq',pal['sequential_ramp'])
plt.rcParams.update({'figure.facecolor':pal['surface'],'axes.facecolor':pal['surface'],'text.color':pal['ink'],'axes.labelcolor':pal['ink'],'xtick.color':pal['ink_2'],'ytick.color':pal['ink_2'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':pal['surface']})
saved=[]
def save(fig,name):
 fig.savefig(OUT/name,dpi=170,bbox_inches='tight');plt.close(fig);saved.append(name)
d=pd.read_csv(B/'rna/library_contrasts.csv');d=d[(d.experiment==2)&(d.group=='all_QC')]
ends=['AT2_identity','transition_RNA','Cd177_associated','AT1_identity','TNFA_NFKB_RNA_disjoint','Nfkbia','Tonsl','cycling'];labels=['AT2 identity','Transition RNA','Cd177-associated RNA','AT1 identity','TNF/NF-kB-associated RNA','Nfkbia','Tonsl','Cycling RNA']
fig,axes=plt.subplots(2,4,figsize=(16,8.5))
for ax,end,label in zip(axes.ravel(),ends,labels):
 for j,(day,var) in enumerate([(14,'raw'),(14,'depth1000_seed20260927'),(84,'raw'),(84,'depth1000_seed20260927')]):
  r=d[(d.collection_day==day)&(d.variant==var)&(d.endpoint==end)].iloc[0];color=cs[0 if var=='raw' else 1]
  ax.hlines(3-j,r.cross_library_min,r.cross_library_max,color=color,lw=2);ax.scatter(r.difference_of_library_means,3-j,color=color,s=40,marker='o' if var=='raw' else 's',zorder=3)
 ax.axvline(0,color=pal['muted'],ls=':',lw=1);ax.set_yticks(range(4),['12w | 1000 UMI','12w | raw','2w | 1000 UMI','2w | raw']);ax.set_title(label,fontweight='bold');ax.grid(axis='x',alpha=.22);ax.set_xlabel('Deletion minus heterozygous')
fig.suptitle('Il1r1 deletion lowers Cd177-associated RNA at both times;\n17 of 32 displayed cross-library ranges include zero',fontsize=19,x=.06,ha='left',y=1.04)
fig.text(.06,.96,'Differences in mean log2(CPM + 1) across module genes; 2 libraries per genotype/time. Lines are all cross-library ranges, NOT confidence intervals.',fontsize=10)
fig.tight_layout(rect=[0,.04,1,.93]);fig.text(.06,.015,'Source-QC populations; pools contain multiple lungs and biological identities remain unresolved. Marker/module RNA is not a direct fate or NF-kB activity measurement.',fontsize=9)
save(fig,'EN_F02_genotype_contrasts.png')
# Coverage-correct the rendering of cached per-cell declared-module means to mapped-module means.
manifest=pd.read_csv(HERE/'metadata/geo_library_manifest.csv');coverage=pd.read_csv(B/'rna/module_coverage.csv');libs=manifest[(manifest.experiment==2)&(manifest.population=='mutant_RFP')]
plot_cells={}; xmax=0.; ymax=0.
for row in libs.itertuples():
 v=pd.read_csv(HERE/f'processed/batch1/rna/{row.gsm}_depth1000_seed20260927_cells.csv.gz');r=coverage[(coverage.gsm==row.gsm)&(coverage.module=='TNFA_NFKB_RNA_disjoint')].iloc[0];v['response_mapped']=v.TNFA_NFKB_RNA_disjoint*r.genes/r.mapped;plot_cells[row.gsm]=v;xmax=max(xmax,v.response_mapped.max());ymax=max(ymax,v.AT1_identity.max())
xmax=float(np.ceil(xmax*10)/10);ymax=float(np.ceil(ymax*2)/2)
fig,axes=plt.subplots(2,4,figsize=(16,8),sharex=True,sharey=True); collections=[]
for ax,row in zip(axes.ravel(),libs.itertuples()):
 v=pd.read_csv(HERE/f'processed/batch1/rna/{row.gsm}_depth1000_seed20260927_cells.csv.gz');r=coverage[(coverage.gsm==row.gsm)&(coverage.module=='TNFA_NFKB_RNA_disjoint')].iloc[0]
 v=plot_cells[row.gsm];x=v.response_mapped;y=v.AT1_identity
 collection=ax.hexbin(x,y,C=np.full(len(v),1/len(v)),reduce_C_function=np.sum,gridsize=25,mincnt=0,cmap=cm,extent=(0,xmax,0,ymax));collections.append(collection);ax.set_xlim(0,xmax);ax.set_ylim(0,ymax)
 gt='het' if row.il1r1_status=='heterozygous' else 'deletion';ax.set_title(f'{int(row.collection_day)//7}w {gt} r{row.reported_replicate_token}\n{row.gsm} | n={len(v):,}',fontsize=11)
 ax.text(.97,.94,f'Nfkbia detected: {(v.Nfkbia>0).mean():.1%}',transform=ax.transAxes,ha='right',va='top',fontsize=9)
for ax in axes[-1,:]:ax.set_xlabel('TNF/NF-kB-associated RNA')
for ax in axes[:,0]:ax.set_ylabel('AT1 identity RNA')
fig.suptitle('Different RNA distributions remain visible within individual libraries',fontsize=18,x=.06,ha='left',y=1.02)
fig.text(.06,.96,'Each cell sampled to 1,000 UMIs; mean log1p(CP10k) over mapped genes. Hexagons encode the per-library cell fraction on a common log color scale.',fontsize=10)
norm=LogNorm(vmin=1/max(len(v) for v in plot_cells.values()),vmax=max(float(c.get_array().max()) for c in collections))
for c in collections:c.set_norm(norm)
fig.tight_layout(rect=[0,.04,.94,.93]);cax=fig.add_axes([.96,.24,.012,.48]);fig.colorbar(collections[-1],cax=cax,label='Fraction of library cells')
fig.text(.06,.01,'Gene-disjoint RNA panels are shown jointly; panels do not trace fate or estimate protein activity. Nfkbia detection is a feedback-associated RNA readout.',fontsize=9)
save(fig,'EN_F03_library_distributions.png')
models=pd.read_csv(B/'clones/model_LOMO_summary.csv');f=models[models.sensitivity=='full_ge2'].pivot(index=['dataset','channel'],columns='model',values='mean_heldout_NLL').reset_index()
fig,(ax,ax2)=plt.subplots(1,2,figsize=(15,7),gridspec_kw={'width_ratios':[1.25,1]});ylabs=[]
for j,r in f.iterrows():
 lab=f'{r.dataset} / '+('WT' if r.channel=='YFP' else 'mutant' if r.channel=='RFP' else 'control');ylabs.append(lab)
 delta=r.two_shifted_geometric_mixture-r.shifted_negative_binomial;ax.scatter(delta,j,color=cs[1] if delta>0 else cs[0],s=65);ax.text(delta,j+.15,f'{delta:+.3f}',fontsize=9,ha='center')
ax.set_yticks(range(len(f)),ylabs);ax.invert_yaxis();ax.axvline(0,color=pal['muted'],ls=':');ax.set_xlabel('Two-component NLL minus negative-binomial NLL\nNegative: mixture predicts better | Positive: alternative predicts better');ax.set_title('Held-out mouse prediction; lower NLL is better',fontweight='bold');ax.grid(axis='x',alpha=.2)
summ=pd.read_csv(B/'clones/clone_summary_by_mouse.csv');s=summ[summ.dataset.str.startswith('kras')]
for channel,color,offset in [('YFP',cs[0],-.035),('RFP',cs[1],.035)]:
 t=s[s.channel==channel]
 for r in t.itertuples():ax2.scatter(r.week+offset,r.top10percent_clone_cell_share,color=color,s=34,alpha=.8)
 avg=t.groupby('week').top10percent_clone_cell_share.mean();ax2.plot(avg.index,avg.values,color=color,label='WT YFP' if channel=='YFP' else 'Mutant RFP')
ax2.set_xlabel('Weeks after induction');ax2.set_ylabel('Fraction of cells in largest 10% of clones');ax2.set_title('Growth becomes concentrated in the clone-size tail',fontweight='bold');ax2.legend(frameon=False);ax2.set_ylim(0,1);ax2.grid(alpha=.2)
fig.suptitle('Clone-size heterogeneity does not uniquely identify two founder classes',fontsize=18,x=.06,ha='left',y=1.02);fig.tight_layout(rect=[0,.055,1,.95]);fig.text(.06,.01,'44 source-indexed mice overall. Models use n >= 2, equal training-mouse weight and leave-one-mouse-out validation; right-hand points are individual mice, lines are means.',fontsize=9)
save(fig,'EN_F05_clone_models.png')
sp=pd.read_csv(B/'clones/spatial_pooled_bin_profiles.csv');fig,axes=plt.subplots(2,3,figsize=(15,8),sharex=True)
for j,ds in enumerate(['kras1w','kras2w','kras4w']):
 s=sp[sp.dataset==ds];x=(s.distance_low_um+s.distance_high_um)/2
 strong=s.pair_rows>=10
 for axis,values,col in [(axes[0,j],s.mean_neighbor_size,cs[0]),(axes[1,j],s.mean_neighbor_spc_negative_fraction*100,cs[1])]:
  axis.plot(x,np.where(strong,values,np.nan),color=col);axis.scatter(x[strong],values[strong],s=12+4*np.log1p(s.pair_rows[strong]),color=col);axis.scatter(x[~strong],values[~strong],s=28,facecolors='none',edgecolors=col)
 axes[0,j].set_title(f'{ds[4:]} | {s.pair_rows.sum():,} pooled pair rows',fontweight='bold')
 axes[1,j].set_xlabel('Distance to mutant clone (micrometres)');axes[1,j].set_ylim(0,100)
 for ax in axes[:,j]:ax.grid(alpha=.2)
axes[0,0].set_ylabel('Mean WT clone size');axes[1,0].set_ylabel('Mean pro-Sftpc-negative fraction (%)')
fig.suptitle('Spatial profiles are descriptive because mouse and clone-pair identities are absent',fontsize=17,x=.06,ha='left',y=1.02);fig.tight_layout(rect=[0,.04,1,.94]);fig.text(.06,.01,'Source 50-micrometre bins; hollow points have <10 pair rows. Neighboring clones may repeat; no biological uncertainty or distance-independence claim is computed.',fontsize=9)
save(fig,'EN_F06_spatial_profiles.png')
(OUT/'render_record.json').write_text(json.dumps({'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'palette_sha256':hashlib.sha256((ROOT/'analysis/config/palette.json').read_bytes()).hexdigest(),'cell_score_rendering':'TNFA/NFKB declared-module cached cell means rescaled by declared/mapped gene count for consistency with pseudobulk mapped-gene denominator; no biological comparison changed','figures':[{'file':n,'sha256':hashlib.sha256((OUT/n).read_bytes()).hexdigest()} for n in saved]},indent=2)+'\n');print('Rendered',len(saved),'figures')
