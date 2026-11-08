"""Pg1-P01 metadata v2: explicit filename discrepancies and preserved failed v1. Outputs are exclusive-create; no expression is read."""
import argparse
import csv
import gzip
import hashlib
import itertools
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = 'raw_data/peng_spatial_20261108'
C3 = 'Research Article/gate2_C3_yu_lee_choi_min_2026/trials'
SERIES = {'GSE307534': 'Visium', 'GSE308103': 'snRNA-seq', 'GSE307529': 'WES'}
PRIOR = [
    'u0_geo_design_audit/sample_inventory.csv',
    'u0_geo_design_audit/human_sample_links.csv',
    'u5_human_pilot/all_series_patient_histology_crosswalk.csv',
    'u5_human_full/library_qc_and_annotation.csv',
    'u5_spatial_context/RNA_spatial_demographic_crosswalk.csv',
    'u5_spatial_context/RNA_spatial_crosswalk_validation.json',
    'u5_spatial_context/deposited_member_inventory.csv',
    'u5_spatial_context/possible_pathology_annotation_members.csv',
]
INPUT_PATHS = ([f'{RAW}/{g}_family.soft.gz' for g in SERIES]
    + [f'{RAW}/acquisition_v{i}.json' for i in range(1, 7)]
    + [f'{RAW}/{n}' for n in ['pmc_article.html', 'zenodo_15670280.json',
       'zenodo_17172149.json', 'author_repository_tree.json', 'author_Figure_1.R',
       'author_Figure_5.R', 'geo_spatial_directory.html']]
    + [f'{C3}/{p}' for p in PRIOR])


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def csv_out(out, name, rows, fields=None):
    fields = fields or list(rows[0])
    with (out / name).open('x', encoding='utf8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def json_out(out, name, data):
    with (out / name).open('x', encoding='utf8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def soft_records(text):
    records, fields, gsm = [], defaultdict(list), None
    for line in text.splitlines():
        if line.startswith('^'):
            if gsm is not None:
                records.append((gsm, dict(fields)))
            gsm = line.split(' = ', 1)[1] if line.startswith('^SAMPLE = ') else None
            fields = defaultdict(list)
        elif gsm is not None and line.startswith('!Sample_'):
            key, value = line.split(' = ', 1)
            fields[key.removeprefix('!Sample_')].append(value)
    if gsm is not None:
        records.append((gsm, dict(fields)))
    if len({g for g, _ in records}) != len(records):
        raise ValueError('Duplicate GSM in SOFT')
    return records


def one(values, field):
    if len(values) != 1:
        raise ValueError(f'Expected exactly one {field}: {values}')
    return values[0]


def parse_sample(gse, gsm, f):
    title = one(f.get('title', []), 'title')
    aliases = [s.removeprefix('Library name: ') for s in f.get('description', [])
               if s.startswith('Library name: ')]
    alias = one(aliases, 'explicit library alias')
    m = re.fullmatch(r'P(\d+)_(Normal|AAH|AIS|MIA|LUAD)(-\d+)?', alias)
    pt = re.search(r'\bpatient (\d+)\b', title)
    ht = re.search(r'\b(AAH|AIS|MIA|LUAD)\b', title)
    hist = ht[1] if ht else ('Normal' if 'normal lung tissue' in title.lower() else '')
    if not m or not pt or not hist:
        raise ValueError(f'Unrecognized identifiers: {gsm} {title} {alias}')
    if pt[1] != m[1] or hist != m[2]:
        raise ValueError(f'Title/alias disagreement: {gsm}')
    characteristics = defaultdict(list)
    for s in f.get('characteristics_ch1', []):
        key, value = s.split(': ', 1)
        characteristics[key.lower()].append(value)
    row = dict(cohort_id='Peng_discovery_GEO', record_id=f'{gse}:{gsm}',
        patient_id_author=pt[1], patient_id_parsed_alias=m[1], lesion_id_author='',
        block_id='', section_id='', platform=SERIES[gse], GSE=gse, GSM=gsm,
        library_name_author=alias, library_alias_suffix=m[3] or '',
        title_author=title, histology_original='', histology_deposited=hist,
        histology_alias_parsed=m[2], histology_reviewed='',
        histology_review_note=('Paper reports P7 precursor-to-LUAD revision; both deposited lesion aliases are LUAD; original diagnosis and revised-library mapping unavailable'
                               if pt[1] == '7' and hist != 'Normal' else ''),
        normal_context=('Not specified per library; normal versus adjacent-normal substitution needs manifest'
                        if hist == 'Normal' else 'Lesion-bearing tissue; not a spot-level pathology assignment'),
        ROI_id='', core_id='', cell_or_spot_id='', coordinate_frame='',
        annotation_source='GEO title, explicit Library name description and characteristics',
        source_locator=f'{RAW}/{gse}_family.soft.gz#SAMPLE={gsm}',
        join_level='deposited_library', join_status='unique_GSM; specimen_and_section_relationships_unverified',
        unknown_reason='No author block/lesion/section IDs, historical diagnosis mapping, ROI or barcode export recovered',
        parsing_rule='Patient from title patient N checked against exact P<N>_<histology><suffix> alias; suffix retained',
        supplementary_files='|'.join(v for k, vv in f.items() if k.startswith('supplementary_file') for v in vv))
    for key in ['age', 'sex', 'smoking', 'ethnicity']:
        row[key] = one(characteristics.get(key, []), key)
    return row


def execute(out):
    failed = ROOT / 'analysis/research/runs/Pg1_metadata_v1_20261108'
    names = ['annotation_availability.csv', 'author_required_objects.csv', 'crosswalk.csv',
             'join_issues.csv', 'patients.csv', 'prior_inventory_comparison.csv', 'receipt.json',
             'samples.csv', 'source_manifest.json', 'stderr.log', 'stdout.log', 'summary.json']
    if json.loads((failed/'receipt.json').read_text())['status'] != 'execution_failed':
        raise ValueError('Expected retained failed v1 receipt')
    (out/'failed_v1').mkdir()
    preserved = []
    for name in names:
        data = (failed/name).read_bytes()
        dest = out/'failed_v1'/name
        with dest.open('xb') as f:
            f.write(data)
        if sha(dest) != sha(failed/name):
            raise ValueError('Failure archive byte mismatch')
        preserved.append(dict(source=(failed/name).relative_to(ROOT).as_posix(),
                              archive='failed_v1/'+name, sha256=sha(dest)))
    json_out(out, 'failure_preservation.json', dict(original_status='execution_failed',
        scope='Byte-identical archive only; v1 remains failed and its partial results are not qualified', files=preserved))
    samples, issues = [], []
    def issue(kind, locator, detail, affected):
        issues.append(dict(issue=kind, source_locator=locator, detail=detail, held_scope=affected))

    for gse in SERIES:
        with gzip.open(ROOT / RAW / f'{gse}_family.soft.gz', 'rt', encoding='utf8') as f:
            text = f.read()
        if f'^SERIES = {gse}' not in text:
            raise ValueError(f'Series identity mismatch: {gse}')
        rows = [parse_sample(gse, gsm, f) for gsm, f in soft_records(text)]
        if len({r['library_name_author'] for r in rows}) != len(rows):
            raise ValueError(f'Duplicate alias within {gse}; do not collapse')
        samples.extend(rows)
    for row in samples:
        gsm = row['GSM']
        names = []
        for url in row['supplementary_files'].split('|'):
            m = re.match(re.escape(gsm)+r'_(.*?)(?:\.raw_counts|\.WES|\.tar\.gz)', url.rsplit('/',1)[-1])
            if not m:
                raise ValueError(f'Unrecognized supplementary filename: {url}')
            names.append(m[1])
        if len(set(names)) != 1:
            raise ValueError(f'Ambiguous supplementary filename aliases: {gsm}')
        row['filename_library_alias'] = names[0]
        row['filename_alias_status'] = ('exact_author_alias' if names[0] == row['library_name_author']
                                        else 'different_verbatim_string_no_normalization')
        row['filename_mapping_basis'] = 'Supplementary URL explicitly attached to this GSM; not alias equivalence'
        if row['filename_alias_status'] != 'exact_author_alias':
            issue('filename_author_alias_difference', row['source_locator'],
                  f"author={row['library_name_author']};filename={names[0]}; GSM links this file; preserve both strings",
                  'filename-only joins; explicit author-alias joins retained at alias level')
    csv_out(out, 'samples.csv', samples)

    patient_rows = []
    for patient in sorted({r['patient_id_author'] for r in samples}, key=int):
        rr = [r for r in samples if r['patient_id_author'] == patient]
        consistent = all(len({r[k].lower() for r in rr}) == 1 for k in ['age', 'sex', 'smoking', 'ethnicity'])
        if not consistent:
            issue('demographic_conflict', f'patient={patient}', 'Disagreement across metadata records; no inferred identity', 'patient linkage')
        patient_rows.append(dict(cohort_id='Peng_discovery_GEO', patient_id_author=patient,
            **{g: '|'.join(r['GSM'] for r in rr if r['GSE'] == g) for g in SERIES},
            demographic_consistency=str(consistent).lower(), join_level='patient_metadata_label',
            join_status='consistent_metadata_not_genotype_verified' if consistent else 'conflict',
            lesion_or_section_match='unverified'))
    csv_out(out, 'patients.csv', patient_rows)

    crosswalk, pair_counts = [], {}
    for a, b in itertools.combinations(SERIES, 2):
        aa = {r['library_name_author']: r for r in samples if r['GSE'] == a}
        bb = {r['library_name_author']: r for r in samples if r['GSE'] == b}
        shared = aa.keys() & bb.keys()
        for alias in sorted(aa.keys() | bb.keys()):
            ar, br = aa.get(alias), bb.get(alias)
            status = 'exact_author_alias_only' if ar and br else 'no_counterpart_in_deposit'
            crosswalk.append(dict(cohort_id='Peng_discovery_GEO', source_GSE=a, target_GSE=b,
                library_name_author=alias, source_GSM=ar['GSM'] if ar else '', target_GSM=br['GSM'] if br else '',
                patient_id_author=(ar or br)['patient_id_author'], join_level='author_library_alias',
                join_status=status, lesion_relationship='unverified', block_relationship='unverified',
                serial_section_relationship='unverified', same_section_or_cell_match='not_established'))
        pair_counts[f'{a}__{b}'] = dict(shared_exact_aliases=len(shared),
            source_only=len(aa.keys()-bb.keys()), target_only=len(bb.keys()-aa.keys()),
            overlapping_patient_labels=len({r['patient_id_author'] for r in aa.values()} & {r['patient_id_author'] for r in bb.values()}))
    csv_out(out, 'crosswalk.csv', crosswalk)

    comparisons = []
    by_gsm = {r['GSM']: r for r in samples}
    for suffix in PRIOR:
        if suffix.endswith('.json') or 'member' in suffix:
            continue
        for old in read_csv(ROOT / C3 / suffix):
            gsm = old.get('gsm', '')
            if gsm not in by_gsm:
                continue
            new = by_gsm[gsm]
            mismatches = []
            for k, nk in [('series', 'GSE'), ('patient_label', 'patient_id_author'), ('patient', 'patient_id_author'),
                          ('title', 'title_author'), ('age', 'age'), ('sex', 'sex'), ('smoking', 'smoking'),
                          ('ethnicity', 'ethnicity'), ('histology', 'histology_deposited'), ('histology_from_title', 'histology_deposited')]:
                if old.get(k) and old[k].lower() != new[nk].lower():
                    mismatches.append(f'{k}:prior={old[k]};current={new[nk]}')
            comparisons.append(dict(source=f'{C3}/{suffix}', GSM=gsm,
                status='disagreement' if mismatches else 'agrees_on_compared_fields', detail='|'.join(mismatches)))
            if mismatches:
                issue('prior_inventory_disagreement', f'{C3}/{suffix}#{gsm}', '|'.join(mismatches), 'affected prior-field correspondence')
    csv_out(out, 'prior_inventory_comparison.csv', comparisons)

    # Validate acquisition receipts against saved public snapshots; failures remain records.
    manifest = []
    for i in range(1, 7):
        for r in json.loads((ROOT / RAW / f'acquisition_v{i}.json').read_text()):
            p = ROOT / RAW / r['file']
            if 'sha256' in r and (not p.is_file() or sha(p) != r['sha256']):
                raise ValueError(f'Acquisition receipt/hash mismatch: {r["file"]}')
            manifest.append(dict(receipt=f'{RAW}/acquisition_v{i}.json', **r))
    json_out(out, 'source_manifest.json', dict(access_attempts=manifest,
        inputs=[dict(path=p, bytes=(ROOT/p).stat().st_size, sha256=sha(ROOT/p)) for p in INPUT_PATHS],
        format_checks='SOFT gzip decompressed and series/GSM/library schema parsed; JSON decoded; CSV headers read; supplied HTML is source text, not spreadsheets',
        scope='Inspected sources only; inaccessible files are not proven absent'))

    members = read_csv(ROOT / C3 / 'u5_spatial_context/deposited_member_inventory.csv')
    spatial_gsms = {r['GSM'] for r in samples if r['platform'] == 'Visium'}
    spatial_members = [r for r in members if r['gsm'] in spatial_gsms]
    candidates = read_csv(ROOT / C3 / 'u5_spatial_context/possible_pathology_annotation_members.csv')
    candidate_spatial = [r for r in candidates if r['gsm'] in spatial_gsms]
    if candidate_spatial:
        raise ValueError('New annotation candidates require a new qualification contract')
    inventory = []
    products = [
        ('Visium coordinate file references', 'present_in_prior_inventory', 'tissue_positions', 'Prior C3 coordinate/barcode QC reused; no new coordinates loaded'),
        ('Visium image references', 'present_in_prior_inventory', '.png', 'Raster is not a pathology or ROI export'),
        ('Visium author spot pathology and exclusion flags', 'not_recovered', None, 'Stage 3 spot-category/geometry QC held'),
        ('Visium author molecular state and clone labels', 'not_recovered', None, 'Must remain separate from morphology'),
        ('Whole-slide 11 mm ROI squares and block/section manifest', 'not_recovered', None, 'Stage 3 alignment held'),
        ('Xenium cell labels, counts, centroids, polygons and transforms', 'not_recovered', None, 'Stages 3-5 held; no invented Xenium GEO rows'),
        ('TMA core-lesion-patient manifest and measured panel', 'not_recovered', None, 'Stage 6 transport eligibility held'),
        ('Tables S1-S4', 'linked_not_recovered', None, 'S1 joins; S2-S3 signatures; S4 add-on panel contents unavailable'),
        ('Human Zenodo 18851077 and code 17172149', 'restricted', None, 'Empty public file list is an access limit'),
    ]
    for product, status, token, limit in products:
        matched = [r for r in spatial_members if token and token in r['name']]
        inventory.append(dict(product=product, availability=status,
            inspected_member_count=len(matched) if token else '',
            represented_GSMs=len({r['gsm'] for r in matched}) if token else '',
            annotation_QC='not_performed_missing_exports' if not token else 'prior_inventory_reference_only',
            evidence=f'{C3}/u5_spatial_context/deposited_member_inventory.csv' if token else 'SOURCE_RECOVERY.md; source_manifest.json',
            consequence=limit))
    csv_out(out, 'annotation_availability.csv', inventory)
    required_objects = []
    for name in ['author_Figure_1.R', 'author_Figure_5.R']:
        for line_no, line in enumerate((ROOT / RAW / name).read_text(encoding='utf8').splitlines(), 1):
            for path in re.findall(r'[\"\']((?:\./)?Data/[^\"\']+)[\"\']', line):
                required_objects.append(dict(author_source=name, line=line_no, object_path=path,
                    availability='referenced_not_recovered', purpose='Plot input dependency; author script not executed'))
    csv_out(out, 'author_required_objects.csv', required_objects)
    issue('missing_specimen_relationships', 'Tables S1; author manifest', 'Exact aliases and consistent demographics do not prove lesion, block, serial-section or same-cell correspondence', 'specimen-level integration')
    issue('P7_original_review_mapping', 'PMC12980502 Results opening cohort description and Histopathological processing of tissues', 'Paper reports one precursor revised to LUAD; deposited P7 lesion titles/aliases already say LUAD; original diagnosis and specific revised alias remain unknown', 'historical histology mapping only')
    issue('WES_coverage_difference', 'PMC12980502 Whole-exome sequencing; GSE307529', 'Paper total samples=79 versus deposited records; do not fabricate missing normal/control libraries or equate VCF count with original sequenced sample count', 'WES sampling/denominator reconciliation')
    issue('annotation_exports_unavailable', 'source_manifest.json; annotation_availability.csv', 'Definitions recovered, actual barcode pathology/polygons/panels not qualified; publisher route also failed', 'Stages 3-6 dependent comparisons')
    csv_out(out, 'join_issues.csv', issues)
    summary = dict(analysis_id='Pg1-P01.metadata_v2', analysis_type='metadata', outcome_exposure='exposed',
        series={g: dict(platform=SERIES[g], records=sum(r['GSE']==g for r in samples),
            patient_labels=len({r['patient_id_author'] for r in samples if r['GSE']==g}),
            histology_deposited=dict(Counter(r['histology_deposited'] for r in samples if r['GSE']==g))) for g in SERIES},
        total_records=len(samples), pairs=pair_counts,
        filename_alias_discrepancies=sum(r['filename_alias_status']!='exact_author_alias' for r in samples),
        prior_comparison_rows=len(comparisons), prior_disagreements=sum(r['status']=='disagreement' for r in comparisons),
        inspected_spatial_archive_members=len(spatial_members), candidate_pathology_members=len(candidate_spatial),
        published_wes_total=79, deposited_WES_records=sum(r['platform']=='WES' for r in samples),
        stages={'0':'complete_bounded_ledger', '1':'complete_metadata_alias_and_patient_joins',
                '2':'accessible_inventory_complete_exports_unrecovered', '3':'held_annotation_geometry',
                '4':'held_author_labels_neighborhood_inputs', '5':'A12_unestimated_no_qualified_inputs_or_new_contract',
                '6':'held_TMA_manifest_and_panel', '7':'not_executed_longitudinal_functional_inputs_missing'},
        interpretation='No population inference, source independence, lesion identity, secretion, receptor activation, clone or fate established; no scientific acceptance')
    json_out(out, 'summary.json', summary)
    subprocess.run([sys.executable, str(Path(__file__).with_name('verify_metadata_v2.py')), '--run', str(out)], check=True)
    print(json.dumps({'records': len(samples), 'status': 'metadata_complete', 'verification': 'see verification.json'}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    execute(p.parse_args().output)
