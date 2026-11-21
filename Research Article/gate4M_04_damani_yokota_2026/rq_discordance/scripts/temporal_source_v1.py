"""E6 source coverage and table qualification; no temporal biological estimate."""
import argparse
import csv
import gzip
import json
import math
import re
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
from reference_source_v1 import parse_soft, audit_counts, streaming_verify

RAW = Path('raw_data/DY1_P02_temporal_source_v1')
STUDIES = ['GSE115505', 'GSE115085', 'GSE115504', 'GSE115502', 'GSE110465', 'GSE151015']
MEMORY = 'GSE115504_memory_averaged.cpm.table.tsv.gz'
RNA2020 = 'GSE151015_mm_BMDM_Egr2_RNAseq_raw_counts.txt.gz'


def memory_column(title):
    match = re.fullmatch(r'mm_BMDM_(Wt|PpargKO)_(1st|2nd)_stim_(ctrl|3hIL4)_RNA_rep([12])', title)
    if not match: return None
    genotype, stage, exposure, rep = match.groups()
    return ('WT' if genotype == 'Wt' else 'KO') + ('_ctrl_' if stage == '1st' else '_IL4_pre_') + ('0h' if exposure == 'ctrl' else '3h_IL4')


def rna2020_column(sample):
    attrs = dict(x.split(': ', 1) for x in sample['characteristics_ch1'])
    title = sample['title'][0]
    rep = re.search(r'replicate (\d+)', title).group(1)
    return f'mm_BMDM_{attrs["genotype"]}_{attrs["treatment"]}_24h_rep{rep}'


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', required=True); args = p.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    membership, files, records, series_notes = [], [], {}, {}
    raw_entries = {}
    for study in STUDIES:
        with gzip.open(RAW / (study + '_family.soft.gz'), 'rt', encoding='utf-8') as f: series, samples = parse_soft(f.read())
        raw_entries[study] = samples; series_notes[study] = series
        for url in series.get('supplementary_file', []): files.append(dict(study=study, gsm='', url=url, level='series'))
        for gsm, sample in samples.items():
            title = sample['title'][0]; attrs = sample.get('characteristics_ch1', [])
            record = dict(gsm=gsm, title=title, assay='|'.join(sample.get('library_strategy', [])), source='|'.join(sample.get('source_name_ch1', [])),
                characteristics=json.dumps(attrs, ensure_ascii=False), title_hour_tokens='|'.join(re.findall(r'(\d+)\s*[-_]?\s*h', title, re.I)),
                unit='source sample record; biological independence/pairing not inferred from title or repeated identifiers')
            membership.append(dict(study=study, **record))
            records.setdefault(gsm, []).append(record)
            for url in sample.get('supplementary_file', []): files.append(dict(study=study, gsm=gsm, url=url, level='sample'))
    unique = []
    conflicts = []
    for gsm, versions in records.items():
        unique.append(dict(**versions[0], source_record_occurrences=len(versions)))
        if any(v != versions[0] for v in versions[1:]): conflicts.append(gsm)
    memory = pd.read_csv(RAW / MEMORY, sep='\t', keep_default_na=False)
    assert memory.ORF.is_unique
    columns = list(memory.columns[1:]); values = memory[columns].to_numpy(dtype=float)
    assert np.isfinite(values).all() and (values >= 0).all()
    links = []
    for gsm, sample in raw_entries['GSE115504'].items():
        col = memory_column(sample['title'][0])
        if col: links.append(dict(study='GSE115504', gsm=gsm, matrix_column=col, title=sample['title'][0], table_semantics='author-labelled group-averaged CPM; no per-replicate variance'))
    group_counts = pd.DataFrame(links).groupby('matrix_column').size()
    assert set(group_counts.index) == set(columns) and (group_counts == 2).all()
    totals = {c: [] for c in columns}; scalar_rows = 0
    with gzip.open(RAW / MEMORY, 'rt', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            scalar_rows += 1
            for c in columns: totals[c].append(float(row[c]))
    checks = [scalar_rows == len(memory)] + [math.isclose(math.fsum(totals[c]), float(values[:, j].sum()), rel_tol=1e-12, abs_tol=1e-8) for j,c in enumerate(columns)]
    rawrna = pd.read_csv(RAW / RNA2020, sep='\t', index_col=0, keep_default_na=False)
    assert rawrna.index.is_unique
    rna_links = []
    for gsm, sample in raw_entries['GSE151015'].items():
        if sample['library_strategy'] == ['RNA-Seq']:
            rna_links.append(dict(study='GSE151015', gsm=gsm, matrix_column=rna2020_column(sample), title=sample['title'][0], table_semantics='raw gene counts; source permits multi-overlap; not certified unique fragments'))
    assert {x['matrix_column'] for x in rna_links} == set(rawrna.columns)
    qc, all_zero = audit_counts(rawrna, list(rawrna.columns), 'RNA2020')
    # Raw source omits a label for the first (gene-ID) column; specify it explicitly
    # for the independent CSV reader rather than shifting the sample fields.
    with gzip.open(RAW / RNA2020, 'rt', encoding='utf-8') as f:
        header = f.readline().strip().split('\t'); sums = [0] * len(header); zeros = [0] * len(header); n = 0
        for row in csv.reader(f, delimiter='\t'):
            assert len(row) == len(header) + 1; n += 1
            for j, value in enumerate(row[1:]):
                value = int(value); sums[j] += value; zeros[j] += value == 0
    checks.extend([n == len(rawrna)])
    for j,r in enumerate(qc): checks.extend([sums[j] == r['count_sum'], zeros[j] == r['zero_rows']])
    for name, rows in [('series_sample_membership.tsv', membership), ('unique_sample_inventory.tsv', unique), ('listed_files.tsv', files), ('rna_column_source_links.tsv', links + rna_links), ('rna2020_count_qc.tsv', qc)]:
        pd.DataFrame(rows).to_csv(out / name, sep='\t', index=False)
    summary = dict(series=len(STUDIES), source_record_occurrences=len(membership), unique_gsm_records=len(unique), shared_gsm_record_conflicts=conflicts,
        memory_table=dict(rows=len(memory), columns=len(columns), nonnegative_finite=True, all_zero_rows=int((values == 0).all(axis=1).sum()), semantics='Source-labelled averaged CPM from two title-labelled records per group; no recoverable per-replicate variance or effective biological n inferred.', eligible='Point description of the four WT group averages with disclosed offset sensitivity; no genotype screen, confidence interval or independent replication.'),
        rna2020=dict(rows=len(rawrna), columns=len(rawrna.columns), all_zero_rows=all_zero, source_timing='Control versus 24-hour RNA groups only; early ChIP time points are not RNA or ATAC time points.', eligible='Assay-specific endpoint counts qualified structurally; not an early-to-late RNA trajectory or a matched temporal multi-assay panel.'),
        exclusions=['GSE115502 muscle-injury RNA is a different source context and is not substituted for cultured memory RNA.', 'Superseries/subseries duplicates are one source lineage, not extra replication.', 'Chromatin BEDGRAPH/bigWig files are normalized signals, not qualified common-region raw counts; no large raw archives acquired.', 'No cross-assay preparation pairing or within-condition independence is manufactured from repeated rep labels.'],
        verification_checks=len(checks), verified=all(checks))
    for name, data in [('source_series.json', series_notes), ('qualification.json', summary), ('verification.json', dict(ok=all(checks), checks=len(checks), method='Whole-file pandas/numpy versus CSV/Python fsum/integer accounting; exact source-column joins; explicit superseries deduplication. Same data, no independent biological replication.'))]:
        (out / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    if not all(checks): raise AssertionError('Source-table arithmetic conflict')
    print(json.dumps(dict(series=len(STUDIES), unique_samples=len(unique), checks=len(checks), verified=True)))


if __name__ == '__main__': main()
