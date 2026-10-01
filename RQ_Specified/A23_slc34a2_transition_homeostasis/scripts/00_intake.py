"""Audit inherited A23 results and source eligibility without new biological fits."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path

QUESTION = Path(__file__).resolve().parents[1]
ROOT = QUESTION.parents[1]
NB3 = ROOT / 'Research Article/gate2_N2_nabhan_2026'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def table(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t'))


def verify_inputs(root, entries):
    for item in entries:
        path = (root / item['path']).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError('Input outside repository')
        if not path.is_file() or digest(path) != item['sha256']:
            raise ValueError(f"Input hash mismatch: {item['path']}")


def guard_outputs(paths):
    if any(path.exists() for path in paths):
        raise FileExistsError('Intake output exists; use --check or a new versioned implementation')


def eligible(source, fields):
    return all(source.get(key) is True for key in fields)


def write_tsv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    contract_path = QUESTION / 'config/intake_v1.json'
    contract = load(contract_path)
    verify_inputs(ROOT, contract['inputs'])
    directories = [QUESTION / f'{part}/intake_v1' for part in ('metadata', 'tables', 'reports')]
    meta, tables, reports = directories
    receipt = meta / 'run_record.json'
    if args.check:
        record = load(receipt)
        verify_inputs(ROOT, record['inputs'])
        verify_inputs(ROOT, record['outputs'])
        if record['status'] != 'PASS_intake_only':
            raise ValueError('Archived intake failed')
        print(f"A23 archived intake PASS: {record['checks']} recorded checks; hashes verified; no fits")
        return
    guard_outputs(directories)
    checks = len(contract['inputs'])

    def require(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            raise ValueError(message)

    def one(rows, **keys):
        matches = [r for r in rows if all(r.get(k) == v for k, v in keys.items())]
        require(len(matches) == 1, f'Expected one row for {keys}, got {len(matches)}')
        return matches[0]

    followup = NB3 / 'runs/followup_v1'
    original = load(followup / 'run_record.json')
    for item in contract['inputs']:
        path = ROOT / item['path']
        if path.parent == followup and path.suffix == '.tsv':
            require(original['output_sha256'].get(path.name) == item['sha256'], f'Original receipt mismatch: {path.name}')
    source_config = load(NB3 / 'config/Nb3_followup_v1.json')
    require(digest(NB3 / 'config/Nb3_followup_v1.json') == original['config_sha256'], 'Source panel config differs from original receipt')
    for name in contract['baseline_programs']:
        genes = source_config['programs']['mouse'][name]
        require(not any(g.lower() == 'slc34a2' for g in genes), f'Target gene in its own state score: {name}')
    evidence = []

    def add(kind, endpoint, variant, value, units, source):
        evidence.append(dict(kind=kind, endpoint=endpoint, variant=variant, value=value, source_units=units, source=source))

    baseline = table(NB3 / 'runs/R4_v1/fixed_panel_effects.tsv')
    for program, expected in contract['baseline_programs'].items():
        row = one(baseline, target=contract['target'], species='mouse', program=program)
        require(round(float(row['effect']), 3) == expected, f'Baseline changed: {program}')
        require(int(row['target_wells']) == contract['baseline_wells'] and row['plates'] == contract['plate'], 'Mouse-QC population changed')
        add('baseline', program, 'mouse_QC', row['effect'], '8 target wells on plate4; independent preparations unresolved', 'runs/R4_v1/fixed_panel_effects.tsv')
    markers = [r for r in table(followup / 'individual_marker_effects.tsv') if r['target'] == contract['target'] and r['species'] == 'mouse' and r['program'] == 'transition_figure3']
    require(sorted(r['gene'] for r in markers) == sorted(contract['transition_markers']), 'Transition marker list changed')
    for row in markers:
        require(float(row['effect']) > 0, 'Transition marker direction changed')
        add('individual_marker', row['gene'], 'mouse_QC', row['effect'], '8 technical target wells', 'runs/followup_v1/individual_marker_effects.tsv')
    summaries = table(followup / 'panel_sensitivity_summary.tsv')
    transition = [r for r in summaries if r['target'] == contract['target'] and r['species'] == 'mouse' and r['program'] == 'transition_figure3']
    require(len(transition) == 4, 'Expected four transition sensitivity variants')
    for row in transition:
        require(int(row['same_direction']) == int(row['estimable']) > 0 and float(row['effect_min']) > 0, 'Transition sensitivity changed')
        for bound in ('min', 'max'):
            add('sensitivity_range', 'transition_figure3', row['variant']+'_'+bound, row['effect_'+bound], 'technical omission/control range, not a confidence interval', 'runs/followup_v1/panel_sensitivity_summary.tsv')
    counter = one(summaries, target=contract['target'], species='mouse', program='AT1_maintext', variant='omit_gene')
    require(float(counter['effect_min']) < 0 < float(counter['effect_max']), 'AT1 sign-change counterexample missing')
    require(int(counter['same_direction']) < int(counter['estimable']), 'AT1 sign-change count missing')
    for bound in ('min', 'max'):
        add('counterexample', 'AT1_maintext', 'omit_gene_'+bound, counter['effect_'+bound], 'near-zero marker summary; not preserved function', 'runs/followup_v1/panel_sensitivity_summary.tsv')
    depth = table(followup / 'paired_depth_effects.tsv')
    for variant, expected in contract['paired_AT2'].items():
        row = one(depth, target=contract['target'], species='mouse', program='AT2_figure3', variant=variant)
        require(round(float(row['effect']), 3) == expected, 'Paired AT2 estimate changed')
        require(int(row['target_wells']) == contract['paired_depth_wells'], 'Paired subset mislabeled as eight wells')
        add('depth_sensitivity', 'AT2_figure3', variant, row['effect'], '7 paired-QC target wells; conditioning is not causal adjustment', 'runs/followup_v1/paired_depth_effects.tsv')
    require(not any(r['target'] == contract['target'] and r['program'] == 'transition_figure3' for r in depth), 'Depth transition scope changed; review current wording')
    target = one(table(followup / 'target_transcript_checks.tsv'), target=contract['target'])
    require(target['ID'] == 'ENSMUSG00000029188' and float(target['logFC']) < 0, 'Target stable ID or RNA direction changed')
    add('target_RNA', 'Slc34a2', 'gene_DE', target['logFC'], 'transcript consistency; not protein or transport validity', 'runs/followup_v1/target_transcript_checks.tsv')
    external = load(QUESTION / 'metadata/external_source_v1/GSE199329_metadata.json')
    require(set(external['samples']) == {'GSM5970468', 'GSM5970469', 'GSM5970470'}, 'External sample inventory changed')
    for gsm, label in [('GSM5970468', 'CD45- PAM lung'), ('GSM5970469', 'CD45+ PAM lung'), ('GSM5970470', 'Normal Donor lung 24 years old')]:
        require('!Sample_source_name_ch1 = '+label in external['samples'][gsm], 'External source fraction changed')
    sources = load(QUESTION / 'config/source_registry.json')['sources']
    gates = []
    for source in sources:
        core = ['replication_resolved', 'slc34a2_exposure_validated', 'linked_transport_state']
        gates.append(dict(source_id=source['id'], source_group=source['source_group'], role=source['role'], P4_time_eligible=eligible(source, core+['linked_temporal_state_identity']), P5_recovery_eligible=eligible(source, core+['linked_restoration_mature_output']), allowed_use=source['use'], hold=source['hold']))
    require(not any(r['P4_time_eligible'] or r['P5_recovery_eligible'] for r in gates), 'Eligibility changed; require a source-specific contract')
    for path in directories:
        path.mkdir(parents=True)
    write_tsv(tables / 'evidence.tsv', evidence)
    write_tsv(tables / 'source_gates.tsv', gates)
    report = f'''# A23 intake: evidence and source roles verified

**PASS: {checks} checks.** No new biological model, expression-matrix analysis
or functional validation was run. This audit extracts {len(evidence)} existing
values/range endpoints and records {len(gates)} source-role decisions.

The transition contrast remains +0.524, with all three markers and the tested
control/gene/well omission summaries positive. The baseline mouse-QC comparison
uses eight target wells. Paired AT2 is -0.136 before and -0.219 after depth
conditioning, using seven paired-QC target wells. That different population
must remain explicit. No transition-panel depth fit exists in that follow-up.
The AT1 marker-omission sign change is retained, and lower Slc34a2 transcript
does not establish transport failure. No biological confidence is inferred
from technical wells or marker omission ranges.

[Evidence table](../../tables/intake_v1/evidence.tsv) |
[Source gates](../../tables/intake_v1/source_gates.tsv) |
[Hash receipt](../../metadata/intake_v1/run_record.json).

GSE199329 metadata resolve three libraries and their CD45 sampling fractions.
They do not supply replicated cases. The next step is processed-file/epithelial
coverage and annotation inspection, followed by a separately frozen descriptive
P2 contract if eligible. The advertised biochemical workbook remains an
endpoint-audit lead. The five-source inventory admits no linked replicated
temporal/transport/restoration test; this is a bounded review, not an exhaustive
claim that suitable data do not exist. [Pipeline](../../PIPELINE.md) |
[Source guide](../../SOURCES.md) | [Sample roles](../../metadata/external_source_v1/SAMPLE_ROLES.md).
'''
    (reports / 'INTAKE.md').write_text(report, encoding='utf-8', newline='\n')
    extra = [contract_path, QUESTION / 'config/pipeline_draft.json', QUESTION / 'config/source_registry.json', QUESTION / 'config/sample_manifest_schema.json', Path(__file__)]
    inputs = contract['inputs'] + [dict(path=p.relative_to(ROOT).as_posix(), sha256=digest(p)) for p in extra]
    outputs = [tables / 'evidence.tsv', tables / 'source_gates.tsv', reports / 'INTAKE.md']
    record = dict(schema='a23-intake-record/v1', date=contract['date'], status='PASS_intake_only', checks=checks, evidence_rows=len(evidence), source_rows=len(gates), new_biological_fits=False, inputs=inputs, outputs=[dict(path=p.relative_to(ROOT).as_posix(), sha256=digest(p)) for p in outputs])
    receipt.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(f'A23 intake PASS: {checks} checks; {len(evidence)} inherited values; {len(gates)} source gates; no new fits')


if __name__ == '__main__':
    main()
