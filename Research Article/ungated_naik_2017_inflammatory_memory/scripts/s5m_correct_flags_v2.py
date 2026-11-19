"""Bounded correction of S5M display flags; preserve all numerical results."""
import argparse
import csv
import gzip
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


# Explicit source-field allowlist. Contrast-range flags are deliberately separate.
COUNT_ZERO_FIELDS = (
    's2__D6_zero_libraries', 's2__D6_control_zero', 's2__D6_exposed_zero', 's2__D6_all_zero',
    's2__D30_zero_libraries', 's2__D30_control_zero', 's2__D30_exposed_zero', 's2__D30_all_zero',
    's4__B0_zero_libraries', 's4__B0_control_zero', 's4__B0_exposed_zero', 's4__B0_all_zero',
    's4__W6_zero_libraries', 's4__W6_control_zero', 's4__W6_exposed_zero', 's4__W6_all_zero',
    's4__W12_zero_libraries', 's4__W12_control_zero', 's4__W12_exposed_zero', 's4__W12_all_zero',
    's4b__primary_reference_any_zero', 's4b__c2_h2_reference_any_zero', 's4b__c1_h1_reference_any_zero',
)
COUNT_NUMBER_FIELDS = (
    's2__D6_zero_libraries', 's2__D30_zero_libraries', 's4__B0_zero_libraries',
    's4__W6_zero_libraries', 's4__W12_zero_libraries',
)
RANGE_FIELDS = ('s4__W6_adjustment_range_includes_zero', 's4__W12_adjustment_range_includes_zero')
OLD = 'rna_any_zero_flag'
NEW = 'rna_any_count_zero_flag'
RANGE = 'rna_any_adjustment_range_includes_zero_flag'
UNCHANGED_FILES = ('gene_atac.tsv.gz', 'association_results.tsv', 'covariance_identity.tsv',
                   'fig01_associations.png', 'fig01_associations.pdf')


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')


def boolean(value):
    if value not in ('True', 'False'):
        raise ValueError('Missing or invalid source boolean: ' + str(value))
    return value == 'True'


def flags(row):
    count_values = []
    for field in COUNT_ZERO_FIELDS:
        value = row[field]
        if field in COUNT_NUMBER_FIELDS:
            number = int(value)
            if not 0 <= number <= 4:
                raise ValueError('Invalid source zero-library count')
            count_values.append(number > 0)
        else:
            count_values.append(boolean(value))
    # Parse every declared field even if an earlier value is true.
    range_values = [boolean(row[field]) for field in RANGE_FIELDS]
    return any(count_values), any(range_values)


def read_rows(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf-8', newline='') as handle:
        yield from csv.DictReader(handle, delimiter='\t')


def corrected_table(source, destination, observe=None):
    opener = gzip.open if source.suffix == '.gz' else open
    with opener(source, 'rt', encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle, delimiter='\t')
        fields = reader.fieldnames
        if OLD not in fields or NEW in fields or RANGE in fields:
            raise ValueError('Unexpected v1 aggregate schema')
        if not set(COUNT_ZERO_FIELDS + RANGE_FIELDS) <= set(fields):
            raise ValueError('Missing explicit source field')
        new_fields = []
        for field in fields:
            new_fields.extend([NEW, RANGE] if field == OLD else [field])
        with destination.open('wb') as raw:
            binary = gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) if destination.suffix == '.gz' else raw
            with io.TextIOWrapper(binary, encoding='utf-8', newline='') as output:
                writer = csv.DictWriter(output, fieldnames=new_fields, delimiter='\t', lineterminator='\n')
                writer.writeheader()
                for row in reader:
                    count, crossing = flags(row)
                    original = row.pop(OLD)
                    row[NEW], row[RANGE] = str(count), str(crossing)
                    writer.writerow(row)
                    if observe is not None:
                        observe(row, original)


def correct(source, output, analysis_id):
    for name in UNCHANGED_FILES:
        shutil.copyfile(source / name, output / name)
    summary = json.loads((source / 'universe_summary.json').read_text())
    manifest = json.loads((source / 'anchor_manifest.json').read_text())
    anchor_ids = {item['gene_id'] for item in manifest}
    anchor_flags = {}
    audit = {'gene_records': 0, 'v1_true_count_zero_false': 0, 'v1_false_count_zero_true': 0,
             'all_original_source_fields_preserved': True, 'count_zero_allowlist': list(COUNT_ZERO_FIELDS),
             'range_includes_zero_allowlist': list(RANGE_FIELDS), 'byte_preserved_files': list(UNCHANGED_FILES)}
    for block in summary['universes'].values():
        del block['rna_any_zero_genes']
        block.update(rna_any_count_zero_genes=0, rna_any_adjustment_range_includes_zero_genes=0,
                     range_includes_zero_without_count_zero_genes=0)

    def observe(row, old):
        count, crossing = boolean(row[NEW]), boolean(row[RANGE])
        previous = boolean(old)
        # The old error was the union of these two concepts, not another signal.
        if previous != (count or crossing):
            raise ValueError('Unexpected v1 aggregate discrepancy')
        audit['gene_records'] += 1
        audit['v1_true_count_zero_false'] += previous and not count
        audit['v1_false_count_zero_true'] += not previous and count
        for universe, block in summary['universes'].items():
            if boolean(row['universe_' + universe]):
                block['rna_any_count_zero_genes'] += count
                block['rna_any_adjustment_range_includes_zero_genes'] += crossing
                block['range_includes_zero_without_count_zero_genes'] += crossing and not count
        if row['gene_id'] in anchor_ids:
            if row['gene_id'] in anchor_flags:
                raise ValueError('Duplicate anchor gene')
            anchor_flags[row['gene_id']] = {NEW: count, RANGE: crossing}

    corrected_table(source / 'gene_join.tsv.gz', output / 'gene_join.tsv.gz', observe)
    corrected_table(source / 'anchor_values.tsv', output / 'anchor_values.tsv')
    for item in manifest:
        if item['source_record_present']:
            del item[OLD]
            item.update(anchor_flags[item['gene_id']])
    summary['analysis_id'] = analysis_id
    save(output / 'universe_summary.json', summary)
    save(output / 'anchor_manifest.json', manifest)
    save(output / 'flag_correction_audit.json', audit)
    return summary, manifest


def run(contract_path, output):
    started = time.monotonic()
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    source = next(root / x['path'] for x in contract['inputs'] if x['path'].endswith('/gene_join.tsv.gz')).parent
    summary, manifest = correct(source, output, contract['analysis_id'])
    import pandas as pd
    from s5m_plot_flags_v2 import plot_anchors
    anchors = pd.read_csv(output / 'anchor_values.tsv', sep='\t', dtype=str, keep_default_na=False)
    plot_anchors(output, manifest, anchors)
    import matplotlib
    save(output / 'runtime.json', dict(python=sys.version, pandas=pd.__version__, matplotlib=matplotlib.__version__,
         elapsed_seconds_before_verification=time.monotonic()-started, source_biological_analyses_rerun=False,
         coefficients_recomputed=False, stochastic_steps='none'))
    subprocess.run([sys.executable, str(Path(__file__).with_name('s5m_verify_flags_v2.py')),
                    '--contract', str(contract_path.resolve()), '--run-dir', str(output.resolve())], check=True)
    print(json.dumps({'analysis_id': contract['analysis_id'], 'status': 'completed_semantic_flag_correction',
                      'elapsed_seconds': time.monotonic()-started, 'gene_records': summary['gene_records']}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run(args.contract, args.output)
