"""Shared read-only count and donor helpers for the Nb4 RQ sequence."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import anndata as ad
import h5py
import numpy as np
import pandas as pd
import scipy.sparse as sp
from common import PACKAGE, REPO, read_json, sha256, write_json, new_run, finish_record

CFG = read_json(PACKAGE / 'config/rq_sequence_v1.json')
ALV = 'Alveolar Fibroblast'
ADV = 'Adventitial Fibroblast'


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=REPO)
    return parser.parse_args()


def begin(name, previous=None):
    if previous and not (PACKAGE / 'runs' / previous / 'run_record.json').is_file():
        raise ValueError('Previous sequential stage has not completed: ' + previous)
    return new_run(PACKAGE / 'runs' / name)


def checked(root, item, receipt):
    path = root / item['path' if 'path' in item else 'cache_path']
    actual = sha256(path)
    if actual != item['sha256']:
        raise ValueError('Input hash mismatch: ' + str(path))
    receipt[str(path.relative_to(root)).replace('\\', '/')] = actual
    return path


def csr_rows(group, start, stop):
    if group.attrs['encoding-type'] != 'csr_matrix':
        raise ValueError('Expected CSR raw count matrix')
    ptr = group['indptr'][start:stop+1]
    lo, hi = int(ptr[0]), int(ptr[-1])
    return sp.csr_matrix((group['data'][lo:hi].astype(float), group['indices'][lo:hi], ptr-ptr[0]),
                         shape=(stop-start, int(group.attrs['shape'][1])))


def read_atlas(path, genes):
    obj = ad.read_h5ad(path, backed='r')
    obs = obj.obs.copy().reset_index(names='cell_id')
    symbols = obj.raw.var.feature_name.astype(str).to_numpy()
    lookup = {g: np.flatnonzero(symbols == g) for g in genes}
    count = np.full((len(obs), len(genes)), np.nan)
    totals = np.empty(len(obs))
    with h5py.File(path, 'r') as f:
        for start in range(0, len(obs), 1024):
            stop = min(start+1024, len(obs))
            block = csr_rows(f['raw/X'], start, stop)
            if np.any(~np.isfinite(block.data)) or np.any(block.data < 0) or np.any(abs(block.data-np.rint(block.data)) > 1e-6):
                raise ValueError('Invalid raw count domain')
            totals[start:stop] = np.asarray(block.sum(axis=1)).ravel()
            for j, g in enumerate(genes):
                if len(lookup[g]):
                    count[start:stop, j] = np.asarray(block[:, lookup[g]].sum(axis=1)).ravel()
    if np.any(totals <= 0) or not obs.cell_id.is_unique:
        raise ValueError('Invalid library totals or cell keys')
    obj.file.close()
    return obs, count, totals, {g: len(v) for g, v in lookup.items()}


def atlases(source_root, genes, receipt, external=True):
    mpath = source_root / 'raw_data/travaglini_nabhan_2020/prepared/cell_metadata.tsv'
    receipt[str(mpath.relative_to(source_root)).replace('\\', '/')] = sha256(mpath)
    metadata = pd.read_csv(mpath, sep='\t')
    for item in read_json(PACKAGE / 'config/expression_sources_v1.json')['files']:
        path = checked(source_root, item, receipt)
        obs, count, totals, mapping = read_atlas(path, genes)
        m = metadata[metadata.assay == item['assay']].reset_index(drop=True).copy()
        if list(m.cell_id) != list(obs.cell_id):
            raise ValueError('Source count/metadata order mismatch')
        m['cohort'] = 'Travaglini'
        m['subtype'] = m.author_cell_type
        m['keep'] = (m.tissue == 'lung') & (m.anatomical_region == 'distal')
        m['stratum'] = [json.dumps([d, a, r]) for d,a,r in zip(m.donor_id,m.assay,m.anatomical_region)]
        yield m, count, totals, mapping
    if external:
        item = read_json(PACKAGE / 'config/external_source_v1.json')
        ecfg = read_json(PACKAGE / 'config/external_pilot_v1.json')
        path = checked(source_root, item, receipt)
        m, count, totals, mapping = read_atlas(path, genes)
        m['stratum'] = m[ecfg['matching_fields']].astype(str).apply(lambda r: json.dumps(list(r)), axis=1)
        m['keep'] = (m.disease == 'normal') & m.Location_long.isin(['Lower Left Lobe','Upper left lobe'])
        m['subtype'] = m.Celltypes.map({ecfg['left_label']: ALV, ecfg['right_label']: ADV}).fillna('other')
        m['assay'] = 'Madissoon ' + m.suspension_type.astype(str)
        m['cohort'] = 'Madissoon'
        yield m, count, totals, mapping


def strata(meta, left=ALV, right=ADV):
    for label, ids in meta[meta.keep].groupby('stratum', sort=True).groups.items():
        ids = np.asarray(list(ids))
        row = meta.loc[ids[0]]
        a = ids[(meta.loc[ids, 'subtype'] == left).to_numpy()]
        b = ids[(meta.loc[ids, 'subtype'] == right).to_numpy()]
        key = {'cohort': row.cohort, 'assay': row.assay, 'donor_id': row.donor_id,
               'stratum': label, 'n_left': len(a), 'n_right': len(b)}
        yield key, a, b


def save(df, out, name):
    df.to_csv(out / name, sep='\t', index=False, float_format='%.12g')


def finish(out, receipt, status, previous=None):
    write_json(out / 'input_hashes.json', receipt)
    record = {'schema': 'Nb4-rq-run/v1', 'completed_at_utc': datetime.now(timezone.utc).isoformat(),
              'status': status, 'scope': 'exploratory reference diagnostics; biological endpoint gates retained'}
    if previous:
        record['previous_run_sha256'] = sha256(PACKAGE / 'runs' / previous / 'run_record.json')
    finish_record(out, record)


def donor_average(frame, fields, extra=()):
    keys = ['cohort','assay','donor_id','cell_floor'] + list(extra)
    grouped = frame.groupby(keys, dropna=False, sort=True)
    result = grouped[list(fields)].mean().reset_index()
    result['n_strata'] = grouped.size().to_numpy()
    return result
