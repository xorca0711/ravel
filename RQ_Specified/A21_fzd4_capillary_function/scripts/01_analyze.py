"""A21 frozen independent expression context; no receptor-effect inference."""
from pathlib import Path
import csv,datetime,gzip,hashlib,io,json,re,tarfile
import h5py,numpy as np,pandas as pd
from scipy.stats import spearmanr
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(df,name):df.to_csv(BASE/'tables'/name,sep='\t',index=False,float_format='%.12g')
def main():
 if (BASE/'reports/analysis_complete.json').exists():raise SystemExit('Completed run exists; version before rerun.')
 cfg=json.loads((BASE/'config/exploratory_v1.json').read_text())
 genes=sum(cfg['genes'].values(),[]);assert len(genes)==len(set(genes))
 records=json.loads((BASE/'metadata/intake.json').read_text())
 for name in ['GSE211335_RAW.tar','godoy_samples.txt.gz','godoy_endothelial_metadata.csv.gz']:
  r=next(r for r in records if r['file']==name and r['status']=='retrieved');assert sha(BASE/'cache'/name)==r['sha256']
 meta=pd.read_csv(BASE/'cache/godoy_endothelial_metadata.csv.gz',index_col=0)
 assert meta.index.is_unique and not meta.Doublet.any()
 meta['animal']=meta.Annotation.str.extract(r'Bar(\d+)',expand=False).astype(int)
 raw_samples=gzip.decompress((BASE/'cache/godoy_samples.txt.gz').read_bytes()).decode().replace('\r','')
 rr=list(csv.reader(io.StringIO(raw_samples),delimiter='\t'));samples=[]
 for r in rr[2:]:
  if not r or not r[0]:continue
  animal=int(re.search(r'Barcode (\d+)',r[0]).group(1))
  day=int(re.search(r'Treatment (\d+) days',r[1]).group(1)) if 'Treatment' in r[1] else 0
  samples.append(dict(animal=animal,day=day,source_title=r[1],barcode_id=r[3],biological_sample_label=r[1].split('Biological sample ')[1]))
 sample=pd.DataFrame(samples);assert len(sample)==12 and sample.groupby('day').size().eq(3).all()
 meta=meta.merge(sample[['animal','day']],on='animal',how='left',validate='many_to_one').set_axis(meta.index)
 assert set(meta.animal)==set(sample.animal)
 source_day=meta.Sample.str.extract(r'(\d+)d',expand=False).fillna(0).astype(int)
 assert np.array_equal(source_day,meta.day)
 write(sample,'samples.tsv')
 X=np.zeros((len(meta),len(genes)),dtype=np.int64);tot=np.zeros(len(meta),dtype=np.int64);matched=np.zeros(len(meta),dtype=bool);maps=[];matrix_records=[]
 with tarfile.open(BASE/'cache/GSE211335_RAW.tar') as tar:
  for member in tar.getmembers():
   pool='Pool'+re.search(r'pool_([ABC])_',member.name).group(1)
   path=BASE/'cache'/Path(member.name).name
   if not path.exists():path.write_bytes(tar.extractfile(member).read())
   with h5py.File(path,'r') as f:
    m=f['matrix'];names=np.array([v.decode() for v in m['features/name'][:]]);barcodes=[v.decode().removesuffix('-1') for v in m['barcodes'][:]]
    positions=[]
    for g in genes:
     ix=np.flatnonzero(names==g);assert len(ix)==1,(g,len(ix));positions.append(int(ix[0]))
    target=dict(zip(positions,range(len(genes))))
    bc={pool+'_'+v:i for i,v in enumerate(barcodes)};ii=np.flatnonzero(meta['orig.ident'].eq(pool))
    ptr=m['indptr'][:];data=m['data'][:];ind=m['indices'][:]
    assert np.all(data>=0) and np.all(data==np.floor(data))
    for i in ii:
     key=meta.index[i];assert key in bc,key;j=bc[key];lo,hi=int(ptr[j]),int(ptr[j+1]);values=data[lo:hi];ids=ind[lo:hi]
     tot[i]=values.sum()
     for ident,value in zip(ids,values):
      k=target.get(int(ident))
      if k is not None:X[i,k]+=int(value)
     matched[i]=True
    maps += [dict(pool=pool,gene=g,feature_index=j) for g,j in zip(genes,positions)]
    matrix_records.append(dict(file=path.name,sha256=sha(path),features=len(names),barcodes=len(barcodes),endothelial_cells=len(ii)))
 assert matched.all() and (tot>0).all()
 audit=pd.read_csv(BASE/'tables/umi_denominator_audit.tsv',sep='\t').set_index('cell').loc[meta.index]
 assert np.array_equal(tot,audit.raw) and np.array_equal(meta.nCount_RNA,audit.author),'Independent denominator audit reconciliation'
 write(pd.DataFrame(maps),'gene_mapping.tsv')
 meta['total_umi']=tot;meta['cell']=meta.index
 # Exact per-cell extraction is regenerable; source identities/hashes are tracked.
 cell=meta[['cell','animal','day','orig.ident','seurat_clusters','Annotation','Sample','total_umi']].copy()
 for j,g in enumerate(genes):cell[g]=X[:,j]
 cell.to_csv(BASE/'cache/selected_cells.tsv.gz',sep='\t',index=False)
 groups=[]
 for kind in ['cluster','coarse']:
  state=meta.seurat_clusters.map({int(k):v for k,v in cfg['clusters'].items()}) if kind=='cluster' else meta.seurat_clusters.map({k:g for g,ks in cfg['coarse_groups'].items() for k in ks})
  assert state.notna().all()
  d=meta.assign(state=state,idx=np.arange(len(meta)))
  for (animal,day,s),z in d.groupby(['animal','day','state']):
   ii=z.idx.to_numpy();counts=X[ii].sum(axis=0);den=tot[ii].sum();author_den=int(meta.nCount_RNA.iloc[ii].sum())
   for j,g in enumerate(genes):
    groups.append(dict(kind=kind,animal=animal,day=day,state=s,cells=len(ii),total_umi=int(den),gene=g,counts=int(counts[j]),cpm=float(counts[j]/den*1e6),log2cpm=float(np.log2(counts[j]/den*1e6+1)),detected_cells=int((X[ii,j]>0).sum()),detection=float((X[ii,j]>0).mean()),author_denominator=author_den,author_denominator_log2cpm=float(np.log2(counts[j]/author_den*1e6+1))))
 expr=pd.DataFrame(groups);write(expr,'unit_expression.tsv')
 cov=expr[['kind','animal','day','state','cells','total_umi']].drop_duplicates();write(cov,'coverage.tsv')
 pool=meta.groupby(['animal','day','orig.ident']).size().reset_index(name='cells');write(pool,'technical_pool_coverage.tsv')
 features=expr.rename(columns={'gene':'feature','log2cpm':'value'})[['kind','animal','day','state','cells','feature','value']].copy()
 for name,gs in cfg['panels'].items():
  pan=expr[expr.gene.isin(gs)].groupby(['kind','animal','day','state','cells']).agg(value=('log2cpm','mean'),genes=('gene','size')).reset_index()
  assert pan.genes.eq(len(gs)).all();pan['feature']=name;features=pd.concat([features,pan[features.columns]],ignore_index=True)
 write(features,'unit_features.tsv')
 definitions=[('gCap_minus_aCap','coarse','gCap','aCap'),('transitional1_minus_gCap0','cluster','gCap_transitional_1','gCap_0'),('cycling7_minus_gCap0','cluster','gCap_cycling_7','gCap_0')]
 pairs=[];eligible=[]
 for floor in [cfg['primary_cell_floor']]+cfg['sensitivity_floors']:
  for contrast,kind,left,right in definitions:
   z=features[features.kind.eq(kind)&features.cells.ge(floor)]
   p=z[z.state.eq(left)].merge(z[z.state.eq(right)],on=['kind','animal','day','feature'],suffixes=('_left','_right'),validate='one_to_one')
   p['delta']=p.value_left-p.value_right;p['contrast']=contrast;p['cell_floor']=floor;pairs.append(p)
   for day in cfg['days']:
    q=p[p.day.eq(day)];eligible.append(dict(contrast=contrast,cell_floor=floor,day=day,paired_animals=q.animal.nunique()))
 pairs=pd.concat(pairs,ignore_index=True);write(pairs,'paired_differences.tsv');write(pd.DataFrame(eligible),'eligibility.tsv')
 alt=expr.rename(columns={'gene':'feature','author_denominator_log2cpm':'alt_value'})[['kind','animal','day','state','feature','alt_value']].copy()
 for name,gs in cfg['panels'].items():
  z=expr[expr.gene.isin(gs)].groupby(['kind','animal','day','state']).author_denominator_log2cpm.mean().reset_index(name='alt_value');z['feature']=name;alt=pd.concat([alt,z],ignore_index=True)
 sens=pairs.merge(alt.rename(columns={'state':'state_left','alt_value':'alt_left'}),on=['kind','animal','day','feature','state_left'],validate='many_to_one').merge(alt.rename(columns={'state':'state_right','alt_value':'alt_right'}),on=['kind','animal','day','feature','state_right'],validate='many_to_one')
 sens['alt_delta']=sens.alt_left-sens.alt_right
 sens=sens.groupby(['contrast','cell_floor','day','feature']).agg(primary_mean=('delta','mean'),author_denominator_mean=('alt_delta','mean')).reset_index()
 sens['same_direction']=np.sign(sens.primary_mean)==np.sign(sens.author_denominator_mean);write(sens,'normalization_sensitivity.tsv')
 summary=pairs.groupby(['contrast','cell_floor','day','feature']).delta.agg(n='size',mean='mean',median='median',minimum='min',maximum='max',positive=lambda x:int((x>0).sum()),negative=lambda x:int((x<0).sum())).reset_index();write(summary,'contrast_summary.tsv')
 assoc=[];points=[]
 for floor in [cfg['primary_cell_floor']]+cfg['sensitivity_floors']:
  for kind,state in [('coarse','gCap'),('cluster','gCap_0')]:
   z=features[features.kind.eq(kind)&features.state.eq(state)&features.cells.ge(floor)].pivot(index=['animal','day'],columns='feature',values='value').reset_index()
   q=expr[expr.kind.eq(kind)&expr.state.eq(state)&expr.gene.eq('Fzd4')][['animal','day','cpm','detection']]
   z=z.merge(q,on=['animal','day'],validate='one_to_one');z['state']=state;z['cell_floor']=floor
   points.append(z[['animal','day','state','cell_floor','cpm','detection','cycling']])
   for day in cfg['days']:
    w=z[z.day.eq(day)];n=len(w);valid=n>=3 and w.cpm.nunique()>1 and w.cycling.nunique()>1
    rho=float(spearmanr(w.cpm,w.cycling).statistic) if valid else np.nan
    assoc.append(dict(state=state,day=day,cell_floor=floor,animals=n,rho=rho,status='descriptive_n3' if valid else 'insufficient_or_constant'))
 write(pd.concat(points,ignore_index=True),'association_inputs.tsv');write(pd.DataFrame(assoc),'within_day_associations.tsv')
 old=ROOT/'Research Article/gate2_N1_nabhan_2023/branch_analysis/trials/extension_v1/tables'
 sm=pd.read_csv(old/'mouse_sample_context.tsv',sep='\t');sm=sm[sm.day.eq(42)].copy();assert len(sm)==8 and sm.unit.is_unique
 sm['tracing_label_day']=sm.geo_sample_name.str.extract(r'tam(\d+)',expand=False).astype(int);assert (sm.sex_x.str.upper()==sm.sex_y).all()
 oldpoints=pd.read_csv(old/'vascular_rival_inputs.tsv',sep='\t');oldpoints=oldpoints[oldpoints.state.eq('CAP1')&oldpoints.panel.eq('cycling')]
 prior=sm.merge(oldpoints[['unit','score','cpm','detection']],on='unit',validate='one_to_one');assert len(prior)==8
 prior['cycling_panel']=prior.pop('score');write(prior,'prior_day42_cohort.tsv')
 oldrho=pd.read_csv(old/'vascular_depth_round_audit.tsv',sep='\t')
 for scope,w in [('pooled',prior)]+list(prior.groupby('round')):
  expect=oldrho[(oldrho.state=='CAP1')&(oldrho.program=='cycling')&(oldrho.measurement=='cpm')&(oldrho.scope==scope)].rho.iloc[0]
  assert np.isclose(spearmanr(w.cpm,w.cycling_panel).statistic,expect)
 (BASE/'metadata/matrix_manifest.json').write_text(json.dumps(matrix_records,indent=2)+'\n')
 report=dict(finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),config_sha256=sha(BASE/'config/exploratory_v1.json'),animals=12,conditions=4,technical_pools=3,endothelial_cells=len(meta),genes=len(genes),raw_umi_matches_author_metadata=False,denominator_audit_reconciled=True,normalization_sign_agreement=int(sens.same_direction.sum()),normalization_comparisons=len(sens),prior_day42_units_reconciled=8,no_functional_Fzd4_test=True)
 (BASE/'reports/analysis_complete.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
 print(summary[(summary.feature=='Fzd4')&(summary.cell_floor==20)].to_string(index=False))
 print(pd.DataFrame(assoc).query('cell_floor==20').to_string(index=False))
if __name__=='__main__':main()
