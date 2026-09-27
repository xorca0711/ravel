import collections,csv,datetime,gzip,hashlib,io,json,urllib.request
from pathlib import Path
OUT=Path(__file__).resolve().parents[1];(OUT/'inputs').mkdir(exist_ok=True)
url='https://sqlifts.fsm.northwestern.edu/public/resources/fig1/meta.tsv'
spec={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cohort':'GSE122960 author Figure 1 browser','annotation_url':url,'labels':{'epithelial':'AT2 Cells','fibroblast':'Fibroblasts','myeloid':'Macrophages'},'floors':[50,30,100],'unit':'author SubjectID; condition kept; no pooling across subjects','rule':'each exact single label reaches floor; no substituting pooled epithelium, monocytes, other ILD or another fibroblast state','threshold':10,'scope':'coverage only; diagnosis/subject crosswalk must be explicit before combining disease groups or fitting; no inference or expression score'}
sp=OUT/'A13_external_coverage_specification.json'
if not sp.exists():sp.write_text(json.dumps(spec,indent=2)+'\n')
cached=OUT/'inputs/GSE122960_author_meta.tsv.gz'
if cached.exists():raw=gzip.decompress(cached.read_bytes())
else:
 raw=urllib.request.urlopen(url,timeout=60).read(8000000);assert len(raw)<8000000
 cached.write_bytes(gzip.compress(raw,mtime=0))
rows=list(csv.DictReader(io.StringIO(raw.decode()),delimiter='\t'));assert len(rows)==76070
counts=collections.Counter((r['Subject ID'],r['Condition'],r['Cluster']) for r in rows)
subjects=sorted({(s,c) for s,c,k in counts});out=[]
for sub,cond in subjects:
 d={key:counts[sub,cond,label] for key,label in spec['labels'].items()}
 out.append({'subject':sub,'condition':cond,**d,**{f'complete_{n}':all(x>=n for x in d.values()) for n in [50,30,100]}})
with (OUT/'A13_external_subject_coverage.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
record={'status':'counts_complete','source_url':url,'raw_sha256':hashlib.sha256(raw).hexdigest(),'cells':len(rows),'subjects':len(subjects),'per_subject':out,'primary_complete':sum(r['complete_50'] for r in out),'schema_correction':'Browser internal key SubjectID is exported as Subject ID; first attempt refused before counts, corrected literal header without changing selection or thresholds.'}
(OUT/'A13_external_coverage_results.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
