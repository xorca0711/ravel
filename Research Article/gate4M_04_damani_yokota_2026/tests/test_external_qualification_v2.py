import gzip,importlib.util,tempfile,unittest
from pathlib import Path
import numpy as np

SCRIPT=Path(__file__).resolve().parents[1]/'scripts'/'qualify_external_human_v2.py'
spec=importlib.util.spec_from_file_location('external',SCRIPT);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class RawAggregationTests(unittest.TestCase):
    def test_duplicates_unassigned_cells_and_all_gene_denominator(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'tiny.gz'
            with gzip.open(p,'wt') as f:f.write('%%MatrixMarket matrix coordinate integer general\n3 3 4\n1 1 2\n2 1 3\n3 2 7\n1 3 11\n')
            selected,total,n=m.raw_aggregate(p,np.array([0,1,-1]),['A','A','B'],['A'],2)
            np.testing.assert_array_equal(selected,[[5],[0]]);np.testing.assert_array_equal(total,[5,7]);self.assertEqual(n,4)
    def test_dimension_conflict(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'tiny.gz'
            with gzip.open(p,'wt') as f:f.write('%%MatrixMarket matrix coordinate integer general\n1 2 1\n1 1 2\n')
            with self.assertRaisesRegex(ValueError,'dimensions'):m.raw_aggregate(p,np.array([0]),['A'],['A'],1)

if __name__=='__main__':unittest.main()
