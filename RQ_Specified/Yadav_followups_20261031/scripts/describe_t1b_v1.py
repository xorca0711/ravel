"""Reviewed literal-channel descriptions; vector diagnostics never gate valid channels."""
import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from decimal import Decimal

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from t1a_common_v1 import (BOOK, HERE, ROOT, cell, closure_tolerance, columns,
                           dump, literal_fields, table, workbook)

PERCENT = 'reported_channel_percent'
AREA = 'reported_area'
V1_QC = ROOT/'analysis/research/runs/Wg_P06_followup_t1a_r1_v1/observation_qc.csv'


def parse_channel(c, measure):
    result = literal_fields(c)
    if measure == PERCENT and result['value_status'] == 'valid' and Decimal(result['numeric_value']) > 100:
        result['value_status'] = 'outside_declared_percent_domain'
    return result


def channel_summary(records, expected_n):
    valid = [r for r in records if r['value_status'] == 'valid']
    okay = (len(records) == expected_n and len(valid) == expected_n
            and len({r['sample_label'] for r in records}) == expected_n
            and all(r['header_status'] == 'qualified' for r in records))
    out = {'n_expected': expected_n, 'n_supplied': len(records), 'n_valid': len(valid),
           'status': 'qualified' if okay else 'held', 'mean': '', 'minimum': '', 'maximum': ''}
    if okay:
        values = [Decimal(r['numeric_value']) for r in records]
        out.update(mean=str(sum(values)/len(values)), minimum=str(min(values)), maximum=str(max(values)))
    return out


def vector_diagnostic(cells):
    parsed = [parse_channel(c, PERCENT) for c in cells]
    valid = [Decimal(r['numeric_value']) for r in parsed if r['value_status'] == 'valid']
    complete = len(valid) == len(cells) and bool(cells)
    total = sum(valid, Decimal(0))
    tolerance = closure_tolerance([c['raw'] for c in cells], 100)
    return {'n_channels_expected': len(cells), 'n_valid_percent_channels': len(valid),
            'completeness': 'complete_supplied_valid_channels' if complete else 'incomplete_missing_or_invalid_channels',
            'partial_valid_channel_subtotal_percent': str(total) if valid and not complete else '',
            'complete_sum_reported_percent': str(total) if complete else '',
            'residual_from_100_percentage_points': str(total-100) if complete else '',
            'fixed_tolerance_at_100': str(tolerance),
            'closure_diagnostic': ('complete:closes_at_fixed_tolerance' if abs(total-100) <= tolerance
                                   else 'complete:does_not_close_at_fixed_tolerance') if complete else 'incomplete:not_tested',
            'normalization_validation': 'not_established; diagnostic only; no rescaling or renormalization'}


def header_issues(sheet, block):
    issues = []
    for m in block['measures']:
        if cell(sheet, m['unit_cell'])['text'] != m['unit_literal']:
            issues.append(m['unit_cell']+':unit_literal_mismatch')
        for address, literal in m['isotope_headers'].items():
            if cell(sheet, address)['text'] != literal:
                issues.append(address+':isotope_header_mismatch')
    for obs in block['observations']:
        if cell(sheet, 'A'+str(obs['row']))['text'] != obs['sample_label']:
            issues.append('A'+str(obs['row'])+':sample_label_mismatch')
        if cell(sheet, block['metabolite_column']+str(obs['row']))['text'] != block['metabolite']:
            issues.append(str(obs['row'])+':metabolite_literal_mismatch')
    return issues


def run(spec, out):
    book = workbook({b['sheet'] for b in spec['blocks']})
    old_qc = {}
    if spec['job'] == 'r1':
        with V1_QC.open(encoding='utf-8', newline='') as f:
            old_qc = {(r['block'], int(r['source_row'])): r for r in csv.DictReader(f)}
    values, units, vectors = [], [], []
    for b in spec['blocks']:
        sh = book[b['sheet']]
        issues = header_issues(sh, b)
        status = 'held' if issues else 'qualified'
        for m in b['measures']:
            cols = columns(*m['columns'])
            units.append({'block': b['id'], 'sheet': b['sheet'], 'metabolite': b['metabolite'],
                          'measure': m['name'], 'unit_cell': m['unit_cell'],
                          'expected_unit_literal': m['unit_literal'], 'observed_unit_literal': cell(sh,m['unit_cell'])['text'],
                          'header_status': status, 'issues': '|'.join(issues),
                          'isotope_headers_json': json.dumps(m['isotope_headers'], sort_keys=True),
                          'sample_map_json': json.dumps(b['observations'], sort_keys=True),
                          'n_per_condition': b['n_per_condition'],
                          'interpretation': 'source-reported percentage; not validated composition' if m['name']==PERCENT else 'native instrument peak area; not calibrated concentration'})
            for obs in b['observations']:
                row = obs['row']
                if m['name'] == PERCENT:
                    vectors.append({'block': b['id'], 'sheet': b['sheet'], 'source_row': row,
                                    'sample_label': cell(sh,'A'+str(row))['text'],
                                    'reported_condition': obs['condition'], 'header_status': status,
                                    **vector_diagnostic([cell(sh,col+str(row)) for col in cols]),
                                    'unchanged_v1_diagnostic_json': json.dumps(old_qc[(b['id'],row)], sort_keys=True) if old_qc else '',
                                    'v1_reference': V1_QC.relative_to(ROOT).as_posix() if old_qc else ''})
                for col in cols:
                    address = col+str(row)
                    header = col+str(b['header_row'])
                    values.append({'block': b['id'], 'sheet': b['sheet'], 'metabolite': b['metabolite'],
                                   'source_row': row, 'source_cell': address,
                                   'sample_cell': 'A'+str(row), 'sample_label': cell(sh,'A'+str(row))['text'],
                                   'expected_sample_label': obs['sample_label'], 'reported_condition': obs['condition'],
                                   'source_group_cell': b['group_column']+str(row) if b['group_column'] else '',
                                   'source_group_literal': cell(sh,b['group_column']+str(row))['text'] if b['group_column'] else '',
                                   'measure': m['name'], 'isotope': m['isotope_headers'][header],
                                   'header_cell': header, 'observed_isotope_header': cell(sh,header)['text'],
                                   'unit_cell': m['unit_cell'], 'source_unit_literal': cell(sh,m['unit_cell'])['text'],
                                   'header_status': status, **parse_channel(cell(sh,address),m['name']),
                                   'endpoint_limit': 'literal channel only; completeness/normalization assessed separately' if m['name']==PERCENT else 'native area only; no cross-metabolite scale comparison'})
    groups = defaultdict(list)
    for r in values:
        groups[(r['block'],r['measure'],r['isotope'],r['reported_condition'])].append(r)
    blocks = {b['id']:b for b in spec['blocks']}
    summaries = []
    for key, records in groups.items():
        block, measure, isotope, condition = key
        summaries.append({'block':block, 'sheet':records[0]['sheet'], 'metabolite':records[0]['metabolite'],
                          'measure':measure,'isotope':isotope,'reported_condition':condition,
                          'source_cells':'|'.join(r['source_cell'] for r in records),
                          'sample_labels':'|'.join(r['sample_label'] for r in records),
                          'unit_literal':records[0]['source_unit_literal'],
                          **channel_summary(records,blocks[block]['n_per_condition'])})
    index = {(r['block'],r['measure'],r['isotope'],r['reported_condition']):r for r in summaries}
    differences = []
    for block,measure,isotope in dict.fromkeys(k[:3] for k in groups):
        a,b = index[(block,measure,isotope,'UT')],index[(block,measure,isotope,'TGF-beta')]
        okay = a['status']==b['status']=='qualified'
        differences.append({'block':block,'measure':measure,'isotope':isotope,
                            'comparison':'TGF-beta minus UT; descriptive source means; no pairing',
                            'n_UT':a['n_supplied'],'n_TGF':b['n_supplied'],
                            'status':'qualified' if okay else 'held',
                            'difference_native_units':str(Decimal(b['mean'])-Decimal(a['mean'])) if okay else '',
                            'difference_unit':'percentage points' if measure==PERCENT else a['unit_literal'],
                            'inference_limit':'No donor inference, test, CI, pooled effect, flux or causal interpretation'})
    for name,rows in [('source_values',values),('unit_and_header_map',units),('vector_qc',vectors),
                      ('summaries',summaries),('descriptive_differences',differences)]:
        table(out/(name+'.csv'),rows)
    plot(spec, values, summaries, vectors, PERCENT, out)
    if spec['job']=='r2':
        plot(spec, values, summaries, vectors, AREA, out)
    dump(out/'disposition.json',{'job':spec['job'],'endpoint':'literal reported channels; not validated normalized composition',
                               'source_sha256':hashlib.sha256(BOOK.read_bytes()).hexdigest(),
                               'literal_cells':len(values),'measure_blocks':len(units),'summaries':len(summaries),
                               'held_summaries':sum(s['status']!='qualified' for s in summaries),
                               'invalid_cells':sum(s['value_status']!='valid' for s in values),
                               'vector_qc_observations':len(vectors),
                               'complete_vectors':sum(v['completeness']=='complete_supplied_valid_channels' for v in vectors),
                               'scope_holds':spec['scope_holds'],
                               'old_v1_qc_sha256':hashlib.sha256(V1_QC.read_bytes()).hexdigest() if old_qc else '',
                               'limit':'No old hold erased, normalization validation, calibrated pool, raw correction, flux, source ARG1 effect, collagen incorporation or mature repair.'})


def plot(spec, values, summaries, vectors, measure, out):
    blocks=spec['blocks']; nrows=math.ceil(len(blocks)/3)
    fig,axes=plt.subplots(nrows,3,figsize=(15,3.3*nrows),squeeze=False)
    colors={'UT':'#216b91','TGF-beta':'#b95320'}
    sv={(s['block'],s['isotope'],s['reported_condition']):s for s in summaries if s['measure']==measure}
    grouped=defaultdict(list)
    for r in values:
        if r['measure']==measure:grouped[(r['block'],r['isotope'],r['reported_condition'])].append(r)
    for ax,b in zip(axes.flat,blocks):
        metas=[m for m in b['measures'] if m['name']==measure]
        title=b['id']+' | '+b['metabolite']
        if not metas:
            ax.text(.5,.5,'Fraction map held\nDuplicated source isotope headers',ha='center',va='center',transform=ax.transAxes)
            ax.set_title(title,loc='left',fontsize=10);ax.set_axis_off();continue
        m=metas[0];isotopes=list(m['isotope_headers'].values())
        q=[v for v in vectors if v['block']==b['id']]
        if measure==PERCENT:
            complete=sum(v['completeness']=='complete_supplied_valid_channels' for v in q)
            title+=f'\nComplete supplied vectors {complete}/{len(q)}; normalization not validated'
        else:title+='\n'+m['unit_literal']
        ax.set_title(title,loc='left',fontsize=9)
        held=0
        for i,iso in enumerate(isotopes):
            for condition,offset in [('UT',-.16),('TGF-beta',.16)]:
                s=sv[(b['id'],iso,condition)];rr=grouped[(b['id'],iso,condition)]
                vals=[float(r['numeric_value']) for r in rr if r['value_status']=='valid' and r['header_status']=='qualified']
                if vals:
                    xs=[i+offset+(j-(len(vals)-1)/2)*.035 for j in range(len(vals))]
                    ax.scatter(xs,vals,s=12,alpha=.7,color=colors[condition],zorder=3)
                if s['status']=='qualified':
                    ax.vlines(i+offset,float(s['minimum']),float(s['maximum']),color=colors[condition],lw=1)
                    ax.hlines(float(s['mean']),i+offset-.09,i+offset+.09,color=colors[condition],lw=1.6)
                else:
                    held+=1
                    ax.text(i+offset,.025,'×',color=colors[condition],ha='center',transform=ax.get_xaxis_transform(),fontsize=10)
        ax.set_xticks(range(len(isotopes)),isotopes,rotation=55,ha='right',fontsize=7)
        ax.text(.98,.96,f'Held channel summaries: {held}',ha='right',va='top',transform=ax.transAxes,fontsize=7)
        ax.set_ylabel('Source-reported channel (%)' if measure==PERCENT else 'Native uncalibrated peak area',fontsize=8)
        if measure==PERCENT:ax.set_ylim(-3,108)
        ax.grid(axis='y',alpha=.14);ax.spines[['top','right']].set_visible(False)
        ax.tick_params(axis='y',labelsize=8)
    for ax in list(axes.flat)[len(blocks):]:ax.set_axis_off()
    title='Hamanaka | '+('R1 reported-channel companion' if spec['job']=='r1' else 'R2 '+('reported percentages' if measure==PERCENT else 'native peak areas'))
    subtitle='Unstacked supplied dots; means/ranges only at full supplied n. × = held summary, not zero. No biological inference.'
    if spec['job']=='r2':subtitle+=' 4F: three supplied labels/condition.'
    fig.suptitle(title+'\n'+subtitle,fontsize=12,y=.997)
    handles=[plt.Line2D([],[],marker='o',ls='',color=c,label=l) for l,c in colors.items()]
    fig.legend(handles=handles,loc='lower center',ncol=2,frameon=False,fontsize=9)
    fig.tight_layout(rect=(0,.025,1,.965))
    stem='reported_percent_channels' if measure==PERCENT else 'native_area_channels'
    fig.savefig(out/(stem+'.png'),dpi=170)
    fig.savefig(out/(stem+'.pdf'))
    plt.close(fig)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--job',choices=['r1','r2'],required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();spec=json.loads((HERE/f'config/t1b_{args.job}_spec_v1.json').read_text())
    out=ROOT/args.output;out.mkdir(parents=True,exist_ok=True)
    run(spec,out)
    print(json.dumps({'ok':True,'job':args.job,'limit':'literal channel description only; old holds unchanged'}))
