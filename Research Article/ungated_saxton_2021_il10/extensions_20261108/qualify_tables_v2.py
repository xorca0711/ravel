"""Qualify published per-comparison tables; do not compute effects."""
import argparse
import csv
import gzip
import json
import math
import re
from pathlib import Path

RAW = Path('raw_data/Saxton_extensions_20261108')
TARGETS = {'IFNG':'ENSG00000111537','GZMB':'ENSG00000100453','IL18RAP':'ENSG00000115607'}


def finite(s):
    try: return math.isfinite(float(s))
    except (TypeError, ValueError): return False


def main(out):
    files = sorted(RAW.glob('GSM*_D*_*genes.DEA.txt.gz'))
    assert len(files) == 12
    tables, mapping, seen = [], [], set()
    for path in files:
        m = re.fullmatch(r'(GSM\d+)_(D\d+)(WTD50|R5D50|WTD01|R5D01)_vs_(D\d+)US.genes.DEA.txt.gz',path.name)
        assert m and m[2] == m[4], 'Unexpected source naming'
        gsm, block, treatment = m[1], m[2], m[3]
        assert (block,treatment) not in seen
        seen.add((block,treatment))
        stem, ctrl = block+treatment+'.value',block+'US.value'
        ids, target_rows, rows, missing_estimates = set(), [], 0, 0
        with gzip.open(path,'rt',encoding='utf-8') as f:
            reader=csv.DictReader(f,delimiter='\t')
            assert reader.fieldnames==['Gene',stem,ctrl,'log2foldchange','pvalue','padjust','significance','gene_name','gene_description']
            for row in reader:
                rows+=1
                assert row['Gene'] not in ids, 'Repeated stable ID'
                ids.add(row['Gene'])
                missing_estimates+=not finite(row['log2foldchange'])
                if row['gene_name'] in TARGETS:
                    gene=row['gene_name'];assert row['Gene']==TARGETS[gene]
                    target_rows.append(gene)
                    mapping.append(dict(file=path.name,gsm=gsm,source_block=block,treatment=treatment,
                                        gene=gene,gene_id=row['Gene'],estimate_finite=finite(row['log2foldchange']),
                                        stimulated_finite=finite(row[stem]),control_finite=finite(row[ctrl])))
        assert sorted(target_rows)==sorted(TARGETS), 'Missing or ambiguous fixed target'
        tables.append(dict(file=path.name,gsm=gsm,source_block=block,treatment=treatment,rows=rows,
                           unique_ids=len(ids),nonfinite_reported_estimates=missing_estimates))
    assert seen=={(b,t) for b in ['D85','D93','D36'] for t in ['WTD50','R5D50','WTD01','R5D01']}
    for name,data in [('tables.csv',tables),('target_mapping.csv',mapping)]:
        with (out/name).open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    result=dict(tables=len(tables),fixed_target_records=len(mapping),
                finite_target_estimates=sum(r['estimate_finite'] for r in mapping),
                comparison_estimate_description_eligible=all(r['estimate_finite'] for r in mapping),
                common_expression_matrix='held: differing repeated controls and literal NA, v1 retained',
                endpoint='deposited log2foldchange estimates, not raw-count or common-RPKM contrasts',
                donor_status='author-reported donors; source blocks D85/D93/D36, external donor identity not verified',
                limit='unknown fit/normalization, six-day context, no population inference or independent replication claim')
    (out/'qualification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
