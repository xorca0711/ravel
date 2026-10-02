"""Audit normalized cell metadata; count eligibility never proves raw-count validity."""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
from common import PACKAGE, read_json, new_run, write_json, write_tsv, sha256, finish_record


def audit_rows(rows, config):
    contract = config['metadata_contract']
    missing_tokens = {s.lower() for s in contract['unknown_tokens']}
    errors, excluded, seen, libraries, donors = [], Counter(), set(), {}, set()
    coverage = Counter()
    for number, row in enumerate(rows, 2):
        missing = [k for k in contract['required'] if str(row.get(k, '')).strip().lower() in missing_tokens]
        if missing:
            errors.append(f'row {number}: missing fields {missing}')
            continue
        assay = row['assay']
        if assay not in contract['assays'] or row['counts_unit'] != contract['counts_unit_by_assay'].get(assay):
            errors.append(f'row {number}: assay/count-unit mismatch')
            continue
        key = tuple(row[k] for k in contract['join_key'])
        if key in seen:
            errors.append(f'row {number}: duplicate assay/library/cell key')
            continue
        seen.add(key)
        library = (assay, row['raw_library_id'])
        identity = tuple(row[k] for k in ('donor_id', 'sample_id', 'tissue', 'condition', 'anatomical_region'))
        if library in libraries and libraries[library] != identity:
            errors.append(f'row {number}: conflicting donor/sample/tissue/region within library')
            continue
        libraries[library] = identity
        donors.add(row['donor_id'])
        if row['tissue'] != contract['eligible_tissue'] or row['condition'] != contract['eligible_condition']:
            excluded[f'{row["tissue"]}|{row["condition"]}'] += 1
            continue
        coverage[(row['donor_id'], assay, row['anatomical_region'], row['author_cell_type'])] += 1
    if not seen:
        errors.append('No valid cells')
    gates = []
    floor = config['cell_floors']['primary']
    for contrast in config['contrasts']:
        for assay in contract['assays']:
            regions = sorted({key[2] for key in coverage if key[1] == assay})
            for region in regions:
                eligible = [d for d in sorted(donors) if min(coverage[d, assay, region, contrast['left']], coverage[d, assay, region, contrast['right']]) >= floor]
                gates.append({'contrast': contrast['id'], 'assay': assay, 'anatomical_region': region, 'cell_floor': floor, 'n_eligible_donors': len(eligible), 'eligible_donors': ','.join(eligible), 'metadata_count_gate': 'PASS' if not errors and len(eligible) >= config['cell_floors']['minimum_donors'] else 'HOLD'})
    return errors, excluded, coverage, gates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata', required=True, help='Normalized UTF-8 TSV; see config metadata contract')
    parser.add_argument('--mapping-record', required=True, help='JSON with source_version, source_sha256, field_mapping, author_label_mapping and matrix_cell_join_status')
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()
    config = read_json(PACKAGE / 'config/pipeline_v1.json')
    mapping = read_json(args.mapping_record)
    for key in ('source_version', 'source_sha256', 'field_mapping', 'author_label_mapping', 'matrix_cell_join_status'):
        if not mapping.get(key):
            raise ValueError(f'Mapping record needs {key}')
    with open(args.metadata, encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle, delimiter='\t')
        missing = set(config['metadata_contract']['required']) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'Missing columns: {sorted(missing)}')
        errors, excluded, coverage, gates = audit_rows(reader, config)
    out = new_run(args.outdir)
    coverage_rows = [dict(zip(('donor_id', 'assay', 'anatomical_region', 'author_cell_type', 'n_cells'), (*k, v))) for k, v in sorted(coverage.items())]
    write_tsv(out / 'coverage.tsv', coverage_rows, ['donor_id', 'assay', 'anatomical_region', 'author_cell_type', 'n_cells'])
    write_tsv(out / 'gates.tsv', gates, ['contrast', 'assay', 'anatomical_region', 'cell_floor', 'n_eligible_donors', 'eligible_donors', 'metadata_count_gate'])
    write_json(out / 'audit.json', {'errors': errors, 'excluded_cell_counts': dict(excluded), 'metadata_valid': not errors, 'expression_gate': 'HOLD: raw-count identity, matrix joins and normalization provenance require a separate TN2 contract', 'matrix_cell_join_status_reported': mapping['matrix_cell_join_status']})
    finish_record(out, {'schema': 'TN2020-metadata-run/v1', 'completed_at_utc': datetime.now(timezone.utc).isoformat(), 'metadata_sha256': sha256(args.metadata), 'mapping_sha256': sha256(args.mapping_record), 'status': 'failed_validation' if errors else 'metadata_audited', 'expression_analysis_run': False})
    print(f'Metadata audit: {len(errors)} errors; {sum(g["metadata_count_gate"] == "PASS" for g in gates)} count gates pass; expression remains gated.')
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
