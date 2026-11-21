import importlib.util
from pathlib import Path
import unittest
import numpy as np
from scipy.stats import t

s=importlib.util.spec_from_file_location('genotype',Path(__file__).parents[1]/'scripts/genotype_reference_v1.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class GenotypeReference(unittest.TestCase):
    def test_unequal_n_closed_form(self):
        r=m.welch(np.array([[1.,2,3]]),np.array([[2.,4,6,8]])).iloc[0]
        a,b=1/3,(20/3)/4;df=(a+b)**2/(a*a/2+b*b/3)
        self.assertAlmostEqual(r.mean_delta,3);self.assertAlmostEqual(r.se,np.sqrt(2))
        self.assertAlmostEqual(r.welch_df,df);self.assertAlmostEqual(r.conditional_upper,3+t.isf(.025,df)*np.sqrt(2))
    def test_swap_reverses_interval(self):
        a=np.array([[0.,1,4]]);b=np.array([[2.,3,8,10]])
        x=m.welch(a,b).iloc[0];y=m.welch(b,a).iloc[0]
        self.assertAlmostEqual(x.conditional_lower,-y.conditional_upper)
    def test_degenerate_is_not_precision(self):
        r=m.welch(np.zeros((1,3)),np.ones((1,4))).iloc[0]
        self.assertTrue(r.degenerate);self.assertTrue(np.isnan(r.conditional_lower));self.assertEqual(r.mean_delta,1)
    def test_insufficient_n_rejected(self):
        with self.assertRaises(ValueError):m.welch(np.zeros((1,1)),np.zeros((1,4)))

if __name__=='__main__':unittest.main()
