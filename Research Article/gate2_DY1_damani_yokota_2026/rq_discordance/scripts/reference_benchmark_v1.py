"""E2: unranked source-labelled measurement contrasts and design sensitivity."""
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t
from verify_reference_benchmark_v1 import verify_features

ROOT = Path('Research Article/gate2_DY1_damani_yokota_2026/rq_discordance')
RAW = Path('raw_data/DY1_P02_reference_source_v1')
QUALIFIED = Path('analysis/research/runs/DY1_P02_reference_source_v1')


def conditional_intervals(control, condition, level, se_tolerance=1e-12):
    if control.shape != condition.shape or control.shape[1] < 2:
        raise ValueError('Equal group sizes >=2 required for the declared pairing sensitivity')
    n = control.shape[1]
    mc, mt = control.mean(axis=1), condition.mean(axis=1)
    vc, vt = control.var(axis=1, ddof=1), condition.var(axis=1, ddof=1)
    delta, v = mt - mc, (vc + vt) / n
    denom = (vc / n) ** 2 / (n - 1) + (vt / n) ** 2 / (n - 1)
    df = np.full(len(delta), np.nan)
    np.divide(v * v, denom, out=df, where=(denom > 0) & (v > se_tolerance ** 2))
    half = t.isf((1 - level) / 2, df) * np.sqrt(v)
    pair_lo, pair_hi = np.full(len(delta), np.inf), np.full(len(delta), -np.inf)
    pair_se_min, pair_se_max = np.full(len(delta), np.inf), np.zeros(len(delta))
    pair_bad = np.zeros(len(delta), dtype=np.int64)
    multiplier = t.isf((1 - level) / 2, n - 1)
    for order in itertools.permutations(range(n)):
        se = (condition - control[:, order]).std(axis=1, ddof=1) / math.sqrt(n)
        pair_se_min = np.minimum(pair_se_min, se); pair_se_max = np.maximum(pair_se_max, se)
        good = se > se_tolerance; pair_bad += ~good
        pair_lo = np.minimum(pair_lo, np.where(good, delta - multiplier * se, np.inf))
        pair_hi = np.maximum(pair_hi, np.where(good, delta + multiplier * se, -np.inf))
    pair_lo[~np.isfinite(pair_lo)] = np.nan; pair_hi[~np.isfinite(pair_hi)] = np.nan
    welch_lo, welch_hi = delta - half, delta + half
    env_lo, env_hi = np.fmin(welch_lo, pair_lo), np.fmax(welch_hi, pair_hi)
    complete = (pair_bad == 0) & np.isfinite(welch_lo)
    directional = complete & ((env_lo > 0) | (env_hi < 0))
    return pd.DataFrame(dict(control_mean=mc, condition_mean=mt, mean_delta=delta,
        control_sd=np.sqrt(vc), condition_sd=np.sqrt(vt), welch_lower=welch_lo, welch_upper=welch_hi,
        paired_lower_min=pair_lo, paired_upper_max=pair_hi, paired_se_min=pair_se_min, paired_se_max=pair_se_max,
        paired_degenerate_models=pair_bad, sensitivity_lower=env_lo, sensitivity_upper=env_hi,
        all_declared_models_nondegenerate=complete, sensitivity_directional=directional))


def normalize(counts, totals, offset):
    if not np.isfinite(counts).all() or (counts < 0).any() or (totals <= 0).any() or offset <= 0:
        raise ValueError('Invalid count normalization inputs')
    return np.log2(offset + 1e6 * counts / totals[None, :])


def summarize_pairs(rna, atac):
    r, a = rna['mean_delta'].to_numpy(), atac['mean_delta'].to_numpy()
    same, opposite = r * a > 0, r * a < 0
    directional = rna['sensitivity_directional'].to_numpy() & atac['sensitivity_directional'].to_numpy()
    return dict(pair_rows=len(r), same_nonzero_sign=int(same.sum()), opposite_nonzero_sign=int(opposite.sum()),
        one_or_both_zero=int((~same & ~opposite).sum()), both_directional_under_declared_models=int(directional.sum()),
        same_sign_and_both_directional=int((same & directional).sum()), opposite_sign_and_both_directional=int((opposite & directional).sum()))


def figure(rows, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    frame = pd.DataFrame(rows); y = np.arange(len(frame))
    labels = [f'{r.mapping_rule.replace("author_", "")} | {r.distance_subset} | offset {r.offset:g}' for r in frame.itertuples()]
    same = frame.same_nonzero_sign / frame.pair_rows
    opposite = frame.opposite_nonzero_sign / frame.pair_rows
    fig, ax = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    ax[0].barh(y, same, label='Same nonzero sign', color='#477b99')
    ax[0].barh(y, opposite, left=same, label='Opposite nonzero sign', color='#ba754a')
    ax[0].set_yticks(y, labels); ax[0].invert_yaxis(); ax[0].legend(loc='lower right', fontsize=8)
    ax[0].set_xlabel('Fraction of mapped gene–region rows'); ax[0].set_title('Directions of separate transformed-mean contrasts')
    ax[1].barh(y, frame.both_directional_under_declared_models / frame.pair_rows, color='#647f62')
    ax[1].set_xlabel('Fraction of mapped rows'); ax[1].set_title('Both sensitivity envelopes exclude zero')
    for axes in ax: axes.set_xlim(0, 1)
    fig.suptitle('External reference: source-labelled WT IL4 versus vehicle', fontsize=14)
    fig.text(.5, .015, 'No assay pairing established; repeated genes across region rows. Envelopes are design-conditional sensitivity, not population CIs or memory evidence.', ha='center', fontsize=9)
    fig.tight_layout(rect=[0, .05, 1, .94]); fig.savefig(path, dpi=160); plt.close(fig)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True); args = parser.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    config = json.loads((ROOT / 'config/reference_benchmark_parameters_v1.json').read_text())
    source = json.loads((QUALIFIED / 'qualification.json').read_text()); assert source['verification_passed']
    samples = pd.read_csv(QUALIFIED / 'sample_map.tsv', sep='\t', keep_default_na=False)
    annotation = pd.read_csv(QUALIFIED / 'author_annotation_map.tsv', sep='\t', keep_default_na=False)
    rna = pd.read_csv(RAW / 'GSE247223_countMatrixUpdated.tsv.gz', sep='\t', keep_default_na=False)
    atac = pd.read_csv(RAW / 'GSE248042_Chinenov_Deochand_submission_ATACseq_peak_count_matrix.csv.gz', keep_default_na=False)
    selected = samples[(samples.genotype == config['genotype']) & samples.condition.isin([config['comparator'], config['condition']])].copy()
    selected.to_csv(out / 'selected_source_samples.tsv', sep='\t', index=False)
    normalization_rows, eligibility, effects, checks = [], [], {}, []
    for assay, study, frame, key in [('RNA', 'GSE247223', rna, 'ensembl_id'),
        ('ATAC', 'GSE248042', atac, 'peak_id')]:
        group = selected[selected.study == study]
        columns = group.matrix_column.tolist()
        ci = np.flatnonzero((group.condition == config['comparator']).to_numpy())
        ti = np.flatnonzero((group.condition == config['condition']).to_numpy())
        assert len(ci) == len(ti) == (3 if assay == 'RNA' else 4)
        all_counts = frame[columns].to_numpy(dtype=np.int64)
        totals = all_counts.sum(axis=0)
        all_zero = (all_counts == 0).all(axis=1)
        eligible = ~all_zero
        counts = all_counts[eligible]; ids = frame.loc[eligible, key].to_numpy()
        for col, total in zip(columns, totals, strict=True): normalization_rows.append(dict(assay=assay, column=col, denominator_all_source_features=int(total)))
        eligibility.append(dict(assay=assay, source_features=len(frame), all_zero_selected_group_rows=int(all_zero.sum()), eligible_features=int(eligible.sum()), control_libraries=len(ci), condition_libraries=len(ti), pairing_models=math.factorial(len(ci)), library_denominator='all source count-matrix rows, including unannotated regions'))
        positions = np.unique(np.linspace(0, len(counts) - 1, min(config['verification_features_per_assay'], len(counts)), dtype=int))
        for offset in config['offsets']:
            transformed = normalize(counts, totals, offset)
            result = conditional_intervals(transformed[:, ci], transformed[:, ti], config['interval_level'], config['numerical_se_tolerance'])
            for c in verify_features(counts, totals, ci, ti, result, offset, config['interval_level'], positions, config['numerical_se_tolerance']): checks.append(dict(assay=assay, offset=offset, **c))
            result.insert(0, 'feature_id', ids); result.insert(1, 'offset', offset)
            effects[(assay, offset)] = result.set_index('feature_id', drop=False)
    for assay in ['RNA', 'ATAC']:
        result = pd.concat([effects[(assay, offset)] for offset in config['offsets']], ignore_index=True).sort_values(['feature_id', 'offset'])
        result.to_csv(out / (assay.lower() + '_descriptive_effects.tsv.gz'), sep='\t', index=False, compression={'method': 'gzip', 'mtime': 0}, na_rep='NA')
    symbol_ids = dict(zip(rna.gene_name, rna.ensembl_id, strict=True)); mapping_rows, summaries = [], []
    for rule in config['mapping_rules']:
        genes = annotation.ensemble_id if rule == 'author_ensembl' else annotation.nearest_tss_symbol.map(symbol_ids)
        pairs = pd.DataFrame(dict(peak_id=annotation.peak_id, gene_id=genes, dist_to_tss=pd.to_numeric(annotation.dist_to_tss, errors='coerce')))
        for distance in ['all_author_annotated', 'within_2kb_of_nearest_tss']:
            candidate = pairs if distance == 'all_author_annotated' else pairs[pairs.dist_to_tss.abs() <= config['distance_sensitivity_bp']]
            for offset in config['offsets']:
                r_effect, a_effect = effects[('RNA', offset)], effects[('ATAC', offset)]
                joined = candidate[candidate.peak_id.isin(a_effect.index) & candidate.gene_id.isin(r_effect.index)].copy()
                if joined.empty: raise ValueError('No exact eligible gene-region joins')
                rp, ap = r_effect.loc[joined.gene_id], a_effect.loc[joined.peak_id]
                summary = dict(mapping_rule=rule, distance_subset=distance, offset=offset, candidate_rows=len(candidate), unique_genes=joined.gene_id.nunique(), unique_regions=joined.peak_id.nunique(), **summarize_pairs(rp, ap))
                summaries.append(summary)
                checks.append(dict(assay='mapping', offset=offset, field=rule + '/' + distance + '/partition', passed=summary['same_nonzero_sign'] + summary['opposite_nonzero_sign'] + summary['one_or_both_zero'] == len(joined)))
                if offset == config['offsets'][0]: mapping_rows.append(joined.assign(mapping_rule=rule, distance_subset=distance))
    pd.concat(mapping_rows, ignore_index=True).sort_values(['mapping_rule', 'distance_subset', 'peak_id']).to_csv(out / 'mapping_membership.tsv.gz', sep='\t', index=False, compression={'method': 'gzip', 'mtime': 0})
    flag = atac.assign(author_annotation_present=atac.peak_id.isin(annotation.peak_id)).groupby(['filtered', 'author_annotation_present'], dropna=False).size().rename('rows').reset_index()
    flag.to_csv(out / 'annotation_flag_contingency.tsv', sep='\t', index=False)
    pd.DataFrame(normalization_rows).to_csv(out / 'library_denominators.tsv', sep='\t', index=False)
    pd.DataFrame(eligibility).to_csv(out / 'feature_eligibility.tsv', sep='\t', index=False)
    pd.DataFrame(summaries).to_csv(out / 'mapping_sensitivity.tsv', sep='\t', index=False)
    verification = dict(ok=all(c['passed'] for c in checks), checks=checks,
        method='Fixed 40 evenly spaced source-order feature positions per assay and offset: Python math/statistics scalar transformation, means, variances and all pairings versus vectorized numpy; shared source parser and scipy t distribution; exact mapping category partitions. Not biological replication.')
    (out / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    if not verification['ok']: raise AssertionError('Independent arithmetic disagreement')
    figure(summaries, out / 'reference_benchmark.png')
    (out / 'summary.json').write_text(json.dumps(dict(verified=True, arithmetic_checks=len(checks), eligible_features=eligibility, context=config['context'], uncertainty=config['uncertainty'],
        source_holds=['ATAC vehicle 24h title versus 25 hours characteristic', 'Within-assay across-condition preparation reuse unknown', 'Cross-assay pairing unknown', 'Batch labels unavailable', 'Exact annotation version unresolved; author mappings used as exposed association rules', 'Source matrices/annotation are author-selected deposited universes, not unbiased whole genomes'],
        endpoint='Separate mean log2(CPM+offset) condition-minus-control differences; not count-model log fold changes, p-values, TF activity, target rank or causal effects.'), indent=2) + '\n')
    print(json.dumps(dict(verified=True, checks=len(checks), mapping_summaries=len(summaries))))


if __name__ == '__main__': main()
