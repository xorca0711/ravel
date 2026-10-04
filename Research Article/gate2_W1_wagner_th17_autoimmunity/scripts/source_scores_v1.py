"""Exposed, descriptive reconstruction of pinned Compass outputs; not flux inference."""
from __future__ import annotations
import argparse
import importlib.metadata
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from scipy.stats import mannwhitneyu, rankdata
from statsmodels.stats.multitest import multipletests

SELECTED = {
    'PGM_neg': 'Phosphoglycerate mutase', 'LDH_L_neg': 'Lactate dehydrogenase',
    'TPI_neg': 'Triosephosphate isomerase', 'PDHm_pos': 'Pyruvate dehydrogenase',
    'ACONTm_pos': 'Aconitate hydratase', 'ICDHyrm_pos': 'Isocitrate dehydrogenase',
    'SUCD1m_pos': 'Succinate dehydrogenase', 'C160CPT1_pos': 'Carnitine palmitoyltransferase',
    'CSNATr_neg': 'Carnitine acetyltransferase', 'ARGN_pos': 'Arginase',
    'ARGDCm_pos': 'Arginine decarboxylase', 'AGMTm_pos': 'Agmatinase',
    'SPMDOX_pos': 'Spermidine dehydrogenase', 'r0281_neg': 'Putrescine diamine oxidase',
}
AMINO = ['Alanine and aspartate metabolism', 'Arginine and Proline Metabolism',
         'beta-Alanine metabolism', 'Cysteine Metabolism', 'D-alanine metabolism',
         'Folate metabolism', 'Glutamate metabolism', 'Glycine, serine, alanine and threonine metabolism',
         'Histidine metabolism', 'Lysine metabolism', 'Methionine and cysteine metabolism',
         'Taurine and hypotaurine metabolism', 'Tryptophan metabolism', 'Tyrosine metabolism',
         'Urea cycle', 'Valine, leucine, and isoleucine metabolism']


def transform(penalties):
    scores = -np.log1p(penalties)
    keep = np.ptp(scores, axis=1) >= 1e-3
    if not np.any(keep):
        raise ValueError('No varying score features')
    scores = scores[keep]
    return scores - scores.min(), keep


def contrasts(scores, positive):
    a, b = scores[:, positive], scores[:, ~positive]
    variance = ((a.shape[1]-1)*a.var(axis=1, ddof=1) +
                (b.shape[1]-1)*b.var(axis=1, ddof=1))/(scores.shape[1]-2)
    delta = a.mean(axis=1) - b.mean(axis=1)
    d = np.divide(delta, np.sqrt(variance), out=np.full(len(delta), np.nan), where=variance > 0)
    mw = mannwhitneyu(a, b, axis=1, alternative='two-sided', method='asymptotic', use_continuity=True)
    q = multipletests(mw.pvalue, method='fdr_bh')[1]
    return pd.DataFrame({'mean_Th17p': a.mean(axis=1), 'mean_Th17n': b.mean(axis=1),
                         'mean_difference': delta, 'cohens_d': d, 'U': mw.statistic,
                         'p_source': mw.pvalue, 'q_source': q,
                         'n_Th17p_cells': a.shape[1], 'n_Th17n_cells': b.shape[1]})


def cluster_raw(raw):
    varying = np.ptp(raw, axis=1) > 0
    if varying.sum() < 2:
        raise ValueError('Insufficient nonconstant reaction profiles')
    ranks = rankdata(raw[varying], axis=1, method='average')
    distances = pdist(ranks, metric='correlation')
    if not np.isfinite(distances).all() or distances.min() < -1e-12 or distances.max() > 2+1e-12:
        raise ValueError('Invalid Spearman distance')
    np.clip(distances, 0, 2, out=distances)
    tree = linkage(distances, method='complete')
    labels = fcluster(tree, 0.02, criterion='distance')
    return varying, labels


def annotate(stats, metadata):
    stats = stats.copy()
    keys = []
    for reaction in stats.index:
        if reaction in metadata.index:
            keys.append(reaction)
        elif reaction.endswith(('_pos', '_neg')) and reaction[:-4] in metadata.index:
            keys.append(reaction[:-4])
        else:
            raise ValueError('Unmapped reaction: '+reaction)
    stats['metadata_r_id'] = keys
    stats = stats.join(metadata, on='metadata_r_id', validate='many_to_one')
    if stats['subsystem'].isna().any() or stats['formula'].isna().any():
        raise ValueError('Missing source subsystem or formula')
    stats['subsystem_source'] = stats['subsystem']
    stats.loc[(stats.subsystem == 'Citric acid cycle') & ~stats.formula.str.contains('[m]', regex=False), 'subsystem'] = 'Other'
    stats['core'] = stats.confidence.isin([0, 4]) & stats.EC_number.notna()
    return stats


def pathway_summary(core):
    summaries = []
    for pathway, rows in core.groupby('subsystem', sort=True):
        if pathway in ['Miscellaneous', 'Unassigned', 'Other'] or 'Transport' in pathway or 'Exchange' in pathway or len(rows) <= 5:
            continue
        unique = rows.drop_duplicates('metareaction_id')
        significant = unique[unique.q_source < .1]
        summaries.append({'subsystem': pathway, 'reaction_count': len(rows),
                          'metareaction_count': len(unique),
                          'positive_q_lt_0_1': int((significant.cohens_d > 0).sum()),
                          'negative_q_lt_0_1': int((significant.cohens_d < 0).sum()),
                          'median_metareaction_d': unique.cohens_d.median(),
                          'median_member_weighted_d': rows.cohens_d.median(),
                          'minimum_d': unique.cohens_d.min(), 'maximum_d': unique.cohens_d.max(),
                          'both_source_significant_directions': bool((significant.cohens_d > 0).any() and (significant.cohens_d < 0).any())})
    return pd.DataFrame(summaries)


def save_table(frame, path, index=True):
    frame.to_csv(path, sep='\t', index=index, lineterminator='\n', float_format='%.15g', na_rep='NA')


def run(source, r0, runtime, output):
    environment = {'python': sys.version, 'packages': {n: importlib.metadata.version(n) for n in ['numpy','pandas','scipy','statsmodels','matplotlib']}}
    if environment != json.loads(runtime.read_text()):
        raise ValueError('Runtime differs from the qualified version record')
    if any(output.iterdir()) and any(output.glob('*.tsv')):
        raise FileExistsError('Refusing to overwrite numerical results')
    raw_df = pd.read_csv(source/'reactions.tsv', sep='\t', index_col=0)
    cells = pd.read_csv(source/'cell_metadata.csv', index_col=0)
    metadata = pd.read_csv(source/'reaction_metadata.csv', index_col=0)
    joined = pd.read_csv(r0/'cell_join.tsv', sep='\t', index_col=0, keep_default_na=False)
    if not raw_df.columns.equals(cells.index) or set(cells.index) != set(joined.index):
        raise ValueError('Cell identity/order differs from R0')
    if raw_df.index.has_duplicates or metadata.index.has_duplicates or cells.index.has_duplicates:
        raise ValueError('Duplicate input identity')
    raw = raw_df.to_numpy(dtype=float)
    if not np.isfinite(raw).all() or (raw < 0).any():
        raise ValueError('Invalid penalties')
    positive = (cells.cell_type == 'Th17p').to_numpy()
    if positive.sum() != 139 or (~positive).sum() != 151:
        raise ValueError('Condition membership differs from source')
    direct_scores, direct_keep = transform(raw)
    direct = contrasts(direct_scores, positive)
    direct.index = raw_df.index[direct_keep]
    direct.index.name = 'reaction_id'
    direct = annotate(direct, metadata)
    print('Reaction contrasts computed', len(direct), flush=True)
    varying, labels = cluster_raw(raw)
    member = pd.DataFrame({'reaction_id': raw_df.index[varying], 'metareaction_id': labels})
    grouped = pd.DataFrame(raw[varying], index=labels, columns=raw_df.columns).groupby(level=0, sort=True).mean()
    meta_scores, meta_keep = transform(grouped.to_numpy())
    meta = contrasts(meta_scores, positive)
    meta.index = grouped.index[meta_keep]
    meta.index.name = 'metareaction_id'
    member['tested'] = member.metareaction_id.isin(meta.index)
    expanded = member[member.tested].set_index('reaction_id').join(meta, on='metareaction_id', validate='many_to_one')
    expanded = annotate(expanded, metadata)
    pathways = pathway_summary(expanded[expanded.core])
    selected = pd.DataFrame(index=pd.Index(SELECTED, name='reaction_id')).join(expanded)
    selected['display_name'] = pd.Series(SELECTED)
    selected['available'] = selected.metareaction_id.notna()
    selected['direct_cohens_d'] = direct.cohens_d.reindex(selected.index)
    cell_scores = cells[['cell_type','MD_SRX','NREADS','NALIGNED','RALIGN']].join(joined[['gsm','source_label']])
    score_lookup = pd.DataFrame(meta_scores, index=meta.index, columns=cells.index)
    for reaction in SELECTED:
        if reaction in expanded.index:
            cell_scores[reaction] = score_lookup.loc[expanded.loc[reaction, 'metareaction_id']]
    cell_scores.index.name = 'cell_id'
    excluded = pd.DataFrame({'reaction_id': raw_df.index, 'raw_constant': ~varying,
                             'direct_range_below_0_001': ~direct_keep})
    save_table(direct, output/'reaction_statistics.tsv')
    save_table(meta, output/'metareaction_statistics.tsv')
    save_table(member, output/'metareaction_membership.tsv', False)
    save_table(expanded, output/'expanded_metareaction_statistics.tsv')
    save_table(pathways, output/'pathway_summary.tsv', False)
    save_table(selected, output/'selected_reactions.tsv')
    save_table(cell_scores, output/'selected_cell_scores.tsv')
    save_table(excluded, output/'exclusions.tsv', False)
    summary = {'cell_counts': cells.cell_type.value_counts().to_dict(), 'raw_reactions': len(raw_df),
               'raw_constant_reactions': int((~varying).sum()), 'tested_single_reactions': len(direct),
               'formed_metareactions': len(grouped), 'tested_metareactions': len(meta),
               'core_expanded_reactions': int(expanded.core.sum()),
               'core_metareactions_any_core_member': int(expanded.loc[expanded.core, 'metareaction_id'].nunique()),
               'source_paper_reported_metareactions': 1911, 'source_paper_reported_core_metareactions': 784,
               'source_count_comparison_is_not_equivalence': True,
               'display_pathways': len(pathways), 'pathways_with_both_source_significant_directions': int(pathways.both_source_significant_directions.sum()),
               'selected_missing': selected.index[~selected.available].tolist(),
               'constant_rule': 'Exactly constant raw rows excluded from undefined Spearman clustering; all excluded identities retained. Source helper has no explicit constant-row guard.',
               'scope': 'Author processed-output reconstruction and exposed aggregation sensitivity. Cells are observations; independent animal/preparation counts are unknown. No measured flux or population inference.'}
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    (output/'environment.json').write_text(json.dumps(environment, indent=2)+'\n')
    from verify_source_scores_v1 import verify
    verification = verify(source, output)
    (output/'verification.json').write_text(json.dumps(verification, indent=2)+'\n')
    if not verification['passed']:
        raise ValueError('Independent numerical checks failed')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--r0', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.r0, args.runtime, args.output)
