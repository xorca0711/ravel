"""Verify inherited A22 evidence and source gates; never refit biology."""
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
    config_path = QUESTION / 'config/intake_v1.json'
    contract = load(config_path)
    verify_inputs(ROOT, contract['inputs'])
    destinations = [QUESTION / f'{part}/intake_v1' for part in ('metadata', 'tables', 'reports')]
    meta, tables, reports = destinations
    receipt = meta / 'run_record.json'
    if args.check:
        record = load(receipt)
        verify_inputs(ROOT, record['inputs'])
        verify_inputs(ROOT, record['outputs'])
        if record['status'] != 'PASS_intake_only':
            raise ValueError('Archived intake did not pass')
        print(f"A22 archived intake PASS: {record['checks']} recorded checks; hashes verified; no new fits")
        return
    guard_outputs(destinations)
    checks = len(contract['inputs'])

    def require(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            raise ValueError(message)

    def one(rows, **keys):
        selected = [row for row in rows if all(row.get(k) == v for k, v in keys.items())]
        require(len(selected) == 1, f'Expected one row for {keys}, got {len(selected)}')
        return selected[0]

    followup = NB3 / 'runs/followup_v1'
    original = load(followup / 'run_record.json')
    for item in contract['inputs']:
        path = ROOT / item['path']
        if path.parent == followup and path.suffix == '.tsv':
            require(original['output_sha256'].get(path.name) == item['sha256'], f'Original receipt mismatch: {path.name}')
    require('human numeric S5 discrepancy' in original['unresolved'], 'Missing inherited S5 hold')
    baseline = table(NB3 / 'runs/R4_v1/fixed_panel_effects.tsv')
    sensitivities = table(followup / 'panel_sensitivity_summary.tsv')
    evidence = []

    def add(kind, species, endpoint, variant, value, units, source):
        evidence.append(dict(kind=kind, species=species, endpoint=endpoint, variant=variant, value=value, source_units=units, source=source))

    for endpoint in contract['endpoints']:
        keys = {k: endpoint[k] for k in ('species', 'program')}
        row = one(baseline, target=contract['target'], **keys)
        require(round(float(row['effect']), 3) == endpoint['expected_rounded_effect'], 'Baseline value changed')
        require(row['target_wells'] == '4' and row['plates'] == 'plate1', 'Focal well/plate structure changed')
        summaries = [r for r in sensitivities if r['target'] == contract['target'] and all(r[k] == v for k, v in keys.items())]
        require(len(summaries) == 4, 'Expected four control/gene/well sensitivity variants')
        for summary in summaries:
            require(int(summary['same_direction']) == int(summary['estimable']) > 0, 'Sensitivity direction unsupported')
        add('baseline', row['species'], row['program'], 'source_v1', row['effect'], '4 technical target wells; preparation independence unresolved', 'runs/R4_v1/fixed_panel_effects.tsv')
    markers = [r for r in table(followup / 'individual_marker_effects.tsv') if r['target'] == contract['target'] and r['species'] == 'human' and r['program'] == 'chemokines_figure4']
    require(sorted(r['gene'] for r in markers) == sorted(contract['expected_chemokine_genes']), 'Chemokine list mismatch')
    for row in markers:
        require(float(row['effect']) < 0, 'Chemokine direction changed')
        add('individual_marker', 'human', row['gene'], 'source_followup', row['effect'], 'technical-well contrast; not secretion', 'runs/followup_v1/individual_marker_effects.tsv')
    for row in table(followup / 'paired_depth_associations.tsv'):
        if row['population'] not in ('common_estimable', 'common_without_NKX21'):
            continue
        expected_n = contract['expected_common_targets'] - (row['population'] == 'common_without_NKX21')
        require(int(row['targets']) == expected_n, 'Common target population changed')
        add('cross_target_association', 'paired', 'AT2_chemokines', row['variant']+'__'+row['population'], row['spearman'], f'{expected_n} target contrasts; not independent preparations', 'runs/followup_v1/paired_depth_associations.tsv')
    for species, program in (('mouse', 'AT2_figure3'), ('human', 'chemokines_figure4')):
        for variant in ('paired_baseline', 'paired_depth'):
            row = one(table(followup / 'paired_depth_effects.tsv'), target=contract['target'], species=species, program=program, variant=variant)
            require(float(row['effect']) < 0, 'Focal depth direction changed')
            add('depth_sensitivity', species, program, variant, row['effect'], '4 target wells; depth conditioning is not causal adjustment', 'runs/followup_v1/paired_depth_effects.tsv')
    target = one(table(followup / 'target_transcript_checks.tsv'), target=contract['target'])
    require(float(target['logFC']) > 0, 'Revisit target-RNA/protein distinction')
    registry_path = QUESTION / 'config/source_registry.json'
    sources = load(registry_path)['sources']
    rna_fields = ['independent_of_Nb3', 'units_resolved', 'linked_epithelial_and_fibroblast_RNA', 'verified_identity_perturbation_per_unit']
    functional_fields = ['units_resolved', 'verified_identity_perturbation_per_unit', 'attributed_secreted_output', 'recipient_function']
    gates = [dict(accession=s['accession'], role=s['role'], allowed_use=s['allowed_use'], P4_RNA_eligible=eligible(s, rna_fields), P5_minimum_endpoint_gate=eligible(s, functional_fields), remaining_hold=s['hold']) for s in sources]
    require(not any(r['P4_RNA_eligible'] or r['P5_minimum_endpoint_gate'] for r in gates), 'Eligibility changed; review a source-specific contract')
    for path in destinations:
        path.mkdir(parents=True)
    write_tsv(tables / 'evidence.tsv', evidence)
    write_tsv(tables / 'source_gates.tsv', gates)
    report = f'''# A22 intake: inherited evidence verified

**PASS: {checks} checks.** This run extracts already exposed Nb3 evidence and
records source eligibility. It performs no new biological fit, no raw-data
analysis, and no independent validation.

The baseline contrasts remain AT2 -2.072, fibroblast chemokines -3.357 and
wound markers +1.468. All seven saved individual chemokine effects are negative.
Saved control, gene and well sensitivities retain the three panel directions.
The 195-target AT2/chemokine correlation is about 0.210, falling to 0.151 with
depth covariates and 0.138 after omitting NKX21 in that conditional comparison.
Technical sensitivity is not biological replication.

[Extracted values](../../tables/intake_v1/evidence.tsv) |
[Source gates](../../tables/intake_v1/source_gates.tsv) |
[Hash receipt](../../metadata/intake_v1/run_record.json).

The four nominated deposits admit no independent A22 RNA validation or
functional test on the available evidence. This bounded intake does not imply
an exhaustive absence. P2 can proceed to a new exploratory join/model contract;
P3 needs spatial identity/design reconciliation; P4/P5 need eligible linked
measurements and biological units. See [pipeline](../../PIPELINE.md) and
[sources](../../SOURCES.md) for the next actions.

The human S5 numeric reproduction conflict remains open. Nkx2-1 RNA increases
despite the paper's reported protein loss; RNA alone cannot certify exposure.
No pathway, immune recruitment or clinical mechanism is established here.
'''
    (reports / 'INTAKE.md').write_text(report, encoding='utf-8', newline='\n')
    extra = [config_path, registry_path, QUESTION / 'config/pipeline_draft.json', QUESTION / 'config/sample_manifest_schema.json', Path(__file__)]
    inputs = contract['inputs'] + [dict(path=p.relative_to(ROOT).as_posix(), sha256=digest(p)) for p in extra]
    outputs = [tables / 'evidence.tsv', tables / 'source_gates.tsv', reports / 'INTAKE.md']
    record = dict(schema='a22-intake-record/v1', status='PASS_intake_only', date=contract['date'], checks=checks, new_biological_fits=False, evidence_rows=len(evidence), source_rows=len(gates), inputs=inputs, outputs=[dict(path=p.relative_to(ROOT).as_posix(), sha256=digest(p)) for p in outputs])
    receipt.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(f'A22 intake PASS: {checks} checks; {len(evidence)} inherited evidence rows; {len(gates)} source gates; no new fits')


if __name__ == '__main__':
    main()
