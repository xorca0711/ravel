"""Fixed test-convention and workbook audit of two previously exposed residuals."""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import statistics

import numpy as np
import openpyxl
from scipy import stats

PACKAGE=Path('Research Article/ungated_navarro_negredo_2026_aged_brain_il10')
RUN=Path('analysis/research/runs/nn26_animal_reproduction_v1')


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True,type=Path)
    out=parser.parse_args().output
    original=load('nn26_original_reproduction',PACKAGE/'scripts/reproduce_animals_v1.py')
    exact=load('nn26_exact_rank',PACKAGE/'scripts/tie_diagnostic_v2.py')
    workbook=Path('raw_data/navarro_2026/source_v1/S4.xlsx')
    values=original.raw_cells(workbook)
    formula=openpyxl.load_workbook(workbook,data_only=False,read_only=True)
    cached=openpyxl.load_workbook(workbook,data_only=True,read_only=True)
    observations=list(csv.DictReader((RUN/'observations.csv').open()))
    prior=list(csv.DictReader(Path('analysis/research/runs/nn26_tie_diagnostic_v2/exact_rank_reconciliation.csv').open()))
    configuration=json.loads((PACKAGE/'config/animal_panels_v1.json').read_text())
    panels={x['id']:x for x in configuration['endpoints']}
    declared=[('open_field','D25K','Control',5),('ifitm3','WT','Control',4)]
    rows=[]; audits=[]; verified=0
    for endpoint,group_a,group_b,digits in declared:
        panel=panels[endpoint]; groups=[]
        for group in (group_a,group_b):
            items=[x for x in observations if x['endpoint']==endpoint and x['group']==group]
            for item in items:
                assert float(item['value'])==values[item['sheet']][item['cell']]
                verified+=1
            groups.append([float(x['value']) for x in items])
        a,b=groups; n,m=len(a),len(b); comparison=group_a+'-'+group_b
        reported=panel['reported'][comparison]
        u=sum((x>y)+.5*(x==y) for x in a for y in b)
        ref=stats.mannwhitneyu(a,b,method='asymptotic',use_continuity=True)
        assert u==ref.statistic
        tied=len(set(a+b))<n+m
        doubled,absolute,_,_=exact.exact(a,b)
        previous=next(x for x in prior if x['endpoint']==endpoint and x['comparison']==comparison)
        assert abs(absolute-float(previous['p_exact_tied_absolute_tail']))<1e-14
        standard=math.sqrt(n*m*(n+m+1)/12)
        variants=[
            ('exact_tied_absolute_tail',absolute,True),
            ('exact_tied_doubled_inclusive_tail',doubled,True),
            ('asymptotic_tie_corrected_with_continuity',ref.pvalue,True),
            ('asymptotic_tie_corrected_no_continuity',stats.mannwhitneyu(a,b,method='asymptotic',use_continuity=False).pvalue,True),
            ('normal_ignoring_ties_no_continuity',stats.ranksums(a,b).pvalue,not tied),
            ('normal_ignoring_ties_with_continuity',min(1.,2*stats.norm.sf((abs(u-n*m/2)-.5)/standard)),not tied),
            ('scipy_exact_untied_reference',stats.mannwhitneyu(a,b,method='exact').pvalue,not tied),
        ]
        for method,p,applicable in variants:
            rows.append(dict(endpoint=endpoint,comparison=comparison,n_a=n,n_b=m,ties=tied,
                method=method,applicable=applicable,p_value=float(p),p_reported=reported,
                matches_reported_rounding=round(float(p),digits)==reported,
                source=f'{panel["sheet"]}!{panel["source_statistics"]}'))
        # Complete untied exact support at the observed n/m, not a search over exclusions.
        _,distribution=exact.distribution(list(range(n+m)),n)
        total=sum(distribution.values()); cumulative=0; support=[]
        for rank_sum,count in sorted(distribution.items()):
            lower=cumulative+count; upper=total-cumulative
            support.append(min(1.,2*min(lower,upper)/total)); cumulative+=count
        attainable=any(round(p,digits)==reported for p in support)
        audits.append(dict(endpoint=endpoint,comparison=comparison,
            observed_group_sizes=[n,m],rank_u=u,ties=tied,reported_p=reported,
            reported_rounding_digits=digits,any_applicable_convention_matches=any(
                r['applicable'] and r['matches_reported_rounding'] for r in rows if r['endpoint']==endpoint),
            untied_exact_reported_value_attainable_at_observed_n=attainable,
            untied_support_applicable=not tied,
            source_statistics_cell=cached[panel['sheet']][panel['source_statistics']].value))
    formulas=[]
    for group,column,stop in [('Control','D',106),('D25K','E',108)]:
        obs=[float(x['value']) for x in observations if x['endpoint']=='open_field' and x['group']==group]
        assert math.isclose(statistics.mean(obs),float(np.mean(obs)),abs_tol=1e-12)
        for row in (109,110):
            cell=column+str(row)
            formulas.append(dict(group=group,cell='Figure 7!'+cell,
                formula=formula['Figure 7'][cell].value,cached_value=cached['Figure 7'][cell].value,
                complete_observation_range=f'{column}94:{column}{stop}',
                complete_observation_n=len(obs),complete_mean=statistics.mean(obs),
                first_listed_value=values['Figure 7'][column+'94']))
    with (out/'test_conventions.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    result=dict(analysis='Nn26-P01.residual_diagnostics_v3',source_values_verified=verified,
        observations_changed=False,exclusions_searched=False,rounding_of_observations=False,
        audits=audits,open_field_formula_audit=formulas,
        interpretation='Diagnostic conventions only. No candidate method replaces v1/v2, and no population or repair claim is added.')
    (out/'diagnostic.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    (out/'.gitattributes').write_text('* -text whitespace=cr-at-eol\n',encoding='utf-8',newline='\n')
    formula.close(); cached.close()
    print(json.dumps({'verified_source_values':verified,'residuals':audits}))


if __name__=='__main__': main()
