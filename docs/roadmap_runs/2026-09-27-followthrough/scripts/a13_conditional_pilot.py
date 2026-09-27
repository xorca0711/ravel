"""A13 fixed-state matched-triad exploratory comparison, following frozen specification."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from a12_conditional_pilot import loo
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parents[1]
PAPER=Path('Research Article/gate2_C3_yu_lee_choi_min_2026')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--data-root',type=Path,required=True);args=p.parse_args()
 sp=OUT/'A13_pilot_specification.json';spec=json.loads(sp.read_text());response=set(spec['response']['genes']);fib=set(spec['fibroblast_predictor']['genes']);assert not response&fib
 records=[];predictions=[];inputs=[];audit=[];coverage=[];hashes={'specification':sha(sp)}
 for unc in [20,30]:
  mp=ROOT/PAPER/f'trials/u5_human_niche/unc{unc}_pooled_units.csv';raw=args.data_root/PAPER/f'cache/u5_human_niche/unc{unc}_pooled_triad_counts.csv.gz'
  hashes[str(mp.relative_to(ROOT))]=sha(mp);hashes[str(raw)]=sha(raw)
  meta=pd.read_csv(mp,dtype={'patient':str}).set_index('unit_id',drop=False)
  keep=meta.histology.isin(['normal','LUAD'])&((meta.comp.eq('macrophages')&meta.view.eq('broad'))|meta.label.isin(['AT2','Alveolar fibroblasts']))
  chosen=meta.loc[keep];units=chosen.index.tolist();sums=np.zeros(len(units),dtype=np.int64);parts=[]
  for chunk in pd.read_csv(raw,usecols=['gene']+units,chunksize=500):
   arr=chunk[units].to_numpy();assert np.isfinite(arr).all() and (arr>=0).all() and (arr==np.floor(arr)).all();sums+=arr.sum(axis=0,dtype=np.int64)
   parts.append(chunk[chunk.gene.isin(response|fib|{'IL1B','TNF'})].set_index('gene')[units])
  count=pd.concat(parts);assert count.index.is_unique and np.array_equal(sums,chosen.full_library_sum.to_numpy())
  resp=sorted(response&set(count.index));fg=sorted(fib&set(count.index));assert len(resp)/spec['response']['source_genes']>=0.7 and len(fg)/len(fib)>=0.7
  log=np.log2(1+count.div(chosen.full_library_sum,axis='columns')*1e6)
  coverage.append({'uncertainty':unc/100,'response_present':len(resp),'response_human_list':len(response),'response_original_source':spec['response']['source_genes'],'fibroblast_present':len(fg),'fibroblast_frozen':len(fib),'count_sum_parity':True})
  for floor in ([50,30,100] if unc==20 else [50]):
   frame=[]
   for patient in sorted(chosen.patient.unique(),key=int):
    vals={};valid=True
    for hist in ['normal','LUAD']:
     part=chosen[(chosen.patient==patient)&(chosen.histology==hist)];a=part[part.label.eq('AT2')];f=part[part.label.eq('Alveolar fibroblasts')];m=part[part.comp.eq('macrophages')]
     if any(len(t)!=1 or int(t.cells.iloc[0])<floor for t in [a,f,m]):valid=False;break
     mono=meta[(meta.patient==patient)&(meta.histology==hist)&meta.label.eq('Monocyte-derived Mph')].cells.sum()
     vals[hist]={'response':float(log.loc[resp,a.index[0]].mean()),'fibroblast_program':float(log.loc[fg,f.index[0]].mean()),'IL1B':float(log.loc['IL1B',m.index[0]]),'TNF':float(log.loc['TNF',m.index[0]]),'mono_fraction':float(mono/m.cells.iloc[0])}
    if valid:frame.append({'patient':patient,**{k:vals['LUAD'][k]-vals['normal'][k] for k in vals['LUAD']}})
   data=pd.DataFrame(frame);tag={'uncertainty':unc/100,'cell_floor':floor,'n':len(data)}
   if len(data)<10:records.append({**tag,'status':'not_fit_below_floor'});continue
   inputs.extend({**tag,**row} for row in data.to_dict('records'));y=data.response.to_numpy();assert y.std()>0
   for alpha in ([1.,.1,10.] if unc==20 and floor==50 else [1.]):
    out={};null=loo(np.empty((len(y),0)),y,alpha)
    for name,cols in spec['models'].items():
     x=data[cols].to_numpy();pred=loo(x,y,alpha);out[name]=pred;other=y.copy();other[0]+=1000;assert abs(loo(x,other,alpha)[0]-pred[0])<1e-10
     err=y-pred;records.append({**tag,'alpha':alpha,'model':name,'status':'fit','RMSE':float(np.sqrt(np.mean(err**2))),'MAE':float(np.mean(abs(err))),'Q2_training_mean':float(1-sum(err**2)/sum((y-null)**2))})
     predictions.extend({**tag,'alpha':alpha,'model':name,'patient':patient,'observed':obs,'predicted':pr,'squared_error':e*e} for patient,obs,pr,e in zip(data.patient,y,pred,err))
    gain=(y-out['alternative'])**2-(y-out['joint'])**2
    audit.append({**tag,'alpha':alpha,'MSE_improvement':float(gain.mean()),'patients_improved':int((gain>0).sum()),'heldout_outcome_isolation_passed':True})
 pd.DataFrame(inputs).to_csv(OUT/'A13_model_inputs.csv',index=False);pd.DataFrame(predictions).to_csv(OUT/'A13_heldout_predictions.csv',index=False);pd.DataFrame(records).to_csv(OUT/'A13_model_metrics.csv',index=False)
 result={'status':'exploratory_pilot_complete','input_sha256':hashes,'coverage':coverage,'comparisons':audit,'no_claim_grade_change':True,'new_rule':'Fixed AT2 and Alveolar fibroblasts with broad assigned macrophages; historical single-label gate remains unchanged'}
 (OUT/'A13_pilot_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
