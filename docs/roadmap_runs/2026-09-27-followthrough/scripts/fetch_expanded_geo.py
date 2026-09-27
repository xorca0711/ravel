import concurrent.futures,datetime,gzip,hashlib,json,urllib.request,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/roadmap_runs/2026-09-27-followthrough'
(OUT/'metadata').mkdir(parents=True,exist_ok=True)
SERIES=sys.argv[1:] or ['GSE262927','GSE243124','GSE243135','GSE252588','GSE129605','GSE132771']
def one(acc):
    url=f'https://ftp.ncbi.nlm.nih.gov/geo/series/{acc[:-3]}nnn/{acc}/soft/{acc}_family.soft.gz'
    raw=urllib.request.urlopen(url,timeout=60).read(5000000)
    assert len(raw)<5000000
    lines=gzip.decompress(raw).decode('utf-8').splitlines();series={};samples=[];obj=series
    for line in lines:
        if line.startswith('^SAMPLE = '):obj={'accession':line.split(' = ',1)[1]};samples.append(obj)
        if ' = ' in line and line.startswith(('!Series_','!Sample_')):
            key,val=line.split(' = ',1)
            if any(x in key for x in ['contact','relation','status','submission','update','platform_id','data_row_count']):continue
            obj.setdefault(key,[]).append(val)
    data={'accession':acc,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_sha256':hashlib.sha256(raw).hexdigest(),'series':series,'samples':samples}
    (OUT/'metadata'/f'{acc}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    return {'accession':acc,'samples':len(samples),'title':series.get('!Series_title'),'design':series.get('!Series_overall_design'),'sample_titles':[s.get('!Sample_title') for s in samples[:3]],'supplements':series.get('!Series_supplementary_file')}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for result in pool.map(one,SERIES):print(json.dumps(result),flush=True)
