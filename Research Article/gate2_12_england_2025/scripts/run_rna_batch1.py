"""Frozen England batch 1: library-level RNA distributions, never cell-level tests."""
from __future__ import annotations
import argparse, os, sys, json, hashlib, importlib.util, datetime, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--data-root',type=Path,required=True);a=p.parse_args()
os.environ.setdefault('NUMBA_NUM_THREADS','4');os.environ.setdefault('OMP_NUM_THREADS','4')
sys.path.insert(0,str(a.data_root/'.venv-x64/Lib/site-packages'))
import numpy as np
import pandas as pd
import scipy.sparse as sp
import scanpy as sc
import anndata as ad
import importlib.metadata as im
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('shared_trial_utils',ROOT/'Research Article/gate1_04_sikkema_2023_hlca/trials/trial_utils.py')
u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
contract_path=HERE/'config/batch1_contract.json';cfg=json.loads(contract_path.read_text())
OUT=HERE/'trials/batch1/rna';CACHE=HERE/'processed/batch1/rna'
OUT.mkdir(parents=True,exist_ok=True);CACHE.mkdir(parents=True,exist_ok=True)
assert not (OUT/'run_record.json').exists(),'Refuse overwrite of completed run'
def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'contract_sha256':digest(contract_path),'script_sha256':digest(Path(__file__)),'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'versions':{m:im.version(m) for m in ['numpy','pandas','scipy','scanpy','anndata']},'inputs':[],'interpretation':'descriptive library-level estimates; biological pool and pairing identities unknown'}
(OUT/'started.json').write_text(json.dumps(record,indent=2))
manifest=pd.read_csv(HERE/'metadata/geo_library_manifest.csv',keep_default_na=False)
needed=sorted(set(sum(cfg['marker_gates'].values(),[])+sum(cfg['modules'].values(),[])+cfg['individual_genes']+sum(cfg['non_epithelial_flags'].values(),[])+['Nkx2-1']))
gi={g:i for i,g in enumerate(needed)}
expr=[];frac=[];qcs=[];coverage=[];dist=[];input_facts=[]
meta_keys=['gsm','title','experiment','reporter','il1r1_status','population','collection_day','reported_replicate_token']
def summary(C,totals,meta,variant,include=None,save_cells=False):
 if include is None:include=np.ones(C.shape[0],dtype=bool)
 C=C[include];totals=totals[include];n=len(totals)
 if n==0:return
 detect=C>0
 gates={g:detect[:,[gi[x] for x in genes]].sum(1)>=2 for g,genes in cfg['marker_gates'].items()}
 gates['mixed_identity']=gates['AT2_supported']&gates['AT1_supported']
 groups={'all_QC':np.ones(n,dtype=bool),**gates}
 log=np.log1p(C/totals[:,None]*1e4)
 scores={k:log[:,[gi[x] for x in genes]].mean(1) for k,genes in cfg['modules'].items()}
 cells={**{k:v for k,v in gates.items()},**scores,'Nfkbia':log[:,gi['Nfkbia']],'Tonsl':log[:,gi['Tonsl']],'total_umis':totals}
 for group,mask in groups.items():
  nc=int(mask.sum());frac.append({**meta,'variant':variant,'group':group,'n_cells':nc,'denominator':n,'fraction':nc/n})
  if nc<cfg['min_cells_for_conditional_expression']:continue
  sums=C[mask].sum(0,dtype=np.float64);denom=float(totals[mask].sum());lcpm=np.log2(sums/denom*1e6+1)
  for endpoint,genes in {**cfg['modules'],**{g:[g] for g in cfg['individual_genes']}}.items():
   ix=[gi[g] for g in genes];valid=[gi[g] for g in genes if g in present_genes]
   cov=len(valid)/len(ix)
   if cov<cfg['module_coverage_floor']:continue
   score=log[mask][:,valid].mean(1)
   expr.append({**meta,'variant':variant,'group':group,'n_cells':nc,'endpoint':endpoint,'coverage':cov,'pseudobulk_mean_log2_CPM1':float(lcpm[valid].mean()),'cell_median_log1p_CP10k':float(np.median(score)),'cell_q90_log1p_CP10k':float(np.quantile(score,.9)),'cell_mean_log1p_CP10k':float(score.mean()),'detection_fraction_any':float(detect[mask][:,valid].any(1).mean()),'positive_mean_log1p_CP10k':float(score[score>0].mean()) if (score>0).any() else np.nan})
 if save_cells:pd.DataFrame(cells).to_csv(CACHE/f"{meta['gsm']}_{variant}_cells.csv.gz",index=False)
for _,row in manifest.iterrows():
 meta={k:row[k] for k in meta_keys};matrix=a.data_root/row.matrix_path
 prefix=matrix.name.removesuffix('_matrix.mtx.gz')
 features=matrix.with_name(prefix+'_features.tsv.gz');barcodes=matrix.with_name(prefix+'_barcodes.tsv.gz')
 X,var,bc=u.read_mtx_triplet(matrix,features,barcodes)
 assert np.all(X.data>=0) and np.all(X.data==np.floor(X.data))
 totals=np.asarray(X.sum(1)).ravel();ng=X.getnnz(1);symbols=var.gene_symbol.astype(str).to_numpy();present_genes=set(symbols)
 mt=np.char.startswith(symbols.astype(str),'mt-');mt_pct=np.asarray(X[:,mt].sum(1)).ravel()/np.maximum(totals,1)*100
 keep=(ng>=1000)&(totals<=50000)&(mt_pct<=15)
 before=X.shape[0];X=X[keep].tocsr();totals=totals[keep];ng=ng[keep];mt_pct=mt_pct[keep];bc=bc[keep]
 # Canonical triplet reader retained; aggregate repeated symbols only for named endpoints.
 rr=[];cc=[]
 for j,g in enumerate(symbols):
  if g in gi:rr.append(j);cc.append(gi[g])
 aggregate=sp.csr_matrix((np.ones(len(rr),dtype=np.int64),(rr,cc)),shape=(len(symbols),len(needed)))
 C=(X@aggregate).toarray().astype(np.int64)
 scores=np.full(len(totals),np.nan);doublets=np.zeros(len(totals),dtype=bool);scrublet_error=''
 try:
  obj=ad.AnnData(X=X.copy());obj.var_names=var.gene_id.astype(str).to_numpy();obj.var_names_make_unique()
  sc.pp.scrublet(obj,random_state=20260927,expected_doublet_rate=float(np.clip(.008*len(totals)/1000,.01,.15)),n_prin_comps=30,verbose=False)
  scores=obj.obs.doublet_score.to_numpy();doublets=obj.obs.predicted_doublet.to_numpy().astype(bool)
  del obj
 except Exception as e:scrublet_error=f'{type(e).__name__}: {e}'
 anchor=(C[:,[gi[g] for g in ['Sftpc','Etv5','Lamp3','Nkx2-1']]]>0).any(1)
 contaminant=np.zeros(len(totals),bool)
 for genes in cfg['non_epithelial_flags'].values():contaminant|=((C[:,[gi[g] for g in genes]]>0).sum(1)>=2)&~anchor
 qcs.append({**meta,'input_barcodes':before,'source_QC_cells':len(totals),'median_genes':float(np.median(ng)),'median_umis':float(np.median(totals)),'median_mito_percent':float(np.median(mt_pct)),'doublet_calls':int(doublets.sum()),'doublet_fraction':float(doublets.mean()),'scrublet_error':scrublet_error,'contamination_flags':int(contaminant.sum()),'source_gate_exact':'genes>=1000;UMI<=50000;mito<=15%'})
 for k,genes in cfg['modules'].items():coverage.append({'gsm':row.gsm,'module':k,'genes':len(genes),'mapped':len(set(genes)&present_genes),'fraction':len(set(genes)&present_genes)/len(genes)})
 summary(C,totals,meta,'raw',save_cells=True)
 if not scrublet_error:summary(C,totals,meta,'raw_auto_doublets_removed',~doublets)
 summary(C,totals,meta,'raw_contamination_flags_removed',~contaminant)
 # Retain sufficient raw summaries for an independent numerical verification.
 np.savez_compressed(CACHE/f'{row.gsm}_named_counts.npz',counts=C,totals=totals,genes=np.array(needed),doublets=doublets,contamination=contaminant)
 pd.DataFrame({'barcode':bc,'n_genes':ng,'total_counts':totals,'mito_percent':mt_pct,'doublet_score':scores,'doublet_flag':doublets,'contamination_flag':contaminant}).to_csv(CACHE/f'{row.gsm}_QC_cells.csv.gz',index=False)
 map_to_selected=np.array([gi.get(g,-1) for g in symbols],dtype=int)
 for seed in cfg['depth_sensitivity']['seeds']:
  rng=np.random.default_rng(seed);D=np.zeros_like(C)
  for i in range(X.shape[0]):
   start,end=X.indptr[i:i+2];values=X.data[start:end].astype(np.int64);ix=X.indices[start:end]
   draw=rng.multivariate_hypergeometric(values,1000)
   selected=map_to_selected[ix];valid=selected>=0
   np.add.at(D[i],selected[valid],draw[valid])
  variant=f'depth1000_seed{seed}';summary(D,np.full(len(totals),1000),meta,variant,save_cells=seed==20260927)
  if seed==20260927:np.savez_compressed(CACHE/f'{row.gsm}_depth1000_named_counts.npz',counts=D,totals=np.full(len(totals),1000),genes=np.array(needed))
 for f in [matrix,features,barcodes]:record['inputs'].append({'path':str(f.relative_to(a.data_root)).replace('\\','/'),'bytes':f.stat().st_size,'sha256':digest(f)})
 print(f"{row.gsm}: {before} -> {len(totals)} source-QC cells; auto-doublets {int(doublets.sum())}",flush=True)
 pd.DataFrame(qcs).to_csv(OUT/'QC_by_library.csv',index=False)
 del X,C
expression=pd.DataFrame(expr);fractions=pd.DataFrame(frac)
expression.to_csv(OUT/'library_expression.csv',index=False);fractions.to_csv(OUT/'phenotype_occupancy.csv',index=False);pd.DataFrame(coverage).to_csv(OUT/'module_coverage.csv',index=False)
contrasts=[]
for contrast in cfg['contrasts']:
 ex=contrast['experiment'];day=contrast['time_days'];sub=expression[(expression.experiment==ex)&(expression.collection_day.astype(str)==str(day))]
 field='il1r1_status' if ex==2 else 'population'
 for (variant,group,endpoint),s in sub.groupby(['variant','group','endpoint']):
  va=s[s[field]==contrast['A']].pseudobulk_mean_log2_CPM1.to_numpy();vb=s[s[field]==contrast['B']].pseudobulk_mean_log2_CPM1.to_numpy()
  if len(va)!=2 or len(vb)!=2:continue
  differences=(va[:,None]-vb[None,:]).ravel()
  contrasts.append({'experiment':ex,'collection_day':day,'contrast':contrast['A']+' minus '+contrast['B'],'primary':contrast['primary'],'variant':variant,'group':group,'endpoint':endpoint,'n_libraries_A':len(va),'n_libraries_B':len(vb),'difference_of_library_means':float(va.mean()-vb.mean()),'cross_library_min':float(differences.min()),'cross_library_max':float(differences.max()),'all_cross_library_directions_agree':bool((differences>0).all() or (differences<0).all()),'range_is_confidence_interval':False})
pd.DataFrame(contrasts).to_csv(OUT/'library_contrasts.csv',index=False)
record.update(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),libraries=len(qcs),source_QC_cells=int(sum(x['source_QC_cells'] for x in qcs)),counts_semantics='nonnegative integer verified',outputs=[{'file':f.name,'sha256':digest(f)} for f in OUT.glob('*.csv')])
(OUT/'run_record.json').write_text(json.dumps(record,indent=2)+'\n');print('RNA batch completed',record['source_QC_cells'],flush=True)
