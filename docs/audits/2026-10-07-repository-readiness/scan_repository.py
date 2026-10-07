"""Read-only inventory, text-integrity and contract/input availability audit.

Standard library only. This complements, rather than replaces, research_gate,
validate_repository, claim_contract and the scientific review ledger.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess


def scan(root):
    files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    files = [p for p in files if p]
    reg = json.loads((root/'analysis/research/registry.json').read_text(encoding='utf-8'))
    errors, json_count, text_count = [], 0, 0
    ext = Counter(Path(p).suffix.lower() or '(none)' for p in files)
    for rel in files:
        path = root/rel
        if not path.is_file():
            errors.append({'path': rel, 'issue': 'tracked file missing'})
            continue
        if path.suffix.lower() in {'.md', '.py', '.r', '.json', '.yml', '.yaml', '.toml'}:
            text = path.read_text(encoding='utf-8-sig', errors='replace')
            text_count += 1
            if re.search(r'^(?:<<<<<<< |>>>>>>> )', text, re.M):
                errors.append({'path': rel, 'issue': 'merge conflict marker'})
            if path.suffix.lower() == '.json':
                json_count += 1
                try:
                    json.loads(text)
                except ValueError as e:
                    errors.append({'path': rel, 'issue': str(e)})
    inputs = {}
    for rel in reg['contracts']:
        contract = json.loads((root/rel).read_text(encoding='utf-8'))
        for item in contract['inputs']:
            inputs.setdefault(item['path'], set()).add(rel)
    availability = [{'path': p, 'present_in_audit_checkout': (root/p).is_file(),
                     'contracts': sorted(cs)} for p, cs in sorted(inputs.items())]
    receipts = [json.loads((root/p).read_text(encoding='utf-8')) for p in reg['receipts']]
    executed = {r['contract'] for r in receipts if r.get('status') == 'executed'}
    return {'scope': 'All tracked paths; all MD/Python/R/JSON/YAML/TOML text; all registered contract input paths. No raw-data completeness or scientific-truth certification.',
        'tracked_files': len(files), 'extensions': dict(sorted(ext.items())),
        'text_files_scanned': text_count, 'json_files_parsed': json_count,
        'questions': len(reg['questions']), 'article_candidates': len(reg['article_candidates']),
        'contracts': len(reg['contracts']), 'receipts': len(reg['receipts']),
        'contracts_without_successful_receipt': [p for p in reg['contracts'] if p not in executed],
        'unique_input_paths': len(inputs), 'inputs_present': sum(x['present_in_audit_checkout'] for x in availability),
        'input_availability': availability, 'errors': errors}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[3]
    result = scan(root)
    Path(args.output).write_bytes((json.dumps(result, indent=2, ensure_ascii=False)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('input_availability', 'extensions')}, indent=2))
    raise SystemExit(bool(result['errors']))
