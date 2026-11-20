"""Artificial source semantics and independent arithmetic/tamper regressions."""
import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest

import openpyxl
from s5f_reconstruct_v1 import read_workbooks,reconstruct,write_outputs
from s5f_verify_v1 import verify,xml_cells


def fixture(root):
    book=openpyxl.Workbook();book.remove(book.active)
    mapping={'endpoints':[],'contrasts':[]}
    for name,left,right,ref in [('Raw',[2,4,None,0],[3,6],False),('Reference',[1,1],[2,4],True),('Single',[0],[2],False)]:
        ws=book.create_sheet(name);ws['A1']='Artificial unit';ws['B1']='Ctrl';ws['C1']='PI'
        for col,values in [('B',left),('C',right)]:
            for row,value in enumerate(values,2):ws[col+str(row)]=value
        e=dict(id=name,workbook='1',sheet=name,title=name,unit='artificial units',kind='records',time='artificial',caption_n=3 if name=='Raw' else len(left),
               caption_n_relation='equal',biological_unit_note='Artificial only',header_guards=[{'cell':'A1','value':'Artificial unit'}],groups=[])
        for gid,col,values in [('Ctrl','B',left),('PI','C',right)]:
            e['groups'].append(dict(id=gid,label=gid,source_label=gid,label_cell=col+'1',expected_n=sum(v is not None for v in values),
                normalization_reference=ref and gid=='Ctrl',cells=[col+str(i) for i in range(2,2+len(values))]))
        mapping['endpoints'].append(e)
        mapping['contrasts'].append(dict(id=name+'_difference',endpoint=name,label='PI minus Ctrl',coefficients={'PI':1,'Ctrl':-1},
                                        leave_one_source_record_out=True,delete_normalization_references=False))
    ws=book.create_sheet('Rate');ws['A1']='Artificial rate summaries'
    e=dict(id='Rate',workbook='1',sheet='Rate',title='Artificial blockade counterexample',unit='day^-1',kind='reported_summary',time='artificial',
           caption_n=3,caption_n_relation='equal',biological_unit_note='Artificial only',header_guards=[{'cell':'A1','value':'Artificial rate summaries'}],groups=[])
    for gid,c,mean,se,n in [('CtrlIg',1,1,.1,3),('CtrlAnti',4,.5,.2,3),('OEIg',7,2,.3,4),('OEAnti',10,1,.4,4)]:
        cs=[openpyxl.utils.get_column_letter(c+i) for i in range(3)]
        ws[cs[0]+'2']=gid
        for x,label,value in zip(cs,['Mean','Std. Error','N'],[mean,se,n]):ws[x+'3']=label;ws[x+'4']=value
        e['groups'].append(dict(id=gid,label=gid,source_label=gid,label_cell=cs[0]+'2',expected_n=n,normalization_reference=False,
            mean_cell=cs[0]+'4',se_cell=cs[1]+'4',n_cell=cs[2]+'4',se_source_label='Std. Error'))
    mapping['endpoints'].append(e)
    for cid,coeff in [('OE_Ig',{'OEIg':1,'CtrlIg':-1}),('OE_Anti',{'OEAnti':1,'CtrlAnti':-1}),('effect_difference',{'OEAnti':1,'CtrlAnti':-1,'OEIg':-1,'CtrlIg':1})]:
        mapping['contrasts'].append(dict(id=cid,endpoint='Rate',label=cid,coefficients=coeff,leave_one_source_record_out=False,delete_normalization_references=False))
    path=root/'artificial.xlsx';book.save(path);book.close();out=root/'output';out.mkdir()
    return mapping,{'1':path},out


def replace_cell(path,column,value,index=0):
    with path.open(encoding='utf-8',newline='') as f:reader=csv.DictReader(f,delimiter='\t');fields=reader.fieldnames;rows=list(reader)
    rows[index][column]=value
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(rows)


class SourceReconstruction(unittest.TestCase):
    def test_all_artificial_arithmetic_and_semantics(self):
        with tempfile.TemporaryDirectory() as tmp:
            m,paths,out=fixture(Path(tmp));data=reconstruct(m,read_workbooks(m,paths));write_outputs(out,data)
            result=verify(m,paths,out);print(json.dumps({'artificial_verification':result}),flush=True)
            groups={(g['endpoint'],g['group']):g for g in data['groups']};cs={c['contrast']:c for c in data['contrasts']}
            self.assertEqual(groups['Raw','Ctrl']['source_n'],3)
            self.assertEqual(groups['Raw','Ctrl']['source_min'],0)
            self.assertEqual(sum(x['missing'] for x in data['observations']),1)
            self.assertEqual(cs['Raw_difference']['mean_contrast'],2.5)
            self.assertEqual(cs['Raw_difference']['median_contrast'],2.5)
            self.assertEqual((cs['Raw_difference']['deletion_count'],cs['Raw_difference']['deletion_min'],cs['Raw_difference']['deletion_max']),(5,1,4))
            self.assertIsNone(groups['Reference','Ctrl']['sample_sd'])
            self.assertEqual(groups['Reference','Ctrl']['dispersion_scope'],'normalization_reference_no_empirical_variance')
            self.assertEqual(cs['Reference_difference']['deletion_count'],2)
            self.assertEqual((cs['Reference_difference']['deletion_min'],cs['Reference_difference']['deletion_max']),(1,3))
            self.assertFalse(any(d['endpoint']=='Reference' and d['removed_group']=='Ctrl' for d in data['deletion_diagnostics']))
            self.assertEqual(cs['Single_difference']['deletion_count'],0)
            self.assertIsNone(cs['Single_difference']['deletion_min'])
            self.assertIsNone(groups['Rate','OEAnti']['sample_sd'])
            self.assertEqual(groups['Rate','OEAnti']['reported_se'],.4)
            self.assertEqual(groups['Rate','OEAnti']['caption_n_comparison'],'source_caption_N_discrepancy')
            # OE+anti equals Ctrl+Ig, but the within-anti OE effect is not zero.
            self.assertEqual(groups['Rate','OEAnti']['mean'],groups['Rate','CtrlIg']['mean'])
            self.assertEqual(cs['OE_Ig']['mean_contrast'],1)
            self.assertEqual(cs['OE_Anti']['mean_contrast'],.5)
            self.assertEqual(cs['effect_difference']['mean_contrast'],-.5)
            self.assertEqual(cs['OE_Anti']['deletion_scope'],'summary_only_no_individual_records')

    def test_wrong_N_header_reference_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            m,paths,out=fixture(Path(tmp));cache=read_workbooks(m,paths)
            wrong=copy.deepcopy(m);wrong['endpoints'][0]['groups'][0]['expected_n']=4
            with self.assertRaises(ValueError):reconstruct(wrong,cache)
            wrong=copy.deepcopy(m);wrong['endpoints'][0]['header_guards'][0]['value']='Wrong unit'
            with self.assertRaises(ValueError):reconstruct(wrong,cache)
            wrong=dict(cache);wrong['1','Reference','B2']=2
            with self.assertRaises(ValueError):reconstruct(m,wrong)

    def test_formula_rejected_by_both_source_readers(self):
        with tempfile.TemporaryDirectory() as tmp:
            m,paths,out=fixture(Path(tmp));wb=openpyxl.load_workbook(paths['1']);wb['Raw']['B2']='=1+1';wb.save(paths['1']);wb.close()
            with self.assertRaises(ValueError):read_workbooks(m,paths)
            with self.assertRaises(AssertionError):xml_cells(m,paths)

    def test_output_tampering_rejected(self):
        cases=[('contrasts.tsv','mean_contrast','999',0),('source_cells.tsv','value','changed',0),
               ('observations.tsv','missing','True',0),('groups.tsv','sample_sd','0',2)]
        for filename,column,value,index in cases:
            with self.subTest(filename=filename),tempfile.TemporaryDirectory() as tmp:
                m,paths,out=fixture(Path(tmp));write_outputs(out,reconstruct(m,read_workbooks(m,paths)))
                replace_cell(out/filename,column,value,index)
                with self.assertRaises(AssertionError):verify(m,paths,out)


if __name__=='__main__':unittest.main()
