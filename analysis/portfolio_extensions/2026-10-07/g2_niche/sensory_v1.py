"""Nb4-P09: fixed candidate expression, specificity and assay transport.

No phenotype-based relabeling, cell-based biological tests, or functional claims.
"""
import argparse
import json
from pathlib import Path
import h5py
import numpy as np
import pandas as pd
from scipy import sparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GENES = ['SCN7A', 'GRIA1', 'COL1A1', 'PDGFRA', 'SOX10', 'S100B', 'PLP1']
TARGETS = GENES[:2]
ROOT = Path(__file__).resolve().parents[4]
CACHE = 'raw_data/travaglini_nabhan_2020/'
FILES = [('SS2', 'cellxgene/c0ee0004-7bd1-4986-9b66-8a9d3593c0e6.h5ad'),
         ('10x', 'cellxgene/f5568ea3-c249-4e4e-91f8-46abc30a5612.h5ad'),
         ('Madissoon', 'external/460b3fe9-f623-4299-a745-78beba61c3d8.h5ad')]
KEYS = ['cohort', 'assay', 'donor', 'region', 'protocol', 'cell_type']


def vector(node):
    if isinstance(node, h5py.Dataset):
        return node.asstr()[:] if node.dtype.kind in 'SO' else node[:]
    categories, codes = vector(node['categories']), node['codes'][:]
    return np.asarray([categories[i] if i >= 0 else None for i in codes])


def read_counts(path):
    with h5py.File(path, 'r') as f:
        ids = vector(f['obs'][f['obs'].attrs['_index']])
        symbols = vector(f['raw/var/feature_name'])
        mapping = {g: np.flatnonzero(symbols == g) for g in GENES}
        if any(len(v) != 1 for v in mapping.values()):
            raise ValueError('Each fixed gene must map exactly once')
        g = f['raw/X']
        if g.attrs['encoding-type'] != 'csr_matrix':
            raise ValueError('Expected CSR raw counts')
        shape = g.attrs['shape']
        values, totals = np.zeros((len(ids), len(GENES)), dtype=np.int64), np.zeros(len(ids), dtype=np.int64)
        for start in range(0, len(ids), 1024):
            end = min(len(ids), start + 1024)
            ptr = g['indptr'][start:end + 1]
            lo, hi = int(ptr[0]), int(ptr[-1])
            raw = g['data'][lo:hi]
            if np.any(~np.isfinite(raw)) or np.any(raw < 0) or np.any(raw != np.rint(raw)):
                raise ValueError('Invalid count domain')
            block = sparse.csr_matrix((raw.astype(np.int64), g['indices'][lo:hi], ptr - ptr[0]), shape=(end-start, int(shape[1])))
            totals[start:end] = np.asarray(block.sum(axis=1)).ravel()
            values[start:end] = block[:, [mapping[x][0] for x in GENES]].toarray()
        if not pd.Index(ids).is_unique or np.any(totals <= 0):
            raise ValueError('Duplicated cells or nonpositive libraries')
        obs = {k: vector(f['obs'][k]) for k in ['donor_id', 'suspension_type', 'disease', 'Celltypes', 'Location_long', 'Protocol_plot', 'assay_ontology_term_id'] if k in f['obs']}
    return ids, values, totals, obs, {g: int(mapping[g][0]) for g in GENES}


def cell_frame(root):
    metadata = pd.read_csv(root / CACHE / 'prepared/cell_metadata.tsv', sep='\t')
    parts, mappings = [], {}
    for assay, name in FILES:
        ids, values, totals, obs, mapping = read_counts(root / CACHE / name)
        mappings[assay] = mapping
        if assay != 'Madissoon':
            m = metadata[metadata.assay.eq(assay)].reset_index(drop=True)
            if list(m.cell_id) != list(ids):
                raise ValueError('Source metadata/count order mismatch')
            data = pd.DataFrame({'cell': ids, 'cohort': 'Travaglini', 'assay': assay,
                                 'donor': m.donor_id, 'region': m.anatomical_region,
                                 'protocol': assay, 'cell_type': m.author_cell_type})
            keep = m.tissue.eq('lung').to_numpy()
        else:
            data = pd.DataFrame({'cell': ids, 'cohort': 'Madissoon',
                                 'assay': ['Madissoon ' + str(x) for x in obs['suspension_type']],
                                 'donor': obs['donor_id'], 'region': obs['Location_long'],
                                 'protocol': [str(a) + '|' + str(b) for a,b in zip(obs['assay_ontology_term_id'], obs['Protocol_plot'])],
                                 'cell_type': obs['Celltypes']})
            keep = (np.asarray(obs['disease']) == 'normal') & (np.asarray(obs['Location_long']) != 'Mix')
            data.cell_type = data.cell_type.replace({'Fibro_alveolar': 'Alveolar Fibroblast', 'Fibro_adventitial': 'Adventitial Fibroblast'})
        data['library'] = totals
        for j, gene in enumerate(GENES):
            data[gene] = values[:, j]
        data['neural_flag'] = (data.SOX10 > 0) & ((data.S100B > 0) | (data.PLP1 > 0))
        data['fibro_marker'] = (data.COL1A1 > 0) | (data.PDGFRA > 0)
        parts.append(data[keep].copy())
    data = pd.concat(parts, ignore_index=True)
    if data[KEYS].isna().any().any():
        raise ValueError('Missing stratum identity')
    return data, mappings


def summarize(data):
    gene_rows, joint_rows = [], []
    for keys, group in data.groupby(KEYS, sort=True):
        key = dict(zip(KEYS, keys))
        for sensitivity in ['all', 'exclude_neural_flag']:
            s = group if sensitivity == 'all' else group[~group.neural_flag]
            if s.empty:
                continue
            ordered = s.sort_values(['library', 'cell'])
            subsets = [('all_depth', s), ('low_half', ordered.iloc[:len(s)//2]), ('high_half', ordered.iloc[len(s)//2:])]
            for depth, block in subsets:
                if block.empty:
                    continue
                base = {**key, 'sensitivity': sensitivity, 'depth': depth, 'n_cells': len(block), 'library': int(block.library.sum())}
                for threshold in [1, 2]:
                    a, b = block.SCN7A.ge(threshold), block.GRIA1.ge(threshold)
                    joint_rows.append({**base, 'threshold': threshold, 'n_scn7a': int(a.sum()), 'n_gria1': int(b.sum()),
                                       'n_joint': int((a & b).sum()), 'fraction_joint': float((a & b).mean()),
                                       'n_joint_fibro_marker': int((a & b & block.fibro_marker).sum()),
                                       'n_neural_flag': int(block.neural_flag.sum())})
                for gene in TARGETS:
                    total = int(block[gene].sum())
                    gene_rows.append({**base, 'gene': gene, 'sum_count': total,
                                      'n_detected': int(block[gene].gt(0).sum()),
                                      'fraction_detected': float(block[gene].gt(0).mean()),
                                      'log2cpm': float(np.log2(1 + 1e6 * total / block.library.sum()))})
    return pd.DataFrame(gene_rows), pd.DataFrame(joint_rows)


def paired(gene):
    use = gene[(gene.depth == 'all_depth') &
               (((gene.cohort == 'Travaglini') & (gene.region == 'distal')) |
                ((gene.cohort == 'Madissoon') & gene.region.isin(['Lower Left Lobe', 'Upper left lobe'])))]
    pairs = []
    group_keys = KEYS[:-1] + ['sensitivity', 'gene']
    for keys, g in use.groupby(group_keys, sort=True):
        by_type = g.set_index('cell_type')
        if not {'Alveolar Fibroblast', 'Adventitial Fibroblast'}.issubset(by_type.index):
            continue
        a, b = by_type.loc['Alveolar Fibroblast'], by_type.loc['Adventitial Fibroblast']
        for floor in [20, 10]:
            pairs.append({**dict(zip(group_keys, keys)), 'floor': floor, 'n_alveolar': int(a.n_cells), 'n_adventitial': int(b.n_cells),
                          'eligible': bool(min(a.n_cells, b.n_cells) >= floor),
                          'delta_log2cpm': float(a.log2cpm - b.log2cpm),
                          'delta_detection': float(a.fraction_detected - b.fraction_detected)})
    frame = pd.DataFrame(pairs)
    dkeys = ['cohort', 'assay', 'donor', 'sensitivity', 'gene', 'floor']
    donor = frame[frame.eligible].groupby(dkeys).agg(delta_log2cpm=('delta_log2cpm', 'mean'), delta_detection=('delta_detection', 'mean'), n_strata=('eligible', 'size')).reset_index()
    return frame, donor


def verify(data, gene, joint, effects, donors):
    """Independent pandas grouping of primary rows, plus exact identities."""
    checks = 0
    main = gene[(gene.sensitivity == 'all') & (gene.depth == 'all_depth')].set_index(KEYS + ['gene'])
    for target in TARGETS:
        x = data.assign(detected=data[target].gt(0).astype(int)).groupby(KEYS).agg(total=(target, 'sum'), detected=('detected', 'sum'), n=('cell', 'size'), library=('library', 'sum'))
        actual = main.xs(target, level='gene').reindex(x.index)
        for col, original in [('sum_count','total'), ('n_detected','detected'), ('n_cells','n'), ('library','library')]:
            np.testing.assert_array_equal(actual[col], x[original]); checks += len(x)
        np.testing.assert_allclose(actual.log2cpm, np.log2(1 + x.total / x.library * 1e6)); checks += len(x)
    if not ((joint.n_joint <= joint.n_scn7a) & (joint.n_joint <= joint.n_gria1) &
            (joint.n_joint >= joint.n_scn7a + joint.n_gria1 - joint.n_cells) &
            (joint.n_joint_fibro_marker <= joint.n_joint)).all():
        raise ValueError('Joint detection bounds failed')
    checks += len(joint)
    np.testing.assert_allclose(joint.fraction_joint, joint.n_joint / joint.n_cells)
    np.testing.assert_array_equal(effects.eligible, effects[['n_alveolar', 'n_adventitial']].min(axis=1) >= effects.floor)
    for _, row in donors.iterrows():
        q = effects[effects.eligible]
        for name in ['cohort','assay','donor','sensitivity','gene','floor']:
            q = q[q[name].eq(row[name])]
        if not np.isclose(sum(q.delta_log2cpm)/len(q), row.delta_log2cpm):
            raise ValueError('Donor stratum-weight check failed')
        checks += 1
    return {'status': 'passed', 'checks': checks, 'method': 'Independent pandas aggregation from cell count evidence; joint bounds; eligibility; equal-stratum donor arithmetic. Same data, not biological replication.'}


def figure(genes, joint, donors, out):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    assays = ['10x', 'SS2', 'Madissoon cell', 'Madissoon nucleus']
    colors = ['#267b91', '#db9b35', '#925dc1', '#cd6057']
    primary = donors[(donors.floor == 20) & (donors.sensitivity == 'all')]
    for j, target in enumerate(TARGETS):
        ax = axes[j]
        for k, (assay, color) in enumerate(zip(assays, colors)):
            g = primary[(primary.assay == assay) & (primary.gene == target)].sort_values('donor')
            xx = k + np.linspace(-.16,.16,max(1,len(g)))[:len(g)]
            ax.scatter(xx, g.delta_log2cpm, color=color, s=42)
            for x, (_, row) in zip(xx, g.iterrows()):
                ax.annotate(row.donor, (x,row.delta_log2cpm), xytext=(2,4), textcoords='offset points', fontsize=7)
        ax.axhline(0,color='#555',lw=.8)
        ax.set_xticks(range(4), ['Source\n10x','Source\nSS2','External\ncells','External\nnuclei'])
        ax.set_title(target + ': matched subtype contrast')
        ax.set_ylabel('Alveolar minus adventitial log2(CPM + 1)')
    j = joint[(joint.sensitivity == 'all') & (joint.depth == 'all_depth') & (joint.threshold == 1) & (joint.n_cells >= 20)]
    labels = ['Alveolar Fibroblast','Adventitial Fibroblast','Schwann_nonmyelinating','Schwann_Myelinating','NAF_endoneurial','NAF_epineurial']
    for i, label in enumerate(labels):
        for k, (assay, color) in enumerate(zip(assays,colors)):
            x = j[(j.cell_type == label) & (j.assay == assay)]
            # One dot per donor, equal average across its eligible regions/protocols.
            d = x.groupby('donor').fraction_joint.mean()
            axes[2].scatter(d*100, np.repeat(i + (k-1.5)*.12,len(d)),s=24,color=color,label=assay if i == 0 else None)
    axes[2].set_yticks(range(len(labels)),['Alveolar fibroblast','Adventitial fibroblast','Nonmyelinating Schwann','Myelinating Schwann','Endoneurial NAF','Epineurial NAF'])
    axes[2].invert_yaxis(); axes[2].set_xlabel('Joint SCN7A / GRIA1 detection (%)')
    axes[2].set_title('Co-detection: different regions remain a limit')
    axes[2].legend(fontsize=7,loc='lower right')
    fig.suptitle('Nb4-P09 | RNA expression and transport, not sensory function',fontsize=14)
    fig.savefig(out/'sensory_v1.png',dpi=180); fig.savefig(out/'sensory_v1.svg'); plt.close(fig)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    if (out/'summary.json').exists():
        raise FileExistsError('Refuse overwrite')
    cells, mapping = cell_frame(ROOT)
    gene, joint = summarize(cells); effects, donors = paired(gene)
    verification = verify(cells,gene,joint,effects,donors)
    for data,name in [(cells,'cell_count_evidence.tsv.gz'),(gene,'stratum_gene.tsv'),(joint,'joint_detection.tsv'),(effects,'pair_effects.tsv'),(donors,'donor_effects.tsv')]:
        data.to_csv(out/name,sep='\t',index=False,float_format='%.12g')
    primary=donors[(donors.floor == 20)&(donors.sensitivity == 'all')]
    summaries=[]
    for (cohort,assay,target),g in primary.groupby(['cohort','assay','gene']):
        summaries.append({'cohort':cohort,'assay':assay,'gene':target,'donors':list(g.donor), 'n_donors':len(g), 'mean_delta_log2cpm':float(g.delta_log2cpm.mean()),'min':float(g.delta_log2cpm.min()),'max':float(g.delta_log2cpm.max()),'n_positive':int(g.delta_log2cpm.gt(0).sum())})
    (out/'summary.json').write_text(json.dumps({'scope':'Exposed descriptive expression check; no sensory, repair or causal inference','cells':len(cells),'gene_mapping':mapping,'primary':summaries},indent=2)+'\n')
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    figure(gene,joint,donors,out)
    print(json.dumps({'status':'complete','cells':len(cells),'verified_checks':verification['checks']}))


if __name__ == '__main__':
    main()
