"""Nb4: genome-wide visual aids and explicitly exploratory functional enrichment."""
from datetime import datetime, timezone
import importlib.util
import sys
import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.stats import hypergeom
from statsmodels.stats.multitest import multipletests
from sklearn.decomposition import PCA
import sklearn
import anndata as ad
import umap
import gseapy
from common import PACKAGE, REPO, read_json, write_json, new_run, finish_record, sha256


def collapse(counts,names):
    return pd.DataFrame(counts,columns=names).T.groupby(level=0,sort=True).sum().T


def main():
    cfg=read_json(PACKAGE/'config/extended_visual_v1.json')
    out=new_run(PACKAGE/'runs/extended_visual_v1')
    cache=REPO/'raw_data/travaglini_nabhan_2020/prepared'
    helper=REPO/'Research Article/gate1_01_niethamer_2025/trials/gsea_utils.py'
    spec=importlib.util.spec_from_file_location('gu',helper);gu=importlib.util.module_from_spec(spec);spec.loader.exec_module(gu)
    libraries={name:REPO/'raw_data/msigdb'/filename for name,filename in [('hallmark','h.all.v2024.1.Hs.symbols.gmt'),('gobp','c5.go.bp.v2024.1.Hs.symbols.gmt')]}
    sets={k:gu.read_gmt(p) for k,p in libraries.items()}
    facts={k:gu.gene_set_facts(p) for k,p in libraries.items()}
    facts['reused_helper']={'path':helper.relative_to(REPO).as_posix(),'sha256':sha256(helper)}
    write_json(out/'gene_set_sources.json',facts)
    source=next(s for s in read_json(PACKAGE/'config/expression_sources_v1.json')['files'] if s['assay']=='10x')
    assert sha256(REPO/source['cache_path'])==source['sha256']
    obj=ad.read_h5ad(REPO/source['cache_path'],backed='r')
    meta=pd.read_csv(cache/'cell_metadata.tsv',sep='\t',keep_default_na=False).query('assay=="10x"').reset_index(drop=True)
    assert list(meta.cell_id)==list(obj.obs_names)
    lung=np.flatnonzero(meta.tissue=='lung')
    tsne=meta.loc[lung,['cell_id','donor_id','anatomical_region','source_compartment','author_cell_type']].copy()
    coords=np.asarray(obj.obsm['X_tSNE'])[lung]
    tsne['tSNE1']=coords[:,0];tsne['tSNE2']=coords[:,1]
    tsne.to_csv(out/'deposited_tsne.tsv',sep='\t',index=False,float_format='%.7g')
    ids=np.flatnonzero((meta.tissue=='lung')&(meta.source_compartment=='stromal'))
    m=meta.loc[ids].reset_index(drop=True)
    x=obj.raw.X[ids,:].astype(np.float64).tocsr();names=obj.raw.var.feature_name.astype(str).to_numpy()
    totals=np.asarray(x.sum(axis=1)).ravel()
    norm=x.multiply((1e4/totals)[:,None]).tocsr();norm.data=np.log1p(norm.data)
    means=np.asarray(norm.mean(axis=0)).ravel();var=np.asarray(norm.multiply(norm).mean(axis=0)).ravel()-means**2
    detected=np.asarray((x>0).sum(axis=0)).ravel()
    eligible=(detected>=10)&~pd.Series(names).str.match(r'^(MT-|RPL|RPS)').to_numpy()
    dispersion=np.log1p(var/np.maximum(means,1e-12));bins=pd.qcut(pd.Series(means[eligible]),20,labels=False,duplicates='drop')
    frame=pd.DataFrame({'index':np.flatnonzero(eligible),'bin':bins,'dispersion':dispersion[eligible]})
    frame['score']=frame.groupby('bin').dispersion.transform(lambda v:(v-v.mean())/max(v.std(),1e-12))
    hvg=frame.sort_values(['score','index'],ascending=[False,True],kind='stable').head(1500)['index'].to_numpy()
    pca=PCA(n_components=30,svd_solver='randomized',random_state=20261002)
    pcs=pca.fit_transform(norm[:,hvg].toarray())
    print(f'Embedding {len(m)} stromal cells using {len(hvg)} genes and 30 PCs.',flush=True)
    xy=umap.UMAP(**cfg['embedding']['umap']).fit_transform(pcs)
    embedding=m[['cell_id','donor_id','anatomical_region','author_cell_type']].copy()
    embedding['UMAP1']=xy[:,0];embedding['UMAP2']=xy[:,1]
    embedding['log1p_C3_CP10K']=np.asarray(norm[:,np.flatnonzero(names=='C3')].sum(axis=1)).ravel()
    embedding.to_csv(out/'stromal_umap.tsv',sep='\t',index=False,float_format='%.7g')
    pd.DataFrame({'stable_id':obj.raw.var.index[hvg],'gene':names[hvg],'dispersion_score':frame.set_index('index').loc[hvg,'score']}).to_csv(out/'embedding_genes.tsv',sep='\t',index=False)
    write_json(out/'embedding_model.json',{'n_cells':len(m),'genes':len(hvg),'pca_variance_ratio':pca.explained_variance_ratio_.tolist(),'umap':cfg['embedding']['umap'],'no_batch_correction':True})
    labels=['Alveolar Fibroblast','Adventitial Fibroblast'];s_counts=[];s_meta=[]
    for donor in ['P1','P2','P3']:
        indices=[np.flatnonzero((m.donor_id==donor)&(m.anatomical_region=='distal')&(m.author_cell_type==label)) for label in labels]
        if min(map(len,indices))<20:continue
        for label,idx in zip(labels,indices):
            s_counts.append(np.asarray(x[idx].sum(axis=0)).ravel());s_meta.append({'donor_id':donor,'subtype':'alveolar' if label==labels[0] else 'adventitial','n_cells':len(idx),'n_strata':1})
    source_counts=collapse(np.vstack(s_counts),names)
    source_cpm=source_counts.to_numpy()/source_counts.sum(axis=1).to_numpy()[:,None]*1e6
    s_log=pd.DataFrame(np.log2(source_cpm+1),columns=source_counts.columns)
    obj.file.close()
    external=read_json(PACKAGE/'config/external_source_v1.json')
    assert sha256(REPO/external['cache_path'])==external['sha256']
    obj=ad.read_h5ad(REPO/external['cache_path'],backed='r')
    obs=obj.obs.reset_index(names='cell_id');coverage=pd.read_csv(PACKAGE/'runs/external_pilot_v1/stratum_coverage.tsv',sep='\t')
    coverage=coverage[(coverage.suspension_type=='cell')&coverage.primary_eligible]
    e_cfg=read_json(PACKAGE/'config/external_pilot_v1.json');all_idx=[];e_meta=[]
    for row in coverage.to_dict('records'):
        mask=np.ones(len(obs),dtype=bool)
        for field in e_cfg['matching_fields']:mask &= obs[field].astype(str).to_numpy()==str(row[field])
        for label,subtype in [(e_cfg['left_label'],'alveolar'),(e_cfg['right_label'],'adventitial')]:
            idx=np.flatnonzero(mask&(obs.Celltypes.to_numpy()==label)&(obs.disease.to_numpy()=='normal'))
            all_idx.append(idx);e_meta.append({**{f:row[f] for f in e_cfg['matching_fields']},'subtype':subtype,'n_cells':len(idx)})
    e_counts=np.vstack([np.asarray(obj.raw.X[idx,:].sum(axis=0)).ravel() for idx in all_idx])
    external_counts=collapse(e_counts,obj.raw.var.feature_name.astype(str).to_numpy());obj.file.close()
    e_cpm=external_counts.to_numpy()/external_counts.sum(axis=1).to_numpy()[:,None]*1e6
    e_log=np.log2(e_cpm+1);e_m=pd.DataFrame(e_meta);external_profiles=[];external_meta=[]
    for key,idx in e_m.groupby(['donor_id','subtype'],sort=True).groups.items():
        external_profiles.append(e_log[list(idx)].mean(axis=0));external_meta.append({'donor_id':key[0],'subtype':key[1],'n_cells':int(e_m.loc[idx,'n_cells'].sum()),'n_strata':len(idx)})
    e_log=pd.DataFrame(external_profiles,columns=external_counts.columns)
    cohorts={'source':(s_log,pd.DataFrame(s_meta)),'external':(e_log,pd.DataFrame(external_meta))}
    summaries={};eligible_sets={}
    for cohort,(log,design) in cohorts.items():
        delta=[];mean_expr=[];expressed=[]
        for donor,ids in design.groupby('donor_id').groups.items():
            left=next(i for i in ids if design.loc[i,'subtype']=='alveolar');right=next(i for i in ids if design.loc[i,'subtype']=='adventitial')
            delta.append(log.iloc[left].to_numpy()-log.iloc[right].to_numpy())
            expressed.append((log.iloc[left].to_numpy()>=1)|(log.iloc[right].to_numpy()>=1))
        delta=np.vstack(delta);n=2 if cohort=='source' else 3
        eligible_sets[cohort]=set(log.columns[np.vstack(expressed).sum(axis=0)>=n])
        summaries[cohort]=pd.DataFrame({'gene':log.columns,'mean_delta':delta.mean(axis=0),'min_delta':delta.min(axis=0),'max_delta':delta.max(axis=0),'positive_donors':(delta>0).sum(axis=0),'negative_donors':(delta<0).sum(axis=0),'mean_expression':log.mean(axis=0).to_numpy(),'n_donors':len(delta)})
    universe=eligible_sets['source']&eligible_sets['external']
    write_json(out/'gene_universe.json',{'rule':cfg['gene_universe'],'source_eligible':len(eligible_sets['source']),'external_eligible':len(eligible_sets['external']),'common_eligible':len(universe),'genes':sorted(universe)})
    gsea_frames=[];ora_frames=[];complement=[];curves=[];pca_rows=[];pca_models={}
    for cohort,(log,design) in cohorts.items():
        ranking=summaries[cohort].query('gene in @universe').sort_values(['mean_delta','gene'],ascending=[False,True],kind='stable').reset_index(drop=True)
        ranking.to_csv(out/(cohort+'_gene_ranking.tsv'),sep='\t',index=False,float_format='%.8g')
        design.to_csv(out/(cohort+'_pseudobulk_units.tsv'),sep='\t',index=False)
        common=log.loc[:,sorted(universe)];variable=common.var(axis=0).sort_values(ascending=False,kind='stable').head(2000).index
        model=PCA(n_components=2,svd_solver='full');xy=model.fit_transform(common.loc[:,variable])
        design=design.copy();design['cohort']=cohort;design['PC1']=xy[:,0];design['PC2']=xy[:,1];pca_rows.append(design)
        pca_models[cohort]={'genes':len(variable),'variance_ratio':model.explained_variance_ratio_.tolist(),'n_units':len(design)}
        np.savez_compressed(cache/(cohort+'_genomewide_profiles.npz'),log_cpm=log.to_numpy(),genes=log.columns.to_numpy(dtype=str))
        print(f'{cohort}: {len(ranking)} genes, {len(design)//2} donors; Hallmark GSEA and GO BP ORA.',flush=True)
        result=gseapy.prerank(rnk=ranking[['gene','mean_delta']],gene_sets={k:sorted(v) for k,v in sets['hallmark'].items()},permutation_num=1000,min_size=15,max_size=500,seed=20261002,threads=2,outdir=None,weight=1,verbose=False)
        gsea=result.res2d.copy();gsea.insert(0,'cohort',cohort);gsea_frames.append(gsea)
        scores=ranking.mean_delta.to_numpy();hit=ranking.gene.isin(sets['hallmark']['HALLMARK_COMPLEMENT']).to_numpy()
        es=gu.enrichment_score(scores,hit)
        recorded=float(gsea.loc[gsea.Term=='HALLMARK_COMPLEMENT','ES'].iloc[0])
        np.testing.assert_allclose(es,recorded,atol=1e-6,rtol=0)
        null=gu.matched_random_null(scores,ranking.mean_expression.to_numpy(),hit,1000,np.random.default_rng(20261002))
        complement.append({'cohort':cohort,'ES':es,'set_size':int(hit.sum()),'expression_matched_two_sided_p':(1+int((np.abs(null)>=abs(es)).sum()))/1001,'draws':1000,'null':'expression-matched random sets, not donor-label permutations'})
        step=np.where(hit,np.abs(scores),0);step=step/step.sum()-np.where(hit,0,1/(len(scores)-hit.sum()));running=np.cumsum(step)
        curves.extend({'cohort':cohort,'rank':i+1,'gene':ranking.gene.iloc[i],'score':scores[i],'hit':bool(hit[i]),'running_ES':running[i]} for i in range(len(scores)))
        rows=[]
        for direction in ['alveolar','adventitial']:
            if direction=='alveolar':foreground=set(ranking.loc[(ranking.mean_delta>=1)&(ranking.positive_donors>=(2 if cohort=='source' else 3)),'gene'])
            else:foreground=set(ranking.loc[(ranking.mean_delta<=-1)&(ranking.negative_donors>=(2 if cohort=='source' else 3)),'gene'])
            for term,genes in sets['gobp'].items():
                members=genes&universe
                if not 15<=len(members)<=500:continue
                overlap=members&foreground;k=len(overlap);n=len(foreground)
                rows.append({'cohort':cohort,'direction':direction,'term':term,'overlap':k,'set_size':len(members),'foreground_size':n,'background_size':len(universe),'gene_ratio':k/n if n else 0,'p_hypergeom':float(hypergeom.sf(k-1,len(universe),len(members),n)),'overlap_genes':';'.join(sorted(overlap))})
        ora=pd.DataFrame(rows);ora['q_BH_cohort_both_directions']=multipletests(ora.p_hypergeom,method='fdr_bh')[1];ora_frames.append(ora)
    pd.concat(gsea_frames).to_csv(out/'hallmark_gsea.tsv',sep='\t',index=False,float_format='%.8g')
    pd.concat(ora_frames).to_csv(out/'go_bp_ora.tsv',sep='\t',index=False,float_format='%.8g')
    pd.DataFrame(complement).to_csv(out/'complement_matched_null.tsv',sep='\t',index=False,float_format='%.8g')
    pd.DataFrame(curves).to_csv(out/'complement_running_curves.tsv',sep='\t',index=False,float_format='%.8g')
    pd.concat(pca_rows).to_csv(out/'pseudobulk_pca.tsv',sep='\t',index=False,float_format='%.8g')
    write_json(out/'pseudobulk_pca_models.json',pca_models)
    finish_record(out,{'schema':'Nb4-extended-visual-run/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'exploratory embedding, PCA, GSEA and GO complete','software':{'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__,'umap':umap.__version__,'gseapy':gseapy.__version__},'gene_set_sources':facts,'profile_hashes':{p.name:sha256(p) for p in cache.glob('*_genomewide_profiles.npz')},'scope':'all enrichment p/q values refer to competitive gene-set/annotation nulls, not biological donor-population inference'})
    print('Nb4 extended analysis complete.',flush=True)


if __name__=='__main__':main()
