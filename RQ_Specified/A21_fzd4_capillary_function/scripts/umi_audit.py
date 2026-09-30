from pathlib import Path
import json,h5py,numpy as np,pandas as pd
b=Path(__file__).resolve().parents[1];m=pd.read_csv(b/'cache/godoy_endothelial_metadata.csv.gz',index_col=0);rows=[]
for pool,filename in [('PoolA','GSM6466253_pool_A_filtered_feature_bc_matrix.h5'),('PoolB','GSM6466255_pool_B_filtered_feature_bc_matrix.h5'),('PoolC','GSM6466257_pool_C_filtered_feature_bc_matrix.h5')]:
 with h5py.File(b/'cache'/filename) as f:
  a=f['matrix'];ptr=a['indptr'][:];data=a['data'][:];ids=a['indices'][:];nb=len(a['barcodes']);ng=len(a['features/name']);ncell=np.bincount(ids,minlength=ng);names=[x.decode() for x in a['features/name'][:]];bc={pool+'_'+v.decode().removesuffix('-1'):i for i,v in enumerate(a['barcodes'][:])}
  for cell,r in m[m['orig.ident'].eq(pool)].iterrows():
   j=bc[cell];lo,hi=ptr[j],ptr[j+1];v=data[lo:hi];gi=ids[lo:hi]
   rows.append(dict(cell=cell,pool=pool,raw=int(v.sum()),author=float(r.nCount_RNA),filtered_ge3=int(v[ncell[gi]>=3].sum()),genes_raw=len(v),genes_author=float(r.nFeature_RNA)))
d=pd.DataFrame(rows);d.to_csv(b/'tables/umi_denominator_audit.tsv',sep='\t',index=False)
summary=dict(cells=len(d),raw_equal=int((d.raw==d.author).sum()),min_delta=float((d.raw-d.author).min()),max_delta=float((d.raw-d.author).max()),median_delta=float((d.raw-d.author).median()),filtered_ge3_equal=int((d.filtered_ge3==d.author).sum()),raw_author_correlation=float(d.raw.corr(d.author)))
(b/'reports/umi_denominator_audit.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
print(d.loc[d.raw.ne(d.author)].head(5).to_string(index=False))
