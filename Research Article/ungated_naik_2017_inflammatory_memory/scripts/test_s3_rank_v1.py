"""Artificial interval/rank pipeline and supported upstream toy-reader checks."""
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

from s3_rank_v1 import annotation_windows, percentile_points, analyze, prepare_examples, flip, tsv, save
from s3_rank_plot_v1 import plot


def test():
    assert np.array_equal(percentile_points([0, 1, 1, 2]), [0, 50, 50, 100])
    assert np.array_equal(percentile_points([4, 4, 4, 4]), [50, 50, 50, 50])
    assert np.array_equal(percentile_points([0, 1, 1, 2]), percentile_points([7, 10, 10, 13]))
    assert flip(np.array([1e-12, 1, 0]), np.array([-1, -1, 1])).tolist() == [False, True, False]
    for bad in [[1, float('nan')], [1, float('inf')]]:
        try: percentile_points(bad)
        except ValueError: pass
        else: raise AssertionError('nonfinite rank input accepted')
    root = Path(__file__).resolve().parents[3]; parent = root / 'raw_data'
    with tempfile.TemporaryDirectory(prefix='s3_rank_synthetic_', dir=parent) as temporary:
        fixture = Path(temporary); assert fixture.resolve().parent == parent.resolve()
        source = fixture / 'source'; source.mkdir(); output = fixture / 'output'; output.mkdir()
        fixed = [('ENSMUSG00000037860.15', 'Aim2'), ('ENSMUSG00000075605.3', '2300005B03Rik'),
                 ('ENSMUSG00000029661.16', 'Col1a2'), ('ENSMUSG00000039775.7', 'Defb3'),
                 ('ENSMUSG00000066756.5', 'Igfl3'), ('ENSMUSG00000054072.11', 'Iigp1'), ('ENSMUSG00000086503.3', 'Xist')]
        genes = fixed + [('artificial_' + str(i), 'Artificial' + str(i)) for i in range(65)]
        lines = []
        for i, (gene, name) in enumerate(genes):
            coordinate = 5000 + i * 5000
            if i == 1: coordinate = 0
            if i == 8: coordinate = 5000 + 7 * 5000
            strand = '+' if i % 2 == 0 else '-'
            left, right = (coordinate + 1, coordinate + 101) if strand == '+' else (max(1, coordinate - 99), coordinate + 1)
            kind = 'lncRNA' if name == 'Xist' else 'protein_coding'
            lines.append(f'chr1\tARTIFICIAL\tgene\t{left}\t{right}\t.\t{strand}\t.\tgene_id "{gene}"; gene_name "{name}"; gene_type "{kind}";\n')
        with gzip.open(source / 'gencode.vM9.annotation.gtf.gz', 'wt') as f: f.writelines(lines)
        (source / 'mm10.chrom.sizes').write_text('chr1\t500000\n')
        selection = pd.DataFrame([{'plot_slot': i, 'gene_id': gene, 'gene_name': name, 'selection_reason': 'frozen_artificial_' + str(i)} for i, (gene, name) in enumerate(fixed[1:], 1)])
        tsv(source / 'selected_cases.tsv', selection)
        windows, mapping, annotations = annotation_windows(source / 'gencode.vM9.annotation.gtf.gz', {'chr1': 500000})
        assert mapping.gene_id.nunique() == 71 and len(windows) == 140
        assert int(windows.clipped.sum()) == 2
        assert mapping.loc[mapping.gene_id == 'ENSMUSG00000075605.3', 'tss'].unique().tolist() == [0]
        tsv(output / 'windows.tsv', windows); tsv(output / 'gene_window_map.tsv.gz', mapping)
        examples = prepare_examples(source / 'selected_cases.tsv', annotations, mapping); save(output / 'example_manifest.json', examples)
        assert examples[-1]['status'] == 'unassayed_non_protein_coding'
        chosen = []
        for flank in [1000, 2000]:
            part = windows.loc[windows.flank == flank].reset_index(drop=True)
            spaced = {i * (len(part) - 1) // 31 for i in range(32)}
            anchors = set(mapping.loc[(mapping.flank == flank) & mapping.gene_id.isin([e['gene_id'] for e in examples if e['eligible']]), 'window_id'])
            for i, row in part.iterrows():
                why = (['annotation_order_spaced'] if i in spaced else []) + (['fixed_example'] if row.window_id in anchors else [])
                if why: chosen.append({'window_id': row.window_id, 'flank': flank, 'selection_reason': '|'.join(why)})
        tsv(output / 'verification_windows.tsv', pd.DataFrame(chosen))
        signals, readback = [], []; chosen_ids = {r['window_id'] for r in chosen}
        for j in range(8):
            gsm = 'GSM' + str(2441001 + j)
            for i, w in windows.iterrows():
                value = ((i * 7 + j * 11 + (i % 4) * (j % 3) + (3 * (j % 2) if w.flank == 2000 else 0)) % 12) / 3
                if i % 13 == 0: value = 0
                zeros = int(w.end - w.start) if value == 0 else 0
                signals.append({'window_id': w.window_id, 'gsm': gsm, 'mean_signal': value, 'encoded_zero_bases': zeros})
                if w.window_id in chosen_ids: readback.append({'gsm': gsm, 'window_id': w.window_id, 'base_array_mean': value, 'interval_weighted_mean': value, 'encoded_zero_bases': zeros, 'intervals': 1, 'scaled_error': 0})
        signal = pd.DataFrame(signals); tsv(output / 'window_signal.tsv.gz', signal); tsv(output / 'mean_readback.tsv', pd.DataFrame(readback))
        exported = pd.read_csv(output / 'window_signal.tsv.gz', sep='\t', float_precision='round_trip')
        assert np.array_equal(signal.mean_signal.to_numpy(), exported.mean_signal.to_numpy())
        signal = exported
        effects, diagnostics, summary = analyze(windows, signal); summary['analysis_id'] = 'synthetic.s3_rank'
        assert np.max(np.abs(diagnostics.mean_percentile - 50)) < 1e-10
        tsv(output / 'window_effects.tsv.gz', effects); tsv(output / 'library_diagnostics.tsv', diagnostics); save(output / 'summary.json', summary)
        cases = []
        for e in examples:
            for flank in [1000, 2000]:
                row = dict(e, flank=flank)
                if e['eligible']:
                    key = mapping.loc[(mapping.gene_id == e['gene_id']) & (mapping.flank == flank), 'window_id'].item()
                    row.update(effects.loc[effects.window_id == key].iloc[0].to_dict())
                cases.append(row)
        cases = pd.DataFrame(cases); tsv(output / 'selected_cases.tsv', cases); plot(output, effects, cases)
        contract = {'analysis_id': 'synthetic.s3_rank', 'inputs': [{'path': p.relative_to(root).as_posix()} for p in source.iterdir()]}
        contract_path = fixture / 'contract.json'; save(contract_path, contract)
        command = [sys.executable, str(Path(__file__).with_name('s3_rank_verify_v1.py')), '--contract', str(contract_path), '--run-dir', str(output)]
        result = subprocess.run(command, capture_output=True, text=True); assert result.returncode == 0, result.stdout + result.stderr
        verification = json.loads((output / 'verification.json').read_text())
        original = (output / 'window_effects.tsv.gz').read_bytes()
        effects.loc[0, 'D6_delta'] += .01; tsv(output / 'window_effects.tsv.gz', effects)
        rejected = subprocess.run(command, capture_output=True, text=True); assert rejected.returncode != 0 and 'D6_delta' in rejected.stderr
        (output / 'window_effects.tsv.gz').write_bytes(original)
        wsl_root = subprocess.run(['wsl.exe', '--exec', 'wslpath', '-a', str(root)], capture_output=True, text=True, check=True).stdout.strip()
        module_dir = wsl_root + '/' + Path(__file__).parent.relative_to(root).as_posix()
        toy = wsl_root + '/raw_data/naik2017_s3_runtime_v1/test.bw'
        code = '''import sys,math,numpy as np,bbi
sys.path.insert(0,sys.argv[1])
from s3_rank_extract_v1 import array_summary
from s3_rank_mean_verify_v1 import interval_mean
with bbi.open(sys.argv[2]) as track:
 values=track.fetch('1',0,3,missing=np.nan,exact=True)
 primary,zeros=array_summary(values,3)
 independent,other_zeros,n=interval_mean(track,'1',0,3)
 assert abs(primary-independent)<1e-12 and zeros==other_zeros==0 and n==3
 try: array_summary(track.fetch('1',0,4,missing=np.nan,exact=True),4)
 except ValueError: pass
 else: raise AssertionError('missing base was accepted')
 try: interval_mean(track,'1',0,4)
 except AssertionError: pass
 else: raise AssertionError('missing interval was accepted')
try: array_summary(np.array([1,float('inf')]),2)
except ValueError: pass
else: raise AssertionError('nonfinite base was accepted')
print('supported toy reader and missingness checks passed')'''
        reader = subprocess.run(['wsl.exe', '--exec', wsl_root + '/raw_data/naik2017_s3_runtime_v1/venv/bin/python', '-c', code, module_dir, toy], capture_output=True, text=True)
        assert reader.returncode == 0, reader.stdout + reader.stderr
        print(json.dumps({'status': 'passed', 'artificial_genes': 71, 'windows_per_width': 70, 'independent_checks': verification['checks'],
                          'maximum_scaled_error': verification['maximum_scaled_error'], 'corrupted_contrast_rejected': True,
                          'toy_reader_and_missingness': 'passed', 'real_research_track_reads': 0}))


if __name__ == '__main__': test()
