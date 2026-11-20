"""End-to-end S2 test using explicitly artificial inputs, never research data."""
import csv
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    root = Path(__file__).resolve().parents[3]
    parent = root / 'raw_data'
    with tempfile.TemporaryDirectory(prefix='s2_synthetic_', dir=parent) as temp:
        folder = Path(temp).resolve()
        assert folder.is_relative_to(parent.resolve())
        output = folder / 'output'; output.mkdir()
        genes = [f'SYNTHETIC_{i:06d}.1' for i in range(47729)]
        inputs, source = [], []
        for j in range(8):
            gsm = f'GSM{2440985 + j}'
            path = folder / f'{gsm}_synthetic.tab.gz'
            with gzip.open(path, 'wt') as handle:
                for i, gene in enumerate(genes):
                    count = (i % 97 + 1) * [1, 2, 3, 2, 2, 3, 1, 2][j]
                    if j % 4 >= 2 and i % 10 < 2: count *= 2 if j < 4 else 3
                    if j % 4 >= 2 and i % 10 in [3, 4]: count //= 2
                    if i % 13 == 0 or (j >= 4 and i % 17 == 0) or (j % 2 == 0 and i % 19 == 0): count = 0
                    handle.write(f'{gene}\t{count}\n')
            inputs.append(path)
            source.append({'gsm': gsm, 'assay': 'RNA-seq', 'day_label': '6' if j < 4 else '30',
                           'wound_hour_label': '', 'history_label': 'control' if j % 4 < 2 else 'prior_inflammation',
                           'runs': 'SYNTHETIC_RUN', 'biosamples': 'SYNTHETIC_SAMPLE',
                           'instrument_models': 'SYNTHETIC', 'library_layouts': 'SYNTHETIC'})
        path = folder / 'library_crosswalk.tsv'
        with path.open('w', newline='') as handle:
            writer = csv.DictWriter(handle, source[0].keys(), delimiter='\t')
            writer.writeheader(); writer.writerows(source)
        inputs.append(path)
        path = folder / 'gencode.vM9.annotation.gtf.gz'
        with gzip.open(path, 'wt') as handle:
            for i, gene in enumerate(genes[:50]):
                handle.write(f'fixture\tfixture\tgene\t1\t10\t.\t+\t.\tgene_id "{gene}"; gene_name "SYNTHETIC{i}"; gene_type "synthetic";\n')
        inputs.append(path)
        contract = folder / 'synthetic_contract.json'
        contract.write_text(json.dumps({'analysis_id': 'synthetic.nonbiological_smoke_test',
                                        'inputs': [{'path': p.relative_to(root).as_posix()} for p in inputs]}))
        process = subprocess.run([sys.executable, str(Path(__file__).with_name('s2_rna_v1.py')),
                                  '--contract', str(contract), '--output', str(output)], capture_output=True, text=True)
        if process.returncode:
            print(process.stderr[-5000:]); raise SystemExit(process.returncode)
        report = json.loads((output / 'verification.json').read_text())
        print(json.dumps(report))
        print('Synthetic end-to-end test passed; artificial fixtures cleaned up; research inputs not read.')


if __name__ == '__main__':
    main()
