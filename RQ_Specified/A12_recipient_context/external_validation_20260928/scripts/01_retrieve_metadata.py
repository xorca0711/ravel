"""Retrieve GEO annotation metadata only; never opens an expression matrix."""
import gzip, hashlib, json, urllib.request
from pathlib import Path
from datetime import datetime, timezone
BASE = Path(__file__).resolve().parents[1]
ACCESSIONS = ['GSE131907', 'GSE123902', 'GSE148071']
records = []
for accession in ACCESSIONS:
    url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{accession[:-3]}nnn/{accession}/soft/{accession}_family.soft.gz'
    path = BASE / 'sources' / f'{accession}_family.soft.gz'
    if not path.exists():
        with urllib.request.urlopen(url, timeout=45) as response:
            data = response.read(8_000_001)
        if len(data) > 8_000_000:
            raise RuntimeError('Metadata download exceeds expected size')
        text = gzip.decompress(data).decode('utf-8')
        if '^SERIES = ' + accession not in text:
            raise RuntimeError('Unexpected GEO metadata response')
        path.write_bytes(data)
    data = path.read_bytes()
    text = gzip.decompress(data).decode('utf-8')
    samples, series, current = [], {}, None
    fields = {'title','geo_accession','source_name_ch1','organism_ch1','characteristics_ch1','data_processing','supplementary_file','relation','platform_id'}
    for line in text.splitlines():
        if line.startswith('^SAMPLE = '):
            current = {'accession': line.split(' = ',1)[1]}; samples.append(current)
        elif line.startswith('!Series_') and ' = ' in line:
            key,value = line[len('!Series_'):].split(' = ',1)
            if key in {'title','summary','overall_design','pubmed_id','supplementary_file','sample_id'}:
                series.setdefault(key,[]).append(value)
        elif current is not None and line.startswith('!Sample_') and ' = ' in line:
            key,value = line[len('!Sample_'):].split(' = ',1)
            if key in fields:
                current.setdefault(key,[]).append(value)
    extracted = BASE / 'sources' / f'{accession}_metadata.json'
    extracted.write_text(json.dumps({'accession':accession,'series':series,'samples':samples},indent=2)+'\n',encoding='utf-8')
    records.append({'accession':accession,'url':url,'metadata_file':str(path.relative_to(BASE)),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'samples':len(samples),'extracted_sha256':hashlib.sha256(extracted.read_bytes()).hexdigest()})
(BASE/'sources/retrieval_manifest.json').write_text(json.dumps({'retrieved_utc':datetime.now(timezone.utc).isoformat(),'expression_opened':False,'records':records},indent=2)+'\n',encoding='utf-8')
print(json.dumps(records))
