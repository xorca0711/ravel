import importlib.util
import json
from pathlib import Path
import unittest
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location('render',ROOT/'scripts/presentation_figures_v1.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def fixtures(params):
    """Synthetic values with wide intervals and long source labels; no source read."""
    weights=[];mapping=[];full=[];robust=[]
    for i,d in enumerate(params['mappings']):
        key={k:d[k] for k in ['mapping_rule','distance_subset']}
        weights.append(dict(**key,pair_weighted_same=.55+i*.02,equal_gene_same=.554+i*.02,equal_gene_minus_pair_weighted=.004,
            mixed_atac_gene_fraction=.56 if i%2==0 else .09,mixed_atac_genes=7667 if i%2==0 else 632,genes=13602 if i%2==0 else 7067))
        for condition in ['IL4','CTRL']:mapping.append(dict(**key,condition=condition,pair_rows=63592-i*500,mapped_row_spearman=.01641 if condition=='IL4' else -.05243))
    for scope in params['human_scopes']:
        key=m.scope_key(scope)
        for panel in ['FABP4_panel','matrix_mac_panel']:
            value=.17 if panel=='FABP4_panel' else 2.3
            full.append(dict(**key,kind='contrast',group='IPF-Control',measure=panel,n_first=32,n_second=28,
                estimate=value,original_ci_low=value-.8,original_ci_high=value+.9))
        full.append(dict(**key,kind='association',group='IPF',measure='FABP4_vs_matrix',n_first=32,n_second=32,
            estimate=-.6,original_ci_low=-.9,original_ci_high=.1))
        for mode in ['leave_component_out','leave_donor_out']:
            robust.append(dict(**key,kind='association',group='IPF',measure='FABP4_vs_matrix',diagnostic=mode,reference=-.6,minimum=-.7,maximum=-.4))
    return {'weighting':pd.DataFrame(weights),'mapping':pd.DataFrame(mapping),'full':pd.DataFrame(full),'robustness':pd.DataFrame(robust)}


class PresentationFigures(unittest.TestCase):
    def setUp(self):self.params=json.loads((ROOT/'config/presentation_parameters_v1.json').read_text())
    def test_all_four_layout_fixtures(self):
        tables=fixtures(self.params);audit=m.Audit(tables,self.params['sources'])
        for builder in m.BUILDERS:
            fig,caption=builder(tables,self.params,audit)
            try:self.assertTrue(m.layout_check(fig,caption)['text_inside_canvas'])
            finally:plt.close(fig)
    def test_nonfinite_value_rejected(self):
        audit=m.Audit({'x':pd.DataFrame([{'id':'a','value':float('nan')}])},{'x':'fixture'})
        with self.assertRaisesRegex(ValueError,'Undefined'):audit.number('x',{'id':'a'},'value')
    def test_ambiguous_selection_rejected(self):
        with self.assertRaisesRegex(ValueError,'one source row'):m.unique_row(pd.DataFrame([{'id':'a'},{'id':'a'}]),{'id':'a'})
    def test_source_coordinate_disagreement_rejected(self):
        audit=m.Audit({'x':pd.DataFrame([{'id':'a','value':.2}])},{'x':'fixture'});r=audit.number('x',{'id':'a'},'value')
        fig,ax=plt.subplots();line,=ax.plot([.3],[0])
        try:
            with self.assertRaisesRegex(ValueError,'coordinate mismatch'):audit.line(line,[r])
        finally:plt.close(fig)
    def test_original_interval_and_range_are_separate(self):
        tables=fixtures(self.params);audit=m.Audit(tables,self.params['sources']);fig,caption=m.human_coupling(tables,self.params,audit)
        try:
            self.assertTrue(all(tuple(ax.get_xlim())==(-1.,1.) for ax in fig.axes))
            self.assertIn('not confidence intervals',caption.get_text())
            self.assertEqual([x['source'] for x in audit.values if x['column']=='original_ci_high'],[self.params['sources']['full']]*2)
        finally:plt.close(fig)


if __name__=='__main__':unittest.main()
