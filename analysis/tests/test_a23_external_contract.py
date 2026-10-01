"""Small failure-path checks for A23 source joins and immutable run receipts."""
import importlib.util
import json
import pathlib
import tempfile
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
PATH=ROOT/'RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/02_external_pilot.py'
SPEC=importlib.util.spec_from_file_location('a23_external',PATH)
MOD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(MOD)
class A23ExternalTests(unittest.TestCase):
 def test_same_barcode_in_different_libraries_stays_distinct(self):
  got=MOD.annotation_map([('neg.AAAA','AT2'),('pos.AAAA','Macrophage')],{'neg':'A','pos':'B'})
  self.assertEqual(len(got),2);self.assertEqual(got[('A','AAAA')],'AT2')
 def test_duplicate_annotation_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'Duplicate'):MOD.annotation_map([('neg.AAAA','AT2'),('neg.AAAA','AT1')],{'neg':'A'})
 def test_gem_suffix_is_not_silently_collapsed(self):
  with self.assertRaisesRegex(ValueError,'gem suffix'):MOD.annotation_key('A','AAAA-2')
 def test_changed_recorded_output_is_rejected(self):
  oldroot,oldrq=MOD.ROOT,MOD.RQ
  try:
   with tempfile.TemporaryDirectory() as d:
    root=pathlib.Path(d);MOD.ROOT=root;MOD.RQ=root/'rq'
    out=root/'result.tsv';out.write_bytes(b'original')
    receipt=MOD.RQ/'metadata'/MOD.RUN/'run_record.json';receipt.parent.mkdir(parents=True)
    receipt.write_text(json.dumps({'inputs':[],'outputs':[{'path':'result.tsv','sha256':MOD.digest(out)}]}))
    out.write_bytes(b'changed')
    with self.assertRaisesRegex(ValueError,'Hash mismatch'):MOD.check(True)
  finally:MOD.ROOT,MOD.RQ=oldroot,oldrq
if __name__=='__main__':unittest.main()
