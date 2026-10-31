import importlib.util, pathlib, unittest
p=pathlib.Path(__file__).parents[1]/"scripts/r1_audit_v1.py"
s=importlib.util.spec_from_file_location("audit",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_bad_counts(self):
  for x in ["nan","inf","-1","1.5"]:
   with self.assertRaises(ValueError):m.valid_count(x)
 def test_integral_float(self): self.assertEqual(m.valid_count("3.0"),3)
 def test_missing_design(self):
  with self.assertRaises(ValueError):m.samples_from_soft("")
