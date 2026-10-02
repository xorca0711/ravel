"""RQ1: exact captured-mixture accounting for C3, without causal interpretation."""
import numpy as np
import pandas as pd
from rq_common import *


def main():
    options = args()
    out = begin('rq1_composition_v1')
    receipt = {}; rows = []; coverage = []; maps = []
    for m, counts, totals, mapping in atlases(options.source_root, ['C3'], receipt):
        maps.append({'cohort':m.cohort.iloc[0], 'assay':m.assay.iloc[0], 'mapping':mapping})
        if not mapping['C3']:
            raise ValueError('C3 missing')
        for key, a, b in strata(m):
            coverage.append(key)
            for floor in CFG['cell_floors']:
                if min(len(a),len(b)) < floor:
                    continue
                pa = counts[a,0]/totals[a]*1e6
                pb = counts[b,0]/totals[b]*1e6
                ma, mb = pa.mean(), pb.mean()
                p = len(b)/(len(a)+len(b))
                observed = np.concatenate([pa,pb]).mean()
                standard = (ma+mb)/2
                component = (p-.5)*(mb-ma)
                la, lb = counts[a,0].sum()/totals[a].sum()*1e6, counts[b,0].sum()/totals[b].sum()*1e6
                w = totals[b].sum()/(totals[a].sum()+totals[b].sum())
                bulk = (counts[a,0].sum()+counts[b,0].sum())/(totals[a].sum()+totals[b].sum())*1e6
                bulk_standard = (la+lb)/2
                bulk_component = (w-.5)*(lb-la)
                if not np.isclose(observed-standard,component,rtol=1e-10,atol=1e-9) or not np.isclose(bulk-bulk_standard,bulk_component,rtol=1e-10,atol=1e-9):
                    raise ValueError('Mixture identity failed')
                rows.append(key | {'cell_floor':floor,'captured_adventitial_fraction':p,
                    'alveolar_mean_cell_CPM':ma,'adventitial_mean_cell_CPM':mb,
                    'observed_cell_CPM':observed,'equal_subtype_cell_CPM':standard,
                    'composition_departure_cell_CPM':component,'library_adventitial_fraction':w,
                    'observed_bulk_CPM':bulk,'equal_subtype_bulk_CPM':bulk_standard,
                    'composition_departure_bulk_CPM':bulk_component,
                    'alveolar_bulk_CPM':la,'adventitial_bulk_CPM':lb})
    frame = pd.DataFrame(rows)
    if frame.empty: raise ValueError('No eligible strata')
    save(pd.DataFrame(coverage),out,'coverage.tsv'); save(frame,out,'stratum_accounting.tsv')
    fields=[c for c in frame.columns if c.endswith('CPM') or c.endswith('fraction')]
    donors=donor_average(frame,fields);save(donors,out,'donor_accounting.tsv')
    write_json(out/'gene_mapping.json',maps)
    write_json(out/'decision.json',{'biological_interaction':'not identifiable: no epithelial identity intervention or matched response',
        'executed':'exact equal-cell and library-weighted mixture accounting',
        'primary_donors_by_assay':donors[donors.cell_floor==20].groupby('assay').size().to_dict(),
        'normal_reference_only':True,'captured_fractions_are_tissue_abundance':False})
    finish(out,receipt,'composition accounting complete; epithelial interaction gate held')
    print(donors[donors.cell_floor==20][['assay','donor_id','captured_adventitial_fraction','observed_cell_CPM','equal_subtype_cell_CPM']].to_string(index=False),flush=True)


if __name__ == '__main__': main()
