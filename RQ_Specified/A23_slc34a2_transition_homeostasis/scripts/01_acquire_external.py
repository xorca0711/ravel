"""Retrieve A23 public processed counts and source workbook, preserving source bytes."""
import datetime, hashlib, json, shutil, tarfile, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
RQ = ROOT / 'RQ_Specified/A23_slc34a2_transition_homeostasis'
FILES = {
 'GSE199329_RAW.tar': 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE199nnn/GSE199329/suppl/GSE199329_RAW.tar',
 '41467_2023_36810_MOESM9_ESM.xlsx': 'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-36810-8/MediaObjects/41467_2023_36810_MOESM9_ESM.xlsx'
}
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
 return h.hexdigest()
def main():
 raw=ROOT/'raw_data/GSE199329'; raw.mkdir(parents=True,exist_ok=True)
 out=RQ/'metadata/external_acquisition_v1'; out.mkdir(parents=True,exist_ok=True)
 receipt=out/'sources.json'
 expected=json.loads(receipt.read_text(encoding='utf-8')) if receipt.exists() else None
 records=[]
 for name,url in FILES.items():
  p=raw/name
  if not p.exists():
   temp=p.with_suffix(p.suffix+'.part')
   req=urllib.request.Request(url,headers={'User-Agent':'A23 academic public-data audit'})
   with urllib.request.urlopen(req,timeout=90) as response, temp.open('wb') as dest:
    shutil.copyfileobj(response,dest)
   temp.replace(p)
  records.append(dict(path=p.relative_to(ROOT).as_posix(),url=url,bytes=p.stat().st_size,sha256=digest(p)))

  if expected:
   saved=next(r for r in expected['source_files'] if r.get('url')==url)
   if records[-1]['sha256']!=saved['sha256']: raise ValueError('Downloaded source differs from receipt')
  print(name,p.stat().st_size,flush=True)
 members=[]; matrices=[]
 with tarfile.open(raw/'GSE199329_RAW.tar') as archive:
  for m in archive.getmembers():
   members.append(dict(name=m.name,bytes=m.size,type=str(m.type)))
   if not m.isfile() or not m.name.endswith('.tar.gz'): continue
   library=m.name.split('_')[0]
   if library not in ['GSM5970468','GSM5970469','GSM5970470']: raise ValueError('Unexpected library')
   with tarfile.open(fileobj=archive.extractfile(m),mode='r:gz') as inner:
    for im in inner.getmembers():
     if not im.isfile() or 'filtered' not in im.name.lower() or not im.name.endswith('.h5'): continue
     p=raw/(library+'_'+Path(im.name).name)
     if p.resolve().parent != raw.resolve(): raise ValueError('Unsafe member')
     if not p.exists():
      with inner.extractfile(im) as src,p.open('wb') as dest: shutil.copyfileobj(src,dest)
     matrices.append(dict(library=library,path=p.relative_to(ROOT).as_posix(),outer_member=m.name,inner_member=im.name,bytes=p.stat().st_size,sha256=digest(p)))
 if not expected:
  receipt.write_text(json.dumps(dict(retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_files=records,tar_inventory=members),indent=2)+'\n',encoding='utf-8')
 mp=out/'matrices.json'
 if mp.exists():
  if json.loads(mp.read_text(encoding='utf-8'))!=matrices: raise ValueError('Matrix receipt mismatch')
 else: mp.write_text(json.dumps(matrices,indent=2)+'\n',encoding='utf-8')
 print('Verified',len(matrices),'filtered matrices',flush=True)
if __name__=='__main__': main()
