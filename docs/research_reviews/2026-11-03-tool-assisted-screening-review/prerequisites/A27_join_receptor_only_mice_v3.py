"""Complete exact source-hashtag mapping for receptor-only records; preserve v2."""
from pathlib import Path
import csv,io,json,hashlib,sys,collections
B=Path(__file__).resolve().parent
source=B/'A27_IGT29_SOURCE_JOIN_V2.tsv';raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()==json.loads((B/'A27_IGT29_SOURCE_JOIN_V2.json').read_text())['output_sha256']
rows=list(csv.DictReader(io.StringIO(raw.decode()),delimiter='\t'))
mm=json.loads((B/'A27_IGT29_JOIN_SUMMARY_V1.json').read_text())['mouse_map'];mapping={v['IGTHT']:v for v in mm.values()};filled=[];counts=collections.Counter()
for r in rows:
 if r['TCR_IGTHT']:
  m=mapping[r['TCR_IGTHT']]
  if r['mouse']:assert (r['mouse'],r['age_weeks'],r['sex'])==(m['mouse'],m['age_weeks'],m['sex'])
  else:
   assert r['join_disposition']=='receptor_only';r.update({k:m[k] for k in ['mouse','age_weeks','sex']});filled.append(r['cell_id'])
 r['mouse_mapping_basis']='TCR_hashtag_only' if r['join_disposition']=='receptor_only' else 'GEX_hashtag'
 assert r['mouse'] and r['age_weeks'] and r['sex']
 if r['join_disposition']=='receptor_only':counts[r['mouse']]+=1
assert len(filled)==354
o=io.StringIO(newline='');w=csv.DictWriter(o,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows);blob=o.getvalue().encode()
m={'date':'2026-11-04','amends':'A27_IGT29_SOURCE_JOIN_V2.tsv','reason':'The354 receptor-only rows retained valid I29H1-I29H9 source hashtags but v2 left mouse/age/sex blank because it used GEX mapping. Fill from the already verified exact source-hashtag map; no new animal or state label inferred.','input_sha256':hashlib.sha256(raw).hexdigest(),'source_mouse_map_sha256':hashlib.sha256((B/'A27_IGT29_JOIN_SUMMARY_V1.json').read_bytes()).hexdigest(),'rows':len(rows),'filled_receptor_only_rows':len(filled),'receptor_only_by_mouse':dict(sorted(counts.items())),'output_sha256':hashlib.sha256(blob).hexdigest(),'scope':'Source identity completion only; all original annotation/chain fields and row order preserved;354 receptor-only cells still lack separate state annotation.'}
for n,d in {'A27_IGT29_SOURCE_JOIN_V3.tsv':blob,'A27_IGT29_SOURCE_JOIN_V3.json':(json.dumps(m,indent=2)+'\n').encode()}.items():
 p=B/n
 if p.exists():assert p.read_bytes()==d
 elif '--write-missing' in sys.argv:p.write_bytes(d)
 else:raise FileNotFoundError(n)
print(json.dumps({'filled':354,'receptor_only_by_mouse':m['receptor_only_by_mouse']}))
