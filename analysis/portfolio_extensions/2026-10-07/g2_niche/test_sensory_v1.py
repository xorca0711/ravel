"""Synthetic tests only: no real outcome access before frozen execution."""
import unittest
import numpy as np
import pandas as pd
from sensory_v1 import summarize, paired, verify, GENES


class SensoryTests(unittest.TestCase):
    def test_counts_joint_denominator_and_pairing(self):
        rows=[]
        for label in ['Alveolar Fibroblast','Adventitial Fibroblast']:
            for i in range(24):
                r={'cohort':'Travaglini','assay':'10x','donor':'test','region':'distal',
                   'protocol':'10x','cell_type':label,'cell':label+str(i),'library':100+i,
                   'neural_flag':False,'fibro_marker':True, **{g:0 for g in GENES}}
                r['SCN7A']=2 if i%2==0 else 0
                r['GRIA1']=1 if i%3==0 else 0
                rows.append(r)
        cells=pd.DataFrame(rows)
        gene,joint=summarize(cells);effects,donors=paired(gene)
        self.assertEqual(verify(cells,gene,joint,effects,donors)['status'],'passed')
        np.testing.assert_array_equal(effects.delta_log2cpm,0)
        j=joint[(joint.depth=='all_depth')&(joint.threshold==1)&(joint.sensitivity=='all')]
        np.testing.assert_array_equal(j.n_joint,4)
        self.assertTrue((gene.library > gene.sum_count).all())
        self.assertEqual(len(donors),8)

    def test_neural_flag_does_not_change_primary(self):
        rows=[]
        for i in range(10):
            rows.append({'cohort':'test','assay':'test','donor':'test','region':'test','protocol':'test',
                         'cell_type':'test','cell':str(i),'library':100,'neural_flag':i<2,'fibro_marker':True,
                         **{g:1 for g in GENES}})
        gene,joint=summarize(pd.DataFrame(rows))
        self.assertEqual(set(gene[(gene.depth=='all_depth')&(gene.sensitivity=='all')].n_cells),{10})
        self.assertEqual(set(gene[(gene.depth=='all_depth')&(gene.sensitivity=='exclude_neural_flag')].n_cells),{8})
        self.assertTrue((joint[joint.threshold==2].n_joint==0).all())


if __name__=='__main__':
    unittest.main()
