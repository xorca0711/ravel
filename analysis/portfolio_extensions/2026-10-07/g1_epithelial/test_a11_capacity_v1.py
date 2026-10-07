import unittest
import numpy as np
from scipy.optimize import minimize
from a11_paired_prediction_v1 import fit


class DuplicateTest(unittest.TestCase):
    def test_duplicate_only_changes_penalty_geometry(self):
        x=np.random.default_rng(25).normal(size=(7,2,4))
        duplicate=2
        w,s,_=fit(x[:,:,[0,1,2,3,duplicate]],1.)
        scale=x.reshape(-1,4).std(axis=0)
        d=(x[:,1]-x[:,0])/scale
        penalty=np.ones(4);penalty[duplicate]=.5
        objective=lambda v:np.logaddexp(0,-d@v).mean()+(penalty*v*v).sum()/2
        result=minimize(objective,np.zeros(4),method='BFGS',options={'gtol':1e-8})
        merged=w[:4].copy();merged[duplicate]+=w[4]
        np.testing.assert_allclose(d@merged,d@result.x,atol=1e-6)
        np.testing.assert_allclose(s[:4],scale)


if __name__=='__main__':unittest.main()
