import importlib.util
from pathlib import Path
import sys
import unittest
import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from synthetic_uncertainty_v1 import events_for, validate
from verify_synthetic_v1 import expectations


class SyntheticTests(unittest.TestCase):
    def test_null_detection_and_sign_are_distinct(self):
        p = expectations(dict(truth_a=0, truth_b=0, se_a=.02, se_b=.5), .05)
        self.assertAlmostEqual(p['detect_a'], .05)
        self.assertAlmostEqual(p['detection_label_mismatch'], .095)
        self.assertAlmostEqual(p['same_sign'], .5)

    def test_boundary_and_sign_handling(self):
        s = dict(truth_a=0, truth_b=0, se_a=1, se_b=1)
        e = events_for(np.array([2., 3., -3., 0.]), np.array([3., 1., -3., 0.]), s, 2)
        self.assertEqual(e['only_b'].tolist(), [True, False, False, False])
        self.assertEqual(e['only_a'].tolist(), [False, True, False, False])
        self.assertEqual(e['both_detect'].tolist(), [False, False, True, False])
        self.assertEqual(e['same_sign'].tolist(), [True, True, True, False])
        self.assertEqual(e['coverage_a'].tolist(), [True, False, False, True])

    def test_bad_scale_rejected(self):
        c = dict(alpha=.05, draws_per_scenario=10, scenarios=[dict(id='x', truth_a=0, truth_b=0, se_a=0, se_b=1)])
        with self.assertRaises(ValueError): validate(c)

    def test_probability_partition_and_opposite_truth(self):
        s = dict(truth_a=.5, truth_b=.5, se_a=.25, se_b=.25)
        p = expectations(s, .05)
        self.assertAlmostEqual(sum(p[k] for k in ['both_detect', 'only_a', 'only_b', 'neither_detect']), 1)
        q = expectations({**s, 'truth_b': -.5}, .05)
        self.assertAlmostEqual(p['detection_label_mismatch'], q['detection_label_mismatch'])
        self.assertAlmostEqual(p['same_sign'], q['opposite_sign'])


if __name__ == '__main__': unittest.main()
