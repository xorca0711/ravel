"""Sx22 R1 source/matrix audit. Standard library only; no expression contrasts."""
import argparse,csv,gzip,hashlib,io,json,math,re,sys
from collections import Counter
from pathlib import Path

def samples_from_soft(text):
    rows=[]
    for block in text.split('^SAMPLE = ')[1:]:
        gsm=block.splitlines()[0].strip()
        def field(key):
            a=[x.split(' = ',1)[1] for x in block.splitlines() if x.startswith(key+' = ')]
            return a
        title=field('!Sample_title')[0]
        treatment=[x.split(': ',1)[1] for x in field('!Sample_characteristics_ch1') if x.startswith('treatment: ')][0]
        bs=[x.rsplit('/',1)[1] for x in field('!Sample_relation') if x.startswith('BioSample: ')][0]
        rows.append(dict(gsm=gsm,column=title,treatment=treatment,biosample=bs))
    for k in ['gsm','column','biosample']:
        if len({x[k] for x in rows})!=len(rows): raise ValueError('Duplicate '+k)
    if Counter(x['treatment'] for x in rows)!=Counter({'PBS':2,'WT IL-22':2,'22-B3':2}): raise ValueError('Unexpected design')
    return rows

def read_table(path):
    with gzip.open(path,'rt',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f,delimiter='\t'); fields=reader.fieldnames; rows=list(reader)
    return fields,rows

def write_csv(path,rows):
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def valid_count(value):
    x=float(value)
    if not math.isfinite(x) or x<0 or x!=int(x): raise ValueError('Invalid count: '+value)
    return int(x)

def main(out):
    c=Path('raw_data/Sx22'); out=Path(out);out.mkdir(exist_ok=True,parents=True)
    samples=samples_from_soft(gzip.decompress((c/'GSE160217_family.soft.gz').read_bytes()).decode())
    columns=[s['column'] for s in samples]
    cf,counts=read_table(c/'GSE160217_060120_22_readcount_genename.xls.gz')
    ff,fpkm=read_table(c/'GSE160217_060120_22_fpkm_genename.xls.gz')
    if cf!=ff or any(x not in cf for x in columns): raise ValueError('Column mismatch')
    if [x['geneID'] for x in counts]!=[x['geneID'] for x in fpkm]: raise ValueError('Gene order mismatch')
    ids=Counter(x['geneID'] for x in counts);symbols=Counter(x['Gene_name'] for x in counts)
    if any(v!=1 for v in ids.values()): raise ValueError('Duplicate Ensembl ID')
    for a,b in zip(counts,fpkm):
        if any(a[k]!=b[k] for k in cf if k not in columns):raise ValueError('Annotation disagreement')
    qc=[];all_vectors=[]
    for sample in samples:
        col=sample['column'];v=[valid_count(x[col]) for x in counts];all_vectors.append(v)
        fv=[float(x[col]) for x in fpkm]
        if any(not math.isfinite(x) or x<0 for x in fv):raise ValueError('Invalid FPKM')
        total=sum(v)
        if total==0:raise ValueError('Empty library')
        sample.update(biological_unit='source-reported independent colon sample',reported_n_per_group=2,mouse_id='not deposited',paired='no')
        qc.append(dict(column=col,treatment=sample['treatment'],total_counts=total,genes_nonzero=sum(x>0 for x in v),top10_count_fraction=sum(sorted(v,reverse=True)[:10])/total))
    if len({tuple(x) for x in all_vectors})<6:raise ValueError('Identical libraries')
    gene_qc=[dict(gene_id=x['geneID'],symbol=x['Gene_name'],symbol_rows=symbols[x['Gene_name']],all_zero=all(valid_count(x[k])==0 for k in columns)) for x in counts]
    summary=dict(n_rows=len(counts),sample_count=len(samples),duplicates_ensembl=0,duplicate_nonempty_symbols=sum(v>1 for k,v in symbols.items() if k),all_zero_rows=sum(x['all_zero'] for x in gene_qc),count_scale='nonnegative integers',annotation='deposited mm10; exact release unknown',group_mapping='GEO treatment attributes',independence='two biological samples per group reported in Methods; no separate mouse IDs/batch',numerical_model_eligible='conditional on source-reported independent biological units; no verified pairing',exclusions='none')
    write_csv(out/'samples.csv',samples);write_csv(out/'library_qc.csv',qc);write_csv(out/'gene_qc.csv',gene_qc)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'environment.txt').write_text(sys.version+'\nstandard library only\n')
    print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();main(a.output)
