import gzip,sys,tempfile,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import rna_extension_v1 as r

class RnaDescriptionTests(unittest.TestCase):
    def test_all_source_denominator_includes_nonreported_gene(self):
        a=r.Accumulator(3,[False]*3,True);a.add(np.array([0,2]),np.array([10.,90.]));p,e=a.finish()
        self.assertEqual(p[0,0],100000);self.assertEqual(e[0,0],100000)
        self.assertNotEqual(p[0,0],1000000) # incorrect common-only denominator
    def test_weighting_and_transform_order_are_distinct(self):
        a=r.Accumulator(2,[False]*2,True)
        a.add(np.array([0,1]),np.array([90.,10.]));a.add(np.array([0,1]),np.array([1.,9.]));p,e=a.finish()
        self.assertAlmostEqual(p[0,0],1e6*91/110);self.assertAlmostEqual(e[0,0],500000)
        self.assertNotAlmostEqual(np.log2(e[0,0]+1),np.mean(np.log2(np.array([900000,100000])+1)))
    def test_qc_inclusive_boundaries(self):
        self.assertTrue(r.qc_pass(500,200,200));self.assertTrue(r.qc_pass(10000,2500,4000))
        for values in [(499,200,0),(500,199,0),(10000,2501,0),(500,200,201)]:self.assertFalse(r.qc_pass(*values))
    def test_zero_depth_and_empty_qc_remain_undefined(self):
        a=r.Accumulator(2,[False]*2,True);self.assertEqual(a.add(np.array([],int),np.array([],float))[:3],(0,0,0))
        a.add(np.array([0]),np.array([2.]));p,e=a.finish()
        self.assertEqual(a.n.tolist(),[1,0]);self.assertTrue(np.isnan(p[1]).all());self.assertTrue(np.isnan(e[1]).all());self.assertEqual(r.number(p[1,0]),'')
    def test_source_symbol_ambiguity_is_local_hold(self):
        m={'a':{'ids':['id1'],'names':['Cd74']},'b':{'ids':['id1'],'names':['Cd74']}}
        resolved,_=r.resolve_targets(m,{'id1'});self.assertEqual(resolved['Cd74'],'id1');self.assertIsNone(resolved['Mif'])
        m['b']={'ids':['id1','id2'],'names':['Cd74','Cd74']};self.assertIsNone(r.resolve_targets(m,{'id1','id2'})[0]['Cd74'])
    def test_mitochondrial_disagreement_holds_only_qc(self):
        m={'a':{'ids':['m1'],'names':['mt-Nd1']},'b':{'ids':['m2'],'names':['mt-Nd1']}}
        self.assertFalse(r.mitochondrial_map(m)[1]);a=r.Accumulator(1,[True],False);a.add(np.array([0]),np.array([600.]));self.assertEqual(a.n.tolist(),[1,0])
    def test_streaming_formats_exclude_atac_and_preserve_empty_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);mapping=np.array([0,-1,1]);h=root/'tiny.h5';t=root/'tiny.mtx.gz'
            with r.h5py.File(h,'w') as f:
                g=f.create_group('matrix');g['indptr']=[0,3,4,4];g['indices']=[0,1,2,1];g['data']=[10,900,90,800]
            with gzip.open(t,'wt') as f:f.write('%%MatrixMarket matrix coordinate integer general\n% fixture\n3 3 4\n1 1 10\n2 1 900\n3 1 90\n2 2 800\n')
            for reader,path in [(r.h5_columns,h),(r.mtx_columns,t)]:
                cols=list(reader(path,mapping,3));self.assertEqual(len(cols),3)
                self.assertEqual(cols[0][1].tolist(),[0,1]);self.assertEqual(cols[0][2].tolist(),[10,90])
                self.assertEqual(len(cols[1][1]),0);self.assertEqual(len(cols[2][1]),0)
                a=r.Accumulator(2,[False]*2,True)
                for _,ix,v in cols:a.add(ix,v)
                self.assertEqual(a.depth.tolist(),[100,0]);self.assertEqual(a.finish()[0][0].tolist(),[100000,900000])
    def test_sparse_accumulation_rejects_duplicates(self):
        a=r.Accumulator(2,[False]*2,True)
        with self.assertRaises(ValueError):a.add(np.array([0,0]),np.array([1.,2.]))
        with self.assertRaises(ValueError):a.add(np.array([0]),np.array([1.5]))

if __name__=='__main__':unittest.main()
