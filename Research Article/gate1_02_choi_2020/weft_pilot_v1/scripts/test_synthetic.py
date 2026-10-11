"""Targeted synthetic-only strict loader, frozen QC and denominator invariants."""
import unittest,tempfile,pathlib,json,gzip,hashlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import numpy as np,pandas as pd,scipy.sparse as sp
from unittest.mock import patch
from sparse_input import load_triplet
import common
from common import counts_and_fractions,BoundsRecorder,require_reviewed_job
import frozen_methods as fm
class LoaderTests(unittest.TestCase):
 def fixture(self,root,matrix='1 1 2\n2 2 3\n',barcodes='BC1\nBC2\n',features='ENSG1\tg1\nENSG2\tg2\n',dims='2 2 2',header='%%MatrixMarket matrix coordinate integer general',uncompressed=True):
  files=[]
  for name,body,kind in [('S_test.mtx.gz',header+'\n'+dims+'\n'+matrix,'matrix'),('S_test_gene.tsv.gz',features,'features'),('S_test_barcodes.tsv.gz',barcodes,'barcodes')]:
   p=root/name;p.write_bytes(gzip.compress(body.encode(),mtime=0));d={'filename':name,'path':name,'gsm':'S','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
   if kind=='matrix':d.update(rows=2,columns=2,stored_entries=2)
   else:
    d['lines']=2
    if uncompressed:d['uncompressed_sha256']=hashlib.sha256(body.encode()).hexdigest()
   files.append(d)
  return files
 def test_valid_orientation_and_prefix(self):
  with tempfile.TemporaryDirectory() as t:
   r=pathlib.Path(t);X,var,bc,a=load_triplet(r,self.fixture(r),'S');self.assertTrue(sp.isspmatrix_csr(X));self.assertEqual(X[0,0],2);self.assertEqual(X[1,1],3);self.assertEqual(bc.tolist(),['S::BC1','S::BC2']);self.assertEqual(a['duplicates'],0)
 def test_reject_unsafe_records(self):
  for matrix in ['1 1 2\n1 1 3\n','0 1 2\n2 2 3\n','1 3 2\n2 2 3\n','1 1 0\n2 2 3\n','1 1 2.5\n2 2 3\n','1 1 -2\n2 2 3\n','1 1 2\n','1 1 2\n2 2 3\n2 1 4\n']:
   with self.subTest(matrix=matrix),tempfile.TemporaryDirectory() as t:
    r=pathlib.Path(t)
    with self.assertRaises(ValueError):load_triplet(r,self.fixture(r,matrix=matrix),'S')
 def test_reject_dimensions_and_header(self):
  for options in [{'dims':'2 3 2'},{'header':'%%MatrixMarket matrix coordinate real general'}]:
   with tempfile.TemporaryDirectory() as t:
    r=pathlib.Path(t)
    with self.assertRaises(ValueError):load_triplet(r,self.fixture(r,**options),'S')
 def test_reject_duplicate_labels_lengths_and_order(self):
  for opts in [{'barcodes':'BC1\nBC1\n'},{'features':'ENSG1\tg1\nENSG1\tg2\n'},{'barcodes':'BC1\n'},{'features':'ENSG1\tg1\n'}]:
   with tempfile.TemporaryDirectory() as t:
    r=pathlib.Path(t)
    with self.assertRaises(ValueError):load_triplet(r,self.fixture(r,**opts),'S')
  with tempfile.TemporaryDirectory() as t:
   r=pathlib.Path(t);f=self.fixture(r);p=r/'S_test_barcodes.tsv.gz';p.write_bytes(gzip.compress(b'BC2\nBC1\n',mtime=0));d=next(x for x in f if x['filename']==p.name);d.update(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
   with self.assertRaisesRegex(ValueError,'order'):load_triplet(r,f,'S')
 def test_reject_compressed_hash_and_crc(self):
  with tempfile.TemporaryDirectory() as t:
   r=pathlib.Path(t);f=self.fixture(r);p=r/'S_test_gene.tsv.gz';v=p.read_bytes();p.write_bytes(v[:-1]+bytes([v[-1]^1]))
   with self.assertRaises(ValueError):load_triplet(r,f,'S')
   d=next(x for x in f if x['filename']==p.name);d['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
   with self.assertRaises((gzip.BadGzipFile,EOFError)):load_triplet(r,f,'S')
class MethodTests(unittest.TestCase):
 def test_frozen_qc_denominators(self):
  X=sp.csr_matrix(np.full((40,601),4,dtype=np.int64));var=pd.DataFrame({'gene_id':['ID'+str(i) for i in range(601)],'gene_symbol':['g'+str(i) for i in range(601)],'feature_type':['']*601})
  def fake(a,**kwargs):
   self.assertEqual(kwargs,{'random_state':0,'verbose':False,'expected_doublet_rate':.008*40/1000});a.obs['doublet_score']=np.linspace(0,.9,40);a.obs['predicted_doublet']=[True]+[False]*39;a.uns['scrublet']={'threshold':.8}
  rec=BoundsRecorder()
  with patch.object(fm.sc.pp,'scrublet',fake):a,row=fm.call_and_qc(X,var,np.array(['S::'+str(i) for i in range(40)]),{'library':'synthetic'},rec)
  self.assertEqual((row['n_barcodes'],row['paper_rule_cells'],row['mad_removed'],row['cells_after_qc'],row['doublets_flagged'],row['cells_final']),(40,40,0,40,1,39));self.assertTrue(sp.issparse(a.X));self.assertIn('bounds_synthetic',rec.bounds)
 def test_paper_filter_strict_boundaries(self):
  genes=np.array([500,501,6999,7000,501]);counts=np.array([2001,2001,2001,2001,2000]);got=(genes>fm.PAPER_FILTER['min_genes_exclusive'])&(genes<fm.PAPER_FILTER['max_genes_exclusive'])&(counts>fm.PAPER_FILTER['min_counts_exclusive']);self.assertEqual(got.tolist(),[False,True,True,False,False])
 def test_corrected_annotation_conditional(self):
  row={k:0. for k in {**fm.STATE_SETS,**fm.CONTAMINANT_SETS}};row.update(cluster='0',n_cells=10,Sftpc=1.,AT1_canonical=.7,AT2_identity=.2)
  table=pd.DataFrame([row]);self.assertEqual(fm.annotate_clusters_b(table).state.tolist(),['AT1']);self.assertFalse(fm.annotate_clusters_b(table).sftpc_informative.iloc[0]);self.assertNotEqual(fm.annotate_clusters(table).state.iloc[0],'AT1')
 def test_denominator_includes_unassigned_and_excludes_contaminants(self):
  obs=pd.DataFrame({'library':['L']*4,'state':['hAT2','unassigned','DATP','contaminant_immune']});rows=counts_and_fractions(obs);self.assertEqual(sum(x['count'] for x in rows),4);self.assertTrue(all(x['alveolar_including_unassigned']==3 for x in rows));self.assertEqual(next(x['fraction_alveolar'] for x in rows if x['state']=='unassigned'),1/3);self.assertIsNone(next(x['fraction_alveolar'] for x in rows if x['state'].startswith('contaminant_')))
 def test_fresh_output_refuses_outside_and_existing_artifacts(self):
  with tempfile.TemporaryDirectory() as t:
   root=pathlib.Path(t)
   with patch.object(common,'ROOT',root):
    with self.assertRaisesRegex(ValueError,'scoped'):common.fresh_output(root/'outside','metadata')
    out=common.fresh_output(root/'analysis/research/runs/p001_metadata_v1_test','metadata');(out/'old.csv').write_text('preserve')
    with self.assertRaisesRegex(ValueError,'already'):common.fresh_output(out,'metadata')
    self.assertEqual((out/'old.csv').read_text(),'preserve')
 def test_metadata_feature_id_order(self):
  from metadata import check_feature_order
  v=pd.DataFrame({'gene_id':['ID1','ID2']});reference=check_feature_order(None,v);self.assertEqual(check_feature_order(reference,v),reference)
  for ids in [['ID2','ID1'],['ID1','ID3']]:
   with self.assertRaisesRegex(ValueError,'feature ID/order'):check_feature_order(reference,pd.DataFrame({'gene_id':ids}))
 def test_describe_synthetic_serialization_and_panels(self):
  import anndata as ad,figure1
  genes=sorted({g for group in list(fm.STATE_SETS.values())+list(fm.CONTAMINANT_SETS.values()) for g in group})
  clusters=['datp']*31+['hat2','at1','immune','empty'];X=np.zeros((len(clusters),len(genes)),dtype=np.int64)
  for i,cl in enumerate(clusters):
   selected={'datp':fm.STATE_SETS['DATP'],'hat2':['Sftpc']+fm.STATE_SETS['AT2_identity'],'at1':fm.STATE_SETS['AT1_canonical'],'immune':fm.CONTAMINANT_SETS['immune'],'empty':[]}[cl]
   for g in selected:X[i,genes.index(g)]=3
  obs=pd.DataFrame({'library':['L'+str(i%3) for i in range(len(clusters))],'gsm':['S'+str(i%3) for i in range(len(clusters))],'timepoint':[['PBS','day 14','day 28'][i%3] for i in range(len(clusters))]},index=['S::'+str(i) for i in range(len(clusters))])
  for resolution in (.3,.5,1.):obs[f'leiden_{resolution}']=clusters
  a=ad.AnnData(sp.csr_matrix(X),obs=obs,var=pd.DataFrame(index=genes));a.layers['counts']=a.X.copy()
  # Synthetic coordinates/connectivities, not a biological embedding or graph qualification.
  a.obsm['X_umap']=np.random.default_rng(0).normal(size=(a.n_obs,2));a.obsm['X_pca']=np.zeros((a.n_obs,30));a.obsp['connectivities']=sp.eye(a.n_obs,format='csr')
  def leiden(sub,**kw):
   self.assertEqual(kw,{'resolution':.5,'key_added':'sub','flavor':'igraph','n_iterations':2,'random_state':0});sub.obs['sub']='0'
  with tempfile.TemporaryDirectory() as t,patch.object(figure1.sc.pp,'neighbors') as neighbors,patch.object(figure1.sc.tl,'leiden',leiden):
   out=pathlib.Path(t);summary=figure1.describe(a,out);common.write_json(out/'descriptive-summary.json',summary);loaded=json.loads((out/'descriptive-summary.json').read_text())
   self.assertEqual(set(loaded['states_assigned_before_subclustering']),{'0.3','0.5','1.0'})
   for states in loaded['states_assigned_before_subclustering'].values():self.assertEqual(states,['AT1','DATP','hAT2'])
   self.assertTrue(loaded['pAT2_absent']);self.assertTrue(loaded['DATP_subclustering']['triggered']);self.assertIn('unassigned',a.obs.state.values);self.assertIn('contaminant_immune',a.obs.state.values)
   self.assertEqual(sum(d['total_post_doublet'] for d in loaded['denominators_by_library'].values()),35);self.assertEqual(sum(d['unassigned'] for d in loaded['denominators_by_library'].values()),1)
   self.assertEqual(neighbors.call_args.kwargs,{'n_neighbors':30,'use_rep':'X_pca','random_state':0})
   for name in ['qc_cell_counts.png','figure1B_state_umap.png','qc_library_timepoint_umap.png','figure1C_composition.png','figure1D_marker_detection.png']:self.assertEqual((out/name).read_bytes()[:8],b'\x89PNG\r\n\x1a\n')
   self.assertFalse((out/'figure1B_counts.png').exists());self.assertGreater(len(pd.read_csv(out/'marker_evidence.csv')),0)
   print('SYNTHETIC_DESCRIBE_OUTPUT_HASHES '+json.dumps({x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(out.iterdir())}))
 def test_draft_job_hold(self):
  with self.assertRaisesRegex(ValueError,'reviewed'):require_reviewed_job(None,'metadata')
if __name__=='__main__':unittest.main()
