"""Frozen exploratory A20 paired context analysis; no perturbation-effect fit."""
from pathlib import Path
import argparse,datetime,hashlib,json
import anndata as ad
import h5py,numpy as np,pandas as pd
from scipy import sparse
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
CFG=json.loads((BASE/'config/exploratory_v1.json').read_text())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
def write(df,name):df.to_csv(BASE/'tables'/name,sep='\t',index=False,float_format='%.12g')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--data-root',type=Path,default=Path(CFG['data_root']));args=parser.parse_args()
 if (BASE/'reports/analysis_complete.json').exists():raise SystemExit('Completed run exists: preserve/version results before rerunning.')
 path=args.data_root/CFG['input'];genes=sorted(set(sum([CFG[k] for k in ['crosswalk_markers','receptors','support_genes','matrix_genes']],[])))
 # Record source and prior-package identities before extracting new values.
 a19=ROOT/'RQ_Specified/A19_fzd_response_reversibility'
 prior={str(p.relative_to(a19)).replace('\\','/'):sha(p) for p in a19.rglob('*') if p.is_file() and 'cache' not in p.relative_to(a19).parts and '__pycache__' not in p.parts}
 (BASE/'metadata/a19_preservation.json').write_text(json.dumps(prior,indent=2)+'\n')
 provenance=dict(input=str(path),input_sha256=sha(path),config_sha256=sha(BASE/'config/exploratory_v1.json'),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 with h5py.File(path,'r') as f:
  obs=ad.io.read_elem(f['obs']);var=ad.io.read_elem(f['var'])
  symbols=pd.Index(var.gene_symbol.astype(str));assert symbols.is_unique
  pos=symbols.get_indexer(genes);assert (pos>=0).all(),[genes[i] for i in np.where(pos<0)[0]]
  write(pd.DataFrame(dict(gene=genes,index=pos)),'gene_mapping.tsv')
  meta=pd.DataFrame(dict(unit=obs.sample_id.astype(str).to_numpy(),state=obs.author_celltype.astype(str).to_numpy(),day=obs.sacrifice_day.to_numpy(),condition=obs.condition.astype(str).to_numpy(),doublet=obs.predicted_doublet.to_numpy(),idx=np.arange(len(obs))))
  select=meta.state.isin(CFG['states']) & meta.condition.ne('unannotated')
  chosen=meta.loc[select].copy();indices=chosen.idx.to_numpy();xx=np.zeros((len(chosen),len(genes)),dtype=np.int64);tot=np.zeros(len(chosen),dtype=np.int64)
  layer=f['layers/counts'];assert layer.attrs['encoding-type']=='csr_matrix';ptr=layer['indptr'][:]
  for start in range(0,len(obs),4096):
   stop=min(start+4096,len(obs));local=np.flatnonzero((indices>=start)&(indices<stop))
   if not len(local):continue
   lo,hi=ptr[start],ptr[stop];vals=layer['data'][lo:hi]
   assert np.all(vals>=0) and np.all(vals==np.floor(vals))
   block=sparse.csr_matrix((vals,layer['indices'][lo:hi],ptr[start:stop+1]-lo),shape=(stop-start,len(var)))[indices[local]-start]
   tot[local]=np.asarray(block.sum(axis=1)).ravel().astype(np.int64);xx[local]=block[:,pos].toarray().astype(np.int64)
 chosen['local']=np.arange(len(chosen));chosen['umi']=tot;rows=[];coverage=[]
 for mode in CFG['modes']:
  subset=chosen[(chosen.umi>0)&(~chosen.doublet if mode=='doublets_removed' else True)]
  for key,g in subset.groupby(['unit','state','day','condition'],observed=True):
   ii=g.local.to_numpy();counts=xx[ii].sum(axis=0);den=int(tot[ii].sum());cpm=counts/den*1e6
   info=dict(mode=mode,unit=key[0],state=key[1],day=key[2],condition=key[3],cells=len(ii),total_umi=den)
   coverage.append(info)
   rows += [dict(**info,gene=gene,counts=int(counts[j]),cpm=float(cpm[j]),log2cpm=float(np.log2(cpm[j]+1)),detected_cells=int((xx[ii,j]>0).sum()),detection=float((xx[ii,j]>0).mean())) for j,gene in enumerate(genes)]
 expr=pd.DataFrame(rows);cov=pd.DataFrame(coverage);write(expr,'unit_expression.tsv');write(cov,'unit_coverage.tsv')
 prior_base=ROOT/'Research Article/gate2_N1_nabhan_2023/branch_analysis/trials/extension_v1/tables'
 old=pd.read_csv(prior_base/'mouse_unit_expression.tsv.gz',sep='\t');joint=expr.merge(old,on=['mode','unit','state','day','condition','gene'],suffixes=('_new','_old'),validate='one_to_one')
 assert len(joint)>0
 for col in ['counts','cells','total_umi']:assert np.array_equal(joint[col+'_new'],joint[col+'_old'])
 assert np.allclose(joint.cpm_new,joint.cpm_old,rtol=1e-10,atol=1e-8)
 sm=pd.read_csv(prior_base/'mouse_sample_context.tsv',sep='\t');assert sm.unit.is_unique
 write(sm[sm.unit.isin(cov.unit)],'sample_context.tsv')
 feature=expr.rename(columns={'gene':'feature','log2cpm':'value'}).copy();feature['kind']='gene'
 features=[feature]
 for name,gs in CFG['panels'].items():
  z=expr[expr.gene.isin(gs)].groupby(['mode','unit','state','day','condition','cells','total_umi'],observed=True).agg(value=('log2cpm','mean'),n_genes=('gene','size')).reset_index();assert z.n_genes.eq(len(gs)).all();z['feature']=name;z['kind']='panel';features.append(z)
 feature=pd.concat(features,ignore_index=True);write(feature[['mode','unit','state','day','condition','cells','feature','kind','value']],'unit_features.tsv')
 pairs=[];eligibility=[]
 for mode in CFG['modes']:
  for floor in CFG['floors']:
   eligible=cov[cov['mode'].eq(mode)&cov.cells.ge(floor)]
   for day,d in cov[cov['mode'].eq(mode)].groupby('day'):
    a=set(eligible.loc[eligible.day.eq(day)&eligible.state.eq('AF1'),'unit']);b=set(eligible.loc[eligible.day.eq(day)&eligible.state.eq('AF2'),'unit'])
    eligibility.append(dict(mode=mode,cell_floor=floor,day=day,AF1_units=len(a),AF2_units=len(b),paired_units=len(a&b)))
   z=feature[feature['mode'].eq(mode)&feature.cells.ge(floor)&feature.day.eq(CFG['day'])]
   w=z[z.state.eq('AF1')].merge(z[z.state.eq('AF2')],on=['mode','unit','day','condition','feature','kind'],suffixes=('_AF1','_AF2'),validate='one_to_one')
   w['delta']=w.value_AF1-w.value_AF2;w['cell_floor']=floor
   pairs.append(w[['mode','cell_floor','unit','day','condition','feature','kind','cells_AF1','cells_AF2','value_AF1','value_AF2','delta']])
 paired=pd.concat(pairs,ignore_index=True).merge(sm[['unit','round','genotype']],on='unit',validate='many_to_one');write(paired,'paired_differences.tsv');write(pd.DataFrame(eligibility),'eligibility.tsv')
 summary=paired.groupby(['mode','cell_floor','feature','kind'],observed=True).agg(n=('unit','nunique'),median=('delta','median'),minimum=('delta','min'),maximum=('delta','max'),positive=('delta',lambda v:int((v>0).sum())),negative=('delta',lambda v:int((v<0).sum()))).reset_index();write(summary,'paired_summary.tsv')
 provenance.update(finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_sha256_unchanged=(sha(path)==provenance['input_sha256']),overlap_rows_reconciled=len(joint),total_AF1_AF2_cells=len(chosen),gene_count=len(genes),primary_pairs=int(len(paired[paired['mode'].eq(CFG['primary_mode'])&paired.cell_floor.eq(CFG['primary_floor'])].unit.unique())),interpretation='RNA context only; H1/H2 functional estimands not identified')
 assert provenance['source_sha256_unchanged']
 (BASE/'reports/analysis_complete.json').write_text(json.dumps(provenance,indent=2)+'\n')
 print(json.dumps({k:provenance[k] for k in ['total_AF1_AF2_cells','gene_count','overlap_rows_reconciled','primary_pairs']}))
 print(summary[summary['mode'].eq(CFG['primary_mode'])&summary.cell_floor.eq(CFG['primary_floor'])][['feature','n','median','minimum','maximum','positive']].to_string(index=False))
if __name__=='__main__':main()
