"""Independently check the RQ table arithmetic, eligibility and prior-result agreement."""
import csv
from collections import defaultdict
from datetime import datetime, timezone
import math
from pypdf import PdfReader
from common import PACKAGE, new_run, read_json, write_json, finish_record, sha256


def table(path):
    with (PACKAGE/path).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))


def num(r,k):
    return float(r[k]) if r.get(k,'') else math.nan


def close(a,b):
    if math.isnan(a) and math.isnan(b):return
    if not math.isclose(a,b,rel_tol=2e-9,abs_tol=2e-6):raise ValueError(f'Arithmetic mismatch: {a} versus {b}')


def average(rows,field):
    values=[num(r,field) for r in rows if math.isfinite(num(r,field))]
    return sum(values)/len(values) if values else math.nan


def main():
    checks=[];out=new_run(PACKAGE/'runs/rq_validation_v1')
    fields=['observed_cell_CPM','equal_subtype_cell_CPM','composition_departure_cell_CPM',
            'observed_bulk_CPM','equal_subtype_bulk_CPM','composition_departure_bulk_CPM']
    rows=table('runs/rq1_composition_v1/stratum_accounting.tsv')
    groups=defaultdict(list)
    for r in rows:
        p=num(r,'captured_adventitial_fraction');a=num(r,'alveolar_mean_cell_CPM');b=num(r,'adventitial_mean_cell_CPM')
        close(p,num(r,'n_right')/(num(r,'n_left')+num(r,'n_right')))
        close(num(r,'observed_cell_CPM'),(1-p)*a+p*b)
        close(num(r,'equal_subtype_cell_CPM'),(a+b)/2)
        close(num(r,'composition_departure_cell_CPM'),(p-.5)*(b-a))
        w=num(r,'library_adventitial_fraction');a=num(r,'alveolar_bulk_CPM');b=num(r,'adventitial_bulk_CPM')
        close(num(r,'observed_bulk_CPM'),(1-w)*a+w*b)
        close(num(r,'equal_subtype_bulk_CPM'),(a+b)/2)
        close(num(r,'composition_departure_bulk_CPM'),(w-.5)*(b-a))
        if min(num(r,'n_left'),num(r,'n_right'))<num(r,'cell_floor'):raise ValueError('Eligibility failure')
        groups[tuple(r[k] for k in ['cohort','assay','donor_id','cell_floor'])].append(r)
    for r in table('runs/rq1_composition_v1/donor_accounting.tsv'):
        part=groups[tuple(r[k] for k in ['cohort','assay','donor_id','cell_floor'])]
        for field in fields:close(num(r,field),average(part,field))
    checks.append({'check':'RQ1 cell/library mixture identities, floors and equal-stratum donor aggregation','rows':len(rows),'status':'pass'})
    for stage,extra in [('rq1b_endpoint_v1',['gene']),('rq2_myrf_v1',['comparator','gene'])]:
        keys=['cohort','assay','donor_id','cell_floor']+extra;groups=defaultdict(list)
        rows=table('runs/'+stage+'/stratum_effects.tsv')
        for r in rows:
            close(num(r,'delta_log2CPM'),num(r,'left_log2CPM')-num(r,'right_log2CPM'))
            if min(num(r,'n_left'),num(r,'n_right'))<num(r,'cell_floor'):raise ValueError('Invalid donor eligibility')
            groups[tuple(r[k] for k in keys)].append(r)
        for r in table('runs/'+stage+'/donor_effects.tsv'):
            part=groups[tuple(r[k] for k in keys)]
            for field in ['left_log2CPM','right_log2CPM','delta_log2CPM','delta_detection']:close(num(r,field),average(part,field))
        checks.append({'check':stage+' differences, floors and donor aggregation','rows':len(rows),'status':'pass'})
    donors=table('runs/rq1b_endpoint_v1/donor_effects.tsv')
    lookup={tuple(r[k] for k in ['cohort','assay','donor_id','cell_floor','gene']):num(r,'delta_log2CPM') for r in donors}
    panel=read_json(PACKAGE/'config/rq_sequence_v1.json')['chemokines']
    panel_rows=table('runs/rq1b_endpoint_v1/panel_sensitivity.tsv')
    for r in panel_rows:
        key=tuple(r[k] for k in ['cohort','assay','donor_id','cell_floor'])
        values=[lookup[key+(g,)] for g in panel if g!=r['omitted_gene']]
        complete=all(math.isfinite(lookup[key+(g,)]) for g in panel)
        expected=sum(values)/len(values) if complete else math.nan
        close(num(r,'panel_delta'),expected);close(num(r,'C3_delta'),lookup[key+('C3',)])
        if str(complete)!=r['panel_complete']:raise ValueError('Panel missingness mismatch')
        if complete:
            c=lookup[key+('C3',)]
            direction='uninformative_zero' if abs(c)<=1e-12 or abs(expected)<=1e-12 else ('same' if c*expected>0 else 'opposite')
            if direction!=r['direction_status']:raise ValueError('Direction mismatch')
    checks.append({'check':'RQ1b fixed and every gene-omission panel, missingness and direction','rows':len(panel_rows),'status':'pass'})
    prior=table('runs/reproduction_v1/paired_effects.tsv')
    lookup={(r['contrast'],r['assay'],r['donor_id'],r['gene']):r for r in prior if r['anatomical_region']=='distal'}
    compared=0
    for stage,contrast in [('rq1b_endpoint_v1','fibroblast_identity'),('rq2_myrf_v1','AT1_vs_AT2')]:
        for r in table('runs/'+stage+'/donor_effects.tsv'):
            if r['cohort']!='Travaglini':continue
            if stage=='rq2_myrf_v1' and r['comparator']!='Alveolar Epithelial Type 2':continue
            old=lookup.get((contrast,r['assay'],r['donor_id'],r['gene']))
            if old:
                close(num(r,'delta_log2CPM'),num(old,'delta_log2CPM'));compared+=1
    old_external={(r['suspension_type'],r['donor_id'],r['cell_floor'],r['gene']):r for r in table('runs/external_pilot_v1/donor_effects.tsv')}
    for r in donors:
        if r['cohort']!='Madissoon':continue
        old=old_external.get((r['assay'].replace('Madissoon ',''),r['donor_id'],r['cell_floor'],r['gene']))
        if old:close(num(r,'delta_log2CPM'),num(old,'mean_delta_log2CPM'));compared+=1
    checks.append({'check':'Agreement with prior source and external fits for overlapping endpoints','comparisons':compared,'status':'pass'})
    for row in read_json(PACKAGE/'runs/rq2_myrf_v1/endpoint_gate.json'):
        if row['linked_non_RNA_mature_endpoint'] or row['maturation_fit_performed']:raise ValueError('Unsupported maturation fit')
    gates=table('runs/rq2_myrf_v1/cohort_summary.tsv')
    for r in gates:
        expected=num(r,'n_donors')>=3
        if str(expected)!=r['replicated_description_eligible']:raise ValueError('Replication threshold changed')
    if len(PdfReader(PACKAGE/'figures/rq_sequence_v1/Nb4_complete_atlas.pdf').pages)!=15:raise ValueError('Atlas page count')
    checks.append({'check':'Mature-endpoint/replication gates and complete atlas page count','status':'pass'})
    write_json(out/'checks.json',checks)
    finish_record(out,{'schema':'Nb4-rq-validation/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),
        'status':'all independent table checks passed','limitations':'No biological causality or independent maturity outcome tested; raw inputs checked by execution readers, not reread here.'})
    print(f'{len(checks)} validation groups passed, including {compared} prior-fit comparisons.')


if __name__=='__main__':main()
