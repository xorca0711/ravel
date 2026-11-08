"""Independent openpyxl verification; does not import the OOXML extraction code."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import openpyxl
from openpyxl.utils import get_column_letter as letter

ROOT=Path(__file__).resolve().parents[3]
RAW=ROOT/'raw_data/peng_supplements_20261108'
PREVIOUS=ROOT/'analysis/research/runs/Pg1_metadata_v3_20261108'
FEATURES=ROOT/'docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A12_FEATURE_MAP_V1.json'
ENDPOINT=ROOT/'docs/roadmap_runs/2026-09-27-followthrough/A12_pilot_specification.json'


def rows(path):
    with path.open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))


def equivalent(text,value):
    if value is None:return text==''
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        try:return float(text)==value
        except ValueError:return False
    if isinstance(value,bool):return text==str(int(value))
    return text==str(value)


def merged_value(sheet,address):
    for region in sheet.merged_cells.ranges:
        if address in region:
            a=region.start_cell.coordinate
            return sheet[a].value,a
    return sheet[address].value,address


def verify(run):
    checks=0;failures=[]
    def ck(name,condition):
        nonlocal checks
        checks+=1
        if not condition:failures.append(name)
    books={};cached={}
    for i in range(1,7):
        p=RAW/f'NIHMS2118436-supplement-{i+1}.xlsx'
        books[i]=openpyxl.load_workbook(p,data_only=False,read_only=False)
        cached[i]=openpyxl.load_workbook(p,data_only=True,read_only=False)
    def locator(i,s,a):return f'NIHMS2118436-supplement-{i+1}.xlsx#{s}!{a}'
    def at(loc):
        file,other=loc.split('#',1);sheet,a=other.rsplit('!',1)
        i=int(file.split('-')[-1].split('.')[0])-1
        return cached[i][sheet][a].value
    cells=rows(run/'source_cells.csv');observed={(r['table'],r['sheet'],r['cell']):r for r in cells};wanted=set()
    ck('Source-cell key uniqueness',len(cells)==len(observed))
    for i,w in books.items():
        for s in w:
            for row in s:
                for c in row:
                    if c.value is None:continue
                    key=(f'S{i}',s.title,c.coordinate);wanted.add(key);o=observed.get(key)
                    ck('Source cell retained '+str(key),o is not None)
                    if o:
                        formula=c.value if c.data_type=='f' else ''
                        value=cached[i][s.title][c.coordinate].value if formula else c.value
                        ck('Cell content '+str(key),equivalent(o['value_text'],value) and o['formula']==formula)
                        ck('Cell locator '+str(key),o['source_locator']==locator(i,s.title,c.coordinate))
    ck('Complete nonempty source cell set',set(observed)==wanted)
    manifest=rows(run/'sheet_manifest.csv')
    ck('Every supplied sheet inventoried',len(manifest)==sum(len(w.sheetnames) for w in books.values()))
    for r in manifest:
        s=books[int(r['table'][1:])][r['sheet']]
        ck('Merged ranges '+r['table']+r['sheet'],set(json.loads(r['merged_ranges']))=={str(m) for m in s.merged_cells.ranges})
    intake=json.loads((RAW/'intake_v1.json').read_text())
    for r in intake:ck('Source checksum '+r['file'],hashlib.sha256((RAW/r['file']).read_bytes()).hexdigest()==r['sha256'])

    clinical=rows(run/'discovery_clinical.csv');prior=rows(PREVIOUS/'samples.csv')
    ck('Clinical records are 25 distinct author labels',len(clinical)==len({r['patient_id_author'] for r in clinical})==25)
    for r in clinical:
        for key,source in json.loads(r['source_cells']).items():ck('Clinical cell '+source,equivalent(r[key],at(source)))
        ck('Clinical cohort distinct',r['cohort_id']=='Peng_discovery')
    cg=rows(run/'clinical_GEO_comparison.csv');by_gsm={r['GSM']:r for r in prior}
    ck('All GEO clinical comparisons retained',len(cg)==4*len(prior))
    for r in cg:
        v=str(at(r['source_locator'])).strip().lower()
        v={'f':'female','m':'male'}.get(v,v) if r['field']=='sex' else v
        v={'smoker':'yes','never smoker':'no'}.get(v,v) if r['field']=='smoking' else v
        old=by_gsm[r['GSM']][r['field']]
        ck('Clinical comparison '+r['GSM']+r['field'],r['GEO_value']==old and (r['comparison']=='agrees')==(v==old.strip().lower()))

    s=books[1]['Tab 2'];part=rows(run/'platform_participation.csv');pk={(r['platform'],r['patient_id_author'],r['histology_table']):r for r in part}
    ck('Participation full matrix',len(pk)==len(part)==500)
    independent={};platforms=[('Visium',2),('snRNA-seq',9),('WES',16),('Xenium_5K_Prime',23)]
    for platform,hr in platforms:
        for row in range(hr+1,hr+6):
            hist=s.cell(row,1).value
            for c in range(2,27):
                patient=s.cell(hr,c).value;raw=s.cell(row,c).value
                n=0 if raw is None else 2 if '*' in raw else 1
                key=(platform,patient,hist);independent[key]=n;o=pk[key]
                candidates=[x for x in prior if x['platform']==platform and 'P'+x['patient_id_author']==patient and x['histology_deposited']==hist]
                ck('Participation '+str(key),o['mark_raw']==(raw or '') and int(o['reported_sample_or_block_count'])==n)
                ck('Participation source '+str(key),o['source_locator']==locator(1,'Tab 2',s.cell(row,c).coordinate))
                ck('No block IDs invented '+str(key),o['explicit_block_ids']==o['explicit_section_ids']=='')
                if platform!='Xenium_5K_Prime':
                    ck('GEO group cardinality '+str(key),int(o['GEO_records'])==len(candidates) and set(filter(None,o['GEO_alias_candidates'].split('|')))=={x['library_name_author'] for x in candidates})
                else:ck('No fake Xenium GEO count '+str(key),o['GEO_records']=='')
    totals=rows(run/'participation_totals.csv')
    ck('Twenty histology rows and four totals',len(totals)==24)
    for r in totals:
        derived=sum(n for (p,patient,h),n in independent.items() if p==r['platform'] and (r['histology']=='ALL' or h==r['histology']))
        report=at(r['source_locator'])
        ck('Table arithmetic '+r['platform']+r['histology'],int(r['marks_derived'])==derived and int(r['table_reported'])==report and (r['marks_match_reported']=='True')==(derived==report))
        if r['platform']!='Xenium_5K_Prime':
            n=sum(x['platform']==r['platform'] and (r['histology']=='ALL' or x['histology_deposited']==r['histology']) for x in prior)
            ck('Table versus deposit '+r['platform']+r['histology'],int(r['GEO_records'])==n and int(r['table_minus_GEO'])==report-n)
    xrows=rows(run/'xenium_participation.csv')
    wanted_x={(p,h) for (platform,p,h),n in independent.items() if platform=='Xenium_5K_Prime' and n}
    ck('Xenium participation only',len(xrows)==12 and {(r['patient_id_author'],r['histology_table']) for r in xrows}==wanted_x)
    for r in xrows:
        rr=[x for x in prior if x['platform']=='Visium' and 'P'+x['patient_id_author']==r['patient_id_author'] and x['histology_deposited']==r['histology_table']]
        ck('Xenium unresolved sections '+r['source_locator'],r['Xenium_library_id']==r['Xenium_section_id']=='' and set(r['candidate_GSMs'].split('|'))=={x['GSM'] for x in rr})
        ck('Xenium ambiguity '+r['source_locator'],(r['block_selection']=='ambiguous_multiple_candidates')==(len(rr)>1))

    tma=rows(run/'TMA_groups.csv');s=books[1]['Tab 3']
    ck('TMA group rows retained',len(tma)==22)
    for r in tma:
        for key,p in json.loads(r['source_cells']).items():
            v,a=merged_value(s,p['address'])
            ck('TMA merged-source fidelity '+p['address'],equivalent(r[key],v) and p['source_cell']==a and p['expanded_from_merge']==(a!=p['address']))
        ck('TMA unknown keys remain unknown '+r['source_row'],r['core_ids']==r['lesion_ids_parsed']=='')
        ck('TMA namespace '+r['source_row'],r['patient_id_author'].startswith('TMA P#') and r['cohort_id']=='Peng_TMA_reported_separate_cohort')
        ck('TMA slide leading zero '+r['source_row'],r['slide_id'].startswith('00') and len(r['slide_id'])==7)
    for r in rows(run/'TMA_totals.csv'):
        subset=[x for x in tma if x['TMA_id']==r['TMA_id']];derived=sum(int(x['group_cores']) for x in subset)
        ck('TMA aggregate '+r['TMA_id'],int(r['group_cores_sum'])==derived and int(r['reported_cores'])==at(r['source_locator']) and (r['agrees']=='True')==(derived==int(r['reported_cores'])))
    ck('No blind mutation forward-fill',next(r for r in tma if r['source_row']=='9')['driver_mutations']=='')

    genes=rows(run/'gene_lists.csv');expected_genes=[]
    for first,last,family in [(1,9,'snRNA_panlineage'),(11,19,'snRNA_epithelial'),(21,31,'Visium')]:
        s=books[2]['Sheet1']
        for c in range(first,last+1):
            for row in range(5,55):
                v=s.cell(row,c).value
                if v is not None:expected_genes.append(('S2::'+family+'::'+s.cell(3,c).value,'Homo_sapiens',locator(2,'Sheet1',s.cell(row,c).coordinate),str(v)))
    for c in range(1,6):
        species='Homo_sapiens' if c<=3 else 'Mus_musculus';s=books[3]['Sheet1']
        for row in range(4,203):
            v=s.cell(row,c).value
            if v is not None:expected_genes.append(('S3::'+species+'::'+s.cell(3,c).value,species,locator(3,'Sheet1',s.cell(row,c).coordinate),str(v)))
    for c,name in [(1,'whole_tissue_5K_Prime'),(3,'TMA_lung')]:
        s=books[4]['Tab 1']
        for row in range(4,104):expected_genes.append(('S4::custom_addon::'+name,'Homo_sapiens',locator(4,'Tab 1',s.cell(row,c).coordinate),s.cell(row,c).value))
    ck('Complete namespace/species/raw-gene inventory',Counter(expected_genes)==Counter((r['namespace'],r['species'],r['source_locator'],r['gene_raw']) for r in genes))
    for r in genes:
        ck('Only trim gene whitespace '+r['source_locator'],r['gene_symbol']==r['gene_raw'].strip())
        if r['ensembl_locator']:ck('Paired Ensembl '+r['source_locator'],equivalent(r['ensembl_id'],at(r['ensembl_locator'])))
    for r in rows(run/'gene_list_inventory.csv'):
        gg=[g for g in genes if g['namespace']==r['namespace']]
        ck('Gene list counts '+r['namespace'],int(r['entries'])==len(gg) and int(r['unique_symbols'])==len({g['gene_symbol'] for g in gg}))
    maps=json.loads(FEATURES.read_text())['mapping'];targetset={r['gene'] for r in maps};response=set(json.loads(ENDPOINT.read_text())['response']['genes'])
    target_rows=rows(run/'A12_addon_membership.csv');ck('Two add-ons by ten existing targets',len(target_rows)==20)
    for r in target_rows:
        gg=[g for g in genes if g['namespace']==r['namespace'] and g['gene_symbol']==r['gene']]
        ck('A12 add-on membership '+r['namespace']+r['gene'],(r['membership']=='listed_in_custom_addon')==bool(gg) and r['gene'] in targetset)
        ck('Absence is not unmeasured '+r['namespace']+r['gene'],r['full_assay_coverage']=='unknown_base_panel_and_measured_matrix_not_qualified')
    overlaps=rows(run/'A12_published_list_overlaps.csv')
    ck('No mouse-to-human endpoint substitution',{r['namespace'] for r in overlaps}=={g['namespace'] for g in genes if g['species']=='Homo_sapiens'})
    for r in overlaps:
        syms={g['gene_symbol'] for g in genes if g['namespace']==r['namespace']}
        ck('A12 exact overlap '+r['namespace'],set(filter(None,r['A12_response_genes'].split('|')))==syms&response and int(r['response_overlap_count'])==len(syms&response) and set(filter(None,r['A12_components'].split('|')))==syms&targetset)
    degs=rows(run/'published_DEG_summaries.csv')
    ck('All published DEG rows retained',len(degs)==sum(1 for i,sh in [(4,'Tab 2'),(5,'Sheet1')] for row in books[i][sh].iter_rows(min_row=3) if row[0].value is not None))
    for r in degs:
        sources=json.loads(r['source_cells'])
        for key,outkey in [('gene','gene'),('log2FC','published_average_log2FC'),('adjusted_p','published_adjusted_p'),('label','label')]:ck('DEG raw value '+sources[key],equivalent(r[outkey],at(sources[key])))
    antibodies=rows(run/'seqIF_COMET_metadata.csv');ck('All seq-IF metadata rows retained',len(antibodies)==20)
    for r in antibodies:
        for key,source in json.loads(r['source_cells']).items():ck('SeqIF source value '+source,equivalent(r[key],at(source)))

    summary=json.loads((run/'summary.json').read_text())
    ck('WES aggregate localization',summary['WES_gap_by_histology']=={'Normal':24,'AAH':1,'AIS':0,'MIA':0,'LUAD':0,'ALL':25})
    ck('TMA distinct units',summary['TMA']['distinct_patients']==len({r['patient_id_author'] for r in tma})==19 and summary['TMA']['sum_group_cores']==sum(int(r['group_cores']) for r in tma)==188 and summary['TMA']['TMAs']==8 and summary['TMA']['slides']==4)
    ck('TMA lesions only reported',summary['TMA']['reported_totals']['G27']==books[1]['Tab 3']['G27'].value)
    issues=rows(run/'qualification_issues.csv')
    ck('P6/P7 unresolved holds retained',{'file_identity_hold_remains','historical_review_hold_remains'}.issubset({r['status'] for r in issues}))
    ck('No claim of raw spatial inputs','No expression refit' in summary['interpretation'])
    result=dict(status='passed' if not failures else 'failed',checks=checks,failures=failures,
        method='Independent openpyxl cell/merge reads versus OOXML extraction; independent participation, join, gene-membership and aggregate arithmetic',
        openpyxl_version=openpyxl.__version__,limit='Same-source numerical verification, not independent biological replication or scientific acceptance')
    with (run/'verification.json').open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    for w in list(books.values())+list(cached.values()):w.close()
    print(json.dumps(result))
    if failures:raise ValueError('Independent source verification failed')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);verify(p.parse_args().run)
