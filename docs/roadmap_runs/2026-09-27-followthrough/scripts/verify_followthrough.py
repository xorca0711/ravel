"""Read-only independent checks of follow-through artefacts and held-out prediction."""
import ast,collections,csv,gzip,hashlib,io,json
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((OUT/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 checks=0;pred_count=0
 for rq in ['A12','A13']:
  spec=read(f'{rq}_pilot_specification.json');result=read(f'{rq}_pilot_results.json')
  assert sha(OUT/f'{rq}_pilot_specification.json')==result['input_sha256']['specification'];checks+=1
  for name,digest in result['input_sha256'].items():
   if name=='specification':continue
   p=Path(name);p=p if p.is_absolute() else ROOT/p
   assert sha(p)==digest;checks+=1
  features=pd.read_csv(OUT/f'{rq}_model_inputs.csv',dtype={'patient':str})
  preds=pd.read_csv(OUT/f'{rq}_heldout_predictions.csv',dtype={'patient':str})
  keys=(['recipient'] if rq=='A12' else [])+['uncertainty','cell_floor','alpha','model']
  for group,d in preds.groupby(keys):
   selected=features.copy();vals=dict(zip(keys,group))
   for name,value in vals.items():
    if name not in ['alpha','model']:selected=selected[selected[name]==value]
   assert selected.patient.is_unique and set(d.patient)==set(selected.patient)
   selected=selected.set_index('patient').loc[d.patient].reset_index();y=selected.response.to_numpy();x=selected[spec['models'][vals['model']]].to_numpy()
   for i,row in enumerate(d.itertuples()):
    mask=np.arange(len(y))!=i;mean_y=y[mask].mean()
    if x.shape[1]:
     xm=x[mask].mean(axis=0);sd=x[mask].std(axis=0);sd[sd==0]=1
     z=(x[mask]-xm)/sd
     # Independent augmented least-squares implementation, not production normal equations.
     aug=np.vstack([z,np.sqrt(vals['alpha'])*np.eye(x.shape[1])]);yy=np.r_[y[mask]-mean_y,np.zeros(x.shape[1])]
     b=np.linalg.lstsq(aug,yy,rcond=None)[0];pred=mean_y+((x[i]-xm)/sd)@b
    else:pred=mean_y
    assert abs(pred-row.predicted)<1e-10
    assert abs((y[i]-pred)**2-row.squared_error)<1e-10
    pred_count+=1
   checks+=1
  metrics=pd.read_csv(OUT/f'{rq}_model_metrics.csv')
  for row in metrics[metrics.status.eq('fit')].to_dict('records'):
   d=preds.copy()
   for k in keys:d=d[d[k]==row[k]]
   assert len(d)==row['n'] and abs(np.sqrt(d.squared_error.mean())-row['RMSE'])<1e-10;checks+=1
  for c in result['comparisons']:
   d=preds[(preds.uncertainty==c['uncertainty'])&(preds.cell_floor==c['cell_floor'])&(preds.alpha==c['alpha'])]
   if rq=='A12':d=d[d.recipient==c['recipient']]
   a=d[d.model.eq('alternative')].set_index('patient').squared_error
   b=d[d.model.eq('joint')].set_index('patient').squared_error
   assert abs((a-b).mean()-c['MSE_improvement'])<1e-10;checks+=1
 external=read('A13_external_coverage_results.json');raw=gzip.decompress((OUT/'inputs/GSE122960_author_meta.tsv.gz').read_bytes());assert sha(OUT/'inputs/GSE122960_author_meta.tsv.gz') and hashlib.sha256(raw).hexdigest()==external['raw_sha256']
 rows=list(csv.DictReader(io.StringIO(raw.decode()),delimiter='\t'));assert len(rows)==76070 and len({r['Cell'] for r in rows})==76070
 counts=collections.Counter((r['Subject ID'],r['Cluster']) for r in rows)
 for row in external['per_subject']:
  values=[counts[row['subject'],label] for label in ['AT2 Cells','Fibroblasts','Macrophages']]
  assert values==[row[k] for k in ['epithelial','fibroblast','myeloid']]
  for n in [30,50,100]:assert row[f'complete_{n}']==all(v>=n for v in values)
  checks+=1
 assert sum(r['complete_50'] for r in external['per_subject'])==3
 assert sum(r['complete_30'] for r in external['per_subject'])==9
 assert sum(r['complete_100'] for r in external['per_subject'])==0
 assert len(list((OUT/'metadata').glob('GSE*.json')))==18
 assert read('A3_design_cells.json')['later_controls']==0
 assert sum(read('A11_candidate_design.json')['tissue_counts'].values())==91
 assert read('GSE262927_early_state_coverage.json')['eligible_transition_samples_upper_bound']==1
 ledger=read('remaining_work.json');assert {r['rq'] for r in ledger['questions']}=={f'A{i}' for i in range(16)}|{'A12-S1'}
 assert not ledger['new_biological_experiments'] and not ledger['new_claim_grades']
 for p in (OUT/'scripts').glob('*.py'):ast.parse(p.read_text());checks+=1
 print(json.dumps({'status':'passed','independent_prediction_checks':pred_count,'group_source_and_metric_checks':checks,'external_cells_recounted':76070,'candidate_records':18,'RQ_entries':17}))
if __name__=='__main__':main()
