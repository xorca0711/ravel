"""Independent scalar arithmetic and membership checks; no biological replication."""
import math
from pathlib import Path
import statistics
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from scipy.spatial.distance import pdist


def scalar_test(a, b):
    na, nb = len(a), len(b)
    ranks = rankdata(np.concatenate([a,b]))
    u = float(sum(ranks[:na]) - na*(na+1)/2)
    _, counts = np.unique(np.concatenate([a,b]), return_counts=True)
    n = na+nb
    variance = na*nb/12 * ((n+1)-sum(int(t)**3-int(t) for t in counts)/(n*(n-1)))
    z = max(0, abs(u-na*nb/2)-.5)/math.sqrt(variance) if variance > 0 else 0
    p = min(1.0, math.erfc(z/math.sqrt(2)))
    pooled = ((na-1)*statistics.variance(a)+(nb-1)*statistics.variance(b))/(n-2)
    d = (statistics.fmean(a)-statistics.fmean(b))/math.sqrt(pooled) if pooled > 0 else float('nan')
    return d, u, p


def bh(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    result = np.empty(len(values))
    running = 1.0
    for rank in range(len(values), 0, -1):
        index = order[rank-1]
        running = min(running, values[index]*len(values)/rank)
        result[index] = running
    return result


def verify(source: Path, output: Path):
    raw = pd.read_csv(source/'reactions.tsv', sep='\t', index_col=0)
    cells = pd.read_csv(source/'cell_metadata.csv', index_col=0)
    positive = cells.cell_type.eq('Th17p').to_numpy()
    direct = pd.read_csv(output/'reaction_statistics.tsv', sep='\t', index_col=0)
    meta = pd.read_csv(output/'metareaction_statistics.tsv', sep='\t', index_col=0)
    members = pd.read_csv(output/'metareaction_membership.tsv', sep='\t')
    expanded = pd.read_csv(output/'expanded_metareaction_statistics.tsv', sep='\t', index_col=0)
    pathways = pd.read_csv(output/'pathway_summary.tsv', sep='\t')
    frozen = np.load(output/'tested_scores.npz', allow_pickle=False)
    assert list(frozen['cell_ids']) == list(cells.index)
    assert list(frozen['single_ids']) == list(direct.index)
    assert list(frozen['meta_ids']) == list(meta.index)
    transform_residual = 0.0
    translation_offsets = {'single': [], 'meta': []}
    rounding_tie_differences = {'single': 0, 'meta': 0}
    maximum = dict(d=0.0, U=0.0, p=0.0, q=0.0, within_group_distance=0.0)
    passed = True
    for level, table in [('single',direct), ('meta',meta)]:
        probabilities = []
        for position, (feature, row) in enumerate(table.iterrows()):
            if level == 'single':
                penalties = raw.loc[feature].to_numpy()
            else:
                ids = members.loc[members.metareaction_id.eq(feature), 'reaction_id']
                penalties = np.mean(raw.loc[ids].to_numpy(), axis=0)
            # Verify transformation up to its common shift, then test the exact
            # saved float64 scores; translation can collapse floating-point ties.
            unshifted = np.array([-math.log1p(float(x)) for x in penalties])
            scores = frozen['single_scores' if level == 'single' else 'meta_scores'][position]
            offset = scores - unshifted
            residual = float(np.ptp(offset))
            transform_residual = max(transform_residual, residual)
            translation_offsets[level].append(float(offset[0]))
            passed = passed and residual <= 1e-11
            original_u = scalar_test(unshifted[positive].tolist(),unshifted[~positive].tolist())[1]
            actual_u = scalar_test(scores[positive].tolist(),scores[~positive].tolist())[1]
            rounding_tie_differences[level] += int(original_u != actual_u)
            d,u,p = scalar_test(scores[positive].tolist(), scores[~positive].tolist())
            probabilities.append(p)
            for name,x,y in [('d',d,row.cohens_d),('U',u,row.U),('p',p,row.p_source)]:
                if math.isnan(x) and math.isnan(y):continue
                maximum[name] = max(maximum[name], abs(x-y))
                passed = passed and bool(np.isclose(x,y,rtol=1e-9,atol=1e-11, equal_nan=True))
        delta = float(np.max(np.abs(bh(probabilities)-table.q_source.to_numpy())))
        maximum['q'] = max(maximum['q'], delta)
        passed = passed and delta <= 1e-10
    for offsets in translation_offsets.values():
        passed = passed and np.ptp(offsets) <= 1e-11
    for _, group in members.groupby('metareaction_id'):
        if len(group)>1:
            ranks=rankdata(raw.loc[group.reaction_id].to_numpy(),axis=1)
            distance=float(np.max(pdist(ranks,metric='correlation')))
            maximum['within_group_distance']=max(maximum['within_group_distance'],distance)
            passed=passed and distance <= .020000000001
    # Expansion must copy one group estimate; reaction multiplicity is not extra tests.
    for feature,row in expanded.iterrows():
        reference=meta.loc[row.metareaction_id]
        passed=passed and bool(np.allclose(row[['cohens_d','q_source']].to_numpy(dtype=float),reference[['cohens_d','q_source']].to_numpy(dtype=float),rtol=1e-12,atol=1e-12,equal_nan=True))
    for _,row in pathways.iterrows():
        unique=expanded[(expanded.subsystem==row.subsystem)&expanded.core].drop_duplicates('metareaction_id')
        passed=passed and len(unique)==row.metareaction_count
        passed=passed and int(((unique.q_source<.1)&(unique.cohens_d>0)).sum())==row.positive_q_lt_0_1
        passed=passed and int(((unique.q_source<.1)&(unique.cohens_d<0)).sum())==row.negative_q_lt_0_1
    expected=set(raw.index[np.ptp(-np.log1p(raw.to_numpy()),axis=1)>=1e-3])
    passed=passed and set(direct.index)==expected and members.reaction_id.is_unique
    return {'passed':bool(passed),'single_features_checked':len(direct),'meta_features_checked':len(meta),
            'expanded_rows_checked':len(expanded),'max_absolute_differences':maximum, 'max_transform_residual':transform_residual, 'unshifted_rounding_tie_differences':rounding_tie_differences,
            'checks':['independent transform and common-shift consistency','scalar pooled variance and effect direction','manual rank-sum U, tie/continuity correction and normal tail','independent BH ordering','all complete-link groups satisfy the declared distance cut','group-to-member expansion','unique-group pathway counts','retained reaction identities'],
            'limits':'Same-data numerical verification, not independent biological replication. Complete-link cut checked within groups; it does not recover unknown manuscript curation or historical software.'}
