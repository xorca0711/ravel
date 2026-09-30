"""Descriptive reanalysis of published source-reported animal values."""
from pathlib import Path
import datetime,hashlib,json,re,zipfile
import numpy as np,pandas as pd
from source_workbooks import read_cells
BASE=Path(__file__).resolve().parents[1]
def sha(blob):return hashlib.sha256(blob).hexdigest()
def write(df,name):df.to_csv(BASE/'tables'/name,sep='\t',index=False,float_format='%.12g')
def main():
 if (BASE/'reports/source_complete.json').exists():raise SystemExit('Completed source analysis exists; version before rerun.')
 cfg=json.loads((BASE/'config/source_mapping.json').read_text());intake=json.loads((BASE/'metadata/intake.json').read_text())
 obs=[];cells=[];manifest=[];comparisons=[]
 for spec in cfg['panels']:
  path=BASE/'cache'/spec['archive'];rec=next(r for r in intake if r['file']==path.name and r['status']=='retrieved');assert sha(path.read_bytes())==rec['sha256']
  with zipfile.ZipFile(path) as z:
   member=next(n for n in z.namelist() if n.endswith('Figure '+spec['panel']+'.xlsx'));blob=z.read(member)
  sheet,data=read_cells(blob);manifest.append(dict(archive=path.name,archive_sha256=rec['sha256'],member=member,sha256=sha(blob),sheet=sheet))
  for address,c in data.items():cells.append(dict(panel=spec['panel'],archive=path.name,member=member,sheet=sheet,cell=address,stored_value=c['value'],formula=c['formula']))
  ns=[]
  for col,label in spec['columns'].items():
   assert data[col+'2']['value']==label
   selected=sorted((int(re.search(r'\d+',k).group()),k,c) for k,c in data.items() if re.fullmatch(col+r'\d+',k) and int(k[1:])>=3)
   for row,address,c in selected:
    assert isinstance(c['value'],(float,int)) and np.isfinite(c['value']) and c['formula'] is None
    assert re.fullmatch(r'data\s*\d+',str(data['A'+str(row)]['value']),re.I)
    obs.append(dict(panel=spec['panel'],outcome=spec['outcome'],unit=spec['unit'],intervention=spec['intervention'],source_group=label,source_column=col,source_row=row,source_row_label=data['A'+str(row)]['value'],value=float(c['value']),archive=path.name,member=member,sheet=sheet,cell=address,source_url=rec['url'],animal_id='unavailable; anonymous source row',pairing='unpaired; no cross-endpoint join'))
   ns.append(len(selected))
  assert ns==spec['expected_n'],(spec['panel'],ns)
  vals={col:np.array([r['value'] for r in obs if r['panel']==spec['panel'] and r['source_column']==col]) for col in spec['columns']}
  left,right=spec['contrast'];v,w=vals[left],vals[right]
  comparisons.append(dict(panel=spec['panel'],outcome=spec['outcome'],unit=spec['unit'],left_group=spec['columns'][left],right_group=spec['columns'][right],n_left=len(v),n_right=len(w),mean_left=v.mean(),mean_right=w.mean(),mean_difference=v.mean()-w.mean(),median_left=np.median(v),median_right=np.median(w),interpretation='source-reported biological replicate values; descriptive only'))
 df=pd.DataFrame(obs);write(df,'source_observations.tsv');write(pd.DataFrame(cells),'source_workbook_cells.tsv');write(pd.DataFrame(comparisons),'source_contrasts.tsv')
 sm=df.groupby(['panel','outcome','unit','source_column','source_group']).value.agg(n='size',mean='mean',median='median',minimum='min',maximum='max',sd='std').reset_index();write(sm,'source_summary.tsv')
 (BASE/'metadata/workbook_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 rec=dict(finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),config_sha256=sha((BASE/'config/exploratory_v1.json').read_bytes()),source_mapping_sha256=sha((BASE/'config/source_mapping.json').read_bytes()),comparator_sha256=sha((BASE/'config/perfusion_comparator.json').read_bytes()),workbooks=len(manifest),observations=len(df),observations_are_not_total_unique_mice=True,cross_endpoint_join=False,new_p_values=False,normal_capillary_lineage_test=False)
 (BASE/'reports/source_complete.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec));print(pd.DataFrame(comparisons)[['panel','n_left','n_right','mean_left','mean_right','mean_difference']].to_string(index=False))
if __name__=='__main__':main()
