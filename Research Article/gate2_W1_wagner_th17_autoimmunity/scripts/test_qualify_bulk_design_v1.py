"""Failure-boundary tests on synthetic data; no biological outcome exposure."""
import csv
import gzip
from pathlib import Path
import tempfile
import unittest
import qualify_bulk_design_v1 as q

def source_rows():
    rows=[]
    for series,animals,types in [(q.SERIES[0],['WT1','WT2','WT3'],['Th17p','Th17n','iTreg']),
        (q.SERIES[1],['WT1','WT2','WT3','WT4','JMJD3CKO1','JMJD3CKO2','JMJD3CKO3'],['Th17n','iTreg'])]:
        for animal in animals:
            for cell in types:
                for treatment in (['Vehicle','DFMO'] if series==q.SERIES[0] else ['ctrl','DFMO']):
                    for run in (['1','2'] if series==q.SERIES[0] else ['']):
                        title=f'{cell}_{treatment}_{animal}'+('_run'+run if run else '')
                        rows.append(dict(series=series,gsm='GSM'+str(len(rows)),title=title,animal_id=animal,cell_type=cell,
                                         treatment=treatment,run_id='run'+run if run else '',genotype='WT' if animal.startswith('WT') else 'JMJD3_KO'))
    return rows

class Boundaries(unittest.TestCase):
    def test_technical_runs_and_incomplete_pair(self):
        rows=source_rows();mapping,libraries=q.qualify(rows)
        self.assertEqual((len(mapping),len(libraries)),(64,46))
        with self.assertRaisesRegex(ValueError,'incomplete'):q.qualify(rows[1:])
    def test_duplicate_identity_and_metadata_conflict(self):
        rows=source_rows()
        with self.assertRaisesRegex(ValueError,'Duplicate GSM'):q.qualify(rows+[rows[0]])
        rows[0]['animal_id']='WT2'
        with self.assertRaisesRegex(ValueError,'disagreement'):q.qualify(rows)
    def test_genotype_main_effect_is_aliased(self):
        _,rows=q.qualify(source_rows());rows=[r for r in rows if r['series']==q.SERIES[1]]
        a,_=q.model(rows);b,_=q.model(rows,True)
        self.assertEqual((a['rank'],a['columns'],a['residual_df_if_fitted']),(13,13,15))
        self.assertEqual((b['rank'],b['columns']),(13,14))
    def test_matrix_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'m.csv.gz'
            for rows,error in [([['symbol','s'],['g','0.25']],None),([['symbol','s','s'],['g',1,2]],'header'),
                 ([['symbol','s'],['g','nan']],'Nonfinite'),([['symbol','s'],['g',-1]],'negative'),
                 ([['symbol','s'],['g',1],['g',2]],'Duplicate gene'),([['symbol','wrong'],['g',1]],'mismatch')]:
                with gzip.open(p,'wt',newline='') as f:csv.writer(f).writerows(rows)
                if error:
                    with self.assertRaisesRegex(ValueError,error):q.read_matrix(p,['s'])
                else:self.assertEqual(q.read_matrix(p,['s'])[2][0,0],0.25)

if __name__=='__main__':unittest.main()
