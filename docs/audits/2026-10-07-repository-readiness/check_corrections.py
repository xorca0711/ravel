"""Independent saved-table arithmetic and two-library raw QC checks.

Requires the research Python stack. --raw-cache is optional for public clones;
without it the two-library raw audit is explicitly skipped, not called passed.
Does not import the generating scripts or modify any scientific output.
"""
import argparse
import gzip
import io
import json
from pathlib import Path
import tarfile

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT/'analysis/research/runs'
checks = []


def equal(name, got, expected, tolerance=1e-7):
    np.testing.assert_allclose(got, expected, atol=tolerance, rtol=1e-7, err_msg=name)
    checks.append({'check': name, 'values': int(np.size(got)), 'passed': True})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw-cache')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    r4 = RUNS/'wp_human_signature_transfer_v3'
    cells = pd.read_csv(r4/'cell_scores.csv.gz')
    identity = pd.read_csv(r4/'cell_identity_qc.csv.gz')
    donor = pd.read_csv(r4/'donor_scores.csv')
    scores = [c for c in cells if c not in ['gsm','donor','tissue','disease']]
    assert cells[['gsm','donor','tissue']].equals(identity[['gsm','donor','tissue']])
    assert not identity.duplicated(['gsm','barcode']).any()
    equal('retained cell identities', len(identity), 35928, 0)
    assert (identity.total >= identity.selected_gene_total).all()
    assert (identity.total > identity.selected_gene_total).any()
    # Denominator-regression property: feature subsetting cannot change the
    # normalization of any retained gene when the original total is carried.
    count = np.array([[2.,3.,95.],[2.,3.,5.]])
    full = count/count.sum(axis=1)[:,None]*1e4
    subset = count[:,:2]/count.sum(axis=1)[:,None]*1e4
    equal('full-library normalization invariant to selected columns', subset, full[:,:2])
    assert not np.allclose(subset, count[:,:2]/count[:,:2].sum(axis=1)[:,None]*1e4)
    keys=['donor','tissue','disease']
    got=cells.groupby(keys)[scores].mean().sort_index()
    want=donor.set_index(keys).sort_index()
    equal('all donor score means', got.to_numpy(), want[scores].to_numpy())
    equal('all donor cell counts', cells.groupby(keys).size().sort_index(),want.n_cells,0)
    paired=pd.read_csv(r4/'paired_tissue.csv').set_index('score')
    for score in scores:
        wide=donor.pivot(index='donor',columns='tissue',values=score).dropna()
        delta=wide.CSF-wide.PBMCs
        equal(f'{score}: paired median, positive count and Wilcoxon',
              [np.median(delta), (delta>0).sum(), stats.wilcoxon(delta).pvalue],
              paired.loc[score,['median_difference','n_positive','wilcoxon_p']].to_numpy(float))
    disease=pd.read_csv(r4/'disease_contrasts.csv')
    for tissue, part in disease.groupby('tissue'):
        pvals=[]
        d=donor[donor.tissue==tissue]
        for row in part.itertuples():
            a=d.loc[d.disease=='MS',row.score].to_numpy()
            b=d.loc[d.disease=='IIH',row.score].to_numpy()
            p=stats.mannwhitneyu(a,b,alternative='two-sided').pvalue
            equal(f'{tissue}/{row.score}: disease difference and p',[np.median(a)-np.median(b),p],[row.median_difference,row.mannwhitney_p])
            pvals.append(p)
        # Alternative BH implementation: minimum p_j*m/j for all j>=i.
        ranked=sorted(enumerate(pvals),key=lambda x:x[1]); adjusted=np.zeros(len(ranked))
        for i,(original,_) in enumerate(ranked):
            adjusted[original]=min(1,min(v*len(ranked)/(j+1) for j,(_,v) in enumerate(ranked) if j>=i))
        equal(tissue+': disease BH family',adjusted,part.mannwhitney_bh)
    qc=pd.read_csv(r4/'sample_qc.csv')
    oldqc=pd.read_csv(RUNS/'wp_human_signature_transfer_v2/sample_qc.csv')
    pd.testing.assert_frame_equal(qc.drop(columns='n_after_cd8_exclusion'),oldqc)
    equal('all original QC selections preserved',len(qc),22,0)
    cascade=qc[['n_cells_called','n_pass_qc','n_t_positive','n_after_cd8_exclusion','n_cd4_lineage']].to_numpy()
    assert (np.diff(cascade,axis=1)<=0).all()
    c3=pd.read_csv(RUNS/'wp_compass_orientation_v3/reaction_correlations.csv').set_index('reaction').sort_index()
    c2=pd.read_csv(RUNS/'wp_compass_sensitivity_v2_rerun/reaction_correlations.csv').set_index('reaction').sort_index()
    for col in c2:
        if col.startswith('rho_'): equal('Compass orientation '+col,c3[col],-c2[col],1e-12)
        elif col.startswith('p_') or col=='bh_pathogenicity': equal('Compass unchanged '+col,c3[col],c2[col],1e-12)
    equal('Compass ascending rank',c3.rho_pathogenicity_authors.rank(method='max'),c3.rank_of_rho_ascending,0)
    # M1/M2 are unchanged controls for the dependent M3 input correction.
    old=RUNS/'wp_metadata_phenotypes_v1'; new=RUNS/'wp_metadata_phenotypes_v2'
    for p in old.glob('*.csv*'):
        if p.name=='tissue_specificity_null.csv': continue
        pd.testing.assert_frame_equal(pd.read_csv(p),pd.read_csv(new/p.name),rtol=1e-12,atol=1e-12)
        checks.append({'check':'M1/M2 unchanged: '+p.name,'passed':True})
    raw_checked=[]
    if args.raw_cache:
        cache=Path(args.raw_cache)
        with tarfile.open(cache/'GSE138266_RAW.tar') as tar:
            # One small library per compartment, selected by matrix size rather
            # than outcome. Vectorized bincount is independent of generator loops.
            for row in qc.sort_values('n_cells_matrix').groupby('tissue').head(1).itertuples():
                names=[n for n in tar.getnames() if n.startswith(row.gsm+'_')]
                matrix=next(n for n in names if 'matrix' in n)
                genes=next(n for n in names if 'genes' in n)
                bcs=next(n for n in names if 'barcodes' in n)
                with gzip.open(tar.extractfile(matrix),'rt') as f:
                    line=f.readline()
                    while line.startswith('%'): line=f.readline()
                    ng,nc,nnz=map(int,line.split())
                    data=np.loadtxt(f)
                equal(row.gsm+': raw dimensions',[ng,nc,len(data)],[row.n_genes_matrix,row.n_cells_matrix,nnz],0)
                with gzip.open(tar.extractfile(genes),'rt') as f: syms=pd.read_csv(f,sep='\t',header=None)[1].astype(str)
                with gzip.open(tar.extractfile(bcs),'rt') as f: barcodes=np.array([s.strip() for s in f])
                gene_idx=data[:,0].astype(int)-1; cell_idx=data[:,1].astype(int)-1
                totals=np.bincount(cell_idx,weights=data[:,2],minlength=nc)
                detected=np.bincount(cell_idx,minlength=nc)
                mt=syms.str.upper().str.startswith('MT-').to_numpy()[gene_idx]
                mito=np.bincount(cell_idx[mt],weights=data[mt,2],minlength=nc)/np.maximum(totals,1)
                ids=identity[identity.gsm==row.gsm]; idx=ids.matrix_column_1based.to_numpy()-1
                assert np.array_equal(barcodes[idx],ids.barcode.to_numpy())
                equal(row.gsm+': full raw denominators',totals[idx],ids.total,0)
                equal(row.gsm+': detected genes',detected[idx],ids.n_genes,0)
                equal(row.gsm+': mitochondrial fraction',mito[idx],ids.mito_frac)
                raw_checked.append(row.gsm)
        # Direct module arithmetic from gene-level donor output; M3 intentionally
        # includes finite constant genes while R4 excludes zero-variance genes.
        s1=pd.read_excel(cache/'NIHMS2092659-supplement-2.xlsx',sheet_name='Table S1')
        s1.columns=s1.columns.astype(str).str.strip()
        g=next(c for c in s1 if c.lower() in ('gene','symbol','gene_symbol'))
        m=next(c for c in s1 if 'module' in c.lower() or 'program' in c.lower())
        h=next(c for c in s1 if 'hvg' in c.lower())
        z=pd.read_csv(r4/'donor_gene_mean_z.csv.gz',index_col=0)
        result=pd.read_csv(new/'tissue_specificity_null.csv').set_index('score')
        for mod,rows in s1.groupby(m):
            key='proinflammatory' if 'inflam' in str(mod).lower() else 'proregulatory'
            for suffix,part in [('all',rows),('authors',rows[rows[h].astype(str).str.upper().isin(['TRUE','YES','1','1.0'])])]:
                members=sorted(set(part[g].astype(str).str.upper()) & set(z.columns))
                donors=sorted(set(i.split('|')[0] for i in z.index if i.endswith('|PBMCs')))
                delta=np.array([z.loc[d+'|CSF',members].mean()-z.loc[d+'|PBMCs',members].mean() for d in donors])
                target=result.loc[key+'_'+suffix]
                equal('M3 gene arithmetic '+key+'_'+suffix,[np.median(delta),(delta>0).sum(),stats.wilcoxon(delta).pvalue],target[['observed_median_csf_minus_blood','n_donors_positive','wilcoxon_p']].to_numpy(float))
    output={'passed':True,'checks':checks,'raw_libraries_checked':raw_checked,'raw_scope':'two smallest libraries, one per tissue; all 22 library selections compared with v2; not all raw matrices independently reconstructed','independence':'Independent arithmetic on reused data, not biological replication.'}
    Path(args.output).write_bytes((json.dumps(output,indent=2)+'\n').encode())
    print(json.dumps({'passed':True,'checks':len(checks),'values':sum(c.get('values',0) for c in checks),'raw_libraries':raw_checked}))


if __name__=='__main__': main()
