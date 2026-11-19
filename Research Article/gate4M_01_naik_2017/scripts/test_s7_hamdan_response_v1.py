"""Constructed data only. No actual Hamdan gene/count row is read by these tests."""
import csv
import gzip
import itertools
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from s7_hamdan_response_v1 import (calculate, factors, read_counts, response, sensitivity,
                                   source_metadata, summarize)
from s7_hamdan_verify_v1 import verify

ROOT = Path(__file__).resolve().parents[3]
ARTICLE = ROOT/'Research Article/ungated_naik_2017_inflammatory_memory'
PREP = ROOT/'raw_data/hamdan2026_s7_preparation_v1'


def fixture(directory):
    manifest = json.loads((ARTICLE/'S7_HAMDAN_SOURCE_MAP_V1.json').read_text())
    (directory/'map.json').write_text(json.dumps(manifest))
    # Keep every real identity/column name but replace ALL numeric source content.
    text = []
    for sample in manifest['samples']:
        text += ['^SAMPLE = '+sample['gsm'], '!Sample_title = '+sample['title'],
                 '!Sample_description = '+sample['column'], '!Sample_platform_id = '+sample['platform']]
    with gzip.open(directory/'soft.gz', 'wt') as handle: handle.write('\n'.join(text)+'\n')
    counts = np.array([[0]*8, [1]*8, [2, 4, 5, 7, 3, 9, 11, 12],
                       [0, 0, 8, 12, 20, 16, 30, 24], [9, 10, 2, 3, 15, 12, 8, 7],
                       [1, 2, 100, 90, 8, 12, 30, 20], [4, 8, 0, 0, 2, 5, 4, 9],
                       [101, 203, 800, 900, 101, 203, 1600, 1800]], dtype=np.int64)
    header = manifest['annotation_columns']+manifest['source_columns']
    generated = []
    for i, values in enumerate(counts):
        r = {key: '0' for key in header}
        r.update(GeneId='toy_gene_'+str(i), Chromosome='chrToy', Start=str(i*100), End=str(i*100+50),
                 Length='51', GeneName='duplicate_symbol' if i < 2 else 'toy_'+str(i), GeneBiotype='constructed')
        for patient in ['4', '83']:
            s = [s for s in manifest['samples'] if s['patient'] == patient]
            donor = values if patient == '4' else values[[1, 0, 3, 2, 5, 4, 7, 6]]
            for sample, value in zip(s, donor): r[sample['column']] = str(value)
        generated.append(r)
    with gzip.open(directory/'counts.gz', 'wt', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=header, delimiter='\t', lineterminator='\n')
        writer.writeheader(); writer.writerows(generated)
    return manifest, counts


class ScientificSemantics(unittest.TestCase):
    def test_monotonic_four_conditions_equal_increments(self):
        r = response(np.array([[0, 0, 1, 1, 3, 3, 7, 7]], float), np.ones(8)).iloc[0]
        self.assertEqual(r.P, 2); self.assertEqual(r.B, 2)
        self.assertEqual(r.R_I, 1); self.assertEqual(r.R_NI, 1); self.assertEqual(r.A, 0)

    def test_post_positive_interaction_negative(self):
        r = response(np.array([[0, 0, 3, 3, 7, 7, 15, 15]], float), np.ones(8)).iloc[0]
        self.assertEqual(r.P, 2); self.assertEqual(r.A, -1)

    def test_positive_interaction_can_mean_less_repression(self):
        f = response(np.array([[15, 15, 1, 1, 15, 15, 7, 7]], float), np.ones(8))
        self.assertEqual(f.A.iloc[0], 2)
        self.assertEqual(summarize(f)['A_positive_responses']['both_repressed'], 1)

    def test_mean_then_log_not_mean_log(self):
        f = response(np.array([[0, 8, 2, 4, 6, 7, 9, 10]], float), np.ones(8))
        self.assertAlmostEqual(f.e_NI0.iloc[0], np.log2(5))
        self.assertNotAlmostEqual(f.e_NI0.iloc[0], np.log2(9)/2)

    def test_exhaustive_cartesian_range(self):
        c = np.array([[0, 8, 2, 4, 6, 7, 9, 10]], float); sf = np.arange(1, 9)
        f = response(c, sf); e = np.log2(c[0]/sf+1)
        combos = [e[d]-e[c]-e[b]+e[a] for a, b, c, d in itertools.product([0, 1], [2, 3], [4, 5], [6, 7])]
        self.assertAlmostEqual(f.A_min.iloc[0], min(combos)); self.assertAlmostEqual(f.A_max.iloc[0], max(combos))

    def test_zeros_and_strata_use_only_raw_counts(self):
        f = response(np.array([[0]*8, [3]*8, [0, 2, 3, 3, 1, 2, 4, 4]], float), np.ones(8))
        s = summarize(f); self.assertEqual(s['eligible_count'], 2); self.assertEqual(s['structural_all_zero_count'], 1)
        self.assertEqual(s['raw_zero_strata']['any_raw_zero']['denominator'], 1)
        self.assertEqual(s['raw_zero_strata']['no_raw_zero']['denominator'], 1)
        self.assertTrue(f.A_range_zero.iloc[1]); self.assertFalse(f.any_raw_zero.iloc[1])
        for table in ['P_vs_A', 'R_NI_vs_R_I']:
            for cell, count in s['sign_tables'][table].items():
                self.assertEqual(count, sum(z['sign_tables'][table][cell] for z in s['raw_zero_strata'].values()))

    def test_empty_strata_and_conditional_fractions_are_null(self):
        s = summarize(response(np.ones((1, 8)), np.ones(8)))
        self.assertIsNone(s['post_positive_A']['1']['fraction'])
        self.assertTrue(all(v is None for table in s['raw_zero_strata']['any_raw_zero']['sign_fractions'].values() for v in table.values()))
        empty = summarize(response(np.zeros((1, 8)), np.ones(8)))
        self.assertIsNone(empty['quantiles']['A'])

    def test_even_median_ratios_and_depth_scaling(self):
        c = np.array([[1, 2, 3, 4, 5, 6, 7, 8], [9, 8, 7, 6, 5, 4, 3, 2]], float)
        result, _, n = factors(c)
        ratios = c/np.exp(np.log(c).mean(axis=1))[:, None]
        m = (ratios[0]+ratios[1])/2
        np.testing.assert_allclose(result['MOR'], m/np.exp(np.log(m).mean()), rtol=1e-13)
        depth = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        changed, _, _ = factors(c*depth)
        np.testing.assert_allclose(changed['MOR'], result['MOR']*depth/np.exp(np.log(depth).mean()), rtol=1e-13)
        self.assertEqual(n, 2)

    def test_empty_reference_stops(self):
        with self.assertRaisesRegex(ValueError, 'reference'): factors(np.eye(8))

    def test_normalization_sensitivity_preserves_universe(self):
        c = np.array([[1]*8, [20]*8, [0, 1, 3, 9, 8, 2, 30, 1]], float)
        sf, _, _ = factors(c); a, b = response(c, sf['MOR']), response(c, sf['total'])
        table, summary = sensitivity(a, b)
        self.assertEqual(len(table), 3); self.assertEqual(summary['eligible_count'], 3)
        self.assertGreater(np.abs(table.A_total_minus_MOR).max(), 0)


class SourceAndIndependentChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        PREP.mkdir(parents=True, exist_ok=True)
        cls.directory = Path(tempfile.mkdtemp(prefix='constructed_', dir=PREP)).resolve()
        if not cls.directory.is_relative_to(PREP.resolve()): raise AssertionError('Test path escaped preparation root')
        cls.manifest, cls.counts = fixture(cls.directory)
        cls.output = cls.directory/'output'; cls.output.mkdir()
        cls.frames = calculate(cls.directory/'counts.gz', cls.directory/'soft.gz', cls.manifest, cls.output)

    def test_complete_independent_reconstruction(self):
        receipt = verify(self.directory/'counts.gz', self.directory/'soft.gz', self.directory/'map.json', self.output)
        self.assertEqual(receipt['status'], 'passed'); self.assertEqual(receipt['source_genes'], 8)

    def test_changed_identity_and_count_failure(self):
        broken = json.loads(json.dumps(self.manifest)); broken['samples'][0]['column'] += '_wrong'
        with self.assertRaisesRegex(ValueError, 'identity'): source_metadata(self.directory/'soft.gz', broken)
        with gzip.open(self.directory/'counts.gz', 'rt') as h: text = h.read()
        lines = text.splitlines(); fields = lines[1].split('\t')
        selected_index = lines[0].split('\t').index(self.manifest['samples'][0]['column'])
        fields[selected_index] = '-1'; lines[1] = '\t'.join(fields)
        path = self.directory/'negative.gz'
        with gzip.open(path, 'wt') as h: h.write('\n'.join(lines)+'\n')
        with self.assertRaisesRegex(ValueError, 'nonnegative integers'): read_counts(path, self.manifest)

    def test_duplicate_gene_and_header_failure(self):
        with gzip.open(self.directory/'counts.gz', 'rt') as h: lines = h.read().splitlines()
        fields = lines[2].split('\t'); fields[0] = lines[1].split('\t')[0]; lines[2] = '\t'.join(fields)
        path = self.directory/'duplicate.gz'
        with gzip.open(path, 'wt') as h: h.write('\n'.join(lines)+'\n')
        with self.assertRaisesRegex(ValueError, 'duplicate'): read_counts(path, self.manifest)
        broken = json.loads(json.dumps(self.manifest)); broken['source_columns'][0] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'header'): read_counts(self.directory/'counts.gz', broken)

    def test_full_summary_mutation_is_detected(self):
        path = self.output/'summary.json'; original = path.read_bytes()
        data = json.loads(original); data['by_patient_method']['4_MOR']['raw_zero_strata']['any_raw_zero']['denominator'] += 1
        try:
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(AssertionError, 'denominator'):
                verify(self.directory/'counts.gz', self.directory/'soft.gz', self.directory/'map.json', self.output)
        finally: path.write_bytes(original)

    @classmethod
    def tearDownClass(cls):
        # Preserve constructed artifacts for review; never delete another run.
        from s7_hamdan_plot_v1 import plot
        plot(cls.frames, cls.output, constructed=True)
        print('Constructed evidence: '+str(cls.output))


if __name__ == '__main__': unittest.main()
