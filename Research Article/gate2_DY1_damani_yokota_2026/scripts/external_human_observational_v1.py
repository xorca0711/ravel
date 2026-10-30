"""Exposed external macrophage RNA transport description, not NAM validation."""
import argparse,json,math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from human_stats_v1 import log_cpm,mean_difference,correlation_summary

ARTICLE=Path('Research Article/gate2_DY1_damani_yokota_2026')
RAW=Path('raw_data/DY1_human_external_v1')
QUAL=Path('analysis/research/runs/DY1_external_human_qualification_v2')
PRIMARY=Path('analysis/research/runs/DY1_human_observational_v1')
LABELS={'external_macrophage_union':['Macrophages','Proliferating Macrophages'],
        'external_Macrophages_only':['Macrophages']}
MEASURES=['FABP4_panel','matrix_mac_panel','ARG1_logCPM']

def aggregate(counts,genes,units,donors,panels):
    needed=sorted(set(panels['FABP4_panel']+panels['matrix_mac_panel']+['ARG1']))
    if any(int((genes==g).sum())!=1 for g in needed):raise ValueError('Outcome symbol missing or ambiguous')
    if donors.Sample_Name.duplicated().any():raise ValueError('Donor source/diagnosis conflict')
    rows=[];source=donors.set_index('Sample_Name')
    for population,labels in LABELS.items():
        subset=units[(units.comp=='macrophages')&units.label.isin(labels)]
        for donor,group in subset.groupby('donor',sort=True):
            if group.disease.nunique()!=1:raise ValueError('Donor disease conflict')
            selected=group.index.to_numpy();pb=counts[selected].sum(axis=0);total=int(pb.sum());cells=int(group.cells.sum())
            if cells<50:continue
            norm=log_cpm(pb[None,:],np.array([total]))[0]
            disease='Control' if group.disease.iloc[0]=='control' else group.disease.iloc[0]
            if source.loc[donor,'Diagnosis']!=disease:raise ValueError('Source diagnosis mismatch')
            r=dict(donor=donor,disease=disease,source=source.loc[donor,'Sample_Source'],population=population,n_cells=cells,all_gene_counts=total)
            for panel in MEASURES[:2]:r[panel]=float(norm[[np.flatnonzero(genes==g)[0] for g in panels[panel]]].mean())
            r['ARG1_logCPM']=float(norm[np.flatnonzero(genes=='ARG1')[0]])
            r['ARG1_raw_counts']=int(pb[np.flatnonzero(genes=='ARG1')[0]])
            rows.append(r)
    return pd.DataFrame(rows)

def write(out,name,t):t.to_csv(out/name,sep='\t',index=False,lineterminator='\n')

def main(out):
    q=json.loads((QUAL/'qualification.json').read_text())
    for key in ['all_cache_units_match_nCount_RNA','all_selected_gene_aggregates_match_current_raw','all_aggregate_totals_match_current_raw','aggregate_serializations_and_historical_totals_match','preparation_code_hash_verified']:
        if q[key] is not True:raise ValueError('Unqualified raw assay: '+key)
    mapping=pd.read_csv(QUAL/'gene_mapping.tsv',sep='\t').set_index('symbol')
    panels=json.loads((ARTICLE/'config/human_panels_v1.json').read_text())['panels']
    needed=sorted(set(panels['FABP4_panel']+panels['matrix_mac_panel']+['ARG1']))
    if not (mapping.loc[needed,'cache_matches']==1).all():raise ValueError('Unqualified outcome gene')
    data=np.load(RAW/'GSE135893_subtypes.npz',allow_pickle=False);counts=data['counts'];genes=data['genes']
    units=pd.read_csv(RAW/'GSE135893_subtypes_units.csv');meta=pd.read_csv(RAW/'GSE135893_IPF_metadata.csv.gz')
    donors=meta[['Sample_Name','Diagnosis','Sample_Source']].drop_duplicates()
    table=aggregate(counts,genes,units,donors,panels);write(out,'donor_expression.tsv',table)
    coverage=table.groupby(['population','source','disease']).agg(donors=('donor','size'),cells=('n_cells','sum')).reset_index();write(out,'coverage.tsv',coverage)
    manifest=json.loads((ARTICLE/'config/external_selection_v1.json').read_text());expected=manifest['populations']
    for population in LABELS:
        actual={d:sorted(g.donor.tolist()) for d,g in table[table.population==population].groupby('disease')}
        if actual!=expected[population]:raise ValueError('Frozen donor set changed')
    actual_sources=donors[donors.Sample_Name.isin(table.donor)].sort_values('Sample_Name').to_dict('records')
    if actual_sources!=manifest['sources']:raise ValueError('Frozen source/diagnosis set changed')
    rng=np.random.default_rng(20261029);contrasts=[];associations=[]
    for population in LABELS:
        for scope in ['all_sources','Vanderbilt']:
            t=table[table.population==population]
            if scope=='Vanderbilt':t=t[t.source=='Vanderbilt']
            for measure in MEASURES:
                a=t.loc[t.disease=='IPF',measure].to_numpy();b=t.loc[t.disease=='Control',measure].to_numpy()
                contrasts.append(dict(population=population,scope=scope,measure=measure,contrast='IPF-Control',n_first=len(a),n_second=len(b),mean_first=float(a.mean()),mean_second=float(b.mean()),mean_difference=float(a.mean()-b.mean()),**mean_difference(a,b,rng)))
            for disease in ['Control','IPF']:
                d=t[t.disease==disease];x=d.FABP4_panel.to_numpy();y=d.matrix_mac_panel.to_numpy()
                result=correlation_summary(x,y,np.empty((len(d),0)),rng)
                result={k:v for k,v in result.items() if not k.startswith('partial_')}
                associations.append(dict(population=population,scope=scope,disease=disease,x='FABP4_panel',y='matrix_mac_panel',**result))
    contrasts=pd.DataFrame(contrasts);associations=pd.DataFrame(associations)
    write(out,'contrasts.tsv',contrasts);write(out,'associations.tsv',associations)
    pc=pd.read_csv(PRIMARY/'contrasts.tsv',sep='\t')
    comparator=pc[(pc.population=='AllMacrophages')&(pc.floor==50)&(pc.contrast=='IPF-Control')&pc.measure.isin(MEASURES)].copy()
    comparison=contrasts[(contrasts.population=='external_macrophage_union')&(contrasts.scope=='all_sources')][['measure','mean_difference','ci_low','ci_high','n_first','n_second']].merge(comparator[['measure','mean_difference','ci_low','ci_high','n_first','n_second']],on='measure',suffixes=('_external','_primary_sensitivity'),validate='one_to_one')
    write(out,'cross_cohort_description.tsv',comparison)
    # Independent audit uses direct sparse-source aggregates and Python's scalar logarithm.
    direct=np.load(QUAL/'direct_selected_counts.npz',allow_pickle=False);checks=0
    for r in table.itertuples():
        sel=units[(units.donor==r.donor)&(units.comp=='macrophages')&units.label.isin(LABELS[r.population])].index
        pb=direct['counts'][sel].sum(axis=0);total=int(direct['totals'][sel].sum())
        if total!=r.all_gene_counts:raise ValueError('Direct denominator mismatch')
        for panel in MEASURES[:2]:
            value=sum(math.log2(1+int(pb[np.flatnonzero(direct['symbols']==g)[0]])*1e6/total) for g in panels[panel])/len(panels[panel])
            if not math.isclose(value,getattr(r,panel),abs_tol=1e-11):raise ValueError('Independent panel mismatch')
            checks+=1
        val=math.log2(1+int(pb[np.flatnonzero(direct['symbols']=='ARG1')[0]])*1e6/total)
        if not math.isclose(val,r.ARG1_logCPM,abs_tol=1e-11):raise ValueError('Independent ARG1 mismatch')
        checks+=2
    for r in contrasts.itertuples():
        t=table[table.population==r.population]
        if r.scope!='all_sources':t=t[t.source==r.scope]
        a=t[t.disease=='IPF'][r.measure].tolist();b=t[t.disease=='Control'][r.measure].tolist()
        if not math.isclose(sum(a)/len(a)-sum(b)/len(b),r.mean_difference,abs_tol=1e-11):raise ValueError('Independent contrast mismatch')
        checks+=1
    for r in associations.itertuples():
        if r.status!='estimated':continue
        t=table[(table.population==r.population)&(table.disease==r.disease)]
        if r.scope!='all_sources':t=t[t.source==r.scope]
        if not math.isclose(float(spearmanr(t.FABP4_panel,t.matrix_mac_panel).statistic),r.rho,abs_tol=1e-11):raise ValueError('Independent correlation mismatch')
        checks+=1
    (out/'verification.json').write_text(json.dumps(dict(ok=True,checks=checks,method='Current-raw selected counts and all-gene denominators; scalar log2; independent mean sums and SciPy Spearman.'),indent=2)+'\n')
    fig,axes=plt.subplots(1,3,figsize=(11,3.7),constrained_layout=True)
    t=table[table.population=='external_macrophage_union']
    for ax,measure in zip(axes,MEASURES):
        for i,disease in enumerate(['Control','IPF']):
            values=t[t.disease==disease][measure].to_numpy();jitter=np.linspace(-.12,.12,len(values))
            ax.scatter(i+jitter,values,s=28,color=['#287f8e','#ba582a'][i],alpha=.8);ax.plot([i-.18,i+.18],[values.mean()]*2,color='black',lw=2)
        ax.set_xticks([0,1],['Control (n=9)','IPF (n=12)']);ax.set_title(measure.replace('_',' '));ax.set_ylabel('mean gene log2(CPM + 1)' if 'panel' in measure else 'ARG1 log2(CPM + 1)');ax.spines[['top','right']].set_visible(False)
    fig.suptitle('GSE135893: deposited macrophage union, donor floor 50\nExposed external description; labels differ from primary atlas',fontsize=11)
    fig.savefig(out/'external_overview.png',dpi=160);plt.close(fig)
    summary=dict(analysis_id='DY1-P01.external_human_observational_v1',eligible_donors={'Control':9,'IPF':12},qualified_outcome_symbols=needed,unmapped_identity_marker='SELENOP; not needed or substituted for this bounded analysis',contrasts=len(contrasts),association_status=associations.status.value_counts().to_dict(),clinical_adjustment='not performed; unqualified external age/sex and other clinical fields',scope='Exposed source-adapted transport description; different annotations, same gene formulas. No NAM, proxy, COPD or recipient mechanism claim.',scientific_acceptance='not_assessed')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
