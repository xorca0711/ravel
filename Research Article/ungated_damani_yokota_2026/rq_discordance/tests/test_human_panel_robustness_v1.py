import importlib.util
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
s=importlib.util.spec_from_file_location('robustness',Path(__file__).parents[1]/'scripts/human_panel_robustness_v1.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class PanelRobustness(unittest.TestCase):
    def test_panel_omission_renormalizes(self):
        d=pd.DataFrame({'gene_a':[1.],'gene_b':[3.],'gene_c':[8.],'gene_d':[12.]})
        self.assertEqual(m.panel_values(d,list('abcd'))[0],6)
        self.assertEqual(m.panel_values(d,list('abcd'),'d')[0],4)
    def test_floor_crossing_is_held(self):
        x=np.arange(8.);self.assertAlmostEqual(m.estimate(x,x,'association')[0],1)
        self.assertEqual(m.estimate(x[:-1],x[:-1],'association')[1],'fewer_than_8_donors')
    def test_nonfinite_component_rejected(self):
        for bad in [np.nan,np.inf,-np.inf]:
            d=pd.DataFrame({'gene_a':[1.],'gene_b':[bad],'gene_c':[8.],'gene_d':[12.]})
            with self.assertRaisesRegex(ValueError,'nonfinite'):m.panel_values(d,list('abcd'))
            with self.assertRaisesRegex(ValueError,'nonfinite'):m.panel_values(d,list('abcd'),'d')
    def test_undefined_reference_is_not_zero_reversals(self):
        r=pd.DataFrame([dict(cohort='x',population='x',floor=50,scope='Vanderbilt',kind='association',measure='panels',group='IPF',diagnostic='leave_component_out',estimate=.2,reference=np.nan,change=np.nan)])
        s=m.summarize_omissions(r).iloc[0]
        self.assertEqual(s.omissions,1);self.assertEqual(s.estimable,1)
        self.assertTrue(np.isnan(s.strict_sign_reversals));self.assertTrue(np.isnan(s.maximum_absolute_change))
        self.assertEqual(s.comparison_status,'reference_unavailable')
    def test_ties_and_constant(self):
        x=np.array([0,0,1,1,2,2,3,3.]);self.assertAlmostEqual(m.estimate(x,-x,'association')[0],-1)
        self.assertEqual(m.estimate(x,np.ones(8),'association')[1],'constant_variable')
    def test_all_donors_and_components_retained(self):
        d=pd.DataFrame({'donor':[str(i) for i in range(18)],'disease':['Control']*9+['IPF']*9})
        panels={'FABP4_panel':['a','b','c','d'],'matrix_mac_panel':['e','f','g','h']}
        for i,g in enumerate('abcdefgh'):d['gene_'+g]=np.arange(18.)+i
        r=m.diagnostics(d,panels,dict(cohort='GSE135893',population='mock',floor=50,scope='all_sources'))
        self.assertEqual(len(r[r.diagnostic=='full']),4)
        self.assertEqual(len(r[r.diagnostic=='leave_component_out']),24)
        self.assertEqual(len(r[r.diagnostic=='leave_donor_out']),54)

if __name__=='__main__':unittest.main()
