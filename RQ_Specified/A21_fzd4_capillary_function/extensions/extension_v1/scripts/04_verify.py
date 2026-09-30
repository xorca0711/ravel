"""Independent raw-matrix, worksheet-cell, summary and preservation checks."""
from pathlib import Path
import datetime,hashlib,io,json,math,re,statistics,zipfile,xml.etree.ElementTree as ET
import h5py,numpy as np,pandas as pd
from scipy.sparse import csc_matrix
BASE=Path(__file__).resolve().parents[1];PARENT=BASE.parents[1];ROOT=PARENT.parents[1]
checks=0
def check(ok,message):
 global checks
 checks+=1
 if not ok:raise AssertionError(message)
def close(a,b,message):check(math.isclose(float(a),float(b),rel_tol=1e-9,abs_tol=1e-8),message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(name):return pd.read_csv(BASE/'tables'/name,sep='\t')
def main():
 cfg=json.loads((BASE/'config/exploratory_v1.json').read_text());genes=cfg['genes'];run=json.loads((BASE/'reports/family_complete.json').read_text());src=json.loads((BASE/'reports/source_complete.json').read_text())
 check(sha(BASE/'config/exploratory_v1.json')==run['config_sha256']==src['config_sha256'],'frozen config')
 check(sha(BASE/'config/source_mapping.json')==src['source_mapping_sha256'],'source map')
 check(sha(BASE/'config/perfusion_comparator.json')==src['comparator_sha256'],'comparator')
 meta=pd.read_csv(PARENT/'cache/godoy_endothelial_metadata.csv.gz',index_col=0);meta['animal']=meta.Annotation.str.extract(r'Bar(\d+)',expand=False).astype(int)
 sample=pd.read_csv(PARENT/'tables/samples.tsv',sep='\t').set_index('animal');meta['day']=meta.animal.map(sample.day)
 check(len(meta)==5423 and meta.animal.nunique()==12 and not meta.Doublet.any(),'sample identity')
 # Independent vectorized sparse-matrix reconstruction, instead of analyzer cell loops.
 X=np.zeros((len(meta),len(genes)),dtype=np.int64);tot=np.zeros(len(meta),dtype=np.int64);seen=np.zeros(len(meta),bool)
 for rec in json.loads((PARENT/'metadata/matrix_manifest.json').read_text()):
  p=PARENT/'cache'/rec['file'];check(sha(p)==rec['sha256'],'raw hash')
  pool='Pool'+p.name.split('pool_')[1][0]
  with h5py.File(p,'r') as f:
   m=f['matrix'];mat=csc_matrix((m['data'][:],m['indices'][:],m['indptr'][:]),shape=tuple(m['shape'][:]))
   names=np.array([v.decode() for v in m['features/name'][:]]);hits=[np.flatnonzero(names==gene) for gene in genes];check(all(len(x)==1 for x in hits),'unique target-gene mapping');indices=np.array([x[0] for x in hits])
   barcodes=pd.Index([pool+'_'+v.decode().removesuffix('-1') for v in m['barcodes'][:]])
   ii=np.flatnonzero(meta['orig.ident'].eq(pool));jj=barcodes.get_indexer(meta.index[ii]);check((jj>=0).all(),'cell mapping')
   X[ii]=mat[indices,:][:,jj].T.toarray();tot[ii]=np.asarray(mat[:,jj].sum(axis=0)).ravel();seen[ii]=True
 check(seen.all(),'all cells extracted')
 expr=load('unit_expression.tsv');recomputed={}
 for kind in ['cluster','coarse']:
  cross={int(k):v for k,v in cfg['clusters'].items()} if kind=='cluster' else {k:g for g,ks in cfg['coarse_groups'].items() for k in ks}
  group=meta.assign(state=meta.seurat_clusters.map(cross),i=np.arange(len(meta)))
  for (animal,day,state),df in group.groupby(['animal','day','state']):
   ii=df.i.to_numpy();counts=X[ii].sum(axis=0);det=(X[ii]>0).sum(axis=0);den=tot[ii].sum();author=df.nCount_RNA.sum()
   for j,gene in enumerate(genes):recomputed[(kind,animal,day,state,gene)]=(len(ii),int(den),int(counts[j]),int(det[j]),float(np.log2(counts[j]/den*1e6+1)),float(np.log2(counts[j]/author*1e6+1)))
 check(len(expr)==len(recomputed)==5184,'all expression rows')
 for row in expr.itertuples():
  r=recomputed[(row.kind,row.animal,row.day,row.state,row.gene)]
  for got,expected in zip([row.cells,row.total_umi,row.counts,row.detected_cells,row.log2cpm,row.author_log2cpm],r):close(got,expected,'raw expression')
  close(row.cpm,row.counts/row.total_umi*1e6,'CPM');close(row.detection,row.detected_cells/row.cells,'detection')
 pairs=load('paired_differences.tsv');con={c['id']:c for c in cfg['contrasts']};expected_keys=set()
 for floor in cfg['floors']:
  for c in cfg['contrasts']:
   for animal in sample.index:
    day=int(sample.loc[animal,'day'])
    for gene in genes:
     kl=(c['kind'],animal,day,c['left'],gene);kr=(c['kind'],animal,day,c['right'],gene)
     if kl in recomputed and kr in recomputed and min(recomputed[kl][0],recomputed[kr][0])>=floor:expected_keys.add((c['id'],floor,day,animal,gene))
 check(set(zip(pairs.contrast,pairs.cell_floor,pairs.day,pairs.animal,pairs.gene))==expected_keys,'pair eligibility complete')
 for row in pairs.itertuples():
  c=con[row.contrast];l=recomputed[(c['kind'],row.animal,row.day,c['left'],row.gene)];r=recomputed[(c['kind'],row.animal,row.day,c['right'],row.gene)]
  close(row.delta,l[4]-r[4],'pair difference');close(row.author_delta,l[5]-r[5],'sensitivity difference');close(row.detected_cells_left,l[3],'left detection')
 sm=load('contrast_summary.tsv');keys=['contrast','cell_floor','day','gene'];indexed=sm.set_index(keys)
 for key,z in pairs.groupby(keys):
  r=indexed.loc[key];values=z.delta.to_list();av=z.author_delta.to_list()
  for got,expected in [(r.n,len(values)),(r['mean'],statistics.mean(values)),(r['median'],statistics.median(values)),(r.minimum,min(values)),(r.maximum,max(values)),(r.positive,sum(v>0 for v in values)),(r.negative,sum(v<0 for v in values)),(r.detected_left,z.detected_cells_left.sum()),(r.author_mean,statistics.mean(av))]:close(got,expected,'contrast summary')
  check(bool(r.same_denominator_direction)==(np.sign(statistics.mean(values))==np.sign(statistics.mean(av))),'sensitivity sign')
 cand=load('candidate_summary.tsv')
 for row in cand.itertuples():
  counts={}
  for floor in cfg['floors']:
   passed=0
   for day in [3,5,7]:
    z=pairs[pairs.contrast.eq('transitional1_minus_gCap0')&pairs.cell_floor.eq(floor)&pairs.day.eq(day)&pairs.gene.eq(row.gene)]
    if len(z)>=2 and statistics.mean(z.delta)>0 and (z.delta>0).sum()>=math.ceil(2*len(z)/3) and z.detected_cells_left.sum()>=5:passed+=1
   counts[floor]=passed;check(getattr(row,'injury_days_floor'+str(floor))==passed,'candidate days')
  check(bool(row.rna_nominee)==(counts[20]>=2 and counts[10]>=2),'candidate nomination')
 # Independent worksheet XML extraction of only the exact recorded data cells.
 ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};source=load('source_observations.tsv')
 for rec in json.loads((BASE/'metadata/workbook_manifest.json').read_text()):
  ap=BASE/'cache'/rec['archive'];check(sha(ap)==rec['archive_sha256'],'source archive')
  with zipfile.ZipFile(ap) as outer:blob=outer.read(rec['member'])
  check(hashlib.sha256(blob).hexdigest()==rec['sha256'],'workbook bytes')
  with zipfile.ZipFile(io.BytesIO(blob)) as z:
   tree=ET.fromstring(z.read('xl/worksheets/sheet1.xml'));cells={c.get('r'):c for c in tree.findall('.//m:c',ns)}
   strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
   for row in source[source.member.eq(rec['member'])].itertuples():
    c=cells[row.cell];check(c.get('t') is None and c.find('m:f',ns) is None,'raw numeric data cell');close(row.value,float(c.find('m:v',ns).text),'exact source observation')
    header=cells[row.source_column+'2'];check(strings[int(header.find('m:v',ns).text)]==row.source_group,'source group')
 for row in load('source_contrasts.tsv').itertuples():
  d=source[source.panel.eq(row.panel)];l=d[d.source_group.eq(row.left_group)].value.to_list();r=d[d.source_group.eq(row.right_group)].value.to_list()
  for got,expected in [(row.n_left,len(l)),(row.n_right,len(r)),(row.mean_left,statistics.mean(l)),(row.mean_right,statistics.mean(r)),(row.mean_difference,statistics.mean(l)-statistics.mean(r)),(row.median_left,statistics.median(l)),(row.median_right,statistics.median(r))]:close(got,expected,'source contrast')
 check(len(source)==88 and not src['cross_endpoint_join'],'source scope')
 prior=json.loads((BASE/'metadata/prior_hashes.json').read_text());changed=[];unchanged=0
 allowed={'README.md','PLAN.md','RESULTS.md','FIGURES.md','SOURCES.md','config/question_contract.json','reports/package_manifest.json'}
 for name,h in prior.items():
  p=ROOT/name
  if sha(p)==h:unchanged+=1;check(True,'prior unchanged');continue
  if PARENT not in p.parents:
   parts=p.relative_to(ROOT).parts;check(parts[0]=='RQ_Specified' and parts[1] in ['A19_fzd_response_reversibility','A20_fibroblast_fzd_context'],'authorized question folder')
   owner=ROOT/parts[0]/parts[1];rel=p.relative_to(owner).as_posix();check(rel in {'README.md','PLAN.md','NARROWED_HYPOTHESIS.md','config/question_contract.json','reports/package_manifest.json'},'wording-only prior document')
   revision=owner/'metadata/history/one_line_refinement_20260930/revision.json';ledger=json.loads(revision.read_text());entry=next(x for x in ledger['snapshots'] if x['file']==rel)
   check(entry['sha256']==h and sha(owner/entry['snapshot'])==h,'pre-wording prior bytes archived');changed.append(name);continue
  rel=p.relative_to(PARENT).as_posix();check(rel in allowed,'allowed parent document')
  backup=BASE/'metadata/history'/(rel.replace('/','_')+('.txt' if rel.endswith('.md') else ''));check(backup.exists() and sha(backup)==h,'original parent bytes archived');changed.append(name)
 check(sha(ROOT/'README.md')==(BASE/'metadata/root_readme_sha256.txt').read_text().strip(),'universal README unchanged')
 figures=json.loads((BASE/'reports/figure_manifest.json').read_text());check(len(figures)==9,'nine exports')
 for f in figures:check(sha(BASE/f['file'])==f['sha256'],'figure hash')
 rec=dict(finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='passed',checks=checks,cells=len(meta),genes=len(genes),source_observations=len(source),prior_files_checked=len(prior),prior_files_unchanged=unchanged,prior_documents_archived=changed,root_readme_unchanged=True,figure_exports=9,limitations='Source rows are reported biological replicates with anonymous identities; functional lineage and independent state validation remain untested.')
 (BASE/'reports/verification.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps({k:v for k,v in rec.items() if k!='prior_documents_archived'}))
if __name__=='__main__':main()
