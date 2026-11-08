import unittest
import numpy as np
from public_spatial_v1 import adjacency, statistics

class Geometry(unittest.TestCase):
    def test_six_neighbors_and_detached_tissue(self):
        a=adjacency([0,0,0,1,1,-1,-1,20],[0,2,-2,1,-1,1,-1,20])
        self.assertEqual(a[0].sum(),6);self.assertEqual(a[7].sum(),0);self.assertEqual((a-a.T).nnz,0);self.assertFalse(a.diagonal().any())
    def test_gap_is_not_bridged(self):
        a=adjacency([0,0],[0,4]);self.assertEqual(a.nnz,0)
    def test_one_and_two_hops_are_distinct(self):
        a=adjacency([0,0,0],[0,2,4]);z=np.array([[-1.,1.],[0.,0.],[1.,-1.]])
        s,_=statistics(z,a);self.assertAlmostEqual(s['lag1'],0);self.assertAlmostEqual(s['lag2'],2/3);self.assertAlmostEqual(s['same_spot'],-2/3)

if __name__=='__main__':unittest.main()
