"""E1 technical qualification; no biological contrast or effect columns read."""
import argparse
import csv
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path('raw_data/DY1_P02_reference_source_v1')
RNA = 'GSE247223_countMatrixUpdated.tsv.gz'
ATAC = 'GSE248042_Chinenov_Deochand_submission_ATACseq_peak_count_matrix.csv.gz'
ANNOT = 'GSE248042_Chinenov_Deochand_submission_ATACseq_differential_peak_analysis_.csv.gz'
ANNOT_COLS = ['peak_id', 'Chr', 'Start', 'End', 'Length', 'gene_name', 'ensemble_id', 'nearest_tss', 'dist_to_tss', 'nearest_tss_gene_id', 'nearest_tss_symbol']


def parse_soft(text):
    samples = {}; series = defaultdict(list); current = None
    for line in text.splitlines():
        if line.startswith('^SAMPLE = '):
            current = line.split(' = ', 1)[1]; samples[current] = defaultdict(list)
        elif line.startswith('!Sample_') and ' = ' in line and current:
            key, value = line.split(' = ', 1); samples[current][key[8:]].append(value)
        elif line.startswith('!Series_') and ' = ' in line:
            key, value = line.split(' = ', 1); series[key[8:]].append(value)
    return dict(series), {k: dict(v) for k, v in samples.items()}


def condition(value):
    compact = re.sub(r'[^a-z0-9]', '', value.lower())
    for key, target in [('corticosterone', 'CORT'), ('dexamethasone', 'DEX'), ('il4', 'IL4'), ('vehicle', 'CTRL')]:
        if key in compact: return target
    raise ValueError('Unrecognized source condition: ' + value)


def source_rows(study, samples):
    rows = []
    for gsm, sample in samples.items():
        attrs = dict(x.split(': ', 1) for x in sample['characteristics_ch1'])
        genotype = 'WT' if 'GRIP1wt/wt' in attrs['genotype'] else 'KO' if 'GRIP1fl/fl' in attrs['genotype'] else None
        if genotype is None: raise ValueError('Unrecognized source genotype')
        title = sample['title'][0]; rep = int(re.search(r'rep\s*(\d+)', title, re.I).group(1))
        treatment = condition(attrs['treatment'])
        column = f'{genotype}_{treatment}_rep{rep}' if study == 'GSE247223' else f'{genotype}_{"C" if treatment == "CTRL" else treatment}_Rep{rep}'
        biosample = next(re.search(r'SAMN\d+', value).group() for value in sample['relation'] if value.startswith('BioSample:'))
        rows.append(dict(study=study, gsm=gsm, matrix_column=column, genotype=genotype, condition=treatment, source_rep_label=rep,
            title=title, source_treatment=attrs['treatment'], source_genotype=attrs['genotype'], biosample=biosample,
            unit_evidence='published biological replicate; exact across-condition preparation reuse unknown',
            within_assay_condition_pairing='unknown', cross_assay_pairing='unknown', batch='not specified',
            timing_conflict=bool('24h' in title.replace(' ', '').lower() and '25 hours' in attrs['treatment'])))
    if len({r['matrix_column'] for r in rows}) != len(rows): raise ValueError('Duplicate sample-to-column keys')
    return rows


def audit_counts(frame, columns, assay):
    values = frame[columns].to_numpy()
    if not np.issubdtype(values.dtype, np.number) or not np.isfinite(values).all(): raise ValueError('Non-numeric/missing counts')
    if (values < 0).any() or not (values == np.floor(values)).all(): raise ValueError('Invalid count value')
    counts = values.astype(np.int64)
    rows = [dict(assay=assay, column=c, feature_rows=len(frame), count_sum=int(counts[:, i].sum()), zero_rows=int((counts[:, i] == 0).sum())) for i, c in enumerate(columns)]
    return rows, int((counts.sum(axis=1) == 0).sum())


def streaming_verify(path, delimiter, columns, expected):
    totals = {c: 0 for c in columns}; zeros = {c: 0 for c in columns}; n = 0
    with gzip.open(path, 'rt', newline='', encoding='utf-8') as handle:
        for row in csv.DictReader(handle, delimiter=delimiter):
            n += 1
            for col in columns:
                value = int(row[col]); totals[col] += value; zeros[col] += value == 0
    checks = []
    for row in expected:
        col = row['column']
        checks.extend([n == row['feature_rows'], totals[col] == row['count_sum'], zeros[col] == row['zero_rows']])
    return checks


def title_verify(rows):
    checks = []
    for r in rows:
        title = r['title'].lower()
        genotype = 'WT' if title.startswith(('bl6', 'wild type')) else 'KO' if ('grip1' in title and ('ko' in title or 'fl/fl' in title)) else None
        checks.extend([genotype == r['genotype'], condition(title) == r['condition']])
    return checks


def write_tsv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t'); w.writeheader(); w.writerows(rows)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True); args = parser.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    series, samples = {}, []
    for study in ['GSE247223', 'GSE248042']:
        with gzip.open(RAW / (study + '_family.soft.gz'), 'rt', encoding='utf-8') as f: metadata, entries = parse_soft(f.read())
        series[study] = metadata; samples.extend(source_rows(study, entries))
    rna = pd.read_csv(RAW / RNA, sep='\t', keep_default_na=False)
    atac = pd.read_csv(RAW / ATAC, keep_default_na=False)
    rna_cols = list(rna.columns[2:]); atac_cols = list(atac.columns[7:])
    assert set(rna_cols) == {r['matrix_column'] for r in samples if r['study'] == 'GSE247223'}
    assert set(atac_cols) == {r['matrix_column'] for r in samples if r['study'] == 'GSE248042'}
    assert rna['ensembl_id'].is_unique and atac['peak_id'].is_unique
    assert rna['ensembl_id'].str.fullmatch(r'ENSMUSG\d+(\.\d+)?').all()
    assert (atac['End'] >= atac['Start']).all() and (atac['Start'] >= 0).all()
    rna_qc, rna_zero = audit_counts(rna, rna_cols, 'RNA'); atac_qc, atac_zero = audit_counts(atac, atac_cols, 'ATAC')
    expected_ids = atac['Chr'] + ':' + atac['Start'].astype(str) + '-' + atac['End'].astype(str)
    assert (expected_ids == atac['peak_id']).all()
    annotation = pd.read_csv(RAW / ANNOT, usecols=ANNOT_COLS, keep_default_na=False)
    assert annotation['peak_id'].is_unique
    joined = annotation.merge(atac[['peak_id', 'Chr', 'Start', 'End', 'Length']], on='peak_id', how='left', suffixes=('_annotation', '_count'), validate='one_to_one', indicator=True)
    in_counts = joined['_merge'] == 'both'
    coordinate_match = {c: bool((joined.loc[in_counts, c + '_annotation'] == joined.loc[in_counts, c + '_count']).all()) for c in ['Chr', 'Start', 'End', 'Length']}
    mapping = annotation[['peak_id', 'gene_name', 'ensemble_id', 'nearest_tss', 'dist_to_tss', 'nearest_tss_gene_id', 'nearest_tss_symbol']].copy()
    mapping['in_count_matrix'] = mapping['peak_id'].isin(atac['peak_id'])
    mapping['ensembl_in_rna'] = mapping['ensemble_id'].isin(rna['ensembl_id'])
    mapping['symbol_in_rna'] = mapping['nearest_tss_symbol'].isin(rna['gene_name'])
    biosamples = ET.parse(RAW / 'biosample_records.xml').getroot().findall('.//BioSample')
    attrs = [dict(biosample=b.attrib['accession'], attribute=a.attrib.get('attribute_name', ''), value=a.text or '') for b in biosamples for a in b.findall('./Attributes/Attribute')]
    assert {r['biosample'] for r in samples} == {b.attrib['accession'] for b in biosamples}
    checks = streaming_verify(RAW / RNA, '\t', rna_cols, rna_qc) + streaming_verify(RAW / ATAC, ',', atac_cols, atac_qc) + title_verify(samples)
    checks.extend(coordinate_match.values())
    summary = dict(rna=dict(rows=len(rna), columns=len(rna_cols), all_zero_rows=rna_zero, duplicate_gene_names=int(rna['gene_name'].duplicated().sum())),
        atac=dict(rows=len(atac), columns=len(atac_cols), all_zero_rows=atac_zero, author_filtered_flag_counts={str(k): int(v) for k,v in atac['filtered'].value_counts().items()}, inclusive_length_consistent=bool((atac['End'] - atac['Start'] + 1 == atac['Length']).all())),
        annotation=dict(rows=len(annotation), joined_to_count=int(in_counts.sum()), coordinate_agreement=coordinate_match, ensembl_in_rna=int(mapping['ensembl_in_rna'].sum()), nearest_symbol_in_rna=int(mapping['symbol_in_rna'].sum()), count_rows_without_annotation=int((~atac['peak_id'].isin(annotation['peak_id'])).sum())),
        source_timing_conflict_samples=[r['gsm'] for r in samples if r['timing_conflict']],
        within_assay_condition_pairing='unknown; source-local rep labels are not identities', cross_assay_pairing='unknown', batch='not specified',
        source_annotation_version='RNA says GENCODE release 27 and mm10; exact file unresolved. Official mouse M27 is GRCm39. Author-provided IDs/annotations are audited, not repaired.',
        unit_qualification='Published biological replicate meaning supports group-local replication; exact cross-condition preparation reuse is unqualified. No numerical population inference in this metadata run.',
        inference_limit='File/count/annotation joins are technical eligibility only. No NAM validation, selected gene effect, genotype comparison or regulatory target ranking.',
        verification_passed=all(checks), verification_checks=len(checks))
    write_tsv(out / 'sample_map.tsv', samples); write_tsv(out / 'count_qc.tsv', rna_qc + atac_qc)
    write_tsv(out / 'biosample_attributes.tsv', attrs); mapping.to_csv(out / 'author_annotation_map.tsv', sep='\t', index=False)
    for name, data in [('source_series.json', series), ('qualification.json', summary), ('verification.json', dict(ok=all(checks), checks=len(checks), method='pandas/numpy counts versus streaming CSV/Python integers; characteristic-derived labels versus title-derived labels; exact annotation-to-count coordinate joins. Same sources, not biological replication.'))]:
        (out / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    if not all(checks): raise AssertionError('Independent metadata verification failed')
    print(json.dumps(dict(samples=len(samples), rna_rows=len(rna), atac_rows=len(atac), annotation_rows=len(annotation), checks=len(checks), verified=True)))


if __name__ == '__main__': main()
