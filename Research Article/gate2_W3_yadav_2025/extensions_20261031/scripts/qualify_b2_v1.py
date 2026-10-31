"""B2: only SCAHN Table S1 source metadata; no gene-expression extraction."""
import argparse,json,re,zipfile,xml.etree.ElementTree as E
from common_v1 import ROOT,EXT,read_csv,save_csv,save_json,sha
CACHE=ROOT/'raw_data/Yd1_checkpoint_b_20261031'
def table_one(path,sheet_name):
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path) as z:
        strings=[''.join(n.itertext()) for n in E.fromstring(z.read('xl/sharedStrings.xml'))]
        rel={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheets=E.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',ns)
        match=[s for s in sheets if s.get('name')==sheet_name];assert len(match)==1
        target=rel[match[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
        x=E.fromstring(z.read(target.lstrip('/') if target.startswith('/') else 'xl/'+target))
        out={}
        for c in x.findall('.//s:sheetData/s:row/s:c',ns):
            ref=c.get('r');v=c.findtext('s:v',namespaces=ns);typ=c.get('t','n')
            if typ=='s' and v is not None:v=strings[int(v)]
            elif typ=='inlineStr':v=''.join(c.find('s:is',ns).itertext())
            if v is not None:out[ref]=v
        return out,[s.get('name') for s in sheets]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    out=ROOT/a.output;out.mkdir(exist_ok=True,parents=True)
    spec=json.loads((EXT/'config/checkpoint_b_spec_v1.json').read_text())
    book=CACHE/'SCAHN_supplementary_tables.xlsx';cells,sheets=table_one(book,spec['X5_sheet'])
    cols=spec['X5_columns'];assert [cells[chr(65+i)+'2'] for i in range(10)]==cols
    maxrow=max(int(re.search(r'\d+',key).group()) for key in cells);rows=[];nonstudy=[]
    for n in range(3,maxrow+1):
        values=[cells.get(chr(65+i)+str(n),'') for i in range(10)]
        if not any(values):continue
        if not(values[0] and re.fullmatch(r'\d+',values[1]) and re.fullmatch(r'\d+',values[2])):
            nonstudy.append(dict(row=n,values=values));continue
        row=dict(source_sheet=spec['X5_sheet'],source_row=n,**dict(zip(cols,values)))
        rows.append(row)
    assert len({r['pid'] for r in rows})==len(rows)
    save_csv(out/'scahn_source_table.csv',rows)
    screen=[]
    for r in rows:
        if 'lung(' in r['tissue'] or 'peripheral blood(' in r['tissue']:
            screen.append(dict(pid=r['pid'],source_row=r['source_row'],tissue=r['tissue'],group=r['group'],technique=r['technique'],DOI=r['DOI'],n_samples_reported=r['n_samples'],healthy_component_listed=int('healthy(' in r['group']),joint_tissue_condition_known='no; table supplies marginals',individual_sample_ids='absent',donor_ids='absent',whole_blood_or_PBMC='not resolved by technique',raw_counts_and_gene_measurement='not qualified',eligibility='source lead only'))
    save_csv(out/'lung_blood_source_screen.csv',screen)
    overlap=[]
    for target in spec['publication_reuse']:
        found=[r for r in rows if r['pid'].lower()==target.lower()]
        overlap.append(dict(parent=target,direct_table_match=';'.join(r['pid'] for r in found),source_rows=';'.join(str(r['source_row']) for r in found),status='direct study-level inclusion; sample/donor overlap unjoined' if found else 'no standalone row; indirect overlap not excluded',repository_relation='Salcher source reused in Yadav; Adams/Habermann are Ravel inputs and Salcher parent sources'))
    save_csv(out/'parent_overlap_map.csv',overlap)
    faq=json.loads((CACHE/'scahn_browser_observation_v1.json').read_text())
    assert 'salcher2022' in faq['faq']['multi_dataset_studies']
    save_json(out/'source_qualification.json',dict(workbook_sha256=sha(book),sheet_read=spec['X5_sheet'],other_sheets_values_read=False,workbook_sheet_names=sheets,study_rows=len(rows),reported_cell_sum=sum(int(r['n_cells']) for r in rows),reported_sample_sum=sum(int(r['n_samples']) for r in rows),screened_lung_or_blood_rows=len(screen),nonstudy_rows=nonstudy,FAQ_source=faq['source'],source_table_recovered=True,source_table_contains_accession_column=False,individual_sample_or_donor_crosswalk=False,gene_measurement_mask_available=False,all_zero_cells_qualified=False,unmeasured_gene_encoding='FAQ: a gene not measured in a source is encoded as zero for all source cells',healthy_whole_blood_design='not executable until specific source/preparation/donor/measurement-mask/raw-count joins qualify; no expression query run',atlas_downloaded=False,expression_values_extracted=False,scientific_acceptance='not_assessed'))
    print('B2 Table S1 source rows, source screen and parent overlap recovered; expression prerequisites remain held')
if __name__=='__main__':main()
