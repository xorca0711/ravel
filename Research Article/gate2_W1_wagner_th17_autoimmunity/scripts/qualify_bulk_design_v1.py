"""Qualify deposited bulk matrices and animal-blocked designs, without contrasts."""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys
import gzip
import numpy as np
import pandas as pd

SERIES=('GSE162300','GSE162382')

def exact_rank(matrix):
    a=[[Fraction(x) for x in row] for row in matrix]
    rank=0
    for column in range(len(a[0])):
        pivot=next((i for i in range(rank,len(a)) if a[i][column]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        value=a[rank][column];a[rank]=[x/value for x in a[rank]]
        for i in range(rank+1,len(a)):
            value=a[i][column]
            if value:a[i]=[x-value*y for x,y in zip(a[i],a[rank])]
        rank+=1
        if rank==len(a):break
    return rank

def qualify(rows):
    selected=[r for r in rows if r['series'] in SERIES]
    if len({r['gsm'] for r in selected})!=len(selected):raise ValueError('Duplicate GSM')
    libraries={}
    mapping=[]
    for row in selected:
        if row['series']==SERIES[0]:
            match=re.fullmatch(r'(Th17p|Th17n|iTreg)_(Vehicle|DFMO)_(WT[1-3])_run([12])',row['title'])
            if not match:raise ValueError('Unexpected first-series title')
            lineage,treatment,animal,run=match.groups();genotype='WT'
            if row['run_id']!='run'+run:raise ValueError('Run/title disagreement')
            library=row['title'].rsplit('_run',1)[0]
        else:
            match=re.fullmatch(r'(Th17n|iTreg)_(ctrl|DFMO)_(WT[1-4]|JMJD3CKO[1-3])',row['title'])
            if not match:raise ValueError('Unexpected genotype-series title')
            lineage,treatment,animal=match.groups();run=''
            genotype='WT' if animal.startswith('WT') else 'JMJD3_KO'
            if row['genotype']!=genotype:raise ValueError('Genotype/title disagreement')
            library=row['title']
        if (row['animal_id'],row['cell_type'],row['treatment'])!=(animal,lineage,treatment):
            raise ValueError('Metadata/title disagreement')
        key=(row['series'],library)
        record={'series':row['series'],'library_id':library,'animal_id':animal,'genotype':genotype,
                'cell_type':lineage,'treatment':'control' if treatment in ['Vehicle','ctrl'] else 'DFMO'}
        if key not in libraries:libraries[key]=dict(record,gsms=[],runs=[])
        libraries[key]['gsms'].append(row['gsm']);libraries[key]['runs'].append(run)
        mapping.append(dict(record,gsm=row['gsm'],source_title=row['title'],source_run=run))
    result=[]
    for key,row in sorted(libraries.items()):
        expected=['1','2'] if row['series']==SERIES[0] else ['']
        if sorted(row['runs'])!=expected:raise ValueError('Technical-run pair incomplete or duplicated')
        result.append({**{k:v for k,v in row.items() if k not in ['gsms','runs']},
                       'source_gsms':';'.join(sorted(row['gsms'])),'source_record_count':len(row['gsms']),
                       'unit_scope':'source-labelled animal; libraries nested within animal'})
    for series,animals,types in [(SERIES[0],['WT1','WT2','WT3'],['Th17n','Th17p','iTreg']),
                                (SERIES[1],['WT1','WT2','WT3','WT4','JMJD3CKO1','JMJD3CKO2','JMJD3CKO3'],['Th17n','iTreg'])]:
        expected={(animal,cell,treatment) for animal in animals for cell in types for treatment in ['control','DFMO']}
        actual={(r['animal_id'],r['cell_type'],r['treatment']) for r in result if r['series']==series}
        if actual!=expected:raise ValueError('Source design incomplete or unexpected')
    return mapping,result

def model(rows, include_genotype_main=False):
    animals=sorted({r['animal_id'] for r in rows});types=sorted({r['cell_type'] for r in rows})
    genotype=len({r['genotype'] for r in rows})>1
    names=['intercept']+['animal_'+x for x in animals[1:]]+['lineage_'+x for x in types[1:]]+['DFMO']
    names+=['lineage_'+x+':DFMO' for x in types[1:]]
    if genotype:
        names+=['KO:DFMO']+['KO:lineage_'+x for x in types[1:]]+['KO:lineage_'+x+':DFMO' for x in types[1:]]
        if include_genotype_main:names+=['KO_main']
    matrix=[]
    for row in rows:
        t=int(row['treatment']=='DFMO');g=int(row['genotype']=='JMJD3_KO')
        lineages=[int(row['cell_type']==x) for x in types[1:]]
        values=[1]+[int(row['animal_id']==x) for x in animals[1:]]+lineages+[t]+[x*t for x in lineages]
        if genotype:
            values+=[g*t]+[g*x for x in lineages]+[g*x*t for x in lineages]
            if include_genotype_main:values+=[g]
        matrix.append(values)
    rank=exact_rank(matrix)
    return {'n_libraries':len(rows),'n_animals':len(animals),'columns':len(names),'rank':rank,
            'residual_df_if_fitted':len(rows)-rank,'full_rank':rank==len(names),'terms':';'.join(names)},matrix

def raw_sample_titles(path):
    result={};current=None
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.startswith('^SAMPLE = '):current=line.strip().split(' = ',1)[1]
            elif current and line.startswith('!Sample_title = '):result[current]=line.strip().split(' = ',1)[1]
    return result

def table(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(rows)

def read_matrix(path, expected_titles):
    with gzip.open(path,'rt',encoding='utf-8-sig',newline='') as f:
        reader=csv.reader(f);header=next(reader);rows=list(reader)
    if header[0]!='symbol' or len(set(header))!=len(header):raise ValueError('Invalid or duplicate matrix header')
    if set(header[1:])!=set(expected_titles):raise ValueError('Matrix/source sample mismatch')
    if any(len(r)!=len(header) for r in rows):raise ValueError('Ragged matrix')
    symbols=[r[0] for r in rows]
    values=np.asarray([r[1:] for r in rows],dtype=float)
    if not np.isfinite(values).all() or (values<0).any():raise ValueError('Nonfinite or negative matrix value')
    if not symbols or any(not x for x in symbols):raise ValueError('Empty gene identifier')
    if len(set(symbols))!=len(symbols):raise ValueError('Duplicate gene symbols; aggregation requires a separate decision')
    # Separate CSV parser and dataframe conversion verify identities, scale and all values.
    alternate=pd.read_csv(path,index_col=0,keep_default_na=False,float_precision='round_trip')
    if list(alternate.index)!=symbols or list(alternate.columns)!=header[1:]:raise ValueError('Independent parser identity disagreement')
    if not np.array_equal(alternate.to_numpy(dtype=float),values):raise ValueError('Independent parser value disagreement')
    return symbols,header[1:],values

def main(source,r0,acquisition,output):
    with (r0/'samples.tsv').open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f,delimiter='\t'))
    mapping,libraries=qualify(rows)
    verified=0
    for series in SERIES:
        titles=raw_sample_titles(source/(series+'_family.soft'))
        expected={r['gsm']:r['source_title'] for r in mapping if r['series']==series}
        if titles!=expected:raise ValueError('Independent raw SOFT title/identity check failed')
        verified+=len(expected)
    text=(source/(SERIES[0]+'_family.soft')).read_text(encoding='utf-8')
    design=next(x for x in text.splitlines() if x.startswith('!Series_overall_design = '))
    if 'Each library was run on two separate Next-Seq runs on the same day.' not in design:
        raise ValueError('Explicit same-library technical-run statement missing')
    models=[];matrices={}
    for series in SERIES:
        group=[r for r in libraries if r['series']==series]
        combinations=[('all_lineages_animal_blocked',group,False)]
        combinations +=[(cell+'_animal_blocked',[r for r in group if r['cell_type']==cell],False) for cell in sorted({r['cell_type'] for r in group})]
        if series==SERIES[1]:combinations.append(('diagnostic_aliased_genotype_main',group,True))
        for name,subset,add_main in combinations:
            result,matrix=model(subset,add_main)
            independent_rank=int(np.linalg.matrix_rank(np.asarray(matrix,dtype=float)))
            if independent_rank!=result['rank']:raise ValueError('Exact/SVD rank disagreement')
            models.append({'series':series,'candidate_model':name,**result,'independent_svd_rank':independent_rank,'expression_fit_status':'not_run; qualification only'})
            matrices[series+'.'+name]={'library_ids':[r['library_id'] for r in subset],'matrix':matrix}
    received=json.loads(acquisition.read_text())
    available={Path(r['path']).name:r for r in received['sources']}
    inventory=[];sample_qc=[];technical=[];matrix_joins=[]
    for series,stem in [(SERIES[0],'DFMO_RNA'),(SERIES[1],'DFMO_JMJD3')]:
        loaded={}
        expected=[r['source_title'] for r in mapping if r['series']==series]
        by_title={r['source_title']:r for r in mapping if r['series']==series}
        for scale in ['TPMs','est_counts']:
            name=f'{series}_{stem}_{scale}.csv.gz'
            record=available[name];path=acquisition.parent/name
            if hashlib.sha256(path.read_bytes()).hexdigest()!=record['sha256']:raise ValueError('Acquisition hash mismatch')
            symbols,columns,values=read_matrix(path,expected);loaded[scale]=(symbols,columns,values)
            inventory.append({'series':series,'file':name,'sha256':record['sha256'],'genes':len(symbols),
                              'columns':len(columns),'unique_gene_symbols':True,'all_finite_nonnegative':True,
                              'independent_parser_exact_values':True,'fractional_value_count':int(np.count_nonzero(values!=np.floor(values))),
                              'zero_gene_rows':int(np.count_nonzero(~np.any(values>0,axis=1))),
                              'matrix_column_join':'exact unique titles; all source records represented'})
            for i,column in enumerate(columns):
                sample_qc.append({'series':series,'scale':scale,'source_title':column,'sum_deposited_values':float(values[:,i].sum()),
                                  'genes_positive':int(np.count_nonzero(values[:,i]>0)),'minimum':float(values[:,i].min()),'maximum':float(values[:,i].max())})
                matrix_joins.append({'series':series,'scale':scale,'column_number_1_based':i+1,**by_title[column]})
        if loaded['TPMs'][:2]!=loaded['est_counts'][:2]:raise ValueError('TPM/count identifiers or column order differ')
        if series==SERIES[0]:
            for library in [r for r in libraries if r['series']==series]:
                name=library['library_id'];columns=loaded['TPMs'][1]
                i,j=columns.index(name+'_run1'),columns.index(name+'_run2')
                for scale in ['TPMs','est_counts']:
                    values=loaded[scale][2]
                    correlation=float(np.corrcoef(np.log1p(values[:,i]),np.log1p(values[:,j]))[0,1])
                    technical.append({'library_id':name,'scale':scale,'log1p_all_gene_pearson_r':correlation,
                                      'run1_sum':float(values[:,i].sum()),'run2_sum':float(values[:,j].sum()),
                                      'count_merge_rule':'sum expected counts of same library; retain fractional values',
                                      'tpm_merge_rule':'not merged here; simple sum is invalid for normalized TPM'})
    table(output/'source_sample_map.tsv',mapping);table(output/'library_design.tsv',libraries)
    table(output/'candidate_designs.tsv',models);table(output/'matrix_inventory.tsv',inventory)
    table(output/'matrix_sample_qc.tsv',sample_qc);table(output/'technical_run_qc.tsv',technical)
    table(output/'matrix_column_join.tsv',matrix_joins)
    (output/'source_manifest.json').write_text(json.dumps(received,indent=2)+'\n')
    (output/'candidate_design_matrices.json').write_text(json.dumps(matrices,indent=2)+'\n')
    report={'scope':'Source/matrix/design qualification; no expression contrasts or fitted differential-expression model','source_sample_records':len(mapping),
            'independently_verified_gsm_titles':verified,'source_library_labels':len(libraries),
            'GSE162300':{'records':36,'libraries':18,'animal_labels':3,'technical_records_per_library':2,'source_processing':'Bowtie2/RSEM; GRCm38.p3'},
            'GSE162382':{'records':28,'libraries':28,'WT_animal_labels':4,'JMJD3_KO_animal_labels':3,'Th17p_present':False,'source_processing':'Kallisto; GRCm38.96'},
            'decision':'PASS exact matrix/source joins, numeric scale and full-rank within-series blocked candidate designs. Eligible for a separate frozen analysis; no model fitted in this run.',
            'technical_run_decision':'36 run columns represent 18 libraries. Sum expected counts over two same-library runs for count-based analysis; keep 3 animal labels. Do not sum TPMs or treat runs as independent samples.',
            'genotype_decision':'Animal-fixed-effect models absorb genotype main effects; directly model within-animal treatment effects and genotype-by-treatment terms. Rank is checked from source labels only.',
            'biological_limits':'Animal identifiers are source labels, not independently audited specimen records. WT identifiers are scoped to each series; no cross-series pairing or independent replication is invented.',
            'source_discrepancy':'Figure 6H legend states n=4; deposit provides four WT and three KO animal labels. Do not invent a fourth KO.',
            'acquisition_failures':received['failures'],'expression_values_inspected':'Only file integrity, numeric domain, totals, detection and technical-run concordance; no biological contrasts.',
            'matrix_files':len(inventory),'matrix_columns_verified':len(matrix_joins),
            'independent_checks':'Raw SOFT vs R0 identity joins; csv vs pandas all matrix values; exact rational vs NumPy SVD design ranks.',
            'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__}
    (output/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['source_sample_records','independently_verified_gsm_titles','source_library_labels','decision']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--r0',type=Path,required=True)
    p.add_argument('--acquisition',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();main(a.source,a.r0,a.acquisition,a.output)
