"""Arz1 source/structure qualification only; no biological contrasts or state calls."""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse,csv,gzip,hashlib,json,math,os
from pathlib import Path
import sys,xml.etree.ElementTree as ET,zipfile
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,os.environ.get('ARZ1_H5PY_PATH',str(ROOT/'.tools/sx22_e1a_runtime')))
import h5py


def require(ok,message):
    if not ok:raise ValueError(message)


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1048576):h.update(chunk)
    return h.hexdigest()


def fingerprint(strings):return hashlib.sha256('\n'.join(strings).encode()).hexdigest()


def write_csv(path,rows,fields):
    with path.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)


def write_json(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')


def soft_records(path):
    records=[];current=None
    with gzip.open(path,'rt',encoding='utf-8') as f:
        for line in f:
            line=line.rstrip('\r\n')
            if line.startswith('^'):
                kind,identifier=line[1:].split(' = ',1);current=dict(kind=kind,id=identifier,fields=defaultdict(list));records.append(current)
            elif current is not None and line.startswith('!') and ' = ' in line:
                key,value=line[1:].split(' = ',1);current['fields'][key].append(value)
    require(records,'Empty SOFT record');return records


def feature_info(ids,names,types,barcodes):
    require(len(ids)==len(names)==len(types)>0,'Feature dimension mismatch')
    require(len(set(ids))==len(ids),'Duplicate feature IDs')
    require(len(set(barcodes))==len(barcodes)>0,'Empty or duplicated barcodes')
    require(all(ids) and all(barcodes),'Blank feature or barcode ID')
    counts=Counter(types);by_type={t:{ids[i] for i,v in enumerate(types) if v==t} for t in counts}
    return dict(n_features=len(ids),n_barcodes=len(barcodes),feature_id_sha256=fingerprint(ids),
                barcode_sha256=fingerprint(barcodes),feature_types=dict(counts)),by_type


def h5_metadata(path):
    schema=[]
    with h5py.File(path,'r') as f:
        def visit(name,node):
            if isinstance(node,h5py.Dataset):schema.append(dict(path=name,shape=list(node.shape),dtype=str(node.dtype)))
        f.visititems(visit)
        m=f['matrix'];g=m['features'];shape=tuple(int(v) for v in m['shape'][:])
        ids=g['id'].asstr()[:].tolist();names=g['name'].asstr()[:].tolist();types=g['feature_type'].asstr()[:].tolist()
        barcodes=m['barcodes'].asstr()[:].tolist();info,by_type=feature_info(ids,names,types,barcodes)
        require(shape==(len(ids),len(barcodes)),'H5 declared shape mismatch')
        ptr=m['indptr'][:].astype(np.int64);nnz=len(m['data'])
        require(len(ptr)==len(barcodes)+1 and ptr[0]==0 and ptr[-1]==nnz and (np.diff(ptr)>=0).all(),'Invalid CSC pointers')
        require(len(m['indices'])==nnz,'Sparse lengths disagree')
        boundaries=set(map(int,ptr));previous=None;strict=True
        seen={t:np.zeros(len(barcodes),dtype=bool) for t in by_type};typecodes={t:i for i,t in enumerate(by_type)}
        codes=np.array([typecodes[t] for t in types],dtype=np.uint8)
        for start in range(0,nnz,500000):
            stop=min(start+500000,nnz);values=m['data'][start:stop];indices=m['indices'][start:stop].astype(np.int64)
            require(np.isfinite(values).all() and (values>=0).all() and (values==np.floor(values)).all(),'Invalid count values')
            require((indices>=0).all() and (indices<len(ids)).all(),'Sparse row out of bounds')
            diffs=np.diff(np.r_[previous,indices]) if previous is not None else np.diff(indices)
            offset=start if previous is not None else start+1
            strict &= all(int(i)+offset in boundaries for i in np.flatnonzero(diffs<=0));previous=indices[-1] if len(indices) else previous
            cols=np.searchsorted(ptr,np.arange(start,stop),side='right')-1
            for t,code in typecodes.items():seen[t][np.unique(cols[(codes[indices]==code)&(values>0)])]=True
        require(strict,'Duplicate or unsorted H5 coordinates within a column')
        info.update(n_stored_entries=nnz,coordinate_uniqueness='verified_strict_CSC',numeric_integrity='finite_nonnegative_integer',
                    barcode_axis='one shared matrix column axis',observed_both_RNA_ATAC=int((seen.get('Gene Expression',np.zeros(len(barcodes),bool))&seen.get('Peaks',np.zeros(len(barcodes),bool))).sum()))
    return info,by_type,barcodes,schema


def mtx_metadata(matrix_path,feature_path,barcode_path):
    with gzip.open(feature_path,'rt',encoding='utf-8') as f:features=[line.rstrip('\r\n').split('\t') for line in f]
    require(all(len(r)>=3 for r in features),'Missing feature-type column')
    ids=[r[0] for r in features];names=[r[1] for r in features];types=[r[2] for r in features]
    with gzip.open(barcode_path,'rt',encoding='utf-8') as f:barcodes=[line.rstrip('\r\n') for line in f]
    info,by_type=feature_info(ids,names,types,barcodes)
    typecodes={t:i for i,t in enumerate(by_type)};codes=np.array([typecodes[t] for t in types],dtype=np.uint8)
    seen={t:np.zeros(len(barcodes),bool) for t in by_type};count=0;last_col=last_row=-1;col_order=row_order=True
    with gzip.open(matrix_path,'rt',encoding='utf-8') as f:
        header=f.readline().strip();require(header.lower() in ['%%matrixmarket matrix coordinate integer general','%%matrixmarket matrix coordinate real general'],'Unexpected MatrixMarket schema')
        line=f.readline()
        while line.startswith('%'):line=f.readline()
        nr,nc,nnz=map(int,line.split());require((nr,nc)==(len(ids),len(barcodes)),'MatrixMarket dimensions disagree')
        for line in f:
            if not line.strip():continue
            parts=line.split();require(len(parts)==3,'Malformed MatrixMarket entry')
            r,c=map(int,parts[:2]);value=float(parts[2]);require(1<=r<=nr and 1<=c<=nc and math.isfinite(value) and value>=0 and value.is_integer(),'Invalid sparse entry')
            colkey=(c-1)*nr+r-1;rowkey=(r-1)*nc+c-1
            col_order &= colkey>last_col;row_order &= rowkey>last_row;last_col=colkey;last_row=rowkey;count+=1
            if value>0:seen[types[r-1]][c-1]=True
    require(count==nnz,'MatrixMarket entry count mismatch')
    info.update(n_stored_entries=nnz,coordinate_uniqueness='verified_strict_column_order' if col_order else 'verified_strict_row_order' if row_order else 'not_verified_unsorted',
                numeric_integrity='finite_nonnegative_integer',barcode_axis='one shared matrix column axis',
                observed_both_RNA_ATAC=int((seen.get('Gene Expression',np.zeros(nc,bool))&seen.get('Peaks',np.zeros(nc,bool))).sum()))
    return info,by_type,barcodes,[]


def dense_metadata(path,kind,barcode_path=None):
    with gzip.open(path,'rt',encoding='utf-8',newline='') as f:
        reader=csv.reader(f,delimiter='\t');header=next(reader);prefix=1 if kind=='immune_DGE' else 3
        require(header[0]=='GENE' if kind=='immune_DGE' else header[:3]==['','gene_id','gene_name'],'Unexpected dense schema')
        columns=header[prefix:];require(len(columns)==len(set(columns)),'Duplicate dense columns');ids=set();rows=0;integer=True
        for row in reader:
            require(len(row)==len(header),'Dense row width mismatch');identifier=row[0] if prefix==1 else row[1]
            require(identifier not in ids and identifier!='','Duplicate/blank dense ID');ids.add(identifier);rows+=1
            values=np.asarray(row[prefix:],dtype=float);require(np.isfinite(values).all() and (values>=0).all(),'Invalid dense values')
            integer &= bool((values==np.floor(values)).all())
    matched=None
    if barcode_path:
        with gzip.open(barcode_path,'rt') as f:expected=[x.strip() for x in f]
        matched=columns==expected;require(matched,'Immune barcode list/order mismatch')
    return dict(n_rows=rows,n_measurement_columns=len(columns),columns=columns,nonnegative_finite=True,
                all_values_integer=integer,barcode_list_order_match=matched,identifier_set_sha256=fingerprint(sorted(ids)))


def workbook_text(path):
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};rows=[]
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
        rel={r.get('Id'):r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',ns):
            target=rel[sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            member=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            for cell in ET.fromstring(z.read(member)).findall('.//s:c',ns):
                typ=cell.get('t');value=cell.find('s:v',ns)
                text=strings[int(value.text)] if typ=='s' and value is not None else ''.join(cell.find('s:is',ns).itertext()) if typ=='inlineStr' else None
                if text is not None:rows.append(dict(sheet=sheet.get('name'),cell=cell.get('r'),text=text))
    return rows


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output).resolve();require(out.parent==ROOT/'analysis/research/runs' and out.is_dir(),'Fresh runner directory required')
    require(all(p.name in ['receipt.json','stdout.log','stderr.log'] for p in out.iterdir()),'Existing output artifacts')
    manifest=json.loads((PACKAGE/'sources/intake_v1.json').read_text(encoding='utf-8'))
    files=[]
    for r in manifest['files']:
        p=ROOT/r['path'];require(p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],'Source manifest mismatch: '+r['path'])
        files.append(r)
    write_csv(out/'file_manifest.csv',files,['path','bytes','sha256','kind'])
    series=[];samples=[];remote=[]
    for accession in manifest['accessions']:
        for record in soft_records(ROOT/manifest['source_directory']/(accession+'_family.soft.gz')):
            fields=record['fields']
            if record['kind']=='SERIES':
                series.append(dict(accession=record['id'],title=' | '.join(fields['Series_title']),
                    status=' | '.join(fields['Series_status']),last_update=' | '.join(fields['Series_last_update_date']),
                    overall_design=' | '.join(fields['Series_overall_design']),relations=' | '.join(fields['Series_relation'])))
            if record['kind']=='SAMPLE':
                samples.append(dict(accession=accession,sample=record['id'],title=' | '.join(fields['Sample_title']),
                    characteristics=json.dumps(fields['Sample_characteristics_ch1'],ensure_ascii=False),
                    source=' | '.join(fields['Sample_source_name_ch1']),library_strategy=' | '.join(fields['Sample_library_strategy']),
                    library_source=' | '.join(fields['Sample_library_source']),relations=' | '.join(fields['Sample_relation'])))
            for key,values in fields.items():
                if 'supplementary_file' in key:
                    for url in values:
                        remote.append(dict(accession=accession,record=record['id'],field=key,url=url,
                            acquired_basename=next((r['path'] for r in files if Path(r['path']).name==url.rsplit('/',1)[-1]),'')))
    write_csv(out/'series_records.csv',series,list(series[0]));write_csv(out/'sample_records.csv',samples,list(samples[0]))
    write_csv(out/'deposited_file_links.csv',remote,['accession','record','field','url','acquired_basename'])
    bios=[]
    for b in ET.parse(ROOT/manifest['source_directory']/'biosamples.xml').getroot().findall('BioSample'):
        attrs=[dict(name=a.get('attribute_name'),value=a.text) for a in b.findall('Attributes/Attribute')]
        geo=[i.text for i in b.findall('Ids/Id') if i.get('db')=='GEO']
        bios.append(dict(biosample=b.get('accession'),geo_samples=';'.join(geo),title=b.findtext('Description/Title'),
                         attributes=json.dumps(attrs,ensure_ascii=False),public_status=b.get('access')))
    for sample in samples:
        linked=[b for b in bios if sample['sample'] in b['geo_samples'].split(';')]
        require(len(linked)==1 and linked[0]['biosample'] in sample['relations'],'BioSample source crosswalk disagreement')
    write_csv(out/'biosample_crosswalk.csv',bios,list(bios[0]))
    matrices=[];feature_rows=[];schemas={};features={};barcodes={};holds=[]
    for spec in manifest['multiome_libraries']:
        for role,strategy in [('rna_sample','RNA-Seq'),('atac_sample','ATAC-seq')]:
            matches=[r for r in samples if r['sample']==spec[role] and r['accession']==spec['accession']]
            require(len(matches)==1 and matches[0]['library_strategy']==strategy,'Declared assay/sample map disagreement')
        name=spec['id'];row=dict(library=name,accession=spec['accession'],condition=spec['condition'],
                               source_format=spec['format'],rna_sample=spec['rna_sample'],atac_sample=spec['atac_sample'])
        try:
            paths=[ROOT/p for p in spec['paths']]
            info,ft,bc,schema=h5_metadata(paths[0]) if spec['format']=='h5' else mtx_metadata(*paths)
            features[name]=ft;barcodes[name]=bc;schemas[name]=schema
            for typ,ids in ft.items():feature_rows.append(dict(library=name,feature_type=typ,n_features=len(ids),identifier_set_sha256=fingerprint(sorted(ids))))
            row.update(status='structure_checked',**{k:v for k,v in info.items() if k!='feature_types'})
        except (ValueError,KeyError,OSError) as exc:
            row.update(status='held_input_structure',error=str(exc));holds.append(dict(component=name,error_type=type(exc).__name__,error=str(exc)))
        matrices.append(row);print('Metadata inspected: '+name,flush=True)
    matrix_fields=['library','accession','condition','source_format','rna_sample','atac_sample','status','n_features','n_barcodes',
                   'feature_id_sha256','barcode_sha256','n_stored_entries','coordinate_uniqueness','numeric_integrity','barcode_axis','observed_both_RNA_ATAC','error']
    write_csv(out/'matrix_inventory.csv',matrices,matrix_fields)
    write_csv(out/'feature_types.csv',feature_rows,['library','feature_type','n_features','identifier_set_sha256'])
    write_json(out/'h5_schema.json',schemas)
    overlap=[];fo=[]
    for first in features:
        for second in features:
            a=set(barcodes[first]);b=set(barcodes[second])
            overlap.append(dict(first=first,second=second,first_n=len(a),second_n=len(b),shared_barcodes=len(a&b),
                exact_order_match=barcodes[first]==barcodes[second],interpretation='Barcode whitelist reuse across libraries is not a cell/animal join'))
            for typ in sorted(set(features[first])|set(features[second])):
                a=features[first].get(typ,set());b=features[second].get(typ,set())
                fo.append(dict(first=first,second=second,feature_type=typ,first_n=len(a),second_n=len(b),shared_ids=len(a&b),identical_sets=a==b))
    write_csv(out/'barcode_overlap.csv',overlap,['first','second','first_n','second_n','shared_barcodes','exact_order_match','interpretation'])
    write_csv(out/'feature_overlap.csv',fo,['first','second','feature_type','first_n','second_n','shared_ids','identical_sets'])
    dense=[]
    for spec in manifest['dense_tables']:
        try:
            result=dense_metadata(ROOT/spec['path'],spec['kind'],ROOT/spec['barcodes'] if spec.get('barcodes') else None)
            dense.append(dict(id=spec['id'],status='structure_checked',**result))
        except (ValueError,KeyError,OSError) as exc:
            dense.append(dict(id=spec['id'],status='held_input_structure',error=str(exc)));holds.append(dict(component=spec['id'],error_type=type(exc).__name__,error=str(exc)))
    write_json(out/'dense_table_inventory.json',dense)
    labels=workbook_text(ROOT/manifest['source_directory']/'41467_2026_79014_MOESM4_ESM.xlsx')
    write_csv(out/'source_workbook_text_cells.csv',labels,['sheet','cell','text'])
    article=ET.parse(ROOT/manifest['source_directory']/'article_fulltext.xml').getroot()
    source_index=dict(title=''.join(article.find('front/article-meta/title-group/article-title').itertext()),
        identifiers=[dict(kind=x.get('pub-id-type'),value=x.text) for x in article.findall('front/article-meta/article-id')],
        section_locators=[dict(id=s.get('id'),title=''.join(s.find('title').itertext())) for s in article.iter('sec') if s.find('title') is not None],
        supplementary_files=sorted({m.get('{http://www.w3.org/1999/xlink}href') for s in article.iter('supplementary-material') for m in s.findall('media')}))
    write_json(out/'article_source_index.json',source_index)
    summary=dict(scope='Source and matrix-structure metadata only; no biological endpoint calculation',
                 n_series=len(series),n_sample_records=len(samples),n_biosample_records=len(bios),
                 n_multiome_library_records=len(matrices),n_structurally_checked_multiome=sum(r['status']=='structure_checked' for r in matrices),
                 structural_holds=holds,runtime=dict(python=sys.version,numpy=np.__version__,h5py=h5py.__version__),
                 interpretation='Shared axes and barcode/feature overlaps do not verify individual animals, state identities, donor deconvolution or longitudinal function joins',
                 biological_independence='unknown',scientific_acceptance='not_assessed')
    write_json(out/'summary.json',summary);print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
