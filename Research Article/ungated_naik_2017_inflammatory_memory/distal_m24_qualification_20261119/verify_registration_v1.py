"""Verify the exposed Step 2 metadata in a fresh governed directory."""
import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
HISTORICAL = ROOT / "raw_data/naik_distal_m24_sources_20261119/historical_b8156c4_git"
SOURCE_COMMIT = "b8156c4f466982c560d43133b8483060492f44d0"
DATA_FILES = ("regions.tsv", "samples.tsv", "region_qualification.json", "source_receipts.json", "track_structure.json")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def historical_bytes(name):
    """Require the declared historical input and its committed Git blob to agree exactly."""
    path = (HERE / name).relative_to(ROOT).as_posix()
    blob = subprocess.check_output(["git", "cat-file", "blob", f"{SOURCE_COMMIT}:{path}"], cwd=ROOT)
    if (HISTORICAL / name).read_bytes() != blob:
        raise ValueError(f"Historical bytes differ from the acquisition snapshot: {name}")
    return blob


def compare_output(folder, name):
    path = folder / name
    original = historical_bytes(name)
    actual = path.read_bytes()
    if actual != original:
        # The two json.dump/text writers use host text-mode newlines.
        if name not in ("region_qualification.json", "source_receipts.json") or actual.replace(b"\r\n", b"\n") != original:
            raise ValueError(f"Metadata reproduction differs from the original Git object: {name}")
        path.write_bytes(actual.replace(b"\r\n", b"\n"))
    assert path.read_bytes() == original
    return {"source_git_blob_sha256": digest(original), "output_sha256": digest(path.read_bytes()), "identical": True}


def reader_stage(output):
    import qualify_track_structure
    # The original script reads an exact registered copy of the selection and all S2 regions here.
    # Its BigWig queries are confined to 12 prespecified candidates with a full-cohort overlap guard.
    qualify_track_structure.HERE = output
    qualify_track_structure.main()


def run_reader(output):
    if os.name == "nt":
        wsl = ["wsl.exe", "-d", "Ubuntu", "--exec"]
        root_wsl = subprocess.check_output(wsl + ["wslpath", "-a", str(ROOT)], text=True).strip()
        script = root_wsl + "/" + Path(__file__).relative_to(ROOT).as_posix()
        dest = root_wsl + "/" + output.relative_to(ROOT).as_posix()
        subprocess.run(wsl + [root_wsl + "/raw_data/naik2017_s3_runtime_v1/venv/bin/python",
                              "-B", script, "--reader-stage", "--output", dest], check=True)
    else:
        interpreter = ROOT / "raw_data/naik2017_s3_runtime_v1/venv/bin/python"
        subprocess.run([str(interpreter), "-B", str(Path(__file__).resolve()), "--reader-stage",
                        "--output", str(output)], check=True)


def verify(output):
    import numpy
    import openpyxl
    import qualify_regions
    import qualify_source_manifest

    if any(p.name not in {"stdout.log", "stderr.log", "receipt.json"} for p in output.iterdir()):
        raise ValueError("Run directory already contains derived files")
    # The inputs and the historical checker code keep their original ROOT, RAW and source paths.
    # Redirect only the three original checkers' output directory to the new run.
    (output / "selection_v1.json").write_bytes(historical_bytes("selection_v1.json"))
    qualify_regions.HERE = output
    qualify_regions.main()
    qualify_source_manifest.HERE = output
    qualify_source_manifest.main()
    checks = {name: compare_output(output, name) for name in ("selection_v1.json", *DATA_FILES[:-1])}

    with (output / "regions.tsv").open(encoding="utf8", newline="") as handle:
        regions = list(csv.DictReader(handle, delimiter="\t"))
    assert len(regions) == 2801 and len({(r["chromosome"], r["start0"], r["end0"]) for r in regions}) == 2801
    queries = [(c, s, s + 10_000) for c in ("chr1", "chr2", "chrX") for s in (0, 5_000_000, 25_000_000, 50_000_000)]
    for c, s, e in queries:
        if any(r["chromosome"] == c and int(r["start0"]) < e and s < int(r["end0"]) for r in regions):
            raise ValueError("Frozen structural probe intersects an S2 region")
    run_reader(output)
    checks["track_structure.json"] = compare_output(output, "track_structure.json")
    structural = json.loads((output / "track_structure.json").read_text())
    assert len(structural["tracks"]) == 4
    for track in structural["tracks"].values():
        assert [(r["chrom"], r["start0"], r["end0"]) for r in track["probes"]] == queries
    original_report = historical_bytes("SOURCE_QUALIFICATION.md")
    (output / "historical_report.txt").write_bytes(original_report)
    counts = {k: sum(r["source_class"] == k and r["primary"] == "1" for r in regions) for k in ("Memory", "Resolved")}
    report = dict(historical_commit=SOURCE_COMMIT, historical_artifact_checks=checks,
                  historical_report_sha256=digest(original_report), source_region_count=len(regions),
                  primary_count=counts, off_region_probe_queries=4*len(queries), research_interval_queries=0,
                  technical_verification="Exposed metadata reproduction, exact canonical Git bytes",
                  host_python=platform.python_version(), host_numpy=numpy.__version__, host_openpyxl=openpyxl.__version__,
                  structural_reader=structural["reader"])
    (output / "verification.json").write_bytes((json.dumps(report, indent=2, allow_nan=False) + "\n").encode("utf8"))
    print(json.dumps({"verified_files": len(checks), "primary": counts, "research_interval_queries": 0}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--reader-stage", action="store_true")
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    out = args.output.resolve()
    if out.parent != (ROOT / "analysis/research/runs").resolve():
        raise ValueError("Output must be an immediate child of the governed runs directory")
    if args.reader_stage:
        reader_stage(out)
    else:
        verify(out)
