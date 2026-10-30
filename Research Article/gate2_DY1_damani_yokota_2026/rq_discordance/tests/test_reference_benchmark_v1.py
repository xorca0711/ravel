from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from reference_benchmark_v1 import conditional_intervals, normalize, summarize_pairs
from verify_reference_benchmark_v1 import scalar_intervals


class BenchmarkTests(unittest.TestCase):
    def test_all_pairings_and_scalar_agreement(self):
        a = np.array([[1., 3., 7.]]); b = np.array([[2., 8., 9.]])
        observed = conditional_intervals(a, b, .95).iloc[0]
        expected = scalar_intervals(a[0].tolist(), b[0].tolist(), .95)
        for key, value in expected.items(): self.assertAlmostEqual(observed[key], value)
        self.assertGreater(observed.paired_se_max, observed.paired_se_min)

    def test_column_order_does_not_assign_pairing(self):
        a = np.array([[1., 3., 7., 8.]]); b = np.array([[2., 8., 9., 11.]])
        x = conditional_intervals(a, b, .95); y = conditional_intervals(a[:, [3, 1, 0, 2]], b[:, [2, 0, 3, 1]], .95)
        np.testing.assert_allclose(x.select_dtypes(include='number'), y.select_dtypes(include='number'), rtol=1e-12, atol=1e-12)

    def test_zero_variance_not_certainty(self):
        r = conditional_intervals(np.array([[1., 1., 1.]]), np.array([[2., 2., 2.]]), .95).iloc[0]
        self.assertEqual(r.paired_degenerate_models, 6); self.assertFalse(r.sensitivity_directional)
        self.assertTrue(np.isnan(r.welch_lower))

    def test_denominator_includes_unreported_features(self):
        counts = np.array([[1., 4.], [9., 6.]])
        full = normalize(counts, counts.sum(axis=0), 1)
        selected = normalize(counts[:1], counts.sum(axis=0), 1)
        np.testing.assert_allclose(full[:1], selected)
        self.assertNotEqual(selected[0, 0], normalize(counts[:1], counts[:1].sum(axis=0), 1)[0, 0])

    def test_sign_partition_is_not_interval_classification(self):
        r = pd.DataFrame(dict(mean_delta=[1., 1., 0.], sensitivity_directional=[False, True, False]))
        a = pd.DataFrame(dict(mean_delta=[2., -1., 0.], sensitivity_directional=[True, True, False]))
        s = summarize_pairs(r, a)
        self.assertEqual((s['same_nonzero_sign'], s['opposite_nonzero_sign'], s['one_or_both_zero']), (1, 1, 1))
        self.assertEqual(s['both_directional_under_declared_models'], 1)


if __name__ == '__main__': unittest.main()
