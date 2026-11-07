"""Annotate preserved v1 results; separately order compatible protein-coding loci."""
import argparse
import csv
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

V1 = Path('analysis/research/runs/dupage_target_screen_v1')
ANNOTATION = Path('raw_data/dupage_target_screen_20261107/Mus_musculus.gene_info.gz')


def read(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def write(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    rows = read(V1 / 'all_candidates.tsv')
    assert len(rows) == len({r['gene_id'] for r in rows}) == 11614
    annotations = defaultdict(dict)
    with gzip.open(ANNOTATION, 'rt', encoding='utf-8') as stream:
        reader = csv.DictReader(stream, delimiter='\t')
        assert {'#tax_id', 'GeneID', 'Symbol', 'chromosome', 'type_of_gene', 'description'} <= set(reader.fieldnames)
        for row in reader:
            if row['#tax_id'] == '10090':
                annotations[row['Symbol']][row['GeneID']] = row
    for row in rows:
        hits = list(annotations[row['gene_id']].values())
        status = 'unmatched' if not hits else 'ambiguous' if len(hits) != 1 else 'exact_unique'
        hit = hits[0] if len(hits) == 1 else {}
        chromosome = row['locus'].split(':')[0].removeprefix('chr')
        chromosome = 'MT' if chromosome == 'M' else chromosome
        if status == 'exact_unique' and chromosome not in hit['chromosome'].split('|'):
            status = 'chromosome_discordant'
        row.update(annotation_status=status, ncbi_gene_id=hit.get('GeneID', ''), ncbi_type=hit.get('type_of_gene', ''),
                   ncbi_chromosome=hit.get('chromosome', ''), ncbi_description=hit.get('description', ''),
                   protein_eligible=status == 'exact_unique' and hit.get('type_of_gene') == 'protein-coding',
                   coding_low_rank='', coding_state_rank='')
    frontier, counts = [], {}
    for track in ['low', 'state']:
        for direction, sign in [('positive', 1), ('negative', -1)]:
            candidates = [r for r in rows if r['protein_eligible'] and r['low_sign_stable'] == 'True'
                          and float(r['delta_low']) * sign > 0 and (track == 'low' or r['state_prioritized'] == 'True')]
            if track == 'low':
                candidates.sort(key=lambda r: (-float(r['low_sign_oriented_min']), r['gene_id']))
            else:
                candidates.sort(key=lambda r: (-float(r['interaction_sign_oriented_min']), -float(r['low_sign_oriented_min']), r['gene_id']))
            counts[track + '_' + direction] = len(candidates)
            for rank, row in enumerate(candidates, 1):
                row['coding_' + track + '_rank'] = rank
                if rank <= 10:
                    frontier.append({'track': track, 'direction': direction, 'rank': rank, 'gene_id': row['gene_id']})
    by_gene = {r['gene_id']: r for r in rows}
    frontier = [{**f, **by_gene[f['gene_id']]} for f in frontier]
    old_frontier = [{**r, **by_gene[r['gene_id']]} for r in read(V1 / 'review_frontier.tsv')]
    anchors = [{**r, **by_gene[r['gene_id']]} for r in read(V1 / 'anchor_lookup.tsv')]
    fields = list(rows[0])
    write(out / 'all_annotated.tsv', rows, fields)
    write(out / 'protein_frontier.tsv', frontier, ['track', 'direction', 'rank'] + fields)
    write(out / 'v1_frontier_audit.tsv', old_frontier, ['track', 'direction', 'rank'] + fields)
    write(out / 'anchor_lookup.tsv', anchors, ['eligible'] + fields)
    summary = {'universe': len(rows), 'annotation_status': dict(Counter(r['annotation_status'] for r in rows)),
               'protein_eligible': sum(r['protein_eligible'] for r in rows), 'track_counts': counts,
               'protein_frontier_unique': len({r['gene_id'] for r in frontier}),
               'v1_frontier_protein_unique': len({r['gene_id'] for r in old_frontier if r['protein_eligible']}),
               'scope': 'Current NCBI exact symbol/chromosome annotation; no alias recovery, coordinate conversion or target validation.'}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
