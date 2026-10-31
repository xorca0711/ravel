"""Approved R1 tracing and B1 native-label pool descriptions only."""
import argparse
import hashlib
import json
import re
from collections import defaultdict
from decimal import Decimal

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from t1a_common_v1 import BOOK, HERE, ROOT, cell, columns, dump, fraction_candidates, literal_fields, summary, table, workbook


def check_headers(sheet, block):
    problems = []
    for measure in ['area', 'fraction']:
        for index, col in enumerate(columns(*block[measure + '_columns'])):
            address = col + str(block['header_row'])
            if cell(sheet, address)['text'] != 'M+' + str(index):
                problems.append(address + ':isotope_header_mismatch')
    for row, expected in zip(block['rows'], block['sample_labels']):
        if cell(sheet, 'A' + str(row))['text'] != expected:
            problems.append('A' + str(row) + ':sample_label_mismatch')
        if cell(sheet, block['metabolite_column'] + str(row))['text'] != block['metabolite']:
            problems.append(str(row) + ':metabolite_mismatch')
    return problems


def r1(spec, out):
    book = workbook({b['sheet'] for b in spec['blocks']})
    values, qc, units, summaries, differences = [], [], [], [], []
    for block in spec['blocks']:
        sheet = book[block['sheet']]
        issues = check_headers(sheet, block)
        observations = []
        for row in block['rows']:
            label = cell(sheet, 'A' + str(row))['text']
            prefix = label.rsplit('_', 1)[0]
            condition = block['groups'].get(prefix, 'unknown')
            f = fraction_candidates([cell(sheet, col + str(row)) for col in columns(*block['fraction_columns'])])
            observations.append({'block': block['id'], 'sheet': block['sheet'], 'source_row': row,
                                 'sample_label': label, 'native_group': prefix, 'reported_condition': condition,
                                 'fraction_sum_native': f['sum'], 'scale_candidates': '|'.join(f['candidates']),
                                 'tolerance_1': f['tolerance_1'], 'tolerance_100': f['tolerance_100'],
                                 'fraction_status': f['status']})
        candidates = {r['scale_candidates'] for r in observations if r['fraction_status'] == 'scale_candidate'}
        scale = next(iter(candidates)) if len(candidates) == 1 else ''
        header_status = 'qualified' if not issues else 'held'
        for obs in observations:
            eligible = header_status == 'qualified' and scale and obs['scale_candidates'] == scale and obs['fraction_status'] == 'scale_candidate' and obs['reported_condition'] != 'unknown'
            obs['fraction_status'] = 'qualified' if eligible else 'held:' + ('header' if issues else 'mixed_or_unknown_scale' if not scale else obs['fraction_status'])
            obs['block_scale'] = scale
            obs['unit_status'] = 'sample label only; biological independence and pairing unknown'
            qc.append(obs)
            for measure in ['area', 'fraction']:
                for index, col in enumerate(columns(*block[measure + '_columns'])):
                    address = col + str(obs['source_row'])
                    c = cell(sheet, address)
                    v = {'block': block['id'], 'sheet': block['sheet'], 'metabolite': block['metabolite'],
                         'sample_label': obs['sample_label'], 'native_group': obs['native_group'],
                         'reported_condition': obs['reported_condition'],
                         'source_group_cell': block['group_column'] + str(obs['source_row']),
                         'source_group_literal': cell(sheet, block['group_column'] + str(obs['source_row']))['text'],
                         'measure': 'corrected_peak_area' if measure == 'area' else 'reported_fraction',
                         'isotope': 'M+' + str(index), 'source_cell': address,
                         'header_cell': col + str(block['header_row']), 'source_header': cell(sheet, col + str(block['header_row']))['text'],
                         **literal_fields(c), 'header_status': header_status,
                         'fraction_status': obs['fraction_status'], 'fraction_scale': scale}
                    values.append(v)
        units.append({'block': block['id'], 'sheet': block['sheet'], 'metabolite': block['metabolite'],
                      'medium': block['medium'], 'tracer': block['tracer'], 'header_status': header_status,
                      'header_issues': '|'.join(issues), 'fraction_scale': scale,
                      'qualified_fraction_observations': sum(r['fraction_status'] == 'qualified' for r in observations),
                      'n_supplied_labels': len(observations), 'biological_independence': 'unknown',
                      'area_unit': 'natural-abundance-corrected instrument peak area; not calibrated concentration',
                      'fraction_unit': 'fraction (0-1)' if scale == '1' else 'percent (0-100)' if scale == '100' else 'held: unresolved scale'})
    grouped = defaultdict(list)
    for r in values:
        grouped[(r['block'], r['measure'], r['isotope'], r['reported_condition'])].append(r)
    for key, records in grouped.items():
        block, measure, isotope, condition = key
        s = summary(records, require_fraction=measure == 'reported_fraction')
        if any(r['header_status'] != 'qualified' or r['reported_condition'] == 'unknown' for r in records):
            s.update(status='held', mean='', minimum='', maximum='')
        summaries.append({'block': block, 'measure': measure, 'isotope': isotope,
                          'reported_condition': condition, 'source_cells': '|'.join(r['source_cell'] for r in records),
                          'source_labels': '|'.join(r['sample_label'] for r in records),
                          'fraction_scale': records[0]['fraction_scale'] if measure == 'reported_fraction' else '', **s})
    indexed = {(r['block'],r['measure'],r['isotope'],r['reported_condition']):r for r in summaries}
    for block, measure, isotope in dict.fromkeys(k[:3] for k in grouped):
        a = indexed.get((block,measure,isotope,'UT'))
        b = indexed.get((block,measure,isotope,'TGF-beta'))
        okay = a is not None and b is not None and a['status'] == b['status'] == 'qualified'
        differences.append({'block': block, 'measure': measure, 'isotope': isotope,
                            'comparison': 'TGF-beta minus UT; unpaired descriptive source means',
                            'n_UT': '' if a is None else a['n_supplied'], 'n_TGF': '' if b is None else b['n_supplied'],
                            'status': 'qualified' if okay else 'held',
                            'difference_native_units': str(Decimal(b['mean'])-Decimal(a['mean'])) if okay else '',
                            'inference_limit': 'No donor test, CI, pairing, cross-medium pooling or flux'})
    table(out/'source_values.csv', values)
    table(out/'observation_qc.csv', qc)
    table(out/'block_units.csv', units)
    table(out/'summaries.csv', summaries)
    table(out/'descriptive_differences.csv', differences)
    plot_r1(spec, values, summaries, units, out)
    dump(out/'disposition.json', {'job':'T1-R1', 'source_sha256': hashlib.sha256(BOOK.read_bytes()).hexdigest(),
                                'blocks':len(units), 'sample_metabolite_observations':len(qc), 'literal_measurements':len(values),
                                'held_fraction_observations':sum(r['fraction_status']!='qualified' for r in qc),
                                'held_summaries':sum(r['status']!='qualified' for r in summaries),
                                'invalid_values':sum(r['value_status']!='valid' for r in values),
                                'limit':'Processed source description only; no raw correction, flux, causal/source-transfer or population inference.'})


def b1(spec, out):
    book = workbook({p['sheet'] for p in spec['panels']})
    values, summaries = [], []
    for panel in spec['panels']:
        sheet = book[panel['sheet']]
        for row, metabolite in panel['rows'].items():
            for col, expected_label in panel['sample_headers'].items():
                label = cell(sheet, col+'1')['text']
                match = re.fullmatch(panel['header_regex'], label)
                prefix = match.group('group') if match else 'UNPARSED:' + label
                suffix = match.group('suffix') if match else ''
                status = 'qualified' if label == expected_label and match and cell(sheet,'A'+row)['text'] == metabolite else 'held'
                values.append({'sheet':panel['sheet'], 'metabolite':metabolite, 'source_cell':col+row,
                               'header_cell':col+'1', 'full_sample_label':label, 'native_group':prefix,
                               'suffix_label':suffix, 'header_status':status,
                               **literal_fields(cell(sheet,col+row)),
                               'unit':'uncalibrated instrument peak area',
                               'condition_key':'unresolved; prefix is not assigned to an amino-acid medium',
                               'biological_independence':'unknown; four suffixes are source observations'})
    groups = defaultdict(list)
    for r in values:
        groups[(r['sheet'],r['metabolite'],r['native_group'])].append(r)
    for (sheet,metabolite,native), records in groups.items():
        s = summary(records)
        if any(r['header_status'] != 'qualified' for r in records) or len(records) != 4 or len({r['suffix_label'] for r in records}) != 4:
            s.update(status='held',mean='',minimum='',maximum='')
        summaries.append({'sheet':sheet,'metabolite':metabolite,'native_group':native,
                          'source_cells':'|'.join(r['source_cell'] for r in records),
                          'full_sample_labels':'|'.join(r['full_sample_label'] for r in records),
                          'unit':'native uncalibrated peak area',**s})
    table(out/'source_values.csv', values)
    table(out/'summaries.csv', summaries)
    plot_b1(values, summaries, out)
    dump(out/'disposition.json',{'job':'T1-B1','source_sha256':hashlib.sha256(BOOK.read_bytes()).hexdigest(),
                               'literal_measurements':len(values),'literal_label_groups':len(summaries),
                               'held_summaries':sum(r['status']!='qualified' for r in summaries),
                               'invalid_values':sum(r['value_status']!='valid' for r in values),
                               'limit':'Native-label description only; condition key unresolved. No nutrient effect, cross-metabolite area comparison, biological test, calibrated pool or synthesis.'})


def save_figure(fig, out, stem):
    for ext in ['png','pdf']:
        path=out/(stem+'.'+ext)
        if path.exists():
            raise FileExistsError(path)
        fig.savefig(path,dpi=170,metadata={'Creator':'Ravel T1-A source description','CreationDate':None} if ext=='pdf' else None)
    plt.close(fig)


def plot_r1(spec, values, summaries, units, out):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(5,3,figsize=(12,14),layout='constrained')
    colors={'UT':'#206A96','TGF-beta':'#BE5B22'}
    for ax,block,unit in zip(axes.flat,spec['blocks'],units):
        ax.set_title(block['id']+' | '+block['metabolite']+'\n'+block['medium']+'; '+block['tracer'],loc='left',fontsize=9)
        points=[r for r in values if r['block']==block['id'] and r['measure']=='reported_fraction']
        if unit['qualified_fraction_observations'] != unit['n_supplied_labels'] or unit['fraction_scale']=='':
            ax.text(.5,.5,'Fraction display held\nSee observation QC and literal values',transform=ax.transAxes,ha='center',va='center')
            ax.set_xticks([]);ax.set_yticks([]);continue
        scale=float(unit['fraction_scale'])
        channels=list(dict.fromkeys(r['isotope'] for r in points))
        for condition,offset in [('UT',-.16),('TGF-beta',.16)]:
            for i,ch in enumerate(channels):
                recs=[r for r in points if r['reported_condition']==condition and r['isotope']==ch]
                ys=[float(r['numeric_value'])*100/scale for r in recs]
                xs=[i+offset+(j-1.5)*.035 for j in range(len(ys))]
                ax.scatter(xs,ys,s=9,color=colors[condition],alpha=.65,zorder=3)
                mean=sum(ys)/len(ys)
                ax.plot([i+offset,i+offset],[min(ys),max(ys)],color=colors[condition],lw=.8)
                ax.plot(i+offset,mean,marker='_',markersize=8,color=colors[condition])
        ax.set_xticks(range(len(channels)),channels,rotation=55,ha='right',fontsize=7)
        ax.set_ylabel('Deposited isotope (%)')
        ax.set_ylim(-3,103);ax.grid(axis='y',alpha=.15)
    handles=[plt.Line2D([],[],color=c,marker='o',ls='',label=k) for k,c in colors.items()]
    fig.legend(handles=handles,loc='outside lower center',ncol=2,frameon=False)
    fig.suptitle('Hamanaka processed isotope observations | approved R1 blocks\nFour source labels per condition; dots, mean and observed range. No donor inference or flux.',fontsize=13)
    save_figure(fig,out,'tracer_source_description')


def plot_b1(values,summaries,out):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    panels=list(dict.fromkeys((r['sheet'],r['metabolite']) for r in values))
    fig,axes=plt.subplots(2,2,figsize=(12,9),layout='constrained')
    for ax,(sheet,metabolite) in zip(axes.flat,panels):
        ss=[s for s in summaries if s['sheet']==sheet and s['metabolite']==metabolite]
        for i,s in enumerate(ss):
            rows=[r for r in values if r['sheet']==sheet and r['metabolite']==metabolite and r['native_group']==s['native_group']]
            if s['status']!='qualified':
                ax.text(i,.5,'held',transform=ax.get_xaxis_transform(),rotation=90,ha='center');continue
            ys=[float(r['numeric_value']) for r in rows]
            ax.scatter([i+(j-1.5)*.07 for j in range(len(ys))],ys,color='#276B73',s=22,alpha=.7,zorder=3)
            ax.plot([i,i],[min(ys),max(ys)],color='#173B43',lw=1)
            ax.plot(i,float(s['mean']),marker='_',markersize=14,color='#173B43')
        ax.set_xticks(range(len(ss)),[s['native_group'] for s in ss],rotation=55,ha='right')
        ax.set_title(sheet+' | '+metabolite,loc='left')
        ax.set_ylabel('Uncalibrated peak area');ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0));ax.grid(axis='y',alpha=.15)
        ax.set_ylim(bottom=0)
    fig.suptitle('Hamanaka intracellular pools | native source-label groups\nFour supplied observations per group; dots, mean and range. Prefix-to-medium key remains unresolved.',fontsize=13)
    save_figure(fig,out,'native_pool_description')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--job',choices=['r1','b1'],required=True);parser.add_argument('--output',type=__import__('pathlib').Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    spec=json.loads((HERE/f'config/t1a_{args.job}_spec_v1.json').read_text(encoding='utf-8'))
    {'r1':r1,'b1':b1}[args.job](spec,args.output)
    print(json.dumps({'job':args.job,'owner':'Wg-P06','status':'source description completed; scientific acceptance not assessed'}))


if __name__=='__main__':
    main()
