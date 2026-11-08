import unittest
import numpy as np
import pandas as pd
from public_cells_v1 import measurements, GENES, masks

class EdgeCases(unittest.TestCase):
    def frame(self):
        a=pd.DataFrame(np.zeros((4,len(GENES)),dtype=int),columns=GENES)
        a['full_library_size']=[1000,2000,4000,8000];a['n_genes_by_counts']=500
        a['ann_finest_level']='AT2';a['ann_level_1']='Epithelial';a['ann_finest_level_uncertainty']=[.2,.3,.31,.1]
        return a
    def test_zeros_are_not_positive_intensity(self):
        rows,pairs=measurements(self.frame(),{})
        self.assertEqual(rows[0]['fraction_detected'],0);self.assertTrue(np.isnan(rows[0]['positive_mean_log']))
        self.assertTrue(np.isnan(pairs[0]['conditional_on_IL1R1']))
    def test_joint_denominators(self):
        a=self.frame();a.IL1R1=[0,1,0,1];a.IL1RAP=[0,0,1,1]
        _,p=measurements(a,{});self.assertEqual([p[0][k] for k in ['n00','n10','n01','n11']],[1]*4)
        self.assertEqual(p[0]['conditional_on_IL1R1'],.5);self.assertEqual(p[0]['joint_fraction'],.25)
    def test_confidence_boundaries(self):
        m=masks(self.frame());self.assertEqual(int(m['AT2_u20'].sum()),2);self.assertEqual(int(m['AT2_u30'].sum()),3);self.assertEqual(int(m['AT2_allQC'].sum()),4)

if __name__=='__main__':unittest.main()
