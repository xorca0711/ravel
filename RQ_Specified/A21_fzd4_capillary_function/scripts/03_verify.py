"""Independent A21 source arithmetic, units, provenance and preservation verification."""
from pathlib import Path
import csv,gzip,hashlib,json,math,statistics
import h5py
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];n=0
def check(v,message):
 global n
 if not v:raise AssertionError(message)
 n+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(name):
 with (BASE/'tables'/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def close(a,b):return math.isclose(float(a),float(b),rel_tol=1e-9,abs_tol=1e-9)
def rho(x,y):
 def ranks(v):
  a=sorted(enumerate(v),key=lambda z:z[1]);out=[0.]*len(v)
  for i,value in enumerate(v):out[i]=statistics.mean(j+1 for j,(_,q) in enumerate(a) if q==value)
  return out
 a=ranks(x);b=ranks(y);am=statistics.mean(a);bm=statistics.mean(b)
 return sum((u-am)*(v-bm) for u,v in zip(a,b))/math.sqrt(sum((u-am)**2 for u in a)*sum((v-bm)**2 for v in b))
cfg=json.loads((BASE/'config/exploratory_v1.json').read_text());run=json.loads((BASE/'reports/analysis_complete.json').read_text())
check(sha(BASE/'config/exploratory_v1.json')==run['config_sha256'],'frozen specification')
records=json.loads((BASE/'metadata/intake.json').read_text());primary={'GSE211335_RAW.tar','godoy_samples.txt.gz','godoy_endothelial_metadata.csv.gz'}
for r in records:
 p=BASE/'cache'/r['file']
 if r['status']=='retrieved' and (r['file'] in primary or p.exists()):check(sha(p)==r['sha256'],'input hash '+r['file'])
with gzip.open(BASE/'cache/selected_cells.tsv.gz','rt',newline='') as f:cells=list(csv.DictReader(f,delimiter='\t'))
with gzip.open(BASE/'cache/godoy_endothelial_metadata.csv.gz','rt',newline='') as f:source={r['']:r for r in csv.DictReader(f)}
check(len(cells)==len(source)==5423,'source cell count');check(len({r['cell'] for r in cells})==5423,'unique cells')
samples={int(r['animal']):r for r in table('samples.tsv')};check(len(samples)==12,'animals, not technical partitions')
for day in cfg['days']:check(sum(int(r['day'])==day for r in samples.values())==3,'three animals per condition')
genes=sum(cfg['genes'].values(),[]);gm={(r['pool'],r['gene']):int(r['feature_index']) for r in table('gene_mapping.tsv')}
for rec in json.loads((BASE/'metadata/matrix_manifest.json').read_text()):
 path=BASE/'cache'/rec['file'];check(sha(path)==rec['sha256'],'matrix hash')
 with h5py.File(path,'r') as f:
  m=f['matrix'];pool='Pool'+rec['file'].split('pool_')[1][0]
  bc={v.decode().removesuffix('-1'):i for i,v in enumerate(m['barcodes'][:])};ptr=m['indptr'][:];data=m['data'][:];ids=m['indices'][:]
  for row in cells:
   if row['orig.ident']!=pool:continue
   j=bc[row['cell'].split('_',1)[1]];lo,hi=int(ptr[j]),int(ptr[j+1]);raw=dict(zip(map(int,ids[lo:hi]),map(int,data[lo:hi])))
   check(sum(raw.values())==int(row['total_umi']),'all-gene UMI')
   for g in genes:check(raw.get(gm[(pool,g)],0)==int(row[g]),'raw target count')
agg={}
for row in cells:
 animal=int(row['animal']);day=int(row['day']);cl=int(row['seurat_clusters']);src=source[row['cell']]
 check(int(src['Annotation'].removeprefix('Bar'))==animal and int(samples[animal]['day'])==day,'animal assignment')
 check(int(src['seurat_clusters'])==cl and src['Doublet']=='FALSE','author state and doublet flag')
 coarse=next(g for g,ks in cfg['coarse_groups'].items() if cl in ks)
 for kind,state in [('cluster',cfg['clusters'][str(cl)]),('coarse',coarse)]:
  a=agg.setdefault((kind,animal,day,state),dict(cells=0,umi=0,author=0,counts={g:0 for g in genes},detected={g:0 for g in genes}))
  a['cells']+=1;a['umi']+=int(row['total_umi']);a['author']+=int(float(src['nCount_RNA']))
  for g in genes:a['counts'][g]+=int(row[g]);a['detected'][g]+=int(int(row[g])>0)
values={};alternates={}
for row in table('unit_expression.tsv'):
 key=(row['kind'],int(row['animal']),int(row['day']),row['state']);a=agg[key];g=row['gene'];ct=a['counts'][g];value=math.log2(ct/a['umi']*1e6+1);alt=math.log2(ct/a['author']*1e6+1)
 for field,expected in [('counts',ct),('cells',a['cells']),('total_umi',a['umi']),('author_denominator',a['author']),('detected_cells',a['detected'][g])]:check(int(row[field])==expected,field)
 check(close(row['cpm'],ct/a['umi']*1e6) and close(row['log2cpm'],value),'normalized value')
 check(close(row['detection'],a['detected'][g]/a['cells']) and close(row['author_denominator_log2cpm'],alt),'detection/sensitivity')
 values[key+(g,)]=value;alternates[key+(g,)]=alt
for key in agg:
 for panel,gs in cfg['panels'].items():
  values[key+(panel,)]=statistics.mean(values[key+(g,)] for g in gs);alternates[key+(panel,)]=statistics.mean(alternates[key+(g,)] for g in gs)
for row in table('unit_features.tsv'):
 key=(row['kind'],int(row['animal']),int(row['day']),row['state'],row['feature']);check(close(row['value'],values[key]),'feature/panel')
summaries={};alts={}
for row in table('paired_differences.tsv'):
 base=(row['kind'],int(row['animal']),int(row['day']));left=base+(row['state_left'],row['feature']);right=base+(row['state_right'],row['feature'])
 check(agg[left[:4]]['cells']>=int(row['cell_floor']) and agg[right[:4]]['cells']>=int(row['cell_floor']),'pair eligibility')
 delta=values[left]-values[right];check(close(row['delta'],delta),'paired delta')
 k=(row['contrast'],row['cell_floor'],row['day'],row['feature']);summaries.setdefault(k,[]).append(delta);alts.setdefault(k,[]).append(alternates[left]-alternates[right])
for row in table('contrast_summary.tsv'):
 k=(row['contrast'],row['cell_floor'],row['day'],row['feature']);v=summaries[k]
 check(int(row['n'])==len(v),'summary units')
 for field,fun in [('mean',statistics.mean),('median',statistics.median),('minimum',min),('maximum',max)]:check(close(row[field],fun(v)),field)
 check(int(row['positive'])==sum(x>0 for x in v) and int(row['negative'])==sum(x<0 for x in v),'signs')
for row in table('normalization_sensitivity.tsv'):
 k=(row['contrast'],row['cell_floor'],row['day'],row['feature']);v=statistics.mean(summaries[k]);w=statistics.mean(alts[k])
 check(close(row['primary_mean'],v) and close(row['author_denominator_mean'],w),'sensitivity means')
 check(row['same_direction']==str((v>0)-(v<0)==(w>0)-(w<0)),'sensitivity direction')
points=table('association_inputs.tsv')
for row in table('within_day_associations.tsv'):
 q=[p for p in points if all(p[k]==row[k] for k in ['state','day','cell_floor'])];check(len(q)==int(row['animals']),'association units')
 if row['rho']:check(len(q)>=3 and close(row['rho'],rho([float(p['cpm']) for p in q],[float(p['cycling']) for p in q])),'independent rank coefficient')
 else:check(len(q)<3 or len({p['cpm'] for p in q})<2 or len({p['cycling'] for p in q})<2,'unavailable correlation')
for row in table('eligibility.tsv'):
 states={'gCap_minus_aCap':('coarse','gCap','aCap'),'transitional1_minus_gCap0':('cluster','gCap_transitional_1','gCap_0'),'cycling7_minus_gCap0':('cluster','gCap_cycling_7','gCap_0')}
 kind,left,right=states[row['contrast']];day=int(row['day']);floor=int(row['cell_floor'])
 leftset={k[1] for k,v in agg.items() if k[0]==kind and k[2]==day and k[3]==left and v['cells']>=floor}
 rightset={k[1] for k,v in agg.items() if k[0]==kind and k[2]==day and k[3]==right and v['cells']>=floor}
 check(int(row['paired_animals'])==len(leftset&rightset),'complete eligible pairs')
for r in json.loads((BASE/'metadata/reused_inputs.json').read_text()):check(sha(ROOT/r['file'])==r['sha256'],'prior source unchanged')
previous=json.loads((BASE/'metadata/prior_evidence_hashes.json').read_text())
for path,h in previous.items():check(sha(BASE.parent/path)==h,'prior A19/A20 preserved')
figs=json.loads((BASE/'reports/figure_manifest.json').read_text());check(len(figs)==9,'nine exports')
for r in figs:check(sha(BASE/r['file'])==r['sha256'],'figure hash')
readme_hash=json.loads((BASE.parent/'A20_fibroblast_fzd_context/metadata/history/scope_refinement_v1/preservation_contract.json').read_text())['root_readme_sha256']
check(sha(ROOT/'README.md')==readme_hash,'universal README unchanged')
report=dict(checks_passed=n,animals=12,cells=5423,independent_source_reconciled=True,prior_A19_A20_files_unchanged=len(previous),figure_exports=9,root_readme_unchanged=True,scope='Arithmetic and provenance; no Fzd4 functional validation')
(BASE/'reports/verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
