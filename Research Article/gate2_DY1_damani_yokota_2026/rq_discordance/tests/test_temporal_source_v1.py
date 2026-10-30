from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from temporal_source_v1 import memory_column, rna2020_column


class TemporalSourceTests(unittest.TestCase):
    def test_history_and_current_exposure_are_separate(self):
        self.assertEqual(memory_column('mm_BMDM_Wt_1st_stim_3hIL4_RNA_rep1'), 'WT_ctrl_3h_IL4')
        self.assertEqual(memory_column('mm_BMDM_Wt_2nd_stim_ctrl_RNA_rep2'), 'WT_IL4_pre_0h')
        self.assertEqual(memory_column('mm_BMDM_PpargKO_2nd_stim_3hIL4_RNA_rep1'), 'KO_IL4_pre_3h_IL4')

    def test_other_source_context_not_forced_into_memory(self):
        self.assertIsNone(memory_column('mm_BMDM_24hIL4pVeh_RNA_rep1'))
        self.assertIsNone(memory_column('muscle_day4_Ly6C_low_rep1'))

    def test_rna2020_header_uses_metadata_not_flox_title_alone(self):
        sample = dict(characteristics_ch1=['genotype: Egr2KO', 'treatment: ctrl'], title=['Egr2fl/fl unstimulated BMDM RNA-seq replicate 3'])
        self.assertEqual(rna2020_column(sample), 'mm_BMDM_Egr2KO_ctrl_24h_rep3')


if __name__ == '__main__': unittest.main()
