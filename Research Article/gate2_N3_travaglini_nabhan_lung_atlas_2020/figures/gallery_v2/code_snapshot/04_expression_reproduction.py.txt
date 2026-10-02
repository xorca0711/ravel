"""Bounded source displays and donor/assay/region effects from verified raw counts."""
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
import scipy.sparse as sp
import anndata as ad
import h5py
from common import PACKAGE, REPO, read_json, write_json, new_run, finish_record, sha256


def csr_block(group, start, end):
    if group.attrs['encoding-type'] != 'csr_matrix':
        raise ValueError('Expected CSR count storage')
    pointers = group['indptr'][start:end + 1]
    lo, hi = int(pointers[0]), int(pointers[-1])
    return sp.csr_matrix((group['data'][lo:hi].astype(np.float64), group['indices'][lo:hi], pointers - lo), shape=(end-start, int(group.attrs['shape'][1])))


def summaries(meta, counts, source_log, totals, genes, assay, group_fields):
    table = []
    scale = 10000 if assay == '10x' else 1000000
    log = np.log1p(counts / totals[:, None] * scale)
    for key, ids in meta.groupby(group_fields, observed=True, sort=True).indices.items():
        key = key if isinstance(key, tuple) else (key,)
        n = len(ids); summed = counts[ids].sum(axis=0)
        bulk = np.log2(summed / totals[ids].sum() * 1e6 + 1)
        detection = (counts[ids] > 0).mean(axis=0)
        means = log[ids].mean(axis=0); original_means = source_log[ids].mean(axis=0)
        for j, gene in enumerate(genes):
            table.append({**dict(zip(group_fields, key)), 'assay':assay, 'gene':gene, 'n_cells':n, 'sum_counts':summed[j], 'sum_library_counts':totals[ids].sum(), 'log2CPM_plus1':bulk[j], 'detection_fraction':detection[j], 'mean_log_normalized':means[j], 'mean_source_X':original_means[j], 'mean_library_counts':totals[ids].mean()})
    return pd.DataFrame(table)


def main():
    cfg=read_json(PACKAGE/'config/execution_v1.json')
    sources=read_json(PACKAGE/'config/expression_sources_v1.json')
    out=new_run(PACKAGE/'runs/reproduction_v1')
    cache=REPO/'raw_data/travaglini_nabhan_2020/prepared'
    metadata=pd.read_csv(cache/'cell_metadata.tsv',sep='\t',keep_default_na=False)
    requested=sorted({g for panel in cfg['panels'].values() for g in panel})
    all_tables=[]; pooled_tables=[]; semantics=[]; gene_maps=[]
    for source in sources['files']:
        assay=source['assay']; path=REPO/source['cache_path']
        if sha256(path)!=source['sha256']:raise ValueError('Source hash mismatch')
        obj=ad.read_h5ad(path,backed='r'); names=obj.raw.var['feature_name'].astype(str)
        meta=metadata[metadata.assay==assay].reset_index(drop=True)
        if list(meta.cell_id)!=list(obj.obs_names):raise ValueError('Cell order mismatch')
        lookup={g:np.where(names.to_numpy()==g)[0] for g in requested}
        genes=[g for g in requested if len(lookup[g])]
        for gene in requested:
            gene_maps.append({'assay':assay,'gene':gene,'stable_ids':';'.join(names.index[lookup[gene]]),'n_columns':len(lookup[gene]),'status':'present' if len(lookup[gene]) else 'missing'})
        x_names=obj.var['feature_name'].astype(str)
        x_lookup={g:np.where(x_names.to_numpy()==g)[0] for g in genes}
        counts=np.zeros((len(meta),len(genes))); original=np.zeros_like(counts); totals=np.zeros(len(meta)); detected=np.zeros(len(meta),dtype=int)
        noninteger=0; nonfinite=0; negative=0
        with h5py.File(path,'r') as handle:
            for start in range(0,len(meta),1024):
                end=min(start+1024,len(meta)); block=csr_block(handle['raw/X'],start,end)
                values=block.data
                noninteger+=int(np.sum(np.abs(values-np.rint(values))>1e-6)); nonfinite+=int(np.sum(~np.isfinite(values))); negative+=int(np.sum(values<0))
                totals[start:end]=np.asarray(block.sum(axis=1)).ravel();detected[start:end]=np.asarray((block>0).sum(axis=1)).ravel()
                xb=csr_block(handle['X'],start,end)
                for j,gene in enumerate(genes):
                    counts[start:end,j]=np.asarray(block[:,lookup[gene]].sum(axis=1)).ravel()
                    original[start:end,j]=np.asarray(xb[:,x_lookup[gene]].sum(axis=1)).ravel() if len(x_lookup[gene]) else np.nan
        if noninteger or nonfinite or negative or np.any(totals<=0):raise ValueError('Raw count semantics fail')
        np.savez_compressed(cache/f'{assay}_selected_counts.npz',counts=counts,original=original,totals=totals,detected=detected,genes=np.asarray(genes),cell_ids=meta.cell_id.to_numpy(dtype=str))
        unit=summaries(meta,counts,original,totals,genes,assay,['donor_id','tissue','anatomical_region','author_cell_type'])
        pooled=summaries(meta,counts,original,totals,genes,assay,['author_cell_type'])
        all_tables.append(unit);pooled_tables.append(pooled)
        raw_log=np.log1p(counts/totals[:,None]*(10000 if assay=='10x' else 1e6))
        obs_total=obj.obs['nReads' if assay=='SS2' else 'nUMI'].to_numpy()
        semantics.append({'assay':assay,'cells':len(meta),'raw_genes':len(names),'selected_genes':len(genes),'missing_genes':sorted(set(requested)-set(genes)),'integer_violations':noninteger,'negative_entries':negative,'nonfinite_entries':nonfinite,'count_total_min':float(totals.min()),'count_total_median':float(np.median(totals)),'count_total_max':float(totals.max()),'median_curated_sum_over_source_library':float(np.median(totals/obs_total)),'max_abs_selected_log_normalization_difference_to_X':float(np.nanmax(np.abs(raw_log-original))),'mean_abs_selected_log_normalization_difference_to_X':float(np.nanmean(np.abs(raw_log-original))),'interpretation':'raw/X is numerically count-like and assay-labeled; source X retained separately; curated gene universe may differ from original source universe'})
        obj.file.close();print(f'{assay}: {len(meta)} cells, {len(genes)} selected genes, raw count checks passed.',flush=True)
    units=pd.concat(all_tables,ignore_index=True);pooled=pd.concat(pooled_tables,ignore_index=True)
    units.to_csv(out/'unit_expression.tsv',sep='\t',index=False,float_format='%.8g')
    pooled.to_csv(out/'source_pooled_expression.tsv',sep='\t',index=False,float_format='%.8g')
    pd.DataFrame(gene_maps).to_csv(out/'gene_mapping.tsv',sep='\t',index=False)
    write_json(out/'matrix_semantics.json',semantics)
    effects=[]
    for contrast in cfg['contrasts']:
        selected=set(g for name in contrast['panels'] for g in cfg['panels'][name])
        subset=units[(units.tissue=='lung') & units.gene.isin(selected)]
        left=subset[subset.author_cell_type==contrast['left']]
        right=subset[subset.author_cell_type==contrast['right']]
        paired=left.merge(right,on=['donor_id','assay','anatomical_region','gene'],suffixes=('_left','_right'))
        for r in paired.to_dict('records'):
            effects.append({'contrast':contrast['id'],'assay':r['assay'],'donor_id':r['donor_id'],'anatomical_region':r['anatomical_region'],'gene':r['gene'],'n_left':r['n_cells_left'],'n_right':r['n_cells_right'],'delta_log2CPM':r['log2CPM_plus1_left']-r['log2CPM_plus1_right'],'delta_detection':r['detection_fraction_left']-r['detection_fraction_right'],'delta_mean_log':r['mean_log_normalized_left']-r['mean_log_normalized_right'],'primary_count_eligible':min(r['n_cells_left'],r['n_cells_right'])>=cfg['primary_cell_floor']})
    effects=pd.DataFrame(effects);effects.to_csv(out/'paired_effects.tsv',sep='\t',index=False,float_format='%.8g')
    result=[]
    for key, frame in effects[effects.primary_count_eligible].groupby(['contrast','assay','anatomical_region','gene'],sort=True):
        v=frame.delta_log2CPM.to_numpy();n=len(v)
        result.append(dict(zip(['contrast','assay','anatomical_region','gene'],key))|{'n_donors':n,'donors':','.join(frame.donor_id),'mean_delta_log2CPM':v.mean(),'min_delta_log2CPM':v.min(),'max_delta_log2CPM':v.max(),'positive_donors':int((v>0).sum()),'negative_donors':int((v<0).sum()),'coverage_status':'three_donor_description' if n>=3 else 'coverage_hold_descriptive_only'})
    pd.DataFrame(result).to_csv(out/'contrast_summary.tsv',sep='\t',index=False,float_format='%.8g')
    finish_record(out,{'schema':'TN2020-reproduction/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'bounded source reconstruction and descriptive estimates complete','expression_analysis_run':True,'selected_gene_count':len(requested),'normalization_caveat':'curated raw universe and source X retained distinctly','cache_hashes':{p.name:sha256(p) for p in cache.glob('*_selected_counts.npz')}})
    print(f'Wrote {len(units)} unit/gene summaries and {len(effects)} matched donor/gene effects; no population p-values.')


if __name__=='__main__':main()
