"""Reproduce source annotation joins only; no clone definition or endpoint."""
from pathlib import Path
import csv,io,json,hashlib,sys
B=Path(__file__).resolve().parent
meta=json.loads((B/'A27_IGT29_LABEL_PROVENANCE_V1.json').read_text())
source=Path(meta['subset_path']); raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()==meta['subset_sha256']
ann=list(csv.DictReader(io.StringIO(raw.decode()),delimiter='\t'))
lookup={x['IGT.cellID']:x for x in ann};assert len(lookup)==len(ann)==12953
original=B/'A27_IGT29_BARCODE_JOIN_V1.tsv'
rows=list(csv.DictReader(io.StringIO(original.read_text()),delimiter='\t'))
assert len({r['cell_id'] for r in rows})==len(rows)==13332
fields=list(rows[0])+['annotation_present','annotation_IGTHT','annotation_level1','annotation_level2','annotation_level2_group']
counts={};conflicts=[];label_conflicts=[]
for row in rows:
 a=lookup.get(row['cell_id']);status=row['join_disposition']
 counts.setdefault(status,{'total':0,'separate_annotation':0,'no_separate_annotation':0})
 counts[status]['total']+=1;counts[status]['separate_annotation' if a else 'no_separate_annotation']+=1
 row['annotation_present']='yes' if a else 'no'
 for dest,src in [('annotation_IGTHT','IGTHT'),('annotation_level1','level1'),('annotation_level2','level2'),('annotation_level2_group','level2.group')]:row[dest]=a.get(src,'') if a else ''
 if a:
  expected=row['TCR_IGTHT'] or {'HT'+str(i):'I29H'+str(i) for i in range(1,10)}[row['GEX_hashtag']]
  if a['IGTHT']!=expected:conflicts.append(row['cell_id'])
  if status=='both' and (row['source_level1']!=a['level1'] or row['source_level2']!=a['level2']):label_conflicts.append(row['cell_id'])
assert not conflicts and not label_conflicts
out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
blob=out.getvalue().encode()
summary={'date':'2026-11-04','scope':'source annotation coverage and exact identifier concordance only; no clone/state concentration','inputs':{original.name:hashlib.sha256(original.read_bytes()).hexdigest(),'separate_annotation_subset':meta['subset_sha256']},'join_rows':len(rows),'coverage_by_join_disposition':counts,'annotation_hashtag_conflicts':len(conflicts),'shared_label_conflicts':len(label_conflicts),'source_CD8_level2_codes':sorted({r['annotation_level2'] for r in rows if r['annotation_level1']=='CD8'}),'output_sha256':hashlib.sha256(blob).hexdigest(),'interpretation':'V1 source_level columns came from the receptor table; blank GEX-only labels there do not establish missing separate RNA-state annotation. Separate annotation fields are kept distinct.'}
outputs={'A27_IGT29_SOURCE_JOIN_V2.tsv':blob,'A27_IGT29_SOURCE_JOIN_V2.json':(json.dumps(summary,indent=2)+'\n').encode()}
for name,data in outputs.items():
 f=B/name
 if f.exists():assert f.read_bytes()==data,'Existing output differs: '+name
 elif '--write-missing' in sys.argv:f.write_bytes(data)
 else:raise FileNotFoundError(name+'; use --write-missing only for absent outputs')
print(json.dumps({'rows':len(rows),'coverage':counts,'hashtag_conflicts':0,'label_conflicts':0,'mode':'verify or create absent outputs'}))
