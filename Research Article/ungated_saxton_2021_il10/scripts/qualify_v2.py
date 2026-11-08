"""GSE160332 identity and measurement qualification; no group outcome contrasts."""
import argparse,csv,gzip,json,re
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
RAW=ROOT/'raw_data/Sx10'
PKG=Path(__file__).resolve().parents[1]
LIBS=['Unt_1','Unt_2','BS30_1','BS30_2','BS65_1','BS65_2','BS45_1','BS45_2']
ARMS={'Unt':'PBS','BS30':'WT IL-10','BS45':'super-10','BS65':'10-DE'}
def write(p,rows):
    with p.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main(out):
    soft=gzip.decompress((RAW/'GSE160332_family.soft.gz').read_bytes()).decode()
    bio={x.attrib['accession']:x for x in ET.parse(RAW/'biosamples.xml').getroot().findall('BioSample')}
    sra={x.find('EXPERIMENT').attrib['accession']:x for x in ET.parse(RAW/'sra.xml').getroot().findall('EXPERIMENT_PACKAGE')}
    cross=[]
    for block in soft.split('^SAMPLE = ')[1:]:
        gsm=block.splitlines()[0];title=re.search(r'!Sample_title = (.+)',block)[1]
        treatment=re.search(r'!Sample_characteristics_ch1 = treatment: (.+)',block)[1]
        assert treatment==ARMS[title.split('_')[0]]
        sam=re.search(r'!Sample_relation = BioSample: .*?/(SAMN\d+)',block)[1]
        srx=re.search(r'!Sample_relation = SRA: .*?=(SRX\d+)',block)[1]
        b=bio[sam];attrs={a.attrib['attribute_name']:a.text for a in b.findall('.//Attribute')};assert attrs['treatment']==treatment
        e=sra[srx];sample=e.find('SAMPLE'); ext={a.attrib.get('namespace'):a.text for a in sample.findall('./IDENTIFIERS/EXTERNAL_ID')}
        assert ext['GEO']==gsm and ext['BioSample']==sam
        sa={a.findtext('TAG'):a.findtext('VALUE') for a in sample.findall('./SAMPLE_ATTRIBUTES/SAMPLE_ATTRIBUTE')};assert sa['treatment']==treatment
        cross.append(dict(library=title,arm=treatment,GSM=gsm,BioSample=sam,SRX=srx,SRS=sample.attrib['accession'],SRR=';'.join(r.attrib['accession'] for r in e.findall('./RUN_SET/RUN')),layout='paired-end' if e.find('.//LIBRARY_LAYOUT/PAIRED') is not None else 'other',donor='unknown',preparation='unknown',pairing='unknown',treatment_hours=24,active_ligand_nM=0 if treatment=='PBS' else 10,biosample_attribute_names=';'.join(attrs)))
    assert len(cross)==8 and {r['library'] for r in cross}==set(LIBS)
    cross.sort(key=lambda r:LIBS.index(r['library']));write(out/'sample_crosswalk.csv',cross)
    tables=[];matrices=[]
    for kind in ['readcount','fpkm']:
        with gzip.open(RAW/f'GSE160332_070720_10_{kind}_genename.txt.gz','rt',encoding='utf-8',newline='') as f:
            reader=csv.DictReader(f,delimiter='\t');fields=reader.fieldnames;rows=list(reader)
        assert set(LIBS).issubset(fields)
        ann=[{k:v for k,v in r.items() if k not in LIBS} for r in rows]
        m=np.array([[float(r[l]) for l in LIBS] for r in rows]); assert np.isfinite(m).all() and (m>=0).all()
        tables.append(ann);matrices.append(m)
    # Source matrices have different row order: require identical unique ID-keyed annotations.
    by_id=[{r["gene_id"]:i for i,r in enumerate(t)} for t in tables]
    assert all(len(d)==len(t) for d,t in zip(by_id,tables))
    assert by_id[0].keys()==by_id[1].keys()
    order=[by_id[1][r["gene_id"]] for r in tables[0]]
    assert tables[0]==[tables[1][i] for i in order]
    matrices[1]=matrices[1][order]
    ann=tables[0];counts,fpkm=matrices
    assert len(set(r['gene_id'] for r in ann))==len(ann) and np.equal(counts,np.floor(counts)).all()
    sums=counts.sum(axis=0);assert (sums>0).all();cpm=counts/sums*1e6;eligible=(cpm>=1).sum(axis=1)>=2
    qc=[dict(library=l,count_sum=int(sums[j]),detected_rows=int((counts[:,j]>0).sum()),rows_CPM_ge_1=int((cpm[:,j]>=1).sum()),FPKM_sum=float(fpkm[:,j].sum())) for j,l in enumerate(LIBS)]
    write(out/'library_qc.csv',qc)
    symbol_counts=Counter(r['gene_name'] for r in ann)
    repeated=[dict(symbol=s,stable_ID_rows=n) for s,n in symbol_counts.items() if n>1]
    write(out/'repeated_symbols.csv',repeated)
    panels=json.loads((PKG/'sources/figure5_memberships_v1.json').read_text())['panels'];mapping=[]
    for panel,members in panels.items():
        for s in members:
            ix=[i for i,r in enumerate(ann) if r['gene_name']==s]
            mapping.append(dict(panel=panel,symbol=s,matches=len(ix),gene_ids=';'.join(ann[i]['gene_id'] for i in ix),eligible=bool(eligible[ix[0]]) if len(ix)==1 else 'unavailable'))
    write(out/'target_mapping.csv',mapping)
    corr=np.corrcoef(np.log2(cpm[eligible]+1).T)
    write(out/'library_correlations.csv',[dict(library_a=a,library_b=b,pearson_log_CPM=float(corr[i,j])) for i,a in enumerate(LIBS) for j,b in enumerate(LIBS)])
    summary=dict(rows=len(ann),libraries=8,unique_stable_ids=True,integer_nonnegative_counts=True,annotation_agreement=True,all_zero_rows=int((counts.sum(axis=1)==0).sum()),eligible_rows=int(eligible.sum()),repeated_symbols=len(repeated),rows_with_repeated_symbols=sum(r['stable_ID_rows'] for r in repeated),qualified_treatment_identity=True,biological_replicates_author_reported=2,donor_identity='unknown',population_inference='held',pairing='unknown',exact_author_replay='held: S9 and exact transformation/filter/aggregation unavailable',scope='finite deposited libraries')
    (out/'qualification.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);main(p.parse_args().output)
