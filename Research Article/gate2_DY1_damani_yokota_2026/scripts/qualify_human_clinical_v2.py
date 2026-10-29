"""Versioned source supplement: exact GEO subject joins for age and recorded sex."""
import argparse,csv,gzip,json,re
from pathlib import Path
import numpy as np
import pandas as pd


def parse_samples(text):
    rows=[]
    for block in re.split(r'^\^SAMPLE = ',text,flags=re.MULTILINE)[1:]:
        accession=block.splitlines()[0].strip()
        titles=re.findall(r'^!Sample_title = (.*)$',block,re.MULTILINE)
        if len(titles)!=1:raise ValueError('Missing/ambiguous sample title')
        match=re.fullmatch(r'(\S+) scRNAseq',titles[0].strip())
        if not match:raise ValueError('Unsupported exact title-to-subject rule')
        values={}
        for item in re.findall(r'^!Sample_characteristics_ch1 = (.*)$',block,re.MULTILINE):
            key,value=item.split(':',1);key=key.strip().lower();value=value.strip()
            if key in values and values[key]!=value:raise ValueError('Conflicting sample characteristic')
            values[key]=value
        age=pd.to_numeric(values.get('age',''),errors='coerce')
        if pd.notna(age) and not 0<=age<=120:raise ValueError('Invalid recorded age')
        sex=values.get('sex','')
        rows.append({'donor':match.group(1),'geo_accession':accession,'title':titles[0].strip(),
                     'disease':values.get('disease',''),'age':age,'age_raw':values.get('age',''),
                     'recorded_sex':sex if sex in ['F','M'] else None,'sex_raw':sex,
                     'tissue':values.get('tissue','')})
    frame=pd.DataFrame(rows)
    if frame.empty or frame.donor.duplicated().any() or frame.geo_accession.duplicated().any():
        raise ValueError('Missing or duplicate GEO subject records')
    return frame


def main(out):
    raw=Path('raw_data/GSE136831')
    with gzip.open(raw/'GSE136831_family.soft.gz','rt') as stream:text=stream.read()
    source=parse_samples(text)
    qual=Path('analysis/research/runs/DY1_human_qualification_v1')
    donors=pd.read_csv(qual/'donors.tsv',sep='\t',dtype={'Subject_Identity':str}).rename(columns={'Subject_Identity':'donor','Disease_Identity':'disease'})
    if set(source.donor)!=set(donors.donor):raise ValueError('GEO/cell subject sets do not match exactly')
    joined=donors.merge(source,on=['donor','disease'],validate='one_to_one')
    if len(joined)!=len(donors):raise ValueError('GEO and cell disease labels disagree')
    libraries=pd.read_csv(qual/'libraries.tsv',sep='\t',dtype={'Subject_Identity':str}).rename(columns={'Subject_Identity':'donor','Disease_Identity':'disease'})
    libjoin=libraries.merge(source,on=['donor','disease'],validate='many_to_one')
    if len(libjoin)!=len(libraries):raise ValueError('Library-level clinical join lost records')
    # Independent source line-state parser, not the regex-based production extraction.
    direct={};current=None
    for line in text.splitlines():
        if line.startswith('^SAMPLE = '):current=line.split(' = ',1)[1];direct[current]={}
        elif current and line.startswith('!Sample_title = '):direct[current]['donor']=line.split(' = ',1)[1].removesuffix(' scRNAseq')
        elif current and line.startswith('!Sample_characteristics_ch1 = '):
            key,value=line.split(' = ',1)[1].split(':',1);direct[current][key.lower().strip()]=value.strip()
    for row in joined.itertuples():
        record=direct[row.geo_accession]
        if record['donor']!=row.donor or record['disease']!=row.disease or record.get('age','')!=row.age_raw or record.get('sex','')!=row.sex_raw:
            raise ValueError('Independent clinical verification mismatch')
    joined.to_csv(out/'donor_clinical.tsv',sep='\t',index=False,lineterminator='\n')
    libjoin.to_csv(out/'library_clinical.tsv',sep='\t',index=False,lineterminator='\n')
    coverage=joined.groupby('disease').agg(donors=('donor','size'),age_available=('age','count'),sex_available=('recorded_sex','count'),age_min=('age','min'),age_max=('age','max')).reset_index()
    coverage.to_csv(out/'clinical_coverage.tsv',sep='\t',index=False,lineterminator='\n')
    summary={'analysis':'human clinical metadata supplement','donors':len(joined),'libraries':len(libjoin),
             'exact_subject_and_disease_joins':True,'independent_line_state_verification':True,
             'available_covariates':['age','recorded_sex'],'remaining_unqualified':['smoking','treatment','lung_function','tissue_region'],
             'supersedes':'Qualification_v1 accurately reports fields absent from the supplied cell table; this supplement recovers age and recorded sex from separate public GEO sample records.',
             'interpretation_limit':'Recorded donor covariates permit descriptive sensitivity only; no causal identification or comprehensive confounder control.',
             'scientific_acceptance':'not_assessed'}
    (out/'qualification.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
