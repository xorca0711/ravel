"""Verify unchanged declarative dependencies against the pre-outcome freeze."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
root = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
contract_path = "RQ_Specified/A12_recipient_context/config/erbb_sorted_contract_v1.json"
receipt_path = "analysis/research/runs/A12_erbb_sorted_reference_v1_20261103/receipt.json"
original = json.loads((root / contract_path).read_text())
receipt = json.loads((root / receipt_path).read_text())
assert receipt["status"] == "executed"
inputs = {i["path"]: i["sha256"] for i in original["inputs"]}
records = []
for name in ["erbb_sorted_spec_v1.json", "erbb_sorted_sources_v1.json"]:
    path = "RQ_Specified/A12_recipient_context/config/" + name
    data = (root / path).read_bytes()
    frozen = subprocess.check_output(["git", "show", receipt["git_commit"] + ":" + path], cwd=root)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == inputs[path] and frozen == data
    json.loads(data)
    records.append(dict(path=path, sha256=digest, prior_contract_input_hash=inputs[path],
                        present_at_numerical_freeze=True, bytes_unchanged=True))
result = dict(status="passed", numerical_freeze=receipt["git_commit"],
              original_contract=contract_path, original_receipt=receipt_path,
              correction="Register existing declarative dependencies; no numerical or design change", assets=records)
(out / "configuration_binding.json").write_text(json.dumps(result, indent=2) + "\n")
print("Both declarative dependencies match their original pre-outcome commit and input hashes.")
