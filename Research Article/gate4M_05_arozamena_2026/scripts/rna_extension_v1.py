"""Frozen finite-library RNA description; no state calls or population inference."""
from __future__ import annotations
import argparse,csv,gzip,hashlib,io,json,math,sys
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.tools/sx22_e1a_runtime'))
import h5py

TARGETS=['Cd74','Reg3g','Reg3b','H2-D1','App','Lgals9','Mif','Ifitm3']
CONTRASTS=[
 ('GSE302685_Lgr5','GSE302685_irradiated','GSE302685_control'),
 ('GSE302687_Krt20','GSE302687_irradiated','GSE302687_control'),
 ('GSE329778_LGR5','GSE329778_LGR5','GSE329778_CTRL'),
 ('GSE329778_KRT20','GSE329778_KRT20','GSE329778_CTRL')]
CASES=[('all','pooled'),('all','equal'),('rna_qc','pooled'),('rna_qc','equal')]

def require(ok,message):
    if not ok:raise ValueError(message)

@contextmanager
def csv_writer(path,fields):
    with path.open('xb') as raw:
        if path.suffix=='.gz':
            with gzip.GzipFile(fileobj=raw,filename='',mode='wb',mtime=0) as z:
                with io.TextIOWrapper(z,encoding='utf-8',newline='') as f:
                    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();yield w
        else:
            with io.TextIOWrapper(raw,encoding='utf-8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();yield w

def write_json(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def number(value):return '' if not math.isfinite(float(value)) else float(value)

def feature_metadata(spec):
    if spec['format']=='h5':
        with h5py.File(ROOT/spec['paths'][0],'r') as f:
            g=f['matrix/features'];ids=g['id'].asstr()[:].tolist();names=g['name'].asstr()[:].tolist();types=g['feature_type'].asstr()[:].tolist();barcodes=f['matrix/barcodes'].asstr()[:].tolist()
    else:
        with gzip.open(ROOT/spec['paths'][1],'rt',encoding='utf-8') as f:rows=[line.rstrip('\r\n').split('\t') for line in f if line.strip()]
        require(all(len(r)>=3 and r[2] for r in rows),'Explicit feature types required')
        ids=[r[0] for r in rows];names=[r[1] for r in rows];types=[r[2] for r in rows]
        with gzip.open(ROOT/spec['paths'][2],'rt',encoding='utf-8') as f:barcodes=[line.strip() for line in f if line.strip()]
    require(len(ids)==len(set(ids)) and len(barcodes)==len(set(barcodes)),'Duplicate source IDs')
    rna=np.array([i for i,t in enumerate(types) if t=='Gene Expression'],dtype=np.int64)
    mapping=np.full(len(ids),-1,dtype=np.int64);mapping[rna]=np.arange(len(rna))
    return dict(ids=[ids[i] for i in rna],names=[names[i] for i in rna],barcodes=barcodes,mapping=mapping,n_features=len(ids))

def resolve_targets(metadata,common):
    resolved={};rows=[]
    for target in TARGETS:
        matches={lib:[i for i,n in zip(m['ids'],m['names']) if n==target] for lib,m in metadata.items()}
        good=all(len(v)==1 for v in matches.values()) and len({v[0] for v in matches.values() if len(v)==1})==1
        stable=next(iter(matches.values()))[0] if good else ''
        good=good and stable in common
        resolved[target]=stable if good else None
        for lib,ids in matches.items():rows.append(dict(target=target,library=lib,matched_ids=';'.join(ids),status='qualified' if good else 'held_ambiguous_or_absent_mapping'))
    return resolved,rows

def mitochondrial_map(metadata):
    sets={lib:{i for i,n in zip(m['ids'],m['names']) if n.startswith('mt-')} for lib,m in metadata.items()}
    names={lib:{i:n for i,n in zip(m['ids'],m['names']) if i in sets[lib]} for lib,m in metadata.items()}
    good=all(sets.values()) and all(v==next(iter(sets.values())) for v in sets.values()) and all(v==next(iter(names.values())) for v in names.values())
    return sets,good

def h5_columns(path,mapping,nc):
    with h5py.File(path,'r') as f:
        m=f['matrix'];ptr=m['indptr'][:].astype(np.int64)
        require(len(ptr)==nc+1,'Barcode shape disagreement')
        for first in range(0,nc,128):
            last=min(first+128,nc);base=int(ptr[first]);stop=int(ptr[last]);rows=m['indices'][base:stop];values=m['data'][base:stop].astype(np.float64)
            for c in range(first,last):
                a,b=int(ptr[c]-base),int(ptr[c+1]-base);ix=mapping[rows[a:b]];v=values[a:b];keep=(ix>=0)&(v>0)
                yield c,ix[keep],v[keep]

def mtx_columns(path,mapping,nc):
    with gzip.open(path,'rt',encoding='utf-8') as f:
        header=f.readline().strip().lower();require(header in ['%%matrixmarket matrix coordinate integer general','%%matrixmarket matrix coordinate real general'],'MatrixMarket header')
        for line in f:
            if line.strip() and not line.startswith('%'):nr,declared_nc,nnz=map(int,line.split());break
        require(nr==len(mapping) and nc==declared_nc,'MatrixMarket shape disagreement')
        column=0;ix=[];values=[];entries=0;previous=-1
        for line in f:
            if not line.strip():continue
            r,c,value=line.split();r=int(r)-1;c=int(c)-1;key=c*nr+r
            require(0<=r<nr and 0<=c<nc and key>previous,'Expected qualified unique column order');previous=key;entries+=1
            while column<c:
                yield column,np.asarray(ix,dtype=np.int64),np.asarray(values,dtype=np.float64)
                column+=1;ix=[];values=[]
            gene=mapping[r]
            if gene>=0:
                v=float(value);require(math.isfinite(v) and v>=0 and v.is_integer(),'Invalid RNA entry')
                if v>0:ix.append(gene);values.append(v)
        require(entries==nnz,'MatrixMarket entry count disagreement')
        while column<nc:
            yield column,np.asarray(ix,dtype=np.int64),np.asarray(values,dtype=np.float64)
            column+=1;ix=[];values=[]

def qc_pass(depth,detected,mito_count):
    return depth>=500 and 200<=detected<=2500 and mito_count<=0.40*depth

class Accumulator:
    def __init__(self,n_genes,mitochondrial,qc_available):
        self.mito=np.asarray(mitochondrial,bool);self.qc_available=qc_available
        self.total=np.zeros((2,n_genes));self.equal=np.zeros((2,n_genes));self.depth=np.zeros(2);self.n=np.zeros(2,dtype=np.int64)
    def add(self,indices,values):
        require(len(indices)==len(set(map(int,indices))) and len(indices)==len(values),'Duplicate RNA coordinate')
        require(np.isfinite(values).all() and (values>0).all() and (values==np.floor(values)).all(),'Positive integer RNA entries required')
        depth=float(values.sum());detected=len(values);mt=float(values[self.mito[indices]].sum());passed=qc_pass(depth,detected,mt) if self.qc_available else None
        for k,keep in enumerate([depth>0,passed is True]):
            if keep:
                self.total[k,indices]+=values;self.equal[k,indices]+=values*(1e6/depth);self.depth[k]+=depth;self.n[k]+=1
        return depth,detected,mt,passed
    def finish(self):
        pooled=np.full_like(self.total,np.nan);equal=np.full_like(self.equal,np.nan)
        for k in range(2):
            if self.n[k]:pooled[k]=self.total[k]*1e6/self.depth[k];equal[k]=self.equal[k]/self.n[k]
        return pooled,equal

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);out=Path(parser.parse_args().output).resolve()
    require(out.parent==ROOT/'analysis/research/runs' and out.is_dir(),'Runner directory required')
    require(all(p.name in ['receipt.json','stdout.log','stderr.log'] for p in out.iterdir()),'Existing output artifacts')
    manifest=json.loads((PACKAGE/'sources/intake_v1.json').read_text());specs=manifest['multiome_libraries']
    metadata={s['id']:feature_metadata(s) for s in specs}
    with (ROOT/'analysis/research/runs/arz1_source_qualification_v2/common_feature_ids.csv').open(newline='') as f:common=[r['stable_id'] for r in csv.DictReader(f) if r['feature_type']=='Gene Expression']
    require(len(common)==31950 and set(common)==set.intersection(*[set(m['ids']) for m in metadata.values()]),'Frozen common RNA universe mismatch')
    commonset=set(common);targets,mappings=resolve_targets(metadata,commonset);mtsets,qc_available=mitochondrial_map(metadata)
    with csv_writer(out/'selected_target_mapping.csv',['target','library','matched_ids','status']) as w:w.writerows(mappings)
    with csv_writer(out/'gene_symbol_mapping.csv.gz',['library','stable_id','source_symbol','common_reported','mitochondrial_by_name']) as w:
        for lib,m in metadata.items():w.writerows(dict(library=lib,stable_id=i,source_symbol=n,common_reported=i in commonset,mitochondrial_by_name=i in mtsets[lib]) for i,n in zip(m['ids'],m['names']))
    with csv_writer(out/'mitochondrial_mapping.csv',['library','stable_id','source_symbol','definition','qc_mapping_status']) as w:
        for lib,m in metadata.items():w.writerows(dict(library=lib,stable_id=i,source_symbol=n,definition='case-sensitive source symbol prefix mt-; not coordinate validation',qc_mapping_status='qualified_operational' if qc_available else 'held_inconsistent_mapping') for i,n in zip(m['ids'],m['names']) if i in mtsets[lib])
    receipt=json.loads((out/'receipt.json').read_text())
    with csv_writer(out/'source_hashes.csv',['path','sha256']) as w:w.writerows({k:r[k] for k in ['path','sha256']} for r in receipt['inputs'])
    results={};library_qc=[]
    with csv_writer(out/'barcode_qc.csv.gz',['library','barcode','rna_counts','detected_rna_genes','mitochondrial_counts','mitochondrial_fraction','positive_rna_depth','rna_qc_pass']) as bw, csv_writer(out/'library_gene_summaries.csv.gz',['library','subset','stable_id','source_symbol','n_barcodes','all_source_rna_denominator','gene_count','pooled_cpm','pooled_log2_cpm1','equal_cpm','equal_log2_cpm1','status']) as gw:
        for spec in specs:
            lib=spec['id'];m=metadata[lib];lookup={i:k for k,i in enumerate(m['ids'])};ix=np.array([lookup[i] for i in common]);acc=Accumulator(len(m['ids']),[i in mtsets[lib] for i in m['ids']],qc_available)
            stats=[];fail=Counter();reader=h5_columns if spec['format']=='h5' else mtx_columns
            for c,indices,values in reader(ROOT/spec['paths'][0],m['mapping'],len(m['barcodes'])):
                depth,detected,mt,passed=acc.add(indices,values);fraction=mt/depth if depth else math.nan
                bw.writerow(dict(library=lib,barcode=m['barcodes'][c],rna_counts=int(depth),detected_rna_genes=detected,mitochondrial_counts=int(mt),mitochondrial_fraction=number(fraction),positive_rna_depth=depth>0,rna_qc_pass=passed if passed is not None else 'held'))
                stats.append((depth,detected,fraction));fail.update(k for k,v in [('zero_depth',depth==0),('detected_below_200',detected<200),('detected_above_2500',detected>2500),('rna_below_500',depth<500),('mitochondrial_above_0.40',depth>0 and fraction>0.40)] if v)
            require(len(stats)==len(m['barcodes']),'Processed barcode count mismatch');pooled,equal=acc.finish()
            results[lib]={(subset,weight):np.log2(array[k,ix]+1) for k,subset in enumerate(['all','rna_qc']) for weight,array in [('pooled',pooled),('equal',equal)]}
            for k,subset in enumerate(['all','rna_qc']):
                for j,g in enumerate(common):
                    r=ix[j];gw.writerow(dict(library=lib,subset=subset,stable_id=g,source_symbol=m['names'][r],n_barcodes=int(acc.n[k]),all_source_rna_denominator=int(acc.depth[k]),gene_count=int(acc.total[k,r]),pooled_cpm=number(pooled[k,r]),pooled_log2_cpm1=number(results[lib][(subset,'pooled')][j]),equal_cpm=number(equal[k,r]),equal_log2_cpm1=number(results[lib][(subset,'equal')][j]),status='defined' if acc.n[k] else 'held_empty_or_unavailable_subset'))
            stats=np.asarray(stats);quantiles={name:np.quantile(stats[:,j][np.isfinite(stats[:,j])],[0,.25,.5,.75,1]).tolist() if np.isfinite(stats[:,j]).any() else [] for j,name in enumerate(['rna_counts','detected_rna_genes','mitochondrial_fraction'])}
            library_qc.append(dict(library=lib,n_source_rna_genes=len(m['ids']),n_barcodes=len(m['barcodes']),n_positive_rna=int(acc.n[0]),n_rna_qc=int(acc.n[1]),all_source_rna_denominators=acc.depth.astype(np.int64).tolist(),common_gene_count_sums=acc.total[:,ix].sum(axis=1).astype(np.int64).tolist(),qc_mapping_available=qc_available,overlapping_failure_counts=dict(fail),source_barcode_quantiles_min_q25_median_q75_max=quantiles))
            print('Completed RNA library: '+lib,flush=True)
    write_json(out/'library_qc_summary.json',library_qc)
    panel=[];summaries=[];gene_index={g:j for j,g in enumerate(common)}
    fields=['contrast','post_library','control_library','subset','weighting','stable_id','post_log2_cpm1','control_log2_cpm1','difference_log2_cpm1','status']
    with csv_writer(out/'gene_contrasts.csv.gz',fields) as w:
        for contrast,post,control in CONTRASTS:
            for subset,weight in CASES:
                a=results[post][(subset,weight)];b=results[control][(subset,weight)];delta=a-b
                for j,g in enumerate(common):w.writerow(dict(contrast=contrast,post_library=post,control_library=control,subset=subset,weighting=weight,stable_id=g,post_log2_cpm1=number(a[j]),control_log2_cpm1=number(b[j]),difference_log2_cpm1=number(delta[j]),status='defined' if math.isfinite(delta[j]) else 'held_empty_or_unavailable_subset'))
                values=[]
                for target,g in targets.items():
                    j=gene_index[g] if g else None;value=delta[j] if j is not None else math.nan
                    panel.append(dict(target=target,contrast=contrast,post_library=post,control_library=control,subset=subset,weighting=weight,stable_id=g or '',post_log2_cpm1=number(a[j]) if g else '',control_log2_cpm1=number(b[j]) if g else '',difference_log2_cpm1=number(value),status='defined' if math.isfinite(value) else 'held_mapping_or_subset'))
                    if math.isfinite(value):values.append(float(value))
                summaries.append(dict(contrast=contrast,subset=subset,weighting=weight,n_defined=len(values),n_held=len(TARGETS)-len(values),n_positive=sum(v>0 for v in values),n_zero=sum(v==0 for v in values),n_negative=sum(v<0 for v in values),median_difference_log2_cpm1=float(np.median(values)) if values else None))
    with csv_writer(out/'selected_target_contrasts.csv',['target',*fields]) as w:w.writerows(panel)
    with csv_writer(out/'selected_target_summary.csv',list(summaries[0])) as w:w.writerows(summaries)
    from plot_rna_v1 import figures
    figures(out,panel,TARGETS,CONTRASTS,CASES)
    summary=dict(analysis='Arz1.rna_description_v1',n_libraries=7,n_common_rna_ids=len(common),n_contrasts=4,n_cases=4,n_gene_contrast_rows=len(common)*16,n_panel_rows=len(panel),target_mapping_holds=[t for t,g in targets.items() if not g],rna_qc_mapping_available=qc_available,rna_qc_definition='source mt- symbol prefix; 200<=detected<=2500, RNA>=500, mitochondrial fraction<=0.40; all source RNA genes',empty_or_unavailable_qc_libraries=[x['library'] for x in library_qc if not x['n_rna_qc']],denominators='all source RNA genes, not common reporting genes or ATAC',transformation='log2(CPM+1) after pooled normalization or equal-barcode averaging',biological_independence='unknown',scientific_acceptance='not_assessed')
    write_json(out/'summary.json',summary);print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
