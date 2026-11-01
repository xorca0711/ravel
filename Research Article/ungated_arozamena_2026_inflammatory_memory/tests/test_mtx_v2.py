from pathlib import Path
import gzip,sys,tempfile,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import qualify_mtx_v2 as q


class EmptyRecordTests(unittest.TestCase):
    def fixture(self,p,feature='g1\tG\tGene Expression\tchr1\t1\t2\n\nchr1:3-5\tP\tPeaks\tchr1\t3\t5\n\n',barcodes='AA\n\nBB\n\n',matrix='%%MatrixMarket matrix coordinate integer general\n\n% source\n\n2 2 3\n\n1 1 2\n\n2 1 1\n\n2 2 3\n\n'):
        for name,text in [('f',feature),('b',barcodes),('m',matrix)]:
            with gzip.open(p/name,'wt',newline='\n') as f:f.write(text)
        return p/'m',p/'f',p/'b'

    def test_interleaved_empty_records_and_explicit_types(self):
        with tempfile.TemporaryDirectory() as d:
            paths=self.fixture(Path(d));info,ft,bc,blanks=q.inspect_mtx(*paths)
            self.assertEqual(info['observed_both_RNA_ATAC'],1);self.assertEqual(ft['Peaks'],{'chr1:3-5'})
            self.assertEqual(blanks['feature_empty_records'],2);self.assertEqual(blanks['barcode_empty_records'],2);self.assertEqual(blanks['matrix_empty_records'],6)
            self.assertEqual(bc,['AA','BB']);self.assertEqual(info['coordinate_uniqueness'],'verified_strict_column_order')
            with self.assertRaisesRegex(ValueError,'Missing feature-type'):q.prior.mtx_metadata(*paths)

    def test_nonempty_missing_type_is_not_guessed(self):
        with tempfile.TemporaryDirectory() as d:
            paths=self.fixture(Path(d),feature='g1\tG\n\nchr1:3-5\n')
            with self.assertRaisesRegex(ValueError,'explicit type'):q.inspect_mtx(*paths)

    def test_dimensions_after_blank_removal(self):
        with tempfile.TemporaryDirectory() as d:
            paths=self.fixture(Path(d),barcodes='AA\n\n')
            with self.assertRaisesRegex(ValueError,'dimensions disagree'):q.inspect_mtx(*paths)

    def test_duplicate_nonempty_barcode_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            paths=self.fixture(Path(d),barcodes='AA\n\nAA\n')
            with self.assertRaisesRegex(ValueError,'barcodes'):q.inspect_mtx(*paths)

    def test_noninteger_entry_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            paths=self.fixture(Path(d),matrix='%%MatrixMarket matrix coordinate real general\n2 2 1\n\n1 1 0.5\n')
            with self.assertRaisesRegex(ValueError,'Invalid sparse'):q.inspect_mtx(*paths)


if __name__=='__main__':unittest.main()
