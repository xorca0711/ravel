"""Structural source qualification only; no biological hypothesis tests."""
from pathlib import Path
import argparse,csv,gzip,json,re,hashlib

def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args()
    out=Path(args.output); raw=Path('raw_data/nam_memory_2026')
    rows=[]
    for p in sorted(raw.glob('GSM*.txt')):
        t=p.read_text(); row={'gsm':p.stem}
        for key in ['title','last_update_date','source_name_ch1']:
            m=re.search(r'^!Sample_'+key+r' = (.*)',t,re.M);row[key]=m.group(1) if m else ''
        row['characteristics']=' | '.join(re.findall(r'^!Sample_characteristics_ch1 = (.*)',t,re.M))
        row['relations']=' | '.join(re.findall(r'^!Sample_relation = (.*)',t,re.M))
        row['unit_status']='unknown animal/pool mapping; GSM denotes library'
        rows.append(row)
    with (out/'sample_map.tsv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
    features=[]
    for p in sorted(raw.glob('*features.tsv.gz')):
        with gzip.open(p,'rt') as f: rr=list(csv.reader(f,delimiter='\t'))
        types=sorted(set(r[2] for r in rr));features.append({'file':p.name,'rows':len(rr),'feature_types':types,'sha256':digest(p)})
    matrices=[]
    for p in sorted(raw.glob('*matrix.mtx.gz')):
        with gzip.open(p,'rt') as f:
            header=next(line.strip() for line in f if not line.startswith('%'))
        nfeat,ncell,nnz=map(int,header.split())
        matrices.append({'file':p.name,'features':nfeat,'barcodes':ncell,'nonzero_entries':nnz,'sha256':digest(p)})
    bins=[]
    for p in sorted(raw.glob('*ExonCounts.txt.gz')):
        with gzip.open(p,'rt') as f: ids=[line.split('\t')[0] for line in f]
        biological=[x for x in ids if x.startswith('ENSMUSG')]
        bins.append({'file':p.name,'rows':len(ids),'distinct_ids':len(set(ids)),'ensembl_bin_rows':len(biological),'gene_prefixes':len(set(x.split(':')[0] for x in biological)),'non_gene_ids':[x for x in ids if not x.startswith('ENSMUSG')][:20],'sha256':digest(p)})
    tags=[]
    for p in sorted(raw.glob('*feature_reference.csv')):
        with p.open() as f:rr=list(csv.DictReader(f))
        tags.append({'file':p.name,'rows':len(rr),'columns':list(rr[0]),'labels':sorted(set(r.get('multiplexed_sample','') for r in rr))})
    result={'analysis':'metadata only','sample_records':len(rows),'features':features,'matrices':matrices,'bulk_exon_bins':bins,'cmo_references':tags,'animal_independence':'unresolved','atac_counts':'not deposited among inspected supplementary files; peak calls are not read counts','source_methods':'GEO ATAC processing and paper methods disagree; no silent version reconciliation','scRNA_condition_batch':'one expression GSM per condition; condition and library confounded','biological_acceptance':'not_assessed'}
    (out/'source_qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'retrieval_manifest.json').write_text((raw/'downloads.json').read_text())
    (out/'access_recovery.json').write_text((raw/'access_recovery.json').read_text())
    print(json.dumps({'sample_records':len(rows),'matrix_dimensions':matrices,'unit_status':'unknown'}))
if __name__=='__main__':main()
