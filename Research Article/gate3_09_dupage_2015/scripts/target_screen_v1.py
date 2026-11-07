"""Exposed, fixed-universe candidate ordering; no population tests or target claims."""
import argparse
import csv
import json
from pathlib import Path

import numpy as np

BASE = Path('analysis/research/runs')
S0 = BASE / 'dupage_s0_qualification_v1'
S1 = BASE / 'dupage_s1_reconstruction_v1'
S2 = BASE / 'dupage_s2_state_contrast_v1'
S3 = BASE / 'dupage_s3_regulatory_context_v1'
GROUPS = ['HET_hi', 'HET_lo', 'KO_hi', 'KO_lo']
ANCHORS = 'Pde3b Tcf7 Lef1 Ezh2 Foxp3 Il10 Ctla4 Il2 Il2ra Tgfb1 Bcl2 Bcl2l11 Bach2 Klf2 Prdm1 Irf4 Ccr7 S1pr1 Areg'.split()


def read(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def write(path, rows, fields=None):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]), delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)


def estimates(raw, groups, pseudo=1, omit=None):
    means = np.array([
        np.log2(raw[:, [j for j, group in enumerate(groups) if group == name and j != omit]] + pseudo).mean(axis=1)
        for name in GROUPS
    ]).T
    high = means[:, 2] - means[:, 0]
    low = means[:, 3] - means[:, 1]
    return means, high, low, low - high


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    out = parser.parse_args().output
    manifest = [row for row in read(S0 / 'sample_manifest.tsv') if row['retained'] == 'True']
    groups = [row['genotype'] + '_' + row['state'] for row in manifest]
    source = {row['gene_id']: row for row in read(S0 / 'common_fpkm.tsv')}
    original = read(S1 / 'gene_contrasts.tsv')
    prior = {row['gene_id']: row for row in read(S2 / 'interaction.tsv')}
    chrom = {row['gene_id']: row for row in read(S3 / 'gene_context.tsv')}
    assert len(original) == len(prior) == len(chrom) == 11614
    assert len(manifest) == 11 and {g: groups.count(g) for g in GROUPS} == dict(zip(GROUPS, [2, 3, 3, 3]))
    assert len({row['gene_id'] for row in original}) == len(original)
    raw = np.array([[float(source[row['gene_id']][sample['gsm'] + '_FPKM']) for sample in manifest] for row in original])
    assert np.isfinite(raw).all() and (raw >= 0).all()
    primary = estimates(raw, groups)
    configurations = [('primary', primary)]
    configurations += [('omit_' + sample['gsm'], estimates(raw, groups, omit=j)) for j, sample in enumerate(manifest)]
    configurations += [('pseudocount_' + str(p), estimates(raw, groups, pseudo=p)) for p in [.5, 2]]
    low_matrix = np.array([result[2] for _, result in configurations])
    int_matrix = np.array([result[3] for _, result in configurations])
    assert np.isfinite(low_matrix).all() and np.isfinite(int_matrix).all()
    assert np.allclose(primary[1], [float(row['delta_high']) for row in original], rtol=0, atol=1e-12)
    assert np.allclose(primary[2], [float(row['delta_low']) for row in original], rtol=0, atol=1e-12)
    assert np.allclose(primary[3], [float(prior[row['gene_id']]['interaction']) for row in original], rtol=0, atol=1e-12)
    rows = []
    for j, old in enumerate(original):
        gene = old['gene_id']
        high, low, interaction = [float(primary[k][j]) for k in [1, 2, 3]]
        low_bound = float((np.sign(low) * low_matrix[:, j]).min())
        int_bound = float((np.sign(interaction) * int_matrix[:, j]).min())
        low_stable = low != 0 and low_bound > 0
        int_stable = interaction != 0 and int_bound > 0
        state = low_stable and int_stable and np.sign(low) == np.sign(interaction) and abs(low) > abs(high)
        rows.append({
            'gene_id': gene, 'locus': old['locus'],
            **{name + '_mean_log2_fpkm1': float(primary[0][j, k]) for k, name in enumerate(GROUPS)},
            'delta_high': high, 'delta_low': low, 'interaction': interaction,
            'activation_HET': old['activation_HET'], 'activation_KO': old['activation_KO'],
            'low_sensitivity_min': float(low_matrix[:, j].min()), 'low_sensitivity_max': float(low_matrix[:, j].max()),
            'interaction_sensitivity_min': float(int_matrix[:, j].min()), 'interaction_sensitivity_max': float(int_matrix[:, j].max()),
            'low_sign_oriented_min': low_bound, 'interaction_sign_oriented_min': int_bound,
            'low_sign_stable': bool(low_stable), 'interaction_sign_stable': bool(int_stable),
            'state_prioritized': bool(state),
            'low_track_rank': '', 'state_track_rank': '',
            'chromatin_class': chrom[gene]['chromatin_class'],
            'arvey_activation_delta_median': chrom[gene]['arvey_activation_delta_median'],
            'domain_count': chrom[gene]['domain_count'],
        })
    by_gene = {row['gene_id']: row for row in rows}
    frontier, counts = [], {}
    for track in ['low', 'state']:
        for direction, sign in [('positive', 1), ('negative', -1)]:
            eligible = [r for r in rows if np.sign(r['delta_low']) == sign and r['low_sign_stable'] and (track == 'low' or r['state_prioritized'])]
            if track == 'low':
                eligible.sort(key=lambda r: (-r['low_sign_oriented_min'], r['gene_id']))
            else:
                eligible.sort(key=lambda r: (-r['interaction_sign_oriented_min'], -r['low_sign_oriented_min'], r['gene_id']))
            counts[track + '_' + direction] = len(eligible)
            for rank, row in enumerate(eligible, 1):
                row[track + '_track_rank'] = rank
                if rank <= 10:
                    frontier.append({'track': track, 'direction': direction, 'rank': rank, 'gene_id': row['gene_id']})
    frontier = [{**item, **by_gene[item['gene_id']]} for item in frontier]
    anchors = [{'gene_id': gene, 'eligible': gene in by_gene, **by_gene.get(gene, {})} for gene in ANCHORS]
    write(out / 'all_candidates.tsv', rows)
    write(out / 'review_frontier.tsv', frontier, ['track', 'direction', 'rank'] + list(rows[0]))
    write(out / 'anchor_lookup.tsv', anchors, ['eligible'] + list(rows[0]))
    summary = {'universe': len(rows), 'retained_libraries': len(manifest), 'configurations': [name for name, _ in configurations],
               'track_eligible_counts': counts, 'frontier_rows': len(frontier), 'frontier_unique_genes': len({r['gene_id'] for r in frontier}),
               'anchor_missing': [g for g in ANCHORS if g not in by_gene],
               'scope': 'Exposed RNA screening. Ordered sensitivity bounds are not confidence intervals, biological effect thresholds, direct targets or validated function.'}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
