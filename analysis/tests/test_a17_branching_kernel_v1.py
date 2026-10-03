import importlib.util
import math
from pathlib import Path
import random
import unittest

P = Path(__file__).resolve().parents[1] / 'scripts/a17_branching_kernel_v1.py'
spec = importlib.util.spec_from_file_location('kernel', P)
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)

class FixedDraws:
    def __init__(self, waits, choices):
        self.waits = iter(waits)
        self.choices = iter(choices)
    def expovariate(self, total):
        return next(self.waits)
    def random(self):
        return next(self.choices)

class BranchingKernelTests(unittest.TestCase):
    def test_slow_loss_is_reachable_and_extinction_absorbs(self):
        self.assertEqual(k.simulate((0,1), [(2,(0,0,0,1,0,0))], FixedDraws([.2],[.9])), (0,0))
        self.assertEqual(k.simulate((0,0), [(2,(1,1,1,1,1,1))], FixedDraws([],[])), (0,0))
    def test_no_event_crosses_a_regime_or_observation_boundary(self):
        rng=FixedDraws([2,.1],[.2])
        self.assertEqual(k.simulate((1,0), [(1,(1,0,0,0,0,0)),(2,(0,1,0,0,0,0))], rng), (0,0))
        self.assertEqual(k.simulate((1,0), [(1,(1,0,0,0,0,0))], FixedDraws([1],[])), (1,0))
    def test_switching_conserves_size_and_both_directions_work(self):
        self.assertEqual(k.simulate((1,0), [(1,(0,0,0,0,1,1))], FixedDraws([.1,.1,2],[.5,.5])), (1,0))
    def test_zero_rate_interval_does_not_prevent_later_events(self):
        self.assertEqual(k.simulate((1,0), [(1,(0,0,0,0,0,0)),(2,(0,1,0,0,0,0))], FixedDraws([.1],[.5])), (0,0))
    def test_invalid_rates_and_numerical_caps_fail_closed(self):
        with self.assertRaises(ValueError):
            k.simulate((1,0), [(1,(-1,0,0,0,0,0))], random.Random(1))
        with self.assertRaises(RuntimeError):
            k.simulate((1,0), [(1,(1,0,0,0,0,0))], FixedDraws([.1],[.5]), cap=2)
    def test_founder_extremes_have_no_extra_fast_clone(self):
        self.assertEqual(k.founder_initial(0, random.Random(1)), (0,1))
        self.assertEqual(k.founder_initial(1, random.Random(1)), (1,0))
    def test_conditioning_uses_model_mass_and_preserves_impossible_observations(self):
        self.assertAlmostEqual(k.conditional_log_score({0:.5,1:.25,2:.125,3:.125},[2,3]), -math.log(2))
        self.assertEqual(k.conditional_log_score({0:.5,2:.5},[3]), -math.inf)
        with self.assertRaises(ValueError):
            k.conditional_log_score({2:.5},[2])
    def test_analytic_reference_has_correct_pure_birth_and_critical_limits(self):
        mean,var,p0=k.birth_death_reference(1,0,1)
        self.assertAlmostEqual(mean, math.e)
        self.assertAlmostEqual(var, math.e*(math.e-1))
        self.assertEqual(p0, 0)
        self.assertEqual(k.birth_death_reference(1,1,1), (1,2,.5))

if __name__ == '__main__':
    unittest.main()
