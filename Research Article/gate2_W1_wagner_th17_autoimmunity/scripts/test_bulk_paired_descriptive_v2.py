import unittest
import numpy as np
import pandas as pd
import bulk_paired_descriptive_v2 as b

class PairedArithmetic(unittest.TestCase):
    def test_technical_sum_preserves_fractional_counts(self):
        raw=pd.DataFrame([[.1,.2,2,3],[2,4,0,2]],columns=['a1','a2','b1','b2'])
        mapping=pd.DataFrame(dict(source_title=raw.columns,library_id=['a','a','b','b']))
        ids,counts=b.collapse_counts(raw,mapping)
        self.assertEqual(ids,['a','b']);np.testing.assert_allclose(counts,[[.3,5],[6,2]])
        with self.assertRaisesRegex(ValueError,'mismatch'):b.collapse_counts(raw.drop(columns='b2'),mapping)
    def test_pairing_uses_animal_not_row_adjacency(self):
        libs=pd.DataFrame(dict(animal_id=['WT2','WT1','WT1','WT2'],cell_type=['Th17n']*4,genotype=['WT']*4,treatment=['DFMO','control','DFMO','control']))
        animals,delta=b.paired_difference(np.array([[9,1,4,7],[0,3,4,1]]),libs,'Th17n','WT')
        self.assertEqual(animals,['WT1','WT2']);np.testing.assert_equal(delta,[[3,2],[1,-1]])
        with self.assertRaisesRegex(ValueError,'Incomplete'):b.paired_difference(np.array([[9,1,4]]),libs.iloc[:3],'Th17n','WT')

if __name__=='__main__':unittest.main()
