"""Dated source and public-matrix qualification; no expression contrasts."""
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

RAW=Path('raw_data/navarro_2026/followup_20261110')
SERIES={
    'GSE318914':'GSE318914_PBMC_Gene_Expression_Count.featureCounts.txt.gz',
    'GSE318915':'GSE318915_Tcell.Gene_Expression_Count.featureCounts.txt.gz',
}
MARKERS=('STAT3','SOCS3','TNF','IFNG','GZMB')


def samples(path):
    records=[]; current=None
    for line in gzip.open(path,'rt',encoding='utf-8'):
        if line.startswith('^SAMPLE = '):
            current={'gsm':line.strip().split(' = ',1)[1],'characteristics':{}}
            records.append(current)
        elif line.startswith('^'):
            current=None
        elif current is not None and ' = ' in line:
            key,value=line.rstrip('\n').split(' = ',1)
            if key=='!Sample_characteristics_ch1':
                name,description=value.split(': ',1)
                assert name not in current['characteristics']
                current['characteristics'][name]=description
            elif key=='!Sample_description' and value.startswith('Library name: '):
                assert 'library' not in current
                current['library']=value.removeprefix('Library name: ')
            elif key in ('!Sample_title','!Sample_organism_ch1'):
                current[key.removeprefix('!Sample_')]=value
    return records


def json_out(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')


def csv_out(path,rows):
    with path.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output
    config=json.loads(Path(__file__).with_name('metadata_inputs_v1.json').read_text())
    manifest=[]
    for item in config['inputs']:
        data=Path(item['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        manifest.append(dict(item,bytes=len(data)))
    old=ET.parse('raw_data/navarro_2026/source_v1/biosample.xml').getroot()
    new=ET.parse(RAW/'biosample_current.xml').getroot()
    def attributes(tree):
        return {x.attrib['accession']:{a.attrib['attribute_name']:a.text for a in x.findall('.//Attribute')} for x in tree.findall('BioSample')}
    old_attrs,new_attrs=attributes(old),attributes(new)
    ena=list(csv.DictReader((RAW/'ena_current.tsv').open(encoding='utf-8'),delimiter='\t'))
    git=json.loads((RAW/'github_current.json').read_text())
    data_record=json.loads((RAW/'zenodo_latest_data.json').read_text())
    code_record=json.loads((RAW/'zenodo_latest_code.json').read_text())
    assert old_attrs==new_attrs, 'Changed BioSample attributes require a new source interpretation'
    assert git['commit']['sha']=='c08010bb29f0cb9b56143a25f6a2b1c28692cf70'
    assert data_record['id']==17594828 and code_record['id']==18174039
    assert not any(x['path'].lower().endswith('.rda') for x in git['tree']['tree'])
    source={
        'checked_date':'2026-11-10 Asia/Seoul','biosample_attributes_unchanged':old_attrs==new_attrs,
        'biosample_attributes':new_attrs,'ena_runs':ena,
        'author_commit':git['commit'],'author_tree_paths':[x['path'] for x in git['tree']['tree']],
        'latest_data_record':data_record['id'],'latest_code_record':code_record['id'],
        'zenodo_files':[{k:x[k] for k in ('key','size','checksum')} for x in data_record['files']],
        'additional_bioproject_search':json.loads((RAW/'additional_bioprojects.json').read_text())['esearchresult'],
        'alias_dose_join':'unresolved; public metadata refresh does not link eight object aliases to six main libraries',
        'donor_assignment':'no main-object per-mouse demultiplexing established',
        'exact_downstream_microglia_and_hallmark':'unchanged holds; no new author code or rda in the inspected tree',
    }
    joins=[]; qualified=[]; libraries=[]
    for series,filename in SERIES.items():
        records=samples(RAW/(series+'_family.soft.gz'))
        by_library={x['library']:x for x in records}
        assert len(by_library)==len(records)
        gene_ids=set(); marker_ids={x:[] for x in MARKERS}; rows=0
        with gzip.open(RAW/filename,'rt',encoding='utf-8') as handle:
            reader=csv.reader(handle,delimiter='\t'); header=next(reader)
            assert header[:4]==['Gene_ID','Gene_Name','Gene_Type','Gene_Length']
            assert len(header[4:])==len(set(header[4:])) and set(header[4:])==set(by_library)
            totals=[0]*len(header[4:])
            for row in reader:
                assert len(row)==len(header) and row[0] not in gene_ids
                gene_ids.add(row[0]); rows+=1
                values=[int(x) for x in row[4:]]
                assert all(x>=0 for x in values)
                totals=[a+b for a,b in zip(totals,values)]
                if row[1] in marker_ids: marker_ids[row[1]].append(row[0])
        assert all(x>0 for x in totals)
        assert all(len(x)==1 for x in marker_ids.values()),marker_ids
        strata={}
        for column,total in zip(header[4:],totals):
            record=by_library[column]; fields=record['characteristics']
            assert record['organism_ch1']=='Homo sapiens'
            row=dict(series=series,gsm=record['gsm'],library=column,donor=fields['donor'],
                     cell_type=fields['cell type'],condition=fields.get('condition','Tcell'),
                     treatment=fields['treatment'],timepoint=fields['timepoint'],total_counts=total)
            key=(row['donor'],row['condition'],row['timepoint'])
            strata.setdefault(key,[]).append(row['treatment']); joins.append(row)
            libraries.append(dict(series=series,library=column,total_counts=total))
        expected={'PBS','IL-10','IL-10-Fc','ms-IL10R agonist'}
        assert all(len(v)==4 and set(v)==expected for v in strata.values())
        qualified.append(dict(series=series,samples=len(records),genes=rows,
            donors=sorted({x['characteristics']['donor'] for x in records}),
            treatments=sorted(expected),paired_strata=len(strata),marker_ids=marker_ids,
            count_semantics='nonnegative integer featureCounts; all columns explicitly joined by Sample_description Library name',
            eligibility='within-series donor-paired human context only',
            not_supplied=['D25K','aged brain','young/old treatment factorial','injury recovery','cross-series donor identity']))
    json_out(out/'source_refresh.json',source)
    json_out(out/'public_deposit_qualification.json',qualified)
    json_out(out/'input_manifest.json',manifest)
    csv_out(out/'public_sample_crosswalk.csv',joins)
    csv_out(out/'library_sizes.csv',libraries)
    (out/'.gitattributes').write_text('* -text whitespace=cr-at-eol\n',encoding='utf-8',newline='\n')
    print(json.dumps({'series':[(x['series'],x['samples'],x['genes']) for x in qualified],'navarro_holds':'retained'}))


if __name__=='__main__': main()
