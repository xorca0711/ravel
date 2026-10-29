import importlib.util,sys,unittest
from pathlib import Path
import numpy as np
import pandas as pd
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location('external_obs',SCRIPTS/'external_human_observational_v1.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ExternalAggregationTests(unittest.TestCase):
    def setUp(self):
        self.genes=np.array(['A','B','ARG1','OTHER']);self.counts=np.array([[10,0,2,88],[0,10,0,990]])
        self.units=pd.DataFrame(dict(comp=['macrophages']*2,label=['Macrophages','Proliferating Macrophages'],donor=['D']*2,disease=['IPF']*2,cells=[60,10]))
        self.donors=pd.DataFrame(dict(Sample_Name=['D'],Diagnosis=['IPF'],Sample_Source=['Vanderbilt']))
        self.panels={'FABP4_panel':['A'],'matrix_mac_panel':['B']}
    def test_sum_counts_before_transform(self):
        t=m.aggregate(self.counts,self.genes,self.units,self.donors,self.panels).set_index('population')
        self.assertAlmostEqual(t.loc['external_macrophage_union','FABP4_panel'],np.log2(1+10/1100*1e6))
        self.assertEqual(t.loc['external_macrophage_union','all_gene_counts'],1100)
        self.assertEqual(t.loc['external_Macrophages_only','n_cells'],60)
    def test_missing_gene_is_not_zero(self):
        with self.assertRaisesRegex(ValueError,'symbol'):m.aggregate(self.counts,self.genes,self.units,self.donors,dict(FABP4_panel=['MISSING'],matrix_mac_panel=['B']))
    def test_conflicting_source_identity(self):
        with self.assertRaisesRegex(ValueError,'conflict'):m.aggregate(self.counts,self.genes,self.units,pd.concat([self.donors,self.donors]),self.panels)

if __name__=='__main__':unittest.main()
