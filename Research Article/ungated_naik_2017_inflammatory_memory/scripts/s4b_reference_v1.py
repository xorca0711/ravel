"""S4B: frozen-output baseline-reference sensitivity, without normalization refit."""
import argparse
import gzip
import io
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd

TIE = 1e-10
REFERENCES = {'c2_h2': ('GSM2440990', 'GSM2440992'), 'c1_h1': ('GSM2440989', 'GSM2440991')}
FLAGS = ['W6_union_qualified', 'W6_both_qualified', 'W12_union_qualified', 'W12_both_qualified', 'global_union_qualified', 'all_three_qualified']


def json_write(path, value):
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode())


def write_tsv(path, frame):
    if path.name.endswith('.gz'):
        with path.open('wb') as raw:
            with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as compressed:
                with io.TextIOWrapper(compressed, encoding='utf-8', newline='') as handle:
                    frame.to_csv(handle, sep='\t', index=False, na_rep='NA', float_format='%.17g', lineterminator='\n')
    else:
        frame.to_csv(path, sep='\t', index=False, na_rep='NA', float_format='%.17g', lineterminator='\n')


def flip(a, b):
    return ((a > TIE) & (b < -TIE)) | ((a < -TIE) & (b > TIE))


def unregularized(h, c):
    out = np.full(len(h), np.nan)
    valid = (h > 0) & (c > 0)
    out[valid] = np.log2(h[valid] / c[valid])
    return out


def quantiles(values):
    return {str(q): float(np.quantile(values, q)) for q in [0, .25, .5, .75, .9, .95, 1]}


def summarize(frame, phase, reference, mask):
    f = frame.loc[mask]
    if f.empty: return {'genes': 0}
    result = {'genes': len(f)}
    for name in [f'{phase}_primary_mor', f'{phase}_{reference}_mor', reference + '_adjusted_shift_mor']:
        values = f[name].to_numpy()
        result[name + '_quantiles'] = quantiles(values)
        result[name + '_absolute_quantiles'] = quantiles(np.abs(values))
    for key in [f'{phase}_{reference}_primary_sign_flip', f'{phase}_{reference}_normalization_sign_flip',
                reference + '_reference_any_zero', reference + '_reference_low_mor']:
        result['fraction_' + key] = float(f[key].mean())
    return result


def plot(output, frame, summary):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.titlesize': 10,
                         'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42})
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 10), layout='constrained')
    fig.suptitle('S4B: changing only the observed baseline reference\nFrozen S4 scale, wound means and qualification; one-library references do not establish matching or correction', fontsize=12)
    for row, phase in enumerate(['W6', 'W12']):
        f = frame.loc[frame[phase + '_union_qualified']]
        for col, reference in enumerate(REFERENCES):
            ax = axes[row, col]
            x, y = f[phase + '_primary_mor'].to_numpy(), f[phase + '_' + reference + '_mor'].to_numpy()
            span = max(np.max(np.abs(x)), np.max(np.abs(y)), .5) * 1.04
            ax.hexbin(x, y, gridsize=55, mincnt=1, bins='log', cmap='cividis', extent=(-span, span, -span, span))
            ax.plot([-span, span], [-span, span], '--', color='#777777', linewidth=.8)
            ax.axhline(0, color='#777777', linewidth=.5); ax.axvline(0, color='#777777', linewidth=.5)
            label = 'C2/H2 observed profile' if reference == 'c2_h2' else 'C1/H1 observed profile'
            fraction = summary['comparisons'][phase]['comparison_union'][reference]['fraction_' + phase + '_' + reference + '_primary_sign_flip']
            ax.set(xlim=(-span, span), ylim=(-span, span), xlabel=f'{phase} primary adjusted log2 effect',
                   ylabel=f'{phase} alternative adjusted log2 effect',
                   title=f'{label}; {phase}, union n = {len(f):,}\nPrimary/alternative sign changes: {fraction:.2%}')
            ax.set_aspect('equal', adjustable='box')
    fig.savefig(output / 'fig01_baseline_reference.png', dpi=300, bbox_inches='tight')
    fig.savefig(output / 'fig01_baseline_reference.pdf', bbox_inches='tight', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def run(contract_path, output):
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    paths = {Path(i['path']).name: root / i['path'] for i in contract['inputs']}
    upstream = pd.read_csv(paths['gene_effects.tsv.gz'], sep='\t', dtype=str, keep_default_na=False)
    use = ['gene_id'] + [gsm + '__' + suffix for gsm in ['GSM2440989', 'GSM2440990', 'GSM2440991', 'GSM2440992'] for suffix in ['raw', 'mor', 'total']]
    values = pd.read_csv(paths['gene_values.tsv.gz'], sep='\t', usecols=use, keep_default_na=False)
    original = json.loads(paths['summary.json'].read_text())
    assert len(upstream) == original['input_genes'] and upstream.gene_id.is_unique
    assert np.array_equal(upstream.gene_id.to_numpy(), values.gene_id.to_numpy())
    fields = {'gene_id': upstream.gene_id.to_numpy(), 'gene_name': upstream.gene_name.to_numpy()}
    for flag in FLAGS:
        assert upstream[flag].isin(['True', 'False']).all()
        fields[flag] = upstream[flag].eq('True').to_numpy()
    def number(name): return pd.to_numeric(upstream[name].replace('NA', np.nan), errors='raise').to_numpy(dtype=float)
    for normalization, suffix in [('mor', 'mor'), ('total', 'total'), ('unregularized', 'unregularized')]:
        effect_key = 'log2_effect_' + suffix
        fields['B0_primary_' + normalization] = number('B0_' + effect_key)
        for phase in ['W6', 'W12']:
            fields[phase + '_post_' + normalization] = number(phase + '_' + effect_key)
            fields[phase + '_primary_' + normalization] = number(phase + '_adjusted_' + suffix)
    fields['primary_reference_low_mor'] = upstream.B0_regularization_sensitive.eq('True').to_numpy()
    fields['primary_reference_any_zero'] = (upstream.B0_control_zero.eq('True') | upstream.B0_exposed_zero.eq('True')).to_numpy()
    for reference, (control, history) in REFERENCES.items():
        c, h = values[control + '__mor'].to_numpy(), values[history + '__mor'].to_numpy()
        fields[reference + '_reference_any_zero'] = (values[control + '__raw'].to_numpy() == 0) | (values[history + '__raw'].to_numpy() == 0)
        fields[reference + '_reference_low_mor'] = np.minimum(c, h) < 1 - TIE
        for normalization in ['mor', 'total', 'unregularized']:
            if normalization == 'unregularized': baseline = unregularized(h, c)
            else:
                hc, cc = values[history + '__' + normalization].to_numpy(), values[control + '__' + normalization].to_numpy()
                baseline = np.log2((hc + 1) / (cc + 1))
            fields['B0_' + reference + '_' + normalization] = baseline
            shift = fields['B0_primary_' + normalization] - baseline
            fields[reference + '_adjusted_shift_' + normalization] = shift
            for phase in ['W6', 'W12']:
                adjusted = fields[phase + '_post_' + normalization] - baseline
                fields[phase + '_' + reference + '_' + normalization] = adjusted
                difference = adjusted - fields[phase + '_primary_' + normalization]
                valid = np.isfinite(difference) & np.isfinite(shift)
                assert np.allclose(difference[valid], shift[valid], atol=TIE, rtol=TIE)
        for phase in ['W6', 'W12']:
            fields[phase + '_' + reference + '_primary_sign_flip'] = flip(fields[phase + '_' + reference + '_mor'], fields[phase + '_primary_mor'])
            fields[phase + '_' + reference + '_normalization_sign_flip'] = flip(fields[phase + '_' + reference + '_mor'], fields[phase + '_' + reference + '_total'])
    frame = pd.DataFrame(fields)
    numeric = [name for name in frame if name.endswith(('_mor', '_total')) and frame[name].dtype != bool]
    assert np.isfinite(frame[numeric].to_numpy()).all()
    write_tsv(output / 'reference_effects.tsv.gz', frame)
    selected = pd.read_csv(paths['selected_cases.tsv'], sep='\t', usecols=['plot_slot', 'selection_reason', 'gene_id'], dtype=str)
    cases = selected.merge(frame, on='gene_id', how='left', validate='one_to_one', sort=False)
    assert list(cases.gene_id) == list(selected.gene_id) and cases.gene_name.notna().all()
    write_tsv(output / 'selected_cases.tsv', cases)
    summary = {'analysis_id': contract['analysis_id'], 'input_genes': len(frame), 'comparisons': {},
               'same_adjusted_shift_at_both_times_by_construction': True, 'size_factors_refit': False,
               'qualification_recomputed': False, 'sex_assignment_pairing_or_exclusion': False,
               'population_inference': False, 'new_example_selection': False}
    for phase in ['W6', 'W12']:
        summary['comparisons'][phase] = {}
        for universe, mask in [('all_genes', np.ones(len(frame), dtype=bool)), ('comparison_union', frame[phase + '_union_qualified']),
                               ('baseline_intersection', frame[phase + '_both_qualified'])]:
            summary['comparisons'][phase][universe] = {reference: summarize(frame, phase, reference, mask) for reference in REFERENCES}
    json_write(output / 'summary.json', summary)
    json_write(output / 'reference_manifest.json', {'primary': {'control': ['GSM2440989', 'GSM2440990'], 'history': ['GSM2440991', 'GSM2440992'], 'operation': 'original arithmetic count-scale means'},
               'alternatives': {key: {'control': c, 'history': h, 'libraries_per_history': 1} for key, (c, h) in REFERENCES.items()},
               'selection_context': 'exposed S4 observed Xist/Y profiles; not verified sex strata or matched samples',
               'normalization_and_wound_components': 'frozen S4 outputs, unchanged', 'recorded_metadata': 'female labels retained; no reassignment'})
    plot(output, frame, summary)
    import matplotlib
    json_write(output / 'runtime.json', {'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__, 'matplotlib': matplotlib.__version__, 'stochastic_steps': 'none'})
    subprocess.run([sys.executable, str(Path(__file__).with_name('s4b_verify_v1.py')), '--contract', str(contract_path.resolve()), '--run-dir', str(output.resolve())], check=True)
    print(json.dumps({'analysis_id': contract['analysis_id'], 'genes': len(frame), 'verification': 'passed'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run(args.contract, args.output)
