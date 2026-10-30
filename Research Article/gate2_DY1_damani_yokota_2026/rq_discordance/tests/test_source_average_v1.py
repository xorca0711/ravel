from pathlib import Path
import sys
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from source_average_response_v1 import contrasts, summarize, verify_all


class AverageTests(unittest.TestCase):
    def test_baseline_shift_not_response_change(self):
        values = np.array([[0., 1., 1., 3.], [0., 3., 0., 1.]])
        r = contrasts(values, 1)
        np.testing.assert_allclose(r.first_stage_log_ratio, [1, 2]); np.testing.assert_allclose(r.second_stage_log_ratio, [1, 1])
        np.testing.assert_allclose(r.second_minus_first, [0, -1]); self.assertTrue(verify_all(values, r, 1)['passed'])

    def test_all_zero_rows_retained_but_separately_counted(self):
        r = contrasts(np.array([[0., 0., 0., 0.], [1., 1., 1., 1.], [0., 1., 1., 0.]]), 1)
        s = summarize(r, 1)
        self.assertEqual(s['source_rows'], 3); self.assertEqual(s['all_zero_wt_rows'], 1)
        self.assertEqual(s['both_zero_contrasts'], 1); self.assertEqual(s['opposite_nonzero_sign'], 1)

    def test_invalid_averages_rejected(self):
        with self.assertRaises(ValueError): contrasts(np.array([[0., -1., 0., 1.]]), 1)
        with self.assertRaises(ValueError): contrasts(np.zeros((1, 4)), 0)


if __name__ == '__main__': unittest.main()
