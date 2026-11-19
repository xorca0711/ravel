"""Finite source-cell reconstruction; no source fits or population inference."""
import argparse
from collections import defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys
import time

import openpyxl


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n', encoding='utf-8')


def render(value):
    if value is None: return 'NA'
    if isinstance(value, bool): return str(value)
    if isinstance(value, float): return format(value, '.17g')
    return str(value)


def table(path, records, fields=None):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer=csv.DictWriter(handle, fieldnames=fields or list(records[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        for row in records: writer.writerow({k:render(v) for k,v in row.items()})


def number(value):
    if isinstance(value, bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
        raise ValueError('Non-numeric or nonfinite source outcome: '+str(value))
    return float(value)


def requested(mapping):
    wanted=defaultdict(set)
    for e in mapping['endpoints']:
        key=e['workbook'],e['sheet']
        wanted[key].update(x['cell'] for x in e['header_guards'])
        for g in e['groups']:
            wanted[key].add(g['label_cell'])
            wanted[key].update(g['cells'] if e['kind']=='records' else [g['mean_cell'],g['se_cell'],g['n_cell']])
    return wanted


def read_workbooks(mapping, paths):
    wanted=requested(mapping); cache={}
    for book,path in paths.items():
        wb=openpyxl.load_workbook(path,read_only=True,data_only=False)
        try:
            for (b,sheet),addresses in wanted.items():
                if b!=book: continue
                coords=[openpyxl.utils.cell.coordinate_to_tuple(c) for c in addresses]
                # Finish the tiny bounded XML stream before semantic checks can raise.
                grid=list(wb[sheet].iter_rows(max_row=max(r for r,c in coords),max_col=max(c for r,c in coords)))
                for row in grid:
                    for cell in row:
                        address=getattr(cell,'coordinate',None)
                        if address in addresses:
                            if cell.data_type=='f': raise ValueError('Formula in requested source cell')
                            cache[b,sheet,address]=cell.value
                for address in addresses: cache.setdefault((b,sheet,address),None)
        finally:
            wb.close()
    return cache


def reconstruct(mapping, cache):
    endpoints={e['id']:e for e in mapping['endpoints']}
    assert len(endpoints)==len(mapping['endpoints'])
    roles=defaultdict(set); observations=[]; groups=[]; vectors={}; by_group={}
    def cell(e,address,role):
        key=e['workbook'],e['sheet'],address;roles[key].add(role)
        return cache[key]
    for e in mapping['endpoints']:
        assert len({g['id'] for g in e['groups']})==len(e['groups'])
        for guard in e['header_guards']:
            if cell(e,guard['cell'],'header')!=guard['value']: raise ValueError('Changed header: '+e['id']+':'+guard['cell'])
        for g in e['groups']:
            if cell(e,g['label_cell'],'group_label')!=g['source_label']:raise ValueError('Changed group label')
            common=dict(endpoint=e['id'],group=g['id'],label=g['label'],source_label=g['source_label'],kind=e['kind'],unit=e['unit'],time=e['time'],
                        normalization_reference=g['normalization_reference'],caption_n=e['caption_n'],caption_n_relation=e['caption_n_relation'])
            if e['kind']=='records':
                values=[]
                for address in g['cells']:
                    v=cell(e,address,'observation');missing=v is None
                    if not missing:values.append((address,number(v)))
                    observations.append(dict(endpoint=e['id'],group=g['id'],workbook=e['workbook'],sheet=e['sheet'],cell=address,
                        value=None if missing else number(v),missing=missing,record_kind='normalization_reference' if g['normalization_reference'] else 'source_observation'))
                n=len(values)
                if n!=g['expected_n'] or n==0:raise ValueError('Unexpected source N: '+e['id']+':'+g['id'])
                vs=[v for address,v in values]
                if g['normalization_reference'] and not all(v==1 for v in vs):raise ValueError('Changed normalization reference')
                stats=dict(source_n=n,source_n_meaning='source_records',mean=statistics.mean(vs),median=statistics.median(vs),
                    source_min=min(vs),source_max=max(vs),sample_sd=statistics.stdev(vs) if n>1 and not g['normalization_reference'] else None,
                    reported_se=None,dispersion_scope='normalization_reference_no_empirical_variance' if g['normalization_reference'] else ('finite_source_values' if n>1 else 'singleton_no_sd'),
                    source_cells=';'.join(g['cells']),se_source_label='NA')
                vectors[e['id'],g['id']]=values
            elif e['kind']=='reported_summary':
                mean=number(cell(e,g['mean_cell'],'reported_mean'));se=number(cell(e,g['se_cell'],'reported_se'));n=number(cell(e,g['n_cell'],'reported_n'))
                if n!=int(n) or n<1 or int(n)!=g['expected_n'] or se<0:raise ValueError('Invalid reported Mean/SE/N')
                stats=dict(source_n=int(n),source_n_meaning='reported_fitted_rate_N',mean=mean,median=None,source_min=None,source_max=None,sample_sd=None,
                    reported_se=se,dispersion_scope='reported_SE_only',source_cells=';'.join([g['mean_cell'],g['se_cell'],g['n_cell']]),se_source_label=g['se_source_label'])
            else:raise ValueError('Unknown endpoint kind')
            if e['caption_n_relation']=='context_only':comparison='not_comparable_daily_records'
            elif e['caption_n_relation']=='at_least':comparison='meets_caption_minimum' if stats['source_n']>=e['caption_n'] else 'source_caption_N_discrepancy'
            elif e['caption_n_relation']=='equal':comparison='matches_caption_number' if stats['source_n']==e['caption_n'] else 'source_caption_N_discrepancy'
            else:raise ValueError('Unknown caption N relationship')
            row={**common,**stats,'caption_n_comparison':comparison}
            groups.append(row);by_group[e['id'],g['id']]=row
    contrasts=[];deletions=[]
    for c in mapping['contrasts']:
        e=endpoints[c['endpoint']];coeff=c['coefficients'];eid=e['id']
        assert set(coeff)<=set(g['id'] for g in e['groups']) and sum(coeff.values())==0
        def effect(means):return math.fsum(coeff[g]*means[g] for g in coeff)
        means={g:by_group[eid,g]['mean'] for g in coeff};full=effect(means)
        selected=[]
        if c['leave_one_source_record_out']:
            assert e['kind']=='records' and not c['delete_normalization_references']
            for gid in coeff:
                if by_group[eid,gid]['normalization_reference']:continue
                values=vectors[eid,gid]
                if len(values)<2:continue
                for i,(address,value) in enumerate(values):
                    updated=dict(means);updated[gid]=statistics.mean(v for j,(a,v) in enumerate(values) if j!=i)
                    estimate=effect(updated);selected.append(estimate)
                    deletions.append(dict(contrast=c['id'],endpoint=eid,removed_group=gid,removed_cell=address,removed_value=value,
                        remaining_group_n=len(values)-1,mean_contrast=estimate,change_from_full=estimate-full,scope='source_record_deletion_not_CI'))
        median=effect({g:by_group[eid,g]['median'] for g in coeff}) if e['kind']=='records' else None
        contrasts.append(dict(contrast=c['id'],endpoint=eid,label=c['label'],kind=e['kind'],unit=e['unit'],coefficients=json.dumps(coeff,sort_keys=True,separators=(',',':')),
            mean_contrast=full,median_contrast=median,source_ns=json.dumps({g:by_group[eid,g]['source_n'] for g in coeff},sort_keys=True,separators=(',',':')),
            deletion_count=len(selected),deletion_min=min(selected) if selected else None,deletion_max=max(selected) if selected else None,
            deletion_scope='source_record_deletion_not_CI' if selected else ('summary_only_no_individual_records' if e['kind']=='reported_summary' else 'no_eligible_nonreference_deletion')))
    source=[]
    for key in sorted(roles,key=lambda k:(int(k[0]),k[1],k[2])):
        v=cache[key];kind='blank' if v is None else ('text' if isinstance(v,str) else 'number')
        source.append(dict(workbook=key[0],sheet=key[1],cell=key[2],kind=kind,value=v,roles='|'.join(sorted(roles[key]))))
    metadata=dict(endpoint_count=len(endpoints),group_count=len(groups),contrast_count=len(contrasts),source_cell_count=len(source),
        observation_slots=len(observations),nonmissing_source_records=sum(not x['missing'] for x in observations),missing_source_slots=sum(x['missing'] for x in observations),
        deletion_rows=len(deletions),normalized_reference_groups=[{'endpoint':x['endpoint'],'group':x['group']} for x in groups if x['normalization_reference']],
        caption_n_discrepancies=[{'endpoint':x['endpoint'],'group':x['group'],'source_n':x['source_n'],'caption_n':x['caption_n']} for x in groups if x['caption_n_comparison']=='source_caption_N_discrepancy'],
        independent_biological_replication=False,population_inference=False,source_fits_rerun=False)
    return dict(source_cells=source,observations=observations,groups=groups,contrasts=contrasts,deletion_diagnostics=deletions,metadata=metadata)


DELETION_FIELDS=['contrast','endpoint','removed_group','removed_cell','removed_value','remaining_group_n','mean_contrast','change_from_full','scope']


def write_outputs(output,data):
    for name in ['source_cells','observations','groups','contrasts','deletion_diagnostics']:
        table(output/(name+'.tsv'),data[name],DELETION_FIELDS if name=='deletion_diagnostics' else None)
    save(output/'metadata.json',data['metadata'])


def run(contract_path,output):
    started=time.monotonic();root=Path(__file__).resolve().parents[3]
    contract=json.loads(contract_path.read_text(encoding='utf-8-sig'))
    map_path=next(root/x['path'] for x in contract['inputs'] if x['path'].endswith('/S5F_SOURCE_MAP_V1.json'))
    mapping=json.loads(map_path.read_text(encoding='utf-8'))
    pdf_lines=(root/mapping['caption_source']['path']).read_text(encoding='utf-8').splitlines()
    for guard in mapping['pdf_axis_guards']:
        assert pdf_lines[guard['line']-1]==guard['value'], 'Changed rate-unit source axis'
    paths={k:root/v['path'] for k,v in mapping['source_files'].items()}
    for k,path in paths.items():assert hashlib.sha256(path.read_bytes()).hexdigest()==mapping['source_files'][k]['sha256']
    data=reconstruct(mapping,read_workbooks(mapping,paths))
    assert [data['metadata'][k] for k in ['endpoint_count','group_count','contrast_count']]==[35,83,38]
    data['metadata']['analysis_id']=contract['analysis_id'];data['metadata']['source_files']=mapping['source_files'];write_outputs(output,data)
    from s5f_plot_v1 import plot
    plot(output,mapping,data)
    import matplotlib
    save(output/'runtime.json',dict(python=sys.version,openpyxl=openpyxl.__version__,matplotlib=matplotlib.__version__,
        elapsed_seconds_before_verification=time.monotonic()-started,source_biological_analyses_rerun=False,stochastic_steps='none'))
    subprocess.run([sys.executable,str(Path(__file__).with_name('s5f_verify_v1.py')),'--contract',str(contract_path.resolve()),'--run-dir',str(output.resolve())],check=True)
    print(json.dumps({'analysis_id':contract['analysis_id'],'status':'completed_finite_source_reconstruction','elapsed_seconds':time.monotonic()-started,
        'endpoints':len(mapping['endpoints']),'groups':len(data['groups']),'contrasts':len(data['contrasts'])}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--contract',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();run(args.contract,args.output)
