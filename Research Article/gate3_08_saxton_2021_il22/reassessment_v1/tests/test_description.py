import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest
import sys
import xml.etree.ElementTree as ET
import numpy as np

PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE/'scripts'))
import describe_v1 as d
import plot_v1 as p


def fixture():
    annotations=[dict(geneID=f'G{i}',Gene_name=f'Gene{i}') for i in range(40)]
    sets=[dict(id=f'S{i}',members=[f'Gene{i*3+j}' for j in range(3)],source_kind='author_selected' if i<8 else 'external',
               role='synthetic',locator='synthetic',label=f'Set{i}') for i in range(10)]
    counts=np.arange(1,241).reshape(40,6)**2
    sizes,cpm,expression,eligible=d.primary_scale(counts)
    mapping,resolved,selected,tested=d.map_members(annotations,sets,eligible)
    background=eligible.copy();background[list(tested)]=False
    values=d.contrasts(expression,np.ones(6,dtype=bool))
    beta,_,_,status=d.amplitude_reference(values,background)
    summaries=[d.summarize_case(s,selected[s['id']],mapping,values,values[:,1]-beta*values[:,0],'CPM','full',status) for s in sets]
    ranges=[dict(scale=scale,membership=s['id'],metric=metric,full_data=float(i)/10-.5,n_omission_views=6,
                 omission_min=float(i)/10-.6,omission_max=float(i)/10-.3) for scale in d.SCALES for i,s in enumerate(sets) for metric in d.METRICS]
    return annotations,sets,mapping,expression,values,background,beta,summaries,ranges


class DescriptionTests(unittest.TestCase):
    def test_full_denominator_and_filter_boundary(self):
        counts=np.array([[1,1,0,0,0,0],[999999,999999,1000000,1000000,1000000,1000000]])
        sizes,cpm,expression,eligible=d.primary_scale(counts)
        np.testing.assert_equal(sizes,1000000);np.testing.assert_equal(eligible,[True,True])
        self.assertEqual(cpm[0,0],1);self.assertEqual(expression[0,0],1)
        with self.assertRaisesRegex(ValueError,'Zero'): d.primary_scale(np.zeros((2,6)))
        with self.assertRaisesRegex(ValueError,'Noninteger'): d.primary_scale(counts+.1)

    def test_mean_log_contrast_and_omission(self):
        expression=np.log2(np.array([[0,3,7,15,31,63]])+1)
        result=d.contrasts(expression,np.ones(6,dtype=bool))
        np.testing.assert_equal(result,[[2.5,4.5,2]])
        keep=np.array([False,True,True,True,True,True])
        np.testing.assert_equal(d.contrasts(expression[:,keep],keep),[[1.5,3.5,2]])
        self.assertNotAlmostEqual(result[0,0],np.log2((7+15)/2+1)-np.log2((0+3)/2+1))

    def test_mapping_does_not_collapse_or_zero_fill(self):
        ann=[dict(geneID=str(i),Gene_name=s) for i,s in enumerate(['A','B','B','C','D'])]
        sets=[dict(id='S',members=['A','B','C','MISSING'],source_kind='test',role='test',locator='test')]
        mapping,resolved,selected,tested=d.map_members(ann,sets,np.array([True,True,True,False,True]))
        self.assertEqual([r['status'] for r in mapping],['unique','ambiguous','unique','unmapped'])
        self.assertEqual(tested,{0,1,2,3});self.assertEqual(resolved['S'],{0,3})
        np.testing.assert_equal(selected['S'],[0]);self.assertEqual(mapping[1]['stable_ids'],'1;2')

    def test_amplitude_is_unclamped_and_hold_is_local(self):
        mask=np.ones(2,dtype=bool)
        for slope in (-2,3):
            values=np.array([[1,slope,0],[2,2*slope,0]])
            self.assertEqual(d.amplitude_reference(values,mask)[0],slope)
        self.assertEqual(d.amplitude_reference(np.zeros((2,3)),mask)[3],'held_zero_denominator')
        self.assertEqual(d.amplitude_reference(np.ones((2,3)),~mask)[3],'held_empty_background')

    def test_empty_summary_and_finite_scalar(self):
        item=dict(id='S',label='S',role='test')
        row=d.summarize_case(item,np.array([],dtype=int),[],np.zeros((2,3)),None,'CPM','full','held')
        self.assertEqual(row['status'],'no_eligible_members');self.assertIsNone(row['WT_minus_PBS'])
        self.assertIsNone(d.scalar(np.nan))

    def test_synthetic_tmm_scaled_identical_composition(self):
        with tempfile.TemporaryDirectory() as folder:
            output=Path(folder);counts=np.arange(1,101)[:,None]*np.arange(1,7)[None,:]
            d.write_csv(output/'counts_for_tmm.csv',[dict(geneID=f'G{i}',**dict(zip(d.LIBRARIES,map(int,row)))) for i,row in enumerate(counts)])
            factors,status=d.run_tmm(output,counts.sum(axis=0))
            self.assertEqual(status['status'],'qualified',status)
            self.assertEqual(len(factors),7)
            for values in factors.values(): np.testing.assert_allclose(values,1,atol=1e-12)

    def test_figures_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            p.render(Path(folder),*fixture())
            for name in ('published_targets','amplitude_reference','sensitivity_ranges'):
                svg=Path(folder)/(name+'.svg');ET.parse(svg)
                self.assertTrue(all(line==line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines()))
                self.assertGreater((Path(folder)/(name+'.png')).stat().st_size,1000)
            with self.assertRaises(FileExistsError): p.render(Path(folder),*fixture())


if __name__=='__main__':unittest.main()
