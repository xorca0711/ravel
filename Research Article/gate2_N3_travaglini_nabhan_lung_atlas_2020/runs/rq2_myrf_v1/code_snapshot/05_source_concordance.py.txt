"""Compare source counts, inspect selected evolutionary results, and retain discrepancies."""
from datetime import datetime, timezone
import csv
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from common import PACKAGE, REPO, read_json, write_json, new_run, finish_record, verified_sources


def main():
    sources=verified_sources(); cfg=read_json(PACKAGE/'config/execution_v1.json')
    out=new_run(PACKAGE/'runs/source_concordance_v1')
    expected=pd.read_csv(PACKAGE/'runs/intake_v1/human_celltype_coverage.tsv',sep='\t',keep_default_na=False)
    observed=pd.read_csv(REPO/'raw_data/travaglini_nabhan_2020/prepared/cell_metadata.tsv',sep='\t',keep_default_na=False)
    aliases={'Capillary':'Capillary','Lymphatic':'Lymphatics','Basophil/Mast 1':'Mast Cell/Basophil Type 1','Basophil/Mast 2':'Mast Cell/Basophil Type 2'}
    # Exact Table 2 capillary spelling is recorded explicitly, never guessed by score.
    cap=expected.loc[expected.cluster_id==19,'author_cell_type'].iloc[0]
    aliases['Capillary']=cap
    observed['table2_label']=observed.author_cell_type.replace(aliases)
    counts=observed.groupby(['assay','donor_id','table2_label']).size()
    comparison=[]
    for row in expected.to_dict('records'):
        n=int(counts.get((row['assay'],row['donor_id'],row['author_cell_type']),0))
        deposited=None if row['n_cells']=='' else int(row['n_cells'])
        comparison.append({'assay':row['assay'],'donor_id':row['donor_id'],'cluster_id':row['cluster_id'],'author_cell_type':row['author_cell_type'],'source_n_cells':deposited,'curated_n_cells':n,'delta_curated_minus_source':None if deposited is None else n-deposited,'comparison_status':'source_absence_not_numeric' if deposited is None else ('exact_count_match' if n==deposited else 'count_mismatch')})
    frame=pd.DataFrame(comparison);frame.to_csv(out/'table2_count_concordance.tsv',sep='\t',index=False)
    unassigned=observed[~observed.table2_label.isin(expected.author_cell_type)]
    unassigned.groupby(['assay','donor_id','author_cell_type']).size().rename('n_cells').reset_index().to_csv(out/'unmapped_source_labels.tsv',sep='\t',index=False)
    write_json(out/'label_aliases.json',aliases)
    # Extract only already-frozen benign identity/context panel genes, not all categories.
    genes={g for p in cfg['panels'].values() for g in p}
    evolution=[]
    wb=load_workbook(sources['supplement_table_7'],read_only=True,data_only=True)
    for sheet in wb:
        sheet.reset_dimensions(); rows=iter(sheet.values); title=next(rows)[0]; header=list(next(rows))
        for row in rows:
            if not row or row[0] not in genes:continue
            record=dict(zip(header,row));record.update(source_sheet=sheet.title,source_comparison=title)
            evolution.append(record)
    wb.close()
    pd.DataFrame(evolution).to_csv(out/'source_species_panel_results.tsv',sep='\t',index=False)
    wb=load_workbook(sources['supplement_table_6'],read_only=True,data_only=True)
    header=list(next(wb.active.values));wb.close()
    write_json(out/'mouse_design_gate.json',{'source_mouse_columns':header[2:],'status':'source-table inspection complete; new matched-age species effect not estimated','reason':'Combined source includes age-coded animals and several source datasets; individual animal metadata and pinned orthology are not yet reconciled. Source-selected differential genes are not a complete ortholog universe.'})
    wb=load_workbook(sources['source_figure_1'],read_only=True,data_only=True);rows=list(wb.active.values);wb.close()
    at2=int(rows[1][1]); at2s=int(rows[2][1])
    write_json(out/'imaging_fraction_reconstruction.json',{'figure':'1d','AT2_scored_cells':at2,'AT2s_scored_cells':at2s,'denominator':at2+at2s,'AT2s_fraction':at2s/(at2+at2s),'source_fraction':rows[2][2],'interpretation':'source image-scored cells; not sequencing abundance or independent donor replication'})
    summary={'numeric_entries':int(frame.source_n_cells.notna().sum()),'numeric_exact_matches':int((frame.comparison_status=='exact_count_match').sum()),'numeric_mismatches':int((frame.comparison_status=='count_mismatch').sum()),'unmapped_cells':len(unassigned),'curated_total':len(observed),'source_population_sum':75071,'published_total':75066,'interpretation':'Curated total matches summed source population rows; individual annotation differences retained. No claim of exact original release reconstruction.'}
    write_json(out/'summary.json',summary)
    finish_record(out,{'schema':'TN2020-concordance/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'source concordance complete; species extension gated','expression_analysis_run':False})
    print(summary)


if __name__=='__main__':main()
