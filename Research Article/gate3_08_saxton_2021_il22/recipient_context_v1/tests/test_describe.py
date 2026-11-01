"""Synthetic endpoint and provenance checks; never open the real transcript matrix."""
import importlib.util
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import h5py
import numpy as np
from scipy.sparse import csr_matrix

spec = importlib.util.spec_from_file_location('describe', Path(__file__).parents[1] / 'scripts/describe_v1.py')
d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)


def fixture():
    libs = [d.LIBRARIES[0]] * 4 + [d.LIBRARIES[1], d.LIBRARIES[2]]
    states = ['hAT2', 'hAT2', 'unassigned', 'contaminant_immune', 'hAT2', 'hAT2']
    obs = {'barcode': np.array([f'cell{i}' for i in range(6)]),
           'library': np.array(libs), 'state': np.array(states),
           'gsm': np.array([d.LIBRARY_METADATA[x][0] for x in libs]),
           'timepoint': np.array([d.LIBRARY_METADATA[x][1] for x in libs])}
    selected = np.array([[1, 0], [1, 1], [0, 2], [1, 0], [0, 0], [2, 1]])
    totals = np.array([10, 90, 20, 30, 10, 20])
    cells = [{'sample_prefixed_cell_id' if key == 'barcode' else key: val[i]
              for key, val in obs.items()} for i in range(6)]
    counts = Counter(zip(libs, states)); composition = []
    for (lib, state), count in counts.items():
        n = libs.count(lib)
        excluded = sum(l == lib and s.startswith('contaminant_') for l, s in zip(libs, states))
        composition.append(dict(library=lib, state=state, count=count, post_doublet_cells=n,
                                contaminant_cells=excluded, alveolar_including_unassigned=n-excluded))
    return obs, selected, totals, cells, composition


class DescriptionTests(unittest.TestCase):
    def rows(self):
        return d.summarize(*fixture()[:3])

    def row(self, label, gene='Il22ra1', library=None):
        return next(r for r in self.rows() if r['library'] == (library or d.LIBRARIES[0])
                    and r['pipeline_label_or_aggregate'] == label and r['gene'] == gene)

    def test_ratio_of_sums_not_mean_of_normalized_cells(self):
        row = self.row('hAT2')
        self.assertEqual((row['n_cells'], row['n_detected'], row['gene_count_sum'], row['total_count_sum']),
                         (2, 2, 2, 100))
        self.assertEqual(row['counts_per_million_stratum_counts'], 20000)
        self.assertNotEqual(row['counts_per_million_stratum_counts'], (1/10 + 1/90)/2*1e6)

    def test_empty_is_unavailable_but_observed_zero_is_zero(self):
        empty = self.row('pAT2'); zero = self.row('hAT2', library=d.LIBRARIES[1])
        self.assertEqual(empty['n_cells'], 0)
        for key in ('n_detected', 'gene_count_sum', 'total_count_sum', 'detection_fraction',
                    'counts_per_million_stratum_counts', 'n_count_zero'):
            self.assertIsNone(empty[key])
        self.assertEqual(zero['n_cells'], 1)
        self.assertEqual(zero['gene_count_sum'], 0)
        self.assertEqual(zero['detection_fraction'], 0)

    def test_non_contaminant_keeps_unassigned(self):
        row = self.row('NON_CONTAMINANT')
        self.assertEqual((row['n_cells'], row['gene_count_sum'], row['total_count_sum']), (3, 2, 120))
        self.assertEqual(self.row('ALL_RETAINED')['n_cells'], 4)
        self.assertEqual(self.row('unassigned', 'Il10rb')['gene_count_sum'], 2)

    def test_all_strata_fixed_gene_order_and_count_bins(self):
        rows = self.rows()
        self.assertEqual(len(rows), 78)
        self.assertEqual([r['gene'] for r in rows], list(d.GENES) * 39)
        for r in rows:
            if r['n_cells']:
                self.assertEqual(r['n_count_zero'] + r['n_count_one'] + r['n_count_ge_two'], r['n_cells'])
                self.assertEqual(r['n_count_one'] + r['n_count_ge_two'], r['n_detected'])

    def test_exact_mapping_rejects_absent_alias_or_duplicate(self):
        self.assertEqual(d.gene_columns(np.array(['other', 'Il10rb', 'Il22ra1'])), [2, 1])
        for genes in (['IL22RA1', 'Il10rb'], ['Il22ra1', 'Il22ra1', 'Il10rb']):
            with self.assertRaises(ValueError): d.gene_columns(np.array(genes))

    def test_count_layer_totals_and_selected_values(self):
        matrix = csr_matrix([[1., 0., 9.], [1., 1., 88.]])
        selected, totals = d.count_metrics(matrix, [0, 1], np.array([10., 90.]))
        self.assertEqual(selected.tolist(), [[1, 0], [1, 1]])
        self.assertEqual(totals.tolist(), [10, 90])
        with self.assertRaises(ValueError): d.count_metrics(matrix, [0, 1], np.array([10, 91]))

    def test_invalid_count_values_and_duplicate_sparse_coordinates(self):
        for bad in (-1., .5, float('nan'), float('inf')):
            with self.assertRaises(ValueError): d.count_metrics(csr_matrix([[bad, 2.]]), [0, 1], [3])
        duplicate = csr_matrix((np.array([1., 2.]), np.array([0, 0]), np.array([0, 2])), shape=(1, 2))
        with self.assertRaises(ValueError): d.count_metrics(duplicate, [0, 1], [3])
        with self.assertRaises(ValueError): d.count_metrics(csr_matrix((1, 2)), [0, 1], [0])

    def test_ordered_metadata_join_and_denominator_rejections(self):
        obs, _, _, cells, composition = fixture()
        d.verify_metadata(obs, cells, composition)
        with self.assertRaises(ValueError): d.verify_metadata(obs, list(reversed(cells)), composition)
        composition[0]['alveolar_including_unassigned'] -= 1
        with self.assertRaises(ValueError): d.verify_metadata(obs, cells, composition)

    def test_nullable_strings_reject_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            with h5py.File(Path(temp)/'fixture.h5', 'w') as f:
                node = f.create_group('index'); node.attrs['encoding-type'] = 'nullable-string-array'
                node.create_dataset('values', data=['a', 'b'], dtype=h5py.string_dtype())
                node.create_dataset('mask', data=[False, False])
                self.assertEqual(d.strings(node).tolist(), ['a', 'b'])
                node['mask'][1] = True
                with self.assertRaises(ValueError): d.strings(node)

    def test_synthetic_plot_has_literal_labels_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp); d.render(self.rows(), out)
            self.assertEqual((out/'recipient_transcripts.png').read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
            svg = (out/'recipient_transcripts.svg').read_text(encoding='utf-8')
            for text in ('contaminant_endothelium', 'NON_CONTAMINANT', 'Il22ra1', 'Il10rb', 'NA'):
                self.assertIn(text, svg)
            with self.assertRaises(ValueError): d.render(self.rows(), out)


if __name__ == '__main__':
    unittest.main()
