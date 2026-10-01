"""Check the Nabhan 2026 scaffold and source availability; never fit or download."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[1]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path, mode: str) -> str:
    if mode == "lf":
        return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def inventory() -> dict:
    pipeline = read_json(PACKAGE / "config/pipeline.json")
    manifest = read_json(PACKAGE / "config/source_manifest.json")
    issues = []
    nodes = pipeline["stages"] + pipeline["extensions"]
    ids = [node["id"] for node in nodes]
    if len(ids) != len(set(ids)):
        issues.append("Duplicate pipeline IDs")
    graph = {node["id"]: node["depends_on"] for node in nodes}
    seen, active = set(), set()

    def visit(key: str) -> None:
        if key in active:
            issues.append(f"Dependency cycle at {key}")
            return
        if key in seen:
            return
        if key not in graph:
            issues.append(f"Unknown dependency {key}")
            return
        active.add(key)
        for parent in graph[key]:
            visit(parent)
        active.remove(key)
        seen.add(key)

    for key in graph:
        visit(key)
    if sorted(node["owner_item"] for node in pipeline["extensions"]) != list(range(1, 9)):
        issues.append("Owner questions 1-8 are not mapped exactly once")
    files = []
    for entry in manifest["files"]:
        path = (REPO / entry["path"]).resolve()
        if not path.is_relative_to(REPO.resolve()):
            issues.append(f"Source path leaves repository: {entry['id']}")
            continue
        record = {"id": entry["id"], "path": entry["path"], "present": path.is_file()}
        if path.is_file():
            record["sha256"] = digest(path, entry["hash_mode"])
            record["matches_recorded_hash"] = record["sha256"] == entry["sha256"]
            if not record["matches_recorded_hash"]:
                issues.append(f"Changed input: {entry['id']}")
        elif entry["required_for_scaffold"]:
            issues.append(f"Missing scaffold source: {entry['id']}")
        files.append(record)
    crosswalk = REPO / manifest["crosswalk"]
    summary = {}
    if crosswalk.is_file():
        with crosswalk.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        for field in ("library", "gsm"):
            if any(not row[field] for row in rows) or len({row[field] for row in rows}) != len(rows):
                issues.append(f"Crosswalk {field} is missing or duplicated")
        summary = {
            "libraries": len(rows),
            "targets": len({row["target"] for row in rows}),
            "plates": len({row["plate"] for row in rows}),
            "rna_repeat_groups": len({row["deposited_repeat_label"] for row in rows}),
            "paired_imaging_wells": sum(all(row[k].strip().lower() not in ("", "nan", "unknown")
                                            for k in ("day07_area", "day14_area")) for row in rows),
            "resolved_animal_ids": len({row["animal_id"] for row in rows
                                         if row["animal_id"].strip().lower() not in ("", "unknown", "nan")}),
        }
        for field, expected in manifest["expected_crosswalk"].items():
            if summary.get(field) != expected:
                issues.append(f"Crosswalk {field}: expected {expected}, observed {summary.get(field)}")
    missing = [record["id"] for record in files if not record["present"]]
    return {
        "schema": "nabhan-2026-intake/v1",
        "scope": "Structure, provenance and existing metadata only; not scientific reproduction",
        "structural_status": "PASS" if not issues else "FAIL",
        "issues": issues, "crosswalk": summary, "files": files,
        "optional_inputs_absent": missing,
        "config_sha256": digest(PACKAGE / "config/pipeline.json", "lf"),
        "script_sha256": digest(Path(__file__), "lf"),
        "source_manifest_sha256": digest(PACKAGE / "config/source_manifest.json", "lf"),
        "biological_models_run": 0,
        "scientific_readiness": "HOLD: full counts, source-model settings and stage contracts; spatial identity/treatment reconciliation",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Optional new JSON record; existing files are refused")
    args = parser.parse_args()
    if args.out and args.out.exists():
        parser.error(f"Refusing to overwrite {args.out}")
    report = inventory()
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
        print(json.dumps({key: report[key] for key in
                          ("structural_status", "issues", "crosswalk", "optional_inputs_absent", "biological_models_run")}))
    else:
        print(rendered, end="")
    return 0 if report["structural_status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
