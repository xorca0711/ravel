"""Annotation-only X1 audit. Expression fields are never selected or parsed."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import json
from pathlib import Path
import re

FIELDS = ('geneID', 'Gene_name', 'Chrom', 'Strand', 'Start', 'End',
          'GeneLength', 'Gene_type', 'Description')
INPUT = Path('raw_data/Sx22')


def annotations(path):
    with gzip.open(path, 'rt', encoding='utf-8-sig', newline='') as stream:
        reader = csv.reader(stream, delimiter='\t')
        header = next(reader)
        if len(header) != len(set(header)) or not set(FIELDS) <= set(header):
            raise ValueError('Missing or duplicate annotation header')
        positions = [header.index(name) for name in FIELDS]
        result = []
        for index, row in enumerate(reader, 1):
            if len(row) != len(header):
                raise ValueError('Malformed source row')
            # Project metadata before retaining any row. Other fields are opaque.
            result.append(dict(row_index=index, **dict(zip(FIELDS, (row[i] for i in positions)))))
        return result


def compare_annotations(left, right):
    if left != right:
        raise ValueError('Annotation tables differ in order, length or values')


def stable_id(value):
    match = re.fullmatch(r'(ENSMUSG\d+)(?:\.(\d+))?', value)
    return match.groups() if match else (value, None)


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        if row['Gene_name']:
            groups[row['Gene_name']].append(row)
    repeated = []
    for symbol, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        distinct = lambda field: sorted({r[field] for r in members})
        repeated.append(dict(
            symbol=symbol, row_count=len(members),
            gene_ids=';'.join(distinct('geneID')),
            stable_id_count=len({stable_id(r['geneID'])[0] for r in members}),
            chromosome_count=len(distinct('Chrom')), chromosomes=';'.join(distinct('Chrom')),
            strand_count=len(distinct('Strand')), strands=';'.join(distinct('Strand')),
            locus_count=len({(r['Chrom'], r['Strand'], r['Start'], r['End']) for r in members}),
            biotype_count=len(distinct('Gene_type')), biotypes=';'.join(distinct('Gene_type')),
            description_count=len(distinct('Description'))))
    ids = Counter(r['geneID'] for r in rows)
    bases = Counter(stable_id(r['geneID'])[0] for r in rows)
    coordinate_issues = []
    for row in rows:
        try:
            start, end, length = (int(row[k]) for k in ('Start', 'End', 'GeneLength'))
            valid = start >= 0 and end >= start and length > 0
        except ValueError:
            valid = False
        if not valid or row['Strand'] not in ('+', '-') or not row['Chrom']:
            coordinate_issues.append(row['row_index'])
    summary = dict(
        rows=len(rows), selected_fields=list(FIELDS), expression_columns_selected=[],
        empty_fields={field: sum(not r[field] for r in rows) for field in FIELDS},
        repeated_gene_id_labels=sum(n > 1 for n in ids.values()),
        repeated_stable_id_labels=sum(n > 1 for n in bases.values()),
        version_suffixed_rows=sum(stable_id(r['geneID'])[1] is not None for r in rows),
        nonstandard_id_rows=sum(re.fullmatch(r'ENSMUSG\d+(?:\.\d+)?', r['geneID']) is None for r in rows),
        repeated_symbol_labels=len(repeated),
        rows_with_repeated_nonempty_symbols=sum(x['row_count'] for x in repeated),
        repeated_symbol_multiplicity=dict(sorted(Counter(str(x['row_count']) for x in repeated).items())),
        repeated_symbols_multiple_stable_ids=sum(x['stable_id_count'] > 1 for x in repeated),
        repeated_symbols_multiple_chromosomes=sum(x['chromosome_count'] > 1 for x in repeated),
        repeated_symbols_multiple_strands=sum(x['strand_count'] > 1 for x in repeated),
        repeated_symbols_multiple_loci=sum(x['locus_count'] > 1 for x in repeated),
        repeated_symbols_multiple_biotypes=sum(x['biotype_count'] > 1 for x in repeated),
        repeated_symbols_multiple_descriptions=sum(x['description_count'] > 1 for x in repeated),
        coordinate_or_strand_issue_rows=coordinate_issues,
        count_fpkm_annotation='exact rowwise equality',
        annotation_release='not reported; mm10 source label retained without remapping',
        mapping_provenance='deposited annotation only; no external gene mapping',
        exclusions='none; original row order and all annotation records retained',
        interpretation='identifier ambiguity only; no expression, target ranking or biological effect')
    return repeated, summary


def write_csv(path, rows, fields):
    with path.open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(output):
    rows = annotations(INPUT / 'GSE160217_060120_22_readcount_genename.xls.gz')
    compare_annotations(rows, annotations(INPUT / 'GSE160217_060120_22_fpkm_genename.xls.gz'))
    repeated, summary = summarize(rows)
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / 'annotations.csv', rows, ['row_index', *FIELDS])
    fields = ['symbol', 'row_count', 'gene_ids', 'stable_id_count', 'chromosome_count',
              'chromosomes', 'strand_count', 'strands', 'locus_count', 'biotype_count',
              'biotypes', 'description_count']
    write_csv(output / 'repeated_symbols.csv', repeated, fields)
    with (output / 'summary.json').open('x', encoding='utf-8') as stream:
        json.dump(summary, stream, indent=2)
        stream.write('\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args().output)
