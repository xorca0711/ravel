"""England continuation EN1: source-inspired full-transcriptome clustering, separately by experiment.

Frozen rules: continuation_contract.json['clustering'] and amendment CA2 (igraph multilevel = Louvain).
Input: the per-library source-QC CSR caches written by prepare_continuation.py and the per-cell table.
All source-QC cells are clustered (contract: 'full raw triplets after source QC'); inclusion flags,
gates and states from the preparation step are cross-tabulated afterwards, never used for clustering.
This is a sensitivity reconstruction. It is not an exact Seurat/author-barcode reproduction, no
six-state solution is forced and no resolution is selected on an outcome.

Outputs: trials/continuation/EN1/ (retention_waterfall.csv, cluster_sizes.csv, cluster_by_library.csv,
cluster_marker_panels.csv, cluster_gate_crosstab.csv, run_record.json); ignored per-cell labels under
processed/continuation/clustering/.
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime, platform, random, gc
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); a = p.parse_args()
os.environ.setdefault('NUMBA_NUM_THREADS', '4'); os.environ.setdefault('OMP_NUM_THREADS', '4')
os.environ['JOBLIB_MULTIPROCESSING'] = '0'  # sandbox forbids worker-process pipes; joblib runs in-process (threads/sequential)
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
os.environ.setdefault('NUMBA_CACHE_DIR', str(HERE / 'processed/continuation/numba_cache'))
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd, scipy.sparse as sp, scanpy as sc, anndata as ad, igraph as ig
import importlib.metadata as im

CONTRACT = HERE / 'config/continuation_contract.json'; AMEND = HERE / 'config/continuation_amendments.json'
cfg = json.loads(CONTRACT.read_text(encoding='utf-8')); cl = cfg['clustering']
OUT = HERE / 'trials/continuation/EN1'; PROC = HERE / 'processed/continuation'; LAB = PROC / 'clustering'
OUT.mkdir(parents=True, exist_ok=True); LAB.mkdir(parents=True, exist_ok=True)
assert not (OUT / 'run_record.json').exists(), 'Refuse overwrite of completed run'
def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
def git_head(root):
    g = root / '.git'; gitdir = Path(g.read_text().split(':', 1)[1].strip()) if g.is_file() else g
    head = (gitdir / 'HEAD').read_text().strip(); ref = head[5:]
    common = (gitdir / (gitdir / 'commondir').read_text().strip()).resolve() if (gitdir / 'commondir').exists() else gitdir
    f = common / ref
    return f.read_text().strip() if f.exists() else [l.split()[0] for l in (common / 'packed-refs').read_text().splitlines() if l.endswith(' ' + ref)][0]

record = {'stage': 'EN1 source-inspired clustering', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'contract_sha256': digest(CONTRACT), 'amendments_sha256': digest(AMEND), 'script_sha256': digest(Path(__file__)), 'git_head': git_head(ROOT),
          'interpreter': sys.executable, 'python': platform.python_version(), 'versions': {m: im.version(m) for m in ['numpy', 'pandas', 'scipy', 'scanpy', 'anndata', 'igraph']},
          'rules': cl, 'amendment': 'CA2: igraph Graph.community_multilevel(weights=connectivities, resolution=r) with random.seed(seed) before each call',
          'inputs': [], 'experiments': {}, 'interpretation': 'sensitivity reconstruction; not author labels; no outcome-selected resolution'}
(OUT / 'started.json').write_text(json.dumps(record, indent=2) + '\n')

manifest = pd.read_csv(HERE / 'metadata/geo_library_manifest.csv', keep_default_na=False)
cells = pd.read_csv(PROC / 'cells_table.csv.gz', usecols=['gsm', 'barcode', 'total_umis', 'n_genes', 'doublet_flag', 'primary_include', 'strict_include',
                                                          'gate_AT2', 'gate_transition', 'gate_AT1', 'state', 'Cd177_umi', 'raw_AT2_identity', 'raw_AT1_identity', 'raw_transition_RNA', 'raw_cycling', 'cycling_markers_detected'])
record['inputs'].append({'path': 'processed/continuation/cells_table.csv.gz', 'sha256': digest(PROC / 'cells_table.csv.gz')})
features = pd.read_csv(PROC / 'matrices/features.csv', keep_default_na=False)
symbols = features.gene_symbol.astype(str).to_numpy().astype(str)
panels = {'AT2_gate': cfg['gates']['AT2'], 'transition_gate': cfg['gates']['transition'], 'AT1_gate': cfg['gates']['AT1'],
          'epithelial_anchors': cfg['epithelial_anchors'], 'immune': cfg['immune_panel'], **{f'nonepi_{k}': v for k, v in cfg['non_epithelial_panels'].items()},
          'cycling': cfg['modules']['cycling'], 'AT1_identity_module': cfg['modules']['AT1_identity'], 'AT2_identity_module': cfg['modules']['AT2_identity'],
          'transition_RNA_module': cfg['modules']['transition_RNA'], 'Cd177': ['Cd177'], 'Itga2': ['Itga2']}
waterfall, sizes, bylib, markers, cross = [], [], [], [], []
for exp in sorted(manifest.experiment.unique()):
    libs = manifest[manifest.experiment == exp]
    mats, obs = [], []
    for _, row in libs.iterrows():
        X = sp.load_npz(PROC / f'matrices/{row.gsm}_sourceQC.npz').tocsr(); bc = np.load(PROC / f'matrices/{row.gsm}_barcodes.npy', allow_pickle=False).astype(str)
        record['inputs'].append({'path': f'processed/continuation/matrices/{row.gsm}_sourceQC.npz', 'sha256': digest(PROC / f'matrices/{row.gsm}_sourceQC.npz'), 'cells': int(X.shape[0])})
        mats.append(X); obs.append(pd.DataFrame({'gsm': row.gsm, 'barcode': bc}))
        waterfall.append({'experiment': exp, 'gsm': row.gsm, 'population': row.population, 'il1r1_status': row.il1r1_status, 'collection_day': row.collection_day,
                          'deposited_barcodes': int(row.matrix_barcodes) if str(row.matrix_barcodes).isdigit() else None, 'source_QC': int(X.shape[0])})
    X = sp.vstack(mats, format='csr'); del mats; gc.collect()
    ob = pd.concat(obs, ignore_index=True).merge(cells, on=['gsm', 'barcode'], how='left', validate='one_to_one')
    assert ob.state.notna().all(), 'cell table join incomplete'
    adata = ad.AnnData(X=X.astype(np.float32), obs=ob.set_index(ob.gsm + ':' + ob.barcode)); adata.var_names = features.gene_id.astype(str).to_numpy(); adata.var['symbol'] = symbols
    nonmt = ~np.char.startswith(symbols, 'mt-'); detected = np.asarray((adata.X > 0).sum(0)).ravel() >= 3
    adata = adata[:, nonmt & detected].copy(); n_genes_used = adata.n_vars
    sc.pp.normalize_total(adata, target_sum=1e4); sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, flavor='seurat', n_top_genes=cl['HVG'])
    sc.pp.pca(adata, n_comps=cl['pcs'], mask_var='highly_variable', zero_center=True, random_state=cl['seed'])
    sc.pp.neighbors(adata, n_neighbors=cl['neighbors'], n_pcs=cl['pcs'], random_state=cl['seed'])
    W = adata.obsp['connectivities'].tocoo(); mask = W.row < W.col
    g = ig.Graph(n=adata.n_obs, edges=list(zip(W.row[mask].tolist(), W.col[mask].tolist())), directed=False); g.es['weight'] = W.data[mask].tolist()
    labels = {}
    for res in cl['resolutions']:
        random.seed(cl['seed']); ig.set_random_number_generator(random)
        part = g.community_multilevel(weights='weight', resolution=res)
        labels[res] = np.asarray(part.membership); adata.obs[f'louvain_r{res}'] = labels[res]
        record['experiments'].setdefault(str(exp), {})[f'r{res}_clusters'] = int(labels[res].max() + 1)
        record['experiments'][str(exp)][f'r{res}_modularity'] = float(part.modularity)
    record['experiments'][str(exp)].update(cells=int(adata.n_obs), genes_used=n_genes_used, hvg=int(adata.var.highly_variable.sum()))
    # per-cluster panels on log-normalized values (mean detection fraction and mean expression of panel genes)
    sym = adata.var['symbol'].to_numpy(); Xl = adata.X.tocsc()
    panel_idx = {k: np.where(np.isin(sym, v))[0] for k, v in panels.items()}
    for res, lab in labels.items():
        for c in np.unique(lab):
            m = lab == c; sub = Xl[m]; n = int(m.sum())
            o = adata.obs[m]
            sizes.append({'experiment': exp, 'resolution': res, 'cluster': int(c), 'n_cells': n, 'fraction_of_experiment': n / adata.n_obs,
                          'median_umis': float(o.total_umis.median()), 'median_genes': float(o.n_genes.median()), 'doublet_fraction': float(o.doublet_flag.mean()),
                          'primary_fraction': float(o.primary_include.mean()), 'strict_fraction': float(o.strict_include.mean())})
            for gsm_, k in o.gsm.value_counts().items(): bylib.append({'experiment': exp, 'resolution': res, 'cluster': int(c), 'gsm': gsm_, 'n_cells': int(k), 'fraction_of_library': float(k / (adata.obs.gsm == gsm_).sum())})
            row = {'experiment': exp, 'resolution': res, 'cluster': int(c), 'n_cells': n}
            for k, ix in panel_idx.items():
                if len(ix) == 0: continue
                block = sub[:, ix]
                row[f'{k}__detect_frac'] = float((block > 0).mean()); row[f'{k}__mean_log1p'] = float(block.mean())
            gate_panels = ['AT2_gate', 'transition_gate', 'AT1_gate', 'immune', 'nonepi_mesenchymal', 'nonepi_endothelial', 'nonepi_ciliated', 'cycling']
            row['top_panel_by_detection'] = max(gate_panels, key=lambda k: row.get(f'{k}__detect_frac', -1))
            markers.append(row)
            st = o.state.value_counts()
            cross.append({'experiment': exp, 'resolution': res, 'cluster': int(c), 'n_cells': n, **{f'state_{s}': int(st.get(s, 0)) for s in ['AT2', 'transition', 'transition_AT1', 'AT1', 'mixed', 'unresolved']},
                          'gate_AT2_frac': float(o.gate_AT2.mean()), 'gate_transition_frac': float(o.gate_transition.mean()), 'gate_AT1_frac': float(o.gate_AT1.mean()),
                          'Cd177_ge1_frac': float((o.Cd177_umi >= 1).mean()), 'cycling_ge2_frac': float((o.cycling_markers_detected >= 2).mean()),
                          'mean_AT2_identity': float(o.raw_AT2_identity.mean()), 'mean_AT1_identity': float(o.raw_AT1_identity.mean()), 'mean_transition_RNA': float(o.raw_transition_RNA.mean()), 'mean_cycling': float(o.raw_cycling.mean())})
    adata.obs[['gsm', 'barcode'] + [f'louvain_r{r}' for r in cl['resolutions']]].to_csv(LAB / f'experiment{exp}_cluster_labels.csv.gz', index=False)
    np.save(LAB / f'experiment{exp}_pca.npy', adata.obsm['X_pca'].astype(np.float32))
    print(f'experiment {exp}: {adata.n_obs} cells, {n_genes_used} genes, clusters ' + ', '.join(f'r{r}={labels[r].max()+1}' for r in cl['resolutions']), flush=True)
    del adata, X, Xl, g, W; gc.collect()
wf = pd.DataFrame(waterfall)
inc = cells.groupby('gsm')[['primary_include', 'strict_include']].sum().astype(int); wf = wf.merge(inc, left_on='gsm', right_index=True)
wf.to_csv(OUT / 'retention_waterfall.csv', index=False)
pd.DataFrame(sizes).to_csv(OUT / 'cluster_sizes.csv', index=False); pd.DataFrame(bylib).to_csv(OUT / 'cluster_by_library.csv', index=False)
pd.DataFrame(markers).to_csv(OUT / 'cluster_marker_panels.csv', index=False); pd.DataFrame(cross).to_csv(OUT / 'cluster_gate_crosstab.csv', index=False)
record.update(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), outputs=[{'file': f.name, 'sha256': digest(f)} for f in sorted(OUT.glob('*.csv'))],
              ignored_outputs=[{'file': f.name, 'sha256': digest(f)} for f in sorted(LAB.glob('*'))])
(OUT / 'run_record.json').write_text(json.dumps(record, indent=2) + '\n'); print('EN1 completed', flush=True)
