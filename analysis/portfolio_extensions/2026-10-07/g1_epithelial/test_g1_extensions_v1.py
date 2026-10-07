"""Synthetic numerical checks only; no source outcomes are read."""
import unittest
import numpy as np
from a11_paired_prediction_v1 import fit
from a17_ascertainment_v1 import law, quantities, independent_probabilities


class Tests(unittest.TestCase):
    def test_training_isolated(self):
        x=np.random.default_rng(45).normal(size=(8,2,3))
        w,s,e=fit(x[:7],1.)
        x[7]*=1e6
        w2,s2,_=fit(x[:7],1.)
        np.testing.assert_array_equal(w,w2);np.testing.assert_array_equal(s,s2)
        self.assertLess(e,1e-6)
    def test_pair_swap(self):
        x=np.random.default_rng(14).normal(size=(7,2,3))
        w,s,_=fit(x,1.);v,t,_=fit(x[:,::-1],1.)
        np.testing.assert_allclose(w,-v,atol=1e-9);np.testing.assert_allclose(s,t)
    def test_no_contrast(self):
        x=np.ones((7,2,3));w,_,_=fit(x,1.)
        np.testing.assert_array_equal(w,np.zeros(3))
    def test_distribution(self):
        p,a,m=law(.8)
        n=np.arange(1,500)
        probs=(1-p)*(1-a)*a**(n-1)
        self.assertAlmostEqual(p+probs.sum(),1,12)
        self.assertAlmostEqual((n*probs).sum(),m,12)
        for k in [1,2,5]:
            _,r,c,_=quantities(.8,k)
            self.assertAlmostEqual(r,probs[n>=k].sum(),12)
            self.assertAlmostEqual(c,(n[n>=k]*probs[n>=k]).sum(),12)
    def test_piecewise_probability(self):
        y=independent_probabilities(.8,.2,3.)
        p,a,m=law(1.8)
        self.assertLess(abs(p-y[0]),1e-8);self.assertLess(abs(m-y[5]),1e-8)
    def test_initial(self):
        self.assertEqual(law(0),(0.,0.,1.))


if __name__=='__main__':unittest.main()
