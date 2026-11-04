"""Source-chain eligibility coverage only. No cross-cell receptor keys or clone outcomes."""
from pathlib import Path
import csv,io,json,hashlib,re,sys,collections
B=Path(__file__).resolve().parent
extract=json.loads((B/'A27_IGT29_EXTRACTION_V1.json').read_text())
source=Path(extract['selected_path']);raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()==extract['selected_sha256']
records=list(csv.DictReader(io.StringIO(raw.decode()),delimiter='\t'));lookup={r['IGT.cellID']:r for r in records};assert len(lookup)==len(records)==12743
join_path=B/'A27_IGT29_SOURCE_JOIN_V2.tsv';jraw=join_path.read_bytes();jm=json.loads((B/'A27_IGT29_SOURCE_JOIN_V2.json').read_text());assert hashlib.sha256(jraw).hexdigest()==jm['output_sha256']
joined=list(csv.DictReader(io.StringIO(jraw.decode()),delimiter='\t'))
allowed={'','productive','unproductive','No results','No rearrangement found'}
flags=['receptor_present','single_pair_eligible','complete_set_eligible','productive_incomplete','nonstandard','alpha_only','beta_only','no_productive','multiple_alpha_slots','multiple_beta_slots','ambiguous_productive_vj','unproductive_present','duplicate_productive_slot_record']
rows=[];coverage={};outside=collections.Counter()
for j in joined:
 r=lookup.get(j['cell_id']);f={k:0 for k in flags};f['receptor_present']=int(r is not None);n={'alpha':0,'beta':0};good={'alpha':[],'beta':[]}
 if r:
  for prefix in ['alpha','alpha2','beta','beta2']:
   chain='alpha' if prefix.startswith('alpha') else 'beta';func=r[prefix+'.functionality'];f['nonstandard']|=int(func not in allowed);f['unproductive_present']|=int(func=='unproductive')
   if func!='productive':continue
   n[chain]+=1;nt=r[prefix+'.junction.nt'];v=r[prefix+'.vgene'];g=r[prefix+'.jgene'];expected='TRA' if chain=='alpha' else 'TRB'
   valid=bool(nt and re.fullmatch('[ACGT]+',nt.upper()) and v and g and all(re.fullmatch(expected+'V[A-Z0-9/-]+',t) for t in v.split('|')) and all(re.fullmatch(expected+'J[A-Z0-9/-]+',t) for t in g.split('|')))
   f['productive_incomplete']|=int(not valid);f['ambiguous_productive_vj']|=int('|' in v or '|' in g)
   if valid:good[chain].append((nt.upper(),tuple(sorted(set(v.split('|')))),tuple(sorted(set(g.split('|'))))))
  f['multiple_alpha_slots']=int(n['alpha']>1);f['multiple_beta_slots']=int(n['beta']>1)
  f['alpha_only']=int(n['alpha']>0 and n['beta']==0);f['beta_only']=int(n['beta']>0 and n['alpha']==0);f['no_productive']=int(n['alpha']==n['beta']==0)
  f['duplicate_productive_slot_record']=int(any(len(x)!=len(set(x)) for x in good.values()))
  f['complete_set_eligible']=int(n['alpha']>0 and n['beta']>0 and not f['productive_incomplete'] and not f['nonstandard'])
  f['single_pair_eligible']=int(f['complete_set_eligible'] and n['alpha']==n['beta']==1)
 if not r:category='no_receptor_record'
 elif f['nonstandard']:category='nonstandard_rearrangement'
 elif f['productive_incomplete']:category='productive_incomplete'
 elif f['no_productive']:category='no_productive_chain'
 elif f['alpha_only']:category='alpha_only'
 elif f['beta_only']:category='beta_only'
 elif f['single_pair_eligible']:category='single_productive_pair'
 else:category='multiple_productive_slots_paired'
 row={k:j[k] for k in ['cell_id','join_disposition','mouse','age_weeks','sex','annotation_level1','annotation_level2']};row.update({'alpha_productive_slots':n['alpha'],'beta_productive_slots':n['beta'],'source_chain_category':category});row.update(f);rows.append(row)
 if j['join_disposition']=='receptor_only':outside[j['mouse']]+=1;continue
 key=(j['mouse'],j['age_weeks'],j['sex'],j['annotation_level1'] or 'ANNOTATION_MISSING',j['annotation_level2'] or 'ANNOTATION_MISSING')
 if key not in coverage:coverage[key]={'gex_cells':0,**{k:0 for k in flags}}
 x=coverage[key];x['gex_cells']+=1
 for k in flags:x[k]+=f[k]
assert len(rows)==13332 and sum(x['gex_cells'] for x in coverage.values())==12978
assert sum(outside.values())==354
coverage_rows=[]
for key,x in sorted(coverage.items()):coverage_rows.append(dict(zip(['mouse','age_weeks','sex','source_level1','source_level2'],key),**x))
mouse=[]
for m in sorted({r['mouse'] for r in coverage_rows}):
 x=[r for r in coverage_rows if r['mouse']==m and r['source_level1']=='CD8'];assert x
 z={k:x[0][k] for k in ['mouse','age_weeks','sex']};z.update({k:sum(v[k] for v in x) for k in ['gex_cells']+flags});z['receptor_only_all_lineages_unlabelled']=outside[m];mouse.append(z)
def tsv(rows):
 o=io.StringIO(newline='');w=csv.DictWriter(o,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows);return o.getvalue().encode()
outputs={'A27_CELL_CHAIN_COVERAGE_V1.tsv':tsv(rows),'A27_MOUSE_STATE_CHAIN_COVERAGE_V1.tsv':tsv(coverage_rows),'A27_CD8_MOUSE_CHAIN_COVERAGE_V1.tsv':tsv(mouse)}
summary={'date':'2026-11-04','scope':'source eligibility/selection coverage, no cross-cell clone assignment or concentration','inputs':{'receptor_subset_sha256':extract['selected_sha256'],'joined_metadata_sha256':jm['output_sha256']},'union_cells':len(rows),'gex_cells':12978,'receptor_only_unlabelled_cells':354,'CD8_GEX_totals':{k:sum(r[k] for r in mouse) for k in ['gex_cells']+flags},'CD8_source_state_count':len({r['source_level2'] for r in coverage_rows if r['source_level1']=='CD8'}),'flags_overlap':'Flags overlap; source_chain_category is a mutually exclusive ordered disposition. No-productivity means no source-annotated productive slot, not absence of a biological receptor.','complete_productive_slot_rule':'functionality exactly productive; nonempty ACGT nucleotide junction; nonempty matching TRA/TRB V and J call tokens. Pipe-delimited source ambiguity retained as sorted call sets, not resolved.','eligibility':'Single: exactly one productive alpha and beta slot, complete. Set: >=1 complete productive slot of each lineage. Both exclude any incomplete productive slot or nonstandard functionality; explicit nonproductive/empty/no-result secondary slots do not imply known biological absence.','duplicates':'Within-cell duplicate slot records identified only as a coverage flag; no cross-cell receptor keys or frequencies generated.','output_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in outputs.items()}}
outputs['A27_CHAIN_COVERAGE_MANIFEST_V1.json']=(json.dumps(summary,indent=2)+'\n').encode()
for name,data in outputs.items():
 p=B/name
 if p.exists():assert p.read_bytes()==data,'Existing bytes differ: '+name
 elif '--write-missing' in sys.argv:p.write_bytes(data)
 else:raise FileNotFoundError(name)
print(json.dumps({'CD8_GEX_totals':summary['CD8_GEX_totals'],'source_states':summary['CD8_source_state_count'],'source_only':354,'mouse_summary':mouse}))
