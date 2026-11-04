"""Operational receptor-key concentration in nominal source codes; no population inference."""
from pathlib import Path
import argparse,csv,hashlib,json,math,re,collections
ROOT=Path(__file__).resolve().parents[3]
PRE=ROOT/'docs/research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites'
MICE=['mouse00'+str(i) for i in range(88,97)]
CODES=['CD8.'+x for x in ['A','B','C','D','E','F','G','H','I','J','K','P','Q','R','S','T','wM','wV','wX','wY']]
FLAGS=['receptor_present','single_pair_eligible','complete_set_eligible','productive_incomplete','nonstandard','alpha_only','beta_only','no_productive','multiple_alpha_slots','multiple_beta_slots','ambiguous_productive_vj','unproductive_present','duplicate_productive_slot_record']
MODES=['single_pair_primary','complete_set_sensitivity']
OUTPUTS=['cell_assignments.tsv','clone_counts.tsv','concentration_by_mouse_code.tsv','support_by_mouse_code.tsv','source_disposition_by_mouse.tsv','concentration_by_source_code.png','representation_and_eligibility.png','summary.json']
def require(x,message):
 if not x:raise ValueError(message)
def read_tsv(path):
 with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write_tsv(path,rows):
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def qualify(r):
 f={k:0 for k in FLAGS};f['receptor_present']=int(r is not None);n={'alpha':0,'beta':0};good={'alpha':[],'beta':[]}
 if r:
  for prefix in ['alpha','alpha2','beta','beta2']:
   chain='alpha' if prefix.startswith('alpha') else 'beta';func=r[prefix+'.functionality'];f['nonstandard']|=int(func not in {'','productive','unproductive','No results','No rearrangement found'});f['unproductive_present']|=int(func=='unproductive')
   if func!='productive':continue
   n[chain]+=1;nt=r[prefix+'.junction.nt'];v=r[prefix+'.vgene'];j=r[prefix+'.jgene'];expected='TRA' if chain=='alpha' else 'TRB'
   valid=bool(nt and re.fullmatch('[ACGT]+',nt.upper()) and v and j and all(re.fullmatch(expected+'V[A-Z0-9/-]+',t) for t in v.split('|')) and all(re.fullmatch(expected+'J[A-Z0-9/-]+',t) for t in j.split('|')))
   f['productive_incomplete']|=int(not valid);f['ambiguous_productive_vj']|=int('|' in v or '|' in j)
   if valid:good[chain].append((nt.upper(),tuple(sorted(set(v.split('|')))),tuple(sorted(set(j.split('|'))))))
  f['multiple_alpha_slots']=int(n['alpha']>1);f['multiple_beta_slots']=int(n['beta']>1);f['alpha_only']=int(n['alpha']>0 and n['beta']==0);f['beta_only']=int(n['beta']>0 and n['alpha']==0);f['no_productive']=int(n['alpha']==n['beta']==0)
  f['duplicate_productive_slot_record']=int(any(len(x)!=len(set(x)) for x in good.values()))
  f['complete_set_eligible']=int(n['alpha']>0 and n['beta']>0 and not f['productive_incomplete'] and not f['nonstandard']);f['single_pair_eligible']=int(f['complete_set_eligible'] and n['alpha']==n['beta']==1)
 canonical=(tuple(sorted(set(good['alpha']))),tuple(sorted(set(good['beta']))))
 return f,n,canonical
def key_id(mouse,canonical):return hashlib.sha256(json.dumps([mouse,canonical],separators=(',',':')).encode()).hexdigest()
def concentration(keys):
 counts=collections.Counter(keys);N=len(keys);pairs=N*(N-1)//2;collisions=sum(n*(n-1)//2 for n in counts.values());require(collisions<=pairs,'pair arithmetic')
 return {'eligible_cells':N,'observed_keys':len(counts),'same_key_pairs':collisions,'observed_pairs':pairs,'concentration':collisions/pairs if pairs else 'NA','single_collision_resolution':1/pairs if pairs else 'NA','support_status':'observed_pairs' if pairs else 'N_less_than_2'},counts
def fraction(n,d):return n/d if d else 'NA'
def draw(conc,support,metadata,output):
 import numpy as np
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 labels=['ALL_CD8']+CODES;mouse_labels=[m[-4:]+'\n'+metadata[m]['age_weeks']+'w '+metadata[m]['sex'][0].upper() for m in MICE]
 lookup={(r['convention'],r['mouse'],r['source_code']):r for r in conc};sl={(r['mouse'],r['source_code']):r for r in support}
 cmap=plt.get_cmap('YlOrRd').copy();cmap.set_bad('#d8d8d8')
 def panel(ax,values,texts,title):
  a=np.array([[float('nan') if x=='NA' else x for x in row] for row in values]);im=ax.imshow(a,cmap=cmap,vmin=0,vmax=1,aspect='auto')
  ax.set_yticks(range(len(labels)),labels,fontsize=9);ax.set_xticks(range(9),mouse_labels,fontsize=9);ax.set_title(title,loc='left',fontsize=13,pad=12)
  ax.axhline(.5,color='black',linewidth=1)
  for i,row in enumerate(texts):
   for j,text in enumerate(row):ax.text(j,i,text,ha='center',va='center',fontsize=7.5,color='white' if not math.isnan(a[i,j]) and a[i,j]>.58 else 'black')
  ax.set_xlabel('Source mouse, age in weeks and sex; no age pooling',fontsize=10);return im
 fig,axes=plt.subplots(1,2,figsize=(19,14));fig.subplots_adjust(left=.08,right=.97,top=.90,bottom=.20,wspace=.25)
 for mode,ax,title in zip(MODES,axes,['Single observed productive pair | primary','Complete productive-chain sets | sensitivity']):
  vals=[[lookup[mode,m,c]['concentration'] for m in MICE] for c in labels];texts=[['NA; n='+str(lookup[mode,m,c]['eligible_cells']) if lookup[mode,m,c]['concentration']=='NA' else 'n='+str(lookup[mode,m,c]['eligible_cells']) for m in MICE] for c in labels];im=panel(ax,vals,texts,title)
 fig.suptitle('A27 | Observed operational receptor-key concentration',x=.08,ha='left',fontsize=18)
 bar=fig.add_axes([.65,.12,.27,.018]);fig.colorbar(im,cax=bar,orientation='horizontal',label='Same-key fraction of observed distinct cell pairs [0,1]')
 fig.text(.08,.115,'Every tile shows eligible-cell N. Grey NA means N < 2, not zero concentration.\nA small-N extreme is a coarse observation, not a confident biological lead.',fontsize=10)
 fig.text(.08,.045,'Codes are nominal source annotations; receptor-independent construction is unestablished. No age effect or biological redistribution is inferred.\nConventions use different eligible populations; differences combine inclusion, matching and chain-observation effects. Shared strict-cell partitions agree.',fontsize=10)
 fig.savefig(output/'concentration_by_source_code.png',dpi=180,facecolor='white');plt.close(fig)
 fig,axes=plt.subplots(1,3,figsize=(25,14));fig.subplots_adjust(left=.06,right=.97,top=.90,bottom=.20,wspace=.25)
 choices=[('RNA representation: code / all RNA CD8','gex_cells','mouse_gex_CD8_total'),('Primary eligibility: single pair / code RNA','single_pair_eligible','gex_cells'),('Sensitivity eligibility: complete set / code RNA','complete_set_eligible','gex_cells')]
 for ax,(title,num,den) in zip(axes,choices):
  vals=[[fraction(sl[m,c][num],sl[m,c][den]) for m in MICE] for c in labels];texts=[[str(sl[m,c][num])+'/'+str(sl[m,c][den]) for m in MICE] for c in labels];im=panel(ax,vals,texts,title)
 fig.suptitle('A27 | RNA representation and receptor eligibility denominators',x=.06,ha='left',fontsize=18)
 bar=fig.add_axes([.70,.12,.23,.018]);fig.colorbar(im,cax=bar,orientation='horizontal',label='Observed source fraction [0,1]')
 fig.text(.06,.11,'Tile text is numerator / denominator. RNA includes labelled GEX-only cells. Grey NA means zero code-RNA denominator.\nReceptor representation and overlapping missing/productivity/ambiguity flags are retained in the support tables.',fontsize=10)
 fig.text(.06,.045,'Receptor-only cells remain outside RNA-state denominators; unlabelled GEX cells are not assigned to CD8.\nProcessed-table representation is not assembly success, technical capture efficiency or population prevalence.',fontsize=10)
 fig.savefig(output/'representation_and_eligibility.png',dpi=180,facecolor='white');plt.close(fig)
def self_test():
 for keys,expected in [([],None),(['x'],None),(['x','y'],0),(['x','x','y'],1/3),(['x','x','x'],1)]:
  x,_=concentration(keys);require(x['concentration']=='NA' if expected is None else math.isclose(x['concentration'],expected),'known concentration')
 def rec():
  r={p+s:'' for p in ['alpha','alpha2','beta','beta2'] for s in ['.functionality','.junction.nt','.vgene','.jgene']}
  for p,nt,v,j in [('alpha','AAA','TRAV1|TRAV2','TRAJ1'),('beta','CCC','TRBV1','TRBJ1')]:r.update({p+'.functionality':'productive',p+'.junction.nt':nt,p+'.vgene':v,p+'.jgene':j})
  return r
 r=rec();f,n,k=qualify(r);require(f['single_pair_eligible']==f['complete_set_eligible']==1,'strict subset');require(key_id('m1',k)!=key_id('m2',k),'cross-mouse separation')
 rr=rec();rr['alpha.vgene']='TRAV2|TRAV1|TRAV1';require(qualify(rr)[2]==k,'canonical ambiguous call set')
 rr=rec()
 for suffix in ['.functionality','.junction.nt','.vgene','.jgene']:rr['alpha2'+suffix]=rr['alpha'+suffix]
 ff,nn,kk=qualify(rr);require(not ff['single_pair_eligible'] and ff['complete_set_eligible'] and ff['duplicate_productive_slot_record'] and kk==k,'duplicate slot set rule')
 rr['alpha2.junction.nt']='GGG';require(len(qualify(rr)[2][0])==2,'distinct dual-chain retention')
 for field,value in [('alpha.junction.nt',''),('alpha.junction.nt','AAN'),('alpha2.functionality','nonstandard')]:
  rr=rec();rr[field]=value;ff,_,_=qualify(rr);require(not ff['single_pair_eligible'] and not ff['complete_set_eligible'],'incomplete/nonstandard exclusion')
 rr=rec();rr['alpha2.functionality']='unproductive';ff,_,kk=qualify(rr);require(ff['single_pair_eligible'] and ff['unproductive_present'] and kk==k,'nonproductive secondary')
 a,_=concentration(['x','y']);pool,_=concentration(['x','y','x','y']);require(a['concentration']==0 and math.isclose(pool['concentration'],1/3),'shared keys across codes; pooling not within-code average')
 shift=rec()
 for prefix in ['alpha','beta']:
  for suffix in ['.functionality','.junction.nt','.vgene','.jgene']:shift[prefix+'2'+suffix]=shift[prefix+suffix];shift[prefix+suffix]=''
 changed=rec();changed['alpha.junction.nt']='GGG'
 fixture=[rec(),shift,changed,rec()];primary=[];sensitivity=[]
 for rr in fixture:
  ff,_,kk=qualify(rr);require(ff['single_pair_eligible'] and ff['complete_set_eligible'],'strict inclusion');primary.append(key_id('m1',kk));sensitivity.append(key_id('m1',kk))
 require(primary[0]==primary[1]==primary[3] and primary[2]!=primary[0] and sorted(collections.Counter(sensitivity).values())==[1,3] and primary==sensitivity,'known strict subset partition')
 print('PASS: concentration/NA, cross-mouse and cross-code keys, ambiguous calls, duplicate/dual/incomplete/nonstandard slots and strict subset fixtures')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);parser.add_argument('--self-test',action='store_true');a=parser.parse_args()
 if a.self_test:self_test();return
 require(a.output is not None,'output required');out=a.output;out.mkdir(exist_ok=True,parents=True);require(not any((out/n).exists() for n in OUTPUTS),'refuse overwrite')
 source=ROOT/'raw_data/source_intake_20261104/A27/A27_IGT29_RECEPTOR_METADATA_V1.tsv';ex=json.loads((PRE/'A27_IGT29_EXTRACTION_V1.json').read_text());require(hashlib.sha256(source.read_bytes()).hexdigest()==ex['selected_sha256'],'raw subset hash');rs=read_tsv(source);receptors={r['IGT.cellID']:r for r in rs};require(len(receptors)==len(rs)==12743,'receptor identity')
 joined=read_tsv(PRE/'A27_IGT29_SOURCE_JOIN_V3.tsv');require(len(joined)==13332 and len({j['cell_id'] for j in joined})==13332,'unique union')
 expected={r['cell_id']:r for r in read_tsv(PRE/'A27_CELL_CHAIN_COVERAGE_V2.tsv')};require(set(expected)=={j['cell_id'] for j in joined},'coverage IDs')
 require(sorted({j['mouse'] for j in joined})==MICE,'nine exact mice');require(sorted({j['annotation_level2'] for j in joined if j['annotation_level1']=='CD8'})==CODES,'twenty exact source codes')
 metadata={};cells=[];checked=0
 for j in joined:
  mouse=j['mouse'];ident={k:j[k] for k in ['age_weeks','sex']}
  if mouse in metadata:require(metadata[mouse]==ident,'consistent mouse metadata')
  metadata[mouse]=ident;r=receptors.get(j['cell_id']);f,n,k=qualify(r)
  for flag in FLAGS:require(f[flag]==int(expected[j['cell_id']][flag]),'coverage flag '+flag);checked+=1
  require(n['alpha']==int(expected[j['cell_id']]['alpha_productive_slots']) and n['beta']==int(expected[j['cell_id']]['beta_productive_slots']),'slot parity')
  gex=j['join_disposition']!='receptor_only';cd8=gex and j['annotation_level1']=='CD8';primary=bool(cd8 and f['single_pair_eligible']);sensitivity=bool(cd8 and f['complete_set_eligible'])
  primary_key=key_id(mouse,k) if primary else '';sensitivity_key=key_id(mouse,k) if sensitivity else ''
  require(not primary or (sensitivity and primary_key==sensitivity_key),'strict subset partition parity')
  cell={k:j[k] for k in ['cell_id','mouse','age_weeks','sex','join_disposition','annotation_level1','annotation_level2']};cell.update({'gex_present':int(gex),'source_CD8':int(cd8),'primary_eligible':int(primary),'sensitivity_eligible':int(sensitivity),'primary_key':primary_key,'sensitivity_key':sensitivity_key});cell.update(f);cells.append(cell)
 support=[];conc=[];clone_rows=[]
 for m in MICE:
  all_cd8=[x for x in cells if x['mouse']==m and x['source_CD8']];total=len(all_cd8)
  for code in ['ALL_CD8']+CODES:
   selected=all_cd8 if code=='ALL_CD8' else [x for x in all_cd8 if x['annotation_level2']==code]
   sp={'mouse':m,**metadata[m],'source_code':code,'mouse_gex_CD8_total':total,'gex_cells':len(selected)};sp.update({flag:sum(x[flag] for x in selected) for flag in FLAGS});sp['RNA_fraction_of_mouse_CD8']=fraction(len(selected),total);sp['receptor_representation_fraction']=fraction(sp['receptor_present'],len(selected));sp['primary_eligible_fraction_of_GEX']=fraction(sp['single_pair_eligible'],len(selected));sp['sensitivity_eligible_fraction_of_GEX']=fraction(sp['complete_set_eligible'],len(selected));support.append(sp)
   for mode,key_col in zip(MODES,['primary_key','sensitivity_key']):
    keys=[x[key_col] for x in selected if x[key_col]];value,counts=concentration(keys);require(sum(counts.values())==len(keys),'clone-count reconstruction')
    row={'convention':mode,'scope':'lineage' if code=='ALL_CD8' else 'nominal_source_code','mouse':m,**metadata[m],'source_code':code,'mouse_gex_CD8_total':total,'gex_code_cells':len(selected),'receptor_record_cells':sp['receptor_present'],**value,'RNA_fraction_of_mouse_CD8':sp['RNA_fraction_of_mouse_CD8'],'receptor_representation_fraction':sp['receptor_representation_fraction'],'eligible_fraction_of_GEX':fraction(len(keys),len(selected)),'eligible_fraction_of_receptor_records':fraction(len(keys),sp['receptor_present'])};conc.append(row)
    for key,count in sorted(counts.items()):clone_rows.append({'convention':mode,'mouse':m,'source_code':code,'operational_key':key,'cell_count':count})
  for mode in MODES:
   local=[x for x in conc if x['mouse']==m and x['convention']==mode];pool=next(x for x in local if x['source_code']=='ALL_CD8');within=[x for x in local if x['source_code']!='ALL_CD8'];require(sum(x['eligible_cells'] for x in within)==pool['eligible_cells'],'state support partition');require(sum(x['same_key_pairs'] for x in within)<=pool['same_key_pairs'],'cross-code pair accounting')
 disposition=[]
 for m in MICE:
  subset=[x for x in cells if x['mouse']==m];disposition.append({'mouse':m,**metadata[m],'gex_cells_all_lineages':sum(x['gex_present'] for x in subset),'GEX_only_cells_all_lineages':sum(x['join_disposition']=='GEX_only' for x in subset),'receptor_only_unannotated_all_lineages':sum(x['join_disposition']=='receptor_only' for x in subset),'gex_separate_annotation_missing':sum(x['gex_present'] and not x['annotation_level1'] for x in subset),'source_labelled_CD8_GEX':sum(x['source_CD8'] for x in subset)})
 require(len(conc)==378 and len(support)==189 and len(disposition)==9,'complete output grid')
 schema=json.loads((PRE/'A27_OUTPUT_SCHEMA_V1.json').read_text());require(schema['expected_outputs']==OUTPUTS,'output paths')
 for name,rows in zip(OUTPUTS[:5],[cells,clone_rows,conc,support,disposition]):
  require(list(rows[0])==schema['tsv_columns'][name],'output columns '+name)
  if name in schema['fixed_rows']:require(len(rows)==schema['fixed_rows'][name],'output rows '+name)
  write_tsv(out/name,rows)
 draw(conc,support,metadata,out)
 summary={'analysis_id':'A27.source_code_concentration_v1','mice':MICE,'source_codes':CODES,'union_rows':len(cells),'source_CD8_GEX':sum(x['source_CD8'] for x in cells),'primary_cells':sum(x['primary_eligible'] for x in cells),'sensitivity_cells':sum(x['sensitivity_eligible'] for x in cells),'concentration_rows':len(conc),'support_rows':len(support),'source_flag_scalar_checks':checked,'strict_subset_partition_parity':True,'source_code_computable_strata':{mode:sum(x['convention']==mode and x['scope']=='nominal_source_code' and x['eligible_cells']>=2 for x in conc) for mode in MODES},'scope':'Finite captured-cell operational-key description conditioned on nominal source codes; no receptor-independent state construction, biological redistribution or age effect established; conventions differ in eligible population and chain observation.'}
 (out/'summary.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode());print(json.dumps({k:summary[k] for k in ['source_CD8_GEX','primary_cells','sensitivity_cells','concentration_rows','strict_subset_partition_parity']}))
if __name__=='__main__':main()
