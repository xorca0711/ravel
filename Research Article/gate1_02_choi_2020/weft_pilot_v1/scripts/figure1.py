"""Draft P001 Figure 1B-D descriptive adapter. Never imports historical modules."""
from __future__ import annotations
import argparse,json,pathlib,sys,time,resource
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from common import ROOT,CONFIG,require_reviewed_job,fresh_output,write_json,BoundsRecorder,counts_and_fractions
from sparse_input import load_triplet
import numpy as np,pandas as pd,anndata as ad,scanpy as sc
import frozen_methods as fm

def describe(a,out):
 annotations={};assigned={}
 for resolution in (0.3,0.5,1.0):
  key=f'leiden_{resolution}';table=fm.annotate_clusters_b(fm.cluster_detection_table(a,key));table.to_csv(out/f'clusters_{resolution}.csv',index=False)
  assigned[str(resolution)]=sorted(set(table.state)&set(fm.STATE_ORDER));annotations[resolution]=table
  a.obs[f'state_b_{resolution}']=a.obs[key].astype(str).map(dict(zip(table.cluster,table.state)))
 # Owner-fixed primary, distinct from historical outcome-dependent selection.
 primary=1.0;a.obs['state_before_subcluster']=a.obs['state_b_1.0'].astype(str);a.obs['state']=a.obs['state_before_subcluster'];a.obs['cluster']=a.obs['leiden_1.0'].astype(str)
 subrecord={'triggered':False}
 pd.DataFrame(columns=['cluster','n_cells','state','rule']).to_csv(out/'datp_subclusters.csv',index=False)
 if 'pAT2' not in assigned['1.0'] and 'DATP' in assigned['1.0']:
  mask=(a.obs.state=='DATP').to_numpy()
  if mask.sum()<=30:raise ValueError('HOLD: DATP subset cannot support frozen 30-neighbor setting')
  sub=a[mask].copy()
  sc.pp.neighbors(sub,n_neighbors=30,use_rep='X_pca',random_state=0)
  sc.tl.leiden(sub,resolution=.5,key_added='sub',flavor='igraph',n_iterations=2,random_state=0)
  table=fm.annotate_clusters_b(fm.cluster_detection_table(sub,'sub'));table.to_csv(out/'datp_subclusters.csv',index=False)
  mapping=dict(zip(table.cluster,table.state));relabel=sub.obs['sub'].astype(str).map(mapping)
  a.obs.loc[sub.obs_names,'state']=relabel.where(relabel.isin(['pAT2','DATP']),'DATP').to_numpy()
  a.obs.loc[sub.obs_names,'cluster']=(a.obs.loc[sub.obs_names,'cluster'].astype(str)+'.'+sub.obs['sub'].astype(str)).to_numpy()
  subrecord={'triggered':True,'cells':int(mask.sum()),'resolution':.5,'mapped_states':mapping,'non_pAT2_DATP_substates_retained_as_DATP':True}
 denominators={}
 for library,group in a.obs.groupby('library',observed=True):
  vc=group.state.astype(str).value_counts();cont=sum(int(v) for k,v in vc.items() if k.startswith('contaminant_'));unassigned=int(vc.get('unassigned',0));assigned=sum(int(vc.get(k,0)) for k in fm.STATE_ORDER)
  assert assigned+unassigned+cont==len(group)
  denominators[str(library)]={'total_post_doublet':len(group),'assigned':assigned,'unassigned':unassigned,'contaminant':cont,'non_contaminant_including_unassigned':len(group)-cont,'states':{k:int(vc.get(k,0)) for k in fm.STATE_ORDER}}
 composition=counts_and_fractions(a.obs);pd.DataFrame(composition).to_csv(out/'composition.csv',index=False)
 marker_rows=[];availability={}
 sets={**fm.STATE_SETS,**fm.CONTAMINANT_SETS}
 for name,genes in sets.items():availability[name]={'present':[g for g in genes if g in a.var_names],'missing':[g for g in genes if g not in a.var_names]}
 for state in sorted(a.obs.state.unique()):
  mask=(a.obs.state==state).to_numpy()
  for name,genes in sets.items():
   for gene,frac in fm.detection(a,genes,mask).items():marker_rows.append({'state':str(state),'n_cells':int(mask.sum()),'marker_set':name,'gene':gene,'detection_fraction':float(frac)})
 markers=pd.DataFrame(marker_rows);markers.to_csv(out/'marker_evidence.csv',index=False)
 h=(a.obs.state=='hAT2').to_numpy();X=a.layers['counts'][h]
 ids=[a.var_names.get_loc(g) for g in fm.STATE_SETS['AT2_identity'] if g in a.var_names];inf=[a.var_names.get_loc(g) for g in fm.STATE_SETS['pAT2_inflammatory'] if g in a.var_names]
 k_id=np.asarray((X[:,ids]>0).sum(axis=1)).ravel();k_inf=np.asarray((X[:,inf]>0).sum(axis=1)).ravel();like=(k_id==0)&(k_inf>=2)
 a.obs[['library','gsm','timepoint','state_before_subcluster','state','cluster']].to_csv(out/'cell_states.csv',index_label='sample_prefixed_cell_id')
 # Fresh descriptive panels; no published-number matching or inference.
 import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
 totals=a.obs.groupby('library',observed=True).size();fig,ax=plt.subplots(figsize=(7,4));totals.plot.bar(ax=ax);ax.set_ylabel('Cells after D1 QC and doublet removal');fig.tight_layout();fig.savefig(out/'figure1B_counts.png',dpi=150);plt.close(fig)
 comp=pd.DataFrame(composition);pivot=comp[~comp.state.str.startswith('contaminant_')].pivot(index='library',columns='state',values='fraction_alveolar').fillna(0)
 fig,ax=plt.subplots(figsize=(7,4));pivot.plot.bar(stacked=True,ax=ax);ax.set_ylabel('Fraction of non-contaminant cells, including unassigned');fig.tight_layout();fig.savefig(out/'figure1C_composition.png',dpi=150);plt.close(fig)
 heat=markers.groupby(['state','marker_set'],observed=True).detection_fraction.mean().unstack();fig,ax=plt.subplots(figsize=(10,4));im=ax.imshow(heat.to_numpy(),aspect='auto',vmin=0,vmax=1);ax.set_yticks(range(len(heat)),heat.index);ax.set_xticks(range(len(heat.columns)),heat.columns,rotation=90);fig.colorbar(im,ax=ax,label='Mean marker detection fraction');fig.tight_layout();fig.savefig(out/'figure1D_marker_detection.png',dpi=150);plt.close(fig)
 return {'primary_resolution':primary,'denominators_by_library':denominators,'states_assigned_before_subclustering':assigned,'final_pAT2_cells':int((a.obs.state=='pAT2').sum()),'pAT2_absent':bool(not (a.obs.state=='pAT2').any()),'DATP_subclustering':subrecord,'cell_level_pAT2_like_among_hAT2':{'denominator':int(h.sum()),'count':int(like.sum()),'fraction':float(like.mean()) if len(like) else None},'marker_availability':availability,'same_library_knn_enrichment':fm.same_library_enrichment(a),'composition':composition,'interpretation':'exposed descriptive benchmark; one pooled library per condition; no animal-level p-values, mechanism inference or biological success tolerance'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--reviewed-job');args=p.parse_args();job=require_reviewed_job(args.reviewed_job,'figure1');out=fresh_output(args.output,'figure1')
 manifest=json.loads((CONFIG/'inputs.json').read_text());kept=[];qc=[];audits=[];bounds={};gene_order=None;start=time.monotonic();sc.settings.n_jobs=4
 for sample in manifest['samples']:
  X,var,bc,audit=load_triplet(ROOT,manifest['files'],sample['gsm'])
  if gene_order is None:gene_order=var.gene_id.tolist()
  elif gene_order!=var.gene_id.tolist():raise ValueError('cross-library feature order mismatch')
  counts=np.asarray(X.sum(axis=1)).ravel();genes=X.getnnz(axis=1)
  if not ((genes>500)&(genes<7000)&(counts>2000)).any():raise ValueError('HOLD: no cells pass frozen paper filter')
  meta={'gsm':sample['gsm'],'library':sample['title'],'timepoint':{'GSM4304609':'PBS','GSM4304611':'day 14','GSM4304613':'day 28'}[sample['gsm']],'sort':'Tomato','accession':'GSE145031'}
  rec=BoundsRecorder();a,row=fm.call_and_qc(X,var,bc,meta,rec);del X,var,bc
  n_raw=row['n_barcodes'];assert 0<=row['paper_rule_cells']<=n_raw and row['paper_rule_cells']-row['mad_removed']==row['cells_after_qc'] and row['cells_after_qc']-row['doublets_flagged']==row['cells_final']
  qc.append(row);bounds.update(rec.bounds);audits.append(audit);kept.append(a[~a.obs.predicted_doublet].copy());del a
 if any(not kept[0].var_names.equals(x.var_names) for x in kept[1:]):raise ValueError('QC feature-index order mismatch')
 a=ad.concat(kept,join='inner',index_unique=None);del kept
 if not a.obs_names.is_unique:raise ValueError('sample-prefixed cell ID collision')
 if a.n_obs<=30:raise ValueError('HOLD: insufficient retained cells for frozen PCA/neighbors')
 a.layers['counts']=a.X.copy();fm.embed(a);summary=describe(a,out);a.write_h5ad(out/'figure1_descriptive.h5ad')
 pd.DataFrame(qc).to_csv(out/'qc_denominators.csv',index=False)
 summary.update({'job_id':job['job_id'],'qc_denominators':qc,'qc_bounds':bounds,'input_audits':audits,'elapsed_seconds':time.monotonic()-start,'process_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'selection_note':'Fixed primary 1.0; sensitivities 0.3/0.5/1.0; no tuning to recover five states'})
 write_json(out/'descriptive-summary.json',summary)
if __name__=='__main__':main()
