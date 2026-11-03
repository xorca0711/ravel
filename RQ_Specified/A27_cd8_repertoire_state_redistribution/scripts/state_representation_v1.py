"""Fixed RNA states and source repertoire representation, conditional on original labels."""
import argparse,itertools,json,math
from pathlib import Path
import h5py
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import hypergeom

PRE=Path('docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A27_INPUT_MAP_V1.json')
JOIN=Path('analysis/research/runs/nb5_completion_metadata_v2/repertoire_annotation_join.tsv')
OLD=Path('analysis/research/runs/nb5_subtype_biological_v1/subtype_mouse.tsv')
STATES=['naive_associated','effector_associated','mixed','indeterminate']
NAIVE=['Tcf7','Lef1','Ccr7','Il7r'];EFFECTOR=['Nkg7','Ccl5','Gzmk','Gzmb','Prf1'];GENES=NAIVE+EFFECTOR

def rarefaction(sizes,depth=5):
    n=sum(sizes)
    return sum(k/n*(1-float(hypergeom.pmf(0,n-1,k-1,depth-1))) for k in sizes)

def scalar_rarefaction(sizes,depth=5):
    n=sum(sizes);den=math.comb(n-1,depth-1)
    return sum(k/n*(1-(math.comb(n-k,depth-1) if n-k>=depth-1 else 0)/den) for k in sizes)

def toy_check():
    vals=[0,0,0,1,1,2];errors=[]
    for depth in [2,3,4,5]:
        exact=np.mean([sum(s.count(x)>1 for x in s)/depth for s in itertools.combinations(vals,depth)])
        errors.extend([abs(exact-rarefaction([3,2,1],depth)),abs(exact-scalar_rarefaction([3,2,1],depth))])
    if max(errors)>1e-12:raise ValueError('Synthetic rarefaction failure')
    return max(errors)

def decode(x):return x.decode() if isinstance(x,bytes) else str(x)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);out.mkdir(parents=True,exist_ok=True);spec=json.loads(PRE.read_text());toy_error=toy_check()
    source=pd.read_csv(JOIN,sep='\t',keep_default_na=False);source=source[source.mouse_id.ne('')].copy()
    if len(source)!=6000 or not source.cell_name.is_unique:raise ValueError('Original source cohort conflict')
    source['clone_key']=['source:'+str(g) if str(g) else 'singleton:'+str(c) for g,c in zip(source.clonal_group,source.cell_name)]
    sizes=source.groupby(['age_months','mouse_id','clone_key']).cell_name.transform('size')
    if not np.array_equal(sizes.to_numpy(),source.within_mouse_clone_size.to_numpy()):raise ValueError('Original clone convention conflict')
    source=source[source.tissue.eq('Spleen')&source.official_cell_ontology_class.eq('CD8-positive, alpha-beta T cell')].copy()
    if len(source)!=288 or not source.official_lookup.is_unique or int(source.clonal_group.eq('').sum())!=237:raise ValueError('Original CD8 cohort conflict')
    with h5py.File(spec['source_path'],'r') as h:
        rawobs=h['obs'][:];obs=pd.DataFrame(index=[decode(x) for x in rawobs['index']])
        for field in ['age','mouse.id','cell_ontology_class','method','tissue','sex']:
            cat=h['uns'][field+'_categories'][:];codes=rawobs[field]
            if not ((codes>=0)&(codes<len(cat))).all():raise ValueError('Missing annotation category')
            obs[field]=[decode(cat[int(i)]) for i in codes]
        if not obs.index.is_unique:raise ValueError('Duplicate RNA IDs')
        names=np.array([decode(x) for x in h['raw.var'][:]['index']]);positions=[np.flatnonzero(names==g) for g in GENES]
        if any(len(p)!=1 for p in positions):raise ValueError('Ambiguous state gene')
        positions=[int(p[0]) for p in positions];m=h['raw.X'];shape=tuple(m.attrs['h5sparse_shape'])
        if list(shape)!=spec['shape'] or decode(m.attrs['h5sparse_format'])!='csr':raise ValueError('Count layer conflict')
        values=m['data'][:]
        if not (np.isfinite(values).all() and (values>=0).all() and (values==np.floor(values)).all()):raise ValueError('Raw layer is not integer nonnegative reads')
        matrix=sparse.csr_matrix((values.astype(np.int64),m['indices'][:],m['indptr'][:]),shape=shape);totals=np.asarray(matrix.sum(axis=1)).ravel();counts=matrix[:,positions].toarray()
    keep=obs.cell_ontology_class.eq('CD8-positive, alpha-beta T cell')&obs.tissue.eq('Spleen')&obs.method.eq('facs')&obs.age.isin(['3m','18m','24m']);cells=obs.loc[keep].copy();cells.insert(0,'official_lookup',cells.index);cells['library_reads']=totals[keep.to_numpy()]
    if len(cells)!=354 or not cells.library_reads.gt(0).all():raise ValueError('RNA denominator/library conflict')
    for j,g in enumerate(GENES):cells[g]=counts[keep.to_numpy(),j]
    cells['n_naive_detected']=cells[NAIVE].gt(0).sum(axis=1);cells['n_effector_detected']=cells[EFFECTOR].gt(0).sum(axis=1)
    a=cells.n_naive_detected;b=cells.n_effector_detected
    cells['state']=np.select([(a>=2)&(b==0),(b>=2)&(a==0),(a>=2)&(b>=2)],STATES[:3],default='indeterminate')
    cells['age_months']=cells.age.str.removesuffix('m').astype(int);cells=cells.rename(columns={'mouse.id':'mouse_id'})
    cells=cells.merge(source[['official_lookup','cell_name','clonal_group','clone_key','age_months','mouse_id']],on='official_lookup',how='left',suffixes=('','_source'),validate='one_to_one',indicator=True)
    cells['represented_in_source']=cells['_merge'].eq('both');represented=cells[cells.represented_in_source]
    if len(represented)!=288 or set(source.official_lookup)!=set(represented.official_lookup):raise ValueError('Incomplete exact source join')
    if not (represented.age_months.eq(represented.age_months_source)&represented.mouse_id.eq(represented.mouse_id_source)).all():raise ValueError('Source age/mouse mismatch')
    for age,n in [(3,6),(18,3),(24,4)]:
        if cells[cells.age_months.eq(age)].mouse_id.nunique()!=n:raise ValueError('RNA mouse roster conflict')
    for age,n in [(3,4),(18,3),(24,4)]:
        if represented[represented.age_months.eq(age)].mouse_id.nunique()!=n:raise ValueError('Original represented mouse roster conflict')
    cells['inherited_blank_label_singleton']=cells.represented_in_source&cells.clonal_group.eq('');cells=cells.drop(columns=['_merge','age_months_source','mouse_id_source']);cells.to_csv(out/'cell_state_primitives.tsv',sep='\t',index=False)
    representation=[];conditional=[];broad=[];occupancy=[];max_error=0.0
    for (age,mouse),g in cells.groupby(['age_months','mouse_id']):
        rec=g[g.represented_in_source]
        if len(rec):
            sizes=rec.groupby('clone_key').size().tolist();v=rarefaction(sizes);scalar=scalar_rarefaction(sizes);max_error=max(max_error,abs(v-scalar));broad.append(dict(age_months=int(age),mouse_id=mouse,cells=len(rec),depth=5,local_fraction=sum(k for k in sizes if k>1)/len(rec),common_depth_fraction=v))
            for key,clone in rec.groupby('clone_key'):
                for state in STATES:occupancy.append(dict(age_months=int(age),mouse_id=mouse,clone_key=key,source_group_blank=bool(clone.inherited_blank_label_singleton.all()),state=state,cells=int(clone.state.eq(state).sum()),all_state_cells=len(clone)))
        for state in STATES:
            rna=g[g.state.eq(state)];r=rna[rna.represented_in_source];n=len(r);counts=r.groupby('clone_key').size().tolist();repeated=sum(k for k in counts if k>1);ok=n>=5
            representation.append(dict(age_months=int(age),mouse_id=mouse,sex=str(g.sex.iloc[0]),state=state,all_mouse_rna_cells=len(g),rna_cells=len(rna),state_rna_fraction=len(rna)/len(g),source_represented_cells=n,observed_representation_fraction=n/len(rna) if len(rna) else np.nan,inherited_blank_singletons=int(r.inherited_blank_label_singleton.sum())))
            value=rarefaction(counts) if ok else np.nan;scalar=scalar_rarefaction(counts) if ok else np.nan
            if ok:
                max_error=max(max_error,abs(value-scalar))
                if not -1e-12<=value<=repeated/n+1e-12:raise ValueError('Conditional rarefaction bound failure')
            conditional.append(dict(age_months=int(age),mouse_id=mouse,state=state,represented_cells=n,source_clone_keys=len(counts),repeated_cells=repeated,observed_repetition_fraction=repeated/n if n else np.nan,depth=5,eligible=ok,status='estimated' if ok else 'unestimated_fewer_than_five',expected_depth5_fraction=value,scalar_depth5_fraction=scalar))
    if max_error>1e-12:raise ValueError('Scalar rarefaction mismatch')
    broad=pd.DataFrame(broad);old=pd.read_csv(OLD,sep='\t');old=old[old.tissue.eq('Spleen')&old.subtype.eq('CD8')];parity=broad.merge(old,on=['age_months','mouse_id'],how='outer',suffixes=('_new','_old'),indicator=True,validate='one_to_one')
    if not parity['_merge'].eq('both').all():raise ValueError('Original broad mouse roster mismatch')
    parity_error=0.0
    for c in ['cells','depth','local_fraction','common_depth_fraction']:
        e=float(np.max(abs(parity[c+'_new']-parity[c+'_old'])));parity_error=max(parity_error,e)
        if e>1e-10:raise ValueError('Original broad CD8 parity failure '+c)
    conditional=pd.DataFrame(conditional);representation=pd.DataFrame(representation);occupancy=pd.DataFrame(occupancy)
    if representation.rna_cells.sum()!=354 or representation.source_represented_cells.sum()!=288 or occupancy.cells.sum()!=288 or representation.inherited_blank_singletons.sum()!=237:raise ValueError('Partition failure')
    contrasts=[]
    for state in STATES:
        for age in [18,24]:
            young=conditional[conditional.state.eq(state)&conditional.age_months.eq(3)&conditional.eligible];older=conditional[conditional.state.eq(state)&conditional.age_months.eq(age)&conditional.eligible];ok=len(young)>=2 and len(older)>=2
            contrasts.append(dict(state=state,older_age=age,reference_age=3,young_mice=len(young),older_mice=len(older),young_roster=';'.join(young.mouse_id),older_roster=';'.join(older.mouse_id),eligible=ok,status='estimated' if ok else 'unestimated_fewer_than_two_mice_per_age',difference_depth5_pp=100*(older.expected_depth5_fraction.mean()-young.expected_depth5_fraction.mean()) if ok else np.nan))
    contrasts=pd.DataFrame(contrasts)
    for frame,name in [(representation,'mouse_state_representation.tsv'),(conditional,'mouse_state_repetition.tsv'),(occupancy,'clone_state_occupancy.tsv'),(broad,'broad_cd8_depth5.tsv'),(parity,'original_broad_parity.tsv'),(contrasts,'state_age_contrasts.tsv')]:frame.to_csv(out/name,sep='\t',index=False)
    result=dict(ok=True,rna_cells=354,represented_cells=288,rna_mice=13,represented_mice=11,inherited_blank_label_singletons=237,mouse_state_rows=len(conditional),supported_mouse_states=int(conditional.eligible.sum()),attempted_age_contrasts=8,estimated_age_contrasts=int(contrasts.eligible.sum()),max_scalar_error=max_error,max_broad_parity_error=parity_error,max_synthetic_error=toy_error,limit='Operational RNA states and prior-table representation; no assembly-attempt denominator. Blank source clone labels inherit singleton convention, not verified sequence uniqueness. Fixed-depth within-state repetition is not fixed-composition attribution or absolute expansion.')
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
