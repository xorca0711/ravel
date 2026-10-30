import gzip,importlib.util,tempfile,unittest
from pathlib import Path
import numpy as np
S=Path(__file__).resolve().parents[1]/'scripts';spec=importlib.util.spec_from_file_location('sparse_qc',S/'baseline_sparse_qc_v1.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class SparseChecks(unittest.TestCase):
    def file(self,text):
        d=tempfile.TemporaryDirectory();self.addCleanup(d.cleanup);p=Path(d.name)/'data.gz'
        with gzip.open(p,'wt') as f:f.write(text)
        return p
    def matrix(self,entries,nnz=4):return self.file('%%MatrixMarket matrix coordinate integer general\n3 2 '+str(nnz)+'\n'+entries)
    def test_type_accounting_across_chunks(self):
        p=self.matrix('1 1 2\n2 1 3\n3 2 4\n1 2 1\n')
        r,a,t=m.audit_matrix(p,np.array([1,0,1]),2,['Antibody Capture','Gene Expression'],chunksize=2)
        self.assertEqual(r['observed_entries'],4);self.assertEqual([x['count_sum'] for x in a],[3,7]);self.assertEqual([x['stored_entries'] for x in a],[1,3])
    def test_out_of_bounds_and_nonpositive_stop(self):
        for entry in ['4 1 2\n','1 1 0\n']:
            with self.assertRaises(ValueError):m.audit_matrix(self.matrix(entry,1),np.array([1,0,1]),2,['Antibody Capture','Gene Expression'])
    def test_wrong_nnz_stops(self):
        with self.assertRaisesRegex(ValueError,'entry count'):m.audit_matrix(self.matrix('1 1 2\n',2),np.array([1,0,1]),2,['Antibody Capture','Gene Expression'])
    def test_duplicate_barcode_stops(self):
        f=self.file('g\tgene\tGene Expression\nt\ttag\tAntibody Capture\n');b=self.file('cell\ncell\n')
        with self.assertRaisesRegex(ValueError,'duplicate barcode'):m.read_labels(f,b)
    def test_duplicate_tag_coordinates_are_explicit(self):
        p=self.matrix('2 1 2\n2 1 5\n',2)
        r,a,t=m.audit_matrix(p,np.array([1,0,1]),2,['Antibody Capture','Gene Expression'],chunksize=1,tag_features={1:'CMO301'})
        self.assertEqual(t[0]['raw_count_sum'],7);self.assertEqual(t[0]['positive_unique_barcodes'],1);self.assertEqual(t[0]['duplicate_stored_tag_coordinates'],1);self.assertEqual(t[0]['max_stored_entry'],5)

if __name__=='__main__':unittest.main()
