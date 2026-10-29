import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from human_stats_v1 import log_cpm,mean_difference,correlation_summary

class HumanObservationTests(unittest.TestCase):
    def test_uses_full_gene_denominator(self):
        self.assertAlmostEqual(log_cpm(np.array([[1,9]]),np.array([100]))[0,0],np.log2(10001))
    def test_invalid_denominator_rejected(self):
        with self.assertRaises(ValueError):log_cpm(np.array([[2,9]]),np.array([10]))
    def test_mean_contrast_interval_known_shift(self):
        result=mean_difference(np.array([5,6,7]),np.array([1,2,3]),np.random.default_rng(1))
        self.assertLess(result['ci_low'],4);self.assertGreater(result['ci_high'],4)
        self.assertEqual(result['bootstrap_valid_replicates'],2000)
    def test_constant_mean_interval_withheld(self):
        result=mean_difference([0]*8,[0]*8,np.random.default_rng(1))
        self.assertEqual(result['ci_status'],'constant_bootstrap_distribution')
        self.assertTrue(np.isnan(result['ci_low']))
    def test_sparse_correlation_held(self):
        result=correlation_summary([1,2],[2,3],np.array([[1],[2]]),np.random.default_rng(1))
        self.assertEqual(result['status'],'fewer_than_8_donors')
    def test_zero_heavy_bootstrap_interval_withheld(self):
        result=correlation_summary([0]*9+[1],np.arange(10),np.arange(10)[:,None],np.random.default_rng(1))
        self.assertEqual(result['ci_status'],'too_many_undefined_resamples')
        self.assertGreater(result['bootstrap_constant_replicates'],50)
    def test_constant_variable_held(self):
        result=correlation_summary([0]*10,np.arange(10),np.arange(10)[:,None],np.random.default_rng(1))
        self.assertEqual(result['status'],'constant_variable')
    def test_monotone_rho_and_reproducibility(self):
        x=np.arange(20);y=x**2;z=np.random.default_rng(7).normal(size=(20,1))
        a=correlation_summary(x,y,z,np.random.default_rng(1));b=correlation_summary(x,y,z,np.random.default_rng(1))
        self.assertAlmostEqual(a['rho'],1);self.assertEqual(a['ci_low'],b['ci_low'])

if __name__=='__main__':unittest.main()
