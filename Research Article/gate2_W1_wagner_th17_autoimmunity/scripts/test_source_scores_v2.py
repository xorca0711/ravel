import unittest
import numpy as np
import pandas as pd
from source_scores_v2 import transform, contrasts, cluster_raw, pathway_summary
from verify_source_scores_v1 import scalar_test, bh


class ScoreTests(unittest.TestCase):
    def test_penalty_direction_and_constant_filter(self):
        scores,keep=transform(np.array([[1,2,3,4],[2,2,2,2.]]))
        self.assertEqual(keep.tolist(),[True,False])
        self.assertTrue(np.all(np.diff(scores[0])<0))

    def test_ties_and_direction_match_independent_arithmetic(self):
        a=[1.,1.,2.,4.];b=[1.,2.,3.,5.,5.]
        scores=np.array([a+b]);positive=np.array([True]*4+[False]*5)
        row=contrasts(scores,positive).iloc[0];d,u,p=scalar_test(a,b)
        np.testing.assert_allclose([row.cohens_d,row.U,row.p_source],[d,u,p],atol=1e-12)
        self.assertLess(d,0)

    def test_bh_not_unadjusted_and_not_input_order_dependent(self):
        np.testing.assert_allclose(bh([.04,.001,.03,.2]),[.0533333333333333,.004,.0533333333333333,.2])

    def test_constant_profiles_do_not_enter_correlation(self):
        raw=np.array([[1,2,3,4],[2,4,6,8],[4,3,2,1],[5,5,5,5.]])
        keep,labels=cluster_raw(raw)
        self.assertFalse(keep[-1]);self.assertEqual(labels[0],labels[1]);self.assertNotEqual(labels[0],labels[2])

    def test_pathways_do_not_count_duplicate_members_as_groups(self):
        rows=pd.DataFrame({'subsystem':['Glycolysis/gluconeogenesis']*8,'metareaction_id':[1]*4+[2]*4,'cohens_d':[1.]*4+[-.5]*4,'q_source':[.01]*8})
        p=pathway_summary(rows).iloc[0]
        self.assertEqual(p.metareaction_count,2);self.assertEqual(p.positive_q_lt_0_1,1);self.assertEqual(p.negative_q_lt_0_1,1)


if __name__=='__main__':unittest.main()
