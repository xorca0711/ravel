import importlib.util
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location('qc_render', Path(__file__).parents[1]/'scripts/render_v1.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


def fixture_r1():
    qc = [dict(column=lib, total_counts=str(19000000 + 500000*i), genes_nonzero=str(19000+100*i),
               top10_count_fraction='0.06123456789') for i,lib in enumerate(r.ORDER)]
    return qc, [dict(column=lib) for lib in r.ORDER]


def fixture_x1():
    repeated = []
    for i in range(52):
        n = 2 if i < 48 else 3 if i < 51 else 17
        repeated.append(dict(symbol=f'synthetic_{i}', row_count=str(n), stable_id_count=str(n),
                             chromosome_count='1', strand_count='2' if i < 4 else '1',
                             locus_count=str(n) if i < 51 else '1',
                             biotype_count='2' if i < 18 else '1', description_count='2' if i < 23 else '1'))
    summary = dict(repeated_symbol_labels=52, rows_with_repeated_nonempty_symbols=122,
                   repeated_symbol_multiplicity={'2':48,'3':3,'17':1},
                   repeated_symbols_multiple_stable_ids=52, repeated_symbols_multiple_chromosomes=0,
                   repeated_symbols_multiple_strands=4, repeated_symbols_multiple_loci=51,
                   repeated_symbols_multiple_biotypes=18, repeated_symbols_multiple_descriptions=23)
    return summary, repeated


class RenderTests(unittest.TestCase):
    def test_source_order_and_exact_value_preservation(self):
        rows = r.r1_values(*fixture_r1())
        self.assertEqual([x['library'] for x in rows], list(r.ORDER))
        self.assertEqual(rows[0]['total_counts'], 19000000)
        self.assertEqual(rows[0]['largest_ten_fraction'], '0.06123456789')
        self.assertEqual(rows[0]['largest_ten_percent'], '6.12345678900')
        self.assertEqual(rows[0]['largest_ten_percent_display'], '6.1235%')

    def test_reordered_missing_or_duplicate_libraries_stop(self):
        qc, samples = fixture_r1()
        for changed in (qc[::-1], qc[:-1], qc[:-1]+[qc[0]]):
            with self.assertRaises(ValueError): r.r1_values(changed, samples)
        with self.assertRaises(ValueError): r.r1_values(qc, samples[::-1])

    def test_invalid_fraction_or_denominator_stops(self):
        for value in ('-0.1','1.1','NaN','Infinity'):
            qc, samples = fixture_r1(); qc[0]['top10_count_fraction']=value
            with self.assertRaises(ValueError): r.r1_values(qc, samples)
        qc, samples = fixture_r1(); qc[0]['total_counts']='0'
        with self.assertRaises(ValueError): r.r1_values(qc, samples)

    def test_multiplicity_and_overlapping_dimensions(self):
        rows = r.x1_values(*fixture_x1())
        self.assertEqual([x['count'] for x in rows[:3]], [48,3,1])
        self.assertEqual(sum(x['count'] for x in rows[:3]),52)
        self.assertEqual([x['count'] for x in rows[3:]], [52,0,4,51,18,23])
        self.assertGreater(sum(x['count'] for x in rows[3:]),52)
        self.assertEqual(rows[4]['display'],'0 / 52')
        self.assertTrue(all('synthetic_' not in str(x) for x in rows))

    def test_source_summary_disagreement_and_duplicates_stop(self):
        summary, repeated = fixture_x1(); summary['repeated_symbols_multiple_strands']=5
        with self.assertRaises(ValueError): r.x1_values(summary,repeated)
        summary, repeated = fixture_x1(); repeated[-1]['symbol']=repeated[0]['symbol']
        with self.assertRaises(ValueError): r.x1_values(summary,repeated)

    def test_invalid_metadata_cardinality_stops(self):
        summary,repeated = fixture_x1(); repeated[0]['chromosome_count']='0'
        with self.assertRaises(ValueError): r.x1_values(summary,repeated)

    def test_svg_cleaning_precedes_first_write(self):
        text='<svg xmlns="http://www.w3.org/2000/svg">  \n<path d="M 0 0 \nL 1 1  \n"/> \n</svg> \n'
        result=r.clean_svg(text)
        self.assertTrue(all(line==line.rstrip() for line in result.splitlines()))
        ET.fromstring(result)
        self.assertEqual(r.clean_svg(result),result)
        with self.assertRaises(ET.ParseError): r.clean_svg('<svg>')

    def test_figures_and_immutable_output_guard(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp); r.render_r1(r.r1_values(*fixture_r1()),out)
            r.render_x1(r.x1_values(*fixture_x1()),out)
            for stem in ('r1_library_qc','x1_annotation_qc'):
                self.assertEqual((out/(stem+'.png')).read_bytes()[:8],b'\x89PNG\r\n\x1a\n')
                text=(out/(stem+'.svg')).read_text(encoding='utf-8'); ET.fromstring(text)
                self.assertTrue(all(line==line.rstrip() for line in text.splitlines()))
            with self.assertRaises(ValueError):r.render_r1(r.r1_values(*fixture_r1()),out)


if __name__ == '__main__':
    unittest.main()
