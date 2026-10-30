"""E6 bounded source-average arithmetic; no replicate or variance reconstruction."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path('Research Article/gate2_DY1_damani_yokota_2026/rq_discordance')
RAW = Path('raw_data/DY1_P02_temporal_source_v1/GSE115504_memory_averaged.cpm.table.tsv.gz')


def contrasts(values, offset):
    if values.ndim != 2 or values.shape[1] != 4 or offset <= 0 or not np.isfinite(values).all() or (values < 0).any():
        raise ValueError('Four finite nonnegative source-average columns and positive offset required')
    logged = np.log2(values + offset)
    first, second = logged[:, 1] - logged[:, 0], logged[:, 3] - logged[:, 2]
    return pd.DataFrame(dict(first_stage_log_ratio=first, second_stage_log_ratio=second,
        second_minus_first=second - first, baseline_log_ratio=logged[:, 2] - logged[:, 0],
        any_nonzero_source_average=(values > 0).any(axis=1)))


def verify_all(values, result, offset):
    errors = []
    for i, (a0, a1, b0, b1) in enumerate(values):
        expected = [math.log2((a1 + offset) / (a0 + offset)), math.log2((b1 + offset) / (b0 + offset)),
            math.log2(((b1 + offset) * (a0 + offset)) / ((b0 + offset) * (a1 + offset))), math.log2((b0 + offset) / (a0 + offset))]
        for name, value in zip(['first_stage_log_ratio', 'second_stage_log_ratio', 'second_minus_first', 'baseline_log_ratio'], expected, strict=True):
            errors.append(abs(float(result.iloc[i][name]) - value))
    return dict(offset=offset, checks=len(errors), max_absolute_error=max(errors, default=0), tolerance=1e-11, passed=all(e <= 1e-11 for e in errors))


def summarize(result, offset):
    eligible = result[result.any_nonzero_source_average]
    a, b = eligible.first_stage_log_ratio, eligible.second_stage_log_ratio
    same, opposite = a * b > 0, a * b < 0
    change = eligible.second_minus_first
    return dict(offset=offset, source_rows=len(result), all_zero_wt_rows=int((~result.any_nonzero_source_average).sum()), eligible_rows=len(eligible),
        same_nonzero_sign=int(same.sum()), opposite_nonzero_sign=int(opposite.sum()), first_only_zero=int(((a == 0) & (b != 0)).sum()),
        second_only_zero=int(((a != 0) & (b == 0)).sum()), both_zero_contrasts=int(((a == 0) & (b == 0)).sum()),
        second_minus_first_positive=int((change > 0).sum()), second_minus_first_negative=int((change < 0).sum()), second_minus_first_zero=int((change == 0).sum()),
        second_minus_first_q25=float(change.quantile(.25)), second_minus_first_median=float(change.median()), second_minus_first_q75=float(change.quantile(.75)))


def figure(frames, config, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharex=True, sharey=True)
    bound = max(float(np.abs(frame[['first_stage_log_ratio', 'second_stage_log_ratio']]).to_numpy().max()) for frame in frames)
    for ax, frame, offset in zip(axes, frames, config['offsets'], strict=True):
        selected = frame[frame.any_nonzero_source_average]
        plot = ax.hexbin(selected.first_stage_log_ratio, selected.second_stage_log_ratio, gridsize=45, bins='log', mincnt=1, cmap='Blues', extent=(-bound, bound, -bound, bound))
        ax.axhline(0, color='grey', lw=.6); ax.axvline(0, color='grey', lw=.6); ax.plot([-bound, bound], [-bound, bound], ':', color='#ba754a', lw=1)
        ax.set_xlabel('First-stage log2 ratio of source averages'); ax.set_title(f'Offset {offset:g}; {len(selected):,} rows with nonzero WT values')
        fig.colorbar(plot, ax=ax, label='Feature rows per hexagon (log scale)')
    axes[0].set_ylabel('Second-stage log2 ratio of source averages')
    fig.suptitle('RNA-only reference: first and second source-defined stimulation stages')
    fig.text(.5, .015, 'Group averages only: no replicate variance, confidence interval, causal interaction or matched RNA–ATAC trajectory.', ha='center', fontsize=9)
    fig.tight_layout(rect=[0, .045, 1, .93]); fig.savefig(path, dpi=160); plt.close(fig)


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', required=True); args = p.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    config = json.loads((ROOT / 'config/source_average_parameters_v1.json').read_text())
    qualified = json.loads(Path('analysis/research/runs/DY1_P02_temporal_source_v1/qualification.json').read_text()); assert qualified['verified']
    data = pd.read_csv(RAW, sep='\t', keep_default_na=False); assert data.ORF.is_unique
    values = data[config['columns']].to_numpy(dtype=float)
    frames, verification, summaries = [], [], []
    for offset in config['offsets']:
        result = contrasts(values, offset); verification.append(verify_all(values, result, offset))
        summary = summarize(result, offset)
        assert sum(summary[k] for k in ['same_nonzero_sign', 'opposite_nonzero_sign', 'first_only_zero', 'second_only_zero', 'both_zero_contrasts']) == summary['eligible_rows']
        assert sum(summary[k] for k in ['second_minus_first_positive', 'second_minus_first_negative', 'second_minus_first_zero']) == summary['eligible_rows']
        summaries.append(summary); result.insert(0, 'source_row_id', data.ORF); result.insert(1, 'offset', offset); frames.append(result)
    pd.concat(frames, ignore_index=True).sort_values(['source_row_id', 'offset']).to_csv(out / 'source_average_contrasts.tsv.gz', sep='\t', index=False, compression={'method':'gzip', 'mtime':0})
    pd.DataFrame(summaries).to_csv(out / 'offset_sensitivity.tsv', sep='\t', index=False)
    check = dict(ok=all(v['passed'] for v in verification), arithmetic=verification, partitions_checked=4,
        method='Every feature and both offsets: numpy log differences versus Python math.log2 ratios/product ratio, plus exhaustive category partitions. Same source averages, not biological replication.')
    (out / 'verification.json').write_text(json.dumps(check, indent=2) + '\n')
    if not check['ok']: raise AssertionError('Independent source-average arithmetic failed')
    figure(frames, config, out / 'source_average_response.png')
    (out / 'summary.json').write_text(json.dumps(dict(verified=True, source_rows=len(data), offsets=config['offsets'], semantics=config['semantics'], endpoint=config['endpoint'], context=config['context'],
        limit='A log ratio of group averages is not a mean of individual log responses. Source rows are not replicate units. No standard errors or biological uncertainty can be recovered from this table.'), indent=2) + '\n')
    print(json.dumps(dict(verified=True, source_rows=len(data), arithmetic_checks=sum(v['checks'] for v in verification))))


if __name__ == '__main__': main()
