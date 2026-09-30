"""Cache public primary literature; metadata and hashes are tracked, payloads ignored."""
from pathlib import Path
import concurrent.futures, hashlib, json, re, urllib.request
BASE=Path(__file__).resolve().parents[1]
URLS={
 'GSE249931.soft':'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE249931&targ=all&form=text&view=full',
 'Zhou2025.xml':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12628998/fullTextXML',
 'Zhou2025_supplement.pdf':'https://static-content.springer.com/esm/art%3A10.1186%2Fs12964-025-02501-8/MediaObjects/12964_2025_2501_MOESM1_ESM.pdf',
 'Jones2024.xml':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13159043/fullTextXML',
 'Guo2023.xml':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10387117/fullTextXML',
 'GSE135893.soft':'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135893&targ=self&form=text&view=full',
}
def fetch(item):
 name,url=item;p=BASE/'cache'/name
 try:
  if not p.exists():p.write_bytes(urllib.request.urlopen(url,timeout=50).read())
  return dict(file='cache/'+name,url=url,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status='retrieved')
 except Exception as e:return dict(file='cache/'+name,url=url,status='failed',error=str(e))
def main():
 (BASE/'cache').mkdir(exist_ok=True)
 rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(fetch,URLS.items()))
 (BASE/'metadata/download_manifest.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
 p=BASE/'cache/GSE249931.soft'
 if p.exists():
  samples=[]
  for block in p.read_text(errors='replace').split('^SAMPLE = ')[1:]:
   samples.append({'gsm':block.splitlines()[0].strip(),'title':re.search(r'^!Sample_title = (.+)$',block,re.M).group(1).strip(),'characteristics':re.findall(r'^!Sample_characteristics_ch1 = (.+)$',block,re.M)})
  (BASE/'metadata/jones_sample_inventory.json').write_text(json.dumps(samples,indent=2)+'\n')
 for r in rows:print(r['file'],r['status'])
if __name__=='__main__':main()
