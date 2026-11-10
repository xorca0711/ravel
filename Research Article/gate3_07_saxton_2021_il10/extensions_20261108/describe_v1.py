"""Describe fixed deposited estimates; no raw-count inference."""
import argparse
import csv
import gzip
import json
import math
import re
import statistics
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
RAW = Path('raw_data/Saxton_extensions_20261108')
TARGETS = {'IFNG':'ENSG00000111537','GZMB':'ENSG00000100453','IL18RAP':'ENSG00000115607'}
BLOCKS = ['D85','D93','D36']


def number(s):
    try:
        x=float(s)
        return x if math.isfinite(x) else None
    except (TypeError,ValueError): return None


def csvout(path, rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main(out):
    q=json.loads(Path('analysis/research/runs/sx10_gorby_qualification_v2/qualification.json').read_text())
    assert q['comparison_estimate_description_eligible']
    values={};source=[]
    for f in sorted(RAW.glob('GSM*_D*_*genes.DEA.txt.gz')):
        m=re.fullmatch(r'(GSM\d+)_(D\d+)(WTD|R5D)(50|01)_vs_\2US.genes.DEA.txt.gz',f.name)
        assert m
        gsm,block,ligand,dose=m.groups();stim=block+ligand+dose+'.value';ctrl=block+'US.value'
        with gzip.open(f,'rt',encoding='utf-8') as h:
            for row in csv.DictReader(h,delimiter='\t'):
                gene=row['gene_name']
                if gene not in TARGETS: continue
                assert row['Gene']==TARGETS[gene]
                a,b=number(row[stim]),number(row[ctrl]);reported=number(row['log2foldchange'])
                ratio=math.log2(a/b) if a is not None and b is not None and a>0 and b>0 else None
                r=dict(gene=gene,gene_id=row['Gene'],gsm=gsm,source_block=block,ligand=ligand,
                       dose_nM=0.1 if dose=='01' else 50,source_file=f.name,
                       stimulated_value=a,control_value=b,reported_log2foldchange=reported,
                       log2_positive_pair_ratio=ratio,low_abundance=(a is not None and a<1) or (b is not None and b<1))
                key=(gene,block,ligand,dose);assert key not in values
                values[key]=r;source.append(r)
    assert len(source)==36
    csvout(out/'source_estimates.csv',source)
    contrasts=[];summaries=[]
    for gene in TARGETS:
        for dose in ['01','50']:
            for measure in ['reported_log2foldchange','log2_positive_pair_ratio']:
                ds={}
                for block in BLOCKS:
                    w=values[gene,block,'WTD',dose][measure];r=values[gene,block,'R5D',dose][measure]
                    ds[block]=r-w if w is not None and r is not None else None
                    contrasts.append(dict(gene=gene,dose_nM=0.1 if dose=='01' else 50,measure=measure,source_block=block,
                                          WT_response=w,R5_response=r,difference=ds[block],supported=ds[block] is not None))
                for omitted in ['none']+BLOCKS:
                    blocks=[b for b in BLOCKS if b!=omitted];ok=all(ds[b] is not None for b in blocks)
                    summaries.append(dict(gene=gene,dose_nM=0.1 if dose=='01' else 50,measure=measure,omitted=omitted,
                                          source_blocks=';'.join(blocks),n_blocks=len(blocks),supported=ok,
                                          mean_difference=statistics.mean(ds[b] for b in blocks) if ok else None,
                                          min_block_difference=min(ds[b] for b in blocks) if ok else None,
                                          max_block_difference=max(ds[b] for b in blocks) if ok else None))
    csvout(out/'block_contrasts.csv',contrasts);csvout(out/'summaries.csv',summaries)
    result=dict(endpoint='difference of reported response estimates; no common expression matrix',
                targets=list(TARGETS),source_rows=len(source),block_contrasts=len(contrasts),summary_cases=len(summaries),
                primary=[r for r in summaries if r['measure']=='reported_log2foldchange' and r['omitted']=='none'],
                source_rows_low_abundance=sum(r['low_abundance'] for r in source),
                source_rows_ratio_unsupported=sum(r['log2_positive_pair_ratio'] is None for r in source),
                inference='finite source description; source donor-code identity and model/normalization limits retained')
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(BASE/'verify_description_v1.py'),'--run',str(out)],check=True)
    subprocess.run([sys.executable,str(BASE/'figures/gen_fig_gorby_reported_v1.py'),'--run',str(out)],check=True)
    print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
