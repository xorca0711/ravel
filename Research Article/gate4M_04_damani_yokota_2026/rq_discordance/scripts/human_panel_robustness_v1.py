"""F2: exposed component/donor influence, keeping frozen panels and donors."""
import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ARTICLE=Path('Research Article/gate2_DY1_damani_yokota_2026')
PRIMARY=Path('analysis/research/runs/DY1_human_observational_v1')
EXTERNAL=Path('analysis/research/runs/DY1_external_human_observational_v1')
QUAL=Path('analysis/research/runs/DY1_external_human_qualification_v2')
RAW=Path('raw_data/DY1_human_external_v1')
LABELS={'external_macrophage_union':['Macrophages','Proliferating Macrophages'],'external_Macrophages_only':['Macrophages']}
PANELS=['FABP4_panel','matrix_mac_panel']


def scalar_ranks(values):
    order=sorted(range(len(values)),key=lambda i:values[i]);ranks=[0.]*len(values);start=0
    while start<len(order):
        stop=start+1
        while stop<len(order) and values[order[stop]]==values[order[start]]:stop+=1
        for i in order[start:stop]:ranks[i]=(start+1+stop)/2
        start=stop
    return ranks


def estimate(x,y,kind):
    x=np.asarray(x,float);y=np.asarray(y,float)
    if not np.isfinite(x).all() or not np.isfinite(y).all():raise ValueError('Nonfinite donor measurement')
    if kind=='contrast':
        if min(len(x),len(y))<3:return np.nan,'fewer_than_3_donors'
        value=float(x.mean()-y.mean());independent=math.fsum(x)/len(x)-math.fsum(y)/len(y)
    else:
        if len(x)!=len(y):raise ValueError('Unpaired donor association')
        if len(x)<8:return np.nan,'fewer_than_8_donors'
        if np.ptp(x)==0 or np.ptp(y)==0:return np.nan,'constant_variable'
        value=float(spearmanr(x,y).statistic)
        a,b=scalar_ranks(x.tolist()),scalar_ranks(y.tolist());ma=math.fsum(a)/len(a);mb=math.fsum(b)/len(b)
        independent=math.fsum((v-ma)*(w-mb) for v,w in zip(a,b))/math.sqrt(math.fsum((v-ma)**2 for v in a)*math.fsum((w-mb)**2 for w in b))
    if not math.isclose(value,independent,rel_tol=1e-12,abs_tol=1e-12):raise ValueError('Independent estimate mismatch')
    return value,'estimated'


def panel_values(data,genes,omitted=''):
    retained=[g for g in genes if g!=omitted]
    if not retained or (omitted and omitted not in genes):raise ValueError('Invalid component omission')
    columns=['gene_'+g for g in retained]
    if any(c not in data for c in columns):raise ValueError('Missing component column')
    values=data[columns].to_numpy(dtype=float)
    if not np.isfinite(values).all():raise ValueError('Missing or nonfinite component value')
    return values.mean(axis=1)


def external_components(panels):
    q=json.loads((QUAL/'qualification.json').read_text())
    for key in ['all_cache_units_match_nCount_RNA','all_selected_gene_aggregates_match_current_raw','all_aggregate_totals_match_current_raw','aggregate_serializations_and_historical_totals_match','preparation_code_hash_verified']:
        if q[key] is not True:raise ValueError('Unqualified raw assay: '+key)
    mapping=pd.read_csv(QUAL/'gene_mapping.tsv',sep='\t').set_index('symbol')
    genes_needed=sorted({g for values in panels.values() for g in values})
    if not (mapping.loc[genes_needed,'cache_matches']==1).all():raise ValueError('Unqualified component')
    cache=np.load(RAW/'GSE135893_subtypes.npz',allow_pickle=False);counts,genes=cache['counts'],cache['genes']
    direct=np.load(QUAL/'direct_selected_counts.npz',allow_pickle=False)
    units=pd.read_csv(RAW/'GSE135893_subtypes_units.csv')
    meta=pd.read_csv(RAW/'GSE135893_IPF_metadata.csv.gz',usecols=['Sample_Name','Diagnosis','Sample_Source']).drop_duplicates()
    if meta.Sample_Name.duplicated().any():raise ValueError('Donor identity conflict')
    source=meta.set_index('Sample_Name');rows=[];checks=0
    if any((genes==g).sum()!=1 or (direct['symbols']==g).sum()!=1 for g in genes_needed):raise ValueError('Missing/ambiguous component symbol')
    for population,labels in LABELS.items():
        selected=units[(units.comp=='macrophages')&units.label.isin(labels)]
        for donor,group in selected.groupby('donor',sort=True):
            if group.disease.nunique()!=1:raise ValueError('Disease conflict')
            disease='Control' if group.disease.iloc[0]=='control' else group.disease.iloc[0]
            if source.loc[donor,'Diagnosis']!=disease:raise ValueError('Metadata disease conflict')
            cells=int(group.cells.sum())
            if cells<50:continue
            ix=group.index.to_numpy();pb=counts[ix].sum(axis=0);total=int(pb.sum())
            dp=direct['counts'][ix].sum(axis=0);dt=int(direct['totals'][ix].sum())
            if total<=0 or total!=dt:raise ValueError('Direct denominator parity failed')
            row=dict(donor=donor,disease=disease,source=source.loc[donor,'Sample_Source'],population=population,n_cells=cells,all_gene_counts=total)
            for g in genes_needed:
                value=int(pb[np.flatnonzero(genes==g)[0]]);ind=int(dp[np.flatnonzero(direct['symbols']==g)[0]])
                if value!=ind:raise ValueError('Direct component parity failed')
                row['gene_'+g]=float(np.log2(1+1e6*value/total));expected=math.log2(1+1e6*ind/dt)
                assert math.isclose(row['gene_'+g],expected,abs_tol=1e-12);checks+=2
            for panel,components in panels.items():row[panel]=math.fsum(row['gene_'+g] for g in components)/len(components)
            rows.append(row)
    result=pd.DataFrame(rows);manifest=json.loads((ARTICLE/'config/external_selection_v1.json').read_text())
    for population in LABELS:
        actual={d:sorted(g.donor.tolist()) for d,g in result[result.population==population].groupby('disease')}
        if actual!=manifest['populations'][population]:raise ValueError('Frozen donor selection changed')
    if meta[meta.Sample_Name.isin(result.donor)].sort_values('Sample_Name').to_dict('records')!=manifest['sources']:raise ValueError('Frozen sources changed')
    old=pd.read_csv(EXTERNAL/'donor_expression.tsv',sep='\t')
    both=result.merge(old,on=['donor','population'],validate='one_to_one',suffixes=('_new','_old'))
    if len(both)!=len(result) or len(both)!=len(old):raise ValueError('External row mismatch')
    for c in ['disease','source','n_cells','all_gene_counts']:
        if not both[c+'_new'].equals(both[c+'_old']):raise ValueError('Frozen donor metadata mismatch: '+c)
        checks+=len(both)
    for panel in PANELS:
        if not np.allclose(both[panel+'_new'],both[panel+'_old'],rtol=0,atol=1e-11):raise ValueError('Frozen panel parity failed')
        checks+=len(both)
    return result,checks


def diagnostics(data,panels,meta):
    if data.donor.duplicated().any():raise ValueError('Donor is not unique in scope')
    rows=[];diseases=['Control','IPF']+(['COPD'] if meta['cohort']=='GSE136831' else [])
    comparisons=[('IPF','Control')]+([('COPD','Control'),('IPF','COPD')] if 'COPD' in diseases else [])
    values={p:panel_values(data,g) for p,g in panels.items()}
    def append(kind,measure,group,mode,omitted,x,y,reference):
        val,status=estimate(x,y,kind)
        rows.append(dict(**meta,kind=kind,measure=measure,group=group,diagnostic=mode,omitted=omitted,
            n_first=len(x),n_second=len(y),estimate=val,reference=val if mode=='full' else reference,
            change=0. if mode=='full' and np.isfinite(val) else val-reference,status=status))
        return val
    for panel,genes in panels.items():
        for first,second in comparisons:
            ia=(data.disease==first).to_numpy();ib=(data.disease==second).to_numpy();v=values[panel];label=first+'-'+second
            full=append('contrast',panel,label,'full','',v[ia],v[ib],np.nan)
            for gene in genes:
                reduced=panel_values(data,genes,gene);append('contrast',panel,label,'leave_component_out',gene,reduced[ia],reduced[ib],full)
            for i in np.flatnonzero(ia|ib):
                keep=np.arange(len(data))!=i
                append('contrast',panel,label,'leave_donor_out',str(data.iloc[i].donor),v[ia&keep],v[ib&keep],full)
    for disease in diseases:
        mask=(data.disease==disease).to_numpy();x=values[PANELS[0]];y=values[PANELS[1]]
        full=append('association','FABP4_vs_matrix',disease,'full','',x[mask],y[mask],np.nan)
        for j,panel in enumerate(PANELS):
            for gene in panels[panel]:
                reduced=panel_values(data,panels[panel],gene)
                append('association','FABP4_vs_matrix',disease,'leave_component_out',panel+':'+gene,(reduced if j==0 else x)[mask],(reduced if j==1 else y)[mask],full)
        for i in np.flatnonzero(mask):
            keep=mask&(np.arange(len(data))!=i)
            append('association','FABP4_vs_matrix',disease,'leave_donor_out',str(data.iloc[i].donor),x[keep],y[keep],full)
    return pd.DataFrame(rows)


def saved_parity(results):
    tables={(cohort,kind):pd.read_csv(path/name,sep='\t') for cohort,path in [('GSE136831',PRIMARY),('GSE135893',EXTERNAL)] for kind,name in [('contrast','contrasts.tsv'),('association','associations.tsv')]}
    full=results[results.diagnostic=='full'].copy();checks=0;lo=[];hi=[]
    for r in full.itertuples(index=False):
        old=tables[(r.cohort,r.kind)];match=old.population==r.population
        match &= (old.floor==r.floor) if r.cohort=='GSE136831' else (old.scope==r.scope)
        if r.kind=='contrast':match&=(old.measure==r.measure)&(old.contrast==r.group);field='mean_difference'
        else:match&=(old.disease==r.group)&(old.x=='FABP4_panel')&(old.y=='matrix_mac_panel');field='rho'
        selected=old[match]
        if len(selected)!=1:raise ValueError('Nonunique prior full result')
        original=selected.iloc[0]
        if not ((pd.isna(original[field]) and pd.isna(r.estimate)) or math.isclose(float(original[field]),r.estimate,rel_tol=0,abs_tol=1e-11)):
            raise ValueError('Frozen full point estimate mismatch')
        expected_n=(int(original.n_first),int(original.n_second)) if r.kind=='contrast' else (int(original.n_donors),int(original.n_donors))
        if (r.n_first,r.n_second)!=expected_n:raise ValueError('Prior donor support changed')
        lo.append(original.ci_low);hi.append(original.ci_high);checks+=2
    full['original_ci_low']=lo;full['original_ci_high']=hi
    full['interval_source']='Frozen original pointwise bootstrap; copied, not refitted'
    return full,checks


def summarize_omissions(results):
    keys=['cohort','population','floor','scope','kind','measure','group','diagnostic']
    summaries=[]
    for key,g in results[results.diagnostic!='full'].groupby(keys,sort=True):
        finite=g[np.isfinite(g.estimate)];reference=float(g.reference.iloc[0]);comparable=np.isfinite(reference)
        summaries.append(dict(zip(keys,key),reference=reference,omissions=len(g),estimable=len(finite),
            minimum=float(finite.estimate.min()) if len(finite) else np.nan,maximum=float(finite.estimate.max()) if len(finite) else np.nan,
            maximum_absolute_change=float(finite.change.abs().max()) if comparable and len(finite) else np.nan,
            strict_sign_reversals=int((finite.estimate*reference<0).sum()) if comparable else np.nan,
            comparison_status='defined_reference' if comparable else 'reference_unavailable',undefined=len(g)-len(finite)))
    return pd.DataFrame(summaries)


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    all_panels=json.loads((ARTICLE/'config/human_panels_v1.json').read_text())['panels'];panels={p:all_panels[p] for p in PANELS}
    primary=pd.read_csv(PRIMARY/'donor_expression.tsv.gz',sep='\t');external,checks=external_components(panels)
    tables=[];selected=[]
    for pop,floor in [('Macrophage',20),('AllMacrophages',50)]:
        data=primary[(primary.population==pop)&(primary.n_cells>=floor)&primary.disease.isin(['Control','IPF','COPD'])].copy()
        for panel,genes in panels.items():
            if not np.allclose(panel_values(data,genes),data[panel],rtol=0,atol=1e-11):raise ValueError('Primary components do not reproduce frozen panel')
            checks+=len(data)
        meta=dict(cohort='GSE136831',population=pop,floor=floor,scope='all_sources')
        selected.append(data.assign(cohort=meta['cohort'],floor=floor,scope=meta['scope']))
        tables.append(diagnostics(data,panels,meta))
    for pop in LABELS:
        for scope in ['all_sources','Vanderbilt']:
            data=external[external.population==pop].copy()
            if scope!='all_sources':data=data[data.source==scope]
            meta=dict(cohort='GSE135893',population=pop,floor=50,scope=scope)
            selected.append(data.assign(cohort=meta['cohort'],floor=50,scope=scope));tables.append(diagnostics(data,panels,meta))
    results=pd.concat(tables,ignore_index=True);full,n=saved_parity(results);checks+=n+len(results)
    summary=summarize_omissions(results)
    components=pd.concat(selected,ignore_index=True)
    cols=['cohort','population','floor','scope','donor','disease','n_cells','all_gene_counts']+PANELS+['gene_'+g for p in PANELS for g in panels[p]]
    for name,frame in [('donor_components.tsv.gz',components[cols]),('external_reaggregated_components.tsv',external),('all_omissions.tsv',results),('full_estimates.tsv',full),('robustness_summary.tsv',summary)]:
        frame.to_csv(out/name,sep='\t',index=False,na_rep='NA',compression={'method':'gzip','mtime':0} if name.endswith('.gz') else None)
    fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained')
    scope=[('GSE136831','Macrophage'),('GSE135893','external_macrophage_union')]
    colors={'leave_component_out':'#d17b37','leave_donor_out':'#477b99'}
    for ax,(cohort,pop) in zip(axes,scope):
        d=summary[(summary.cohort==cohort)&(summary.population==pop)&(summary.scope=='all_sources')&(summary.kind=='contrast')&(summary.group=='IPF-Control')]
        for i,panel in enumerate(PANELS):
            for j,mode in enumerate(colors):
                r=d[(d.measure==panel)&(d.diagnostic==mode)].iloc[0];y=i+(j-.5)*.16
                ax.plot([r.minimum,r.maximum],[y,y],lw=4,color=colors[mode],label=mode.replace('_',' ') if i==0 else None)
                ax.plot(r.reference,y,'ko',ms=4)
        ax.axvline(0,color='gray',lw=.7);ax.set(yticks=[0,1],yticklabels=['FABP4 panel','Matrix-associated panel'],xlabel='IPF minus Control: mean gene log2(CPM + 1)',title=cohort+' | '+('Macrophage >=20 cells' if cohort=='GSE136831' else 'Macrophage union >=50 cells'))
        ax.legend(fontsize=8);ax.invert_yaxis()
    fig.suptitle('Observed omission ranges; black points retain the full estimate\nRanges are influence diagnostics, not confidence intervals',fontsize=12)
    fig.savefig(out/'human_panel_robustness.png',dpi=150);plt.close(fig)
    (out/'verification.json').write_text(json.dumps({'status':'passed','checks':checks,'method':'Qualified external count/component parity; exact frozen donors/sites; all full-result parity; scalar means and independently tied ranks for every estimated omission; held rows retain original floors'},indent=2)+'\n')
    (out/'summary.json').write_text(json.dumps({'analysis_id':'DY1-P01.human_panel_robustness_v1','rows':len(results),'full_rows':len(full),'status_counts':results.status.value_counts().to_dict(),'missing_symbol':'SELENOP remains unavailable externally; no identity/proxy analysis or substitution','scope':'Two fixed macrophage panels; separate one-component or one-donor omissions, never combined; no reduced panel or excluded donor replaces primary','other_holds':'External Vanderbilt within-disease correlations and fibroblast recipient correlations remain unsupported; no clinical/depth/floor rerun','scientific_acceptance':'not_assessed'},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
