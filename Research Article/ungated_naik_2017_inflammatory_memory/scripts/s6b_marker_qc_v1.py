"""Fixed D6 source-marker QC; reuse frozen factors and never infer sex or pairing."""
import argparse
import csv
import gzip
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import time

import numpy as np
import pandas as pd

MARKERS = [
    ('Xist', 'ENSMUSG00000086503.3', 'chrX', 'lincRNA'),
    ('Ddx3y', 'ENSMUSG00000069045.11', 'chrY', 'protein_coding'),
    ('Eif2s3y', 'ENSMUSG00000069049.11', 'chrY', 'protein_coding'),
    ('Kdm5d', 'ENSMUSG00000056673.14', 'chrY', 'protein_coding'),
    ('Uty', 'ENSMUSG00000068457.14', 'chrY', 'protein_coding')]
SAMPLES = ['GSM2440985', 'GSM2440986', 'GSM2440987', 'GSM2440988']


def read_rows(path):
    with path.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t'))


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def table(path, rows):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def annotate(path):
    names = {m[0] for m in MARKERS}
    ids = {m[1] for m in MARKERS}
    selected = []
    with gzip.open(path, 'rt', encoding='utf-8') as handle:
        for line in handle:
            if not line.strip() or line.startswith('#'): continue
            fields = line.rstrip('\n').split('\t')
            if len(fields) != 9: raise ValueError('Malformed GTF record')
            if fields[2] != 'gene': continue
            attrs = dict(re.findall(r'(\w+) "([^"]*)"', fields[8]))
            if attrs.get('gene_name') in names or attrs.get('gene_id') in ids:
                selected.append((attrs['gene_name'], attrs['gene_id'], fields[0], attrs['gene_type']))
    if sorted(selected) != sorted(MARKERS):
        raise ValueError('Absent, ambiguous or changed exact M9 marker annotation')
    return [dict(marker=n, gene_id=g, chromosome=c, gene_type=t, annotation_status='unique_exact_M9_gene') for n, g, c, t in MARKERS]


def reconstruct(count_paths, crosswalk_path, s2_qc_path, annotation_path, expected_gene_count=47729):
    annotation = annotate(annotation_path)
    crosswalk_rows, prior_rows = read_rows(crosswalk_path), read_rows(s2_qc_path)
    crosswalk = {r['gsm']: r for r in crosswalk_rows}
    prior = {r['gsm']: r for r in prior_rows}
    if len(crosswalk) != len(crosswalk_rows) or len(prior) != len(prior_rows):
        raise ValueError('Duplicate source library identity')
    sample_rows, marker_rows, gene_order = [], [], None
    for j, gsm in enumerate(SAMPLES):
        meta, q = crosswalk[gsm], prior[gsm]
        role = 'control' if j < 2 else 'exposed'
        condition = 'control' if j < 2 else 'acute_inflamed'
        expected_run = 'SRR'+str(5133553+j)
        checks = [meta['assay'] == 'RNA-seq', meta['day_label'] == '6', not meta['wound_hour_label'],
            meta['history_label'] == ('control' if j < 2 else 'prior_inflammation'), not meta['label_conflicts'],
            meta['runs'] == q['run'] == expected_run, meta['biosamples'] == q['biosample'],
            meta['instrument_models'] == q['instrument'] == 'Illumina HiSeq 4000',
            meta['library_layouts'] == q['layout'] == 'PAIRED', q['time'] == 'D6',
            q['role'] == role, q['condition'] == condition,
            q['short_label'] == ['D6_C1', 'D6_C2', 'D6_A1', 'D6_A2'][j],
            meta['count_files'] == q['source_file'] == count_paths[gsm].name]
        if not all(checks): raise ValueError('Changed D6 identity or source-factor join: '+gsm)
        sex = [x.strip().split(':', 1)[1].strip() for x in meta['characteristics'].split('|') if x.strip().lower().startswith('sex:')]
        if sex != ['female']: raise ValueError('Changed or ambiguous recorded sex metadata')
        frame = pd.read_csv(count_paths[gsm], sep='\t', header=None, dtype=str, keep_default_na=False)
        if frame.shape[1] != 2 or not frame[1].str.fullmatch(r'[0-9]+').all():
            raise ValueError('Count source must contain two columns and nonnegative integer text')
        frame.columns = ['gene_id', 'count']
        frame['count'] = frame['count'].astype(np.int64)
        if len(frame) != expected_gene_count or frame['gene_id'].duplicated().any() or (frame['count'] < 0).any():
            raise ValueError('Invalid count-file structure')
        order = frame['gene_id'].tolist()
        if gene_order is not None and order != gene_order: raise ValueError('Changed versioned gene order')
        gene_order = order
        total = int(frame['count'].sum())
        if total <= 0 or total != int(q['gene_count_total']): raise ValueError('S2 count-total mismatch')
        sf, tf = float(q['mor_size_factor']), float(q['total_count_size_factor'])
        if not all(math.isfinite(v) and v > 0 for v in [sf, tf]): raise ValueError('Invalid frozen size factor')
        sample_rows.append(dict(gsm=gsm, short_label=q['short_label'], role=role, condition=condition,
            run=meta['runs'], biosample=meta['biosamples'], instrument=meta['instrument_models'], layout=meta['library_layouts'],
            recorded_sex=sex[0], source_characteristics=meta['characteristics'], source_file=count_paths[gsm].name,
            gene_rows=len(frame), gene_count_total=total, mor_size_factor=sf, total_count_size_factor=tf,
            normalization_origin='frozen_S2_D6_factors_not_refitted', biological_unit='RNA_library_with_unresolved_exact_pool_membership'))
        counts = dict(zip(frame['gene_id'], frame['count']))
        for name, gene, chromosome, gene_type in MARKERS:
            if gene not in counts: raise ValueError('Missing fixed versioned marker: '+gene)
            raw = int(counts[gene])
            cpm = raw*1e6/total
            marker_rows.append(dict(marker=name, gene_id=gene, chromosome=chromosome, gene_type=gene_type,
                gsm=gsm, short_label=q['short_label'], role=role, condition=condition, recorded_sex=sex[0],
                raw=raw, mor=raw/sf, total=raw/tf, cpm=cpm, log2_cpm_plus1=math.log2(cpm+1), raw_zero=raw == 0))
    metadata = dict(libraries=SAMPLES, marker_order=[m[0] for m in MARKERS], marker_rows=len(marker_rows),
        exact_gene_rows_per_library=expected_gene_count, recorded_sex_labels=['female']*4,
        no_sex_assignment_exclusion_or_pairing=True, no_new_marker_selection=True,
        frozen_factors_reused=True, upstream_analyses_rerun=False, population_inference=False,
        independent_biological_replication=False, threshold_or_classifier_fitted=False)
    return dict(annotation=annotation, sample_qc=sample_rows, marker_qc=marker_rows, metadata=metadata)


def write_outputs(output, data):
    for name in ['annotation', 'sample_qc', 'marker_qc']: table(output/(name+'.tsv'), data[name])
    save_json(output/'metadata.json', data['metadata'])


def plot(output, data):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'pdf.fonttype': 42})
    rows = {(r['gene_id'], r['gsm']): r for r in data['marker_qc']}
    raw = [[rows[g, s]['raw'] for s in SAMPLES] for _, g, _, _ in MARKERS]
    log = np.array([[rows[g, s]['log2_cpm_plus1'] for s in SAMPLES] for _, g, _, _ in MARKERS])
    labels = [r['short_label'] for r in data['sample_qc']]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), layout='constrained', gridspec_kw={'width_ratios': [1, 1.1]})
    fig.suptitle('Fixed five-marker RNA profiles in four D6 libraries\nRecorded metadata: female for all; RNA profiles do not assign sex or sample matching', fontsize=14)
    axes[0].axis('off')
    tbl = axes[0].table(cellText=[[str(v) for v in row] for row in raw], rowLabels=[m[0] for m in MARKERS],
        colLabels=labels, cellLoc='center', loc='center', bbox=[.1, .05, .9, .85])
    tbl.auto_set_font_size(False); tbl.set_fontsize(10)
    for (i, j), cell in tbl.get_celld().items():
        cell.set_edgecolor('#dddddd')
        if i == 0: cell.set_facecolor('#edf1f3')
    axes[0].set_title('Exact supplied read counts')
    vmax = max(1., float(log.max()))
    im = axes[1].imshow(log, cmap='viridis', vmin=0, vmax=vmax, aspect='auto')
    axes[1].set(xticks=range(4), xticklabels=labels, yticks=range(5), yticklabels=[m[0] for m in MARKERS],
        title='log₂(CPM + 1); one shared scale, no row scaling')
    for i in range(5):
        for j in range(4): axes[1].text(j, i, f'{log[i,j]:.2f}', ha='center', va='center', color='black' if log[i,j] > .55*vmax else 'white')
    fig.colorbar(im, ax=axes[1], label='log₂(CPM + 1)', fraction=.05, pad=.03)
    for ax in axes:
        for spine in ax.spines.values(): spine.set_visible(False)
    fig.savefig(output/'fig01_fixed_d6_markers.png', dpi=230, bbox_inches='tight')
    fig.savefig(output/'fig01_fixed_d6_markers.pdf', bbox_inches='tight', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def run(contract_path, output):
    start = time.monotonic()
    root = Path(__file__).resolve().parents[3]
    c = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    paths = {Path(x['path']).name: root/x['path'] for x in c['inputs']}
    count_paths = {s: next(p for n, p in paths.items() if n.startswith(s+'_') and n.endswith('.tab.gz')) for s in SAMPLES}
    data = reconstruct(count_paths, paths['library_crosswalk.tsv'], paths['sample_qc.tsv'], paths['gencode.vM9.annotation.gtf.gz'])
    data['metadata']['analysis_id'] = c['analysis_id']
    write_outputs(output, data); plot(output, data)
    import matplotlib
    save_json(output/'runtime.json', dict(python=sys.version, pandas=pd.__version__, numpy=np.__version__, matplotlib=matplotlib.__version__,
        elapsed_seconds_before_verification=time.monotonic()-start, upstream_analyses_rerun=False))
    subprocess.run([sys.executable, str(Path(__file__).with_name('s6b_verify_v1.py')), '--contract', str(contract_path.resolve()),
        '--run-dir', str(output.resolve())], check=True)
    print(json.dumps(dict(status='completed_fixed_D6_marker_QC', elapsed_seconds=time.monotonic()-start)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); run(args.contract, args.output)
