"""Independent numerical spot checks, artifact integrity and package links."""
import ast
from datetime import datetime, timezone
import importlib.util
import re
from urllib.parse import unquote
import numpy as np
import pandas as pd
import anndata as ad
from scipy.stats import hypergeom
from statsmodels.stats.multitest import multipletests
from pypdf import PdfReader
from common import PACKAGE, REPO, read_json, write_json, new_run, finish_record, sha256


def main():
    checks=[]
    def passed(name, detail):checks.append({'check':name,'status':'pass','detail':detail})
    records=list((PACKAGE/'runs').glob('*/run_record.json'))+list((PACKAGE/'figures').glob('*/run_record.json'))
    output_count=0
    for path in records:
        record=read_json(path)
        for name,digest in record['outputs'].items():
            assert sha256(path.parent/name)==digest,(path,name)
            output_count+=1
        for name,digest in record['code_sha256'].items():
            snapshot=path.parent/'code_snapshot'/(name+'.txt')
            assert sha256(snapshot if snapshot.exists() else PACKAGE/'scripts'/name)==digest,(path,name)
        for name,digest in record['config_sha256'].items():
            assert sha256(PACKAGE/'config'/name)==digest,(path,name)
    passed('frozen_records',f'{len(records)} existing runs; {output_count} outputs and all recorded code/config hashes')
    for path in (PACKAGE/'scripts').glob('*.py'):ast.parse(path.read_text(encoding='utf-8'))
    passed('python_syntax','All current package scripts parse')
    spec=importlib.util.spec_from_file_location('follow',PACKAGE/'scripts/06_followup_analysis.py')
    follow=importlib.util.module_from_spec(spec);spec.loader.exec_module(follow)
    totals=np.array([1000,1001,10000,1000000],dtype=float)
    counts=np.array([[0,1,10,n-1,n] for n in totals])
    expected=hypergeom.sf(0,totals[:,None],counts,1000)
    actual=follow.expected_detection(counts,totals,1000)
    np.testing.assert_allclose(actual,expected,rtol=1e-7,atol=1e-8)
    passed('hypergeometric_math','20 boundary/large-library cases agree with scipy.stats.hypergeom.sf to 1e-8 absolute tolerance')
    cache=REPO/'raw_data/travaglini_nabhan_2020/prepared'
    metadata=pd.read_csv(cache/'cell_metadata.tsv',sep='\t',keep_default_na=False)
    sources=read_json(PACKAGE/'config/expression_sources_v1.json')['files']
    selected_genes=['C3','MYRF','TBX5','WIF1']
    unit=pd.read_csv(PACKAGE/'runs/reproduction_v1/unit_expression.tsv',sep='\t')
    for source in sources:
        assert sha256(REPO/source['cache_path'])==source['sha256']
        obj=ad.read_h5ad(REPO/source['cache_path'],backed='r')
        bundle=np.load(cache/(source['assay']+'_selected_counts.npz'))
        indices=np.array([0,len(obj.obs)//3,len(obj.obs)-1])
        direct=obj.raw.X[indices,:]
        np.testing.assert_array_equal(np.asarray(direct.sum(axis=1)).ravel(),bundle['totals'][indices])
        for gene in selected_genes:
            columns=np.flatnonzero(obj.raw.var.feature_name.to_numpy()==gene)
            j=list(bundle['genes']).index(gene)
            np.testing.assert_array_equal(np.asarray(direct[:,columns].sum(axis=1)).ravel(),bundle['counts'][indices,j])
        m=metadata[metadata.assay==source['assay']].reset_index(drop=True)
        for gene,label in [('C3','Adventitial Fibroblast'),('MYRF','Alveolar Epithelial Type 1')]:
            ids=np.flatnonzero((m.donor_id=='P1')&(m.anatomical_region=='distal')&(m.author_cell_type==label)&(m.tissue=='lung'))
            block=obj.raw.X[ids,:]
            columns=np.flatnonzero(obj.raw.var.feature_name.to_numpy()==gene)
            direct_bulk=np.log2(float(block[:,columns].sum())/float(block.sum())*1e6+1)
            row=unit[(unit.assay==source['assay'])&(unit.donor_id=='P1')&(unit.anatomical_region=='distal')&(unit.author_cell_type==label)&(unit.gene==gene)&(unit.tissue=='lung')]
            assert len(row)==1
            np.testing.assert_allclose(direct_bulk,row.log2CPM_plus1.iloc[0],atol=1e-6,rtol=0)
        obj.file.close()
    passed('source_count_spot_checks','Independent AnnData reads: six full cell-library sums, 24 gene counts, four donor/type pseudobulks agree')
    external=read_json(PACKAGE/'config/external_source_v1.json')
    assert sha256(REPO/external['cache_path'])==external['sha256']
    obj=ad.read_h5ad(REPO/external['cache_path'],backed='r')
    frame=pd.read_csv(PACKAGE/'runs/external_pilot_v1/stratum_effects.tsv',sep='\t')
    row=frame[(frame.gene=='C3')&(frame.suspension_type=='cell')&(frame.n_left>=20)&(frame.n_right>=20)].iloc[0]
    cfg=read_json(PACKAGE/'config/external_pilot_v1.json')
    m=obj.obs;mask=np.ones(len(m),dtype=bool)
    for field in cfg['matching_fields']:mask &= m[field].astype(str).to_numpy()==str(row[field])
    col=np.flatnonzero(obj.raw.var.feature_name.to_numpy()=='C3')
    values=[]
    for label in [cfg['left_label'],cfg['right_label']]:
        ids=np.flatnonzero(mask&(m.Celltypes.to_numpy()==label)&(m.disease.to_numpy()=='normal'))
        block=obj.raw.X[ids,:]
        values.append(np.log2(float(block[:,col].sum())/float(block.sum())*1e6+1))
    np.testing.assert_allclose(values[0]-values[1],row.delta_log2CPM,atol=1e-6,rtol=0)
    obj.file.close()
    donors=pd.read_csv(PACKAGE/'runs/external_pilot_v1/donor_effects.tsv',sep='\t')
    primary=donors[(donors.cell_floor==20)&(donors.gene=='C3')]
    assert primary[primary.suspension_type=='cell'].donor_id.nunique()==4
    assert primary[primary.suspension_type=='nucleus'].donor_id.nunique()==2
    assert (primary.mean_delta_log2CPM<0).all()
    passed('external_count_and_units','Independent raw C3 stratum calculation; four primary cell donors and two separate nuclear donors')
    extended=PACKAGE/'runs/extended_visual_v1'
    external_summary=pd.read_csv(PACKAGE/'runs/external_pilot_v1/summary.tsv',sep='\t')
    source_effects=pd.read_csv(PACKAGE/'runs/reproduction_v1/paired_effects.tsv',sep='\t')
    for cohort in ['source','external']:
        rank=pd.read_csv(extended/(cohort+'_gene_ranking.tsv'),sep='\t').set_index('gene')
        assert len(rank)==11113 and rank.index.is_unique
        assert np.isfinite(rank.mean_delta).all()
        for gene in ['C3','CXCL2','IL32','CCL2','CXCL12','SPINT2','SFRP2','GPC3','PI16']:
            if cohort=='source':
                frame=source_effects[(source_effects.contrast=='fibroblast_identity')&(source_effects.assay=='10x')&(source_effects.anatomical_region=='distal')&source_effects.primary_count_eligible&(source_effects.gene==gene)]
                value=frame.delta_log2CPM.mean()
            else:value=external_summary[(external_summary.suspension_type=='cell')&(external_summary.cell_floor==20)&(external_summary.gene==gene)].mean_delta_log2CPM.iloc[0]
            np.testing.assert_allclose(rank.loc[gene,'mean_delta'],value,atol=1e-6,rtol=0)
    go=pd.read_csv(extended/'go_bp_ora.tsv',sep='\t')
    p=hypergeom.sf(go.overlap-1,go.background_size,go.set_size,go.foreground_size)
    np.testing.assert_allclose(p,go.p_hypergeom,rtol=1e-6,atol=1e-12)
    for cohort,frame in go.groupby('cohort'):
        q=multipletests(frame.p_hypergeom,method='fdr_bh')[1]
        np.testing.assert_allclose(q,frame.q_BH_cohort_both_directions,rtol=1e-6,atol=1e-12)
    diag=pd.read_csv(PACKAGE/'figures/extended_v2/gsea_tie_diagnostic.tsv',sep='\t')
    assert len(diag)==98 and diag.engine_input_difference.max()<1e-6
    assert diag.absolute_tie_change.max()<.001
    u=pd.read_csv(extended/'stromal_umap.tsv',sep='\t')
    assert len(u)==5033 and u.cell_id.is_unique and np.isfinite(u[['UMAP1','UMAP2']]).all().all()
    assert len(PdfReader(PACKAGE/'figures/gallery_v2/Nb4_figure_atlas.pdf').pages)==12
    passed('extended_analysis','18 focal rank effects agree with prior independent calculations; all GO p/BH q recomputed; 98 GSEA scores independently checked; finite unique UMAP coordinates; 12-page atlas')
    out=new_run(PACKAGE/'runs/validation_v1')
    write_json(out/'checks.json',checks)
    linked=0
    for path in PACKAGE.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            target=target.strip('<>').split('#')[0]
            if not target or re.match(r'\w+://',target):continue
            assert (path.parent/unquote(target)).exists(),(path,target)
            linked+=1
    passed('package_links',f'{linked} local Markdown targets exist')
    write_json(out/'checks.json',checks)
    finish_record(out,{'schema':'TN2020-validation/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'independent numeric and artifact checks passed'})
    print(f'{len(checks)} validation groups passed; {output_count} immutable outputs verified.')


if __name__=='__main__':main()
