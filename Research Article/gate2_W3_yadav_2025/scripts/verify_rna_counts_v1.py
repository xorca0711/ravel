"""Independent chunked MatrixMarket reader and endpoint arithmetic checks."""
import gzip,math
import numpy as np

def stream_library(tar,sample,genes):
    names={u.rsplit('/',1)[-1].rsplit('_',1)[-1]:u.rsplit('/',1)[-1] for u in sample['files']}
    with gzip.GzipFile(fileobj=tar.extractfile(names['features.tsv.gz'])) as f:
        features=[line.decode().rstrip().split('\t') for line in f]
    indices={g:[i+1 for i,row in enumerate(features) if row[1]==g] for g in genes}
    assert all(len(x)==1 for x in indices.values())
    with gzip.GzipFile(fileobj=tar.extractfile(names['matrix.mtx.gz'])) as f:
        assert f.readline().startswith(b'%%MatrixMarket')
        line=f.readline()
        while line.startswith(b'%'):line=f.readline()
        nf,nc,declared=map(int,line.split())
        totals=np.zeros(nc,dtype=np.int64);detected=np.zeros(nc,dtype=np.int64)
        target={g:np.zeros(nc,dtype=np.int64) for g in genes};seen=0
        while True:
            lines=f.readlines(8*1024*1024)
            if not lines:break
            a=np.fromstring(b''.join(lines).decode('ascii'),dtype=np.int64,sep=' ')
            assert len(a)%3==0;a=a.reshape(-1,3);seen+=len(a)
            col=a[:,1]-1
            totals+=np.bincount(col,weights=a[:,2],minlength=nc).astype(np.int64)
            detected+=np.bincount(col[a[:,2]>0],minlength=nc)
            for g,ix in indices.items():
                keep=a[:,0]==ix[0];np.add.at(target[g],col[keep],a[keep,2])
        assert seen==declared
    return totals,detected,target,seen

def independent_summary(counts,totals,mask):
    a=[int(v) for v in counts[mask]];den=[int(v) for v in totals[mask]];n=len(a)
    normalized=[x/d*10000 for x,d in zip(a,den)]
    return dict(n_cells=n,gene_counts=sum(a),total_counts=sum(den),detection_fraction=sum(x>0 for x in a)/n,
        mean_per10k=math.fsum(normalized)/n,mean_log1p_per10k=math.fsum(math.log1p(x) for x in normalized)/n,
        pseudobulk_cpm=sum(a)/sum(den)*1e6)
