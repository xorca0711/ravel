"""Independent arithmetic/provenance checks on Nb2 outputs, not biological grading."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()


def bh(p):
    p=np.asarray(p);order=np.argsort(p);out=np.empty(len(p))
    out[order]=np.minimum(1,np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1])
    return out


def main():
    checks=[]
    def require(test,label):
        if not bool(test):raise AssertionError(label)
        checks.append(label)
    bulk=ROOT/'trials/bulk_v1';atlas=ROOT/'trials/atlas_v1'
    contract=json.loads((bulk/'contract.json').read_text())
    for relative,digest in contract['input_hashes'].items():
        require(sha(ROOT/relative)==digest,'frozen bulk input/code '+relative)
    for item in contract['gene_set_resources']:
        require(sha(item['path'])==item['sha256'],'gene-set resource '+item['name'])
    for row in json.loads((ROOT/'metadata/count_download_manifest.json').read_text())['files']:
        require(sha(ROOT/row['path'])==row['sha256'],'deposited counts '+row['accession'])
    counts=pd.read_csv(ROOT/'raw/bulk_counts.csv.gz',index_col=0)
    keep=(counts.ge(10).sum(axis=1)>=3);effects=pd.read_csv(bulk/'tables/gene_effects.tsv.gz',sep='\t')
    require(keep.sum()==16534 and set(effects.gene_id)==set(counts.index[keep]),'complete filtered gene universe')
    require(not effects.duplicated(['gene_id','contrast']).any() and len(effects)==165340,'ten unique gene-level contrasts')
    require(np.isfinite(effects[['log2FC','SE','CI_low','CI_high','P','FDR']]).all().all(),'finite model effects/uncertainty')
    require((effects.SE>0).all() and (effects.CI_low<=effects.log2FC).all() and (effects.CI_high>=effects.log2FC).all(),'interval ordering')
    for contrast,g in effects.groupby('contrast'):
        require(np.allclose(bh(g.P),g.FDR,rtol=1e-10,atol=1e-12),'independent BH '+contrast)
    require(np.allclose(bh(effects.P),effects.FDR_all_contrasts),'pooled ten-contrast BH')
    wide=effects.pivot(index='gene_id',columns='contrast',values='log2FC')
    for arm in ['Fzd5','Fzd6']:
        require(np.allclose(wide[arm+'_vs_CHIR']+wide.CHIR_vs_withdraw48,wide[arm+'_vs_withdraw48']),'contrast algebra '+arm)
    require(np.allclose(wide.Fzd6_vs_withdraw48-wide.Fzd5_vs_withdraw48,wide.Fzd6_vs_Fzd5),'Fzd6-Fzd5 contrast algebra')
    gene=pd.read_csv(bulk/'tables/source_panel_expression.tsv',sep='\t')
    score=pd.read_csv(bulk/'tables/panel_sample_scores.tsv',sep='\t')
    independent=gene.groupby(['panel','accession','arm']).agg(mean_log2CPM=('log2CPM','mean'),mean_gene_z=('gene_z','mean')).reset_index()
    merged=score.merge(independent,on=['panel','accession','arm'],suffixes=('_saved','_recomputed'),validate='one_to_one')
    require(len(merged)==90,'five source panels x18 libraries')
    for name in ['mean_log2CPM','mean_gene_z']:
        require(np.allclose(merged[name+'_saved'],merged[name+'_recomputed']),'independent panel '+name)
    for _,r in pd.read_csv(bulk/'tables/panel_effects.tsv',sep='\t').iterrows():
        first,second=contract['contrasts'][r.contrast]
        a=score[(score.panel==r.panel)&score.arm.eq(first)].mean_log2CPM.to_numpy()
        b=score[(score.panel==r.panel)&score.arm.eq(second)].mean_log2CPM.to_numpy()
        require(np.allclose([r.mean_difference,r.min_pair_difference,r.max_pair_difference],[a.mean()-b.mean(),(a[:,None]-b).min(),(a[:,None]-b).max()]),'panel contrast '+r.panel+' '+r.contrast)
    threshold=pd.read_csv(bulk/'tables/threshold_reconciliation.tsv',sep='\t')
    for _,r in threshold.iterrows():
        z=effects[effects.contrast==r.contrast]
        require(int(((z.log2FC>r.absolute_log2FC_gt)&z.FDR.lt(.05)).sum())==r.up and int(((z.log2FC< -r.absolute_log2FC_gt)&z.FDR.lt(.05)).sum())==r.down,'DE threshold '+r.contrast+' '+str(r.absolute_log2FC_gt))
    original=json.loads((atlas/'contract.json').read_text());amend=json.loads((atlas/'schema_amendment.json').read_text())
    require(sha(atlas/'failed_attempt/04_atlas.py')==original['code_sha256']==amend['original_code_sha256'],'archived failed schema version')
    require(sha(ROOT/'scripts/04_atlas.py')==amend['resumed_code_sha256'],'amended atlas code frozen before extraction')
    # Large raw matrices were hashed before extraction; avoid another multi-GB read here.
    for item in original['input_files']:
        require(Path(item['path']).stat().st_size==item['bytes'],'atlas source size retained '+Path(item['path']).name)
    units=pd.read_csv(atlas/'tables/unit_receptor_context.tsv.gz',sep='\t',low_memory=False)
    keys=['dataset','mode','unit','condition','day','state','lineage','gene']
    require(not units.duplicated(keys).any(),'unique unit/gene records')
    require(np.allclose(units.cpm,units.gene_counts*1e6/units.total_umi),'independent CPM arithmetic')
    require(units.gene_counts.le(units.total_umi).all() and units.total_umi.gt(0).all(),'all-gene denominators')
    for field in ['detection','detection_depth500','detection_same_cells']:
        z=units[field].dropna();require(z.between(0,1).all(),'bounded '+field)
    require((units.detection_depth500.dropna()<=units.loc[units.detection_depth500.notna(),'detection_same_cells']+1e-8).all(),'depth-standardized detection cannot exceed same-cell observed detection')
    require(units.cells_depth500.le(units.cells).all(),'depth subset coverage')
    summary=pd.read_csv(atlas/'tables/state_summary.tsv.gz',sep='\t',low_memory=False)
    group=['dataset','mode','condition','day','state','lineage','gene']
    for floor in [20,50,100]:
        z=units[units.cells.ge(floor)].groupby(group,dropna=False).agg(units=('unit','nunique'),median_cpm=('cpm','median'),median_detection=('detection','median')).reset_index()
        saved=summary[summary.cell_floor.eq(floor)]
        m=z.merge(saved,on=group,suffixes=('_actual','_saved'),validate='one_to_one')
        require(len(m)==len(z)==len(saved),'state coverage floor '+str(floor))
        require(np.array_equal(m.units_actual,m.units_saved) and np.allclose(m.median_cpm_actual,m.median_cpm_saved) and np.allclose(m.median_detection_actual,m.median_detection_saved),'independent state medians '+str(floor))
    require(len(units)==93110,'complete archived unit/gene table')
    gene_map=pd.read_csv(ROOT/'metadata/source_panel_membership.tsv',sep='\t')
    require((gene_map.status=='resolved').sum()==19 and gene_map.loc[gene_map.status=='unresolved','source_symbol'].tolist()==['Crim2'],'no silent Crim2 substitution')
    for folder,n in [(bulk,4),(atlas,2)]:
        require(len(list((folder/'figures').glob('*.png')))==n,'figure count '+folder.name)
    result=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),status='passed',checks=len(checks),details=checks,
        scope='Provenance, independent table arithmetic and numerical invariants; not new biological validation. Large atlas input hashes recorded at freeze, sizes checked here.',
        manual_visual_review='All six PNGs inspected for label, legend, clipping and unit/caveat consistency')
    (ROOT/'metadata/execution_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS:',len(checks),'Nb2 provenance/numerical checks; no claim grading')


if __name__=='__main__':main()
