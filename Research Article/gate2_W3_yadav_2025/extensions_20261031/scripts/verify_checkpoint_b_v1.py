"""Independent source rereads: openpyxl for Table S1, explicit author-code mapping."""
import csv,json
from pathlib import Path
import openpyxl

ROOT=Path(__file__).resolve().parents[4]
CACHE=ROOT/'raw_data/Yd1_checkpoint_b_20261031'
RUNS=ROOT/'analysis/research/runs'

def rows(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def main():
    b1=RUNS/'Yd1_extension_b1_v1';b2=RUNS/'Yd1_extension_b2_v1'
    annotations=rows(b1/'author_code_annotation_vector.csv')
    expected=['Alveolar','Fibrotic','Alveolar','Inflammatory','Adventitial','Smooth muscle','Peribronchial','Stress-activated','Proliferating','Mesothelial','Pericyte']
    assert [r['label'] for r in annotations]==expected
    code=(CACHE/'Tsukui_integrate_by_MNN.R').read_text().splitlines()
    assert 'names(annotation) <- levels(MG)' in code[92]
    assert 'RenameIdents' in code[93]
    for row in rows(b1/'author_code_locators.csv'):assert code[int(row['line'])-1]==row['text']
    grid=rows(b1/'requested_state_support_grid.csv')
    coverage=rows(RUNS/'Yd1_extension_x0_v1/x3_sample_coverage.csv')
    expected_grid={(r['sample'],r['day'],s,r['pre_filter_barcodes']) for r in coverage for s in ['Alveolar','Inflammatory','Fibrotic']}
    assert len(grid)==36 and {(r['sample'],r['day'],r['proposed_author_label'],r['pre_filter_barcodes']) for r in grid}==expected_grid
    assert all(r[k]=='' for r in grid for k in ['author_retained_barcodes','author_state_cells','demultiplex_ambiguity'])
    book=openpyxl.load_workbook(CACHE/'SCAHN_supplementary_tables.xlsx',read_only=True,data_only=True)
    sheet=book['Table S1'];header=[c.value for c in sheet[2]][:10]
    source=[]
    for cells in sheet.iter_rows(min_row=3,max_col=10):
        v=[c.value for c in cells]
        if v[0] and isinstance(v[1],(int,float)) and isinstance(v[2],(int,float)):
            source.append(dict(source_sheet='Table S1',source_row=str(cells[0].row),**{key:'' if val is None else str(val) for key,val in zip(header,v)}))
    book.close()
    saved=rows(b2/'scahn_source_table.csv');assert saved==source
    summary=json.loads((b2/'source_qualification.json').read_text())
    assert summary['study_rows']==len(source)
    assert summary['reported_cell_sum']==sum(int(r['n_cells']) for r in source)
    assert summary['reported_sample_sum']==sum(int(r['n_samples']) for r in source)
    assert len(rows(b2/'lung_blood_source_screen.csv'))==sum('lung(' in r['tissue'] or 'peripheral blood(' in r['tissue'] for r in source)
    print(json.dumps(dict(annotation_positions_verified=len(annotations),support_grid_rows_verified=len(grid),table_S1_source_rows_verified=len(source),table_S1_source_fields_verified=len(source)*10,reported_cell_sum=summary['reported_cell_sum'],reported_sample_sum=summary['reported_sample_sum'],expression_extraction=False)))

if __name__=='__main__':main()
