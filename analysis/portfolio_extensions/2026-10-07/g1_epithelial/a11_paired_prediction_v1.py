"""Fixed-gene paired discrimination with patient holdout; no prospective fate claim."""
import argparse
import gzip
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit

ROOT = Path(__file__).resolve().parents[4]
HERE = ROOT / 'RQ_Specified/A11_lesion_programme_addition'
BASE = ['shared_remodelling', 'HALLMARK_P53_PATHWAY', 'HALLMARK_HYPOXIA', 'HALLMARK_INFLAMMATORY_RESPONSE']


def fit(train, penalty):
    scale = train.reshape(-1, train.shape[-1]).std(axis=0, ddof=0)
    scale = np.where(scale > 0, scale, 1.)
    d = (train[:, 1] - train[:, 0]) / scale
    def objective(w):
        z = d @ w
        return np.logaddexp(0, -z).mean() + penalty * (w @ w) / 2
    def gradient(w):
        return -(d.T @ expit(-d @ w)) / len(d) + penalty*w
    result = minimize(objective, np.zeros(d.shape[1]), jac=gradient, method='BFGS', options={'gtol':1e-10, 'maxiter':1000})
    if np.linalg.norm(gradient(result.x), np.inf) > 1e-7:
        raise ValueError('Optimizer did not meet gradient tolerance')
    # Independent Newton solution, not a second call to the optimizer.
    w = np.zeros(d.shape[1])
    for _ in range(100):
        p = expit(d @ w)
        grad = d.T @ (p-1)/len(d) + penalty*w
        hess = (d.T * (p*(1-p))) @ d / len(d) + penalty*np.eye(d.shape[1])
        step = np.linalg.solve(hess, grad)
        w -= step
        if np.max(np.abs(step)) < 1e-11:
            break
    if np.max(np.abs(w-result.x)) > 1e-6:
        raise ValueError('Independent Newton coefficients disagree')
    return result.x, scale, float(np.max(np.abs(w-result.x)))


def load_counts(output):
    units = pd.read_csv(HERE/'tables/test_v2/units.tsv', sep='\t')
    pairs = pd.read_csv(HERE/'tables/kim_pairing.tsv', sep='\t').set_index('patient')
    cfg = json.loads((HERE/'config/kim2020_test_contract.json').read_text())
    ann = pd.read_csv(ROOT/'raw_data/GSE131907/GSE131907_Lung_Cancer_cell_annotation.txt.gz', sep='\t')
    labels = {arm:cfg['populations'][arm+'_arm']['author_labels'] for arm in ['normal','lesion']}
    groups=[]
    for u in units.itertuples():
        sample=pairs.loc[u.patient, 'normal_sample' if u.arm=='normal' else 'tumour_sample']
        selected=ann.loc[(ann.Sample==sample)&ann.Cell_subtype.isin(labels[u.arm]),'Index'].tolist()
        if len(selected)!=u.cells:raise ValueError('Original population count mismatch')
        groups.append(selected)
    cells=[c for group in groups for c in group]
    if len(cells)!=len(set(cells)):raise ValueError('Duplicated selected cell')
    raw=ROOT/'raw_data/GSE131907/GSE131907_Lung_Cancer_raw_UMI_matrix.txt.gz'
    with gzip.open(raw,'rt') as handle:
        header=[v.strip('"') for v in handle.readline().rstrip('\r\n').split('\t')]
    matrices=[];genes=[]
    for chunk in pd.read_csv(raw,sep='\t',usecols=[header[0],*cells],index_col=0,chunksize=256):
        a=chunk.to_numpy()
        if not (np.isfinite(a).all() and (a>=0).all() and (a==np.floor(a)).all()):raise ValueError('Invalid counts')
        matrices.append(np.column_stack([chunk[cs].sum(axis=1).to_numpy(dtype=np.int64) for cs in groups]))
        genes.extend(chunk.index.astype(str))
    counts=np.vstack(matrices)
    if len(set(genes))!=29634 or len(genes)!=29634:raise ValueError('Gene universe changed')
    old=pd.read_csv(HERE/'tables/test_v2/normalization.tsv',sep='\t')
    if units.unit_id.tolist()!=old.unit_id.tolist() or not np.array_equal(counts.sum(axis=0),old.library_size.to_numpy()):raise ValueError('Pseudobulk library totals differ from original')
    pd.DataFrame(counts,index=genes,columns=units.unit_id).to_csv(output/'pseudobulk_counts.tsv.gz',sep='\t',index_label='gene')
    return units,genes,counts


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    out=args.output
    units,genes,counts=load_counts(out)
    # Per-sample full-library normalization requires no estimate from another patient.
    lc=np.log2(1 + 1e6*counts/counts.sum(axis=0))
    index={g:i for i,g in enumerate(genes)}
    modules=pd.read_csv(HERE/'tables/test_v2/human_module_genes.tsv',sep='\t')
    features=BASE+['lesion_specific','stress_excluded']
    scores={}
    for m in features:
        selected=modules.loc[modules.module==m,'gene'].tolist()
        if not selected or len(selected)!=len(set(selected)) or not set(selected)<=set(index):
            raise ValueError('Empty, duplicate or unmapped fixed module: '+m)
        scores[m]=lc[[index[g] for g in selected]].mean(axis=0)
    patients=sorted(units.patient.unique())
    if len(patients)!=8:raise ValueError('Expected eight frozen patient pairs')
    x=np.empty((8,2,len(features)))
    score_rows=[]
    for i,patient in enumerate(patients):
        for j,arm in enumerate(['normal','lesion']):
            loc=units.index[(units.patient==patient)&(units.arm==arm)].tolist()
            if len(loc)!=1:raise ValueError('Nonunique pair')
            x[i,j]=[scores[m][loc[0]] for m in features]
            score_rows.extend({'patient':patient,'arm':arm,'module':m,'score':x[i,j,k]} for k,m in enumerate(features))
    pd.DataFrame(score_rows).to_csv(out/'module_scores.tsv',sep='\t',index=False)
    rows=[];coef=[];verrors=[]
    for penalty in [1.,.1,10.]:
        for model,inds in [('shared_stress',list(range(4))),('add_lesion',list(range(5))),('add_stress_excluded',[0,1,2,3,5])]:
            for held,patient in enumerate(patients):
                train=np.delete(x[:,:,inds],held,axis=0)
                w,scale,error=fit(train,penalty);verrors.append(error)
                d=(x[held,1,inds]-x[held,0,inds])/scale
                z=float(d@w);loss=float(np.logaddexp(0,-z))
                # Reversed pair receives complementary probability and equal loss.
                if abs(float(expit(z)+expit(-z))-1)>1e-14:raise ValueError('Pair orientation failure')
                rows.append({'patient':patient,'penalty':penalty,'model':model,'lesion_pair_probability':float(expit(z)),'log_loss':loss,'correct_pair_order':int(z>0),'training_patients':7})
                coef.extend({'patient':patient,'penalty':penalty,'model':model,'feature':features[k],'coefficient':float(v),'train_scale':float(s)} for k,v,s in zip(inds,w,scale))
    frame=pd.DataFrame(rows);frame.to_csv(out/'heldout_predictions.tsv',sep='\t',index=False)
    pd.DataFrame(coef).to_csv(out/'coefficients.tsv',sep='\t',index=False)
    comparisons=[]
    for penalty in [1.,.1,10.]:
        z=frame[frame.penalty==penalty].pivot(index='patient',columns='model',values='log_loss')
        for model in ['add_lesion','add_stress_excluded']:
            gain=z.shared_stress-z[model]
            comparisons.append({'penalty':penalty,'model':model,'baseline_mean_loss':float(z.shared_stress.mean()),'augmented_mean_loss':float(z[model].mean()),'mean_log_loss_gain':float(gain.mean()),'patients_improved':int((gain>0).sum()),'worst_patient_gain':float(gain.min()),'best_patient_gain':float(gain.max()),'chance_loss':float(np.log(2))})
    pd.DataFrame(comparisons).to_csv(out/'comparisons.tsv',sep='\t',index=False)
    verification={'patients':8,'units':len(units),'cells':int(units.cells.sum()),'genes':len(genes),'library_totals_exact_match':True,'independent_optimizer_max_coefficient_error':max(verrors),'normalization':'per-library full-count log2(CPM+1); fixed offset; no TMM','historical_scores_used_for_fit':False,'all_feature_scaling_training_only':True,'no_patient_outcome_centering':True}
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    print(json.dumps({'comparisons':comparisons,'verification':verification}))


if __name__=='__main__':main()
