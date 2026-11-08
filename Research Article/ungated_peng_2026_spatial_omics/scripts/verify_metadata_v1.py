"""Independent implementation: raw SOFT regex blocks, CSV joins, no parser imports."""
import argparse
import csv
import gzip
import itertools
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / 'raw_data/peng_spatial_20261108'
C3 = ROOT / 'Research Article/gate2_C3_yu_lee_choi_min_2026/trials'


def csv_read(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def verify(run):
    checks = []
    def check(name, ok):
        checks.append(dict(check=name, passed=bool(ok)))
        if not ok:
            raise ValueError(f'Independent verification failed: {name}')

    rows = csv_read(run / 'samples.csv')
    observed = {r['GSM']: r for r in rows}
    raw, aliases = {}, {}
    expected = {'GSE307534': (56,25), 'GSE308103': (75,23), 'GSE307529': (54,25)}
    for gse, (n, npatient) in expected.items():
        text = gzip.decompress((RAW / f'{gse}_family.soft.gz').read_bytes()).decode()
        blocks = re.findall(r'^\^SAMPLE = (GSM\d+)\r?\n(.*?)(?=^\^|\Z)', text, re.M | re.S)
        check(f'{gse}: known exposed sample count', len(blocks)==n)
        aliases[gse] = {}
        for gsm, body in blocks:
            def field(key):
                return re.findall(r'^!Sample_'+key+r' = (.*)$',body,re.M)[0].strip()
            title = field('title')
            alias = re.findall(r'^!Sample_description = Library name: (.*)$',body,re.M)[0].strip()
            patient = title.split('patient ')[1].split()[0]
            hist = next((h for h in ['AAH','AIS','MIA','LUAD'] if f' {h} ' in title), 'Normal')
            raw[gsm] = dict(GSE=gse, alias=alias, patient=patient, hist=hist)
            check(f'{gsm}: unique raw library alias', alias not in aliases[gse])
            aliases[gse][alias] = gsm
            rr=observed[gsm]
            check(f'{gsm}: fields from independent raw extraction',
                  rr['library_name_author']==alias and rr['title_author']==title
                  and rr['patient_id_author']==patient and rr['histology_deposited']==hist
                  and rr['GSE']==gse and alias.split('_',1)[0]=='P'+patient)
            suffix = alias.split('-',1)[1] if '-' in alias else ''
            check(f'{gsm}: suffix preserved', rr['library_alias_suffix']==('-'+suffix if suffix else ''))
            urls = re.findall(r'^!Sample_supplementary_file_\d+ = (.*)$',body,re.M)
            check(f'{gsm}: explicit alias agrees with supplementary filename',
                  any(gsm+'_'+alias+'.' in url or gsm+'_'+alias+'_' in url for url in urls))
            for key in ['age','sex','smoking','ethnicity']:
                v = re.findall(r'^!Sample_characteristics_ch1 = '+key+r': (.*)$',body,re.M|re.I)[0].strip()
                check(f'{gsm}: {key} verbatim', rr[key]==v)
        check(f'{gse}: known exposed patient count', len({v['patient'] for v in raw.values() if v['GSE']==gse})==npatient)
    check('GSM uniqueness/completeness', len(rows)==len(observed)==len(raw) and set(observed)==set(raw))
    check('No fabricated Xenium records', {r['platform'] for r in rows}=={'Visium','snRNA-seq','WES'})
    check('Unavailable identities remain empty', all(not r[k] for r in rows for k in
        ['lesion_id_author','block_id','section_id','ROI_id','core_id','cell_or_spot_id','coordinate_frame','histology_original','histology_reviewed']))

    cross = csv_read(run/'crosswalk.csv')
    keys = {(r['source_GSE'],r['target_GSE'],r['library_name_author']) for r in cross}
    expected_keys=set()
    for a,b in itertools.combinations(expected,2):
        for alias in set(aliases[a])|set(aliases[b]):
            expected_keys.add((a,b,alias))
    check('Crosswalk union cardinality and uniqueness', keys==expected_keys and len(cross)==len(keys))
    for r in cross:
        a,b,alias = r['source_GSE'],r['target_GSE'],r['library_name_author']
        check(f'{a}/{b}/{alias}: exact matches and missing counterparts',
              r['source_GSM']==aliases[a].get(alias,'') and r['target_GSM']==aliases[b].get(alias,''))
        check(f'{a}/{b}/{alias}: no promoted specimen join',
              r['lesion_relationship']==r['block_relationship']==r['serial_section_relationship']=='unverified')
    patients=csv_read(run/'patients.csv')
    check('Patient rows unique and complete', len(patients)==25 and len({r['patient_id_author'] for r in patients})==25)
    for p in patients:
        for g in expected:
            actual=set(p[g].split('|')) if p[g] else set()
            want={gsm for gsm,v in raw.items() if v['GSE']==g and v['patient']==p['patient_id_author']}
            check(f'Patient {p["patient_id_author"]}/{g}: membership',actual==want)
        pp=[r for r in rows if r['patient_id_author']==p['patient_id_author']]
        consistent=all(len({r[k].lower() for r in pp})==1 for k in ['age','sex','smoking','ethnicity'])
        check(f'Patient {p["patient_id_author"]}: demographic status',p['demographic_consistency']==str(consistent).lower())

    old=csv_read(C3/'u5_spatial_context/RNA_spatial_demographic_crosswalk.csv')
    check('C3 demographic GSM coverage exact', {r['gsm'] for r in old}=={g for g,r in raw.items() if r['GSE']!='GSE307529'})
    check('C3 RNA library coverage exact', {r['gsm'] for r in csv_read(C3/'u5_human_full/library_qc_and_annotation.csv')}==set(aliases['GSE308103'].values()))
    check('C3 three-series audit GSM coverage',
          {r['gsm'] for r in csv_read(C3/'u0_geo_design_audit/sample_inventory.csv') if r['series'] in expected}==set(raw))
    prior=csv_read(run/'prior_inventory_comparison.csv')
    # Verify disagreement reporting against independent source/field comparisons.
    for r in prior:
        old_rows=[x for x in csv_read(ROOT/r['source']) if x.get('gsm')==r['GSM']]
        check(f'{r["source"]}/{r["GSM"]}: prior key unique',len(old_rows)==1)
        oldrow=old_rows[0];new=observed[r['GSM']]
        mapping={'series':'GSE','patient_label':'patient_id_author','patient':'patient_id_author','title':'title_author',
                 'age':'age','sex':'sex','smoking':'smoking','ethnicity':'ethnicity','histology':'histology_deposited','histology_from_title':'histology_deposited'}
        diff=any(oldrow.get(k) and oldrow[k].lower()!=new[v].lower() for k,v in mapping.items())
        check(f'{r["source"]}/{r["GSM"]}: disagreement retained',(r['status']=='disagreement')==diff)
    summary=json.loads((run/'summary.json').read_text())
    for g,(n,np) in expected.items():
        check(f'{g}: summary counts',summary['series'][g]['records']==n and summary['series'][g]['patient_labels']==np)
        check(f'{g}: summary histology',summary['series'][g]['histology_deposited']==dict(Counter(r['hist'] for r in raw.values() if r['GSE']==g)))
    paper=(RAW/'pmc_article.html').read_text(encoding='utf8')
    check('Published WES denominator source literal present', bool(re.search(r'total samples\s*=\s*79',paper)))
    check('P7 case review source literal present','P7 with 2 LUADs' in paper)
    result=dict(status='passed', method='Separately implemented raw-block regex extraction and CSV/set arithmetic; no production parser imports',
                checks=len(checks), failures=[], covered=['GSM and patient counts','suffixes','filename aliases','demographics',
                'join union/cardinality','C3 coverage and disagreements','unknown identity preservation','published WES/P7 locators'],
                limit='Same source numerical verification, not independent biological replication or human scientific acceptance')
    with (run/'verification.json').open('x',encoding='utf8',newline='\n') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True)
    verify(p.parse_args().run)
