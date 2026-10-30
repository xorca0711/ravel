"""F1: descriptive weighting audit of frozen E2 membership/effects; no refit."""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path('analysis/research/runs/DY1_P02_reference_benchmark_v1')
KEYS = ['mapping_rule', 'distance_subset']


def attach_effects(membership, rna, atac):
    if membership.duplicated(KEYS + ['peak_id']).any():
        raise ValueError('Repeated region within mapping/subset')
    for data in (rna, atac):
        if data.feature_id.duplicated().any() or not np.isfinite(data.mean_delta).all():
            raise ValueError('Nonunique or nonfinite effects')
    rows = membership.merge(rna.rename(columns={'feature_id': 'gene_id', 'mean_delta': 'rna_delta'}), on='gene_id', validate='many_to_one')
    rows = rows.merge(atac.rename(columns={'feature_id': 'peak_id', 'mean_delta': 'atac_delta'}), on='peak_id', validate='many_to_one')
    if len(rows) != len(membership):
        raise ValueError('Frozen membership lost at effect join')
    rows['rna_sign'] = np.sign(rows.rna_delta).astype(int)
    rows['atac_sign'] = np.sign(rows.atac_delta).astype(int)
    prod = rows.rna_sign * rows.atac_sign
    rows['direction_class'] = np.where(prod > 0, 'same', np.where(prod < 0, 'opposite', 'zero'))
    return rows


def aggregate(rows):
    data = rows.assign(same=rows.direction_class.eq('same').astype(int),
                       opposite=rows.direction_class.eq('opposite').astype(int),
                       zero=rows.direction_class.eq('zero').astype(int),
                       positive=rows.atac_sign.gt(0).astype(int), negative=rows.atac_sign.lt(0).astype(int),
                       atac_zero=rows.atac_sign.eq(0).astype(int))
    genes = data.groupby(KEYS + ['gene_id'], sort=True).agg(
        n_regions=('peak_id', 'size'), same=('same', 'sum'), opposite=('opposite', 'sum'),
        zero=('zero', 'sum'), atac_positive=('positive', 'sum'), atac_negative=('negative', 'sum'),
        atac_zero=('atac_zero', 'sum'), rna_sign=('rna_sign', 'first')).reset_index()
    for c in ['same', 'opposite', 'zero']:
        genes[c + '_fraction'] = genes[c] / genes.n_regions
    genes['mixed_atac_directions'] = (genes.atac_positive > 0) & (genes.atac_negative > 0)
    summaries = []
    for key, g in genes.groupby(KEYS, sort=True):
        total = int(g.n_regions.sum())
        summaries.append(dict(zip(KEYS, key), pair_rows=total, genes=len(g),
            same=int(g.same.sum()), opposite=int(g.opposite.sum()), zero=int(g.zero.sum()),
            pair_weighted_same=float(g.same.sum()/total), equal_gene_same=float(g.same_fraction.mean()),
            equal_gene_minus_pair_weighted=float(g.same_fraction.mean()-g.same.sum()/total),
            mixed_atac_genes=int(g.mixed_atac_directions.sum()),
            mixed_atac_gene_fraction=float(g.mixed_atac_directions.mean()),
            regions_per_gene_min=int(g.n_regions.min()), regions_per_gene_median=float(g.n_regions.median()),
            regions_per_gene_max=int(g.n_regions.max()),
            single_region_genes=int((g.n_regions == 1).sum())))
    return genes, pd.DataFrame(summaries)


def common_mapping(rows):
    reports, members = [], []
    for subset, d in rows.groupby('distance_subset', sort=True):
        a = d[d.mapping_rule == 'author_ensembl']
        b = d[d.mapping_rule == 'author_nearest_tss_symbol']
        c = a[['peak_id','gene_id','direction_class']].merge(
            b[['peak_id','gene_id','direction_class']], on='peak_id', validate='one_to_one', suffixes=('_ensembl','_nearest'))
        c['distance_subset'] = subset
        c['same_gene'] = c.gene_id_ensembl == c.gene_id_nearest
        c['same_class'] = c.direction_class_ensembl == c.direction_class_nearest
        members.append(c)
        for (same_gene, left, right), g in c.groupby(['same_gene','direction_class_ensembl','direction_class_nearest'], sort=True):
            reports.append(dict(distance_subset=subset, common_regions=len(c), ensembl_only_regions=len(a)-len(c),
                nearest_only_regions=len(b)-len(c), same_gene=bool(same_gene),
                ensembl_class=left, nearest_class=right, regions=len(g)))
    return pd.concat(members, ignore_index=True), pd.DataFrame(reports)


def scalar_verify(rows, genes, summary, common):
    """Independently count using dictionaries and scalar comparisons, not groupby."""
    buckets = defaultdict(list)
    peak_maps = defaultdict(dict)
    for r in rows.itertuples(index=False):
        cls = 'zero' if r.rna_delta == 0 or r.atac_delta == 0 else ('same' if (r.rna_delta > 0) == (r.atac_delta > 0) else 'opposite')
        buckets[(r.mapping_rule, r.distance_subset, r.gene_id)].append((cls, r.atac_delta))
        peak_maps[(r.mapping_rule, r.distance_subset)][r.peak_id] = (r.gene_id, cls)
    checks = 0
    for r in genes.itertuples(index=False):
        v = buckets[(r.mapping_rule, r.distance_subset, r.gene_id)]
        expected = [len(v), sum(c == 'same' for c,a in v), sum(c == 'opposite' for c,a in v), sum(c == 'zero' for c,a in v),
                    sum(a > 0 for c,a in v), sum(a < 0 for c,a in v), sum(a == 0 for c,a in v)]
        actual = [r.n_regions,r.same,r.opposite,r.zero,r.atac_positive,r.atac_negative,r.atac_zero]
        assert expected == actual
        checks += len(actual)
    for r in summary.itertuples(index=False):
        groups = [v for k,v in buckets.items() if k[:2] == (r.mapping_rule,r.distance_subset)]
        same = [sum(c == 'same' for c,a in v) for v in groups]
        pair = sum(same) / sum(map(len, groups))
        equal = math.fsum(n/len(v) for n,v in zip(same, groups)) / len(groups)
        assert math.isclose(pair, r.pair_weighted_same, abs_tol=1e-13)
        assert math.isclose(equal, r.equal_gene_same, abs_tol=1e-13)
        checks += 2
    for r in common.itertuples(index=False):
        a = peak_maps[('author_ensembl',r.distance_subset)][r.peak_id]
        b = peak_maps[('author_nearest_tss_symbol',r.distance_subset)][r.peak_id]
        assert (a[0] == b[0]) == r.same_gene and (a[1] == b[1]) == r.same_class
        checks += 2
    for subset in rows.distance_subset.unique():
        a = peak_maps[('author_ensembl',subset)]
        b = peak_maps[('author_nearest_tss_symbol',subset)]
        assert len(a.keys() & b.keys()) == int((common.distance_subset == subset).sum())
        checks += 1
    return checks


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    read = lambda n: pd.read_csv(BASE/n, sep='\t')
    def effects(name):
        d = pd.read_csv(BASE/name, sep='\t', usecols=['feature_id','offset','mean_delta'])
        return d[d.offset == 1][['feature_id','mean_delta']]
    rows = attach_effects(read('mapping_membership.tsv.gz'), effects('rna_descriptive_effects.tsv.gz'), effects('atac_descriptive_effects.tsv.gz'))
    genes, summary = aggregate(rows)
    common, comparison = common_mapping(rows)
    checks = scalar_verify(rows, genes, summary, common)
    saved = read('mapping_sensitivity.tsv'); saved = saved[saved.offset == 1]
    eligibility = read('feature_eligibility.tsv').set_index('assay')
    coverage = summary[KEYS+['pair_rows','genes']].merge(saved[KEYS+['candidate_rows','unique_regions','same_nonzero_sign','opposite_nonzero_sign','one_or_both_zero']], on=KEYS, validate='one_to_one')
    for r in summary.itertuples(index=False):
        old = saved[(saved.mapping_rule == r.mapping_rule) & (saved.distance_subset == r.distance_subset)].iloc[0]
        assert (r.pair_rows,r.genes,r.same,r.opposite,r.zero) == (old.pair_rows,old.unique_genes,old.same_nonzero_sign,old.opposite_nonzero_sign,old.one_or_both_zero)
        checks += 5
    coverage['eligible_atac_regions'] = int(eligibility.loc['ATAC','eligible_features'])
    coverage['eligible_rna_genes'] = int(eligibility.loc['RNA','eligible_features'])
    coverage['mapped_fraction_of_eligible_atac'] = coverage.unique_regions / coverage.eligible_atac_regions
    coverage['mapped_fraction_of_eligible_rna'] = coverage.genes / coverage.eligible_rna_genes
    coverage['eligible_pair_fraction_of_candidates'] = coverage.pair_rows / coverage.candidate_rows
    for n, t in [('gene_representation.tsv.gz', genes), ('weighting_summary.tsv', summary),
                 ('common_mapping_membership.tsv.gz', common), ('common_mapping_contingency.tsv', comparison), ('annotation_coverage.tsv', coverage)]:
        t.to_csv(out/n, sep='\t', index=False, lineterminator='\n', compression={'method':'gzip','mtime':0} if n.endswith('.gz') else None)
    fig, axes = plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
    labels = [('Ensembl' if r.mapping_rule == 'author_ensembl' else 'Nearest symbol')+'\n'+('all annotated' if r.distance_subset == 'all_author_annotated' else 'nearest TSS <=2 kb') for r in summary.itertuples()]
    x = np.arange(len(summary))
    axes[0].bar(x-.18,summary.pair_weighted_same,.36,label='Equal region weight')
    axes[0].bar(x+.18,summary.equal_gene_same,.36,label='Equal gene weight')
    axes[0].set(xticks=x,xticklabels=labels,ylim=(0,1),ylabel='Fraction agreeing with RNA direction')
    axes[0].legend(fontsize=8)
    for key,g in genes.groupby(KEYS,sort=True):
        counts = g.n_regions.value_counts().sort_index()
        axes[1].step(counts.index,counts.cumsum()/counts.sum(),where='post',label=('Ensembl' if key[0]=='author_ensembl' else 'Nearest')+(' all' if key[1]=='all_author_annotated' else ' <=2 kb'))
    axes[1].set(xscale='log',xlabel='Mapped regions per gene (log scale)',ylabel='Cumulative fraction of genes',ylim=(0,1.02))
    axes[1].legend(fontsize=8)
    fig.suptitle('Frozen external WT benchmark: representation audit, offset 1\nDependent mapped rows; descriptive fractions, no independent-trial inference',fontsize=11)
    fig.savefig(out/'representation_audit.png',dpi=150);plt.close(fig)
    (out/'verification.json').write_text(json.dumps({'status':'passed','scalar_and_frozen_parity_checks':checks},indent=2)+'\n')
    (out/'summary.json').write_text(json.dumps({'analysis_id':'DY1-P02.representation_audit_v1','offset':1,'denominator':'All mapped rows per gene, including zero directions; equal mean across represented genes','precision':'No gene/region independent-trial intervals','distance_limit':'Source nearest TSS, not necessarily the Ensembl-assigned gene','scientific_acceptance':'not_assessed'},indent=2)+'\n')


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
