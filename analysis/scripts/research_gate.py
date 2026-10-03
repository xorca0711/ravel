#!/usr/bin/env python
"""Research governance: check, preflight, run and verify (no shell execution)."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from lib.research_governance import (ResearchError, check_registry, contract_errors,
    execute, read_json, receipt_errors, within)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    sub=p.add_subparsers(dest='command',required=True)
    check=sub.add_parser('check'); check.add_argument('--base')
    pre=sub.add_parser('preflight'); pre.add_argument('contract'); pre.add_argument('--inputs',action='store_true')
    run=sub.add_parser('run'); run.add_argument('contract'); run.add_argument('--run-id',required=True)
    verify=sub.add_parser('verify'); verify.add_argument('receipt')
    args=p.parse_args()
    try:
        if args.command=='check': errors=check_registry(args.root,base=args.base)
        elif args.command=='preflight': errors=contract_errors(args.root,read_json(within(args.root,args.contract)),check_inputs=args.inputs)
        elif args.command=='verify': errors=receipt_errors(args.root,args.receipt)
        else:
            receipt=execute(args.root,args.contract,args.run_id)
            print(json.dumps({'receipt':receipt.relative_to(args.root).as_posix(),'status':'executed','scientific_acceptance':'not_assessed'})); return 0
    except (ResearchError,OSError,ValueError,KeyError,subprocess.CalledProcessError) as exc:
        errors=[str(exc)]
    print(json.dumps({'ok':not errors,'errors':errors},indent=2))
    return 1 if errors else 0


if __name__=='__main__':
    raise SystemExit(main())
