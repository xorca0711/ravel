"""Frozen, donor-held-out exploratory A12 RNA comparison; no claim grading."""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parents[1]
PAPER=Path('Research Article/gate2_C3_yu_lee_choi_min_2026')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def loo(x,y,alpha):
    preds=[]
    for hold in range(len(y)):
        train=np.arange(len(y))!=hold;ym=y[train].mean()
        if x.shape[1]==0:preds.append(ym);continue
        mean=x[train].mean(axis=0);sd=x[train].std(axis=0);sd[sd==0]=1
        z=(x[train]-mean)/sd
        coef=np.linalg.solve(z.T@z+alpha*np.eye(x.shape[1]),z.T@(y[train]-ym))
        preds.append(float(ym+((x[hold]-mean)/sd)@coef))
    return np.array(preds)

def main():
    arg=argparse.ArgumentParser();arg.add_argument('--data-root',type=Path,required=True);args=arg.parse_args()
    specpath=OUT/'A12_pilot_specification.json';spec=json.loads(specpath.read_text())
    genes=set(spec['response']['genes']);components=set(spec['response']['excluded_predictor_genes'])
    records=[];features=[];predictions=[];inputs={'specification':sha(specpath)};coverage=[];checks=[]
    for uncertainty in [20,30]:
        meta_path=ROOT/PAPER/f'trials/u5_human_niche/unc{uncertainty}_pooled_units.csv'
        raw_path=args.data_root/PAPER/f'cache/u5_human_niche/unc{uncertainty}_pooled_triad_counts.csv.gz'
        inputs[str(meta_path.relative_to(ROOT))]=sha(meta_path);inputs[str(raw_path)]=sha(raw_path)
        meta=pd.read_csv(meta_path,dtype={'patient':str}).set_index('unit_id',drop=False)
        keep=meta.histology.isin(['LUAD','normal']) & ((meta.comp.eq('macrophages')&meta.view.eq('broad'))|meta.label.isin(['AT2','Alveolar fibroblasts']))
        chosen=meta.loc[keep];units=chosen.index.tolist();sums=np.zeros(len(units),dtype=np.int64);parts=[]
        for chunk in pd.read_csv(raw_path,usecols=['gene']+units,chunksize=500):
            arr=chunk[units].to_numpy();assert np.isfinite(arr).all() and (arr>=0).all() and (arr==np.floor(arr)).all()
            sums+=arr.sum(axis=0,dtype=np.int64)
            parts.append(chunk[chunk.gene.isin(genes|components)].set_index('gene')[units])
        assert np.array_equal(sums,chosen.full_library_sum.to_numpy())
        count=pd.concat(parts);assert count.index.is_unique and components<=set(count.index)
        present=sorted(genes&set(count.index));assert len(present)/len(genes)>=spec['response']['coverage_floor']
        log=np.log2(1+count.div(chosen.full_library_sum,axis='columns')*1e6)
        coverage.append({'uncertainty':uncertainty/100,'response_genes_present':len(present),'response_genes_frozen':len(genes),'missing':sorted(genes-set(present)),'library_total_parity':True})
        for label in ['AT2','Alveolar fibroblasts']:
            for floor in ([50,30,100] if uncertainty==20 else [50]):
                frame=[]
                for patient in sorted(chosen.patient.unique(),key=int):
                    vals={};fail=False
                    for hist in ['normal','LUAD']:
                        source=chosen[(chosen.patient==patient)&(chosen.histology==hist)&chosen.comp.eq('macrophages')]
                        receiver=chosen[(chosen.patient==patient)&(chosen.histology==hist)&chosen.label.eq(label)]
                        if len(source)!=1 or len(receiver)!=1 or int(source.cells.iloc[0])<floor or int(receiver.cells.iloc[0])<floor:fail=True;break
                        s=source.index[0];r=receiver.index[0]
                        mono=meta[(meta.patient==patient)&(meta.histology==hist)&meta.label.eq('Monocyte-derived Mph')].cells.sum()
                        d={g:float(log.loc[g,s]) for g in ['IL1A','IL1B','TNF']}
                        d.update(mono_fraction=float(mono/source.cells.iloc[0]),recipient_index=float(log.loc[['IL1R1','IL1RAP'],r].mean()-log.loc[['IL1R2','IL1RN','SIGIRR'],r].mean()),response=float(log.loc[present,r].mean()))
                        vals[hist]=d
                    if fail:continue
                    d={k:vals['LUAD'][k]-vals['normal'][k] for k in vals['LUAD']}
                    frame.append({'patient':patient,**d,'source_normal_unit':chosen[(chosen.patient==patient)&chosen.histology.eq('normal')&chosen.comp.eq('macrophages')].index[0],
                                  'source_LUAD_unit':s,'recipient_normal_unit':chosen[(chosen.patient==patient)&chosen.histology.eq('normal')&chosen.label.eq(label)].index[0],'recipient_LUAD_unit':r})
                data=pd.DataFrame(frame);tag={'recipient':label,'uncertainty':uncertainty/100,'cell_floor':floor,'n':len(data)}
                if len(data)<spec['launch_floor']:
                    records.append({**tag,'status':'not_fit_below_pilot_floor'});continue
                y=data.response.to_numpy();assert y.std()>0
                features.extend({**tag,**r} for r in data.to_dict('records'))
                for alpha in ([1.0,0.1,10.0] if uncertainty==20 and floor==50 else [1.0]):
                    outputs={}
                    for name,predictor_names in spec['models'].items():
                        x=data[predictor_names].to_numpy();pred=loo(x,y,alpha);outputs[name]=pred
                        # Verify changing a held-out outcome cannot influence its own prediction.
                        altered=y.copy();altered[0]+=1000
                        assert abs(loo(x,altered,alpha)[0]-pred[0])<1e-10
                        residual=y-pred
                        predictions.extend({**tag,'alpha':alpha,'model':name,'patient':p,'observed':obs,'predicted':pr,'squared_error':err*err} for p,obs,pr,err in zip(data.patient,y,pred,residual))
                        records.append({**tag,'alpha':alpha,'model':name,'status':'fit','RMSE':float(np.sqrt(np.mean(residual**2))),'MAE':float(np.mean(abs(residual))),
                          'Q2_training_mean':float(1-np.sum(residual**2)/np.sum((y-loo(np.empty((len(y),0)),y,alpha))**2))})
                    gain=(y-outputs['alternative'])**2-(y-outputs['joint'])**2
                    checks.append({**tag,'alpha':alpha,'comparison':'joint_minus_alternative','MSE_improvement':float(gain.mean()),'patients_improved':int((gain>0).sum()),'heldout_outcome_isolation_passed':True})
    pd.DataFrame(features).to_csv(OUT/'A12_model_inputs.csv',index=False)
    pd.DataFrame(predictions).to_csv(OUT/'A12_heldout_predictions.csv',index=False)
    pd.DataFrame(records).to_csv(OUT/'A12_model_metrics.csv',index=False)
    result={'status':'exploratory_pilot_complete','input_sha256':inputs,'coverage':coverage,'comparisons':checks,'no_confirmatory_inference':True,'source_attribution':'conditional on assigned macrophages; unknown cells not relabelled'}
    (OUT/'A12_pilot_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'primary_comparisons':[r for r in checks if r['uncertainty']==0.2 and r['cell_floor']==50 and r['alpha']==1],'coverage':coverage,'sensitivity_checks':len(checks)}))

if __name__=='__main__':main()
