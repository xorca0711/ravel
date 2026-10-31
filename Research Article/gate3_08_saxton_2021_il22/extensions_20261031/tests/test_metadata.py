import copy
import csv
import gzip
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET


def load(name):
    path = Path(__file__).parents[1] / 'scripts' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


a = load('annotation_v1')
p = load('provenance_v1')


def record(gene='ENSMUSG001', symbol='alias'):
    return dict(row_index=1, geneID=gene, Gene_name=symbol, Chrom='chr1', Strand='+',
                Start='1', End='10', GeneLength='5', Gene_type='source_type', Description='source label')


def sources():
    attrs = {'source_name': ['colon'], 'tissue': ['colon'], 'strain': ['source_strain'], 'treatment': ['source_label']}
    geo = [dict(gsm='GSM1', title='sample1', biosample='SAMN1', experiment='SRX1', attributes=attrs)]
    bs = ET.fromstring('<BioSampleSet><BioSample accession="SAMN1"><Description><Title>sample1</Title></Description><Ids><Id db="GEO">GSM1</Id><Id db="SRA">SRS1</Id></Ids><Attributes/></BioSample></BioSampleSet>')
    sra = ET.fromstring('''<EXPERIMENT_PACKAGE_SET><EXPERIMENT_PACKAGE>
      <EXPERIMENT accession="SRX1" alias="GSM1"><DESIGN><SAMPLE_DESCRIPTOR accession="SRS1"><IDENTIFIERS><EXTERNAL_ID namespace="GEO">GSM1</EXTERNAL_ID></IDENTIFIERS></SAMPLE_DESCRIPTOR><LIBRARY_DESCRIPTOR><LIBRARY_LAYOUT><PAIRED/></LIBRARY_LAYOUT></LIBRARY_DESCRIPTOR></DESIGN></EXPERIMENT>
      <SAMPLE accession="SRS1"><TITLE>sample1</TITLE><IDENTIFIERS><EXTERNAL_ID namespace="GEO">GSM1</EXTERNAL_ID><EXTERNAL_ID namespace="BioSample">SAMN1</EXTERNAL_ID></IDENTIFIERS><SAMPLE_ATTRIBUTES/></SAMPLE>
      <RUN_SET><RUN accession="SRR1" alias="GSM1_r1"><EXPERIMENT_REF accession="SRX1"/><Pool><Member accession="SRS1"><IDENTIFIERS><EXTERNAL_ID namespace="GEO">GSM1</EXTERNAL_ID><EXTERNAL_ID namespace="BioSample">SAMN1</EXTERNAL_ID></IDENTIFIERS></Member></Pool></RUN></RUN_SET><SUBMISSION accession="SRA1"/>
      </EXPERIMENT_PACKAGE></EXPERIMENT_PACKAGE_SET>''')
    for key, value in attrs.items():
        ET.SubElement(bs.find('.//Attributes'), 'Attribute', attribute_name=key).text = value[0]
        n = ET.SubElement(sra.find('.//SAMPLE_ATTRIBUTES'), 'SAMPLE_ATTRIBUTE')
        ET.SubElement(n, 'TAG').text = key
        ET.SubElement(n, 'VALUE').text = value[0]
    return geo, bs, sra


class AnnotationTests(unittest.TestCase):
    def test_opaque_expression_is_never_selected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'source.gz'
            with gzip.open(path, 'wt', newline='') as stream:
                writer = csv.writer(stream, delimiter='\t')
                writer.writerow(['expression', *a.FIELDS])
                writer.writerow(['THIS IS NOT A NUMBER', *[record()[k] for k in a.FIELDS]])
            rows = a.annotations(path)
        self.assertEqual(rows, [record()])
        self.assertNotIn('expression', rows[0])

    def test_missing_annotation_field_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'source.gz'
            with gzip.open(path, 'wt') as stream:
                stream.write('geneID\texpression\nENSMUSG1\t3\n')
            with self.assertRaises(ValueError):
                a.annotations(path)

    def test_annotation_disagreement_rejected(self):
        left, right = [record()], [record()]
        right[0]['Chrom'] = 'chr2'
        with self.assertRaises(ValueError):
            a.compare_annotations(left, right)

    def test_versions_are_diagnosed_not_collapsed(self):
        rows = [record('ENSMUSG001.1'), record('ENSMUSG001.2')]
        repeated, summary = a.summarize(rows)
        self.assertEqual(len(rows), 2)
        self.assertEqual(summary['version_suffixed_rows'], 2)
        self.assertEqual(summary['repeated_stable_id_labels'], 1)
        self.assertEqual(repeated[0]['stable_id_count'], 1)


class ProvenanceTests(unittest.TestCase):
    def test_sequencing_pair_and_member_do_not_certify_animals(self):
        rows, detail, fields = p.join_records(*sources())
        self.assertEqual(rows[0]['library_layout'], 'PAIRED')
        self.assertEqual(rows[0]['animal_pairing'], 'not established')
        self.assertEqual(rows[0]['biological_independence'], 'unknown')
        self.assertEqual(len(detail[0]['runs'][0]['sample_members']), 1)

    def test_wrong_cross_reference_rejected(self):
        geo, bs, sra = sources()
        sra.find('.//SAMPLE/IDENTIFIERS/EXTERNAL_ID[@namespace="BioSample"]').text = 'SAMN2'
        with self.assertRaises(ValueError):
            p.join_records(geo, bs, sra)

    def test_duplicate_experiment_rejected(self):
        geo, bs, sra = sources()
        sra.append(copy.deepcopy(sra[0]))
        with self.assertRaises(ValueError):
            p.join_records(geo, bs, sra)

    def test_candidate_unit_field_is_preserved_not_certified(self):
        geo, bs, sra = sources()
        ET.SubElement(bs.find('.//Attributes'), 'Attribute', attribute_name='animal_id').text = 'reported_mouse'
        rows, detail, fields = p.join_records(geo, bs, sra)
        self.assertEqual(rows[0]['source_unit_attribute_candidates'], 1)
        self.assertEqual(rows[0]['biological_independence'], 'unknown')
        self.assertEqual(detail[0]['unit_attribute_candidates'][0]['values'], ['reported_mouse'])


if __name__ == '__main__':
    unittest.main()
