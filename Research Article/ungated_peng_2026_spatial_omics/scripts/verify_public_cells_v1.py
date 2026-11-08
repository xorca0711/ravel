"""Independent A12 verification: sparse vectors and scalar aggregation, no producer import."""
import math
from pathlib import Path
import h5py
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix

def verify(root,manifest,out):
    checks=0;failures=[];max_error=0.
    def check(ok,label):
        nonlocal checks
        checks+=1
        if not bool(ok):failures.append(label)
    def close(x,y,label):
        nonlocal max_error
        if pd.isna(x) and pd.isna(y):check(True,label);return
        err=abs(float(x)-float(y));max_error=max(max_error,err)
        check(math.isclose(float(x),float(y),rel_tol=1e-10,abs_tol=1e-10),label)
    targets=['IL1R1','IL1RAP','IL1R2','IL1RN','SIGIRR','MYD88','IRAK1','IRAK4','NFKBIA','TNFAIP3']
    roster={4,5,6,7,14,17,18,19,21,22,24,25};frames=[]
    for item in manifest['libraries']:
        f={Path(x['path']).name:root/x['path'] for x in item['files']};a=pd.read_csv(f['cell_annotations.csv.gz'])
        with h5py.File(f['raw_counts.csc.h5'],'r') as h:
            index=a.source_cell_index.to_numpy();check(a.cell_id.is_unique,item['gsm']+' unique')
            check(list(h['barcodes'].asstr()[:][index])==a.cell_id.str.split(':',n=1).str[1].tolist(),item['gsm']+' barcode')
            check(np.array_equal(h['full_library_size'][:][index],a.full_library_size),item['gsm']+' depth')
            if int(item['patient']) not in roster or item['histology'] not in ['normal','LUAD']:continue
            a=a[(a.ann_finest_level=='AT2')&(a.ann_finest_level_uncertainty<=.2)].copy();index=a.source_cell_index.to_numpy()
            n=int(h.attrs['shape'][0]);gene=h['genes'].asstr()[:].tolist()
            for g in targets:
                j=gene.index(g);lo=int(h['indptr'][j]);hi=int(h['indptr'][j+1])
                vector=coo_matrix((h['data'][lo:hi],(h['indices'][lo:hi],np.zeros(hi-lo,dtype=int))),shape=(n,1)).tocsr()
                a[g]=vector[index,0].toarray().ravel()
            frames.append(a)
    cells=pd.concat(frames,ignore_index=True)
    table=pd.read_csv(out/'patient_gene_components.csv');table=table[table.population.eq('AT2_u20')]
    pair=pd.read_csv(out/'patient_codetection.csv');pair=pair[pair.population.eq('AT2_u20')]
    old=pd.read_csv(root/'analysis/research/runs/A12_il1_components_v1_20261103/unit_gene_primitives.tsv',sep='\t');old=old[old.recipient.eq('AT2')]
    for (patient,hist),a in cells.groupby(['patient','histology']):
        check(len(a)>=50,f'{patient}/{hist} floor')
        t=table[(table.patient==patient)&(table.histology==hist)].set_index('gene')
        o=old[(old.patient==patient)&(old.histology==hist)].set_index('gene')
        den=a.full_library_size.to_numpy();library=sum(int(x) for x in den)
        for g in targets:
            v=a[g].to_numpy(); logs=[math.log2(1+10000*int(c)/int(d)) for c,d in zip(v,den)]
            pos=[x for x,c in zip(logs,v) if c>0];total=sum(int(c) for c in v);count=len(pos);tag=f'{patient}/{hist}/{g}'
            for field,value in [('cells',len(v)),('library_total',library),('count_sum',total),('detected',count),('fraction_detected',count/len(v)),('mean_count',total/len(v)),('mean_log',math.fsum(logs)/len(v)),('positive_mean_log',math.fsum(pos)/len(pos) if pos else np.nan),('pseudobulk_logCPM',math.log2(1+1e6*total/library))]:close(t.loc[g,field],value,tag+'/'+field)
            for new,prior in [('cells','n_cells'),('library_total','full_library_sum'),('count_sum','gene_count'),('pseudobulk_logCPM','log2_1_plus_cpm')]:close(t.loc[g,new],o.loc[g,prior],tag+'/old_'+new)
        for g in ['IL1RAP','IL1R2','IL1RN','SIGIRR']:
            p=pair[(pair.patient==patient)&(pair.histology==hist)&pair.pair.eq('IL1R1__'+g)].iloc[0]
            for x,y,field in [(0,0,'n00'),(1,0,'n10'),(0,1,'n01'),(1,1,'n11')]:
                count=sum((int(v)>0)==bool(x) and (int(w)>0)==bool(y) for v,w in zip(a.IL1R1,a[g]));close(p[field],count,f'{patient}/{hist}/{g}/{field}')
            close(p.joint_fraction,p.n11/len(a),'joint fraction')
            close(p.conditional_on_IL1R1,p.n11/(p.n11+p.n10) if p.n11+p.n10 else np.nan,'conditional denominator')
    # Reconstruct every paired delta, irrespective of population.
    genes=pd.read_csv(out/'patient_gene_components.csv');pairs=pd.read_csv(out/'patient_codetection.csv')
    for r in pd.read_csv(out/'paired_deltas.csv').itertuples():
        src=genes if '__' not in r.feature else pairs;key='gene' if '__' not in r.feature else 'pair'
        q=src[(src.population==r.population)&(src.patient==r.patient)&(src[key]==r.feature)].set_index('histology')
        close(r.delta,q.loc['LUAD',r.metric]-q.loc['normal',r.metric],'delta '+r.feature)
    # Verify common-support bin membership and standardized detections independently.
    ds=pd.read_csv(out/'depth_standardized_deltas.csv');support=pd.read_csv(out/'depth_support.csv')
    for patient,a in cells.groupby('patient'):
        a=a.copy();a['db']=[sum(int(x)>=v for v in [2000,4000,8000]) for x in a.full_library_size];a['gb']=[sum(int(x)>=v for v in [1000,2000,4000]) for x in a.n_genes_by_counts]
        s=support[support.patient==patient];included=s[s.included]
        close(included.weight.sum(),1 if len(included) else 0,'weight total')
        for r in s.itertuples():
            for hist in ['normal','LUAD']:
                n=len(a[(a.db==r.depth_bin)&(a.gb==r.gene_bin)&a.histology.eq(hist)])
                close(n,getattr(r,hist),'stratum count')
            check(r.included==(min(r.normal,r.LUAD)>=5),'support floor')
        for r in ds[ds.patient==patient].itertuples():
            values={}
            for hist in ['normal','LUAD']:
                val=0.
                for b in included.itertuples():
                    q=a[(a.db==b.depth_bin)&(a.gb==b.gene_bin)&a.histology.eq(hist)]
                    n=sum(all(row[g]>0 for g in r.feature.split('__')) for row in q[r.feature.split('__')].to_dict('records'))
                    val+=b.weight*n/len(q)
                values[hist]=val if len(included) else np.nan
                close(getattr(r,hist),values[hist],'standardized fraction')
            close(r.delta,values['LUAD']-values['normal'],'standardized delta')
    return {'method':'Separate SciPy sparse-vector reader, scalar primary arithmetic, frozen pseudobulk parity, all paired deltas and independent common-depth bins','checks':checks,'failures':failures,'max_absolute_error':max_error,'biological_replication':False}
