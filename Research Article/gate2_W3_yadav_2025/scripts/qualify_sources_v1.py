"""Source qualification only: no expression or functional effect analysis."""
import argparse,csv,gzip,hashlib,io,json,re,tarfile,zipfile
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/'raw_data/Yd1_source_v1'
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()

def workbook():
    sheets,cells=[],[]
    with zipfile.ZipFile(SRC/'JCI188734.sdval.xlsx') as z:
        strings=[''.join(s.itertext()) for s in E.fromstring(z.read('xl/sharedStrings.xml'))]
        rels={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sh in E.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',NS):
            target=rels[sh.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            x=E.fromstring(z.read(target.lstrip('/') if target.startswith('/') else 'xl/'+target))
            nums,labels,formulas=Counter(),{},[]
            for c in x.findall('.//s:sheetData/s:row/s:c',NS):
                kind=c.get('t','n'); value=c.findtext('s:v',namespaces=NS)
                if kind=='s' and value is not None: value=strings[int(value)]
                elif kind=='inlineStr': value=''.join(c.find('s:is',NS).itertext())
                if value is None: continue
                if kind=='n':
                    float(value)
                    nums[re.match('[A-Z]+',c.get('r'))[0]]+=1
                else: labels[c.get('r')]=value
                formula=c.findtext('s:f',default='',namespaces=NS)
                if formula: formulas.append(c.get('r'))
                cells.append([sh.get('name'),c.get('r'),kind,value,c.get('s','0'),formula])
            sheets.append(dict(sheet=sh.get('name'),dimension=x.find('s:dimension',NS).get('ref'),
                state=sh.get('state','visible'),numeric_cells_by_column=dict(nums),labels=labels,
                formula_cells=formulas,merged_ranges=[m.get('ref') for m in x.findall('s:mergeCells/s:mergeCell',NS)]))
        extras=[n for n in z.namelist() if re.search('comments|externalLink|drawing',n,re.I)]
    return dict(sheets=sheets,extra_parts=extras),cells

def geo():
    records={}; cur=None
    for line in gzip.decompress((SRC/'GSE242510_family.soft.gz').read_bytes()).decode().splitlines():
        if line.startswith('^SAMPLE = '):
            cur=line.split(' = ',1)[1]; records[cur]={}
        elif line.startswith('^'): cur=None
        elif cur and line.startswith('!Sample_'):
            k,v=line.split(' = ',1); records[cur].setdefault(k,[]).append(v)
    bios={}
    for s in E.parse(SRC/'biosamples.xml').findall('BioSample'):
        ids={i.get('db'):i.text for i in s.findall('Ids/Id')}
        bios[ids['GEO']]=dict(biosample=s.get('accession'),srs=ids['SRA'],
            attributes={a.get('attribute_name'):a.text for a in s.findall('Attributes/Attribute')})
    exps={}
    for e in E.parse(SRC/'experiments.xml').findall('EXPERIMENT'):
        exps[e.findtext('DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_NAME')]=dict(srx=e.get('accession'),
            srs=e.find('DESIGN/SAMPLE_DESCRIPTOR').get('accession'),pool_elements=len(e.findall('.//POOL')))
    assert len(records)==len(bios)==len(exps)==6
    out=[]
    for gsm,r in records.items():
        assert bios[gsm]['srs']==exps[gsm]['srs']
        files=[v for k,vs in r.items() if k.startswith('!Sample_supplementary_file') for v in vs]
        assert len(files)==3
        out.append(dict(gsm=gsm,title=r['!Sample_title'][0],characteristics=r['!Sample_characteristics_ch1'],
            relations=r['!Sample_relation'],files=files,**bios[gsm],**{k:v for k,v in exps[gsm].items() if k!='srs'},
            animal_ids=None,preparation_ids=None,independent_biological_replicates=None,
            pooling='not reported; missing XML pool elements do not prove no pooling',
            pairing='unknown; suffixes and accessions do not establish pairing'))
    return out

def matrices(samples):
    inventory,data=[],{}
    expected={u.rsplit('/',1)[-1] for s in samples for u in s['files']}
    with tarfile.open(SRC/'GSE242510_RAW.tar') as tar:
        members=[m for m in tar.getmembers() if m.isfile()]
        assert {m.name for m in members}==expected
        for m in members:
            b=tar.extractfile(m).read()  # no untrusted archive path is written
            r=data.setdefault(m.name.split('_',1)[0],{})
            with gzip.GzipFile(fileobj=io.BytesIO(b)) as f:
                if m.name.endswith('_matrix.mtx.gz'):
                    banner=f.readline().decode().strip()
                    assert banner=='%%MatrixMarket matrix coordinate integer general',banner
                    line=f.readline()
                    while line.startswith(b'%'): line=f.readline()
                    a,c,n=map(int,line.split())
                    r.update(features=a,barcodes=c,declared_nonzero_entries=n)
                    scope='header only; expression entries not analyzed or exhaustively validated'
                else:
                    rows=[l.decode().rstrip('\r\n').split('\t') for l in f]
                    ids=[row[0] for row in rows]
                    assert len(ids)==len(set(ids)),m.name
                    kind='feature' if m.name.endswith('_features.tsv.gz') else 'barcode'
                    r[kind+'_rows']=len(rows)
                    if kind=='feature':
                        r['feature_columns']=sorted({len(row) for row in rows})
                        r['arg1_il6_features']=[row for row in rows if len(row)>1 and row[1] in ('Arg1','Il6')]
                    scope='all identifiers read; unique IDs verified'
            inventory.append(dict(file=m.name,bytes=m.size,sha256=hashlib.sha256(b).hexdigest(),inspection=scope))
    for gsm,r in data.items():
        assert r['features']==r['feature_rows'] and r['barcodes']==r['barcode_rows'],gsm
    return dict(members=inventory,libraries=data,scope='Deposited count-file structure only; no cell QC, annotation or biological inference.')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    def save(name,x):
        with (args.output/name).open('x',encoding='utf-8',newline='\n') as f:
            json.dump(x,f,ensure_ascii=False,indent=2); f.write('\n')
    inputs=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(SRC.iterdir()) if p.is_file()]
    book,cells=workbook(); samples=geo(); matrix=matrices(samples)
    save('input_inventory.json',inputs);save('workbook_inventory.json',book)
    with (args.output/'workbook_cells.tsv').open('x',encoding='utf-8',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n')
        w.writerow(['sheet','cell','type','source_value','style','formula']);w.writerows(cells)
    save('geo_library_qualification.json',samples);save('matrix_inventory.json',matrix)
    save('qualification_checks.json',dict(workbook_sheet_count=len(book['sheets']),library_count=len(samples),
        archive_member_count=len(matrix['members']),geo_biosample_sra_join='passed',
        matrix_dimensions_match_unique_identifiers='passed',biological_unit_qualification='unknown for coculture libraries',
        effect_analyses_executed=False))
    print('Source qualification completed; biological effects not analyzed.')

if __name__=='__main__': main()

