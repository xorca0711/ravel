"""Verify tracked intake evidence and local links without requiring private inputs."""
import argparse
import csv
import re
from pathlib import Path
from urllib.parse import unquote
from common import PACKAGE, read_json, sha256, verified_sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--with-sources', action='store_true')
    args = parser.parse_args()
    for path in PACKAGE.rglob('*.json'):
        read_json(path)
    run = PACKAGE / 'runs/intake_v1'
    record = read_json(run / 'run_record.json')
    for name, expected in record['outputs'].items():
        if sha256(run / name) != expected:
            raise ValueError(f'Changed recorded output: {name}')
    for name, expected in record['code_sha256'].items():
        candidates = [PACKAGE / 'scripts' / name, run / 'code_snapshot' / (name + '.txt')]
        if not any(p.exists() and sha256(p) == expected for p in candidates):
            raise ValueError(f'Original run code unavailable: {name}')
    for name, expected in record['config_sha256'].items():
        if sha256(PACKAGE / 'config' / name) != expected:
            raise ValueError(f'Changed intake configuration: {name}')
    with (run / 'human_celltype_coverage.tsv').open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle, delimiter='\t'))
    if len(rows) != 348 or len({r['cluster_id'] for r in rows}) != 58:
        raise ValueError('Incomplete donor/assay/type table')
    audit = read_json(run / 'table2_reconciliation.json')
    total = sum(int(r['n_cells']) for r in rows if r['n_cells'] != '')
    if total != audit['sum_population_rows_total'] or total == audit['reported_grand_total']:
        raise ValueError('Source discrepancy was lost or coverage no longer reconciles')
    schemas = read_json(run / 'supplement_schema.json')
    if len(schemas) != 12 or not all(s['dimensions_reset'] and s['actual_shape_after_reset'][0] > 1 for s in schemas['supplement_table_7']):
        raise ValueError('Incomplete workbook inventory or lost Table 7 rows')
    for doc in PACKAGE.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', doc.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            destination = unquote(target.split('#')[0]).strip('<>')
            if destination and not (doc.parent / destination).exists():
                raise ValueError(f'Broken link in {doc.name}: {target}')
    if args.with_sources:
        print(f'{len(verified_sources())} local source hashes verified.')
    print('Package passed: JSON, output hashes, original code/config, 348 coverage rows, discrepancy retention, 12 workbook schemas, Table 7 dimensions and local links.')


if __name__ == '__main__':
    main()
