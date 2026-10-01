"""Verify A23 archived outputs and independent arithmetic; optionally inspect source bytes."""
import argparse,collections,csv,hashlib,importlib.util,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
RQ=ROOT/'RQ_Specified/A23_slc34a2_transition_homeostasis';RUN='external_pilot_v2';T=RQ/'tables'/RUN

def rows(name):
 with (T/(name+'.tsv')).open(encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def near(a,b):
 if not math.isclose(float(a),float(b),rel_tol=1e-9,abs_tol=1e-10):raise AssertionError((a,b))
def verify(with_raw=False):
 record=json.loads((RQ/'metadata'/RUN/'run_record.json').read_text())
 for r in record['inputs']+record['outputs']:
  if r['path'].startswith('raw_data/') and not with_raw:continue
  assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
 for name in ['figure_record.json','figure_correction_v2.json','review_record.json']:
  for r in json.loads((RQ/'metadata'/RUN/name).read_text())['outputs']:
   assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
 sensitivity=RQ/'metadata/published_cell_audit_v1'
 for name in ['run_record.json','figure_record.json']:
  rec=json.loads((sensitivity/name).read_text())
  for item in rec.get('inputs',[])+rec['outputs']:
   if item['path'].startswith('raw_data/') and not with_raw:continue
   assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
 st=RQ/'tables/published_cell_audit_v1'
 def sensitivity_rows(name):
  with (st/(name+'.tsv')).open(encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
 for item in sensitivity_rows('coverage'):
  assert int(item['published_cells'])==int(item['matched_raw']) and int(item['missing_raw'])==0
 sm=sensitivity_rows('marker_summaries')
 for item in sensitivity_rows('marker_differences'):
  a=next(x for x in sm if (x['library'],x['group'],x['gene'])==('GSM5970468',item['group'],item['gene']))
  b=next(x for x in sm if (x['library'],x['group'],x['gene'])==('GSM5970470',item['group'],item['gene']))
  near(item['mean_log1p_difference'],float(a['mean_log1p_10k'])-float(b['mean_log1p_10k']))
 cells=rows('cell_selection');coverage=rows('coverage');markers=rows('marker_summaries')
 for c in coverage:
  subset=[r for r in cells if (r['library'],r['qc'])==(c['library'],c['qc'])]
  assert len(subset)==int(c['filtered_cells'])
  assert len({r['barcode'] for r in subset})==len(subset)
  for field,key in [('qc_pass','qc_cells'),('epithelial_candidate','epithelial_candidate'),('AT2_candidate','AT2_candidate')]:assert sum(r[field]=='True' for r in subset)==int(c[key])
  for r in subset:
   if r['AT2_candidate']=='True':assert r['epithelial_candidate']=='True'
   if r['epithelial_candidate']=='True':assert r['qc_pass']=='True' and r['epi_features_pass']=='True' and r['colineage_flag']=='False'
 for r in markers:
  if r['available']=='True':near(r['fraction_detected'],int(r['n_detected'])/int(r['n']))
 for r in rows('marker_differences'):
  if r['coverage_pass']!='True':continue
  a=next(x for x in markers if (x['library'],x['qc'],x['group'],x['gene'])==('GSM5970468',r['qc'],r['group'],r['gene']))
  b=next(x for x in markers if (x['library'],x['qc'],x['group'],x['gene'])==('GSM5970470',r['qc'],r['group'],r['gene']))
  near(r['mean_log1p_difference'],float(a['mean_log1p_10k'])-float(b['mean_log1p_10k']))
 for r in rows('stone_pairs'):near(r['D56_D0_ratio'],float(r['D56_g'])/float(r['D0_g']))
 vals=rows('biochemical_values')
 for s in rows('biochemical_summary'):
  vv=[float(r['value']) for r in vals if all(r[k]==s[k] for k in ['sheet','genotype','diet'])]
  assert len(vv)==int(s['n']);near(s['mean'],sum(vv)/len(vv))
 for r in rows('annotation_coverage'):
  assert int(r['matched'])+int(r['published_not_filtered'])==int(r['published_barcodes'])
  assert int(r['matched'])+int(r['filtered_not_published'])==int(r['filtered_barcodes'])
 if with_raw:
  import h5py,openpyxl,numpy as np
  from scipy.sparse import csc_matrix
  for lib in ['GSM5970468','GSM5970470']:
   with h5py.File(ROOT/f'raw_data/GSE199329/{lib}_filtered_gene_bc_matrices_h5.h5','r') as f:
    g=f['hg19'];names=[v.decode() for v in g['gene_names'][:]];barcodes=[v.decode() for v in g['barcodes'][:]]
    matrix=csc_matrix((g['data'][:],g['indices'][:],g['indptr'][:]),shape=tuple(g['shape'][:]))
   selected={r['barcode'] for r in cells if r['library']==lib and r['qc']=='primary' and r['AT2_candidate']=='True'}
   jj=[j for j,b in enumerate(barcodes) if b in selected]
   # Direct Python accumulation of each cell's normalized value, separate from the vectorized generator.
   for gene in ['KRT8','SPRR1A','CLU','SLC34A2']:
    i=names.index(gene);terms=[];det=0
    for j in jj:
     col=matrix.getcol(j);v=float(col[i,0]);den=float(col.sum());terms.append(math.log1p(10000*v/den));det+=v>0
    saved=next(r for r in markers if (r['library'],r['qc'],r['group'],r['gene'])==(lib,'primary','AT2_candidate',gene))
    near(saved['mean_log1p_10k'],sum(terms)/len(terms));assert det==int(saved['n_detected'])
  book=openpyxl.load_workbook(ROOT/'raw_data/GSE199329/41467_2023_36810_MOESM9_ESM.xlsx',read_only=True,data_only=True)
  assert len(book.sheetnames)==len(rows('workbook_inventory'))
  for r in vals:near(r['value'],book[r['sheet']][r['coordinate']].value)
  for r in rows('stone_pairs'):
   near(r['D0_g'],book[r['sheet']].cell(int(r['source_row']),2).value);near(r['D56_g'],book[r['sheet']].cell(int(r['source_row']),3).value)
  book.close()
 print('A23 verification PASS: source/output hashes, selection counts, barcode coverage, marker/assay arithmetic'+('; independent raw-count and workbook-coordinate checks' if with_raw else ''))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--with-raw',action='store_true');verify(p.parse_args().with_raw)
