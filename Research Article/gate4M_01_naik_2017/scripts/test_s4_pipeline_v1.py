"""Analytical and full synthetic S4 tests; never read biological count inputs."""
import csv
import gzip
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
from s4_rna_v1 import calculate
from s2_rna_v1 import normalize


def analytical_checks():
    row = np.array([[1, 3, 3, 5, 3, 7, 7, 11, 0, 0, 0, 0],
                    [0, 0, 2, 2, 0, 0, 0, 0, 1, 1, 3, 3]], dtype=float)
    result = calculate(row, row, row, row)
    assert math.isclose(result['B0_log2_effect_mor'][0], math.log2(5 / 3))
    assert abs(result['W6_adjusted_mor'][0]) < 1e-10
    assert math.isclose(result['W6_control_wound_baseline_mor'][0], 1)
    assert math.isclose(result['W6_exposed_wound_baseline_mor'][0], 1)
    assert result['W12_all_zero'][0] and result['W12_adjustment_low_mean'][0]
    assert math.isclose(result['W6_adjusted_mor'][1], -math.log2(3))
    assert np.isnan(result['W6_adjusted_unregularized'][1])
    baseline = [math.log2((h + 1) / (c + 1)) for h in [3, 5] for c in [1, 3]]
    wound = [math.log2((h + 1) / (c + 1)) for h in [7, 11] for c in [3, 7]]
    combos = [w - b for w in wound for b in baseline]
    assert math.isclose(result['W6_adjustment_min'][0], min(combos))
    assert math.isclose(result['W6_adjustment_max'][0], max(combos))
    matrix = np.arange(1, 13, dtype=float)[None, :] * np.array([[1], [2], [3], [0]])
    mor, total, _, sf, tf, basis = normalize(matrix)
    assert basis == 3 and np.allclose(mor[:, :1], mor) and np.allclose(total[:, :1], total)
    assert math.isclose(np.prod(sf), 1) and math.isclose(np.prod(tf), 1)


def main():
    analytical_checks()
    root = Path(__file__).resolve().parents[3]
    parent = root / 'raw_data'
    with tempfile.TemporaryDirectory(prefix='s4_synthetic_', dir=parent) as temp:
        folder = Path(temp).resolve()
        assert folder.is_relative_to(parent.resolve())
        output = folder / 'output'; output.mkdir()
        genes = [f'SYNTHETIC_{i:06d}.1' for i in range(47729)]
        inputs, source = [], []
        for j in range(12):
            gsm = f'GSM{2440989 + j}'
            path = folder / f'{gsm}_synthetic.tab.gz'
            with gzip.open(path, 'wt') as handle:
                for i, gene in enumerate(genes):
                    count = (i % 97 + 1) * [1, 2, 3, 2, 2, 3, 1, 2, 3, 2, 2, 1][j]
                    if j % 4 >= 2 and i % 10 < 2:
                        count = count * 2 if j < 8 else count // 2
                    if j % 4 >= 2 and i % 10 in [3, 4]:
                        count = count // 2 if j < 8 else count * 3
                    if i % 13 == 0 or (j >= 4 and i % 17 == 0) or (j % 2 == 0 and i % 19 == 0): count = 0
                    handle.write(f'{gene}\t{count}\n')
            inputs.append(path)
            source.append({'gsm': gsm, 'assay': 'RNA-seq', 'day_label': '30',
                           'wound_hour_label': ['', '6', '12'][j // 4],
                           'history_label': 'control' if j % 4 < 2 else 'prior_inflammation',
                           'runs': f'SYNTHETIC_RUN_{j}', 'biosamples': f'SYNTHETIC_SAMPLE_{j}',
                           'instrument_models': 'Illumina HiSeq 2500', 'library_layouts': 'SINGLE',
                           'label_conflicts': '', 'source_compartment': 'synthetic fixture',
                           'characteristics': 'Sex: synthetic fixture only'})
        path = folder / 'library_crosswalk.tsv'
        with path.open('w', newline='') as handle:
            writer = csv.DictWriter(handle, source[0].keys(), delimiter='\t')
            writer.writeheader(); writer.writerows(source)
        inputs.append(path)
        path = folder / 'gencode.vM9.annotation.gtf.gz'
        with gzip.open(path, 'wt') as handle:
            for i, gene in enumerate(genes[:50]):
                name = ['Xist', 'Ddx3y', 'Eif2s3y', 'Kdm5d', 'Uty'][i] if i < 5 else f'SYNTHETIC{i}'
                chromosome = 'chrX' if i == 0 else 'chrY' if i < 5 else 'fixture'
                handle.write(f'{chromosome}\tfixture\tgene\t1\t10\t.\t+\t.\tgene_id "{gene}"; gene_name "{name}"; gene_type "synthetic";\n')
        inputs.append(path)
        contract = folder / 'synthetic_contract.json'
        contract.write_text(json.dumps({'analysis_id': 'synthetic.nonbiological_s4_test',
                                        'inputs': [{'path': p.relative_to(root).as_posix()} for p in inputs]}))
        process = subprocess.run([sys.executable, str(Path(__file__).with_name('s4_rna_v1.py')),
                                  '--contract', str(contract), '--output', str(output)], capture_output=True, text=True)
        if process.returncode:
            print(process.stderr[-5500:]); raise SystemExit(process.returncode)
        print(json.dumps(json.loads((output / 'verification.json').read_text())))
        print('Analytical and full synthetic S4 tests passed; artificial fixtures cleaned; research inputs not read.')


if __name__ == '__main__':
    main()
