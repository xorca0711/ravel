"""Known-answer tests before real treatment contrasts are executed."""
import unittest
import numpy as np
from describe_v1 import median_ratio_denominators,contrast_values
class KnownAnswers(unittest.TestCase):
    def test_proportional_libraries(self):
        x=np.array([0,2,5,11,39])[:,None]*np.array([1,2,3,8])[None,:]
        den,sf,n=median_ratio_denominators(x)
        self.assertEqual(n,4)
        np.testing.assert_allclose(den,x.sum(axis=0))
        normalized=x/den*1e6
        np.testing.assert_allclose(normalized,np.repeat(normalized[:,:1],4,axis=1))
    def test_known_contrasts(self):
        v=contrast_values(np.array([[0,2,3,5,2,4,7,9]],dtype=float),np.array(['PBS','PBS','WT','WT','DE','DE','SUPER','SUPER']))
        self.assertEqual({k:float(x[0]) for k,x in v.items()},{'WT-PBS':3,'DE-PBS':2,'SUPER-PBS':7,'DE-WT':-1,'SUPER-WT':4})
    def test_empty_positive_reference_stops(self):
        with self.assertRaises(AssertionError):median_ratio_denominators(np.array([[0,1],[1,0]]))
if __name__=='__main__':unittest.main()
