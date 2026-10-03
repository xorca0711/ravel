"""Qualify newly recovered official atlas sources; no biological effect fitting."""
import argparse
from pathlib import Path
import json
import h5py
import numpy as np
import pandas as pd
from nb5_io import read_obs, read_matrix, read_genes, write_tsv, write_json

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / 'raw_data/tabula_muris_senis_2020'
RUNS = ROOT / 'analysis/research/runs'
MISSING = {'', 'nan', 'NA', 'None'}


def join_metadata(left, right, key, suffix, label):
    """Accept exact or one documented assay-concatenation suffix; never fuzzy IDs."""
    assert right['index'].is_unique
    index = right.set_index('index', drop=False)
    identities = set(index.index)
    rows = []
    for _, row in left.iterrows():
        value = str(row[key])
        candidates = [value, value + suffix]
        if value.endswith(suffix):
            candidates.append(value[:-len(suffix)])
        hits = sorted(set(candidates).intersection(identities))
        if len(hits) > 1:
            raise ValueError(f'Ambiguous identity in {label}: {value}')
        out = row.to_dict()
        out['source_index'] = hits[0] if hits else ''
        out['join_rule'] = ('exact' if hits[0] == value else 'one_assay_suffix') if hits else 'unmatched'
        if hits:
            src = index.loc[hits[0]]
            for field in right.columns:
                if field != 'index': out['official_' + field] = src[field]
            expected_age = str(row.get('age', str(row.get('age_months', '')) + 'm'))
            for target, observed in [('age', expected_age), ('mouse.id', str(row.get('mouse_id', ''))), ('tissue', str(row.get('tissue', '')))]:
                if observed and str(src[target]) != observed:
                    raise ValueError(f'Conflicting {target} for {label}: {value}')
        rows.append(out)
    return pd.DataFrame(rows)


def grouped(df, fields):
    return df.groupby(fields, dropna=False).size().rename('cells').reset_index()


def main(out):
    recovered = RAW / 'completion_v1'
    official = pd.read_csv(recovered/'full_metadata.csv', dtype=str, keep_default_na=False)
    assert official['index'].is_unique
    with h5py.File(recovered/'official_brain.h5ad') as h:
        brain = read_obs(h)
        layers = []
        for key in ['X', 'raw.X', 'raw/X']:
            if key not in h: continue
            x = read_matrix(h,key); totals = np.asarray(x.sum(axis=1)).ravel()
            layers.append({'layer':key,'cells':x.shape[0],'genes':x.shape[1],
                           'nonzero':x.nnz,'min_nonzero':float(x.data.min()),'max':float(x.data.max()),
                           'finite':bool(np.isfinite(x.data).all()),'nonnegative':bool((x.data>=0).all()),
                           'integer':bool(np.allclose(x.data,np.rint(x.data),rtol=0,atol=1e-7)),
                           'row_total_min':float(totals.min()),'row_total_median':float(np.median(totals)),
                           'row_total_max':float(totals.max())})
        var_key = 'raw.var' if 'raw.var' in h else ('raw/var' if 'raw/var' in h else 'var')
        genes = read_genes(h,var_key)
        assert len(genes)==len(set(genes))
    with h5py.File(RAW/'case_study_v1/facs.Brain_Myeloid.clustered_diversity.h5ad') as h:
        case = read_obs(h)
    facs = official.query("method == 'facs'")
    brain_join = join_metadata(brain, facs, 'cell_id', '-1', 'brain')
    case_join = join_metadata(case, brain.rename(columns={'cell_id':'index','mouse_id':'mouse.id'}), 'cell_id', '-1', 'case_to_brain')
    write_tsv(out/'brain_cells.tsv',brain_join)
    write_tsv(out/'brain_layers.tsv',pd.DataFrame(layers))
    write_tsv(out/'case_brain_join.tsv',case_join)
    fields = [f for f in ['age','mouse_id','sex','subtissue','batch','plate','cell_ontology_class'] if f in brain]
    write_tsv(out/'brain_design.tsv',grouped(brain,fields))
    covariates = []
    for field in ['subtissue','batch','plate','sex','cell_ontology_class','free_annotation']:
        if field in brain:
            q=brain.groupby(['age',field],dropna=False).agg(cells=('cell_id','size'),mice=('mouse_id','nunique')).reset_index()
            q=q.rename(columns={field:'value'});q['field']=field;covariates.append(q)
    write_tsv(out/'brain_covariates.tsv',pd.concat(covariates,ignore_index=True))
    rep = pd.read_csv(RUNS/'nb5_repertoire_v2/repertoire_cells.tsv',sep='\t',keep_default_na=False)
    repertoire_join = join_metadata(rep, facs, 'join_key', '-1', 'repertoire')
    write_tsv(out/'repertoire_annotation_join.tsv',repertoire_join)
    write_tsv(out/'repertoire_subtype_support.tsv',grouped(repertoire_join.fillna(''),['age_months','mouse_id','tissue','join_rule','official_cell_ontology_class','official_free_annotation']))
    kidney = pd.read_csv(RUNS/'nb5_metadata_v3/cell_metadata.tsv',sep='\t',keep_default_na=False)
    kidney = kidney.query("dataset == 'Kidney_droplet'")
    kidney_join = join_metadata(kidney,official.query("method == 'droplet'"),'cell_id','-0','kidney')
    write_tsv(out/'kidney_annotation_join.tsv',kidney_join)
    write_tsv(out/'kidney_annotation_support.tsv',grouped(kidney_join.fillna(''),['age','mouse_id','join_rule','cell_ontology_class','official_cell_ontology_class','official_free_annotation']))
    checks = {'scope':'metadata qualification only; no biological effects or independent replication',
              'source_index_unique':True,'ambiguous_join_count':0,'matched_identity_conflict_count':0,
              'brain_cells':len(brain),'brain_genes':len(genes),
              'brain_age_cells':brain.groupby('age').size().to_dict(),
              'brain_age_mice':brain.groupby('age').mouse_id.nunique().to_dict()}
    for label,table in [('brain',brain_join),('case',case_join),('repertoire',repertoire_join),('kidney',kidney_join)]:
        checks[label+'_join_counts']=table.join_rule.value_counts().to_dict()
        assert len(table)==len(set(table['cell_id'] if 'cell_id' in table else table['cell_name']))
    write_json(out/'qualification.json',checks)
    print(json.dumps(checks,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
