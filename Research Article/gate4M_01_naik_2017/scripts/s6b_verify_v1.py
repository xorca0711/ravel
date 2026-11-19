"""Independent gzip/CSV/Decimal marker verification; no imports from the reducer."""
import argparse
import csv
from decimal import Decimal, InvalidOperation, getcontext
import gzip
import json
from pathlib import Path
import re

getcontext().prec = 50
MARKERS = [('Xist', 'ENSMUSG00000086503.3', 'chrX', 'lincRNA'),
    ('Ddx3y', 'ENSMUSG00000069045.11', 'chrY', 'protein_coding'),
    ('Eif2s3y', 'ENSMUSG00000069049.11', 'chrY', 'protein_coding'),
    ('Kdm5d', 'ENSMUSG00000056673.14', 'chrY', 'protein_coding'),
    ('Uty', 'ENSMUSG00000068457.14', 'chrY', 'protein_coding')]
SAMPLES = ['GSM2440985', 'GSM2440986', 'GSM2440987', 'GSM2440988']


def rows(path):
    with path.open(encoding='utf-8', newline='') as handle: return list(csv.DictReader(handle, delimiter='\t'))


def verify(count_paths, crosswalk_path, s2_qc_path, annotation_path, run_dir, expected_gene_count=47729, analysis_id=None):
    checks, maximum = 0, Decimal(0)
    def equal(a, b, label):
        nonlocal checks, maximum
        checks += 1
        if isinstance(b, Decimal):
            try: value = Decimal(a)
            except InvalidOperation as error: raise AssertionError((label, 'nonnumeric', a)) from error
            assert value.is_finite() and b.is_finite(), label
            err = abs(value-b)/max(Decimal(1), abs(b)); maximum = max(maximum, err)
            assert err <= Decimal('1e-10'), (label, a, b)
        else: assert a == str(b), (label, a, b)
    def table_equal(name, expected):
        actual = rows(run_dir/(name+'.tsv'))
        assert len(actual) == len(expected), name
        for i, (a, b) in enumerate(zip(actual, expected)):
            assert set(a) == set(b), (name, 'fields')
            for k, v in b.items(): equal(a[k], v, name+':'+str(i)+':'+k)
    found = []
    with gzip.open(annotation_path, 'rt', encoding='utf-8') as handle:
        for line in handle:
            if not line.strip() or line.startswith('#'): continue
            cells = line.rstrip('\n').split('\t')
            assert len(cells) == 9, 'Malformed GTF record'
            if cells[2] != 'gene': continue
            attrs = {}
            for part in cells[8].split(';'):
                if not part.strip(): continue
                key, value = part.strip().split(' ', 1)
                attrs[key] = value.strip().strip('"')
            if attrs.get('gene_name') in [m[0] for m in MARKERS] or attrs.get('gene_id') in [m[1] for m in MARKERS]:
                found.append((attrs['gene_name'], attrs['gene_id'], cells[0], attrs['gene_type']))
    assert sorted(found) == sorted(MARKERS), 'Changed/ambiguous exact M9 annotation'
    annotation = [dict(marker=n, gene_id=g, chromosome=c, gene_type=t, annotation_status='unique_exact_M9_gene') for n, g, c, t in MARKERS]
    table_equal('annotation', annotation)
    crosswalk_records, qc_records = rows(crosswalk_path), rows(s2_qc_path)
    crosswalk, prior = {r['gsm']: r for r in crosswalk_records}, {r['gsm']: r for r in qc_records}
    assert len(crosswalk) == len(crosswalk_records) and len(prior) == len(qc_records)
    sample_out, marker_out, first_order = [], [], None
    for j, gsm in enumerate(SAMPLES):
        meta, q = crosswalk[gsm], prior[gsm]
        role, condition = ('control', 'control') if j < 2 else ('exposed', 'acute_inflamed')
        assert meta['assay'] == 'RNA-seq' and meta['day_label'] == '6' and meta['wound_hour_label'] == ''
        assert meta['history_label'] == ('control' if j < 2 else 'prior_inflammation') and not meta['label_conflicts']
        assert meta['runs'] == q['run'] == 'SRR'+str(5133553+j) and meta['biosamples'] == q['biosample']
        assert meta['instrument_models'] == q['instrument'] == 'Illumina HiSeq 4000'
        assert meta['library_layouts'] == q['layout'] == 'PAIRED'
        assert q['time'] == 'D6' and q['role'] == role and q['condition'] == condition
        assert q['short_label'] == ['D6_C1', 'D6_C2', 'D6_A1', 'D6_A2'][j]
        assert meta['count_files'] == q['source_file'] == count_paths[gsm].name
        sex = re.findall(r'(?:^|\|)\s*[Ss]ex:\s*([^|]+)', meta['characteristics'])
        assert [s.strip() for s in sex] == ['female'], 'Changed recorded metadata'
        raw_counts, order = {}, []
        with gzip.open(count_paths[gsm], 'rt', encoding='utf-8', newline='') as handle:
            for cells in csv.reader(handle, delimiter='\t'):
                assert len(cells) == 2 and re.fullmatch(r'[0-9]+', cells[1]), 'Invalid integer count'
                assert cells[0] not in raw_counts, 'Duplicate gene'
                raw_counts[cells[0]] = int(cells[1]); order.append(cells[0]); checks += 1
        assert len(order) == expected_gene_count
        if first_order is None: first_order = order
        else: assert order == first_order, 'Changed gene order'
        total = sum(raw_counts.values())
        assert total == int(q['gene_count_total']) and total > 0
        sf, tf = Decimal(q['mor_size_factor']), Decimal(q['total_count_size_factor'])
        assert sf.is_finite() and sf > 0 and tf.is_finite() and tf > 0
        checks += 12
        sample_out.append(dict(gsm=gsm, short_label=q['short_label'], role=role, condition=condition,
            run=meta['runs'], biosample=meta['biosamples'], instrument=meta['instrument_models'], layout=meta['library_layouts'],
            recorded_sex='female', source_characteristics=meta['characteristics'], source_file=count_paths[gsm].name,
            gene_rows=expected_gene_count, gene_count_total=total, mor_size_factor=sf, total_count_size_factor=tf,
            normalization_origin='frozen_S2_D6_factors_not_refitted', biological_unit='RNA_library_with_unresolved_exact_pool_membership'))
        for name, gene, chromosome, gene_type in MARKERS:
            raw = raw_counts[gene]; cpm = Decimal(raw)*1000000/total
            marker_out.append(dict(marker=name, gene_id=gene, chromosome=chromosome, gene_type=gene_type,
                gsm=gsm, short_label=q['short_label'], role=role, condition=condition, recorded_sex='female', raw=raw,
                mor=Decimal(raw)/sf, total=Decimal(raw)/tf, cpm=cpm,
                log2_cpm_plus1=(cpm+1).ln()/Decimal(2).ln(), raw_zero=raw == 0))
    table_equal('sample_qc', sample_out); table_equal('marker_qc', marker_out)
    meta = json.loads((run_dir/'metadata.json').read_text(encoding='utf-8'))
    expected = dict(libraries=SAMPLES, marker_order=[m[0] for m in MARKERS], marker_rows=20,
        exact_gene_rows_per_library=expected_gene_count, recorded_sex_labels=['female']*4,
        no_sex_assignment_exclusion_or_pairing=True, no_new_marker_selection=True, frozen_factors_reused=True,
        upstream_analyses_rerun=False, population_inference=False, independent_biological_replication=False,
        threshold_or_classifier_fitted=False)
    if analysis_id: expected['analysis_id'] = analysis_id
    assert set(meta) == set(expected)
    for k, v in expected.items():
        checks += 1; assert meta[k] == v, ('metadata', k)
    return dict(status='passed', checks=checks, maximum_scaled_error=float(maximum), source_reader='stdlib gzip/CSV and separate GTF parser',
        arithmetic='50-digit Decimal including logarithm', marker_rows=20, libraries=4,
        normalization_refitted=False, independent_biological_replication=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--contract', type=Path, required=True); parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args(); root = Path(__file__).resolve().parents[3]
    c = json.loads(args.contract.read_text(encoding='utf-8-sig')); ps = {Path(x['path']).name: root/x['path'] for x in c['inputs']}
    cps = {s: next(p for n, p in ps.items() if n.startswith(s+'_') and n.endswith('.tab.gz')) for s in SAMPLES}
    result = verify(cps, ps['library_crosswalk.tsv'], ps['sample_qc.tsv'], ps['gencode.vM9.annotation.gtf.gz'], args.run_dir, analysis_id=c['analysis_id'])
    result['analysis_id'] = c['analysis_id']
    (args.run_dir/'verification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result), flush=True)
