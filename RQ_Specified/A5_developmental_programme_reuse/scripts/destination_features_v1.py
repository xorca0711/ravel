"""Fixed, exposed, mouse-level named-feature screen; writes only runner output."""
import argparse
import gzip
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.io import mmread
from scipy.special import gammaln
from scipy.stats import t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def detection(n, k, budget):
    n, k = np.broadcast_arrays(np.asarray(n, float), np.asarray(k, float))
    if np.any(n < budget) or np.any(k < 0) or np.any(k > n):
        raise ValueError('Invalid rarefaction counts')
    p = np.ones_like(n)
    ok = n-k >= budget
    nn, kk = n[ok], k[ok]
    logq = gammaln(nn-kk+1)-gammaln(nn-kk-budget+1)-gammaln(nn+1)+gammaln(nn-budget+1)
    p[ok] = -np.expm1(np.minimum(logq, 0))
    p[k == 0] = 0
    assert np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all()
    return p


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--output', required=True)
    out = Path(ap.parse_args().output)
    cfg = json.loads(Path('RQ_Specified/A5_developmental_programme_reuse/config/destination_features_spec_v1.json').read_text())
    src = Path(cfg['source_root'])
    def lines(n):
        with gzip.open(src/n, 'rt') as f: return [x.strip() for x in f]
    genes = lines('GSE141259_HighResolution_genes.txt.gz')
    barcodes = lines('GSE141259_HighResolution_barcodes.txt.gz')
    assert len(set(genes)) == len(genes) and len(set(barcodes)) == len(barcodes)
    meta = pd.read_csv(gzip.open(src/'strunz_cells.source'), sep='\t').set_index('cell_barcode')
    assert meta.index.is_unique and set(meta.index) == set(barcodes)
    meta = meta.loc[barcodes].copy()
    assert meta.groupby('sample_id').identifier.nunique().max() == 1
    assert meta.groupby('identifier').sample_id.nunique().max() == 1
    meta['day'] = meta.time_point.str.extract(r'(\d+)').astype(int)
    assert meta.groupby('sample_id').day.nunique().max() == 1
    with gzip.open(src/'GSE141259_HighResolution_rawcounts.mtx.gz', 'rb') as f:
        x = mmread(f).tocsc()
    if x.shape == (len(barcodes), len(genes)): x = x.T.tocsc()
    x.sum_duplicates(); x.eliminate_zeros()
    assert x.shape == (len(genes), len(barcodes))
    assert np.isfinite(x.data).all() and (x.data >= 0).all() and (x.data == np.floor(x.data)).all()
    totals = np.asarray(x.sum(axis=0)).ravel()
    assert set(cfg['genes']) <= set(genes)
    selected = x[[genes.index(g) for g in cfg['genes']], :].toarray()
    meta['depth_pass'] = totals >= cfg['budget']
    in_window = meta.day.between(cfg['day_min'], cfg['day_max']) & ~meta.sample_id.str.startswith(cfg['exclude_sample_prefix'])
    eligible_cells = in_window & meta.depth_pass
    prob = np.full(selected.shape, np.nan)
    prob[:, eligible_cells] = detection(totals[eligible_cells], selected[:, eligible_cells], cfg['budget'])
    support, values = [], []
    for (sample, day, state), group in meta[in_window & meta.cell_type.isin(cfg['states'])].groupby(['sample_id','day','cell_type']):
        ix = meta.index.get_indexer(group.index); good = ix[meta.depth_pass.iloc[ix].to_numpy()]
        ok = len(good) >= cfg['cell_floor']
        support.append(dict(sample_id=sample, day=day, state=state, before_depth=len(ix), after_depth=len(good), eligible=ok))
        if ok:
            for j,gene in enumerate(cfg['genes']):
                values.append(dict(sample_id=sample,day=day,state=state,gene=gene,n_cells=len(good),mean_detection_pp=float(100*prob[j,good].mean())))
    support = pd.DataFrame(support); values = pd.DataFrame(values)
    sets = {s:set(support.loc[(support.state==s)&support.eligible,'sample_id']) for s in cfg['states']}
    common = set.intersection(*(sets[s] for s in cfg['destination_common']))
    paired, summary = [], []
    for name,case,ref,scope in cfg['contrasts']:
        mice = sorted(sets[case] & sets[ref] if scope=='primary' else common)
        for gene in cfg['genes']:
            q=values[(values.gene==gene)&values.sample_id.isin(mice)].pivot(index='sample_id',columns='state',values='mean_detection_pp')
            delta=q[case]-q[ref]
            assert set(delta.index)==set(mice) and delta.notna().all()
            days = meta.groupby('sample_id').day.first().loc[delta.index]
            for mouse,diff in delta.items():paired.append(dict(contrast=name,sample_id=mouse,day=int(days.loc[mouse]),gene=gene,case=case,reference=ref,case_pp=float(q.loc[mouse,case]),reference_pp=float(q.loc[mouse,ref]),delta_pp=float(diff)))
            n=len(delta); ok=n>=cfg['unit_floor']; mean=float(delta.mean()) if ok else None
            sd=float(delta.std(ddof=1)) if ok else None
            half=float(t.ppf(.975,n-1)*sd/np.sqrt(n)) if ok else None
            equal_day=float(pd.DataFrame({'d':delta,'day':days}).groupby('day').d.mean().mean()) if ok else None
            summary.append(dict(contrast=name,gene=gene,n_mice=n,eligible=ok,mean_pp=mean,sd_pp=sd,pointwise_lower=mean-half if ok else None,pointwise_upper=mean+half if ok else None,equal_day_pp=equal_day,positive_mice=int((delta>0).sum()),negative_mice=int((delta<0).sum()),zero_mice=int((delta==0).sum())))
    paired=pd.DataFrame(paired); summary=pd.DataFrame(summary)
    per_day=paired.groupby(['contrast','gene','day']).agg(n_mice=('delta_pp','size'),mean_pp=('delta_pp','mean')).reset_index()
    for name,df in [('state_support.tsv',support),('mouse_state_features.tsv',values),('paired_features.tsv',paired),('feature_summary.tsv',summary),('per_day_features.tsv',per_day)]:df.to_csv(out/name,sep='\t',index=False)
    # Exact integer-combination verification, not another biological replicate.
    max_error=0.; checks=0
    tests=[(500,0),(500,1),(500,500),(501,1),(1000,3),(3000,18),(10000,50)]
    good=np.flatnonzero(eligible_cells)
    for i in good[np.linspace(0,len(good)-1,20,dtype=int)]:
        for j in range(len(cfg['genes'])):tests.append((int(totals[i]),int(selected[j,i])))
    for n,k in tests:
        exact=1-(math.comb(n-k,500)/math.comb(n,500) if n-k>=500 else 0)
        err=abs(float(detection(n,k,500))-exact);max_error=max(max_error,err);checks+=1
    assert max_error < 1e-8
    # Scalar summation independently checks exported aggregation and contrast means.
    for row in values.itertuples():
        ix=np.flatnonzero((meta.sample_id==row.sample_id)&(meta.cell_type==row.state)&eligible_cells)
        j=cfg['genes'].index(row.gene)
        scalar=math.fsum(float(prob[j,k])*100 for k in ix)/len(ix)
        assert abs(scalar-row.mean_detection_pp)<1e-10;checks+=1
    for row in summary.itertuples():
        q=paired[(paired.contrast==row.contrast)&(paired.gene==row.gene)]
        if row.eligible:assert abs(math.fsum(q.delta_pp)/len(q)-row.mean_pp)<1e-10
        checks+=1
    fig,axes=plt.subplots(1,3,figsize=(14,7),sharey=True)
    for ax,(name,_,_,_) in zip(axes,cfg['contrasts']):
        q=summary[summary.contrast==name].set_index('gene').loc[cfg['genes']]
        yy=np.arange(len(q)); err=np.vstack([q.mean_pp-q.pointwise_lower,q.pointwise_upper-q.mean_pp])
        ax.errorbar(q.mean_pp,yy,xerr=err,fmt='o',capsize=3,color='#21618c')
        ax.axvline(0,color='grey',lw=.8);ax.set_title(name.replace('_',' ')+f'\nn = {int(q.n_mice.iloc[0])} mice')
        ax.set_xlabel('Mean paired detection difference (pp)');ax.grid(axis='x',alpha=.2)
    axes[0].set_yticks(np.arange(len(cfg['genes'])),cfg['genes']);axes[0].invert_yaxis()
    fig.suptitle('A5: named RNA features in original repair states',fontsize=16)
    fig.text(.5,.015,'500-UMI expected detection; pointwise descriptive 95% t intervals. Different primary/common support; no fate inference. Basal state below floor.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.045,1,.94]);fig.savefig(out/'destination_features.png',dpi=170);plt.close(fig)
    info={'verification_passed':True,'checks':checks,'max_exact_probability_error':max_error,'matrix_shape':list(x.shape),'features':cfg['genes'],'common_destination_mice':sorted(common),'primary_mice':sorted(sets['Krt8+ ADI']&sets['AT2 activated']),'basal_eligible_mice':sorted(sets['Basal']),'interpretation':'Cross-sectional named-feature RNA; no trajectory, HIF activity, basal-fate discrimination or Guo replication.'}
    (out/'verification.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info))

if __name__=='__main__':main()
