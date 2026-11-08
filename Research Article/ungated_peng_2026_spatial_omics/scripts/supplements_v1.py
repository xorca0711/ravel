"""Read-only Pg1 source qualification: OOXML cells, source-defined lists and joins."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from posixpath import normpath

ROOT = Path(__file__).resolve().parents[3]
RAW = 'raw_data/peng_supplements_20261108'
PREVIOUS = 'analysis/research/runs/Pg1_metadata_v3_20261108'
FEATURES = 'docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A12_FEATURE_MAP_V1.json'
ENDPOINT = 'docs/roadmap_runs/2026-09-27-followthrough/A12_pilot_specification.json'
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
INPUTS = [f'{RAW}/NIHMS2118436-supplement-{i}.xlsx' for i in range(2, 8)] + [
    f'{RAW}/intake_v1.json', f'{PREVIOUS}/samples.csv', f'{PREVIOUS}/summary.json',
    f'{PREVIOUS}/receipt.json', FEATURES, ENDPOINT]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_json(out, name, obj):
    with (out/name).open('x', encoding='utf8', newline='\n') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')


def write_csv(out, name, rows, fields=None):
    with (out/name).open('x', encoding='utf8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def csv_read(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def col(n):
    result = ''
    while n:
        n, r = divmod(n-1, 26)
        result = chr(65+r)+result
    return result


def rc(a):
    m = re.fullmatch(r'([A-Z]+)(\d+)', a)
    if not m:
        raise ValueError('Unexpected cell address: '+a)
    c = 0
    for char in m[1]:
        c = c*26+ord(char)-64
    return int(m[2]), c


def merged_anchors(ranges):
    result = {}
    for region in ranges:
        first, last = region.split(':') if ':' in region else (region, region)
        r1,c1 = rc(first); r2,c2 = rc(last)
        for r in range(r1,r2+1):
            for c in range(c1,c2+1):
                address = col(c)+str(r)
                if address in result:
                    raise ValueError('Overlapping merged ranges')
                result[address] = first
    return result


def read_xlsx(path, table):
    """Decode saved cells/formula caches; do not execute workbook formulas."""
    sheets = {}
    with zipfile.ZipFile(path) as z:
        shared = []
        if 'xl/sharedStrings.xml' in z.namelist():
            for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS):
                shared.append(''.join(t.text or '' for t in si.findall('.//s:t', NS)))
        links = {e.attrib['Id']: e.attrib['Target'] for e in
                 ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        for node in wb.findall('s:sheets/s:sheet', NS):
            target = links[node.attrib['{'+REL+'}id']]
            member = target.lstrip('/') if target.startswith('/') else normpath('xl/'+target)
            x = ET.fromstring(z.read(member)); cells = {}
            for c in x.findall('s:sheetData/s:row/s:c', NS):
                kind = c.get('t', 'n'); v = c.find('s:v', NS); f = c.find('s:f', NS)
                raw = v.text if v is not None and v.text is not None else ''
                text = shared[int(raw)] if kind == 's' else (
                    ''.join(t.text or '' for t in c.findall('s:is//s:t', NS)) if kind == 'inlineStr' else raw)
                formula = '='+f.text if f is not None and f.text else ''
                if text == '' and not formula and not (kind == 's' and raw != ''):
                    continue
                cells[c.attrib['r']] = dict(value=text, kind=kind, formula=formula, style=c.get('s',''))
            ranges = [m.attrib['ref'] for m in x.findall('s:mergeCells/s:mergeCell', NS)]
            sheets[node.attrib['name']] = dict(cells=cells, merged=ranges, anchors=merged_anchors(ranges),
                dimension=x.find('s:dimension',NS).get('ref'), table=table, file=path.name)
    return sheets


def cell(sheet, address, expand=False):
    origin = sheet['anchors'].get(address, address) if expand else address
    return sheet['cells'].get(origin, {}).get('value', ''), origin


def val(sheet, address, expand=False):
    return cell(sheet, address, expand)[0]


def loc(sheet, address):
    return f"{sheet['file']}#{sheet['name']}!{address}"


def marks(text):
    normalized = text.replace(' ', '')
    if normalized not in ('', '✓', '✓*'):
        raise ValueError('Unsupported participation mark: '+repr(text))
    return {'':0, '✓':1, '✓*':2}[normalized]


def main(out):
    books = {}; ledger = []; manifests = []
    intake = json.loads((ROOT/RAW/'intake_v1.json').read_text())
    for i in range(2,8):
        file = f'NIHMS2118436-supplement-{i}.xlsx'; p=ROOT/RAW/file
        record = next(r for r in intake if r['file']==file)
        if sha(p)!=record['sha256']:
            raise ValueError('Source intake checksum differs')
        books[i-1] = read_xlsx(p, f'S{i-1}')
        for name, sheet in books[i-1].items():
            sheet['name'] = name
            manifests.append(dict(table=sheet['table'], file=file, sha256=sha(p), sheet=name,
                dimension=sheet['dimension'], merged_ranges=json.dumps(sheet['merged']),
                nonempty_cells=len(sheet['cells']), formula_count=sum(bool(c['formula']) for c in sheet['cells'].values())))
            for a,c in sorted(sheet['cells'].items(),key=lambda x:rc(x[0])):
                ledger.append(dict(table=sheet['table'], file=file, sheet=name, cell=a,
                    stored_type=c['kind'], value_text=c['value'], formula=c['formula'], style_id=c['style'],
                    source_locator=loc(sheet,a)))
    write_csv(out,'source_cells.csv',ledger)
    write_csv(out,'sheet_manifest.csv',manifests)
    write_json(out,'source_manifest.json', dict(source_kind='user_supplied_local_supplementary_workbooks',
        files=[{k:r[k] for k in ['table','file','sha256','bytes','source_kind','source_url','received_date','copied_utc']} for r in intake],
        input_hashes=[dict(path=p,sha256=sha(ROOT/p)) for p in INPUTS],
        access_limit='Supplied file hashes verified; download provenance before local supply is user-provided; prior failed public routes remain historical',
        read_semantics='Read OOXML saved cells and formula caches without executing formulas; originals and local copies unchanged'))
    prior=csv_read(ROOT/PREVIOUS/'samples.csv')
    prior_keys=defaultdict(list)
    for r in prior:
        prior_keys[(r['platform'],'P'+r['patient_id_author'],r['histology_deposited'])].append(r)

    s=books[1]['Tab 1']; clinical=[]; clinical_checks=[]
    clinical_fields=['patient_id_author','institute','ethnicity','sex','age','tumor_greatest_diameter_mm','T','N','M','stage','smoking','driver_mutations']
    for r in range(4,29):
        d={k:val(s,col(c)+str(r)) for c,k in enumerate(clinical_fields,1)}
        d.update(cohort_id='Peng_discovery',source_cells=json.dumps({k:loc(s,col(c)+str(r)) for c,k in enumerate(clinical_fields,1)}))
        clinical.append(d)
        pp=[x for x in prior if 'P'+x['patient_id_author']==d['patient_id_author']]
        for old in pp:
            for key in ['age','sex','ethnicity','smoking']:
                raw=d[key]; compare=raw.strip().lower()
                if key=='sex': compare={'f':'female','m':'male'}.get(compare,compare)
                if key=='smoking': compare={'smoker':'yes','never smoker':'no'}.get(compare,compare)
                clinical_checks.append(dict(patient=d['patient_id_author'],GSM=old['GSM'],field=key,
                    table_value=raw,GEO_value=old[key],comparison='agrees' if compare==old[key].strip().lower() else 'disagrees_or_unknown',
                    source_locator=json.loads(d['source_cells'])[key],prior_locator=f'{PREVIOUS}/samples.csv#{old["GSM"]}'))
    write_csv(out,'discovery_clinical.csv',clinical)
    write_csv(out,'clinical_GEO_comparison.csv',clinical_checks)

    s=books[1]['Tab 2']; participation=[]; totals=[]; xenium=[]
    for header,platform in [(2,'Visium'),(9,'snRNA-seq'),(16,'WES'),(23,'Xenium_5K_Prime')]:
        platform_rows=[]
        for r in range(header+1,header+6):
            hist=val(s,'A'+str(r)); this=[]
            for c in range(2,27):
                patient=val(s,col(c)+str(header)); address=col(c)+str(r); raw=val(s,address); n=marks(raw)
                rr=prior_keys[(platform,patient,hist)]
                d=dict(platform=platform,patient_id_author=patient,histology_table=hist,mark_raw=raw,
                    reported_sample_or_block_count=n,mark_status='marked' if n else 'not_marked',
                    explicit_block_ids='',explicit_section_ids='',GEO_records=len(rr) if platform!='Xenium_5K_Prime' else '',
                    GEO_alias_candidates='|'.join(x['library_name_author'] for x in rr),
                    source_locator=loc(s,address),patient_source=loc(s,col(c)+str(header)),histology_source=loc(s,'A'+str(r)),
                    multiplicity_source=loc(s,'A31'),join_level='patient_histology_participation_not_library_identity')
                participation.append(d);this.append(d);platform_rows.append(d)
                if platform=='Xenium_5K_Prime' and n:
                    candidates=prior_keys[('Visium',patient,hist)]
                    xenium.append(dict(patient_id_author=patient,histology_table=hist,reported_samples=n,
                        Visium_alias_candidates='|'.join(x['library_name_author'] for x in candidates),
                        candidate_GSMs='|'.join(x['GSM'] for x in candidates),
                        block_selection='ambiguous_multiple_candidates' if len(candidates)>1 else 'single_candidate_not_section_proof',
                        Xenium_library_id='',Xenium_section_id='',source_locator=loc(s,address)))
            derived=sum(d['reported_sample_or_block_count'] for d in this);reported=int(float(val(s,'AA'+str(r))))
            geo=sum(len(prior_keys[(platform,d['patient_id_author'],hist)]) for d in this) if platform!='Xenium_5K_Prime' else None
            totals.append(dict(platform=platform,histology=hist,marks_derived=derived,table_reported=reported,
                GEO_records='' if geo is None else geo,table_minus_GEO='' if geo is None else reported-geo,
                marks_match_reported=derived==reported,source_locator=loc(s,'AA'+str(r)),
                marks_range=loc(s,f'B{r}:Z{r}'),formula='',comparison_level='aggregate_participation'))
        a='AA'+str(header+6);total=int(float(val(s,a)));derived=sum(d['reported_sample_or_block_count'] for d in platform_rows)
        geo=sum(x['platform']==platform for x in prior) if platform!='Xenium_5K_Prime' else None
        totals.append(dict(platform=platform,histology='ALL',marks_derived=derived,table_reported=total,
            GEO_records='' if geo is None else geo,table_minus_GEO='' if geo is None else total-geo,
            marks_match_reported=derived==total,source_locator=loc(s,a),marks_range=loc(s,f'B{header+1}:Z{header+5}'),
            formula=s['cells'][a]['formula'],comparison_level='aggregate_participation'))
    write_csv(out,'platform_participation.csv',participation)
    write_csv(out,'participation_totals.csv',totals)
    write_csv(out,'xenium_participation.csv',xenium)

    s=books[1]['Tab 3']; tma=[]
    fields=['slide_number','slide_id','position','TMA_id','TMA_total_cores','patient_id_author','lesion_text_raw','group_cores',
            'institute','ethnicity','sex','age','tumor_greatest_diameter_mm','T','N','M','stage','smoking','driver_mutations']
    for r in range(5,27):
        d=dict(cohort_id='Peng_TMA_reported_separate_cohort',source_row=r);provenance={}
        for c,key in enumerate(fields,1):
            address=col(c)+str(r);value,origin=cell(s,address,True);d[key]=value
            provenance[key]=dict(address=address,source_cell=origin,expanded_from_merge=origin!=address,source_locator=loc(s,origin))
        d.update(source_cells=json.dumps(provenance,ensure_ascii=False),core_ids='',lesion_ids_parsed='',
                 interpretation='Aggregated group only; parentheses retained uninterpreted; no individual core/barcode map')
        tma.append(d)
    write_csv(out,'TMA_groups.csv',tma)
    tma_totals=[]
    for tid in sorted({r['TMA_id'] for r in tma}):
        rows=[r for r in tma if r['TMA_id']==tid];reported={r['TMA_total_cores'] for r in rows}
        if len(reported)!=1:raise ValueError('TMA total ambiguity')
        count=int(float(next(iter(reported))));derived=sum(int(float(r['group_cores'])) for r in rows)
        tma_totals.append(dict(TMA_id=tid,reported_cores=count,group_cores_sum=derived,agrees=count==derived,
            patients='|'.join(sorted({r['patient_id_author'] for r in rows})),
            source_locator=json.loads(rows[0]['source_cells'])['TMA_total_cores']['source_locator']))
    write_csv(out,'TMA_totals.csv',tma_totals)

    genes=[]
    def gene(sheet,address,namespace,species,kind,label,header,ensembl_cell=''):
        raw=val(sheet,address)
        if raw=='':return
        genes.append(dict(namespace=namespace,species=species,list_kind=kind,label_raw=label,gene_raw=raw,
            gene_symbol=raw.strip(),source_locator=loc(sheet,address),header_locator=loc(sheet,header),
            ensembl_id=val(sheet,ensembl_cell) if ensembl_cell else '',ensembl_locator=loc(sheet,ensembl_cell) if ensembl_cell else ''))
    s=books[2]['Sheet1']
    for start,end,family in [(1,9,'snRNA_panlineage'),(11,19,'snRNA_epithelial'),(21,31,'Visium')]:
        for c in range(start,end+1):
            a=col(c);mp=val(s,a+'3');label=val(s,a+'4')
            for r in range(5,55):gene(s,a+str(r),'S2::'+family+'::'+mp,'Homo_sapiens','meta_program',label,a+'3')
    s=books[3]['Sheet1']
    for c in range(1,6):
        a=col(c);species='Homo_sapiens' if c<4 else 'Mus_musculus';label=val(s,a+'3')
        for r in range(4,203):gene(s,a+str(r),'S3::'+species+'::'+label,species,'published_signature',label,a+'3')
    s=books[4]['Tab 1']
    for a,b,ns in [('A','B','whole_tissue_5K_Prime'),('C','D','TMA_lung')]:
        for r in range(4,104):gene(s,a+str(r),'S4::custom_addon::'+ns,'Homo_sapiens','custom_addon_only',val(s,a+'2'),a+'2',b+str(r))
    write_csv(out,'gene_lists.csv',genes)
    list_summary=[]
    for ns in sorted({g['namespace'] for g in genes}):
        gg=[g for g in genes if g['namespace']==ns]
        list_summary.append(dict(namespace=ns,species=gg[0]['species'],list_kind=gg[0]['list_kind'],
            label_raw=gg[0]['label_raw'],entries=len(gg),unique_symbols=len({g['gene_symbol'] for g in gg}),
            duplicate_entries=len(gg)-len({g['gene_symbol'] for g in gg}),header_locator=gg[0]['header_locator']))
    write_csv(out,'gene_list_inventory.csv',list_summary)

    degs=[]
    for table,sh,species in [(4,'Tab 2','Homo_sapiens'),(5,'Sheet1','Mus_musculus')]:
        s=books[table][sh];last=rc(s['dimension'].split(':')[-1])[0]
        for r in range(3,last+1):
            if not val(s,'A'+str(r)):continue
            degs.append(dict(table=f'S{table}',species=species,source_row=r,gene=val(s,'A'+str(r)),
                published_average_log2FC=val(s,'B'+str(r)),published_adjusted_p=val(s,'C'+str(r)),label=val(s,'D'+str(r)),
                source_cells=json.dumps({k:loc(s,c+str(r)) for k,c in [('gene','A'),('log2FC','B'),('adjusted_p','C'),('label','D')]}),
                interpretation='Published DEG summary, not raw cell/animal outcomes or a new differential test'))
    write_csv(out,'published_DEG_summaries.csv',degs)
    s=books[6]['Sheet1'];antibodies=[]
    for r in range(3,23):
        values={};origins={}
        for c,key in enumerate(['cycle','target','catalog','vendor','host_species','clone','channel','dilution_factor','incubation_min'],1):
            value,origin=cell(s,col(c)+str(r),True);values[key]=value;origins[key]=loc(s,origin)
        values.update(source_row=r,source_cells=json.dumps(origins),interpretation='Assay/run metadata; no measured treatment outcome')
        antibodies.append(values)
    write_csv(out,'seqIF_COMET_metadata.csv',antibodies)

    feature_map=json.loads((ROOT/FEATURES).read_text())['mapping'];targets=[x['gene'] for x in feature_map]
    response=set(json.loads((ROOT/ENDPOINT).read_text())['response']['genes'])
    target_rows=[];overlaps=[]
    for ns in sorted({g['namespace'] for g in genes}):
        gg=[g for g in genes if g['namespace']==ns];syms={g['gene_symbol'] for g in gg}
        if gg[0]['species']!='Homo_sapiens':continue
        shared=syms & response
        overlaps.append(dict(namespace=ns,list_kind=gg[0]['list_kind'],A12_components='|'.join(sorted(syms&set(targets))),
            A12_response_genes='|'.join(sorted(shared)),response_overlap_count=len(shared),
            source_cells='|'.join(g['source_locator'] for g in gg if g['gene_symbol'] in shared),
            endpoint_source=ENDPOINT+'#response.genes',
            interpretation='Exact human-symbol overlap only; potential feature sharing, not proof of label circularity or measured assay coverage'))
        if gg[0]['list_kind']=='custom_addon_only':
            for target in feature_map:
                matching=[g for g in gg if g['gene_symbol']==target['gene']]
                target_rows.append(dict(namespace=ns,gene=target['gene'],index_weight=target['index_weight'],
                    in_old_response=target['in_original_response'],membership='listed_in_custom_addon' if matching else 'not_listed_in_custom_addon',
                    source_locator='|'.join(g['source_locator'] for g in matching),panel_header=gg[0]['header_locator'],
                    full_assay_coverage='unknown_base_panel_and_measured_matrix_not_qualified',target_source=FEATURES+'#'+target['gene']))
    write_csv(out,'A12_addon_membership.csv',target_rows)
    write_csv(out,'A12_published_list_overlaps.csv',overlaps)

    wes=[r for r in participation if r['platform']=='WES' and r['reported_sample_or_block_count']!=r['GEO_records']]
    issues=[dict(issue='WES_table_deposit_difference',source_locator=r['source_locator'],detail=f"{r['patient_id_author']} {r['histology_table']}: table={r['reported_sample_or_block_count']}; GEO={r['GEO_records']}",status='aggregate_gap_localized_not_missing_file_identity') for r in wes]
    issues += [dict(issue='P6_WES_file_histology',source_locator=loc(books[1]['Tab 2'],'G18'),detail='Table marks P6 AAH; current GEO title/alias agree, linked VCF filename says AIS. Table does not identify the VCF.',status='file_identity_hold_remains'),
               dict(issue='P7_original_review',source_locator=loc(books[1]['Tab 2'],'H21'),detail='Table marks two LUAD blocks; no original category or revised-alias mapping.',status='historical_review_hold_remains'),
               dict(issue='TMA_lesion_parentheses',source_locator=loc(books[1]['Tab 3'],'G5:G26'),detail='Raw lesion text preserved; parenthetical numerals not interpreted as sizes/counts or resolved lesion IDs.',status='individual_core_lesion_barcode_map_missing'),
               dict(issue='custom_addon_only',source_locator=loc(books[4]['Tab 1'],'A2:D103'),detail='Listed add-on genes are not the complete base-plus-addon panel or evidence of measured gene availability.',status='full_assay_coverage_hold_remains')]
    write_csv(out,'qualification_issues.csv',issues)
    summary=dict(analysis_id='Pg1-P01.supplements_v1',outcome_exposure='exposed',source_workbooks=6,
        clinical_patients=len(clinical),clinical_GEO_comparisons=len(clinical_checks),
        clinical_GEO_disagreements=[r for r in clinical_checks if r['comparison']!='agrees'],
        platform_totals=[r for r in totals if r['histology']=='ALL'],
        WES_gap_by_histology={r['histology']:r['table_minus_GEO'] for r in totals if r['platform']=='WES'},
        WES_patient_histology_gap_rows=wes,xenium_participation=xenium,
        TMA=dict(group_rows=len(tma),distinct_patients=len({r['patient_id_author'] for r in tma}),TMAs=len(tma_totals),
            slides=len({r['slide_id'] for r in tma}),sum_group_cores=sum(int(r['group_cores']) for r in tma),
            sum_unique_TMA_core_totals=sum(r['reported_cores'] for r in tma_totals),
            reported_totals={a:val(books[1]['Tab 3'],a) for a in ['E27','F27','G27']},
            lesion_total_verification='Reported 36 only; not reconstructed by interpreting parenthetical numbers',core_ID_mapping='not_supplied'),
        gene_lists=list_summary,DEG_rows=dict(Counter(r['table'] for r in degs)),seqIF_rows=len(antibodies),
        A12_addon_membership=target_rows,
        interpretation='Metadata/source qualification only. No expression refit, population estimate, independent validation, new RQ or scientific acceptance. Prior v3 and unfavorable A11/A12/A13 outcomes remain unchanged.')
    write_json(out,'summary.json',summary)
    subprocess.run([sys.executable,str(Path(__file__).with_name('verify_supplements_v1.py')),'--run',str(out)],check=True)
    print(json.dumps({'status':'supplementary_sources_qualified','interpretation':'metadata_only'}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    main(p.parse_args().output)
