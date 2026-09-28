"""Regression checks for the versioned A15 count-normalization correction."""
import importlib.util
import math
from pathlib import Path
import tempfile
import unittest

PATH = (Path(__file__).resolve().parents[2] / "RQ_Specified" /
        "A15_epithelial_integrin_tgfb_activation/scripts/04_rival2_normalization_correction.py")
SPEC = importlib.util.spec_from_file_location("a15_correction", PATH)
correction = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(correction)


class NormalizationCorrectionTests(unittest.TestCase):
    def test_proportional_library_invariance_and_old_denominator_failure(self):
        multipliers = [1, 2, 3, 7, 11, 19, 23, 31]
        matrix = {str(g): [g * m for m in multipliers] for g in (100, 200, 300)}
        factors, reference = correction.median_ratio_factors(matrix)
        for counts in matrix.values():
            normalized = [count / factor for count, factor in zip(counts, factors)]
            for value in normalized:
                self.assertAlmostEqual(value, normalized[0], places=8)
        scores = correction.panel_scores(matrix, reference, factors)
        for value in scores:
            self.assertAlmostEqual(value, scores[0], places=10)
        totals = [600 * m for m in multipliers]
        defective = [matrix["100"][j] / (factors[j] * totals[j] / 1e6) for j in range(8)]
        self.assertAlmostEqual(defective[1] / defective[0], 0.5)
        self.assertGreater(abs(math.log2(defective[1] + 1) - math.log2(defective[0] + 1)), 0.99)

    def test_reference_excludes_endpoints_and_any_zero(self):
        matrix = {"r1": [10, 20], "r2": [20, 40], "endpoint": [999, 1], "zero": [0, 99]}
        factors, reference = correction.median_ratio_factors(matrix, {"endpoint"})
        self.assertEqual(reference, ["r1", "r2"])
        self.assertAlmostEqual(factors[1] / factors[0], 2)

    def test_even_reference_uses_arithmetic_ratio_median(self):
        factors, _ = correction.median_ratio_factors({"r1": [1, 1, 1], "r2": [1, 8, 1]})
        # Ratios are [1,1,1] and [0.5,4,0.5]; arithmetic medians [0.75,2.5,0.75].
        self.assertAlmostEqual(factors[1] / factors[0], 2.5 / 0.75)

    def test_empty_or_insufficient_reference_stops(self):
        with self.assertRaisesRegex(ValueError, "insufficient"):
            correction.median_ratio_factors({"zero": [0, 1]})
        with self.assertRaisesRegex(ValueError, "insufficient"):
            correction.median_ratio_factors({"one": [1, 1]}, minimum_reference_genes=2)

    def test_exact_separation_and_ties(self):
        separated = correction.contrast([1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(separated["exact_test"]["p_two_sided"], 2 / 70)
        self.assertTrue(separated["separates_at_declared_alpha"])
        self.assertEqual(separated["shift"]["lower"], -7)
        self.assertEqual(separated["shift"]["upper"], -1)
        tied = correction.contrast([1] * 8)
        self.assertEqual(tied["exact_test"]["p_two_sided"], 1)
        self.assertFalse(tied["separates_at_declared_alpha"])

    def test_sensitivity_disagreement_adds_only_its_downgrade(self):
        baseline = {
            "results": {f"primary1_{name}": {"standardised": {"separates_at_declared_alpha": False}}
                        for name in ("transitional", "identity")},
            "verdict": {"value": "weak_bound_on_rival_2", "downgrade_reasons": [],
                        "transitional_separates": False, "identity_separates": False,
                        "omnibus_correlation_separates": False,
                        "engagement_separates_in_declared_direction": True},
        }
        corrected = {name: {"separates_at_declared_alpha": name == "identity"}
                     for name in ("transitional", "identity")}
        decision = correction.updated_decision(baseline, corrected)
        self.assertEqual(decision["corrected_algorithmic_verdict"], "inconclusive")
        self.assertEqual(decision["downgrade_reasons"], [correction.MOR_REASON])
        self.assertEqual(baseline["verdict"]["downgrade_reasons"], [])
    def test_existing_output_is_never_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            sentinel = path / "original.txt"
            sentinel.write_text("preserve", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                correction.refuse_existing_output(path)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")


if __name__ == "__main__":
    unittest.main()
