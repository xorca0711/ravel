"""Full entry-integrity and technical QC for all deposited libraries; no annotation."""
import argparse,csv,gzip,hashlib,io,json,sys,tarfile
from pathlib import Path
import numpy as np
import scipy
from scipy.io import mmread
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3]
INVENTORY=ROOT/'analysis/research/runs/Yd1_source_qualification_v1/geo_library_qualification.json'
ARCHIVE=ROOT/'raw_data/Yd1_source_v1/GSE242510_RAW.tar'

def read_library(tar,sample):
    names={u.rsplit('/',1)[-1].rsplit('_',1)[-1]:u.rsplit('/',1)[-1] for u in sample['files']}
    def rows(suffix):
        with gzip.GzipFile(fileobj=tar.extractfile(names[suffix])) as f:
            return [l.decode().rstrip('\r\n').split('\t') for l in f]
    features=rows('features.tsv.gz');barcodes=[r[0] for r in rows('barcodes.tsv.gz')]
    assert len({r[0] for r in features})==len(features)
    assert len(set(barcodes))==len(barcodes)
    with gzip.GzipFile(fileobj=tar.extractfile(names['matrix.mtx.gz'])) as f:
        banner=f.readline().decode().strip();assert banner=='%%MatrixMarket matrix coordinate integer general'
        line=f.readline()
        while line.startswith(b'%'):line=f.readline()
        dims=list(map(int,line.split()))
    with gzip.GzipFile(fileobj=tar.extractfile(names['matrix.mtx.gz'])) as f:
        matrix=mmread(f)
        assert not f.read().strip(),'Unexpected trailing matrix data'
    assert matrix.shape==(len(features),len(barcodes))==tuple(dims[:2])
    assert matrix.nnz==dims[2]
    assert np.issubdtype(matrix.data.dtype,np.integer)
    assert np.all(matrix.data>=0)
    assert np.all((matrix.row>=0)&(matrix.row<dims[0])) and np.all((matrix.col>=0)&(matrix.col<dims[1]))
    zeros=int(np.sum(matrix.data==0));maximum=int(matrix.data.max());total=int(matrix.data.sum())
    csr=matrix.tocsr();assert csr.nnz==matrix.nnz,'Duplicate coordinates'
    csr.eliminate_zeros()
    return csr,features,barcodes,dict(declared_entries=dims[2],actual_entries=int(matrix.nnz),
        zero_entries=zeros,maximum_entry=maximum,total_counts=total,duplicate_coordinates=0,
        shape_and_indices='passed',integer_nonnegative='passed',gzip_complete='passed')

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output;out.mkdir(exist_ok=True,parents=True)
    samples=json.loads(INVENTORY.read_text());summaries=[];integrity=[];cells=[];plot=[]
    with tarfile.open(ARCHIVE) as tar:
        for s in samples:
            m,features,barcodes,check=read_library(tar,s)
            totals=np.asarray(m.sum(axis=0)).ravel().astype(np.int64);genes=np.asarray((m>0).sum(axis=0)).ravel()
            mito=np.array([f[1].lower().startswith('mt-') for f in features])
            mito_counts=np.asarray(m[mito].sum(axis=0)).ravel()
            pct=np.divide(100*mito_counts,totals,out=np.zeros(len(totals),dtype=float),where=totals>0)
            assert int(totals.sum())==check['total_counts']
            integrity.append(dict(gsm=s['gsm'],title=s['title'],features=len(features),barcodes=len(barcodes),mitochondrial_features=int(mito.sum()),**check))
            for i,bc in enumerate(barcodes):
                cells.append(dict(gsm=s['gsm'],barcode=bc,total_counts=int(totals[i]),detected_genes=int(genes[i]),mitochondrial_counts=int(mito_counts[i]),mitochondrial_percent=float(pct[i])))
            summary=dict(gsm=s['gsm'],title=s['title'],n_barcodes=len(barcodes),zero_count_barcodes=int(np.sum(totals==0)))
            for name,v in [('counts',totals),('genes',genes),('mitochondrial_percent',pct)]:
                for q in [0,.05,.5,.95,1]:summary[f'{name}_q{int(q*100):02}']=float(np.quantile(v,q))
            for cut in [5,10,20,25,50]:summary[f'mito_gt_{cut}']=int(np.sum(pct>cut))
            summary['genes_lt_200']=int(np.sum(genes<200));summaries.append(summary)
            plot.append((s['title'],totals,genes,pct));print(s['gsm'],'full-entry integrity passed',flush=True)
    for name,rows in [('library_integrity.csv',integrity),('library_qc.csv',summaries),('cell_qc.csv',cells)]:
        with (out/name).open('x',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axes=plt.subplots(2,3,figsize=(11.5,7.5))
    for ax,(title,totals,genes,pct) in zip(axes.flat,plot):
        sc=ax.scatter(totals,genes,c=pct,s=3,cmap='viridis',vmin=0,vmax=50,rasterized=True)
        ax.set_xscale('log');ax.set_yscale('log');ax.set_title(title);ax.set_xlabel('Total deposited counts');ax.set_ylabel('Detected genes')
    fig.colorbar(sc,ax=list(axes.flat),label='Mitochondrial counts (%)',fraction=.02,pad=.02)
    fig.suptitle('Six coculture libraries: technical QC before annotation',x=.07,ha='left',fontsize=14)
    fig.subplots_adjust(left=.07,right=.88,top=.88,bottom=.15,wspace=.4,hspace=.52)
    fig.text(.07,.035,'All deposited barcodes retained in this diagnostic. Colors saturate at 50%; no biological classes or effects inferred.\nSource: GSE242510; outcome-exposed qualification. Cells are not independent preparations.',fontsize=8)
    fig.savefig(out/'qc.png',dpi=200);fig.savefig(out/'qc.pdf');plt.close(fig)
    (out/'runtime.json').write_text(json.dumps(dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,annotation_executed=False,expression_effects_executed=False),indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
