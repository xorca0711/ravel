import importlib.util
from pathlib import Path
import unittest
import pandas as pd

spec=importlib.util.spec_from_file_location('audit',Path(__file__).parents[1]/'scripts/representation_audit_v1.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class RepresentationAudit(unittest.TestCase):
    def fixture(self):
        rows=[]
        for rule in ['author_ensembl','author_nearest_tss_symbol']:
            for peak,gene,a,r in [('p1','g1',1,1),('p2','g1',-1,1),('p3','g1',0,1),('p4','g2',-1,-1)]:
                cls='zero' if a==0 else ('same' if a*r>0 else 'opposite')
                rows.append(dict(mapping_rule=rule,distance_subset='all',peak_id=peak,gene_id=gene,atac_delta=a,rna_delta=r,atac_sign=a,rna_sign=r,direction_class=cls))
        return pd.DataFrame(rows)

    def test_unequal_representation_and_zero(self):
        g,s=m.aggregate(self.fixture())
        self.assertEqual(s.iloc[0].pair_weighted_same,.5)
        self.assertAlmostEqual(s.iloc[0].equal_gene_same,2/3)
        self.assertEqual(s.iloc[0].mixed_atac_genes,1)
        self.assertEqual(g.iloc[0].zero,1)

    def test_mapping_disagreement(self):
        d=self.fixture();i=(d.mapping_rule=='author_nearest_tss_symbol')&(d.peak_id=='p1')
        d.loc[i,'gene_id']='g3';d.loc[i,'direction_class']='opposite';d.loc[i,'rna_delta']=-1;d.loc[i,'rna_sign']=-1
        c,t=m.common_mapping(d);g,s=m.aggregate(d)
        self.assertEqual(int((~c.same_gene).sum()),1);self.assertEqual(int((~c.same_class).sum()),1)
        self.assertGreater(m.scalar_verify(d,g,s,c),0)

    def test_join_loss_rejected(self):
        members=pd.DataFrame([dict(mapping_rule='x',distance_subset='all',peak_id='p',gene_id='missing')])
        with self.assertRaisesRegex(ValueError,'lost'):
            m.attach_effects(members,pd.DataFrame({'feature_id':['g'],'mean_delta':[1]}),pd.DataFrame({'feature_id':['p'],'mean_delta':[1]}))

    def test_duplicate_region_rejected(self):
        d=self.fixture()[['mapping_rule','distance_subset','peak_id','gene_id']]
        d=pd.concat([d,d.iloc[:1]])
        with self.assertRaisesRegex(ValueError,'Repeated'):
            m.attach_effects(d,pd.DataFrame(),pd.DataFrame())


if __name__=='__main__':unittest.main()
