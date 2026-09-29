"""Verify source/design agreement and navigation; never grade biological claims."""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    config = json.loads((ROOT / "config/pipeline.json").read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location("nabhan_intake", ROOT / "scripts/00_intake.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tsv, summary = module.derive((ROOT / "sources/GSE208770_family.soft.gz").read_bytes())
    require(tsv == (ROOT / "metadata/samples.tsv").read_text(encoding="utf-8"), "Sample manifest differs from source")
    require(summary == json.loads((ROOT / "metadata/intake_summary.json").read_text(encoding="utf-8")), "Summary differs from source")
    manifest = json.loads((ROOT / "metadata/source_manifest.json").read_text(encoding="utf-8"))
    source = next(s for s in manifest["sources"] if s["id"] == "D1")
    require(summary["source_sha256"] == source["sha256"], "SOFT hash mismatch")
    rows = list(csv.DictReader(tsv.splitlines(), delimiter="\t"))
    require(len(rows) == len({r["accession"] for r in rows}) == 18, "Sample IDs not unique/complete")
    require({r["accession"] for r in rows} == {f"GSM{i}" for i in range(6369132, 6369150)}, "GSM range mismatch")
    require(summary["condition_counts"] == {c: 3 for c in config["primary_deposit"]["conditions"]}, "Condition mismatch")
    require(all(r["biological_unit_id"] == r["pairing_id"] == "unresolved" for r in rows), "Unverified identity added")
    require(config["namespace"] == "Nb2", "Wrong paper namespace")
    require(config["biological_analysis_executed"] and config["run_contract_frozen"], "Execution state missing")
    for run in ["bulk_v1", "atlas_v1"]:
        require((ROOT / "trials" / run / "contract.json").is_file(), "Missing frozen contract")
        require((ROOT / "trials" / run / "run_complete.json").is_file(), "Missing completed measurement record")
    require(not config["primary_deposit"]["preparation_map_verified"], "Unverified preparation identity promoted")
    for contrast in config["primary_contrasts"] + config["secondary_contrasts"]:
        require(len(contrast) == 2 and contrast[0] != contrast[1] and set(contrast) <= set(summary["condition_counts"]), "Invalid contrast")
    stages = {s["id"]: s for s in config["stages"]}
    require(len(stages) == len(config["stages"]), "Duplicate stage ID")
    visited, active = set(), set()

    def visit(stage_id: str) -> None:
        require(stage_id in stages, f"Missing stage {stage_id}")
        require(stage_id not in active, f"Dependency cycle at {stage_id}")
        if stage_id in visited:
            return
        active.add(stage_id)
        for parent in stages[stage_id]["depends_on"]:
            visit(parent)
        active.remove(stage_id)
        visited.add(stage_id)

    for stage_id in stages:
        visit(stage_id)
    ledger = list(csv.DictReader((ROOT / "metadata/stage_status.tsv").read_text(encoding="utf-8").splitlines(), delimiter="\t"))
    require({r["stage_id"]: r["status"] for r in ledger} == {k: v["status"] for k, v in stages.items()}, "Stage ledger drift")
    register = (ROOT / "HYPOTHESIS_REGISTER.md").read_text(encoding="utf-8")
    candidates = config["owner_nabhan_candidates"]
    require([c["id"] for c in candidates] == [f"Nb2-N{i}" for i in range(1, 9)], "Owner candidate order changed")
    for candidate in candidates:
        require(f'### {candidate["id"]} ' in register and set(candidate["stages"]) <= set(stages), "Candidate card/stage missing")
    for i in range(1, 11):
        require(f"| Nb2-P{i} |" in register, f"Missing source proposition P{i}")
    require(config["source_panels"]["Hippo_associated"] == ["Cyr61", "Ctgf", "Amotl2", "Crim2"], "Source panel mismatch")
    roadmap = json.loads((REPO / "Research Article/ROADMAP.json").read_text(encoding="utf-8"))
    paper = next(p for p in roadmap["papers"] if p["key"] == "nabhan_2023")
    require(paper["folder"] == ROOT.name and paper["order"] == 6 and paper["gate"] == "2N", "Roadmap identity mismatch")
    require(ROOT.name in (REPO / "Research Article/README.md").read_text(encoding="utf-8"), "Article index not linked")
    require('id="nabhan-branch"' in (REPO / "RESEARCH_QUESTIONS.md").read_text(encoding="utf-8"), "Missing Nabhan register entry")
    print("PASS: source hash, 18 samples, 6 conditions, contrasts, 11-stage DAG, 10 claims, 8 ordered candidates and navigation")


if __name__ == "__main__":
    main()
