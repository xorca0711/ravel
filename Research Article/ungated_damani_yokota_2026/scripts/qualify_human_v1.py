"""Qualify public human atlas identifiers and coverage; no expression fits."""
import argparse
import gzip
import json
from pathlib import Path
import numpy as np
import pandas as pd

RAW=Path('raw_data/GSE136831')
META='GSE136831_AllCells.Samples.CellType.MetadataTable.txt.gz'
GENES='GSE136831_AllCells.GeneIDs.txt.gz'
BARCODES='GSE136831_AllCells.cellBarcodes.txt.gz'
MATRIX='GSE136831_RawCounts_Sparse.mtx.gz'


def check_identity(meta, barcodes):
    required=['CellBarcode_Identity','Subject_Identity','Library_Identity','Disease_Identity',
              'Manuscript_Identity','Subclass_Cell_Identity','CellType_Category','nUMI','nGene']
    if not set(required).issubset(meta.columns):
        raise ValueError('Missing required metadata fields')
    if meta[required].isna().any().any() or meta.CellBarcode_Identity.duplicated().any():
        raise ValueError('Missing metadata value or duplicated barcode')
    if len(set(barcodes))!=len(barcodes) or meta.CellBarcode_Identity.tolist()!=barcodes:
        raise ValueError('Barcode identity/order mismatch')
    if (meta.groupby('Subject_Identity').Disease_Identity.nunique()!=1).any():
        raise ValueError('Donor maps to more than one disease')
    if (meta.groupby('Library_Identity').Subject_Identity.nunique()!=1).any():
        raise ValueError('Library maps to more than one donor')
    if not set(meta.Disease_Identity).issubset({'Control','IPF','COPD'}):
        raise ValueError('Unexpected disease label')
    for key in ['nUMI','nGene']:
        values=pd.to_numeric(meta[key],errors='raise')
        if (values<=0).any() or (values%1!=0).any():
            raise ValueError('Invalid assay count metadata')


def main(out):
    meta=pd.read_csv(RAW/META,sep='\t')
    with gzip.open(RAW/BARCODES,'rt') as stream: barcodes=[line.strip() for line in stream]
    check_identity(meta,barcodes)
    genes=pd.read_csv(RAW/GENES,sep='\t')
    if genes.Ensembl_GeneID.duplicated().any() or genes.isna().any().any():
        raise ValueError('Missing or duplicate gene identity')
    with gzip.open(RAW/MATRIX,'rt') as stream:
        header=next(stream).strip()
        if header!='%%MatrixMarket matrix coordinate integer general':
            raise ValueError('Unexpected matrix convention: '+header)
        line=next(stream)
        while line.startswith('%'): line=next(stream)
        n_genes,n_cells,nnz=map(int,line.split())
    if (n_genes,n_cells)!=(len(genes),len(meta)):
        raise ValueError('Matrix dimensions disagree with source identifiers')
    donor=meta.groupby(['Subject_Identity','Disease_Identity'],sort=True).agg(
        n_cells=('CellBarcode_Identity','size'),n_libraries=('Library_Identity','nunique'),
        metadata_UMI_sum=('nUMI','sum'),median_nUMI=('nUMI','median')).reset_index()
    coverage=meta.groupby(['Subject_Identity','Disease_Identity','CellType_Category',
                         'Manuscript_Identity','Subclass_Cell_Identity'],sort=True).agg(
        n_cells=('CellBarcode_Identity','size'),metadata_UMI_sum=('nUMI','sum')).reset_index()
    libraries=meta.groupby(['Subject_Identity','Disease_Identity','Library_Identity'],sort=True).size().rename('n_cells').reset_index()
    # Independent CSV-reader count provides a different implementation of joins.
    import csv
    from collections import Counter
    with gzip.open(RAW/META,'rt',newline='') as stream:
        direct=Counter((r['Subject_Identity'],r['Disease_Identity'],r['CellType_Category'],
                        r['Manuscript_Identity'],r['Subclass_Cell_Identity']) for r in csv.DictReader(stream,delimiter='\t'))
    observed={tuple(row[:5]):int(row[5]) for row in coverage.itertuples(index=False,name=None)}
    if dict(direct)!=observed or coverage.n_cells.sum()!=n_cells:
        raise ValueError('Independent coverage arithmetic disagrees')
    wanted=['ATP10A','FABP4','SERPING1','SVIL','MMP9','LGMN','PLA2G7','RGS1',
            'COL1A1','COL1A2','COL3A1','COL6A1','COL6A2','FN1','ACTA2','ARG1']
    mappings=[]
    for symbol in wanted:
        rows=genes[genes.HGNC_EnsemblAlt_GeneID==symbol]
        mappings.append({'symbol':symbol,'n_rows':len(rows),'ensembl_ids':';'.join(rows.Ensembl_GeneID),
                         'status':'unique' if len(rows)==1 else 'missing' if len(rows)==0 else 'ambiguous',
                         'orthology':'not_applicable_native_human_symbols'})
    for name,table in [('donors.tsv',donor),('annotation_coverage.tsv',coverage),('libraries.tsv',libraries),
                       ('panel_gene_mapping.tsv',pd.DataFrame(mappings))]:
        table.to_csv(out/name,sep='\t',index=False,lineterminator='\n')
    summary={'analysis':'human source qualification only','n_cells':n_cells,'n_genes':n_genes,'matrix_nnz':nnz,
             'matrix_header':header,'donors_by_disease':donor.Disease_Identity.value_counts().sort_index().to_dict(),
             'libraries':len(libraries),'max_libraries_per_donor':int(donor.n_libraries.max()),
             'categories':sorted(meta.CellType_Category.unique()),'annotations':sorted(meta.Manuscript_Identity.unique()),
             'exact_barcode_order_verified':True,'independent_coverage_rows_verified':len(coverage),
             'clinical_covariates_absent':['age','sex','smoking','treatment','lung_function','tissue_region'],
             'assay_limit':'Deposited integer UMI matrix; agreement with metadata nUMI must be checked during numerical aggregation.',
             'identity_limit':'Deposited generic macrophage labels do not identify validated human NAMs or anatomical nerve association.',
             'eligible_for_donor_description':True,'scientific_acceptance':'not_assessed',
             'source_lineage':'GSE136831 already reused in Ravel; no independent replication.'}
    (out/'qualification.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path)
    main(p.parse_args().output)
