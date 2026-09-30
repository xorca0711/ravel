"""Extract only prespecified workbook assays and uninfected bulk libraries."""
from pathlib import Path
import hashlib,json,re,sys
import numpy as np
import pandas as pd
import openpyxl
BASE=Path(__file__).resolve().parents[1]
TABLES=BASE/'tables/exploratory_v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 TABLES.mkdir(parents=True,exist_ok=True);(BASE/'reports').mkdir(exist_ok=True)
 cfg=json.loads((BASE/'config/exploratory_v1.json').read_text(encoding='utf-8'))
 frozen=BASE/'reports/exploratory_v1_contract.json'
 if not frozen.exists():frozen.write_text(json.dumps({'contract':cfg,'contract_sha256':sha(BASE/'config/exploratory_v1.json'),'input_sha256':{x['file']:x['sha256'] for x in json.loads((BASE/'metadata/download_manifest.json').read_text())}},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 else:assert json.loads(frozen.read_text(encoding='utf-8'))['contract_sha256']==sha(BASE/'config/exploratory_v1.json')
 w=openpyxl.load_workbook(BASE/cfg['qpcr']['file'],read_only=True,data_only=True);rows=[]
 aliases={'GSK3β':'GSK3B','P63':'TP63','TGFb1':'TGFB1'}
 for sheet in cfg['qpcr']['sheets']:
  gene=condition=None
  for cells in w[sheet].iter_rows(min_row=4):
   vals=[c.value for c in cells]
   if vals[0] is not None:gene=str(vals[0]).strip()
   if vals[1] is not None:condition=str(vals[1]).strip()
   donor=str(vals[2]).strip() if vals[2] is not None else ''
   if not re.fullmatch(r'D\d+',donor):continue
   dct=vals[3];numeric=isinstance(dct,(int,float)) and np.isfinite(dct)
   rows.append({'sheet':sheet.strip(),'source_row':cells[0].row,'gene':aliases.get(gene,gene),'source_gene':gene,'condition':condition,'donor':donor,'delta_ct':float(dct) if numeric else np.nan,'delta_ct_source':str(dct),'ct_status':'measured' if numeric else 'undetected' if str(dct).startswith('undet') else 'missing','ddct':vals[4] if isinstance(vals[4],(int,float)) else np.nan,'source_fold':vals[5] if isinstance(vals[5],(int,float)) else np.nan})
 w.close();df=pd.DataFrame(rows);assert not df.duplicated(['sheet','gene','condition','donor']).any();df.to_csv(TABLES/'qpcr_source_rows.tsv',sep='\t',index=False,na_rep='NA')
 meta=pd.DataFrame(json.loads((BASE/'metadata/bulk_samples.json').read_text()));counts=[]
 for row in meta.itertuples():
  path=BASE/'cache'/row.url.split('/')[-1]
  d=pd.read_csv(path,sep='\t',comment='#',usecols=[0,6]);d.columns=['gene_id',row.title];d=d.set_index('gene_id');assert not d.index.duplicated().any();assert np.all(d.values>=0) and np.all(d.values==np.floor(d.values));counts.append(d)
 matrix=pd.concat(counts,axis=1);assert not matrix.isna().any().any();matrix.to_csv(BASE/'cache/bulk_counts.tsv.gz',sep='\t')
 meta.to_csv(TABLES/'bulk_samples.tsv',sep='\t',index=False)
 pd.DataFrame({'sample':matrix.columns,'total_counts':matrix.sum().values,'genes_detected':(matrix>0).sum().values}).to_csv(TABLES/'bulk_qc.tsv',sep='\t',index=False)
 print(f'Extracted {len(df)} qPCR source rows; {len(matrix)} count rows x {matrix.shape[1]} libraries. Nonquantified Ct rows: {(df.ct_status!="measured").sum()}')
if __name__=='__main__':main()
