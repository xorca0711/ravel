"""D180 ranks on the exact S3 universe, with source qualification before extraction."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

import numpy as np
import pandas as pd

from s3_rank_v1 import percentile_points, flip, quantiles, tsv, save

TIE = 1e-10
OLD = ['GSM' + str(i) for i in range(2441001, 2441009)]
NEW = ['GSM' + str(i) for i in range(2652413, 2652417)]
CANONICAL = ['chr' + str(i) for i in range(1, 20)] + ['chrX']
ANCHORS = [
    ('Aim2', 'ENSMUSG00000037860.15', 'chr1:173350878'),
    ('Casp1', 'ENSMUSG00000025888.5', 'chr9:5298516'),
    ('Il1b', 'ENSMUSG00000027398.13', 'chr2:129371138'),
    ('Il1r1', 'ENSMUSG00000026072.12', 'chr1:40225079'),
    ('Il18', 'ENSMUSG00000039217.12', 'chr9:50575272'),
]
PHASES = {'D6': (OLD[:2], OLD[2:4]), 'D30': (OLD[4:6], OLD[6:]), 'D180': (NEW[2:], NEW[:2])}


def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()


def read(path): return pd.read_csv(path, sep='\t', float_precision='round_trip')


def qualify_universe(windows, mappings, old, sizes, expected_windows=21760, expected_genes=21775):
    cols = ['window_id', 'anchor_id', 'flank', 'chrom', 'start', 'end', 'clipped']
    assert list(windows) == cols and len(windows) == 2 * expected_windows
    assert windows.window_id.is_unique and not windows.clipped.any()
    assert set(windows.flank) == {1000, 2000} and set(windows.chrom) <= set(CANONICAL)
    assert old[cols].equals(windows), 'S3 effects/window order or coordinates changed'
    for row in windows.itertuples(index=False):
        tss = int(row.anchor_id.split(':')[1])
        assert row.anchor_id == f'{row.chrom}:{tss}'
        assert row.window_id == f'{row.flank}:{row.chrom}:{row.start}-{row.end}'
        assert row.start == tss-row.flank and row.end == tss+row.flank
        assert 0 <= row.start < row.end <= sizes[row.chrom]
    assert len(mappings) == 2*expected_genes and not mappings.duplicated(['gene_id', 'flank']).any()
    lookup = windows.set_index('window_id')
    for flank in [1000, 2000]:
        w = windows.loc[windows.flank == flank]; m = mappings.loc[mappings.flank == flank]
        assert len(w) == expected_windows and w.anchor_id.is_unique
        assert len(m) == expected_genes and m.gene_id.is_unique
        assert set(m.window_id) == set(w.window_id) and set(m.gene_type) == {'protein_coding'}
        joined = lookup.loc[m.window_id]
        assert np.array_equal(joined.anchor_id.to_numpy(), m.anchor_id.to_numpy())
        assert np.array_equal(joined.start.to_numpy()+flank, m.tss.to_numpy())
        assert set(m.strand) <= {'+', '-'}
    assert set(windows.loc[windows.flank == 1000, 'anchor_id']) == set(windows.loc[windows.flank == 2000, 'anchor_id'])
    assert set(mappings.loc[mappings.flank == 1000, 'gene_id']) == set(mappings.loc[mappings.flank == 2000, 'gene_id'])
    for gsm in OLD:
        assert np.isfinite(old[[gsm+'__mean', gsm+'__percentile', gsm+'__zero_bases']].to_numpy()).all()
    anchors = []
    for slot, (name, gene, anchor) in enumerate(ANCHORS, 1):
        for flank in [1000, 2000]:
            match = mappings.loc[(mappings.gene_id == gene) & (mappings.flank == flank)]
            assert len(match) == 1 and match.iloc[0].gene_name == name and match.iloc[0].anchor_id == anchor
            anchors.append(dict(slot=slot, gene_name=name, gene_id=gene, anchor_id=anchor, flank=flank,
                                window_id=match.iloc[0].window_id, selection='fixed published anchor; exposed'))
    chosen = []
    for flank in [1000, 2000]:
        w = windows.loc[windows.flank == flank].reset_index(drop=True)
        spaced = {int(i*(len(w)-1)//31) for i in range(32)}
        fixed = {a['window_id'] for a in anchors if a['flank'] == flank}
        for i, row in w.iterrows():
            reasons = (['annotation_order_spaced'] if i in spaced else []) + (['fixed_anchor'] if row.window_id in fixed else [])
            if reasons: chosen.append(dict(window_id=row.window_id, flank=flank, selection_reason='|'.join(reasons)))
    return anchors, pd.DataFrame(chosen)


def qualify_sources(manifest, crosswalk, contract, root):
    assert manifest['all_downloaded'] is True and len(manifest['files']) == 4
    sources = {x['gsm']: x for x in manifest['files']}
    assert len(sources) == 4 and set(sources) == set(NEW)
    hashes = {x['path']: x['sha256'] for x in contract['inputs']}
    records = []
    for index, gsm in enumerate(NEW):
        source = sources[gsm]; rows = crosswalk.loc[crosswalk.gsm == gsm]
        assert len(rows) == 1
        row = rows.iloc[0].to_dict(); history = 'prior_inflammation' if index < 2 else 'control'
        assert row['assay'] == 'ATAC-seq' and str(row['day_label']) == '180'
        assert row['history_label'] == history and row['wound_hour_label'] == '' and row['label_conflicts'] == ''
        assert row['wound_status_label'] == 'no wound stated in selected metadata'
        assert row['runs'] == 'SRR'+str(5657347+index)
        assert row['biosamples'] == ['SAMN07203513','SAMN07203512','SAMN07203511','SAMN07203514'][index]
        assert row['instrument_models'] == 'Illumina HiSeq 2500' and row['library_layouts'] == 'PAIRED'
        assert row['organism'] == 'Mus musculus' and row['source_compartment'] == 'Skin'
        assert str(row['replicate_label']) == str(index % 2 + 1)
        label = 'PI' if index < 2 else 'Ctrl'
        name = f'{gsm}_{label}_D180_mm10_ATAC_Rep_{index % 2 + 1}_.bw'
        assert source['path'] == 'raw_data/naik2017_s6_d180_sources_v1/'+name
        assert source['url'] == f'https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2652nnn/{gsm}/suppl/{name}'
        assert source['sha256'] == hashes[source['path']]
        assert source['bytes'] == source['expected_bytes'] == (root/source['path']).stat().st_size
        assert source['exit_code'] == 0 and source['status'] == 'downloaded_size_and_hash_recorded'
        records.append(dict(source, source_identity=row, group='PI' if index < 2 else 'Ctrl'))
    return dict(files=records, hashes_verified_by_governed_runner=True, population_inference=False,
                cross_time_platform_difference=True, exact_pool_membership='unresolved', cross_assay_pairing='unresolved')


def analyze(windows, signal, old):
    assert set(signal.gsm) == set(NEW) and len(signal) == 4*len(windows)
    assert not signal.duplicated(['window_id', 'gsm']).any()
    frame = old.copy(); diagnostics = []
    assert frame[list(windows)].equals(windows)
    for gsm in NEW:
        part = signal.loc[signal.gsm == gsm].set_index('window_id')
        assert set(part.index) == set(windows.window_id)
        part = part.loc[frame.window_id]
        means = part.mean_signal.to_numpy(dtype=float); zeros = part.encoded_zero_bases.to_numpy(dtype=float)
        assert np.isfinite(means).all() and np.isfinite(zeros).all()
        assert np.equal(zeros, np.floor(zeros)).all() and ((zeros >= 0) & (zeros <= (frame.end-frame.start).to_numpy())).all()
        frame[gsm+'__mean'] = means; frame[gsm+'__zero_bases'] = zeros.astype(int)
        frame[gsm+'__percentile'] = np.nan
        for flank in [1000, 2000]:
            mask = frame.flank == flank; values = means[mask]; ranks = percentile_points(values)
            frame.loc[mask, gsm+'__percentile'] = ranks
            counts = np.unique(values, return_counts=True)[1]
            diagnostics.append(dict(gsm=gsm, flank=flank, windows=len(values), mean_percentile=float(ranks.mean()),
                zero_mean_windows=int((values == 0).sum()), unique_means=len(counts), tied_windows=int(counts[counts > 1].sum()),
                tied_window_fraction=float(counts[counts > 1].sum()/len(values)), largest_tie_group=int(counts.max())))
    c = frame[[g+'__percentile' for g in NEW[2:]]].to_numpy()
    h = frame[[g+'__percentile' for g in NEW[:2]]].to_numpy()
    frame['D180_delta'] = h.mean(axis=1)-c.mean(axis=1)
    combinations = np.stack([h[:,i]-c[:,j] for i in range(2) for j in range(2)], axis=1)
    for k, name in enumerate(['h1_c1','h1_c2','h2_c1','h2_c2']): frame['D180_'+name] = combinations[:,k]
    frame['D180_range_min'] = combinations.min(axis=1); frame['D180_range_max'] = combinations.max(axis=1)
    frame['D180_range_width'] = np.ptp(combinations, axis=1)
    frame['D180_range_touches_zero'] = (combinations.min(axis=1) <= TIE) & (combinations.max(axis=1) >= -TIE)
    # Local encoded zeros, local mean zeros, rank-contrast zeros and spread flags are distinct.
    for gsm in OLD+NEW:
        frame[gsm+'__mean_zero'] = frame[gsm+'__mean'] == 0
        frame[gsm+'__all_bases_zero'] = frame[gsm+'__zero_bases'] == frame.end-frame.start
    for phase in PHASES: frame[phase+'_computational_zero'] = np.abs(frame[phase+'_delta']) <= TIE
    summary = dict(by_flank={}, width_sensitivity={}, units='within-library rank percentile points',
        population_inference=False, original_memory_domain_classification=False, global_mean_rank_is_constrained=True,
        old_tracks_reextracted=False, matched_animals=False, comparator_priority=['D30','D6'])
    for flank in [1000, 2000]:
        f = frame.loc[frame.flank == flank]; d = f.D180_delta.to_numpy()
        block = dict(windows=len(f), D180_delta_quantiles=quantiles(d), D180_absolute_delta_quantiles=quantiles(np.abs(d)),
            D180_range_width_quantiles=quantiles(f.D180_range_width.to_numpy()),
            D180_fraction_range_touches_zero=float(f.D180_range_touches_zero.mean()),
            D180_fraction_computational_zero=float(f.D180_computational_zero.mean()),
            D180_mean_delta_constrained_zero=float(d.mean()), comparisons={})
        assert abs(float(d.mean())) <= TIE
        for phase in ['D30','D6']:
            other = f[phase+'_delta'].to_numpy(); difference = np.abs(d)-np.abs(other)
            block['comparisons'][phase] = dict(signed_shift_quantiles=quantiles(d-other),
                absolute_magnitude_difference_quantiles=quantiles(difference),
                fraction_absolute_smaller=float((difference < -TIE).mean()),
                fraction_absolute_larger=float((difference > TIE).mean()),
                fraction_absolute_within_computational_rule=float((np.abs(difference) <= TIE).mean()),
                fraction_opposite_signs=float(flip(d, other).mean()),
                fraction_computational_zero_status_change=float(((np.abs(d) <= TIE) != (np.abs(other) <= TIE)).mean()))
        summary['by_flank'][str(flank)] = block
    primary = frame.loc[frame.flank == 1000].set_index('anchor_id')
    sensitivity = frame.loc[frame.flank == 2000].set_index('anchor_id').loc[primary.index]
    a, b = primary.D180_delta.to_numpy(), sensitivity.D180_delta.to_numpy()
    summary['width_sensitivity'] = dict(anchors=len(a), signed_shift_quantiles=quantiles(b-a),
        absolute_shift_quantiles=quantiles(np.abs(b-a)), fraction_sign_flip=float(flip(a,b).mean()),
        fraction_computational_zero_status_change=float(((np.abs(a) <= TIE) != (np.abs(b) <= TIE)).mean()))
    return frame, pd.DataFrame(diagnostics), summary


def run(contract_path, output):
    started = time.monotonic(); root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    inputs = {Path(x['path']).name: root/x['path'] for x in contract['inputs']}
    def remaining():
        seconds = 7200-(time.monotonic()-started)
        if seconds <= 0: raise RuntimeError('Analysis entrypoint budget exceeded; preserve partial outputs')
        return seconds
    receipt = json.loads(inputs['receipt.json'].read_text())
    assert receipt['analysis_id'] == 'Nk17-P01.s3_tss_rank_v1' and receipt['status'] == 'executed'
    receipt_hashes = {Path(x['path']).name: x['sha256'] for x in receipt['outputs']}
    for name in ['windows.tsv','gene_window_map.tsv.gz','window_effects.tsv.gz']:
        assert sha(inputs[name]) == receipt_hashes[name], 'Frozen S3 output/receipt mismatch'
    assert any(x['path'].endswith('/gencode.vM9.annotation.gtf.gz') and x['sha256'] ==
        '93406cb8e6835339b0e64d0ad904a6d3e4527333f62a3a24f9a53c16083ca9fa' for x in receipt['inputs'])
    sizes = {line.split()[0]: int(line.split()[1]) for line in inputs['mm10.chrom.sizes'].read_text().splitlines()}
    windows, mappings, old = [read(inputs[n]) for n in ['windows.tsv','gene_window_map.tsv.gz','window_effects.tsv.gz']]
    anchors, chosen = qualify_universe(windows, mappings, old, sizes)
    crosswalk = pd.read_csv(inputs['library_crosswalk.tsv'], sep='\t', dtype=str, keep_default_na=False)
    sources = qualify_sources(json.loads(inputs['acquisition_manifest_v1.json'].read_text()), crosswalk, contract, root)
    save(output/'source_manifest.json', sources); save(output/'anchor_manifest.json', anchors)
    for name in ['windows.tsv','gene_window_map.tsv.gz']: shutil.copyfile(inputs[name], output/name)
    tsv(output/'verification_windows.tsv', chosen)
    wsl_root = subprocess.run(['wsl.exe','--exec','wslpath','-a',str(root)], capture_output=True,text=True,check=True).stdout.strip()
    def linux(path): return wsl_root+'/'+path.resolve().relative_to(root).as_posix()
    python = wsl_root+'/raw_data/naik2017_s3_runtime_v1/venv/bin/python'
    subprocess.run(['wsl.exe','--exec',python,linux(Path(__file__).with_name('s6c_reader_v1.py')),
        '--output',linux(output),'--sizes',linux(inputs['mm10.chrom.sizes']),
        '--s3-headers',linux(inputs['header_metadata.json']),'--max-seconds',str(remaining())], check=True,timeout=remaining())
    assert json.loads((output/'extraction_progress.json').read_text())['status'] == 'completed'
    signal = read(output/'window_signal.tsv.gz'); frame, diagnostics, summary = analyze(windows, signal, old)
    summary['analysis_id'] = contract['analysis_id']; save(output/'summary.json', summary)
    tsv(output/'window_effects.tsv.gz', frame); tsv(output/'library_diagnostics.tsv', diagnostics)
    indexed = frame.set_index('window_id', drop=False)
    cases = pd.DataFrame([dict(indexed.loc[a['window_id']].to_dict(), **{k:v for k,v in a.items() if k not in indexed.columns}) for a in anchors])
    tsv(output/'fixed_anchors.tsv', cases)
    from s6c_plot_v1 import plot
    plot(output, frame, cases)
    import matplotlib
    save(output/'runtime.json', dict(host_python=sys.version, numpy=np.__version__, pandas=pd.__version__, matplotlib=matplotlib.__version__,
        elapsed_seconds_before_final_verification=time.monotonic()-started, analysis_wall_budget_seconds=7200,
        reader=dict(python='3.13.18',pybbi='0.4.2',numpy='2.5.5',peak_rss_limit_mib=2048),
        derived_artifact_limit_mib=50, old_tracks_reextracted=False, stochastic_steps='none'))
    subprocess.run([sys.executable,str(Path(__file__).with_name('s6c_verify_v1.py')),'--contract',str(contract_path.resolve()),
        '--run-dir',str(output.resolve())],check=True,timeout=remaining())
    remaining(); total_bytes = sum(p.stat().st_size for p in output.iterdir() if p.is_file())
    assert total_bytes < 50*1024*1024, 'Artifact budget exceeded; preserve outputs for review'
    print(json.dumps(dict(status='completed_D180_finite_proxy_description',derived_bytes_before_receipt=total_bytes,
        analysis_elapsed_seconds=time.monotonic()-started)),flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--contract',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();run(args.contract,args.output)
