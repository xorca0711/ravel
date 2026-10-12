import time,resource,json,hashlib,importlib.metadata as md,platform,pathlib
start=time.monotonic()
import numpy as np,pandas as pd,scipy.sparse as sp,anndata as ad,scanpy as sc
import sklearn,igraph,leidenalg,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
rng=np.random.default_rng(731)
x=rng.poisson(rng.gamma(1.2,1.0,(240,2400))).astype(np.int32)
x[rng.random(x.shape)<.72]=0
x[:80,:50]+=rng.poisson(3,(80,50));x[80:160,50:100]+=rng.poisson(3,(80,50));x[160:,100:150]+=rng.poisson(3,(80,50))
counts=sp.csr_matrix(x);del x
a=ad.AnnData(counts.copy());a.var_names=[('mt-' if i<10 else 'g')+str(i) for i in range(2400)]
a.var['mt']=a.var_names.str.startswith('mt-');a.layers['counts']=counts.copy()
sc.settings.n_jobs=4
sc.pp.calculate_qc_metrics(a,qc_vars=['mt'],percent_top=None,log1p=False,inplace=True)
assert np.array_equal(a.obs.total_counts.to_numpy(),np.asarray(counts.sum(axis=1)).ravel())
metrics={}
for col in ['total_counts','n_genes_by_counts']:
 v=np.log1p(a.obs[col].to_numpy());med=np.median(v);mad=np.median(np.abs(v-med))*1.4826;metrics[col]={'median':float(med),'mad':float(mad),'within_5mad':int(((v>=med-5*mad)&(v<=med+5*mad)).sum())}
mt=a.obs.pct_counts_mt.to_numpy();metrics['pct_mt_upper']=float(min(20,np.median(mt)+3*np.median(np.abs(mt-np.median(mt)))*1.4826))
# Pinned D1 route: official Scanpy Scrublet implementation, no standalone distribution.
s=a.copy();sc.pp.scrublet(s,random_state=0,verbose=False,expected_doublet_rate=.06)
assert np.isfinite(s.obs.doublet_score).all()
assert 'predicted_doublet' in s.obs and np.isfinite(s.uns['scrublet']['threshold'])
sc.pp.normalize_total(a,target_sum=1e4);sc.pp.log1p(a)
assert sp.issparse(a.X)
sc.pp.highly_variable_genes(a,n_top_genes=2000,flavor='seurat_v3',layer='counts')
emb=a[:,a.var.highly_variable].copy()
sc.pp.scale(emb,max_value=10)
sc.tl.pca(emb,n_comps=30,random_state=0)
a.obsm['X_pca']=emb.obsm['X_pca'].copy()
sc.pp.neighbors(a,n_neighbors=30,n_pcs=30,use_rep="X_pca",random_state=0)
sc.tl.leiden(a,resolution=.5,flavor='igraph',n_iterations=2,random_state=0,key_added='leiden_igraph')
sc.tl.leiden(a,resolution=.5,flavor='leidenalg',random_state=0,key_added='leiden_leidenalg')
sc.tl.umap(a,random_state=0,maxiter=100)
assert np.isfinite(a.obsm['X_umap']).all()
fig,ax=plt.subplots();ax.scatter(*a.obsm['X_umap'].T,s=2);fig.savefig('/tmp/synthetic.png');plt.close(fig)
a.write_h5ad('/tmp/synthetic.h5ad');assert ad.read_h5ad('/tmp/synthetic.h5ad').shape==a.shape
result={'status':'PASS','fixture':{'seed':731,'shape':list(counts.shape),'nnz':int(counts.nnz),'csr_sha256':hashlib.sha256(counts.data.tobytes()+counts.indices.tobytes()+counts.indptr.tobytes()).hexdigest()},'qc':metrics,'hvg_count':int(a.var.highly_variable.sum()),'pca_shape':list(a.obsm['X_pca'].shape),'umap_shape':list(a.obsm['X_umap'].shape),'leiden_clusters':{k:int(a.obs[k].nunique()) for k in ['leiden_igraph','leiden_leidenalg']},'scanpy_scrublet_finite_scores':True,'external_scrublet':'excluded: pinned D1 uses the self-contained official scanpy.pp.scrublet API','versions':{n:md.version(n) for n in ['numpy','scipy','pandas','anndata','scanpy','scikit-learn','igraph','leidenalg','matplotlib','scikit-image','scikit-misc']},'python':platform.python_version(),'elapsed_seconds':time.monotonic()-start,'process_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'cgroup':{n:pathlib.Path('/sys/fs/cgroup/'+n).read_text().strip() for n in ['cpu.max','memory.max','memory.swap.max','pids.max','memory.peak']},'scientific_results':False,'full_data_memory_qualified':False,'author_method_equivalence':False}
print(json.dumps(result,indent=2),flush=True)
