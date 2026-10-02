"""Audit deposited tables without fitting biological effects or changing sources."""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import platform
import sys
import openpyxl
from common import PACKAGE, verified_sources, read_json, write_json, write_tsv, new_run, finish_record


def source_number(value):
    # A dash is a source absence marker, not a measured numeric zero.
    if value in (None, '-', ''):
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0 or int(value) != value:
        raise ValueError(f'Invalid source count: {value!r}')
    return int(value)


def human_coverage(path):
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = list(workbook.active.values)
    workbook.close()
    if list(rows[0][3:9]) != [f'Patient {d} ({a})' for d in (1, 2, 3) for a in ('SS2', '10x')]:
        raise ValueError('Unexpected Table 2 donor/assay columns')
    long_rows, checks, compartment = [], [], None
    sums = [0] * 6
    reported_row_total = 0
    compartments = Counter()
    ids = []
    for sheet_row, row in enumerate(rows[1:], 2):
        if row[1] in ('Epithelial', 'Endothelial', 'Stromal', 'Immune'):
            compartment = row[1]
        if not isinstance(row[0], (int, float)):
            continue
        if compartment is None:
            raise ValueError('Cell type lacks compartment')
        cluster = source_number(row[0]); ids.append(cluster)
        compartments[compartment] += 1
        counts = [source_number(v) for v in row[3:9]]
        total = source_number(row[9]); reported_row_total += total
        observed_sum = sum(v for v in counts if v is not None)
        checks.append({'cluster_id': cluster, 'source_row': sheet_row, 'reported_total': total, 'sum_numeric_entries': observed_sum, 'agrees': total == observed_sum})
        for j, value in enumerate(counts):
            sums[j] += value if value is not None else 0
            long_rows.append({'cluster_id': cluster, 'compartment': compartment, 'author_cell_type': row[1], 'short_name': row[2], 'donor_id': f'P{j // 2 + 1}', 'assay': ('SS2', '10x')[j % 2], 'n_cells': '' if value is None else value, 'source_count_status': 'not_reported_dash_or_blank' if value is None else 'numeric', 'source_row': sheet_row, 'source_location': row[10] or ''})
    if ids != list(range(1, 59)):
        raise ValueError('Table 2 cluster IDs are not exactly 1..58')
    grand = next(r for r in rows if r[1] == 'Total (all compartments)')
    reported_columns = [source_number(v) for v in grand[3:9]]
    audit = {'n_populations': len(ids), 'compartments': dict(compartments), 'column_order': list(rows[0][3:9]), 'sum_population_rows_by_column': sums, 'reported_grand_row_by_column': reported_columns, 'sum_population_rows_total': sum(sums), 'sum_reported_population_totals': reported_row_total, 'sum_reported_grand_row_columns': sum(reported_columns), 'reported_grand_total': source_number(grand[9]), 'all_population_row_totals_agree': all(c['agrees'] for c in checks), 'published_10x': 65662, 'published_SS2': 9404, 'recomputed_10x': sum(sums[1::2]), 'recomputed_SS2': sum(sums[::2]), 'resolution': 'unresolved; retain deposited and recomputed values until versioned cell metadata reconciles membership'}
    return long_rows, audit, checks


def workbook_schema(path):
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheets = []
    for sheet in workbook:
        declared = [sheet.max_row, sheet.max_column]
        reset = declared == [1, 1]
        if reset:
            sheet.reset_dimensions()
            rows = list(sheet.values)
            actual = [len(rows), max((len(row) for row in rows), default=0)]
        else:
            rows = list(sheet.iter_rows(min_row=1, max_row=2, max_col=min(sheet.max_column, 14), values_only=True))
            actual = None
        sheets.append({'sheet': sheet.title, 'declared_shape': declared, 'actual_shape_after_reset': actual, 'dimensions_reset': reset, 'first_two_rows_up_to_14_columns': [list(row[:14]) for row in rows[:2]]})
    workbook.close()
    return sheets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()
    sources = verified_sources()
    config = read_json(PACKAGE / 'config/pipeline_v1.json')
    coverage, audit, row_checks = human_coverage(sources['supplement_table_2'])
    schemas = {key: workbook_schema(path) for key, path in sources.items() if path.suffix == '.xlsx'}
    library_design = []
    for key, path in sources.items():
        if not key.startswith('library_metadata_'):
            continue
        with path.open(encoding='utf-8-sig', newline='') as handle:
            for row in csv.DictReader(handle):
                library_design.append({'source_id': key, 'library_id': row.get('channel') or row.get('plate.barcode'), 'donor_id': row.get('patient'), 'assay': 'SS2' if key.endswith('SS2') else '10x', 'tissue': row.get('tissue', ''), 'source_region_field': row.get('region', ''), 'anatomical_location': row.get('location', ''), 'sampling_label': row.get('compartment') or row.get('label', ''), 'use': 'candidate_normal' if row.get('region') == 'normal' else 'exclude_or_resolve'})
    gates = []
    for contrast in config['contrasts']:
        for assay in config['metadata_contract']['assays']:
            for floor in [config['cell_floors']['primary']] + config['cell_floors']['sensitivity']:
                eligible = []
                for donor in ('P1', 'P2', 'P3'):
                    matched = [r for r in coverage if r['assay'] == assay and r['donor_id'] == donor and r['author_cell_type'] in (contrast['left'], contrast['right'])]
                    if len(matched) == 2 and all(r['n_cells'] != '' and r['n_cells'] >= floor for r in matched):
                        eligible.append(donor)
                gates.append({'contrast': contrast['id'], 'assay': assay, 'cell_floor': floor, 'eligible_donors_from_table2': ','.join(eligible), 'n_eligible_donors': len(eligible), 'passes_count_floor_only': len(eligible) >= config['cell_floors']['minimum_donors'], 'expression_gate': 'NOT_ASSESSED: cell metadata, region matching and count semantics pending'})
    out = new_run(args.outdir)
    write_tsv(out / 'human_celltype_coverage.tsv', coverage, list(coverage[0]))
    write_tsv(out / 'table2_row_checks.tsv', row_checks, list(row_checks[0]))
    write_tsv(out / 'library_design.tsv', library_design, list(library_design[0]))
    write_tsv(out / 'source_coverage_gates.tsv', gates, list(gates[0]))
    write_json(out / 'table2_reconciliation.json', audit)
    write_json(out / 'supplement_schema.json', schemas)
    finish_record(out, {'schema': 'TN2020-intake-run/v1', 'completed_at_utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version, 'platform': platform.platform(), 'openpyxl': openpyxl.__version__, 'stage': 'TN0', 'status': 'source intake complete with unresolved source discrepancies', 'source_files_verified': len(sources), 'expression_analysis_run': False})
    print(f'TN0 complete: {len(coverage)} donor/assay/type rows; {len(schemas)} workbooks; source total={audit["reported_grand_total"]}, recomputed={audit["sum_population_rows_total"]}.')


if __name__ == '__main__':
    main()
