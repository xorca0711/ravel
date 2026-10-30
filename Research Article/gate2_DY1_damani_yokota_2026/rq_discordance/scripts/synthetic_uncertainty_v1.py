"""E3: fixed illustrative normal-estimate diagnostic, with no biological data."""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
from scipy.special import ndtri
from verify_synthetic_v1 import verify

ROOT = Path('Research Article/gate2_DY1_damani_yokota_2026/rq_discordance')


def validate(config):
    if not 0 < config['alpha'] < 1 or config['draws_per_scenario'] < 1:
        raise ValueError('Invalid alpha or sample count')
    ids = [s['id'] for s in config['scenarios']]
    if len(ids) != len(set(ids)) or not ids:
        raise ValueError('Scenario identifiers must be unique and nonempty')
    for s in config['scenarios']:
        if not all(np.isfinite(s[k]) for k in ['truth_a', 'truth_b', 'se_a', 'se_b']) or min(s['se_a'], s['se_b']) <= 0:
            raise ValueError('Finite truths and positive known SEs required')


def events_for(a, b, scenario, cutoff):
    da, db = np.abs(a / scenario['se_a']) > cutoff, np.abs(b / scenario['se_b']) > cutoff
    return dict(detect_a=da, detect_b=db, both_detect=da & db,
        only_a=da & ~db, only_b=~da & db, neither_detect=~da & ~db,
        detection_label_mismatch=da != db, same_sign=a * b > 0, opposite_sign=a * b < 0,
        coverage_a=np.abs(a - scenario['truth_a']) <= cutoff * scenario['se_a'],
        coverage_b=np.abs(b - scenario['truth_b']) <= cutoff * scenario['se_b'])


def write_table(path, rows):
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t')
        writer.writeheader(); writer.writerows(rows)


def plot(config, rows, events, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    y = np.arange(len(rows))
    mismatch = [next(e['fraction'] for e in events if e['scenario'] == s['id'] and e['event'] == 'detection_label_mismatch') for s in config['scenarios']]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={'width_ratios': [1.3, 1]})
    axes[0].barh(y, mismatch, color='#3c6e91')
    axes[0].set_yticks(y, [s['label'] for s in config['scenarios']]); axes[0].invert_yaxis()
    axes[0].set_xlim(0, 1); axes[0].set_xlabel('Fraction with one detected estimate and one not detected')
    axes[0].set_title('Detection-label mismatch (two-sided alpha = 0.05)')
    for i, value in enumerate(mismatch): axes[0].text(value + .015, i, f'{value:.3f}', va='center')
    axes[1].barh(y - .18, [r['ci_width_a'] for r in rows], height=.33, label='Assay A', color='#3c6e91')
    axes[1].barh(y + .18, [r['ci_width_b'] for r in rows], height=.33, label='Assay B', color='#c98a45')
    axes[1].set_yticks(y, [''] * len(rows)); axes[1].invert_yaxis(); axes[1].legend()
    axes[1].set_xlabel('Fixed 95% interval width (illustrative units)'); axes[1].set_title('Precision depends on known SE, not detection')
    fig.suptitle('Synthetic measurement diagnostic — independent normal estimates', fontsize=14)
    fig.text(.5, .01, 'No biological calibration, equivalence margin or inference about NAM biology; real RNA and ATAC scales are not equated.', ha='center', fontsize=9)
    fig.tight_layout(rect=[0, .045, 1, .94]); fig.savefig(path, dpi=160); plt.close(fig)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True); args = parser.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    config = json.loads((ROOT / 'config/synthetic_parameters_v1.json').read_text())
    validate(config)
    cutoff = float(ndtri(1 - config['alpha'] / 2)); n = config['draws_per_scenario']
    rows, events = [], []
    seeds = np.random.SeedSequence(config['seed']).spawn(len(config['scenarios']))
    for s, seed in zip(config['scenarios'], seeds, strict=True):
        rng = np.random.default_rng(seed)
        a = rng.normal(s['truth_a'], s['se_a'], n); b = rng.normal(s['truth_b'], s['se_b'], n)
        row = dict(scenario=s['id'], draws=n, truth_a=s['truth_a'], truth_b=s['truth_b'],
            se_a=s['se_a'], se_b=s['se_b'], mean_a=float(a.mean()), mean_b=float(b.mean()),
            ci_width_a=2 * cutoff * s['se_a'], ci_width_b=2 * cutoff * s['se_b'])
        rows.append(row)
        for event, values in events_for(a, b, s, cutoff).items():
            count = int(np.count_nonzero(values))
            events.append(dict(scenario=s['id'], event=event, count=count, denominator=n, fraction=count / n))
    exact, verification = verify(config, rows, events)
    write_table(out / 'scenario_summary.tsv', rows); write_table(out / 'event_frequencies.tsv', events)
    write_table(out / 'analytic_expectations.tsv', exact)
    (out / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    if not verification['ok']: raise AssertionError('Prespecified Monte Carlo/analytic verification failed')
    plot(config, rows, events, out / 'synthetic_diagnostic.png')
    (out / 'summary.json').write_text(json.dumps(dict(scenarios=len(rows), draws_per_scenario=n, checks=len(verification['checks']), verified=True,
        limit=config['assumptions'], context='Methodological extension to DY1-P02, whose original context includes N. brasiliensis history and later IAV challenge. This run uses synthetic data only.'), indent=2) + '\n')
    print(json.dumps(dict(scenarios=len(rows), checks=len(verification['checks']), verified=True)))


if __name__ == '__main__': main()
