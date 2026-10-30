"""Six-library exon-hit profile diagnostic, not author gene-level PCA or an effect test."""
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ARTICLE=Path('Research Article/gate2_DY1_damani_yokota_2026')
QC=Path('analysis/research/runs/DY1_baseline_file_qc_v1')

def profile(counts):
    counts=np.asarray(counts)
    if counts.ndim!=2 or counts.shape[1]<2 or not np.issubdtype(counts.dtype,np.integer) or (counts<0).any():raise ValueError('Invalid feature-by-library count matrix')
    total=counts.sum(axis=0,dtype=np.int64)
    if (total<=0).any():raise ValueError('Nonpositive exon-hit denominator')
    keep=np.any(counts!=0,axis=1)
    transformed=np.log2(1+counts[keep]/total[None,:]*1e6)
    centered=transformed-transformed.mean(axis=1,keepdims=True)
    matrix=centered.T
    tol=np.finfo(float).eps*max(1.,float(np.abs(transformed).max()))*counts.shape[1]*8
    if np.abs(matrix).max()<=tol:raise ValueError('Numerically constant sample profiles; variance fractions undefined')
    u,s,_=np.linalg.svd(matrix,full_matrices=False)
    scores=u*s
    for k in range(len(s)):
        pivot=int(np.argmax(np.abs(scores[:,k])))
        if scores[pivot,k]<0:scores[:,k]*=-1
    eigen=np.linalg.eigvalsh(matrix@matrix.T)[::-1]
    if not np.allclose(s*s,eigen,rtol=1e-10,atol=1e-7):raise ValueError('Independent covariance eigenvalue check failed')
    if not np.allclose(scores@scores.T,matrix@matrix.T,rtol=1e-10,atol=1e-7):raise ValueError('Full-coordinate Gram reconstruction failed')
    if not np.allclose(centered.sum(axis=1),0,rtol=0,atol=1e-10):raise ValueError('Feature centering failed')
    return scores,s*s/(counts.shape[1]-1),s*s/(s*s).sum(),total,keep

def main(out):
    q=json.loads((QC/'exon_universe.json').read_text());receipt=json.loads((QC/'receipt.json').read_text())
    if receipt['status']!='executed' or not q['count_format_eligible'] or not q['same_ordered_ids']:raise ValueError('Structural qualification not satisfied')
    manifest=json.loads((ARTICLE/'config/baseline_file_qc_inputs_v1.json').read_text());files=[x for x in manifest['files'] if x['kind']=='exon_counts']
    if len(files)!=6:raise ValueError('Fixed six-library set changed')
    source=pd.read_csv('analysis/research/runs/DY1_source_v1/sample_map.tsv',sep='\t').set_index('gsm');columns=[];ids=None;labels=[];accessions=[]
    for item in files:
        path=Path(item['path']);d=pd.read_csv(path,sep='\t',header=None,names=['id','count'],dtype={'id':str,'count':np.int64});d=d[~d.id.str.startswith('_')]
        if ids is None:ids=d.id.to_numpy()
        elif not np.array_equal(ids,d.id.to_numpy()):raise ValueError('Feature axes differ')
        columns.append(d['count'].to_numpy());accession=path.name.split('_')[0];accessions.append(accession);labels.append(source.loc[accession,'title'])
    counts=np.column_stack(columns);scores,variance,ratio,totals,keep=profile(counts)
    if len(ids)!=q['union_features'] or int((~keep).sum())!=q['all_zero_feature_ids']:raise ValueError('Qualified feature/zero count changed')
    table=pd.DataFrame({'gsm':accessions,'source_title':labels,'exon_hit_denominator':totals})
    for i in range(scores.shape[1]):table[f'PC{i+1}']=scores[:,i]
    table.to_csv(out/'sample_coordinates.tsv',sep='\t',index=False,lineterminator='\n')
    pd.DataFrame({'component':[f'PC{i+1}' for i in range(len(ratio))],'transformed_variance':variance,'fraction':ratio}).to_csv(out/'variance.tsv',sep='\t',index=False,lineterminator='\n')
    fig,(ax,key)=plt.subplots(1,2,figsize=(11,4.3),gridspec_kw={'width_ratios':[1.1,1]},constrained_layout=True)
    ax.scatter(scores[:,0],scores[:,1],s=170,color='#287f8e')
    for i,(x,y) in enumerate(scores[:,:2]):ax.text(x,y,str(i+1),ha='center',va='center',color='white',fontsize=9)
    ax.set_xlabel(f'PC1 ({ratio[0]*100:.1f}% transformed variance)');ax.set_ylabel(f'PC2 ({ratio[1]*100:.1f}% transformed variance)');ax.margins(.18);ax.spines[['top','right']].set_visible(False)
    key.axis('off')
    for i,(accession,label) in enumerate(zip(accessions,labels)):key.text(0,.95-i*.145,f'{i+1}. {accession}\n    {label}',va='top',fontsize=10)
    fig.suptitle('Technical exon-bin profile diagnostic: fixed six libraries\nN. brasiliensis-history / IAV-study context; no animal-level effect inference',fontsize=11)
    fig.savefig(out/'sample_profile.png',dpi=160);plt.close(fig)
    verification=dict(ok=True,checks=['All six exact source-label/feature joins','Qualified all-zero feature count and positive exon-hit denominators','Full deterministic SVD versus covariance eigenvalues','All-component coordinate Gram reconstruction','Feature centering'],floating_tolerances='rtol1e-10/atol1e-7 for covariance checks; centering atol1e-10; numerical-constant guard scales with machine epsilon.',limit='Arithmetic on the same transformed files, not author-PCA replication or biological independence.')
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    summary=dict(analysis_id='DY1-P01.baseline_exon_profile_v1',samples=6,all_exon_features=len(ids),all_zero_removed=int((~keep).sum()),features_retained=int(keep.sum()),transformation='log2(1 + 1e6 * exon-bin count / sum of all non-summary exon-bin counts); feature-centered; full SVD; no variance or condition feature selection.',output_scope='Sample coordinates and transformed variance only. No named-gene loadings/ranking, group effect, exclusion or infection-response model.',author_difference='Author Methods report unspecified low-overall-count filtering, DESeq2v1.48.2 VST and plotPCA. This fixed exon-hit diagnostic is a different adaptation, not that reproduction.',interpretation_limit='Exon-hit denominator is not unique fragment/gene counts. Unknown library-to-independent-pool mapping prevents animal/pool effect inference; source labels are descriptive. No original outlier decision is recovered.',scientific_acceptance='not_assessed')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
