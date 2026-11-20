import importlib.util,unittest
from pathlib import Path
import numpy as np
S=Path(__file__).resolve().parents[1]/'scripts';spec=importlib.util.spec_from_file_location('profiles',S/'baseline_exon_profile_v1.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ProfileTests(unittest.TestCase):
    def test_only_all_zero_rows_removed_and_full_denominator(self):
        x=np.array([[0,0,0],[1,2,4],[8,4,1],[2,2,2]])
        scores,var,ratio,tot,keep=m.profile(x)
        np.testing.assert_array_equal(keep,[False,True,True,True]);np.testing.assert_array_equal(tot,[11,8,7]);self.assertEqual(scores.shape,(3,3));self.assertAlmostEqual(float(ratio.sum()),1)
    def test_library_scaling_preserves_exon_hit_profile(self):
        x=np.array([[1,2,4],[8,4,1],[2,2,2]])
        a=m.profile(x);b=m.profile(x*np.array([2,3,5]))
        np.testing.assert_allclose(a[0]@a[0].T,b[0]@b[0].T,atol=1e-10)
    def test_invalid_or_constant_profiles_stop(self):
        for x in [np.array([[0,1],[0,2]]),np.array([[-1,2],[4,1]]),np.ones((3,3),dtype=int)]:
            with self.assertRaises(ValueError):m.profile(x)

if __name__=='__main__':unittest.main()
