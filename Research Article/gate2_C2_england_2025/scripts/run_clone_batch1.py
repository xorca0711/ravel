"""England clonal re-analysis: mouse-nested sizes, pooled spatial descriptions."""
from __future__ import annotations
import argparse,sys,io,zipfile,json,hashlib,datetime,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--data-root',type=Path,required=True);p.add_argument('--archive',type=Path,required=True);a=p.parse_args()
sys.path.insert(0,str(a.data_root/'.venv-x64/Lib/site-packages'))
import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy.optimize import minimize
from scipy.special import gammaln,logsumexp
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
OUT=HERE/'trials/batch1/clones';CACHE=HERE/'processed/batch1/clones';OUT.mkdir(parents=True,exist_ok=True);CACHE.mkdir(parents=True,exist_ok=True)
assert not (OUT/'run_record.json').exists(),'Refuse completed-run overwrite'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'contract_sha256':sha(HERE/'config/batch1_contract.json'),'script_sha256':sha(Path(__file__)),'archive_sha256':sha(a.archive),'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}
assert record['archive_sha256']=='404697263ca941b1b74dee9feb4c4680ff3077d9e20bb7105482d17f14e96a70'
(OUT/'started.json').write_text(json.dumps(record,indent=2))
z=zipfile.ZipFile(a.archive)
def read(name,simplify=False):return loadmat(io.BytesIO(z.read(next(n for n in z.namelist() if n.endswith('/'+name+'.mat')))),simplify_cells=simplify)[name]
names=read('datasets',True);times=read('time_points',True);channels=read('chlbls',True)
cs=read('clone_sizes_total').ravel();spc=read('clone_sizes_SPC_pos').ravel();areas=read('lobe_area_total').ravel()
rows=[];schemas=[]
for di,(name,t) in enumerate(zip(names,times)):
 mice=cs[di].ravel();mspc=spc[di].ravel();mar=areas[di].ravel()
 assert len(mice)==len(mspc)==len(mar)
 for mi,(mx,sx,ar) in enumerate(zip(mice,mspc,mar)):
  assert mx.shape==sx.shape and mx.shape[1]==2
  ar=np.asarray(ar).ravel();assert len(ar)==mx.shape[0]
  schemas.append({'dataset':name,'week':t,'mouse_index':mi,'mouse_id':f'{name}:m{mi+1}','lobes':mx.shape[0],'channel_order':'YFP,RFP','sum_lobe_area_source_units':float(ar.sum())})
  for li in range(mx.shape[0]):
   for ci,channel in enumerate(channels):
    sizes=np.asarray(mx[li,ci]).ravel();pos=np.asarray(sx[li,ci]).ravel();assert len(sizes)==len(pos)
    for j,(n,s) in enumerate(zip(sizes,pos)):
     rows.append({'dataset':name,'week':float(t),'mouse_id':f'{name}:m{mi+1}','lobe_index':li,'channel':channel,'clone_index':j,'size':float(n),'spc_positive_estimate':float(s),'spc_valid':bool(np.isfinite(s) and 0<=s<=n),'size_valid':bool(np.isfinite(n) and n>=1)})
clones=pd.DataFrame(rows);clones.to_csv(CACHE/'clone_measurements.csv.gz',index=False);pd.DataFrame(schemas).to_csv(OUT/'mouse_schema.csv',index=False)
clones=clones[clones.size_valid].copy();assert np.all(clones['size']==np.floor(clones['size'])),'Integer support gate failed'
clones['analysis_channel']=np.where(clones.dataset.str.startswith('conf'),'combined_YFP_RFP',clones.channel)
stats=[];ccdf=[];groups={}
for (ds,ch,mouse),d in clones.groupby(['dataset','analysis_channel','mouse_id']):
 n=d['size'].to_numpy();valid=d.spc_valid.to_numpy();pos=d.spc_positive_estimate.to_numpy();n2=n[n>=2];k=max(1,int(np.ceil(.1*len(n))))
 stats.append({'dataset':ds,'week':float(d.week.iloc[0]),'channel':ch,'mouse_id':mouse,'clones':len(n),'proliferative_clones':len(n2),'mean_size_all':float(n.mean()),'mean_size_ge2':float(n2.mean()) if len(n2) else np.nan,'median_size_all':float(np.median(n)),'p90_size_all':float(np.quantile(n,.9)),'singlet_fraction':float((n==1).mean()),'top10percent_clone_cell_share':float(np.sort(n)[-k:].sum()/n.sum()),'spc_invalid_clones':int((~valid).sum()),'spc_negative_cell_fraction_valid_clones':float((n[valid].sum()-pos[valid].sum())/n[valid].sum()) if valid.any() else np.nan,'mean_clone_spc_negative_fraction_valid':float(np.mean(1-pos[valid]/n[valid])) if valid.any() else np.nan})
 if len(n2):
  for v in np.unique(n2):ccdf.append({'dataset':ds,'channel':ch,'mouse_id':mouse,'size':int(v),'probability_size_ge':float((n2>=v).mean()),'conditioning':'size>=2'})
  groups.setdefault((ds,ch),{})[mouse]=n2.astype(int)-2
pd.DataFrame(stats).to_csv(OUT/'clone_summary_by_mouse.csv',index=False);pd.DataFrame(ccdf).to_csv(OUT/'clone_CCDF_by_mouse.csv',index=False)
# All models share x=n-2 >=0. The negative-binomial competitor is a gamma-Poisson
# distribution of extra cells, not a mechanistic branching-model claim.
def logp(model,theta,x):
 if model=='shifted_geometric':
  p=theta[0];return np.log(p)+x*np.log1p(-p)
 if model=='two_shifted_geometric_mixture':
  w,p,q=theta;return logsumexp(np.array([np.log(w)+np.log(p)+x*np.log1p(-p),np.log1p(-w)+np.log(q)+x*np.log1p(-q)]),axis=0)
 r,p=theta;return gammaln(x+r)-gammaln(r)-gammaln(x+1)+r*np.log(p)+x*np.log1p(-p)
def fit(model,train):
 maxx=max(int(v.max()) for v in train);x=np.arange(maxx+1);weights=np.mean([np.bincount(v,minlength=maxx+1)/len(v) for v in train],axis=0);mu=float(weights@x)
 def objective(t):return -float(weights@logp(model,t,x))
 if model=='shifted_geometric':theta=[float(np.clip(1/(mu+1),1e-7,1-1e-7))];return theta,objective(theta),True
 if model=='two_shifted_geometric_mixture':starts=[[.2,.05,.5],[.5,.1,.8],[.8,.03,.3]];bounds=[(.001,.999),(1e-7,1-1e-7),(1e-7,1-1e-7)]
 else:starts=[[.3,.3/(.3+mu)],[1,1/(1+mu)],[5,5/(5+mu)]];bounds=[(.0001,10000),(1e-7,1-1e-7)]
 fits=[minimize(objective,s,bounds=bounds,method='L-BFGS-B',options={'maxiter':1000}) for s in starts]
 best=min(fits,key=lambda r:r.fun);return best.x.tolist(),float(best.fun),bool(best.success)
fits=[]
for (ds,ch),mice in groups.items():
 week=float(next(r['week'] for r in stats if r['dataset']==ds))
 if (ds.startswith('conf') and week<12) or (ds.startswith('kras') and week<1) or len(mice)<3:continue
 for sensitivity in ['full_ge2','within_mouse_trim99']:
  selected={m:v if sensitivity=='full_ge2' else v[v<=np.quantile(v,.99)] for m,v in mice.items()}
  for heldout,test in selected.items():
   train=[v for m,v in selected.items() if m!=heldout]
   for model in ['shifted_geometric','two_shifted_geometric_mixture','shifted_negative_binomial']:
    theta,nll,success=fit(model,train);held=-float(logp(model,theta,test).mean())
    fits.append({'dataset':ds,'week':week,'channel':ch,'sensitivity':sensitivity,'heldout_mouse':heldout,'model':model,'n_training_mice':len(train),'n_heldout_clones':len(test),'training_equal_mouse_NLL':nll,'heldout_mean_NLL':held,'converged':success,'parameters_json':json.dumps(theta)})
 print('Clone models:',ds,ch,len(mice),'mice',flush=True)
f=pd.DataFrame(fits);f.to_csv(OUT/'model_LOMO_by_mouse.csv',index=False)
f.groupby(['dataset','channel','sensitivity','model'],as_index=False).agg(mean_heldout_NLL=('heldout_mean_NLL','mean'),mice=('heldout_mouse','nunique'),all_converged=('converged','all')).to_csv(OUT/'model_LOMO_summary.csv',index=False)
# The archive has pooled distances; retain this limitation in every output row.
spatial={k:read(k).ravel() for k in ['all_ds','all_nv_cent','all_nv_neigh','all_nv_neigh_spc']};spatialrows=[];schema=[]
for i,ds in enumerate(names):
 d=np.asarray(spatial['all_ds'][i]).ravel();central=np.asarray(spatial['all_nv_cent'][i]).ravel();near=np.asarray(spatial['all_nv_neigh'][i]).ravel();positive=np.asarray(spatial['all_nv_neigh_spc'][i]).ravel()
 assert len(d)==len(central)==len(near)==len(positive)
 valid=np.isfinite(d)&(d>=0)&(d<=1500)&(near>0)&(positive>=0)&(positive<=near)
 schema.append({'dataset':ds,'pair_rows':len(d),'eligible_pair_rows':int(valid.sum()),'mouse_id_available':False,'unique_clone_id_available':False,'distance_unit':'micrometres_as_labeled_in_author_script'})
 for low in np.arange(0,1500,50):
  m=valid&(d>=low)&(d<low+50 if low<1450 else d<=1500)
  if not m.any():continue
  spatialrows.append({'dataset':ds,'distance_low_um':low,'distance_high_um':low+50,'pair_rows':int(m.sum()),'mean_neighbor_size':float(near[m].mean()),'median_neighbor_size':float(np.median(near[m])),'mean_central_size':float(central[m].mean()),'mean_neighbor_spc_negative_fraction':float((1-positive[m]/near[m]).mean()),'pooled_only':True,'biological_inference_allowed':False})
pd.DataFrame(spatialrows).to_csv(OUT/'spatial_pooled_bin_profiles.csv',index=False);pd.DataFrame(schema).to_csv(OUT/'spatial_identity_gate.csv',index=False)
record.update(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),clone_rows=len(rows),source_indexed_mice=len(schemas),spatial_inference='blocked: no mouse/clone IDs in the supplied distance arrays',outputs=[{'file':p.name,'sha256':sha(p)} for p in OUT.glob('*.csv')])
(OUT/'run_record.json').write_text(json.dumps(record,indent=2)+'\n');print('Clone batch complete:',len(rows),'clones;',len(schemas),'source-indexed mice',flush=True)
