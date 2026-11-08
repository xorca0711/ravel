"""Independent scalar check from raw tables; no production imports."""
import argparse
import csv
import gzip
import json
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path


def d(s):
    try:
        x=Decimal(str(s))
        return x if x.is_finite() else None
    except InvalidOperation: return None


def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))


def main(run):
    raw=Path('raw_data/Saxton_extensions_20261108');reference={};checks=0
    for recorded in read(run/'source_estimates.csv'):
        with gzip.open(raw/recorded['source_file'],'rt',encoding='utf-8') as f:
            rows=csv.reader(f,delimiter='\t');header=next(rows)
            matches=[r for r in rows if r[0]==recorded['gene_id']]
        assert len(matches)==1
        r=matches[0];assert r[7]==recorded['gene'];a,b,fc=map(d,[r[1],r[2],r[3]])
        with localcontext() as c:
            c.prec=35
            ratio=(a.ln()-b.ln())/Decimal(2).ln() if a is not None and b is not None and a>0 and b>0 else None
        expected={'stimulated_value':a,'control_value':b,'reported_log2foldchange':fc,'log2_positive_pair_ratio':ratio}
        for name,truth in expected.items():
            observed=d(recorded[name]);assert (truth is None)==(observed is None)
            if truth is not None:assert abs(truth-observed)<=Decimal('1e-10')
            checks+=1
        reference[recorded['gene'],recorded['source_block'],recorded['ligand'],Decimal(recorded['dose_nM'])]=expected
    deltas={}
    for r in read(run/'block_contrasts.csv'):
        gene,block,dose,metric=r['gene'],r['source_block'],Decimal(r['dose_nM']),r['measure']
        a=reference[gene,block,'R5D',dose][metric];b=reference[gene,block,'WTD',dose][metric]
        truth=a-b if a is not None and b is not None else None;obs=d(r['difference'])
        assert (truth is None)==(obs is None)
        if truth is not None:assert abs(truth-obs)<=Decimal('1e-10')
        deltas[gene,block,dose,metric]=truth;checks+=1
    for r in read(run/'summaries.csv'):
        xs=[deltas[r['gene'],b,Decimal(r['dose_nM']),r['measure']] for b in r['source_blocks'].split(';')]
        ok=all(x is not None for x in xs);assert ok==(r['supported']=='True')
        for field,truth in [('mean_difference',sum(xs)/Decimal(len(xs)) if ok else None),
                            ('min_block_difference',min(xs) if ok else None),('max_block_difference',max(xs) if ok else None)]:
            obs=d(r[field]);assert (truth is None)==(obs is None)
            if truth is not None:assert abs(truth-obs)<=Decimal('1e-10')
            checks+=1
    record=dict(ok=True,scalar_checks=checks,source_records=len(reference),method='direct raw-file stable-ID lookup and Decimal arithmetic/logarithms; no production imports',absolute_tolerance='1e-10',limits='same-source numerical verification, not independent biological replication or normalization validation')
    (run/'verification.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(record))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);main(p.parse_args().run)
