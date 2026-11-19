"""Prospective S1M: selected molecular metadata and count-table structure only."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
import tempfile
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


GEO_FIELDS = {
    'title', 'geo_accession', 'type', 'source_name_ch1', 'organism_ch1',
    'characteristics_ch1', 'molecule_ch1', 'data_processing', 'platform_id',
    'library_strategy', 'library_source', 'library_selection', 'relation',
    'supplementary_file', 'supplementary_file_1', 'taxid_ch1',
}
ENA_FIELDS = {
    'study_accession', 'secondary_study_accession', 'sample_accession',
    'secondary_sample_accession', 'experiment_accession', 'run_accession',
    'sample_alias', 'experiment_alias', 'run_alias', 'sample_title',
    'experiment_title', 'tax_id', 'scientific_name', 'instrument_platform',
    'instrument_model', 'library_layout', 'library_strategy', 'library_source',
    'library_selection', 'library_name', 'base_count', 'read_count',
}
ATTRIBUTE_KEYS = re.compile(
    r'strain|tissue|cell.?type|age|sex|genotype|condition|treatment|time|day|'
    r'pool|replicat|animal|mouse|batch|reference|genome|assembly', re.I)
SPECIAL = {'N_unmapped', 'N_multimapping', 'N_noFeature', 'N_ambiguous'}
ASSEMBLY = re.compile(r'\b(?:mm\d+|GRCm\d+(?:\.p\d+)?|hg\d+|GRCh\d+(?:\.p\d+)?)\b')
ACCESSIONS = re.compile(r'\b(?:GSM\d+|SRX\d+|SRR\d+|SRS\d+|SAM[NED]\d+)\b')
GENE = re.compile(r'^ENSMUSG\d+(?:\.\d+)?$')


def unique(items):
    return sorted({str(x) for x in items if x is not None and str(x).strip()})


def joined(items):
    return ';'.join(unique(items))


def values(record, key):
    return [item['value'] for item in record.get(key, [])]


def ids(text):
    return set(ACCESSIONS.findall(text or ''))


def read_soft(path):
    samples, platforms = {}, {}
    current = None
    kind = None
    with gzip.open(path, 'rt', encoding='utf-8-sig') as handle:
        for line_number, line in enumerate(handle, 1):
            line = line.rstrip('\r\n')
            if line.startswith('^'):
                label, _, accession = line[1:].partition(' = ')
                kind = label
                current = None
                if kind in {'SAMPLE', 'PLATFORM'}:
                    target = samples if kind == 'SAMPLE' else platforms
                    current = target.setdefault(accession, {})
                continue
            if current is None or not line.startswith('!'):
                continue
            key, sep, value = line.partition(' = ')
            key = key.split('_', 1)[-1]
            allowed = GEO_FIELDS if kind == 'SAMPLE' else {'title', 'technology', 'organism'}
            if sep and key in allowed:
                current.setdefault(key, []).append({'value': value, 'line': line_number})
    return samples, platforms


def xml_root(path):
    root = ET.parse(path).getroot()
    for element in root.iter():
        element.tag = element.tag.split('}')[-1]
    return root


def identifiers(element):
    if element is None:
        return set()
    result = ids(' '.join(str(v) for v in element.attrib.values()))
    for node in element.findall('./IDENTIFIERS/*') + element.findall('./Ids/Id'):
        result.update(ids(node.text or ''))
    return result


def selected_attributes(element, biosample=False):
    out = []
    if element is None:
        return out
    if biosample:
        pairs = [(x.attrib.get('attribute_name', x.attrib.get('harmonized_name', '')),
                  x.text or '') for x in element.findall('./Attributes/Attribute')]
    else:
        pairs = [(x.findtext('TAG', ''), x.findtext('VALUE', ''))
                 for x in element.findall('./SAMPLE_ATTRIBUTES/SAMPLE_ATTRIBUTE')]
    for key, value in pairs:
        if ATTRIBUTE_KEYS.search(key):
            out.append({'key': key, 'value': value})
    return out


def read_sra(path):
    packages = []
    for package in xml_root(path).iter('EXPERIMENT_PACKAGE'):
        experiment = package.find('EXPERIMENT')
        sample = package.find('SAMPLE')
        if experiment is None:
            raise ValueError('SRA experiment package has no EXPERIMENT')
        descriptor = experiment.find('./DESIGN/SAMPLE_DESCRIPTOR')
        linked_ids = identifiers(sample) | identifiers(descriptor)
        if sample is not None:
            linked_ids.update(ids(sample.findtext('TITLE', '')))
        library = experiment.find('./DESIGN/LIBRARY_DESCRIPTOR')
        layout = library.find('LIBRARY_LAYOUT') if library is not None else None
        layouts = [child.tag for child in layout] if layout is not None else []
        model = experiment.findtext('./PLATFORM/ILLUMINA/INSTRUMENT_MODEL', '')
        platforms = [x.tag for x in experiment.findall('./PLATFORM/*')]
        runs = [run.attrib.get('accession', '') for run in package.findall('./RUN_SET/RUN')]
        packages.append({
            'experiment': experiment.attrib.get('accession', ''),
            'sample_accession': sample.attrib.get('accession', '') if sample is not None else '',
            'linked_accessions': unique(linked_ids), 'runs': unique(runs),
            'title': experiment.findtext('TITLE', ''),
            'sample_title': sample.findtext('TITLE', '') if sample is not None else '',
            'library_name': library.findtext('LIBRARY_NAME', '') if library is not None else '',
            'strategy': library.findtext('LIBRARY_STRATEGY', '') if library is not None else '',
            'source': library.findtext('LIBRARY_SOURCE', '') if library is not None else '',
            'selection': library.findtext('LIBRARY_SELECTION', '') if library is not None else '',
            'layout': joined(layouts), 'instrument_model': model,
            'instrument_platform': joined(platforms),
            'attributes': selected_attributes(sample),
            'locator': f'EXPERIMENT_PACKAGE/EXPERIMENT[@accession="{experiment.attrib.get("accession", "")}"]',
        })
    return packages


def read_ena(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle, delimiter='\t')
        rows = [{**{key: value for key, value in row.items() if key in ENA_FIELDS},
                 'source_line': n} for n, row in enumerate(reader, 2)]
    return rows


def read_biosamples(path):
    out = {}
    for sample in xml_root(path).iter('BioSample'):
        accession = sample.attrib.get('accession', '')
        if not accession or accession in out:
            raise ValueError('Missing or duplicate BioSample accession')
        out[accession] = {
            'accession': accession, 'linked_accessions': unique(identifiers(sample)),
            'title': sample.findtext('./Description/Title', ''),
            'attributes': selected_attributes(sample, biosample=True),
        }
    return out


def label_fields(title, characteristics):
    # Explicit deposit title grammar; no suffix-derived biological pairing.
    text = ' | '.join(characteristics)
    compact = re.fullmatch(r'D(?P<day>6|30|180)(?P<history>Ctrl|IMQ)l?EpdSC_R(?P<rep>[12])_(?:RNA|ATAC)-seq', title, re.I)
    wound = re.fullmatch(r'(?P<hours>6|12)hrwounding_(?P<history>Ctrl|PI)EpdSC_+R(?P<rep>[12])_RNA-seq', title, re.I)
    conflicts = []
    evidence = []
    day = hours = replicate = ''
    history = 'unknown_or_ambiguous'
    if compact:
        day, replicate = compact['day'], compact['rep']
        history = 'control' if compact['history'].lower() == 'ctrl' else 'prior_inflammation'
        evidence.append('compact GEO title')
    elif wound:
        hours, replicate = wound['hours'], wound['rep']
        history = 'control' if wound['history'].lower() == 'ctrl' else 'prior_inflammation'
        evidence.append('wound GEO title')
        explicit_days = unique(re.findall(r'wounded at (\d+) days', text, re.I))
        if len(explicit_days) == 1:
            day = explicit_days[0]
            evidence.append('day from explicit GEO wound characteristic')
    else:
        normalized = re.sub(r'[_-]+', ' ', title)
        histories = []
        if re.search(r'\b(?:control|ctrl)\b', normalized, re.I): histories.append('control')
        if re.search(r'\b(?:post\s*inflamed|imq|pi)\b', normalized, re.I): histories.append('prior_inflammation')
        history = histories[0] if len(histories) == 1 else 'unknown_or_ambiguous'
        day = joined(re.findall(r'\bD(?:ay)?\s*(\d+)\b', normalized, re.I))
        hours = joined(re.findall(r'\b(\d+)\s*(?:hr|hrs|hour|hours)\b', normalized, re.I))
        replicate = joined(re.findall(r'(?:\brep(?:licate)?|\bR)\s*(\d+)\b', normalized, re.I))
        evidence.append('tokenized GEO title; noncompact form')
    treatment = ' | '.join(x for x in characteristics if x.lower().startswith('treatment:'))
    attributed_history = []
    if re.search('imiquimod', treatment, re.I): attributed_history.append('prior_inflammation')
    if re.search('vanicream', treatment, re.I): attributed_history.append('control')
    if len(attributed_history) == 1:
        if attributed_history[0] != history:
            conflicts.append('history title/characteristic disagreement')
        else:
            evidence.append('history corroborated by GEO treatment characteristic')
    else:
        evidence.append('history not independently specified by selected characteristic')
    harvest_days = unique(re.findall(r'harvested (\d+) days', treatment, re.I))
    if harvest_days:
        if len(harvest_days) != 1 or (day and day != harvest_days[0]):
            conflicts.append('day title/harvest characteristic disagreement')
        else: evidence.append('day corroborated by explicit harvest characteristic')
    wound_hours = unique(re.findall(r'(\d+)hr wounds', treatment, re.I))
    if wound_hours:
        if len(wound_hours) != 1 or (hours and hours != wound_hours[0]):
            conflicts.append('wound hour title/characteristic disagreement')
        else: evidence.append('wound hour corroborated by GEO characteristic')
    return {'history_label': history, 'day_label': day, 'wound_hour_label': hours,
            'replicate_label': replicate, 'characteristics': characteristics,
            'label_evidence': '; '.join(evidence), 'label_conflicts': conflicts,
            'wound_status_label': 'post_wound' if hours else 'no wound stated in selected metadata'}


def count_structure(path):
    widths = Counter()
    genes, special = [], []
    invalid_numeric = 0
    other_ids = []
    blank_lines = 0
    with gzip.open(path, 'rt', encoding='utf-8-sig') as handle:
        for line in handle:
            if not line.strip():
                blank_lines += 1
                continue
            parts = line.rstrip('\r\n').split('\t')
            widths[len(parts)] += 1
            key = parts[0]
            if key in SPECIAL:
                special.append(key)
            else:
                genes.append(key)
                if not GENE.fullmatch(key):
                    other_ids.append(key)
            invalid_numeric += sum(not re.fullmatch(r'\d+', x) for x in parts[1:])
    gene_set = set(genes)
    width = next(iter(widths)) if len(widths) == 1 else None
    numeric_columns = width - 1 if width is not None else None
    if numeric_columns == 1:
        semantics = 'one nonnegative-integer gene-count column if validation passes; strand convention not established by structure'
    elif numeric_columns == 3 and set(special) == SPECIAL:
        semantics = 'STAR ReadsPerGene-compatible structure; column strand semantics require explicit documented selection before S2'
    else:
        semantics = 'column semantics unresolved; qualify before an expression comparison'
    summary = {
        'file': path.name, 'gsm': re.match(r'GSM\d+', path.name).group(),
        'data_rows': sum(widths.values()), 'gene_rows': len(genes),
        'unique_gene_ids': len(gene_set), 'duplicate_gene_rows': len(genes) - len(gene_set),
        'field_width_counts': json.dumps(dict(widths), sort_keys=True),
        'numeric_columns': numeric_columns, 'invalid_numeric_cells': invalid_numeric,
        'special_rows': joined(special), 'other_identifier_rows': len(other_ids),
        'other_identifier_examples': ';'.join(other_ids[:5]),
        'versioned_gene_ids': sum(bool(re.search(r'\.\d+$', x)) for x in gene_set),
        'blank_lines': blank_lines,
        'ordered_gene_id_sha256': hashlib.sha256(('\n'.join(genes) + '\n').encode()).hexdigest(),
        'filename_reference_hint': joined(ASSEMBLY.findall(path.name.replace('_', ' '))),
        'structure_semantics': semantics,
        'structure_pass': bool(genes and numeric_columns in {1, 3} and
                               not invalid_numeric and len(genes) == len(gene_set) and
                               not other_ids and len(special) == len(set(special))),
    }
    return summary, gene_set


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def write_tsv(path, rows):
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def run(contract_path, output):
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    root = Path(__file__).resolve().parents[3]
    declared = {Path(item['path']).name: root / item['path'] for item in contract['inputs']}
    samples, platforms = read_soft(declared['GSE92967_family.soft.gz'])
    sra = read_sra(declared['sra_experiments.xml'])
    ena = read_ena(declared['ena_read_run.tsv'])
    biosamples = read_biosamples(declared['biosamples.xml'])
    ena_by_run = defaultdict(list)
    for row in ena:
        ena_by_run[row.get('run_accession', '')].append(row)
    counts, gene_sets = [], {}
    for name, path in sorted(declared.items()):
        if re.fullmatch(r'GSM\d+_.*\.tab\.gz', name):
            summary, gene_set = count_structure(path)
            counts.append(summary)
            gene_sets[summary['gsm']] = gene_set
    count_by_gsm = defaultdict(list)
    for row in counts:
        count_by_gsm[row['gsm']].append(row)
    acquisition = []
    for name in ['acquisition_initial.json', 'acquisition_followup.json']:
        for row in json.loads(declared[name].read_text(encoding='utf-8-sig')):
            if row.get('file') in declared:
                acquisition.append({key: row.get(key) for key in
                                    ['file', 'url', 'resolved_url', 'retrieved_at_utc', 'sha256', 'bytes']})
    crosswalk, run_rows, issues = [], [], []
    label_issues = []
    selected_sources = {}
    used_experiments, used_runs = set(), set()
    for gsm, geo in sorted(samples.items()):
        title = ' | '.join(values(geo, 'title'))
        char = values(geo, 'characteristics_ch1')
        labels = label_fields(title, char)
        if labels['label_conflicts'] or labels['history_label'] == 'unknown_or_ambiguous' or not labels['day_label']:
            label_issues.append({'gsm': gsm, 'title': title, 'label_details': labels})
        geo_ids = ids(' '.join(values(geo, 'relation'))) | {gsm}
        packages = [p for p in sra if gsm in p['linked_accessions'] or p['experiment'] in geo_ids]
        experiments = unique(p['experiment'] for p in packages)
        runs = unique(run for p in packages for run in p['runs'])
        used_experiments.update(experiments)
        used_runs.update(runs)
        ena_records = [row for run in runs for row in ena_by_run.get(run, [])]
        linked_samples = set()
        for p in packages:
            linked_samples.update(x for x in p['linked_accessions'] if x.startswith('SAM'))
        for row in ena_records:
            linked_samples.update(ids(row.get('sample_accession', '')))
        bio = [biosamples[x] for x in sorted(linked_samples) if x in biosamples]
        strategies = unique(values(geo, 'library_strategy') + [p['strategy'] for p in packages])
        assay_tokens = ' '.join(strategies + [title]).lower()
        assay = 'RNA-seq' if 'rna' in assay_tokens else 'ATAC-seq' if 'atac' in assay_tokens else 'unknown'
        processing = values(geo, 'data_processing')
        references = unique(ASSEMBLY.findall(' '.join(processing)))
        supplements = [value for key in geo if key.startswith('supplementary_file') for value in values(geo, key)]
        supplement_names = {Path(unquote(urlsplit(x).path)).name for x in supplements}
        count_rows = count_by_gsm.get(gsm, [])
        count_names = [x['file'] for x in count_rows]
        if not packages or not runs:
            issues.append({'gsm': gsm, 'issue': 'no explicit SRA experiment/run join'})
        if len(packages) != 1:
            issues.append({'gsm': gsm, 'issue': 'SRA experiment multiplicity', 'count': len(packages)})
        if any(len(ena_by_run.get(run, [])) != 1 for run in runs):
            issues.append({'gsm': gsm, 'issue': 'missing or duplicate ENA run row'})
        if any(name not in supplement_names for name in count_names):
            issues.append({'gsm': gsm, 'issue': 'count filename not in GEO supplementary-file field'})
        for run in runs:
            package_matches = [p for p in packages if run in p['runs']]
            if len(package_matches) != 1:
                issues.append({'gsm': gsm, 'run': run, 'issue': 'ambiguous run-to-experiment join'})
            for p in package_matches:
                erows = ena_by_run.get(run, [])
                for erow in erows or [{}]:
                    mismatches = []
                    for skey, ekey in [('experiment', 'experiment_accession'),
                                       ('layout', 'library_layout'), ('instrument_model', 'instrument_model')]:
                        if p[skey] and erow.get(ekey) and p[skey].upper() != erow[ekey].upper():
                            mismatches.append(ekey)
                    if mismatches:
                        issues.append({'gsm': gsm, 'run': run, 'issue': 'SRA/ENA field disagreement', 'fields': mismatches})
                    run_rows.append({'gsm': gsm, 'experiment': p['experiment'], 'run': run,
                                     'sra_sample': p['sample_accession'],
                                     'biosample': erow.get('sample_accession', ''),
                                     'sra_layout': p['layout'], 'ena_layout': erow.get('library_layout', ''),
                                     'sra_instrument': p['instrument_model'],
                                     'ena_instrument': erow.get('instrument_model', ''),
                                     'ena_experiment': erow.get('experiment_accession', ''),
                                     'ena_source_line': erow.get('source_line', ''),
                                     'disagreements': ';'.join(mismatches)})
        pool_claim = ('final paper review: four animals per condition in duplicate; manuscript: 3-4'
                      if assay == 'RNA-seq' else
                      'final paper review: three pooled mice per group in duplicate'
                      if assay == 'ATAC-seq' else 'not assigned')
        crosswalk.append({
            'gsm': gsm, 'title': title, 'assay': assay, 'history_label': labels['history_label'],
            'day_label': labels['day_label'], 'wound_hour_label': labels['wound_hour_label'],
            'replicate_label': labels['replicate_label'], 'label_evidence': labels['label_evidence'],
            'label_conflicts': ';'.join(labels['label_conflicts']), 'wound_status_label': labels['wound_status_label'],
            'experiments': joined(experiments),
            'runs': joined(runs), 'biosamples': joined(linked_samples),
            'geo_platform': joined(values(geo, 'platform_id')),
            'instrument_models': joined([p['instrument_model'] for p in packages] +
                                        [row.get('instrument_model', '') for row in ena_records]),
            'library_layouts': joined([p['layout'] for p in packages] +
                                      [row.get('library_layout', '') for row in ena_records]),
            'library_strategies': joined(strategies),
            'organism': joined(values(geo, 'organism_ch1')), 'source_compartment': joined(values(geo, 'source_name_ch1')),
            'characteristics': ' | '.join(char), 'processing_reference': joined(references),
            'processing_metadata': ' | '.join(processing), 'count_files': joined(count_names),
            'count_declared_by_geo': all(name in supplement_names for name in count_names) if count_names else '',
            'filename_reference_hint': joined(x['filename_reference_hint'] for x in count_rows),
            'pooling_claim_attributed': pool_claim,
            'exact_pool_to_library_map': 'not established by accessions or replicate suffixes',
            'animal_ids_and_overlap': 'unknown unless explicitly evidenced in selected source attributes',
            'cross_assay_pairing': 'not established; no suffix-based pairing',
        })
        selected_sources[gsm] = {'geo_fields_with_line_numbers': geo, 'sra': packages,
                                 'ena': ena_records, 'biosamples': bio}
    for gsm in count_by_gsm:
        if gsm not in samples:
            issues.append({'gsm': gsm, 'issue': 'count file has no GEO sample record'})
    pairwise = []
    keys = sorted(gene_sets)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            pairwise.append({'a': a, 'b': b, 'intersection': len(gene_sets[a] & gene_sets[b]),
                             'a_only': len(gene_sets[a] - gene_sets[b]), 'b_only': len(gene_sets[b] - gene_sets[a])})
    common = set.intersection(*gene_sets.values()) if gene_sets else set()
    union = set.union(*gene_sets.values()) if gene_sets else set()
    groups = []
    group_map = defaultdict(list)
    for row in crosswalk:
        group_map[(row['assay'], row['day_label'], row['wound_hour_label'], row['history_label'])].append(row)
    for group, rows in sorted(group_map.items()):
        groups.append({'assay': group[0], 'day': group[1], 'wound_hours': group[2], 'history': group[3],
                       'libraries': len(rows), 'gsm': [r['gsm'] for r in rows],
                       'platforms': unique(r['geo_platform'] for r in rows),
                       'instruments': unique(r['instrument_models'] for r in rows),
                       'references': unique(r['processing_reference'] for r in rows)})
    summary = {'stage': 'S1M', 'analysis_id': contract['analysis_id'],
               'geo_samples': len(samples), 'sra_experiments': len(sra), 'ena_runs': len(ena),
               'biosample_records': len(biosamples), 'count_files': len(counts),
               'assay_counts': dict(Counter(r['assay'] for r in crosswalk)),
               'metadata_join_issues': issues, 'label_qualification_issues': label_issues,
               'unjoined_sra_experiments': sorted({p['experiment'] for p in sra} - used_experiments),
               'unjoined_ena_runs': sorted({r.get('run_accession', '') for r in ena} - used_runs),
               'count_structure_failures': [r['file'] for r in counts if not r['structure_pass']],
               'common_gene_ids': len(common), 'union_gene_ids': len(union),
               'all_count_id_orders_identical': len({r['ordered_gene_id_sha256'] for r in counts}) == 1,
               'groups': groups,
               'inference_limit': 'Metadata qualification only; no gene effects or independently verified animal/pool pairing.'}
    write_tsv(output / 'library_crosswalk.tsv', crosswalk)
    write_tsv(output / 'run_crosswalk.tsv', run_rows)
    write_tsv(output / 'count_structure.tsv', counts)
    write_json(output / 'source_fields.json', {'acquisition': acquisition, 'geo_platforms': platforms,
                                             'selected_source_fields': selected_sources})
    write_json(output / 'identifier_coverage.json', {'common': len(common), 'union': len(union),
                                                   'pairwise': pairwise})
    write_json(output / 'qualification.json', summary)
    report = ['# S1M molecular metadata execution', '',
              f'Analysis: `{contract["analysis_id"]}`. These are source and structure observations, not expression effects.', '',
              f'GEO libraries: {len(samples)}; SRA experiments: {len(sra)}; ENA runs: {len(ena)}; BioSample records: {len(biosamples)}.',
              f'Count files: {len(counts)}; shared gene IDs: {len(common)}; union: {len(union)}.',
              f'Join issues: {len(issues)}; label issues: {len(label_issues)}; count-structure failures: {len(summary["count_structure_failures"])}.', '',
              '| Assay | Day label | Wound-hour label | History label | Libraries | Instrument models | Reference metadata |',
              '|---|---|---|---|---:|---|---|']
    for g in groups:
        report.append('| ' + ' | '.join([g['assay'], g['day'], g['wound_hours'], g['history'],
                                        str(g['libraries']), '; '.join(g['instruments']), '; '.join(g['references'])]) + ' |')
    report += ['', '## Eligibility interpretation pending source review', '',
               'Explicit accessions establish a metadata join, not independent animals. The existing paper review attributes pooled duplicate preparations to the assays; exact animal identities, overlap and cross-assay pairing are not supplied by a replicate suffix.', '',
               'Within-time control/history groups with qualified structure can support a descriptive processed-count comparison. Formal inference requires an explicit assessment of pool/preparation evidence. Platform/time associations qualify cross-time effects without automatically invalidating within-time comparisons. Raw-layout conflicts restrict exact raw replay, not automatically processed-count use.', '',
               'Column selection, feature universe, normalization and the exact comparison must be frozen in a separate S2 contract after review. No normalization, differential expression, statistical testing, equivalence claim or functional inference was performed.', '',
               'This stage does not qualify source workbooks, functional measurements, chromatin signal normalization or whole-paper methods. The original restrictions and remaining stages are retained.', '']
    (output / 'S1M_REPORT.md').write_text('\n'.join(report), encoding='utf-8')
    print(json.dumps({k: summary[k] for k in ['analysis_id', 'geo_samples', 'sra_experiments', 'ena_runs',
                                             'count_files', 'assay_counts', 'common_gene_ids']}))


def self_test():
    # Synthetic fixtures only; this route never opens research inputs.
    assert label_fields('RNA_D6_Control_R1', [])['history_label'] == 'control'
    assert label_fields('RNA_D30_Postinflamed_R2', [])['day_label'] == '30'
    assert label_fields('RNA_PI_6hr_Rep2', [])['wound_hour_label'] == '6'
    assert label_fields('RNA_D6_Control_R1', [])['replicate_label'] == '1'
    assert label_fields('RNA_D6_unknown_R1', [])['history_label'] == 'unknown_or_ambiguous'
    assert label_fields('D30CtrlEpdSC_R1_RNA-seq', ['treatment: vanicream for 6 days and harvested 30 days after treatment'])['day_label'] == '30'
    assert label_fields('D6IMQlEpdSC_R2_ATAC-seq', ['treatment: topical imiquimod for 6 days'])['history_label'] == 'prior_inflammation'
    assert label_fields('6hrwounding_PIEpdSC__R1_RNA-seq', ['treatment: imiquimod and wounded at 30 days. 6hr wounds were harvested'])['day_label'] == '30'
    assert label_fields('D30CtrlEpdSC_R1_RNA-seq', ['treatment: imiquimod'])['label_conflicts']
    assert label_fields('D180IMQEpdSC_R2_ATAC-seq', [])['history_label'] == 'prior_inflammation'
    with tempfile.TemporaryDirectory() as temp:
        folder = Path(temp)
        path = folder / 'GSM9999999_mm10.tab.gz'
        with gzip.open(path, 'wt') as handle:
            handle.write('ENSMUSG000001.1\t1\nENSMUSG000002.2\t0\n')
        result, genes = count_structure(path)
        assert result['structure_pass'] and len(genes) == 2 and result['numeric_columns'] == 1
        with gzip.open(path, 'wt') as handle:
            handle.write('ENSMUSG000001\t-1\nENSMUSG000001\t2\n')
        result, _ = count_structure(path)
        assert not result['structure_pass'] and result['duplicate_gene_rows'] == 1
        soft = folder / 'synthetic.soft.gz'
        with gzip.open(soft, 'wt') as handle:
            handle.write('^SAMPLE = GSM9999999\n!Sample_title = RNA_D6_Control_R1\n!Sample_extract_protocol_ch1 = excluded\n!Sample_relation = SRA: https://example.invalid/SRX9999999\n')
        samples, _ = read_soft(soft)
        assert 'extract_protocol_ch1' not in samples['GSM9999999']
        assert values(samples['GSM9999999'], 'title') == ['RNA_D6_Control_R1']
        srafile = folder / 'synthetic.xml'
        srafile.write_text('<EXPERIMENT_PACKAGE_SET><EXPERIMENT_PACKAGE><EXPERIMENT accession="SRX9999999"><DESIGN><SAMPLE_DESCRIPTOR accession="SRS9999999"/><LIBRARY_DESCRIPTOR><LIBRARY_STRATEGY>RNA-Seq</LIBRARY_STRATEGY><LIBRARY_LAYOUT><PAIRED/></LIBRARY_LAYOUT></LIBRARY_DESCRIPTOR></DESIGN></EXPERIMENT><SAMPLE accession="SRS9999999" alias="GSM9999999"><IDENTIFIERS><EXTERNAL_ID namespace="BioSample">SAMN9999999</EXTERNAL_ID></IDENTIFIERS></SAMPLE><RUN_SET><RUN accession="SRR9999999"/></RUN_SET></EXPERIMENT_PACKAGE></EXPERIMENT_PACKAGE_SET>', encoding='utf-8')
        packages = read_sra(srafile)
        assert packages[0]['layout'] == 'PAIRED' and packages[0]['runs'] == ['SRR9999999']
        assert {'GSM9999999', 'SAMN9999999'} <= set(packages[0]['linked_accessions'])
        assert 'GSM8888888' not in packages[0]['linked_accessions']
    print('Synthetic metadata/parser checks passed; no scientific input read.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.contract and args.output and args.output.is_dir():
        run(args.contract, args.output)
    else:
        parser.error('Use the research runner with --contract and its existing --output directory')
