"""Read-only repository/source-cache census; no biological analysis or downloads.

Use a new output directory for a new snapshot. Only output files are written.
Accession mentions and receipt input filenames do not establish analytical use.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import os
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone

ACCESSION = re.compile(r"(?<![A-Za-z0-9])(?:GSE\d{4,}|E-MTAB-\d+|PRJ(?:NA|EB|DB)\d+)(?![A-Za-z0-9])")
TEXT_SUFFIXES = {".md", ".json", ".py", ".r", ".csv", ".tsv"}
MAX_TEXT_BYTES = 2_000_000


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args]).decode("utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def scan(repo, storage_repo, output):
    output.mkdir(parents=True, exist_ok=True)
    names = ["accession_references.csv", "local_files.csv", "local_directories.csv", "snapshot.json"]
    if any((output / name).exists() for name in names):
        raise SystemExit("Snapshot exists; choose a new directory/version.")
    started = datetime.now(timezone.utc).isoformat()
    tracked = [p for p in git(repo, "ls-files", "-z").split("\0") if p]
    refs = collections.defaultdict(set)
    legacy = collections.defaultdict(set)
    excluded = collections.Counter()
    scanned = 0
    for relative in tracked:
        path = repo / relative
        if path.suffix.lower() not in TEXT_SUFFIXES:
            excluded["non_text_suffix"] += 1
            continue
        if ("/history/" in relative or "legacy_artifacts.json" in relative
                or "2026-11-07-public-data-inventory/" in relative):
            excluded["history_baseline_or_this_audit"] += 1
            continue
        if path.stat().st_size > MAX_TEXT_BYTES:
            excluded["over_2MB"] += 1
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        scanned += 1
        for accession in set(ACCESSION.findall(text)):
            refs[accession].add(relative)
            if path.name in {"run_record.json", "provenance.json"}:
                legacy[accession].add(relative)
    registry = read_json(repo / "analysis/research/registry.json")
    receipt_refs = collections.defaultdict(set)
    analyses = collections.defaultdict(set)
    for relative in registry["receipts"]:
        receipt = read_json(repo / relative)
        for source in receipt.get("inputs", []):
            for accession in set(ACCESSION.findall(source.get("path", ""))):
                receipt_refs[accession].add(relative)
                analyses[accession].add(receipt["analysis_id"])
                refs[accession].add(relative)
    accession_rows = []
    for accession, paths in sorted(refs.items()):
        rank = lambda p: (not p.endswith("RESULTS.md"), not p.endswith("DATASETS.md"),
                          not p.endswith("README.md"), len(p), p)
        accession_rows.append({
            "accession": accession,
            "evidence_kind": "registered_input_path" if receipt_refs[accession] else
                             "legacy_record_reference" if legacy[accession] else "reference_only",
            "reference_file_count": len(paths),
            "example_reference": min(paths, key=rank),
            "registered_analysis_ids": ";".join(sorted(analyses[accession])),
            "registered_receipts": ";".join(sorted(receipt_refs[accession])),
            "legacy_records": ";".join(sorted(legacy[accession])),
            "all_references": ";".join(sorted(paths)),
        })
    write_csv(output / names[0], list(accession_rows[0]), accession_rows)

    worktrees = []
    roots = []
    errors = []
    seen_roots = set()
    for block in git(storage_repo, "worktree", "list", "--porcelain").strip().split("\n\n"):
        info = dict(line.split(" ", 1) for line in block.splitlines() if " " in line)
        worktree = Path(info["worktree"])
        label = "project-root" if worktree.resolve() == storage_repo.resolve() else worktree.parent.name
        if worktree.name != "ravel":
            label = worktree.name
        record = {"storage_id": label, "path": worktree.as_posix(), "head": info["HEAD"],
                  "branch": info.get("branch", "detached"), "cache_roots": []}
        worktrees.append(record)
        candidates = [worktree / "raw_data"]
        # Conventional ignored source/reference caches; tmp, processed objects,
        # runtimes and arbitrary external paths are deliberately outside scope.
        for pattern in ["RQ_Specified/*/cache", "RQ_Specified/*/reference",
                        "Research Article/*/cache", "Research Article/*/reference",
                        "analysis/corrections/*/cache"]:
            candidates.extend(worktree.glob(pattern))
        for source in sorted(set(candidates)):
            if not source.is_dir():
                continue
            real = os.path.normcase(str(source.resolve()))
            relative = source.relative_to(worktree).as_posix()
            record["cache_roots"].append(relative)
            if real in seen_roots:
                continue
            seen_roots.add(real)
            roots.append((label, relative, source))
    local_rows = []
    groups = collections.defaultdict(lambda: {"files": 0, "bytes": 0, "accessions": set()})
    for label, cache_relative, source in roots:
        def walk_error(error):
            errors.append({"storage_id": label, "path": str(error.filename), "error": str(error)})
        for directory, dirs, files in os.walk(source, followlinks=False, onerror=walk_error):
            dirs.sort()
            for name in list(dirs):
                path = Path(directory) / name
                if path.is_symlink() or path.is_junction():
                    dirs.remove(name)
                    errors.append({"storage_id": label, "path": str(path), "error": "nested link not traversed"})
            for name in sorted(files):
                path = Path(directory) / name
                relative = path.relative_to(source)
                try:
                    if path.is_symlink():
                        raise OSError("file link not followed")
                    size = path.stat().st_size
                except OSError as error:
                    walk_error(error)
                    continue
                source_path = f"{cache_relative}/{relative.as_posix()}"
                accessions = set(ACCESSION.findall(source_path))
                group = f"{cache_relative}/{relative.parts[0]}" if len(relative.parts) > 1 else cache_relative
                local_rows.append({"storage_id": label, "path": source_path,
                                   "size_bytes": size, "path_accessions": ";".join(sorted(accessions))})
                summary = groups[label, group]
                summary["files"] += 1
                summary["bytes"] += size
                summary["accessions"].update(accessions)
    local_rows.sort(key=lambda r: (r["storage_id"], r["path"]))
    write_csv(output / names[1], ["storage_id", "path", "size_bytes", "path_accessions"], local_rows)
    directory_rows = [{"storage_id": label, "directory": group, "files": v["files"],
                       "size_bytes": v["bytes"], "path_accessions": ";".join(sorted(v["accessions"]))}
                      for (label, group), v in sorted(groups.items())]
    write_csv(output / names[2], ["storage_id", "directory", "files", "size_bytes", "path_accessions"], directory_rows)
    assert sum(r["size_bytes"] for r in local_rows) == sum(r["size_bytes"] for r in directory_rows)
    assert len(local_rows) == sum(r["files"] for r in directory_rows)
    assert len({(r["storage_id"], r["path"]) for r in local_rows}) == len(local_rows)
    summary = {"started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
               "repository_revision": git(repo, "rev-parse", "HEAD").strip(),
               "integration_base": git(repo, "rev-parse", "origin/main").strip(),
               "tracked_paths": len(tracked), "scanned_text_files": scanned,
               "excluded_files": dict(excluded), "text_limit_bytes": MAX_TEXT_BYTES,
               "accession_count": len(refs), "accession_evidence_kinds": dict(collections.Counter(
                   r["evidence_kind"] for r in accession_rows)),
               "registered_receipts_inspected": len(registry["receipts"]),
               "worktrees": worktrees, "scanned_cache_roots": len(roots),
               "local_file_count": len(local_rows), "local_size_bytes": sum(r["size_bytes"] for r in local_rows),
               "local_path_accession_count": len(set().union(*(v["accessions"] for v in groups.values()))),
               "scan_errors_or_exclusions": errors,
               "limits": ["References are not confirmed use; inspect owning result/receipt.",
                          "Local presence uses paths and byte sizes, not fresh content hashes or integrity checks.",
                          "Counts are apparent file bytes, not unique datasets, physical disk use or independent samples.",
                          "Copies in different worktrees count separately; resolved duplicate roots do not.",
                          "tmp, processed/model objects, runtimes, external caches and cloud storage are outside scope.",
                          "No remote source availability refresh or biological rerun."]}
    (output / names[3]).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ["scanned_text_files", "accession_count", "accession_evidence_kinds",
                     "scanned_cache_roots", "local_file_count", "local_size_bytes"]}))
    print("scan_errors_or_exclusions:", len(errors))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--storage-repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scan(args.repo.resolve(), args.storage_repo.resolve(), args.output.resolve())
