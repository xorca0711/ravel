"""Artificial semantic regression: positive counts can have a zero-crossing range."""
import csv
import gzip
import json
from pathlib import Path
import tempfile
import unittest

from s5m_correct_flags_v2 import correct, flags, read_rows
from s5m_verify_flags_v2 import verify


def write_table(path, records):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'wt', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def fixture(root):
    source, output = root / 'v1', root / 'v2'
    source.mkdir(); output.mkdir()
    names = ['positive_crossing', 'zero_crossing', 'zero_non_crossing', 'positive_non_crossing']
    raw = {g: [100 + i for i in range(16)] for g in names}
    raw['zero_crossing'][0] = 0
    raw['zero_non_crossing'][13] = 0
    paths = []
    for i in range(16):
        path = root / ('GSM' + str(2440985+i) + '_artificial.tab.gz')
        with gzip.open(path, 'wt') as handle:
            for gene in names: handle.write(gene + '\t' + str(raw[gene][i]) + '\n')
        paths.append(path)
    records = []
    for i, gene in enumerate(names):
        r = dict(gene_id=gene, rna_any_zero_flag=str(i < 3), universe_primary='True', universe_all_mapped='True',
                 untouched_value='1.2345678901234567', rna_any_low_or_regularization_flag='False')
        for prefix, start in [('s2__D6', 0), ('s2__D30', 4), ('s4__B0', 4), ('s4__W6', 8), ('s4__W12', 12)]:
            values = raw[gene][start:start+4]
            r[prefix+'_zero_libraries'] = str(values.count(0))
            r[prefix+'_control_zero'] = str(values[:2] == [0,0])
            r[prefix+'_exposed_zero'] = str(values[2:] == [0,0])
            r[prefix+'_all_zero'] = str(values == [0,0,0,0])
        r['s4b__primary_reference_any_zero'] = 'False'
        r['s4b__c2_h2_reference_any_zero'] = 'False'
        r['s4b__c1_h1_reference_any_zero'] = 'False'
        r['s4__W6_adjustment_range_includes_zero'] = str(i < 2)
        r['s4__W12_adjustment_range_includes_zero'] = 'False'
        records.append(r)
    write_table(source/'gene_join.tsv.gz', records)
    write_table(source/'anchor_values.tsv', records[:2])
    manifest = [dict(gene_id=r['gene_id'], source_record_present=True, rna_any_zero_flag=True, plot_slot=i+1) for i,r in enumerate(records[:2])]
    (source/'anchor_manifest.json').write_text(json.dumps(manifest))
    block = dict(genes=4, unique_anchors=4, rna_any_zero_genes=3, rna_any_low_or_regularization_genes=0, atac_zero_flags={})
    (source/'universe_summary.json').write_text(json.dumps(dict(analysis_id='fixture_v1', gene_records=4, universes={u:dict(block) for u in ['primary','all_mapped']})))
    for name in ['gene_atac.tsv.gz','fig01_associations.png','fig01_associations.pdf']:
        (source/name).write_bytes(b'artificial immutable payload')
    for name in ['association_results.tsv','covariance_identity.tsv']:
        (source/name).write_text('coefficient\n0.125\n')
    return source, output, paths, records


class FlagCorrection(unittest.TestCase):
    def test_positive_counts_and_crossing_are_different(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output, paths, records = fixture(Path(tmp))
            self.assertTrue(all(int(line.split('\t')[1]) > 0 for p in paths for line in gzip.open(p,'rt') if line.startswith('positive_crossing\t')))
            self.assertEqual(flags(records[0]), (False, True))
            self.assertEqual(flags(records[1]), (True, True))
            self.assertEqual(flags(records[2]), (True, False))
            self.assertEqual(flags(records[3]), (False, False))
            extra = dict(records[3], arbitrary_zero_named_metric='True')
            self.assertEqual(flags(extra), (False, False))
            summary, manifest = correct(source, output, 'fixture_v2')
            checked = verify(source, output, paths)
            self.assertEqual(checked['status'], 'passed')
            self.assertEqual(checked['v1_false_positive_count_flags'], 1)
            self.assertFalse(manifest[0]['rna_any_count_zero_flag'])
            for b in summary['universes'].values():
                self.assertEqual(b['rna_any_count_zero_genes'], 2)
                self.assertEqual(b['rna_any_adjustment_range_includes_zero_genes'], 2)
                self.assertEqual(b['range_includes_zero_without_count_zero_genes'], 1)
            print(json.dumps({'artificial_verification':checked}), flush=True)

    def test_invalid_or_missing_declared_fields_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, _, _, records = fixture(Path(tmp))
            bad = dict(records[0]); del bad['s4__W12_all_zero']
            with self.assertRaises(KeyError): flags(bad)
            bad = dict(records[1]); bad['s4__W12_all_zero'] = 'NA'
            with self.assertRaises(ValueError): flags(bad)

    def test_copy_and_count_tampering_are_rejected(self):
        for field, replacement in [('rna_any_count_zero_flag','True'),('untouched_value','999')]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                source, output, paths, _ = fixture(Path(tmp))
                correct(source, output, 'fixture_v2')
                altered = list(read_rows(output/'gene_join.tsv.gz'))
                altered[0][field] = replacement
                write_table(output/'gene_join.tsv.gz', altered)
                with self.assertRaises(AssertionError): verify(source, output, paths)

    def test_coefficient_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output, paths, _ = fixture(Path(tmp))
            correct(source, output, 'fixture_v2')
            (output/'association_results.tsv').write_text('coefficient\n0.126\n')
            with self.assertRaises(AssertionError): verify(source, output, paths)


if __name__ == '__main__':
    unittest.main()
