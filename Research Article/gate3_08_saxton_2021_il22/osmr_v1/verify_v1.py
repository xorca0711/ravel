"""Independent raw-source arithmetic; does not import production code."""
import csv,gzip,math,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
RUN=ROOT/'analysis/research/runs/sx22_osmr_v1'
libs=['PBS_1','PBS_2','LH5_1','LH5_2','LH30_1','LH30_2']
groups=dict(PBS=libs[:2],WT=libs[2:4],B3=libs[4:])
def rows(p):
    with open(p,encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
raw=[]
for kind in ['readcount','fpkm']:
    with gzip.open(ROOT/f'raw_data/Sx22/GSE160217_060120_22_{kind}_genename.xls.gz','rt',encoding='utf-8') as f:raw.append(list(csv.DictReader(f,delimiter='\t')))
targets=[[r for r in table if r['Gene_name']=='Osmr'] for table in raw]
assert all(len(t)==1 and t[0]['geneID']=='ENSMUSG00000022146' for t in targets)
sizes={l:sum(int(r[l]) for r in raw[0]) for l in libs}
factors={(r['view'],r['library']):float(r['effective_library_size']) for r in rows(ROOT/'analysis/research/runs/sx22_program_description_v1/normalization_factors.csv')}
values={}
for r in rows(RUN/'library_values.csv'):
    l=r['library']; scale=r['scale']; view=r['view']
    v=float(targets[1][0][l]) if scale=='FPKM' else int(targets[0][0][l])*1e6/(sizes[l] if scale=='CPM' else factors[view,l])
    assert math.isclose(v,float(r['abundance']),rel_tol=1e-12)
    values[scale,view,l]=math.log2(v+1)
    assert abs(values[scale,view,l]-float(r['log2_plus_1']))<1e-12
cs=rows(RUN/'contrasts.csv')
for r in cs:
    a,b=r['contrast'].split('-'); scale,view=r['scale'],r['view']
    means={g:statistics.mean(values[scale,view,l] for l in ls if view!='omit_'+l) for g,ls in groups.items()}
    assert abs(float(r['value'])-(means[a]-means[b]))<1e-12
for r in rows(RUN/'ranges.csv'):
    rs=[c for c in cs if c['scale']==r['scale'] and c['contrast']==r['contrast']]
    assert float(r['full'])==float(next(c['value'] for c in rs if c['view']=='full'))
    assert float(r['omission_min'])==min(float(c['value']) for c in rs if c['view']!='full')
    assert float(r['omission_max'])==max(float(c['value']) for c in rs if c['view']!='full')
print('PASS: raw source mapping, all 108 library-scale-view values, 63 contrasts and 9 figure ranges; tolerance 1e-12')
