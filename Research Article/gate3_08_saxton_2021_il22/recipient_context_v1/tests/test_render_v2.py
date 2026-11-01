import importlib.util
import sys
import unittest
from pathlib import Path

scripts = Path(__file__).parents[1] / 'scripts'
sys.path.insert(0, str(scripts))
spec = importlib.util.spec_from_file_location('render_v2', scripts/'render_v2.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


class DisplayTests(unittest.TestCase):
    def test_empty_zero_and_small_positive_are_distinct(self):
        self.assertEqual(r.display_value(None), 'NA')
        self.assertEqual(r.display_value(float('nan')), 'NA')
        self.assertEqual(r.display_value(0), '0')
        for value in (1e-12, .0278, .0306, .09999):
            self.assertEqual(r.display_value(value), '<0.1')

    def test_threshold_and_invalid_values(self):
        self.assertEqual(r.display_value(.1), '0.1')
        self.assertEqual(r.display_value(12.34), '12.3')
        for value in (-.01, float('inf')):
            with self.assertRaises(ValueError): r.display_value(value)


if __name__ == '__main__':
    unittest.main()
