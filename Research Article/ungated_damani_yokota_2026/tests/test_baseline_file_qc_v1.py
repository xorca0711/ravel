import gzip,importlib.util,sys,tempfile,unittest
from pathlib import Path
S=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(S))
spec=importlib.util.spec_from_file_location('qc',S/'baseline_file_qc_v1.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class FormatTests(unittest.TestCase):
    def file(self,text):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);p=Path(t.name)/'test.gz'
        with gzip.open(p,'wt') as f:f.write(text)
        return p
    def test_summary_is_not_feature_denominator(self):
        r,s,u,z=m.exon_qc(self.file('ENSMUSG1:001\t0\nENSMUSG2:001\t5\n_empty\t100\n'))
        self.assertEqual(r['feature_count_sum'],5);self.assertEqual(r['summary_count_sum'],100);self.assertEqual(z,{'ENSMUSG1:001'});self.assertEqual(len(s),1)
    def test_bad_counts_and_duplicate_ids_hold(self):
        r,s,u,z=m.exon_qc(self.file('ENSMUSG1:001\t-1\nENSMUSG1:001\t2\nENSMUSG2:001\t1.5\n'))
        self.assertEqual(r['negative_counts'],1);self.assertEqual(r['duplicate_id_occurrences'],1);self.assertEqual(r['invalid_integer'],1);self.assertFalse(m.exon_universe([r],[u],[z])['count_format_eligible'])
    def test_different_feature_universe_is_not_aligned_by_position(self):
        a,_,u,z=m.exon_qc(self.file('ENSMUSG1:001\t2\n'));b,_,v,y=m.exon_qc(self.file('ENSMUSG2:001\t2\n'))
        self.assertFalse(m.exon_universe([a,b],[u,v],[z,y])['count_format_eligible'])
    def test_peak_duplicates_missingness_and_summit(self):
        p=self.file('chr1\t10\t20\tp1\t0\t.\t2\t-1\t-1\t5\nchr1\t10\t20\tp2\t0\t.\t2\t-1\t-1\t10\n')
        r=m.peak_qc(p);self.assertEqual(r['duplicate_interval_occurrences'],1);self.assertEqual(r['invalid_summit'],1);self.assertEqual(r['missing_q_field'],2);self.assertEqual(r['width_median'],10)

if __name__=='__main__':unittest.main()
