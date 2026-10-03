"""Source list and annotation concordance; no new expression or state model."""
from pathlib import Path
import argparse,json
import h5py,pandas as pd
from openpyxl import load_workbook
from nb5_io import read_obs,write_tsv,write_json

def sheet(w,name):
    rows=w[name].values;next(rows);header=[v if v is not None else 'gene' for v in next(rows)];return pd.DataFrame(rows,columns=header).dropna(how='all')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output);out.mkdir(exist_ok=True);raw=Path('raw_data/tabula_muris_senis_2020')
    w=load_workbook(raw/'intake_v1/supplement_table_10.xlsx',read_only=True,data_only=True)
    older=sheet(w,'facs.Brain_Myeloid.101214vs16');younger=sheet(w,'facs.Brain_Myeloid.16vs101214');disease=sheet(w,'Amit_expression_mic3tomic1');w.close()
    source=pd.concat([older.head(100).assign(source_direction='old_cluster_up'),younger.head(100).assign(source_direction='young_cluster_up')],ignore_index=True)
    disease_set=set(disease.gene.dropna().astype(str));source['in_full_disease_source']=source.gene.astype(str).isin(disease_set)
    write_tsv(out/'bidirectional_source_overlap.tsv',source[['gene','source_direction','in_full_disease_source']])
    stats={'older_rows':len(older),'younger_rows':len(younger),'combined_rows':len(source),'unique_combined_genes':source.gene.nunique(),'disease_rows':len(disease),'unique_overlap':len(set(source.gene)&disease_set),'overlapping_rows':int(source.in_full_disease_source.sum()),'published_overlap':55,'source_selection':'Pinned source notebook combines the first 100 old-up rows and first 100 young-up rows; compare to the full deposited disease list, not its arbitrary first 200 rows.','interpretation':'Source-list reuse and prior selection; no independent disease validation or enrichment test.'}
    with h5py.File(raw/'case_study_v1/facs.Brain_Myeloid.clustered_diversity.h5ad','r') as f:o=read_obs(f)
    rows=[]
    for field in ['cell_ontology_class','cell_ontology_class_old','cell_ontology_class_reannotated','free_annotation','free_annotation_reannotated','leiden','louvain']:
        if field not in o:continue
        for (age,label),g in o.groupby(['age',field],observed=True,dropna=False):rows.append(dict(field=field,age=age,label=str(label),cells=len(g),mouse_labels=g.mouse_id.nunique()))
    write_tsv(out/'case_annotation_audit.tsv',pd.DataFrame(rows))
    write_json(out/'source_audit.json',stats);print(json.dumps(stats))

if __name__=='__main__':main()
