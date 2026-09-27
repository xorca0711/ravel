import collections,csv,gzip,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
SRC=Path(__file__).resolve().parents[1]/'inputs'
OUT=ROOT/'docs/roadmap_runs/2026-09-27'
def tsv(path):return list(csv.DictReader(path.open(encoding='utf-8-sig',newline=''),delimiter='\t'))
def well(x):return x[0]+str(int(x[1:])).zfill(2)
joined=tsv(ROOT/'RQ_Specified/A10_organoid_growth_outcome/tables/well_join.tsv')
geo=tsv(ROOT/'RQ_Specified/A10_organoid_growth_outcome/tables/followup_v1/diagnostic_geo_sample_fields.tsv')
gs={x['library_name']:x for x in geo}
design=list(csv.DictReader(io.StringIO(gzip.decompress((SRC/'GSE307112_plate_design.csv.gz').read_bytes()).decode())))
di={(r['plate'],well(r['well'])):r for r in design}
assert len(gs)==886 and len(di)==len(design)==232
rows=[]
for r in joined:
    d=di.get((r['plate'],well(r['well_key'])))
    if d is None:assert r['crispr_target']=='TDTOMATO',r
    else:assert d['gene_id']==r['gene_id'],r
    g=gs[r['library name']]
    assert g['batch'].replace('-','-rep')==r['unit']
    guide='|'.join(d[f'sgrna{i}'] for i in (1,2,3)) if d else None
    rows.append({'library':r['library name'],'gsm':g['gsm'],'target':r['crispr_target'],'plate':r['plate'],
        'deposited_repeat_label':g['batch'],'position':well(r['well_key']),
        'guide_pool_sha256':hashlib.sha256(guide.encode()).hexdigest() if guide else 'not_in_plate_design',
        'guide_count':sum(bool(d[f'sgrna{i}']) for i in (1,2,3)) if d else 'unknown',
        'day07_area':r['organoids_area_mean_day07'],'day14_area':r['organoids_area_mean_day14'],
        'animal_id':'unknown','isolation_id':'unknown','fibroblast_donor_id':'unknown','fibroblast_lot_id':'unknown',
        'source':'GEO sample description + deposited plate design + tracked imaging join'})
by=collections.defaultdict(list)
for r in rows:by[r['target']].append(r)
stats=[{'target':t,'libraries':len(rr),'plates':len({r['plate'] for r in rr}),
        'positions':len({r['position'] for r in rr}),'guide_pools':len({r['guide_pool_sha256'] for r in rr if r['guide_pool_sha256']!='not_in_plate_design'}),
        'plate_positions':len({(r['plate'],r['position']) for r in rr})} for t,rr in sorted(by.items())]
assert len(rows)==886 and len(by)==203
focus={x['target']:x for x in stats if x['target'] in ('AREG','ITGB6','EGFR','ERBB2','ERBB3','ERBB4')}
for r in focus.values():assert r['plates']==r['positions']==r['guide_pools']==1
for name,values in [('P1_library_crosswalk.tsv',rows),('P1_target_identifiability.tsv',stats)]:
    with (OUT/name).open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(values[0]),delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(values)
summary={'libraries':len(rows),'unique_targets':len(by),'cross_plate_targets':sum(x['plates']>1 for x in stats),
         'axis_targets':focus,'preparation_identifiers_recovered_from_deposited_tables':0,
         'libraries_without_plate_design':sum(r['guide_pool_sha256']=='not_in_plate_design' for r in rows),
         'unmapped_target':'TDTOMATO only; guide pool is unknown, not an additional measured pool',
         'finding':'Each nominated axis target is inseparable from its one position and one guide pool in this screen; deposited repeat labels do not establish biological replication.',
         'sources':json.loads((SRC/'p1_metadata_retrieval.json').read_text())}
for r in summary['sources']:r.pop('preview',None)
(OUT/'P1_crosswalk_checks.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='sources'}))
