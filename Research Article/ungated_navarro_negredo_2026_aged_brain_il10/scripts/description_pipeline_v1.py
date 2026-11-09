"""Execute frozen R description, independently check arithmetic, and plot measured summaries."""
import argparse
import collections
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True);a=p.parse_args()
cfg=json.loads(Path(a.config).read_text());out=Path(a.output)
subprocess.run([sys.executable,cfg['bounded_launcher'],'--script',cfg['R_script'],'--config',a.config,'--output',str(out)],check=True)
readtab=lambda name:pd.read_csv(out/name,sep='\t')
denom=readtab('cell_denominators.tsv');summary=readtab('summaries_R.tsv');availability=readtab('marker_availability.tsv')
assert not denom.cell_index.duplicated().any()
assert set(denom.condition)==set(cfg['conditions'])
assert set(denom.celltype)=={'Microglia','T_cells'}
cellinfo=denom.set_index('cell_index').to_dict('index')
groupcells=collections.defaultdict(set)
for cell,d in cellinfo.items():groupcells[d['celltype'],d['condition']].add(cell)
recovery=pd.read_csv(cfg['recovery_table'],sep='\t')
for key,cells in groupcells.items():
    expected=recovery.loc[(recovery.celltype==key[0])&(recovery.condition==key[1]),'cells']
    assert len(expected)==1 and int(expected.iloc[0])==len(cells)
norm_values=collections.defaultdict(list);raw_values=collections.defaultdict(list);seen=set();gzm_positive=set()
max_normalization_error=0.0;entry_count=0
with gzip.open(out/'selected_entries.tsv.gz','rt') as f:
    for r in csv.DictReader(f,delimiter='\t'):
        cell=int(r['cell_index']);d=cellinfo[cell];key=(r['celltype'],r['condition'],r['gene'])
        assert r['condition']==d['condition'] and r['celltype']==d['celltype']
        assert (cell,r['gene']) not in seen;seen.add((cell,r['gene']))
        raw=float(r['raw_count']);norm=float(r['normalized']);total=float(r['library_total'])
        assert raw>0 and raw==int(raw) and total==d['library_total'] and math.isfinite(norm)
        err=abs(norm-math.log1p(raw/total*cfg['scale_factor']))
        max_normalization_error=max(max_normalization_error,err)
        assert err<=cfg['arithmetic_tolerance']
        raw_values[key].append(raw);norm_values[key].append(norm);entry_count+=1
        if r['celltype']=='T_cells' and r['gene']=='Gzmb':gzm_positive.add(cell)
assert {i for i,d in cellinfo.items() if d['celltype']=='T_cells' and d['gzmb_positive']==1}==gzm_positive
checks=0;max_summary_error=0.0
def equal(actual,expected):
    global checks,max_summary_error
    checks+=1
    if expected is None:
        assert pd.isna(actual),(actual,expected)
    else:
        assert not pd.isna(actual)
        error=abs(float(actual)-float(expected));max_summary_error=max(max_summary_error,error)
        assert error<=cfg['arithmetic_tolerance']*max(1,abs(float(expected))),(actual,expected,error)
for _,s in summary.iterrows():
    conditional=s.scope=='T_cells_Gzmb_positive';scope='T_cells' if conditional else s.scope
    cells=groupcells[scope,s.condition];n_all=len(cells)
    if conditional:cells=cells&gzm_positive
    n=len(cells);key=(scope,s.condition,s.gene)
    values=norm_values[key];raw=raw_values[key]
    equal(s.n_cells,n)
    if not s.gene_present:
        assert not values
        for field in ['n_detected','sum_normalized','total_raw','mean_log_expression','detection_fraction','mean_log_expression_positive']:equal(s[field],None)
        continue
    detected=len(raw)
    # The conditional scope contains exactly the positive Gzmb cells.
    if conditional:assert detected==n and s.gene=='Gzmb'
    total=math.fsum(values)
    equal(s.n_detected,detected);equal(s.sum_normalized,total);equal(s.total_raw,math.fsum(raw))
    equal(s.mean_log_expression,total/n if n else None)
    equal(s.detection_fraction,detected/n if n else None)
    equal(s.mean_log_expression_positive,total/detected if detected else None)
    if scope=='T_cells':equal(s.n_all_T,n_all)
    equal(s.gzmb_positive_fraction_all_T,len(cells&gzm_positive)/n_all if conditional and n_all else None)
summary.to_csv(out/'summaries.tsv',sep='\t',index=False,float_format='%.17g',na_rep='NA')
index=summary.set_index(['scope','gene','condition']);contrasts=[]
for spec in cfg['contrasts']:
    for (scope,gene),rows in summary.groupby(['scope','gene'],sort=False):
        left=index.loc[(scope,gene,spec['left'])];right=index.loc[(scope,gene,spec['right'])]
        contrasts.append({'scope':scope,'family':left.family,'gene':gene,'contrast':spec['id'],
          'left':spec['left'],'right':spec['right'],'n_left':int(left.n_cells),'n_right':int(right.n_cells),
          'mean_log_difference':left.mean_log_expression-right.mean_log_expression,
          'detection_fraction_difference':left.detection_fraction-right.detection_fraction,
          'gzmb_positive_fraction_all_T_difference':left.gzmb_positive_fraction_all_T-right.gzmb_positive_fraction_all_T})
contrast=pd.DataFrame(contrasts);original=readtab('contrasts_R.tsv').set_index(['scope','gene','contrast'])
for _,r in contrast.iterrows():
    other=original.loc[(r.scope,r.gene,r.contrast)]
    for field in ['n_left','n_right','mean_log_difference','detection_fraction_difference','gzmb_positive_fraction_all_T_difference']:
        equal(other[field],None if pd.isna(r[field]) else r[field])
contrast.to_csv(out/'contrasts.tsv',sep='\t',index=False,float_format='%.17g',na_rep='NA')
absent=availability.loc[~availability.present,['scope','family','gene']].to_dict('records')
verification={'selected_sparse_entries_checked':entry_count,'explicit_cell_denominators_checked':len(cellinfo),
  'summary_rows_checked':len(summary),'contrast_rows_checked':len(contrast),'scalar_arithmetic_checks':checks,
  'max_normalization_error_python':max_normalization_error,'max_scalar_difference_R_vs_Python':max_summary_error,
  'arithmetic_tolerance':cfg['arithmetic_tolerance'],'all_checks_passed':True,
  'method':'Independent Python math.fsum and raw-count normalization from selected sparse entries; implicit zeros retained through full cell denominators. R and Python contrasts independently agree.',
  'absent_markers':absent,'independent_biological_replication':False}
(out/'independent_verification.json').write_text(json.dumps(verification,indent=2)+'\n')
holds={'held_expression_aliases':['WT50','Mut50'],'held_reason':'Observed extra conditions lack qualified numerical dose/accession mapping to the six reported source libraries.',
  'other_concentration_numeric_dose_verified':False,'main_figure_pair':'WT5/Mut5; caption-associated 0.02 mg/mL, indirect code/figure cross-reference',
  'other_pair':'WT1/Mut1; other-concentration code block, not a verified numeric-dose join',
  'downstream_microglia_exclusion_reproduced':False,'microglia_scope':'Original broad Celltype==Microglia; Micro_types and later Remove exclusion absent.',
  'hallmark_score_reproduced':False,'hallmark_reason':'Exact external .rda gene membership absent; explicit 20-gene author vector only.',
  'Figure3E':'Published caption Stat3 versus code Socs3; both reported separately.',
  'filename_discrepancy_retained':True,'population_P_values_or_CIs_computed':False,
  'one_pool_per_reported_condition':True,'optional_objects_acquired':False,'scientific_acceptance':'not_assessed'}
(out/'scientific_holds.json').write_text(json.dumps(holds,indent=2)+'\n')
(out/'software_versions.json').write_text(json.dumps({'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,'matplotlib':matplotlib.__version__},indent=2)+'\n')

# Measured figures: fixed marker vectors and all declared contrasts; no selected positive panel.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
markers=json.loads(Path(cfg['marker_manifest']).read_text())['vectors']
conditions=cfg['conditions'];colors=['#6677aa','#666666','#254c77','#32a7a1','#8b5c32','#ca8c42']
def save(fig,name):
    fig.savefig(out/name,format='svg',metadata={'Date':None},bbox_inches='tight');plt.close(fig)
def marker_matrix(genes,field):
    return np.array([[index.loc[('Microglia',g,c),field] for c in conditions] for g in genes],dtype=float)
fig,axes=plt.subplots(1,2,figsize=(13,11),gridspec_kw={'width_ratios':[1,1]})
vmax=max(0.1,float(summary.loc[summary.scope=='Microglia','mean_log_expression'].max()))
for ax,key,title in zip(axes,['il10','ifng'],['IL-10-related markers (mixed directions)','IFN-related author marker vector']):
    genes=markers[key]['genes'];mean=marker_matrix(genes,'mean_log_expression');det=marker_matrix(genes,'detection_fraction')
    for y in range(len(genes)):
        for x in range(len(conditions)):
            if np.isnan(mean[y,x]):ax.plot(x,y,marker='x',color='#888888',ms=5)
            elif det[y,x]==0:ax.scatter(x,y,s=6,facecolors='white',edgecolors='#999999',linewidths=.5)
            else:sc=ax.scatter(x,y,s=145*det[y,x],c=[mean[y,x]],cmap='viridis',vmin=0,vmax=vmax,edgecolors='none')
    ax.set(xticks=range(6),xticklabels=conditions,yticks=range(len(genes)),yticklabels=genes,xlim=(-.65,5.65),ylim=(len(genes)-.3,-.7),title=title)
    ax.grid(axis='x',alpha=.12);ax.tick_params(axis='y',length=0)
    ax.set_xlabel('Original condition alias; WT50/Mut50 held')
fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(0,vmax),cmap='viridis'),ax=axes,shrink=.6,pad=.04,label='Mean RNA log1p(count / library total × 10,000)')
fig.suptitle('Navarro main deposit: broad microglial RNA description',fontsize=14,y=.94)
fig.text(.08,.015,'Point area = raw-count detection fraction (0–100%); × = gene absent. One observed pool per condition.\nWT5/Mut5: main-figure pair (caption 0.02 mg/mL); WT1/Mut1: other-concentration pair, numeric mapping unverified.\nOriginal broad annotation; downstream microglial exclusion not recreated. No population tests or uncertainty intervals.',fontsize=9)
save(fig,'microglia_markers.svg')

fig,axes=plt.subplots(2,2,figsize=(16,16),gridspec_kw={'height_ratios':[28,20]})
ids=[x['id'] for x in cfg['contrasts']]
ci=contrast.set_index(['scope','gene','contrast'])
for row,key in enumerate(['il10','ifng']):
    genes=markers[key]['genes']
    for col,field in enumerate(['mean_log_difference','detection_fraction_difference']):
        arr=np.array([[ci.loc[('Microglia',g,c),field] for c in ids] for g in genes],dtype=float)
        if col:arr*=100
        allvalues=contrast.loc[contrast.scope=='Microglia',field].to_numpy(float)*(100 if col else 1)
        limit=max(.01,float(np.nanmax(np.abs(allvalues))))
        ax=axes[row,col];im=ax.imshow(np.ma.masked_invalid(arr),cmap='RdBu_r',vmin=-limit,vmax=limit,aspect='auto')
        ax.set(yticks=range(len(genes)),yticklabels=genes,xticks=range(len(ids)),xticklabels=ids)
        ax.tick_params(axis='x',rotation=45);ax.set_title(('IL-10-related (mixed directions)' if row==0 else 'IFN-related')+' — '+('mean log-expression difference' if col==0 else 'detection difference (percentage points)'))
        fig.colorbar(im,ax=ax,shrink=.65,pad=.02)
fig.suptitle('All declared broad-microglia contrasts; positive = left alias higher',fontsize=15)
fig.tight_layout(rect=(0,.06,1,.96))
fig.text(.04,.012,'WT5/Mut5 is the main-figure pair; WT1/Mut1 is the other-concentration pair. Young−Control is age context only.\nThese are differences of observed pool means/detection fractions, not the authors’ differential-expression log2 fold changes.\nNo marker-vector score, favorable-direction aggregation, cell-based P values, or population confidence intervals.',fontsize=10)
save(fig,'microglia_contrasts.svg')

fig,axes=plt.subplots(2,2,figsize=(13,9));ax=axes[0,0]
allconds=conditions+['WT50','Mut50'];tcounts=[int(recovery.loc[(recovery.condition==c)&(recovery.celltype=='T_cells'),'cells'].iloc[0]) for c in allconds]
bars=ax.bar(allconds,tcounts,color=colors+['#cccccc','#cccccc'])
for bar,n in zip(bars,tcounts):ax.text(bar.get_x()+bar.get_width()/2,n+2,str(n),ha='center',fontsize=8)
for bar in bars[-2:]:bar.set_hatch('//')
ax.set(title='A  Recovered original T cells (all eight aliases)',ylabel='Recovered cells');ax.tick_params(axis='x',rotation=35)
for gene,color,marker in [('Ifng','#8d436f','o'),('Gzmb','#267c73','s')]:
    for ax,field,title in [(axes[0,1],'mean_log_expression','B  All-T mean RNA log expression'),(axes[1,0],'detection_fraction','C  All-T raw-count detection')]:
        vals=[index.loc[('T_cells',gene,c),field] for c in conditions]
        if field=='detection_fraction':vals=[v*100 for v in vals]
        ax.plot(conditions,vals,marker=marker,color=color,label=gene);ax.set_title(title);ax.tick_params(axis='x',rotation=35);ax.legend(frameon=False)
axes[0,1].set_ylabel('Mean RNA log1p normalized expression');axes[1,0].set_ylabel('Detected T cells (%)');axes[1,0].set_ylim(0,105)
ax=axes[1,1];vals=[index.loc[('T_cells_Gzmb_positive','Gzmb',c),'mean_log_expression'] for c in conditions]
bars=ax.bar(conditions,vals,color=colors)
for c,b in zip(conditions,bars):
    s=index.loc[('T_cells_Gzmb_positive','Gzmb',c)]
    if np.isfinite(b.get_height()):ax.text(b.get_x()+b.get_width()/2,b.get_height()+.04,f'{int(s.n_cells)}/{int(s.n_all_T)}',ha='center',fontsize=9)
ax.set(title='D  Gzmb-positive T cells: conditional mean',ylabel='Mean RNA log expression among positive cells');ax.tick_params(axis='x',rotation=35)
fig.suptitle('T-cell endpoints retain all-T and Gzmb-positive denominators',fontsize=14)
fig.tight_layout(rect=(0,.08,1,.95))
fig.text(.03,.015,'Panel D labels = Gzmb-positive / all T cells; panel C retains the all-T denominator. Old Control has only nine T cells.\nWT50/Mut50 recovery is shown for transparency but expression comparisons are held. Lines connect finite-pool summaries only.\nWT5/Mut5: main-figure pair; WT1/Mut1: other-concentration pair. No independent mouse replication or inferential error bars.',fontsize=9)
save(fig,'T_cells.svg')

fig,ax=plt.subplots(figsize=(13,6));types=sorted(recovery.celltype.unique());bottom=np.zeros(len(allconds));palette=plt.get_cmap('tab20')
for k,type_ in enumerate(types):
    rows=recovery.loc[recovery.celltype==type_].set_index('condition')
    values=np.array([rows.loc[c,'fraction_of_recovered_condition']*100 for c in allconds])
    ax.bar(allconds,values,bottom=bottom,label=type_,color=palette(k),width=.8);bottom+=values
for x,c in enumerate(allconds):
    total=int(recovery.loc[recovery.condition==c,'cells'].sum());ax.text(x,102,f'n={total:,}',ha='center',fontsize=8)
ax.set(ylim=(0,110),ylabel='Fraction of recovered cells (%)',title='Original broad cell-type recovery; all retained aliases')
ax.legend(bbox_to_anchor=(1.02,1),loc='upper left',frameon=False,fontsize=8)
fig.text(.07,-.02,'Recovery is a capture/composition description, not tissue abundance or biological replication. WT50/Mut50 remain dose-unmapped.',fontsize=9)
save(fig,'recovery.svg')
print(json.dumps(verification),flush=True)
