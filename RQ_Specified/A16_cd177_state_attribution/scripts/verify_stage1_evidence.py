"""Verify archived A16 Stage 1 provenance and table summaries, without raw data.

This does not rerun the analysis or validate a biological interpretation.
The original scripts are preserved and are not imported (they overwrite outputs).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
TABLES = HERE / 'tables/stage1'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    failures = []
    checks = 0

    def require(ok, message):
        nonlocal checks
        checks += 1
        if not ok:
            failures.append(message)

    def equal_number(a, b, message):
        require(math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-10), message)

    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def rows(name):
        with (TABLES / name).open(encoding='utf-8-sig', newline='') as f:
            return list(csv.DictReader(f))

    record_paths = [('run_record.json', '01_stage1_c3_c4.py'),
                    ('run_record_c1_c2_c5.json', '02_stage1_c1_c2_c5.py')]
    for record_name, script_name in record_paths:
        record = json.loads((TABLES / record_name).read_text(encoding='utf-8'))
        require(sha(HERE / 'config/a16_question_contract.json') == record['a16_contract_sha256'], record_name + ': contract hash')
        require(sha(HERE / 'scripts' / script_name) == record['script_sha256'], script_name + ': script hash')
        for name, digest in record['outputs'].items():
            require(sha(TABLES / name) == digest, name + ': output hash')
        require(record['exposure']['declared'] == 'FULL', record_name + ': exposure')
        require(record['floor_cells_per_side'] == 30, record_name + ': cell floor')
        if 'erratum_sha256' in record:
            require(sha(HERE / 'reports/STAGE1_ERRATUM.md') == record['erratum_sha256'], 'erratum hash')
            # This England JSON is a text-normalized Git file. The recorded
            # digest is its LF Git-blob representation, also verified at both
            # the source branch and integration base; Windows checks out CRLF.
            source_contract = (ROOT / 'Research Article/gate2_C2_england_2025/config/continuation_contract.json').read_bytes()
            require(hashlib.sha256(source_contract.replace(b'\r\n', b'\n')).hexdigest() == record['england_continuation_contract_sha256'], 'continuation contract LF hash')

    c3 = [r for r in rows('A16_C3_matched_gene_null.csv') if r['endpoint'] == 'priming_associated']
    detail = defaultdict(list)
    for r in rows('A16_C3_control_gene_detail.csv'):
        detail[(r['arm'], r['unit'])].append(r)
    require(len(c3) == 9, 'C3: nine descriptive arm/stratum entries')

    def quantile(values, q):
        values = sorted(values)
        position = (len(values) - 1) * q
        lo, hi = math.floor(position), math.ceil(position)
        return values[lo] + (values[hi] - values[lo]) * (position - lo)

    for r in c3:
        key = (r['arm'], r['unit'])
        d = detail[key]
        values = [float(x['smd_priming']) for x in d
                  if x['smd_priming'] and math.isfinite(float(x['smd_priming']))]
        require(len(d) == int(r['n_control_genes_used']), str(key) + ': control detail count')
        require(len(values) == int(float(r['n_control_genes_estimable'])), str(key) + ': estimable controls')
        equal_number(quantile(values, .5), r['null_median'], str(key) + ': median')
        equal_number(quantile(values, .95), r['null_p95'], str(key) + ': p95')
        obs = float(r['cd177_smd'])
        equal_number(sum(v >= obs for v in values) / len(values), r['frac_control_ge_cd177'], str(key) + ': tail fraction')
        for x in d:
            det, mean = float(r['cd177_detection_rate']), float(r['cd177_mean_log1p_cp10k'])
            require(abs(float(x['detection_rate']) - det) <= .25 * det + 1e-12, str(key) + ': detection band')
            require(abs(float(x['mean_log1p_cp10k']) - mean) <= .35 * mean + 1e-12, str(key) + ': expression band')

    low = sum(int(r['n_control_genes_used']) < 40 for r in c3)
    above = sum(float(r['frac_control_ge_cd177']) == 0 for r in c3)
    require(low == 7, 'C3 erratum: seven of nine entries have <40 controls')
    require(above == 4, 'C3: four of nine exceed all sampled controls')

    c4 = rows('A16_C4_ambient_neutrophil_control.csv')
    require(len(c4) == 9, 'C4: nine entries')
    for r in c4:
        equal_number(float(r['smd_priming_residual_on_neutro']) / float(r['smd_priming_unadjusted']), r['retained_fraction_after_neutro'], r['unit'] + ': descriptive SMD ratio')

    c1 = [r for r in rows('A16_C1_neighbourhood_matched.csv') if r['endpoint'] == 'priming_associated' and r['k'] == '10']
    require(len(c1) == 9, 'C1: nine k=10 estimates')
    require(sum(float(r['mean_matched_difference']) > 0 for r in c1) == 8, 'C1: eight positive estimates')
    c5 = rows('A16_C5_threshold_sensitivity.csv')
    thin_a = [r for r in c5 if r['arm'].startswith('A_') and r['column'].startswith('d2026')]
    require(len(thin_a) == 4, 'C5: four primary-library thinned definitions')
    require(all(r['status'].startswith('not assessed') and int(r['n_pos']) < 30 for r in thin_a), 'C5: all primary-library thinning rows fail floor')
    c2 = rows('A16_C2_resolution_ladder.csv')
    require(len(c2) == 8, 'C2: two experiments with marginal and three resolutions')

    result = {'scope': 'Archived provenance and table consistency; no raw-data rerun or biological validation.',
              'checks': checks, 'failures': failures,
              'summary': {'C3_entries': len(c3), 'C3_below_40_controls': low,
                          'C3_above_all_sampled_controls': above, 'C1_positive_k10': 8,
                          'C5_primary_thinning_rows_below_floor': len(thin_a)},
              'unverified': ['Raw count matrices and barcode arrays used by C3/C4 are not directly hashed in its run record.',
                             'Recorded inputs and numerical computations were not independently replayed by this table verifier.',
                             'No contamination exclusion, position-independent mechanism or biological replication follows.']}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
