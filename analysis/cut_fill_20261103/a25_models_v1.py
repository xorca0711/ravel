"""A25 exposed male-cortex predictive representation comparison; train-only fits."""
import argparse,json
from pathlib import Path
import numpy as np,pandas as pd,h5py
from scipy import sparse,linalg
from scipy.special import logsumexp
from scipy.optimize import minimize_scalar

AGES=[3,18,24]

def weights(mouse):
    names=np.unique(mouse);return np.array([1/(len(names)*sum(mouse==m)) for m in mouse])

def moments(x,w):
    w=w/w.sum();mu=w@x;return mu,np.maximum(w@((x-mu)**2),.05)

def lp(x,mu,var):return -.5*(np.log(2*np.pi*var)+((x-mu)**2)/var).sum(axis=1)

def mixture_fit(L,w):
    f=lambda a: -sum(w*logsumexp(L+np.log([1-a,a]),axis=1))
    fit=minimize_scalar(f,bounds=(1e-8,1-1e-8),method='bounded',options={'xatol':1e-9})
    cand=[(f(fit.x),fit.x),(-sum(w*L[:,0]),0.),(-sum(w*L[:,1]),1.)];return min(cand)[1]

def mixlog(L,pi):
    keep=np.asarray(pi)>0;return logsumexp(L[:,keep]+np.log(np.asarray(pi)[keep]),axis=1)

def fit_rep(x,mouse):
    w=weights(mouse);mu=w@x;v=w@((x-mu)**2);det=w@(x>0)
    eligible=np.flatnonzero((det>=.1)&(v>1e-8));assert len(eligible)>=500
    features=eligible[np.argsort(-v[eligible],kind='stable')[:500]]
    scale=np.sqrt(v[features]);z=(x[:,features]-mu[features])/scale
    cov=(z*w[:,None]).T@z;e,V=linalg.eigh(cov,subset_by_index=[495,499]);V=V[:,::-1];e=e[::-1]
    # Fix signs deterministically; cell representation has unit training variance.
    for j in range(5):
        if V[np.argmax(abs(V[:,j])),j]<0:V[:,j]*=-1
    P=V/np.sqrt(e)
    return features,mu[features],scale,P

def models(z,age,mouse):
    stats={}; w=weights(mouse)
    for a in AGES:
        ix=age==a;stats[a]=moments(z[ix],weights(mouse[ix]))
    end=np.column_stack([lp(z,*stats[a]) for a in [3,24]])
    pis={a:mixture_fit(end[age==a],weights(mouse[age==a])) for a in AGES}
    mid=age==18;zm=z[mid];wm=weights(mouse[mid]);L=end[mid]
    # Exactly one additional normal, fitted to middle-age training animals.
    # Endpoint components are identical to the two-component baseline.
    mu,var=stats[18]; pi=np.array([(1-pis[18])*.5,pis[18]*.5,.5]); previous=-np.inf
    for iteration in range(300):
        ll=np.column_stack([L,lp(zm,mu,var)]);den=mixlog(ll,pi);value=sum(wm*den)
        assert value>=previous-1e-7
        if value-previous<1e-8:break
        previous=value;resp=np.exp(ll+np.log(np.maximum(pi,1e-300))-den[:,None]);pi=wm@resp;pi/=pi.sum()
        mu,var=moments(zm,wm*resp[:,2])
    return stats,pis,(mu,var,pi,iteration,value)

def main(out):
    out.mkdir(exist_ok=True)
    bridge=pd.read_csv('analysis/research/runs/nb5_completion_metadata_v2/case_brain_join.tsv',sep='\t')
    d=bridge[(bridge.cell_ontology_class=='microglial cell')&(bridge.sex=='male')&(bridge.subtissue.str.strip()=='Cortex')].copy()
    d['age_months']=d.age.str.replace('m','').astype(int);assert d.mouse_id.nunique()==9;assert d.groupby('mouse_id').size().min()>=20;assert d.groupby('age_months').mouse_id.nunique().to_dict()=={3:3,18:2,24:4}
    with h5py.File('raw_data/tabula_muris_senis_2020/completion_v1/official_brain.h5ad') as h:
        ids=[x.decode() for x in h['obs']['index']];assert len(ids)==len(set(ids));lookup={v:i for i,v in enumerate(ids)}
        ix=np.array([lookup[v] for v in d.official_lookup]);assert len(ix)==len(set(ix))
        G=h['raw.X'];C=sparse.csr_matrix((G['data'][:],G['indices'][:],G['indptr'][:]),shape=tuple(G.attrs['h5sparse_shape']))[ix]
        genes=np.array([x.decode() for x in h['raw.var']['index']]);assert len(genes)==len(set(genes));tot=np.asarray(C.sum(axis=1)).ravel()
        assert np.array_equal(tot,d.official_n_counts.to_numpy());assert np.all(C.data>=0) and np.all(C.data==np.floor(C.data))
        X=(sparse.diags(1e6/tot)@C).toarray();X=np.log1p(X)
    d[['cell_id','official_lookup','mouse_id','sex','age_months','subtissue']].to_csv(out/'cell_units.csv.gz',index=False)
    mice=d.mouse_id.to_numpy();age=d.age_months.to_numpy();pred=[];details={};directions=[];coherence=[]
    for hold in sorted(set(mice)):
        train=mice!=hold;test=~train;features,mu,scale,P=fit_rep(X[train],mice[train]);z=(X[:,features]-mu)/scale@P
        stats,pis,extra=models(z[train],age[train],mice[train]);a=int(age[test][0]);zt=z[test]
        L=np.column_stack([lp(zt,*stats[b]) for b in [3,24]]);endpoint=mixlog(L,[1-pis[a],pis[a]])
        continuous=lp(zt,*stats[a]);em,ev,epi,it,obj=extra
        additional=mixlog(np.column_stack([L,lp(zt,em,ev)]),epi) if a==18 else endpoint
        for name,vals in [('endpoint_mixture',endpoint),('continuous_age',continuous),('additional_component',additional)]:
            pred.append(dict(mouse=hold,age=a,cells=int(test.sum()),model=name,mean_nll=float(-vals.mean())))
        details[hold]={'training_mice':sorted(set(mice[train])),'genes':genes[features].tolist(),'center':mu.tolist(),'scale':scale.tolist(),'projection':P.tolist(),'age_gaussian_means':{str(k):v[0].tolist() for k,v in stats.items()},'age_gaussian_variances':{str(k):v[1].tolist() for k,v in stats.items()},'endpoint_old_weights':pis,'extra_mean':em.tolist(),'extra_variance':ev.tolist(),'extra_weights':epi.tolist(),'em_iterations':it,'em_converged':it<299,'training_objective':obj}
        if a==18:
            posterior=np.exp(lp(zt,em,ev)+np.log(epi[2])-additional)
            # Direction in log expression, relative to fitted endpoint mean.
            delta=em-((1-pis[18])*stats[3][0]+pis[18]*stats[24][0]);direction=(delta@np.linalg.pinv(P))*scale
            full=np.zeros(X.shape[1]);full[features]=direction;directions.append(full)
            coherence.append({'heldout_mouse':hold,'mean_extra_posterior':float(posterior.mean()),'fraction_posterior_above_half':float((posterior>.5).mean()),'extra_training_weight':float(epi[2])})
    tab=pd.DataFrame(pred);tab.to_csv(out/'heldout_losses.csv',index=False)
    wide=tab.pivot(index='mouse',columns='model',values='mean_nll');gains={}
    for base in ['endpoint_mixture','continuous_age']:
        v=wide[base]-wide.additional_component
        gains[base]={'equal_mouse_gain':float(v.mean()),'positive_mice':int((v>1e-10).sum()),'per_mouse':v.to_dict(),'delete_one_mouse_range':[float(v.drop(m).mean()) for m in v.index]}
    cosine=float(np.dot(*directions)/np.prod([np.linalg.norm(v) for v in directions])) if all(np.linalg.norm(v)>0 for v in directions) else None
    (out/'fold_models.json').write_text(json.dumps(details,indent=2))
    (out/'summary.json').write_text(json.dumps({'scope':'male cortex only; 3/2/4 mice at 3/18/24 months','cells':len(d),'mean_nll_by_model':tab.groupby('model').mean_nll.mean().to_dict(),'additional_component_gains':gains,'middle_age_coherence':coherence,'middle_age_gene_direction_cosine':cosine,'limits':'Exposed internal leave-mouse-out prediction; overlapping training sets; only two middle-age males; continuous age moments saturated at three ages. Gaussian-family restrictions and processing confounding preclude a distinct functional-state claim. Deletion ranges are sensitivity, not confidence intervals.'},indent=2))
    assert all(hold not in x['training_mice'] for hold,x in details.items())
    assert np.isfinite(tab.mean_nll).all()
    # Equal-mouse weights are invariant to repeating every cell within one mouse.
    tx=np.array([[0.,1.],[2.,3.],[5.,7.]]);tm=np.array(['a','a','b']);dup=[0,1,0,1,2]
    assert np.allclose(weights(tm)@tx,weights(tm[dup])@tx[dup])
    # Independently reconstruct all saved losses from fold parameters.
    maxerr=0.
    for hold,x in details.items():
        ix=[int(np.where(genes==g)[0][0]) for g in x['genes']];z=(X[mice==hold][:,ix]-np.array(x['center']))/np.array(x['scale'])@np.array(x['projection']);a=str(int(age[mice==hold][0]))
        logs=[]
        for b in ['3','24']:
            m=np.array(x['age_gaussian_means'][b]);v=np.array(x['age_gaussian_variances'][b]);logs.append(np.array([sum(-.5*(np.log(2*np.pi*v)+(row-m)**2/v)) for row in z]))
        ep=mixlog(np.column_stack(logs),[1-x['endpoint_old_weights'][int(a)],x['endpoint_old_weights'][int(a)]])
        co=lp(z,np.array(x['age_gaussian_means'][a]),np.array(x['age_gaussian_variances'][a]))
        ex=mixlog(np.column_stack(logs+[lp(z,np.array(x['extra_mean']),np.array(x['extra_variance']))]),x['extra_weights']) if a=='18' else ep
        for name,val in [('endpoint_mixture',ep),('continuous_age',co),('additional_component',ex)]:maxerr=max(maxerr,abs(-val.mean()-float(wide.loc[hold,name])))
    assert maxerr<1e-9
    (out/'verification.json').write_text(json.dumps({'passed':True,'raw_full_library_totals_exact':True,'unique_cell_join':True,'all_mouse_holdouts_disjoint':True,'equal_mouse_duplication_invariance':True,'saved_model_loss_reconstruction_max_error':maxerr},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);main(ap.parse_args().output)
