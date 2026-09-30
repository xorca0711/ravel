"""Retrieve public noninfectious differentiation inputs; full payloads stay in ignored cache."""
from pathlib import Path
import concurrent.futures, hashlib, json, re, urllib.request
BASE=Path(__file__).resolve().parents[1]
CACHE=BASE/'cache'
URLS={
 'engineered_lung.xml':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10147714/fullTextXML',
 'adult_organoids.xml':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9409623/fullTextXML',
 'GSE197949.soft':'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE197949&targ=all&form=text&view=full',
 'adult_source3.xlsx':'https://static-content.springer.com/esm/art%3A10.1038%2Fs42003-022-03828-5/MediaObjects/42003_2022_3828_MOESM6_ESM.xlsx',
}
def fetch(item):
 name,url=item;p=CACHE/name
 if not p.exists():
  req=urllib.request.Request(url,headers={'User-Agent':'A19-source-audit/1.0'})
  data=urllib.request.urlopen(req,timeout=60).read();p.write_bytes(data)
 return {'file':name,'url':url,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def main():
 CACHE.mkdir(exist_ok=True)
 rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(fetch,URLS.items()))
 samples=[]
 for block in (CACHE/'GSE197949.soft').read_text(errors='replace').split('^SAMPLE = ')[1:]:
  match=re.search(r'^!Sample_title = (.+)$',block,re.M)
  if not match or not re.fullmatch(r'(ctrl|GSK3kd)_(ctrl|CHIR)_[12]',match.group(1).strip()):continue
  title=match.group(1).strip();files=re.findall(r'^!Sample_supplementary_file_\d+ = (.+)$',block,re.M)
  url=next(x.strip().replace('ftp://','https://') for x in files if 'feature_counts' in x)
  samples.append({'gsm':block.splitlines()[0].strip(),'title':title,'block':int(title[-1]),'background':'GSK3KD' if title.startswith('GSK3') else 'control','input':'CHIR' if '_CHIR_' in title else 'no_CHIR','characteristics':'; '.join(re.findall(r'^!Sample_characteristics_ch1 = (.+)$',block,re.M)),'url':url})
 assert len(samples)==8
 rows+=list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(fetch,[(x['url'].split('/')[-1],x['url']) for x in samples]))
 (BASE/'metadata/bulk_samples.json').write_text(json.dumps(samples,indent=2)+'\n',encoding='utf-8')
 cfg=json.loads((BASE/'config/exploratory_v1.json').read_text(encoding='utf-8'))
 symbols=sorted(set(sum(cfg['bulk']['panels'].values(),[])+cfg['bulk']['sentinels']))
 annotation=CACHE/'human_marker_lookup.json';url='https://rest.ensembl.org/lookup/symbol/homo_sapiens'
 if not annotation.exists():
  req=urllib.request.Request(url,data=json.dumps({'symbols':symbols}).encode(),headers={'Content-Type':'application/json','Accept':'application/json'})
  annotation.write_bytes(urllib.request.urlopen(req,timeout=60).read())
 records=json.loads(annotation.read_text());assert all(x in records and records[x]['species']=='homo_sapiens' for x in symbols)
 (BASE/'metadata/human_marker_lookup.json').write_text(json.dumps({'url':url,'symbols':symbols,'records':records},indent=2)+'\n',encoding='utf-8')
 rows.append({'file':annotation.name,'url':url,'bytes':annotation.stat().st_size,'sha256':hashlib.sha256(annotation.read_bytes()).hexdigest()})
 (BASE/'metadata/download_manifest.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
 print(f'Inputs verified: {len(samples)} selected bulk libraries, {len(symbols)} human gene mappings.')
if __name__=='__main__':main()
