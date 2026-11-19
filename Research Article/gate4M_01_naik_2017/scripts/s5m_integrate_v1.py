"""Exact-ID integration of immutable finite-source RNA and ATAC endpoints."""
import argparse
from collections import Counter
import gzip
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import time

import numpy as np
import pandas as pd

from s5m_math_v1 import average_ranks, moments

ANCHORS = [('Aim2', 'ENSMUSG00000037860.15'), ('Casp1', 'ENSMUSG00000025888.5'),
           ('Il1b', 'ENSMUSG00000027398.13'), ('Il1r1', 'ENSMUSG00000026072.12'), ('Il18', 'ENSMUSG00000039217.12')]
GSMS = ['GSM' + str(i) for i in range(2441001, 2441009)]
CHROMS = ['chr' + str(i) for i in range(1, 20)] + ['chrX']
MEASUREMENTS = [
    ('S2_D6', 'D6', 's2__D6_log2_effect_{norm}', 'S2 D6'),
    ('S2_D30', 'D30', 's2__D30_log2_effect_{norm}', 'S2 D30 (same B0 libraries)'),
    ('S4_B0_primary', 'D30', 's4__B0_log2_effect_{norm}', 'S4 B0 primary'),
    ('S4_W6_post', 'D30', 's4__W6_log2_effect_{norm}', 'S4 W6 unadjusted'),
    ('S4_W12_post', 'D30', 's4__W12_log2_effect_{norm}', 'S4 W12 unadjusted'),
    ('S4_W6_primary', 'D30', 's4__W6_adjusted_{norm}', 'S4 W6 adjusted primary'),
    ('S4_W12_primary', 'D30', 's4__W12_adjusted_{norm}', 'S4 W12 adjusted primary'),
    ('S4B_B0_c2_h2', 'D30', 's4b__B0_c2_h2_{norm}', 'S4B B0 C2/H2 reference'),
    ('S4B_W6_c2_h2', 'D30', 's4b__W6_c2_h2_{norm}', 'S4B W6 adjusted C2/H2'),
    ('S4B_W12_c2_h2', 'D30', 's4b__W12_c2_h2_{norm}', 'S4B W12 adjusted C2/H2'),
    ('S4B_B0_c1_h1', 'D30', 's4b__B0_c1_h1_{norm}', 'S4B B0 C1/H1 reference'),
    ('S4B_W6_c1_h1', 'D30', 's4b__W6_c1_h1_{norm}', 'S4B W6 adjusted C1/H1'),
    ('S4B_W12_c1_h1', 'D30', 's4b__W12_c1_h1_{norm}', 'S4B W12 adjusted C1/H1')]


def save(path, value): path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
def read(path): return pd.read_csv(path, sep='\t', dtype=str, keep_default_na=False)
def tsv(path, frame):
    if path.name.endswith('.gz'):
        with path.open('wb') as raw:
            with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as compressed:
                with io.TextIOWrapper(compressed, encoding='utf-8', newline='') as handle:
                    frame.to_csv(handle, sep='\t', index=False, na_rep='NA', float_format='%.17g', lineterminator='\n')
    else: frame.to_csv(path, sep='\t', index=False, na_rep='NA', float_format='%.17g', lineterminator='\n')


def numbers(column): return np.fromiter((float(v) for v in column), dtype=float, count=len(column))
def finite_source(value):
    if pd.isna(value) or value in ['', 'NA']: return False
    return bool(np.isfinite(float(value)))
def boolean(value):
    if value in ['True', True]: return True
    if value in ['False', False]: return False
    raise ValueError('unexpected source boolean: ' + str(value))


def annotations(gtf):
    result = {}
    with gzip.open(gtf, 'rt') as handle:
        for line in handle:
            if line.startswith('#'): continue
            f = line.rstrip().split('\t')
            if len(f) != 9 or f[2] != 'gene': continue
            a = dict(re.findall(r'(\w+) "([^"]*)";', f[8])); gene = a['gene_id']; assert gene not in result
            result[gene] = dict(gene_name=a['gene_name'], gene_type=a['gene_type'], chrom=f[0])
    return result


def prepare(s2, s4, s4b, mapping, effects, annotation):
    for f in [s2, s4, s4b]: assert not f.gene_id.duplicated().any()
    assert not mapping.duplicated(['gene_id', 'flank']).any() and not effects.window_id.duplicated().any()
    assert set(mapping.flank) == {'1000', '2000'}
    genes = sorted(set(s2.gene_id) | set(s4.gene_id) | set(s4b.gene_id) | set(mapping.gene_id))
    joined = pd.DataFrame({'gene_id': genes})
    for prefix, source in [('s2', s2), ('s4', s4), ('s4b', s4b)]:
        renamed = source.rename(columns={c: prefix + '__' + c for c in source.columns if c != 'gene_id'})
        joined = joined.merge(renamed, on='gene_id', how='left', validate='one_to_one', sort=False)
    by_id = joined.set_index('gene_id'); membership = {p: set(f.gene_id) for p, f in [('s2', s2), ('s4', s4), ('s4b', s4b)]}
    maps = {(r.gene_id, r.flank): r._asdict() for r in mapping.itertuples(index=False)}
    lookup = effects.set_index('window_id'); feature_rows = []; meta = []
    fields = [template.format(norm=norm) for unused, phase, template, label in MEASUREMENTS for norm in ['mor', 'total']]
    warning_zero = [c for c in joined.columns if '__' in c and 'zero' in c]
    warning_low = [c for c in joined.columns if '__' in c and ('low' in c or 'regularization_sensitive' in c)]
    def warning(row, columns):
        for c in columns:
            v = row[c]
            if pd.isna(v) or v in ['', 'NA', 'False']: continue
            if v == 'True' or float(v) != 0: return True
        return False
    for gene in genes:
        a = annotation.get(gene); row = by_id.loc[gene]; assayed = (gene, '1000') in maps
        assert assayed == ((gene, '2000') in maps)
        present = {prefix: gene in ids for prefix, ids in membership.items()}
        finite = all(present.values()) and all(finite_source(row[c]) for c in fields)
        if assayed:
            m = maps[(gene, '1000')]; assert a is not None and a['gene_type'] == 'protein_coding' and a['chrom'] in CHROMS
            assert m['gene_name'] == a['gene_name'] and m['anchor_id'] == maps[(gene, '2000')]['anchor_id']
            status, anchor = 'assayed_TSS_proxy', m['anchor_id']
        else:
            status = 'unassayed_annotation' if a is None else ('unassayed_non_protein_coding' if a['gene_type'] != 'protein_coding' else 'unassayed_chromosome')
            if a and a['gene_type'] == 'protein_coding' and a['chrom'] in CHROMS: raise ValueError('eligible M9 gene missing from frozen S3 mapping')
            anchor = 'NA'
        qualified = False
        if all(present.values()):
            s2_both = boolean(row['s2__eligible_both']); s4_all = boolean(row['s4__all_three_qualified'])
            assert s2_both == (boolean(row['s2__D6_qualified_cpm']) and boolean(row['s2__D30_qualified_cpm']))
            assert s4_all == all(boolean(row['s4__' + phase + '_qualified_cpm']) for phase in ['B0', 'W6', 'W12'])
            assert s4_all == boolean(row['s4b__all_three_qualified'])
            qualified = s2_both and s4_all
        all_mapped = assayed and finite; primary = all_mapped and qualified
        reasons = ([] if assayed else [status]) + ['missing_' + p for p, ok in present.items() if not ok]
        if all(present.values()) and not finite: reasons.append('nonfinite_required_rna')
        primary_reasons = reasons + (['frozen_expression_not_qualified'] if all(present.values()) and not qualified else [])
        mrow = dict(gene_id=gene, annotation_present=a is not None, gene_name=a['gene_name'] if a else 'NA', gene_type=a['gene_type'] if a else 'NA',
                    chrom=a['chrom'] if a else 'NA', atac_assayed=assayed, atac_status=status, anchor_id=anchor,
                    finite_required_rna=finite, frozen_expression_qualified=qualified, universe_primary=primary, universe_all_mapped=all_mapped,
                    rna_any_zero_flag=warning(row, warning_zero), rna_any_low_or_regularization_flag=warning(row, warning_low),
                    all_mapped_eligibility_reason='|'.join(reasons) if reasons else 'eligible', primary_eligibility_reason='|'.join(primary_reasons) if primary_reasons else 'eligible')
        mrow.update({prefix + '_present': value for prefix, value in present.items()})
        for flank in ['1000', '2000']:
            key = maps[(gene, flank)]['window_id'] if assayed else 'NA'; mrow['window_id_' + flank] = key
            result = dict(gene_id=gene, flank=flank, atac_status=status)
            if assayed:
                source = lookup.loc[key]; assert source.flank == flank and source.anchor_id == anchor
                result.update({'atac__' + c: source[c] for c in lookup.columns}); result['atac__window_id'] = key
                for gsm in GSMS: result[gsm + '__zero_mean'] = float(source[gsm + '__mean']) == 0
                for phase, group in [('D6', GSMS[:4]), ('D30', GSMS[4:])]:
                    zeros = [result[g + '__zero_mean'] for g in group]
                    result[phase + '_any_zero_means'] = any(zeros); result[phase + '_all_zero_means'] = all(zeros)
            feature_rows.append(result)
        meta.append(mrow)
    metadata = pd.DataFrame(meta)
    for universe in ['primary', 'all_mapped']:
        chosen = metadata['universe_' + universe]; counts = Counter(metadata.loc[chosen, 'anchor_id'])
        metadata['anchor_multiplicity_' + universe] = [counts[a] if flag else np.nan for a, flag in zip(metadata.anchor_id, chosen)]
        metadata['weight_' + universe] = [1 / counts[a] if flag else np.nan for a, flag in zip(metadata.anchor_id, chosen)]
    return metadata.merge(joined, on='gene_id', validate='one_to_one', sort=False), pd.DataFrame(feature_rows)


def calculate(joined, atac):
    results, identities = [], []; summary = {'universes': {}, 'finite_feature_description_only': True, 'independent_biological_replication': False}
    for universe in ['primary', 'all_mapped']:
        subset = joined.loc[joined['universe_' + universe]].set_index('gene_id'); ids = subset.index
        weights = subset['weight_' + universe].to_numpy(float); anchor_n = subset.anchor_id.nunique()
        block = dict(genes=len(subset), unique_anchors=anchor_n, additional_gene_mappings=len(subset)-anchor_n,
                     inverse_multiplicity_weight_sum=float(weights.sum()), rna_any_zero_genes=int(subset.rna_any_zero_flag.sum()),
                     rna_any_low_or_regularization_genes=int(subset.rna_any_low_or_regularization_flag.sum()), atac_zero_flags={})
        for flank in ['1000', '2000']:
            features = atac.loc[atac.flank == flank].set_index('gene_id').loc[ids]
            for phase in ['D6', 'D30']:
                block['atac_zero_flags'][flank + '_' + phase] = {'any_zero_mean_genes': int(features[phase + '_any_zero_means'].sum()), 'all_zero_mean_genes': int(features[phase + '_all_zero_means'].sum())}
            for norm in ['mor', 'total']:
                for name, phase, template, label in MEASUREMENTS:
                    x, y = numbers(features['atac__' + phase + '_delta']), numbers(subset[template.format(norm=norm)])
                    for statistic in ['pearson', 'spearman', 'inverse_anchor_pearson']:
                        xx, yy = (average_ranks(x), average_ranks(y)) if statistic == 'spearman' else (x, y)
                        w = weights if statistic == 'inverse_anchor_pearson' else None
                        result = dict(universe=universe, flank=int(flank), normalization=norm, measurement=name, label=label,
                                      atac_time=phase, rna_field=template.format(norm=norm), statistic=statistic, genes=len(ids), unique_anchors=anchor_n,
                                      weight_sum=float(weights.sum()) if w is not None else len(ids))
                        result.update(moments(xx, yy, w)); results.append(result)
                x = numbers(features['atac__D30_delta'])
                for reference in ['primary', 'c2_h2', 'c1_h1']:
                    baseline_field = 's4__B0_log2_effect_' + norm if reference == 'primary' else 's4b__B0_' + reference + '_' + norm
                    baseline = numbers(subset[baseline_field])
                    for phase in ['W6', 'W12']:
                        post = numbers(subset['s4__' + phase + '_log2_effect_' + norm])
                        adjusted_field = 's4__' + phase + '_adjusted_' + norm if reference == 'primary' else 's4b__' + phase + '_' + reference + '_' + norm
                        adjusted = numbers(subset[adjusted_field]); assert np.allclose(adjusted, post-baseline, rtol=1e-10, atol=1e-10)
                        for weighting in ['ordinary', 'inverse_anchor']:
                            w = weights if weighting == 'inverse_anchor' else None
                            cb, cp, ca = [moments(x, y, w)['covariance'] for y in [baseline, post, adjusted]]
                            difference = cp-cb if cp is not None and cb is not None else None
                            error = abs(ca-difference) / max(1, abs(ca), abs(difference)) if ca is not None and difference is not None else None
                            assert error is None or error <= 1e-10
                            identities.append(dict(universe=universe, flank=int(flank), normalization=norm, reference=reference, wound_time=phase,
                                                   weighting=weighting, genes=len(ids), unique_anchors=anchor_n, covariance_baseline=cb, covariance_post=cp,
                                                   covariance_adjusted=ca, post_minus_baseline_covariance=difference, scaled_identity_error=error,
                                                   reason='defined' if error is not None else 'fewer_than_two_features'))
        summary['universes'][universe] = block
    summary['gene_records'] = len(joined); summary['atac_status_counts'] = {str(k): int(v) for k, v in joined.atac_status.value_counts().items()}
    return pd.DataFrame(results), pd.DataFrame(identities), summary


def run(contract_path, output):
    started = time.monotonic(); root = Path(__file__).resolve().parents[3]
    c = json.loads(contract_path.read_text(encoding='utf-8-sig')); inputs = {Path(x['path']).name: root / x['path'] for x in c['inputs']}
    annotation = annotations(inputs['gencode.vM9.annotation.gtf.gz'])
    for name, gene in ANCHORS: assert annotation[gene]['gene_name'] == name
    joined, atac = prepare(read(inputs['gene_effects.tsv']), read(inputs['gene_effects.tsv.gz']), read(inputs['reference_effects.tsv.gz']),
                           read(inputs['gene_window_map.tsv.gz']), read(inputs['window_effects.tsv.gz']), annotation)
    tsv(output / 'gene_join.tsv.gz', joined); tsv(output / 'gene_atac.tsv.gz', atac)
    associations, covariance, summary = calculate(joined, atac); summary['analysis_id'] = c['analysis_id']
    tsv(output / 'association_results.tsv', associations); tsv(output / 'covariance_identity.tsv', covariance); save(output / 'universe_summary.json', summary)
    manifest = []; anchors = []
    for slot, (name, gene) in enumerate(ANCHORS, 1):
        gene_rows = joined.loc[joined.gene_id == gene]; present = len(gene_rows) == 1
        item = dict(plot_slot=slot, gene_id=gene, gene_name=name, selection='published pathway anchor; exposed', source_record_present=present)
        if present:
            row = gene_rows.iloc[0]; item.update(atac_status=row.atac_status, universe_primary=bool(row.universe_primary), universe_all_mapped=bool(row.universe_all_mapped),
                                               rna_any_zero_flag=bool(row.rna_any_zero_flag), rna_any_low_or_regularization_flag=bool(row.rna_any_low_or_regularization_flag),
                                               primary_eligibility_reason=row.primary_eligibility_reason, all_mapped_eligibility_reason=row.all_mapped_eligibility_reason)
            for unused, feature in atac.loc[atac.gene_id == gene].iterrows():
                result = row.to_dict(); result.update(feature.to_dict()); result['plot_slot'] = slot; anchors.append(result)
        else: item.update(atac_status='unassayed_no_source_record', universe_primary=False, universe_all_mapped=False)
        manifest.append(item)
    save(output / 'anchor_manifest.json', manifest); anchor_values = pd.DataFrame(anchors); tsv(output / 'anchor_values.tsv', anchor_values)
    from s5m_plot_v1 import plot
    plot(output, associations, manifest, anchor_values, summary)
    import matplotlib
    save(output / 'runtime.json', dict(python=sys.version, numpy=np.__version__, pandas=pd.__version__, matplotlib=matplotlib.__version__,
                                     elapsed_seconds_before_verification=time.monotonic()-started, source_biological_analyses_rerun=False, stochastic_steps='none'))
    subprocess.run([sys.executable, str(Path(__file__).with_name('s5m_verify_v1.py')), '--contract', str(contract_path.resolve()), '--run-dir', str(output.resolve())], check=True)
    print(json.dumps({'analysis_id': c['analysis_id'], 'status': 'completed_finite_feature_description', 'elapsed_seconds': time.monotonic()-started,
                      'association_rows': len(associations), 'covariance_rows': len(covariance)}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--contract', type=Path, required=True); parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); run(args.contract, args.output)
