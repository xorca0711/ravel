"""Failure modes that could produce false source/sample identity."""
import unittest
from metadata_v1 import soft_records, parse_sample


class MetadataTests(unittest.TestCase):
    def fields(self):
        return dict(title=['Lung tissue with second AAH of patient 4 [ST]'],
                    description=['Library name: P4_AAH-1'],
                    characteristics_ch1=['age: 65','Sex: Female','smoking: Yes','ethnicity: East Asian'])

    def test_preserve_ordinal_and_unknown_specimen(self):
        row=parse_sample('GSE307534','GSM1',self.fields())
        self.assertEqual(row['library_name_author'],'P4_AAH-1')
        self.assertEqual(row['library_alias_suffix'],'-1')
        self.assertEqual(row['section_id'],'')
        self.assertEqual(row['histology_original'],'')

    def test_refuse_ambiguous_author_alias(self):
        f=self.fields();f['description'].append('Library name: P4_AAH')
        with self.assertRaises(ValueError): parse_sample('GSE307534','GSM1',f)

    def test_refuse_patient_or_histology_conflict(self):
        for alias in ['P5_AAH-1','P4_LUAD-1','P4_AAHunknown']:
            f=self.fields();f['description']=['Library name: '+alias]
            with self.assertRaises(ValueError): parse_sample('GSE307534','GSM1',f)

    def test_refuse_duplicate_gsm(self):
        with self.assertRaises(ValueError):soft_records('^SAMPLE = GSM1\n!Sample_title = a\n^SAMPLE = GSM1\n!Sample_title = b\n')

    def test_stop_sample_at_next_entity(self):
        rows=soft_records('^SAMPLE = GSM1\n!Sample_title = a\n^PLATFORM = GPL1\n!Sample_title = not_a_sample\n')
        self.assertEqual(rows,[('GSM1',{'title':['a']})])


if __name__=='__main__':unittest.main()
