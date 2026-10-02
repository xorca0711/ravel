"""Prepare source-linked metadata from curated H5AD objects without expression fitting."""
from datetime import datetime, timezone
import importlib.util
import pandas as pd
import anndata as ad
from common import PACKAGE, REPO, read_json, write_json, new_run, finish_record, sha256


def main():
    sources = read_json(PACKAGE / 'config/expression_sources_v1.json')
    out = new_run(PACKAGE / 'runs/metadata_v1')
    prepared = REPO / 'raw_data/travaglini_nabhan_2020/prepared'
    prepared.mkdir(parents=True, exist_ok=True)
    rows, audits = [], []
    for source in sources['files']:
        path = REPO / source['cache_path']
        if sha256(path) != source['sha256']:
            raise ValueError('Expression-object hash mismatch')
        obj = ad.read_h5ad(path, backed='r')
        obs = obj.obs.copy()
        assay = source['assay']
        normalized = pd.DataFrame(index=obs.index)
        normalized['cell_id'] = obs.index.astype(str)
        normalized['donor_id'] = 'P' + obs['donor_id'].astype(str)
        normalized['assay'] = assay
        normalized['sample_id'] = obs['sample'].astype(str)
        normalized['tissue'] = obs['tissue'].astype(str)
        normalized['condition'] = obs['region'].astype(str).replace({'normal': 'histologically_normal'})
        normalized['anatomical_region'] = obs['location'].astype(str)
        normalized['author_cell_type'] = obs['free_annotation'].astype(str)
        normalized['raw_library_id'] = obs['plate.barcode' if assay == 'SS2' else 'channel'].astype(str)
        normalized['counts_unit'] = 'read_count' if assay == 'SS2' else 'UMI'
        normalized['source_compartment'] = obs['compartment'].astype(str)
        rows.append(normalized)
        counts = obs.groupby(['donor_id', 'free_annotation'], observed=True).size().rename('n_cells').reset_index()
        counts.insert(0, 'assay', assay)
        counts.to_csv(out / f'{assay}_author_label_counts.tsv', sep='\t', index=False)
        audits.append({'assay': assay, 'dataset_version': source['dataset_version_id'], 'n_cells': obj.n_obs, 'n_genes': obj.n_vars, 'raw_shape': list(obj.raw.shape), 'donors': obs['donor_id'].astype(str).value_counts().to_dict(), 'tissue': obs['tissue'].astype(str).value_counts().to_dict(), 'locations': obs['location'].astype(str).value_counts().to_dict(), 'curation': 'CELLxGENE standardized cell_type is not substituted for the source free_annotation', 'matrix_cell_join': 'obs rows and matrix rows are in the same H5AD with unique obs names', 'unique_obs_names': bool(obs.index.is_unique)})
        if not obs.index.is_unique:
            raise ValueError('Duplicate H5AD obs names')
        obj.file.close()
    metadata = pd.concat(rows, ignore_index=True)
    metadata.to_csv(prepared / 'cell_metadata.tsv', sep='\t', index=False)
    config = read_json(PACKAGE / 'config/pipeline_v1.json')
    spec = importlib.util.spec_from_file_location('metadata_gate', PACKAGE / 'scripts/01_metadata_gate.py')
    gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
    errors, excluded, coverage, gates = gate.audit_rows(metadata.to_dict('records'), config)
    pd.DataFrame(gates).to_csv(out / 'gates.tsv', sep='\t', index=False)
    pd.DataFrame([dict(zip(['donor_id','assay','anatomical_region','author_cell_type','n_cells'],[*key,value])) for key,value in sorted(coverage.items())]).to_csv(out / 'coverage.tsv', sep='\t', index=False)
    mapping = {'source_version': {s['assay']:s['dataset_version_id'] for s in sources['files']}, 'source_sha256': {s['assay']:s['sha256'] for s in sources['files']}, 'field_mapping': {'cell_id':'obs.index', 'donor_id':'P + donor_id', 'sample_id':'sample', 'condition':'region: normal -> histologically_normal', 'anatomical_region':'location', 'author_cell_type':'free_annotation', 'raw_library_id':'plate.barcode (SS2) / channel (10x)', 'counts_unit':'assay-derived; numerical semantics checked in expression stage'}, 'author_label_mapping':'identity: preserve source free_annotation without replacement by standardized ontology labels', 'matrix_cell_join_status':'verified H5AD row identity and unique obs names', 'normalized_metadata_sha256':sha256(prepared/'cell_metadata.tsv')}
    write_json(prepared/'metadata_mapping.json', mapping)
    write_json(out/'metadata_mapping.json', mapping)
    write_json(out/'audit.json', {'errors':errors, 'excluded':dict(excluded), 'objects':audits, 'normal_lung_cells':int((metadata.tissue=='lung').sum()), 'interpretation':'metadata eligibility only; no biological fit'})
    finish_record(out, {'schema':'TN2020-metadata-preparation/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'failed' if errors else 'metadata complete','expression_analysis_run':False})
    print(f'Metadata: {len(metadata)} cells, {len(errors)} validation errors, {sum(g["metadata_count_gate"]=="PASS" for g in gates)} matched-region count gates pass.')
    if errors:
        print(errors[:5]); raise SystemExit(1)


if __name__ == '__main__':
    main()
