"""Frozen A21 extension: family-wide descriptive capillary receptor context."""
from pathlib import Path
import datetime,hashlib,json
import h5py,numpy as np,pandas as pd
BASE=Path(__file__).resolve().parents[1];PARENT=BASE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(df,name):df.to_csv(BASE/'tables'/name,sep='\t',index=False,float_format='%.12g')
def main():
 if (BASE/'reports/family_complete.json').exists():raise SystemExit('Completed run exists; preserve and version before rerunning.')
 cfg=json.loads((BASE/'config/exploratory_v1.json').read_text());genes=cfg['genes']
 meta=pd.read_csv(PARENT/'cache/godoy_endothelial_metadata.csv.gz',index_col=0)
 samples=pd.read_csv(PARENT/'tables/samples.tsv',sep='\t').set_index('animal')
 meta['animal']=meta.Annotation.str.extract(r'Bar(\d+)',expand=False).astype(int);meta['day']=meta.animal.map(samples.day)
 assert meta.index.is_unique and not meta.Doublet.any() and meta.day.notna().all()
 matrices=json.loads((PARENT/'metadata/matrix_manifest.json').read_text());mapping=[]
 # Resolve every symbol and verify all input hashes before extracting expression.
 for rec in matrices:
  path=PARENT/'cache'/rec['file'];assert sha(path)==rec['sha256']
  with h5py.File(path,'r') as f:
   names=np.array([x.decode() for x in f['matrix/features/name'][:]])
   for gene in genes:
    ix=np.flatnonzero(names==gene);assert len(ix)==1,(path.name,gene,len(ix))
    mapping.append(dict(file=path.name,gene=gene,index=int(ix[0])))
 write(pd.DataFrame(mapping),'gene_mapping.tsv')
 X=np.zeros((len(meta),len(genes)),dtype=np.int64);total=np.zeros(len(meta),dtype=np.int64);matched=np.zeros(len(meta),bool)
 for rec in matrices:
  path=PARENT/'cache'/rec['file'];pool='Pool'+path.name.split('pool_')[1][0]
  with h5py.File(path,'r') as f:
   m=f['matrix'];bc={pool+'_'+v.decode().removesuffix('-1'):j for j,v in enumerate(m['barcodes'][:])};mp={r['index']:genes.index(r['gene']) for r in mapping if r['file']==path.name}
   ptr=m['indptr'][:];ind=m['indices'][:];data=m['data'][:]
   assert np.all(data>=0) and np.all(data==np.floor(data))
   for i in np.flatnonzero(meta['orig.ident'].eq(pool)):
    j=bc[meta.index[i]];lo,hi=ptr[j:j+2];total[i]=data[lo:hi].sum()
    for gi,value in zip(ind[lo:hi],data[lo:hi]):
     if int(gi) in mp:X[i,mp[int(gi)]]+=int(value)
    matched[i]=True
 assert matched.all() and (total>0).all()
 oldaudit=pd.read_csv(PARENT/'tables/umi_denominator_audit.tsv',sep='\t').set_index('cell').loc[meta.index]
 assert np.array_equal(total,oldaudit.raw) and np.array_equal(meta.nCount_RNA,oldaudit.author)
 rows=[]
 for kind in ['cluster','coarse']:
  cross={int(k):v for k,v in cfg['clusters'].items()} if kind=='cluster' else {k:g for g,ks in cfg['coarse_groups'].items() for k in ks}
  md=meta.assign(state=meta.seurat_clusters.map(cross),idx=np.arange(len(meta)));assert md.state.notna().all()
  for (animal,day,state),group in md.groupby(['animal','day','state']):
   ii=group.idx.to_numpy();den=int(total[ii].sum());author=int(group.nCount_RNA.sum());counts=X[ii].sum(axis=0)
   for j,gene in enumerate(genes):
    rows.append(dict(kind=kind,animal=animal,day=day,state=state,cells=len(ii),total_umi=den,author_denominator=author,gene=gene,counts=int(counts[j]),detected_cells=int((X[ii,j]>0).sum()),detection=float((X[ii,j]>0).mean()),cpm=float(counts[j]/den*1e6),log2cpm=float(np.log2(counts[j]/den*1e6+1)),author_log2cpm=float(np.log2(counts[j]/author*1e6+1))))
 expr=pd.DataFrame(rows);write(expr,'unit_expression.tsv')
 old=pd.read_csv(PARENT/'tables/unit_expression.tsv',sep='\t');joint=expr.merge(old,on=['kind','animal','day','state','gene'],suffixes=('_new','_old'),validate='one_to_one')
 assert len(joint)==len(old)
 for col in ['counts','cells','total_umi','detected_cells']:assert np.array_equal(joint[col+'_new'],joint[col+'_old'])
 assert np.allclose(joint.log2cpm_new,joint.log2cpm_old,atol=1e-9,rtol=1e-10)
 paired=[];eligibility=[]
 for floor in cfg['floors']:
  for con in cfg['contrasts']:
   z=expr[expr.kind.eq(con['kind'])&expr.cells.ge(floor)]
   d=z[z.state.eq(con['left'])].merge(z[z.state.eq(con['right'])],on=['kind','animal','day','gene'],suffixes=('_left','_right'),validate='one_to_one')
   d['delta']=d.log2cpm_left-d.log2cpm_right;d['author_delta']=d.author_log2cpm_left-d.author_log2cpm_right;d['contrast']=con['id'];d['cell_floor']=floor;paired.append(d)
   for day in cfg['days']:eligibility.append(dict(contrast=con['id'],cell_floor=floor,day=day,n=int(d[d.day.eq(day)].animal.nunique())))
 paired=pd.concat(paired,ignore_index=True);write(paired,'paired_differences.tsv');write(pd.DataFrame(eligibility),'eligibility.tsv')
 summary=paired.groupby(['contrast','cell_floor','day','gene']).agg(n=('animal','size'),mean=('delta','mean'),median=('delta','median'),minimum=('delta','min'),maximum=('delta','max'),positive=('delta',lambda x:int((x>0).sum())),negative=('delta',lambda x:int((x<0).sum())),detected_left=('detected_cells_left','sum'),detected_right=('detected_cells_right','sum'),counts_left=('counts_left','sum'),counts_right=('counts_right','sum'),author_mean=('author_delta','mean')).reset_index()
 summary['same_denominator_direction']=np.sign(summary['mean'])==np.sign(summary.author_mean);write(summary,'contrast_summary.tsv')
 candidates=[];dayflags=[]
 for gene in [f'Fzd{i}' for i in range(1,11) if i!=4]:
  tally={}
  for floor in cfg['floors']:
   z=summary[summary.gene.eq(gene)&summary.contrast.eq('transitional1_minus_gCap0')&summary.cell_floor.eq(floor)&summary.day.ne(0)].copy()
   z['passes']=(z.n>=2)&(z['mean']>0)&(z.positive/z.n>=2/3)&(z.detected_left>=5)
   dayflags.append(z);tally[floor]=int(z.passes.sum())
  candidates.append(dict(gene=gene,injury_days_floor20=tally[20],injury_days_floor10=tally[10],injury_days_floor50=tally[50],rna_nominee=tally[20]>=2 and tally[10]>=2,independently_validated=False))
 write(pd.concat(dayflags,ignore_index=True),'candidate_day_gates.tsv');write(pd.DataFrame(candidates),'candidate_summary.tsv')
 record=dict(finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),config_sha256=sha(BASE/'config/exploratory_v1.json'),cells=len(meta),animals=int(meta.animal.nunique()),genes=len(genes),prior_rows_reconciled=len(joint),expression_rows=len(expr),pair_rows=len(paired),denominator_directions_agree=int(summary.same_denominator_direction.sum()),denominator_directions_total=len(summary),rna_nominees=[r['gene'] for r in candidates if r['rna_nominee']],functional_effect_estimated=False)
 (BASE/'reports/family_complete.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
 print(pd.DataFrame(candidates).to_string(index=False))
if __name__=='__main__':main()
