"""Numerical/provenance audit, including independent earlier extraction and BH checks."""
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from common import *

checks=[]
def check(name,value):
    ok=bool(value);checks.append(dict(name=name,passed=ok));assert ok,name

c=json.loads((OUT/'contract.json').read_text())
check('contract_settings_unchanged',c['config']==CONFIG)
for f in c['input_files']:
    path=Path(f['path']);check('input_bytes:'+path.name,path.stat().st_size==f['bytes'])
    if path.stat().st_size<20_000_000: check('input_hash:'+path.name,sha(path)==f['sha256'])
for name,h in c['scripts'].items():
    source=ROOT/name
    if source.name=='03_mouse_context.py':source=OUT/'failed_attempt/03_mouse_context.py'
    check('frozen_script:'+name,sha(source)==h)
am=json.loads((OUT/'schema_amendment.json').read_text())
check('amended_script_hash',sha(ROOT/'scripts/03_mouse_context.py')==am['resumed_script_sha256'])
g=load('gaona_gene_effects.tsv.gz')
for med,q in g.groupby('medium'):
    p=q['P.Value'].to_numpy();ix=np.argsort(p);n=len(p)
    bh=np.empty(n);bh[ix]=np.minimum(1,np.minimum.accumulate((p[ix]*n/np.arange(1,n+1))[::-1])[::-1])
    check('BH:'+med,np.allclose(bh,q['adj.P.Val'],rtol=1e-10,atol=1e-13))
    check('unique_genes:'+med,q.gene_id.is_unique)
    check('CI_direction:'+med,(q['CI.L']<=q.logFC).all() and (q['CI.R']>=q.logFC).all())
raw=pd.read_csv(PAPER/'raw/GSE327565_raw_counts_GEO_YapTaz.csv.gz')
gm=load('gaona_samples.tsv');xx=raw[gm['column']].to_numpy()
check('raw_integral',np.isfinite(xx).all() and (xx>=0).all() and np.equal(xx,np.floor(xx)).all())
check('filter_gene_universe',set(raw.loc[(xx>=10).sum(axis=1)>=3,'ID'])==set(g.gene_id))
scores=load('bulk_program_scores.tsv');effects=load('bulk_program_effects.tsv');influence=load('bulk_library_influence.tsv')
bc=json.loads((PAPER/'trials/bulk_v1/contract.json').read_text())['contrasts']
for study,cs in [('Nb2',bc),('Gaona',{'YT_vs_WT_SFFFM':['YT_SFFFM','WT_SFFFM'],'YT_vs_WT_ADM':['YT_ADM','WT_ADM']})]:
    maxerr=0
    for rec in effects[effects.study.eq(study)].to_dict('records'):
        s=scores[(scores.study==study)&(scores.panel==rec['panel'])];a,b=cs[rec['contrast']]
        d=s[s.arm.eq(a)].score.mean()-s[s.arm.eq(b)].score.mean();maxerr=max(maxerr,abs(d-rec['delta']))
    check('library_mean_contrasts:'+study,maxerr<1e-10)
check('Nb2_influence_number',len(influence[influence.study.eq('Nb2')])==15*len(effects[effects.study.eq('Nb2')]))
# Existing source-panel extraction was implemented independently in R.
source=pd.read_csv(PAPER/'trials/bulk_v1/tables/panel_sample_scores.tsv',sep='\t')
y=scores[(scores.study=='Nb2')&(scores.panel=='YAP_source')].merge(source[source.panel.eq('Hippo_associated')],left_on='sample',right_on='accession',validate='one_to_one')
check('source_panel_reconciliation',len(y)==18 and np.allclose(y.score,y.mean_log2CPM))
sig=load('frozen_gaona_signature.tsv');freeze=json.loads((OUT/'signature_freeze.json').read_text())
check('signature_not_changed',sha(OUT/'tables/frozen_gaona_signature.tsv')==freeze['signature_sha256'])
check('signature_rule',len(sig)==100 and (sig['adj.P.Val']<.05).all() and (sig.logFC.abs()>.5).all() and sig.symbol.is_unique)
r=load('mouse_unit_expression.tsv.gz');p=load('mouse_program_scores.tsv');cov=load('mouse_unit_coverage.tsv')
check('CPM_denominators',np.allclose(r.cpm,1e6*r['counts']/r.total_umi,rtol=1e-11))
check('detection_bounds',r.detection.between(0,1).all())
check('unit_keys_unique',not cov.duplicated(['mode','unit','state','day']).any())
check('unit_gene_keys_unique',not r.duplicated(['mode','unit','state','day','gene']).any())
old=pd.read_csv(PAPER/'trials/atlas_v1/tables/unit_receptor_context.tsv.gz',sep='\t',low_memory=False)
old=old[old.dataset.eq('Niethamer2025')].copy();old['day']=old.day.astype(float)
j=r.merge(old,on=['mode','unit','state','day','condition','gene'],suffixes=('_new','_old'),validate='one_to_one')
check('independent_count_extraction',len(j)==57380 and np.array_equal(j['counts'],j.gene_counts) and np.array_equal(j.total_umi_new,j.total_umi_old) and np.array_equal(j.cells_new,j.cells_old))
ps=load('mouse_within_unit_differences.tsv');check('paired_arithmetic',np.allclose(ps.delta,ps.value_a-ps.value_b))
summary=load('mouse_paired_summary.tsv');check('no_sparse_cohort_promotion',np.array_equal(summary.cohort_eligible,summary.units>=3))
check('known_units_only',set(cov.unit)<=set(load('mouse_sample_context.tsv').unit))
# Recompute focal rank association by rank covariance, independently of scipy.spearmanr.
v=load('vascular_rival_inputs.tsv');z=v[(v.state=='CAP1')&(v.panel=='cycling')]
rho=z[['cpm','score']].rank().corr().iloc[0,1]
q=load('vascular_depth_round_audit.tsv');target=q[(q.state=='CAP1')&(q.program=='cycling')&(q.scope=='pooled')&(q.measurement=='cpm')]
check('vascular_rank_covariance',len(z)==8 and np.isclose(rho,target.rho.iloc[0]))
check('rounds_reported',set(q.scope)=={'pooled','2021-10-21','2022-07-06'})
check('figures_complete',len(list((OUT/'figures').glob('*.png')))==5 and len(list((OUT/'figures').glob('*.svg')))==5)
done('verification.json',passed=len(checks),failed=0,checks=checks,scope='Numerical and provenance checks, not biological validation. Large raw hash was frozen before execution; current size and independent aggregate reconciliation checked here.')
print('PASS:',len(checks),'numerical/provenance checks')
