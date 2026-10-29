import importlib.util
from pathlib import Path
import unittest
import pandas as pd

spec=importlib.util.spec_from_file_location('hq',Path(__file__).resolve().parents[1]/'scripts/qualify_human_v1.py')
hq=importlib.util.module_from_spec(spec);spec.loader.exec_module(hq)

class HumanQualificationTests(unittest.TestCase):
    def sample(self):
        return pd.DataFrame({'CellBarcode_Identity':['a','b'],'Subject_Identity':['d1','d2'],
            'Library_Identity':['l1','l2'],'Disease_Identity':['Control','IPF'],
            'Manuscript_Identity':['Macrophage']*2,'Subclass_Cell_Identity':['Macrophage']*2,
            'CellType_Category':['Myeloid']*2,'nUMI':[1000,1200],'nGene':[500,600]})
    def test_valid_identity(self):hq.check_identity(self.sample(),['a','b'])
    def test_order_mismatch(self):
        with self.assertRaisesRegex(ValueError,'order mismatch'):hq.check_identity(self.sample(),['b','a'])
    def test_donor_disease_conflict(self):
        m=self.sample();m['Subject_Identity']='d'
        with self.assertRaisesRegex(ValueError,'more than one disease'):hq.check_identity(m,['a','b'])
    def test_library_donor_conflict(self):
        m=self.sample();m['Library_Identity']='l'
        with self.assertRaisesRegex(ValueError,'more than one donor'):hq.check_identity(m,['a','b'])
    def test_missing_metadata(self):
        m=self.sample();m.loc[0,'Manuscript_Identity']=None
        with self.assertRaisesRegex(ValueError,'Missing metadata'):hq.check_identity(m,['a','b'])

if __name__=='__main__':unittest.main()
