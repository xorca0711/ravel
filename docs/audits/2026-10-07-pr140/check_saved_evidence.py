"""Read-only arithmetic/provenance audit of saved PR140 outputs; no model fits."""
from pathlib import Path
import json, sys, subprocess
import numpy as np
import pandas as pd
from scipy import stats
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'analysis'))
from lib.research_governance import receipt_errors
RUN=ROOT/'analysis/research/runs'
registry=json.loads((ROOT/'analysis/research/registry.json').read_text(encoding='utf-8'))
receipts=[p for p in registry['receipts'] if '/wp_' in p]
verification={p:receipt_errors(ROOT,p) for p in receipts}
checks=[]
def check(label,condition):
    checks.append({'check':label,'passed':bool(condition)})
def near(a,b):return np.allclose(a,b,rtol=1e-6,atol=2e-7,equal_nan=True)
def bh(p):
    p=np.asarray(p,float);order=np.argsort(p);q=np.empty(len(p));q[order]=np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1];return np.minimum(q,1)
act=RUN/'wp_a30_activation_stratified_v3'
cells=pd.read_csv(act/'cell_strata.csv.gz')
contr=pd.read_csv(act/'stratified_contrasts.csv')
support=pd.read_csv(act/'stratum_support.csv')
for r in contr.itertuples():
    sub=cells[cells.stratum==r.stratum]
    sizes=sub.groupby(['donor','tissue']).size().unstack().fillna(0)
    keep=sizes.index[(sizes.CSF>=50)&(sizes.PBMCs>=50)]
    means=sub.groupby(['donor','tissue'])[r.score].mean().unstack().loc[keep]
    d=means.CSF-means.PBMCs
    check(f'{r.stratum}/{r.score}: donor median, signs, Wilcoxon',len(d)==r.n_donors and (d>0).sum()==r.n_donors_positive and near(d.median(),r.median_difference) and near(stats.wilcoxon(d).pvalue,r.wilcoxon_p))
fam=contr[contr.in_primary_family]
check('A30 primary BH arithmetic',near(bh(fam.empirical_two_sided_p),fam.bh_within_family))
qcs=pd.read_csv(act/'sample_qc.csv')
check('QC counts sum to exported cells',qcs.n_cd4_lineage.sum()==len(cells))
check('Stratum support equals saved cells',near(support.n_cells,cells.groupby(['donor','tissue','stratum']).size().reindex(pd.MultiIndex.from_frame(support[['donor','tissue','stratum']])).to_numpy()))
cellsets={}
decs={}
for name,file,state in [('wp_a30_activation_stratified_v3','cell_strata.csv.gz','stratum'),('wp_a30_state_decomposition_v3','cell_states.csv.gz','state')]:
    c=pd.read_csv(RUN/name/file);table=pd.read_csv(RUN/name/'decomposition.csv')
    unmatched=[]
    for r in table.itertuples():
        sub=c[c.donor==r.donor]
        n=sub.groupby([state,'tissue']).size().unstack().fillna(0)
        m=sub.groupby([state,'tissue'])[r.score].mean().unstack()
        pooled=sub.groupby(state)[r.score].mean()
        w=n/n.sum(axis=0)
        absent=(n.CSF==0)|(n.PBMCs==0)
        if state=='state':m=m.apply(lambda s:s.fillna(pooled))
        else:m=m.fillna(0)
        comp=((w.CSF-w.PBMCs)*(m.CSF+m.PBMCs)/2).sum()
        within=((w.CSF+w.PBMCs)*(m.CSF-m.PBMCs)/2).sum()
        total=(w.CSF*m.CSF-w.PBMCs*m.PBMCs).sum()
        check(f'{name}/{r.score}/{r.donor}: decomposition',near([total,comp,within],[r.total,r.composition,r.within]))
        if r.score=='proinflammatory_authors':unmatched.append({'donor':r.donor,'one_compartment_states':int(absent.sum()),'csf_fraction_in_unmatched_states':float(w.CSF[absent].sum()),'blood_fraction_in_unmatched_states':float(w.PBMCs[absent].sum())})
    primary=table[table.score=='proinflammatory_authors']
    decs[name]={'donors':len(primary),'median_total':float(primary.total.median()),'median_composition':float(primary.composition.median()),'median_within':float(primary.within.median()),'ratio_of_medians':float(primary.composition.median()/primary.total.median()),'median_donor_share':float((primary.composition/primary.total).median()),'one_compartment_support':unmatched}
    cellsets[name]={'rows':len(c),'has_barcode_column':any('barcode' in k.lower() for k in c.columns),'counts_by_donor_tissue':c.groupby(['donor','tissue']).size().reset_index(name='n_cells').to_dict('records')}
floor=RUN/'wp_r1_floor_sensitivity_v1'
named=pd.read_csv(floor/'floor_sweep_named_genes.csv');hits=pd.read_csv(floor/'unfiltered_bh_hits.csv')
check('R1 floor-invariant named-gene effects and raw p',all(g.glucose_effect_25mM_minus_1mM.dropna().max()-g.glucose_effect_25mM_minus_1mM.dropna().min()<1e-12 and g.p_interaction.dropna().max()-g.p_interaction.dropna().min()<1e-12 for _,g in named.groupby(['cell_type','symbol'])))
compass=pd.read_csv(RUN/'wp_compass_sensitivity_v2_rerun/named_reactions.csv')
pgm=compass[compass.reaction=='PGM_pos'].iloc[0]
result={'audit_head':'74d6bd6b1c0ee411c929efbf473b5fd39dcce243','mode':'saved-artifact verification; no scientific fits or source-data reruns','receipt_count':len(verification),'receipt_failures':{k:v for k,v in verification.items() if v},'checks':checks,'a30_primary':fam.to_dict('records'),'a30_activation_control':contr[contr.score=='activation_disjoint'].to_dict('records'),'cellsets':cellsets,'decomposition':decs,'r1_floor_universes':pd.read_csv(floor/'floor_sweep_universe.csv').to_dict('records'),'r1_unfiltered_hits':len(hits),'r1_hits_never_reaching_1cpm':int((hits.n_libraries_at_1cpm==0).sum()),'compass_pgm_penalty_rho':float(pgm.rho_pathogenicity_authors),'compass_pgm_monotonic_consistency_rho':float(-pgm.rho_pathogenicity_authors),'compass_note':'Sign inversion follows a strictly decreasing -log1p transformation of nonnegative penalties. Raw reactions.tsv is not tracked; no solver re-execution claimed.','limits':['Empirical null tails cannot be independently re-counted: null_draw_sample.csv saves summaries, not 10000 draw statistics.','No raw-input or barcode-level QC replay; cell exports lack original barcode IDs.','No equivalence, biological acceptance, causal inference or independent replication established.']}
out=Path(__file__).with_name('verification.json');out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'receipts':len(verification),'receipt_failures':result['receipt_failures'],'checks':len(checks),'failed_checks':[c for c in checks if not c['passed']],'decomposition':{k:{a:b for a,b in v.items() if a!='one_compartment_support'} for k,v in decs.items()},'compass_pgm_penalty_rho':float(pgm.rho_pathogenicity_authors),'corrected_orientation_rho':float(-pgm.rho_pathogenicity_authors)},indent=2))
sys.exit(bool(result['receipt_failures'] or any(not c['passed'] for c in checks)))
