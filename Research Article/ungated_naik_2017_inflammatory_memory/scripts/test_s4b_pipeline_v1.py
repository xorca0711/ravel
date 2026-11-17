"""Small artificial frozen-output fixture, including undefined post-wound ratios."""
import csv
import gzip
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile


def write_rows(path, rows):
    opener = gzip.open if path.name.endswith('.gz') else open
    with opener(path, 'wt', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({k: 'NA' if isinstance(v, float) and math.isnan(v) else v for k, v in row.items()})


def run_test():
    root = Path(__file__).resolve().parents[3]
    parent = root / 'raw_data'
    parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='s4b_synthetic_', dir=parent) as directory:
        fixture = Path(directory)
        assert fixture.resolve().parent == parent.resolve()
        output = fixture / 'output'; output.mkdir()
        gsms = ['GSM' + str(n) for n in range(2440989, 2441001)]
        mor_factors = [.8, 1.2, 1.5, .6, 1, 1.1, .9, 1.4, .7, 1.3, 1.6, 1.8]
        total_factors = [1.3, .7, .8, 1.2, 1.4, .9, 1.1, .6, 1.8, 1.6, 1, 1.5]
        effects, values = [], []
        for i in range(64):
            raw = [(i * 31 + j * 13 + 7) % 300 + 1 for j in range(12)]
            if i == 0: raw = [0] * 12
            if i == 1: raw[:4] = [20, 40, 30, 60]; raw[4:8] = [0, 0, 50, 80]
            if i == 2: raw[:4] = [0, 30, 15, 40]
            if i == 3: raw[:4] = [0, 0, 30, 50]
            if i == 4: raw[:4] = [2, 1, 1, 2]
            if i == 5: raw = [0] * 12; raw[0] = 1; raw[2] = 1
            mor = [x / f for x, f in zip(raw, mor_factors)]
            total = [x / f for x, f in zip(raw, total_factors)]
            gene = 'synthetic_' + str(i)
            v = {'gene_id': gene}
            for j, gsm in enumerate(gsms):
                for suffix, matrix in [('raw', raw), ('mor', mor), ('total', total)]: v[gsm + '__' + suffix] = matrix[j]
            values.append(v)
            e = {'gene_id': gene, 'gene_name': gene}
            baseline_ok, w6_ok, w12_ok = i % 3 != 0, i % 4 != 0, i % 5 != 0
            e.update({'W6_union_qualified': baseline_ok or w6_ok, 'W6_both_qualified': baseline_ok and w6_ok,
                      'W12_union_qualified': baseline_ok or w12_ok, 'W12_both_qualified': baseline_ok and w12_ok,
                      'global_union_qualified': baseline_ok or w6_ok or w12_ok, 'all_three_qualified': baseline_ok and w6_ok and w12_ok})
            for norm in ['mor', 'total', 'unregularized']:
                matrix = total if norm == 'total' else mor
                offset = 0 if norm == 'unregularized' else 1
                for k, phase in enumerate(['B0', 'W6', 'W12']):
                    c, h = sum(matrix[4*k:4*k+2])/2, sum(matrix[4*k+2:4*k+4])/2
                    e[phase + '_log2_effect_' + norm] = math.log2((h + offset) / (c + offset)) if offset or min(c, h) > 0 else math.nan
                for phase in ['W6', 'W12']:
                    e[phase + '_adjusted_' + norm] = e[phase + '_log2_effect_' + norm] - e['B0_log2_effect_' + norm]
            e['B0_regularization_sensitive'] = min(sum(mor[:2])/2, sum(mor[2:4])/2) < 1 - 1e-10
            e['B0_control_zero'], e['B0_exposed_zero'] = sum(raw[:2]) == 0, sum(raw[2:4]) == 0
            effects.append(e)
        write_rows(fixture / 'gene_effects.tsv.gz', effects)
        write_rows(fixture / 'gene_values.tsv.gz', values)
        write_rows(fixture / 'selected_cases.tsv', [{'plot_slot': i+1, 'selection_reason': 'frozen_artificial_example_' + str(i), 'gene_id': effects[i]['gene_id']} for i in range(6)])
        (fixture / 'summary.json').write_text(json.dumps({'input_genes': 64}))
        contract = {'analysis_id': 'synthetic.s4b', 'inputs': [{'path': (fixture / name).relative_to(root).as_posix()} for name in ['gene_effects.tsv.gz', 'gene_values.tsv.gz', 'selected_cases.tsv', 'summary.json']]}
        contract_path = fixture / 'contract.json'; contract_path.write_text(json.dumps(contract))
        command = [sys.executable, str(Path(__file__).with_name('s4b_reference_v1.py')), '--contract', str(contract_path), '--output', str(output)]
        completed = subprocess.run(command, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stdout + completed.stderr
        with gzip.open(output / 'reference_effects.tsv.gz', 'rt') as handle: actual = list(csv.DictReader(handle, delimiter='\t'))
        assert actual[0]['W6_c2_h2_mor'] == '0'
        assert actual[1]['W6_c2_h2_unregularized'] == 'NA' and actual[1]['c2_h2_adjusted_shift_unregularized'] != 'NA'
        assert actual[2]['B0_c1_h1_unregularized'] == 'NA'
        assert actual[3]['primary_reference_any_zero'] == 'True'
        assert actual[5]['c2_h2_reference_low_mor'] == 'True'
        # Prove that summary corruption is detected, without changing real outputs.
        summary_path = output / 'summary.json'; saved = summary_path.read_bytes()
        summary = json.loads(saved); summary['comparisons']['W6']['comparison_union']['c2_h2']['fraction_W6_c2_h2_primary_sign_flip'] = -1
        summary_path.write_text(json.dumps(summary))
        rejected = subprocess.run([sys.executable, str(Path(__file__).with_name('s4b_verify_v1.py')), '--contract', str(contract_path), '--run-dir', str(output)], capture_output=True, text=True)
        assert rejected.returncode != 0 and 'fraction_W6_c2_h2_primary_sign_flip' not in rejected.stdout
        assert 'W6_c2_h2_primary_sign_flip' in rejected.stderr
        summary_path.write_bytes(saved)
        result = json.loads((output / 'verification.json').read_text())
        assert (output / 'fig01_baseline_reference.png').stat().st_size > 10000
        assert (output / 'fig01_baseline_reference.pdf').stat().st_size > 1000
        print(json.dumps({'status': 'passed', 'fixture_genes': 64, 'checks': result['checks'], 'maximum_scaled_error': result['maximum_scaled_error'], 'summary_corruption_rejected': True, 'real_inputs_read': False}))


if __name__ == '__main__': run_test()
