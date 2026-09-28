"""Independent arithmetic/provenance checks for completed England batch1."""
import sys,json,hashlib,io,zipfile
from pathlib import Path
import argparse
pa=argparse.ArgumentParser();pa.add_argument('--data-root',type=Path,required=True);pa.add_argument('--archive',type=Path,required=True);args=pa.parse_args()
sys.path.insert(0,str(args.data_root/'.venv-x64/Lib/site-packages'))
import numpy as np
import pandas as pd
from scipy.io import mmread,loadmat
from scipy.stats import geom,nbinom
HERE=Path(__file__).resolve().parents[1];B=HERE/'trials/batch1';cache=HERE/'processed/batch1';cfg=json.loads((HERE/'config/batch1_contract.json').read_text())
checks=0;worst=0.
def close(x,y,label,tol=1e-10):
 global checks,worst
 checks+=1;err=float(np.max(np.abs(np.asarray(x)-np.asarray(y))));worst=max(worst,err)
 if not np.isfinite(err) or err>tol:raise AssertionError((label,err))
def require(ok,label):
 global checks
 checks+=1
 if not ok:raise AssertionError(label)
exp=pd.read_csv(B/'rna/library_expression.csv');fra=pd.read_csv(B/'rna/phenotype_occupancy.csv');qc=pd.read_csv(B/'rna/QC_by_library.csv');man=pd.read_csv(HERE/'metadata/geo_library_manifest.csv')
for row in man.itertuples():
 source_matrix=args.data_root/row.matrix_path; source_stem=source_matrix.name.removesuffix('_matrix.mtx.gz'); source_symbols=set(pd.read_csv(source_matrix.with_name(source_stem+'_features.tsv.gz'),sep='\t',header=None)[1].astype(str))
 d=np.load(cache/f'rna/{row.gsm}_named_counts.npz');C=d['counts'];N=d['totals'];genes=list(d['genes']);idx={g:i for i,g in enumerate(genes)}
 close(len(N),qc.loc[qc.gsm==row.gsm,'source_QC_cells'].iloc[0],row.gsm+' QC')
 mask={k:np.count_nonzero(C[:,[idx[g] for g in panel]],axis=1)>=2 for k,panel in cfg['marker_gates'].items()};mask['mixed_identity']=mask['AT2_supported']&mask['AT1_supported'];mask['all_QC']=np.ones(len(N),bool)
 for group,m in mask.items():
  r=fra[(fra.gsm==row.gsm)&(fra.variant=='raw')&(fra.group==group)].iloc[0];close(m.sum(),r.n_cells,'gate count');close(m.mean(),r.fraction,'gate fraction')
  if m.sum()<30:continue
  for endpoint,panel in {**cfg['modules'],**{g:[g] for g in cfg['individual_genes']}}.items():
   r=exp[(exp.gsm==row.gsm)&(exp.variant=='raw')&(exp.group==group)&(exp.endpoint==endpoint)]
   if len(r)==0:continue
   value=np.mean([np.log2(C[m,idx[g]].sum()*1e6/N[m].sum()+1) for g in panel if g in source_symbols]);close(value,r.iloc[0].pseudobulk_mean_log2_CPM1,'pseudobulk')
 thin=np.load(cache/f'rna/{row.gsm}_depth1000_named_counts.npz');require((thin['counts'].sum(1)<=1000).all(),'named counts exceed budget');require((thin['counts']<=C).all(),'without-replacement count bound')
# Independently re-read four genotype source matrices, bypassing the production reader.
import gzip
for gsm in ['GSM7890841','GSM7890843','GSM7890845','GSM7890847']:
 r=man[man.gsm==gsm].iloc[0];p=args.data_root/r.matrix_path;stem=p.name.removesuffix('_matrix.mtx.gz')
 with gzip.open(p,'rb') as h:X=mmread(h).tocsr().T.tocsr()
 symbols=pd.read_csv(p.with_name(stem+'_features.tsv.gz'),sep='\t',header=None)[1].astype(str).to_numpy();N=np.asarray(X.sum(1)).ravel();ng=X.getnnz(1);mito=np.array([x.startswith('mt-') for x in symbols]);mt=np.asarray(X[:,mito].sum(1)).ravel()/np.maximum(N,1)*100;keep=(ng>=1000)&(N<=50000)&(mt<=15);X=X[keep];N=N[keep]
 d=np.load(cache/f'rna/{gsm}_named_counts.npz');close(N,d['totals'],'direct raw totals')
 for gene in ['Sftpc','Cd177','Nfkbia','Tonsl','Pdpn','Abca3']:
  expected=np.asarray(X[:,symbols==gene].sum(1)).ravel();observed=d['counts'][:,list(d['genes']).index(gene)];close(expected,observed,'direct raw named gene')
con=pd.read_csv(B/'rna/library_contrasts.csv')
for r in con.itertuples():
 s=exp[(exp.experiment==r.experiment)&(exp.collection_day.astype(str)==str(r.collection_day))&(exp.variant==r.variant)&(exp.group==r.group)&(exp.endpoint==r.endpoint)]
 key='il1r1_status' if r.experiment==2 else 'population';A,Blabel=r.contrast.split(' minus ');v=s[s[key]==A].pseudobulk_mean_log2_CPM1.values;w=s[s[key]==Blabel].pseudobulk_mean_log2_CPM1.values
 close(v.mean()-w.mean(),r.difference_of_library_means,'contrast');close(min(v)-max(w),r.cross_library_min,'range minimum');close(max(v)-min(w),r.cross_library_max,'range maximum')
# Derive the held-out likelihood from scipy.stats independently of production formulas.
cl=pd.read_csv(cache/'clones/clone_measurements.csv.gz');cl=cl[cl.size_valid];fit=pd.read_csv(HERE/'trials/batch1/clones/model_LOMO_by_mouse.csv')
for r in fit.itertuples():
 d=cl[(cl.dataset==r.dataset)&(cl.mouse_id==r.heldout_mouse)]
 if r.channel!='combined_YFP_RFP':d=d[d.channel==r.channel]
 x=d.loc[d['size']>=2,'size'].to_numpy()-2
 if r.sensitivity=='within_mouse_trim99':x=x[x<=np.quantile(x,.99)]
 theta=json.loads(r.parameters_json)
 if r.model=='shifted_geometric':lp=geom.logpmf(x+1,theta[0])
 elif r.model=='shifted_negative_binomial':lp=nbinom.logpmf(x,theta[0],theta[1])
 else:lp=np.logaddexp(np.log(theta[0])+geom.logpmf(x+1,theta[1]),np.log1p(-theta[0])+geom.logpmf(x+1,theta[2]))
 close(-lp.mean(),r.heldout_mean_NLL,'heldout likelihood',1e-9)
z=zipfile.ZipFile(args.archive);name=next(n for n in z.namelist() if n.endswith('/clone_sizes_total.mat'));data=loadmat(io.BytesIO(z.read(name)))['clone_sizes_total'].ravel();total=sum(len(np.asarray(lobe).ravel()) for dataset in data for mouse in dataset.ravel() for lobe in mouse.ravel());close(total,len(pd.read_csv(cache/'clones/clone_measurements.csv.gz')),'archive clone total')
for branch in ['rna','clones']:
 record=json.loads((HERE/f'trials/batch1/{branch}/run_record.json').read_text());require(record['contract_sha256']==hashlib.sha256((HERE/'config/batch1_contract.json').read_bytes()).hexdigest(),'contract hash')
 for f in record['outputs']:require(hashlib.sha256((HERE/f"trials/batch1/{branch}/{f['file']}").read_bytes()).hexdigest()==f['sha256'],'output hash')
result={'passed':True,'checks':checks,'max_absolute_arithmetic_difference':worst,'source_matrix_rechecks':4,'clone_likelihoods_recomputed':len(fit),'limits':'Verifies arithmetic/joins and recorded bytes; does not verify unresolved biological pool identity, prove state identity, or independently optimize the clonal likelihoods.'}
(HERE/'trials/batch1/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
