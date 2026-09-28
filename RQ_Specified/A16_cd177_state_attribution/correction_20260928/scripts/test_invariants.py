"""Dependency-free contract tests; synthetic data only."""
import unittest
from c1_invariants import freeze_population, remaining_columns, quartiles, eligibility, effects
class InvariantTests(unittest.TestCase):
    def test_population_is_original_gate_and_library(self):
        rows=[{'gsm':g,'barcode':b,'primary_include':p,'gate_transition':t} for g,b,p,t in [('A','z',True,True),('A','a',True,True),('A','b',False,True),('A','c',True,False),('B','d',True,True)]]
        self.assertEqual([r['barcode'] for r in freeze_population(rows,'A')],['a','z'])
    def test_excluded_gene_perturbation_cannot_change_latent_or_depth_input(self):
        symbols=['Cd177','Lcn2','Cldn4','mt-X','GeneA','GeneB']; excluded={'Cd177','Lcn2','Cldn4'}
        keep=remaining_columns(symbols,excluded); self.assertEqual(keep,[4,5])
        a=[[1,2,3,4,5,6],[9,8,7,6,5,4]]; b=[r[:] for r in a]
        for row in b:
            for j in range(4): row[j]+=100000
        latent=lambda rows:[[r[j] for j in keep] for r in rows]
        self.assertEqual(latent(a),latent(b)); self.assertEqual([sum(r) for r in latent(a)],[sum(r) for r in latent(b)])
    def test_depth_ties_are_barcode_deterministic(self):
        self.assertEqual(quartiles([5]*4,['d','b','a','c']),[3,1,0,2])
    def test_one_unmatchable_positive_rejects_entire_k(self):
        pos=[True]*30+[False]*30; strata=[0]*29+[1]+[0]*30
        self.assertEqual(eligibility(pos,strata,5),'not_assessed_all_positives_not_matchable')
    def test_group_and_unique_control_floors(self):
        self.assertEqual(eligibility([True]*29+[False]*31,[0]*60,5),'not_assessed_group_floor')
        self.assertEqual(eligibility([True]*30+[False]*30,[0]*60,5,[31]*150),'not_assessed_unique_negative_floor')
    def test_common_effect_scale_and_no_dropped_positives(self):
        e=effects([3,5],[1,2],[2,2],[3,5,1,2])
        self.assertAlmostEqual(e['marginal_raw'],2.5); self.assertAlmostEqual(e['matched_raw'],2)
        self.assertAlmostEqual(e['marginal_standardized']*e['fixed_population_sd'],e['marginal_raw'])
        self.assertAlmostEqual(e['matched_standardized']*e['fixed_population_sd'],e['matched_raw'])
        with self.assertRaises(ValueError): effects([3,5],[1,2],[2],[3,5,1,2])
if __name__=='__main__': unittest.main()
