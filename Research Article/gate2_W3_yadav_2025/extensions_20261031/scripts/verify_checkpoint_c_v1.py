"""Independent source-level verification for the frozen C metadata output."""
import csv,gzip,json,re,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
CACHE=ROOT/'raw_data/Yd1_checkpoint_c_20261031'
OUT=ROOT/'analysis/research/runs/Yd1_extension_c_v1'
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def main():
    samples=read(OUT/'sample_library_map.csv');expected=[]
    for gse in ['GSE145230','GSE188288']:
        expected+=re.findall(r'^!Series_sample_id = (GSM\d+)$',(CACHE/(gse+'.txt')).read_text(),re.M)
    assert sorted(r['GSM'] for r in samples)==sorted(expected)
    for row in samples:
        text=(CACHE/(row['GSM']+'.txt')).read_text()
        assert '!Sample_title = '+row['title']+'\n' in text
        assert row['BioSample'] in text and row['SRA_experiment'] in text
        for key,pattern in [('sex',r'^!Sample_characteristics_ch1 = (?:Sex|gender): (.+)$'),('age',r'^!Sample_characteristics_ch1 = age: (.+)$')]:
            match=re.search(pattern,text,re.M)
            assert row[key]==(match.group(1) if match else ''),(row['GSM'],key)
        assert row['donor_id']==''
    features=read(OUT/'target_feature_support.csv');known=0
    for row in features:
        if row['feature_file']:
            with gzip.open(CACHE/row['feature_file'],'rt') as f:lines=f.read().splitlines()
            found=[(i+1,x.split('\t')[0]) for i,x in enumerate(lines) if x.split('\t')[1]==row['target']]
            assert row['feature_rows']==str(len(lines))
            assert row['matched_rows']==str(len(found))
            assert row['row_1based']==';'.join(str(i) for i,g in found)
            assert row['feature_ids']==';'.join(g for i,g in found)
            known+=1
        else:assert row['feature_rows']=='' and row['matched_rows']==''
        assert row['expression_read']=='False'
    inventory=read(OUT/'file_inventory.csv');look={}
    for p in CACHE.glob('*_filelist.txt'):
        for line in p.read_text().splitlines()[1:]:
            v=line.split('\t');look[v[1]]=int(v[3])
    assert {r['filename']:int(r['listed_bytes']) for r in inventory}==look
    for row in read(OUT/'state_denominator_coverage.csv'):
        assert all(row[k]=='' for k in ['author_retained_barcodes','author_state_field','author_state_assignments','complete_target_zero_denominator'])
    maps=read(OUT/'sequencing_run_map.csv')
    raw_runs={r['Run']:r for p in CACHE.glob('*_runinfo.csv') for r in read(p)}
    assert set(raw_runs)=={r['Run'] for r in maps}
    for row in maps:
        for k in ['Experiment','BioSample','LibraryName','Subject_ID']:
            assert row[k]==raw_runs[row['Run']][k]
    summary=json.loads((OUT/'source_decision.json').read_text())
    assert summary['expression_container_accessed'] is False and summary['target_expression_calculated'] is False
    print(json.dumps(dict(source_samples_checked=len(samples),feature_target_rows_checked=len(features),feature_rows_with_source_files=known,listed_file_sizes_checked=len(inventory),sequencing_runs_checked=len(maps),unknown_denominators_preserved=True)))
if __name__=='__main__':main()
