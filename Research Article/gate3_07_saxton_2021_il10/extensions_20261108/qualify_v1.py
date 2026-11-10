"""Prospective source qualification; no gene-effect estimation."""
import argparse
import collections
import csv
import gzip
import json
import math
import re
from pathlib import Path

RAW = Path('raw_data/Saxton_extensions_20261108')
TARGETS = ('IFNG', 'GZMB', 'IL18RAP')


def write_csv(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def parse_soft(path):
    records = []
    current = None
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for line in f:
            if line.startswith('^SAMPLE = '):
                current = {'accession': line.strip().split(' = ', 1)[1]}
                records.append(current)
            elif current is not None and line.startswith('!Sample_') and ' = ' in line:
                k, v = line.rstrip('\n').split(' = ', 1)
                current.setdefault(k.removeprefix('!Sample_'), []).append(v)
    return records


def gorby(out):
    import openpyxl
    samples = []
    for r in parse_soft(RAW / 'GSE146438_family.soft.gz'):
        title = r['title'][0]
        alias = title.split(':')[0]
        samples.append(dict(accession=r['accession'], alias=alias,
                            source=r['source_name_ch1'][0], title=title,
                            characteristics=' | '.join(r.get('characteristics_ch1', [])),
                            description=' | '.join(r.get('description', [])),
                            relations=' | '.join(r.get('relation', []))))
    write_csv(out / 'samples.csv', samples, list(samples[0]))
    aliases = {r['alias']: r for r in samples if 'CD8' in r['source']}
    assert len(aliases) == 21, 'Unexpected or duplicate CD8 sample aliases'
    book = openpyxl.load_workbook(RAW / 'GSE146438_CD8_Normalised_Data.xlsx',
                                 read_only=True, data_only=True)
    assert book.sheetnames == ['Sheet1']
    sheet = book['Sheet1']
    it = sheet.iter_rows(values_only=True)
    header = next(it)
    assert header[:2] == ('Gene', 'gene_name')
    groups = collections.defaultdict(list)
    for i, h in enumerate(header):
        if isinstance(h, str) and h.endswith('.value'):
            groups[h[:-6]].append(i)
    assert set(groups) == set(aliases), 'Workbook/SOFT alias mismatch'
    ids, duplicate_ids, mapping = set(), 0, []
    n, mismatch, invalid = 0, 0, 0
    for row_number, row in enumerate(it, 2):
        if not any(v is not None for v in row):
            continue
        n += 1
        gid, symbol = row[:2]
        duplicate_ids += gid in ids
        ids.add(gid)
        for alias, ix in groups.items():
            vals = [row[i] for i in ix]
            mismatch += any(v != vals[0] for v in vals[1:])
            for v in vals:
                invalid += not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0
        if symbol in TARGETS:
            mapping.append(dict(symbol=symbol, gene_id=gid, workbook_row=row_number))
    book.close()
    write_csv(out / 'target_mapping.csv', mapping, ['symbol', 'gene_id', 'workbook_row'])
    unique_targets = all(sum(r['symbol'] == t for r in mapping) == 1 for t in TARGETS)
    result = dict(rows=n, unique_ids=len(ids), duplicate_id_rows=duplicate_ids,
                  unique_CD8_samples=len(groups), repeated_control_columns={a: len(i) for a, i in groups.items() if len(i)>1},
                  repeated_control_mismatches=mismatch, invalid_abundance_cells=invalid,
                  unique_targets=unique_targets,
                  finite_description_eligible=unique_targets and not duplicate_ids and not mismatch and not invalid,
                  abundance_unit='RPKM, per GEO and Gorby RNA methods; not raw counts',
                  unit_status='three human donors author-reported; D85/D93/D36 source blocks; independent donor crosswalk unresolved',
                  timing='activation/expansion with ligand over six days; differs from Saxton 24-hour post-activation treatment',
                  inference='finite source description only; no population tests or pooled study effect')
    (out / 'qualification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))


def screen(out, route):
    config = json.loads((Path(__file__).parent / 'screen_dispositions_v1.json').read_text())
    spec = config[route]
    summaries = json.loads((RAW / 'candidate_summaries_v1.json').read_text())['result']
    records = {r['accession']:r for k,r in summaries.items() if k!='uids'}
    queries, accessions = [], []
    for name in spec['queries']:
        q = json.loads((RAW / name).read_text())['esearchresult']
        assert int(q['count']) == len(q['idlist']), 'Search truncated: qualification must stop'
        accs = [summaries[u]['accession'] for u in q['idlist']]
        queries.append(dict(file=name, count=int(q['count']), query=q['querytranslation'], accessions=accs,
                            warnings=q.get('warninglist', {}), errors=q.get('errorlist', {})))
        accessions += accs
    accessions = list(dict.fromkeys(accessions))
    assert set(accessions) == set(spec['dispositions']), 'Every hit needs an explicit disposition'
    rows = []
    for a in accessions:
        r = records[a]
        rows.append(dict(accession=a, title=r['title'], organism=r.get('taxon',''),
                         sample_records=r['n_samples'], source_url='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='+a,
                         inspected='GEO summary and sample-title list; see plan for full-SOFT subset',
                         disposition=spec['dispositions'][a],
                         sample_titles=' | '.join(x.get('title','') for x in r.get('samples',[]))))
    write_csv(out / 'source_candidates.csv', rows, list(rows[0]))
    result = dict(route=route, queries=queries, retained_candidates=len(rows),
                  qualified_exact_interaction_sources=[], numerical_interaction='held',
                  missing=spec['missing'], scope='bounded public-source screen, not proof of universal absence or novelty')
    (out / 'screen.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=['gorby','coinput','priming'], required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.mode == 'gorby': gorby(args.output)
    else: screen(args.output, args.mode)
