from pathlib import Path
import csv,gzip,json,sys,tempfile,unittest,zipfile
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import qualify_v1 as q


class QualificationTests(unittest.TestCase):
    def test_soft_repeated_fields_and_identity(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.gz'
            with gzip.open(p,'wt') as f:f.write('^SERIES = GSE1\n!Series_title = title\n^SAMPLE = GSM1\n!Sample_characteristics_ch1 = a: one\n!Sample_characteristics_ch1 = b: two\n')
            records=q.soft_records(p)
            self.assertEqual([r['id'] for r in records],['GSE1','GSM1'])
            self.assertEqual(records[1]['fields']['Sample_characteristics_ch1'],['a: one','b: two'])

    def test_ids_not_symbols_and_duplicate_barcode_rejection(self):
        info,groups=q.feature_info(['g1','g2'],['same','same'],['Gene Expression']*2,['AA','BB'])
        self.assertEqual(info['n_features'],2)
        with self.assertRaisesRegex(ValueError,'Duplicate feature'):q.feature_info(['g1','g1'],['a','b'],['X']*2,['AA'])
        with self.assertRaisesRegex(ValueError,'barcodes'):q.feature_info(['g1'],['a'],['X'],['AA','AA'])

    def h5(self,path,indices=(0,1,0),data=(1,2,3)):
        with q.h5py.File(path,'w') as f:
            m=f.create_group('matrix');m['shape']=[2,2];m['indptr']=np.array([0,2,3],dtype='uint64')
            m['indices']=np.asarray(indices,dtype='uint32');m['data']=np.asarray(data)
            m['barcodes']=np.array(['AA','BB'],dtype=q.h5py.string_dtype())
            g=m.create_group('features')
            for name,values in [('id',['g1','chr1:1-3']),('name',['same','same']),('feature_type',['Gene Expression','Peaks'])]:g[name]=np.array(values,dtype=q.h5py.string_dtype())

    def test_h5_shared_axis_and_unsigned_column_reset(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.h5';self.h5(p);info,ft,bc,schema=q.h5_metadata(p)
            self.assertEqual(info['observed_both_RNA_ATAC'],1);self.assertEqual(info['n_stored_entries'],3)
            self.assertEqual(bc,['AA','BB']);self.assertEqual(ft['Peaks'],{'chr1:1-3'})

    def test_h5_duplicate_coordinate_and_invalid_value(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.h5';self.h5(p,indices=(0,0,1))
            with self.assertRaisesRegex(ValueError,'Duplicate or unsorted'):q.h5_metadata(p)
            p=Path(d)/'b.h5';self.h5(p,data=(1,float('nan'),2))
            with self.assertRaisesRegex(ValueError,'Invalid count'):q.h5_metadata(p)

    def test_mtx_axes_integer_and_declared_nnz(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            def gz(name,text):
                with gzip.open(p/name,'wt') as f:f.write(text)
            gz('f.gz','g1\tG\tGene Expression\nchr1:1-3\tchr1:1-3\tPeaks\n');gz('b.gz','AA\nBB\n')
            gz('m.gz','%%MatrixMarket matrix coordinate integer general\n% source\n2 2 3\n1 1 2\n2 1 1\n2 2 4\n')
            info,*_=q.mtx_metadata(p/'m.gz',p/'f.gz',p/'b.gz')
            self.assertEqual(info['coordinate_uniqueness'],'verified_strict_column_order');self.assertEqual(info['observed_both_RNA_ATAC'],1)
            gz('bad.gz','%%MatrixMarket matrix coordinate integer general\n2 2 2\n1 1 2\n')
            with self.assertRaisesRegex(ValueError,'entry count'):q.mtx_metadata(p/'bad.gz',p/'f.gz',p/'b.gz')

    def test_dense_fractional_estimates_not_integer_counts(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.gz'
            with gzip.open(p,'wt') as f:f.write('\tgene_id\tgene_name\tS1\n1\tg1\tG\t1.25\n')
            info=q.dense_metadata(p,'bulk_counts');self.assertFalse(info['all_values_integer']);self.assertEqual(info['n_rows'],1)

    def test_lf_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.csv';q.write_csv(p,[{'key':'value'}],['key']);self.assertNotIn(b'\r',p.read_bytes())
            with self.assertRaises(FileExistsError):q.write_csv(p,[{'key':'new'}],['key'])

    def test_workbook_labels_keep_locators_and_ignore_numeric_values(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.xlsx'
            with zipfile.ZipFile(p,'w') as z:
                z.writestr('xl/workbook.xml','<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Figure" r:id="r1"/></sheets></workbook>')
                z.writestr('xl/_rels/workbook.xml.rels','<Relationships><Relationship Id="r1" Target="worksheets/s1.xml"/></Relationships>')
                z.writestr('xl/worksheets/s1.xml','<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row><c r="A1" t="inlineStr"><is><t>Control</t></is></c><c r="B1"><v>42</v></c></row></sheetData></worksheet>')
            self.assertEqual(q.workbook_text(p),[dict(sheet='Figure',cell='A1',text='Control')])


if __name__=='__main__':unittest.main()
