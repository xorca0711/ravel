"""Prospective research contracts and evidence checks; standard library only.

These checks verify declared structure and provenance, not scientific truth.
Historical evidence is indexed, never retrospectively preregistered.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

SCIENTIFIC_ROOTS = ('analysis/', 'Research Article/', 'RQ_Specified/')
ASSET_SUFFIXES = {'.py', '.r', '.ipynb', '.json', '.csv', '.tsv', '.png', '.svg', '.pdf', '.rds', '.h5ad', '.parquet'}
DOSSIER_SECTIONS = ('Biological problem', 'Established knowledge', 'Repository evidence',
                    'Unresolved gap', 'Working hypothesis', 'Competing explanations',
                    'Discriminating outcomes', 'Next investigation', 'Experimental bridge',
                    'Interpretation boundary', 'Decision and maturity')


class ResearchError(ValueError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def content_hash(path: Path) -> str:
    """Git text checkouts can differ only in line endings; binary hashes stay exact."""
    data = path.read_bytes()
    if path.suffix.lower() in {'.py', '.r', '.json', '.csv', '.tsv', '.svg', '.ipynb'}:
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def within(root: Path, relative: str, *, exists=True) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ResearchError(f'Expected repository-relative POSIX path: {relative!r}')
    p = PurePosixPath(relative)
    if p.is_absolute() or '..' in p.parts or ':' in relative:
        raise ResearchError(f'Unsafe path: {relative}')
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ResearchError(f'Path escapes root: {relative}')
    if exists and not target.is_file():
        raise ResearchError(f'Missing file: {relative}')
    return target


def schema_errors(value, schema: dict, at='$') -> list[str]:
    """The deliberately small JSON Schema subset used by contract.schema.json."""
    errors = []
    kind = schema.get('type')
    matches = {'object': isinstance(value, dict), 'array': isinstance(value, list),
               'string': isinstance(value, str), 'boolean': isinstance(value, bool),
               'integer': isinstance(value, int) and not isinstance(value, bool)}
    if kind and not matches.get(kind, False):
        return [f'{at}: expected {kind}']
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{at}: invalid value {value!r}')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                errors.append(f'{at}: missing {key}')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            errors.extend(f'{at}: unknown field {key}' for key in value if key not in props)
        for key in value.keys() & props.keys():
            errors.extend(schema_errors(value[key], props[key], f'{at}.{key}'))
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(f'{at}: too few items')
        if schema.get('uniqueItems') and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            errors.append(f'{at}: duplicate items')
        for i, item in enumerate(value):
            errors.extend(schema_errors(item, schema.get('items', {}), f'{at}[{i}]'))
    if isinstance(value, str):
        if len(value.strip()) < schema.get('minLength', 0):
            errors.append(f'{at}: empty or too short')
        if schema.get('pattern') and re.fullmatch(schema['pattern'], value) is None:
            errors.append(f'{at}: invalid format')
    return errors


def contract_errors(root: Path, contract: dict, *, check_inputs=False) -> list[str]:
    schema = read_json(root / 'analysis/research/contract.schema.json')
    errors = schema_errors(contract, schema)
    if errors:
        return errors
    index = read_json(root / 'analysis/research/registry.json')
    owners = {q['id'] for q in index['questions']} | {q['id'] for q in index['article_candidates']}
    if contract['owner'] not in owners:
        errors.append('Unknown question/candidate owner')
    if contract['analysis_type'] == 'confirmatory' and contract['prior_outcome_exposure'] != 'unexposed':
        errors.append('Confirmatory execution requires unexposed outcomes; a new freeze does not erase exposure')
    if contract['inference_scope'] != 'descriptive' and contract['unit_status'] != 'verified':
        errors.append('Population inference requires verified independent biological units')
    if contract['analysis_type'] == 'metadata' and contract['inference_scope'] != 'descriptive':
        errors.append('Metadata work cannot carry population or causal inference')
    if contract['inference_scope'] == 'causal' and contract['design_identifiability'] != 'supported':
        errors.append('A causal test needs a supported intervention/identification design')
    if contract['analysis_type'] == 'confirmatory' and contract['precision_status'] != 'justified':
        errors.append('Confirmation requires a justified precision/effect-margin basis')
    sources = contract['inputs']
    for source in sources:
        try:
            within(root, source['path'], exists=False)
        except ResearchError as exc:
            errors.append(str(exc))
    if len({x['path'] for x in sources}) != len(sources):
        errors.append('Duplicate input path')
    discovery = [s for s in sources if s['role'] == 'discovery']
    validation = [s for s in sources if s['role'] == 'validation']
    if contract['validation_scope'] == 'external':
        if not validation or not discovery:
            errors.append('External validation must identify discovery and validation sources')
        for a in discovery:
            for b in validation:
                if (a['study_id'] == b['study_id'] or a['sha256'] == b['sha256'] or
                        set(a['unit_ids']) & set(b['unit_ids'])):
                    errors.append('Discovery/validation overlap: cannot claim independent external validation')
        if any(s['independence'] != 'verified' or not s['unit_ids'] for s in sources if s['role'] in {'discovery','validation'}):
            errors.append('External validation needs verified source units and overlap accounting')
    if contract['analysis_type'] == 'confirmatory' and any(s['exposure'] != 'unexposed' for s in validation):
        errors.append('Previously exposed validation outcomes cannot be labelled confirmatory')
    if contract['entrypoint'] not in [x['path'] for x in contract['code']]:
        errors.append('Entrypoint must be hash-bound in code')
    if not any('{run_dir}' in arg for arg in contract['arguments']):
        errors.append('Arguments must route outputs through {run_dir}')
    for ref in contract['evidence_refs']:
        try:
            within(root, ref)
        except ResearchError as exc:
            errors.append(str(exc))
    for asset in contract['code'] + (sources if check_inputs else []):
        try:
            path = within(root, asset['path'])
            if sha256(path) != asset['sha256']:
                errors.append(f'Hash mismatch: {asset["path"]}')
        except ResearchError as exc:
            errors.append(str(exc))
    for output in contract['expected_outputs']:
        try:
            within(root, output, exists=False)
        except ResearchError as exc:
            errors.append(str(exc))
        if output in {'receipt.json', 'stdout.log', 'stderr.log'}:
            errors.append('Expected output uses runner-reserved name')
    if contract['amendment_of']:
        try:
            predecessor = read_json(within(root, contract['amendment_of']))
            if predecessor['analysis_id'] == contract['analysis_id']:
                errors.append('Amendment must use a new analysis ID')
        except (ResearchError, KeyError, ValueError) as exc:
            errors.append(f'Invalid amendment predecessor: {exc}')
    return errors


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(['git', '-c', f'safe.directory={root.resolve().as_posix()}', '-C', str(root), *args],
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def committed(root: Path, relative: str) -> bool:
    try:
        saved = git(root, 'show', f'HEAD:{relative}')
        current = within(root, relative).read_bytes()
        return saved.replace(b'\r\n', b'\n') == current.replace(b'\r\n', b'\n')
    except (subprocess.CalledProcessError, ResearchError):
        return False


def execute(root: Path, contract_path: str, run_id: str) -> Path:
    contract_file = within(root, contract_path)
    c = read_json(contract_file)
    errors = contract_errors(root, c, check_inputs=True)
    if errors:
        raise ResearchError('\n'.join(errors))
    if contract_path not in read_json(root/'analysis/research/registry.json')['contracts']:
        raise ResearchError('Execution requires a registered contract')
    if c.get('status') != 'frozen':
        errors.append('Execution requires a frozen contract')
    if re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,95}', run_id) is None:
        errors.append('Invalid run ID')
    for p in [contract_path] + [a['path'] for a in c.get('code', [])]:
        if not committed(root, p):
            errors.append(f'Freeze contract/code in Git before execution: {p}')
    if errors:
        raise ResearchError('\n'.join(errors))
    output = root / 'analysis/research/runs' / run_id
    if output.exists():
        raise ResearchError('Run directory already exists; reruns require a new ID')
    executable = sys.executable if c['runtime'] == 'python' else shutil.which('Rscript')
    if not executable:
        raise ResearchError('Rscript is unavailable; no analysis started')
    output.mkdir(parents=True)
    argv = [executable, str(within(root, c['entrypoint']))] + [arg.replace('{run_dir}', str(output.resolve())) for arg in c['arguments']]
    # Record a replayable repository-relative command, not local user/runtime paths.
    portable_argv = [c['runtime'], c['entrypoint']] + [
        arg.replace('{run_dir}', output.relative_to(root).as_posix()) for arg in c['arguments']]
    record = {'schema_version':1, 'analysis_id':c['analysis_id'], 'owner':c['owner'],
              'contract':contract_path, 'contract_sha256':sha256(contract_file),
              'git_commit':git(root, 'rev-parse', 'HEAD').decode().strip(),
              'started_at':datetime.now(timezone.utc).isoformat(), 'argv':portable_argv,
              'argv_format':'repository_relative',
              'environment':{'python':sys.version, 'platform':platform.platform()},
              'inputs':c['inputs'], 'code':c['code'], 'status':'started', 'outputs':[],
              'scientific_acceptance':'not_assessed', 'verification':'pending'}
    # Receipt exists even if the process is interrupted or produces no expected output.
    receipt = output / 'receipt.json'
    receipt.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
    try:
        with (output/'stdout.log').open('wb') as stdout, (output/'stderr.log').open('wb') as stderr:
            process = subprocess.run(argv, cwd=root, stdout=stdout, stderr=stderr, check=False)
        record['exit_code'] = process.returncode
        record['status'] = 'executed' if process.returncode == 0 else 'execution_failed'
        for rel in c['expected_outputs']:
            p = within(output, rel)
            record['outputs'].append({'path':p.relative_to(root).as_posix(), 'sha256':sha256(p)})
        if sha256(contract_file) != record['contract_sha256'] or contract_errors(root, c, check_inputs=True):
            record['status'] = 'provenance_changed'
    except BaseException as exc:
        record['status'] = 'interrupted' if isinstance(exc, (KeyboardInterrupt, SystemExit)) else 'execution_failed'
        record['error'] = str(exc)
        raise
    finally:
        record['finished_at'] = datetime.now(timezone.utc).isoformat()
        receipt.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
    if record['status'] != 'executed':
        raise ResearchError(f'Run failed: {receipt}')
    return receipt


def receipt_errors(root: Path, receipt_path: str) -> list[str]:
    errors=[]
    try:
        r=read_json(within(root, receipt_path))
        c=read_json(within(root,r['contract']))
        if sha256(within(root,r['contract'])) != r['contract_sha256']:
            errors.append('Recorded contract changed')
        if r['analysis_id'] != c['analysis_id'] or r['owner'] != c['owner']:
            errors.append('Receipt owner/analysis mismatch')
        if r['code'] != c['code'] or r['inputs'] != c['inputs']:
            errors.append('Receipt input/code manifest differs from contract')
        if r['status'] != 'executed' or r.get('exit_code') != 0:
            errors.append('Receipt does not report successful execution')
        run_root = within(root, receipt_path).parent
        expected = {(run_root/p).relative_to(root).as_posix() for p in c['expected_outputs']}
        if {o['path'] for o in r['outputs']} != expected:
            errors.append('Receipt output list differs from contract')
        for item in r['code']+r['outputs']:
            if sha256(within(root,item['path'])) != item['sha256']:
                errors.append(f'Receipt hash mismatch: {item["path"]}')
        # Raw inputs may be unavailable in a clean clone; execution hashes remain recorded.
    except (ResearchError, KeyError, ValueError, TypeError) as exc:
        errors.append(f'Invalid receipt: {exc}')
    return errors


def check_registry(root: Path, *, base: str | None = None) -> list[str]:
    errors=[]
    index=read_json(root/'analysis/research/registry.json')
    cards=(root/'RESEARCH_QUESTIONS.md').read_text(encoding='utf-8-sig')
    ids=re.findall(r'^### (A\d+)\.',cards,re.M)
    declared=[q['id'] for q in index['questions']]
    if len(ids)!=len(set(ids)) or len(declared)!=len(set(declared)) or set(ids)!=set(declared):
        errors.append('Canonical question IDs and registry differ or contain duplicates')
    for q in index['questions']:
        try:
            if q['card'] != f'RESEARCH_QUESTIONS.md#{q["id"].lower()}':
                errors.append(f'{q["id"]}: invalid canonical card')
            dossier=within(root,q['dossier']).read_text(encoding='utf-8-sig')
            for section in DOSSIER_SECTIONS:
                match=re.search(rf'^## {re.escape(section)}\n(.+?)(?=\n## |\Z)',dossier,re.M|re.S)
                if not match or len(match.group(1).strip())<30:
                    errors.append(f'{q["id"]}: missing/substantively empty dossier section {section}')
            for evidence in q['evidence']:
                within(root,evidence)
            if not q['evidence']:
                errors.append(f'{q["id"]}: no evidence locator')
        except ResearchError as exc:
            errors.append(str(exc))
    for candidate in index['article_candidates']:
        try:
            within(root,candidate['plan'])
        except ResearchError as exc:
            errors.append(str(exc))
    contracts={}
    bound_code=set()
    for path in index['contracts']:
        try:
            c=read_json(within(root,path))
            errors.extend(f'{path}: {e}' for e in contract_errors(root,c))
            if c['analysis_id'] in contracts:
                errors.append(f'Duplicate analysis ID: {c["analysis_id"]}')
            contracts[c['analysis_id']]=c
            bound_code.update(a['path'] for a in c['code'])
        except (ResearchError, KeyError, ValueError) as exc:
            errors.append(f'{path}: {exc}')
    bound_outputs=set()
    for path in index['receipts']:
        errors.extend(f'{path}: {e}' for e in receipt_errors(root,path))
        try:
            receipt=read_json(within(root,path))
            if receipt['analysis_id'] not in contracts:
                errors.append(f'{path}: receipt has no registered contract')
            bound_outputs.update(o['path'] for o in receipt['outputs'])
        except (ResearchError, KeyError, ValueError):
            pass
    legacy=read_json(root/'analysis/research/legacy_artifacts.json')
    for item in legacy['artifacts']:
        try:
            if content_hash(within(root,item['path'])) != item['sha256']:
                errors.append(f'Historical artifact changed: {item["path"]}; use a versioned correction')
        except ResearchError as exc:
            errors.append(str(exc))
    if base:
        paths=git(root,'diff','--name-only','--diff-filter=ACDMRTUXB',base,'--').decode().splitlines()
        paths+=git(root,'ls-files','--others','--exclude-standard').decode().splitlines()
        approved=set(index['infrastructure_paths'])|set(index['contracts'])|set(index['receipts'])|bound_code|bound_outputs
        for path in set(paths):
            if path.startswith(SCIENTIFIC_ROOTS) and Path(path).suffix.lower() in ASSET_SUFFIXES and path not in approved:
                errors.append(f'Unregistered scientific asset change: {path}')
        # A baseline cannot be rewritten to conceal changed frozen evidence.
        try:
            prior=json.loads(git(root,'show',f'{base}:analysis/research/legacy_artifacts.json'))
        except subprocess.CalledProcessError:
            prior=None  # Initial migration; file is owner-reviewed infrastructure.
        if prior is not None and prior != legacy:
            errors.append('Historical baseline is immutable; changes require a separately reviewed migration')
        try:
            previous= json.loads(git(root,'show',f'{base}:analysis/research/registry.json'))
        except subprocess.CalledProcessError:
            previous=None
        if previous is not None:
            for kind in ('contracts','receipts'):
                for path in previous[kind]:
                    if path not in index[kind]:
                        errors.append(f'Registered {kind} cannot be removed: {path}')
                    try:
                        saved=git(root,'show',f'{base}:{path}')
                        frozen=kind=='receipts' or json.loads(saved).get('status')=='frozen'
                        if frozen and saved.replace(b'\r\n',b'\n') != within(root,path).read_bytes().replace(b'\r\n',b'\n'):
                            errors.append(f'Frozen {kind} changed: {path}; create a versioned amendment')
                    except (subprocess.CalledProcessError, ResearchError, ValueError) as exc:
                        errors.append(f'Cannot verify prior {kind}: {path}: {exc}')
    return errors
