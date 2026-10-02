"""Read-only, standard-library verification of the deposited Nb4 run archive.

This checks archive integrity and links, not raw-data scientific recomputation.
"""
from common import PACKAGE, read_json, sha256
import verify_package

REQUIRED = {
    "runs/" + name for name in (
        "intake_v1", "metadata_v1", "reproduction_v1", "source_concordance_v1",
        "followup_v1", "external_pilot_v1", "extended_visual_v1", "validation_v1",
    )
} | {
    "figures/" + name for name in (
        "execution_v1", "publication_v1", "extended_v2", "refinement_v1",
        "gallery_v1", "gallery_v2",
    )
}


def local_file(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"Missing or nonlocal archive file: {root.name}/{name}")
    return path


def verify_record(record_path):
    record = read_json(record_path)
    root = record_path.parent
    for field in ("outputs", "code_sha256", "config_sha256"):
        if not isinstance(record.get(field), dict) or not record[field]:
            raise ValueError(f"Missing {field}: {record_path}")
    for name, expected in record["outputs"].items():
        if sha256(local_file(root, name)) != expected:
            raise ValueError(f"Changed recorded output: {root.name}/{name}")
    for name, expected in record["code_sha256"].items():
        # Historical snapshots remain valid when a current script is refined.
        archived = local_file(root / "code_snapshot", name + ".txt")
        if sha256(archived) != expected:
            raise ValueError(f"Changed archived code: {root.name}/{name}")
    for name, expected in record["config_sha256"].items():
        if sha256(local_file(PACKAGE / "config", name)) != expected:
            raise ValueError(f"Changed run configuration: {root.name}/{name}")
    return len(record["outputs"])


def main():
    records = sorted(PACKAGE.rglob("run_record.json"))
    present = {p.parent.relative_to(PACKAGE).as_posix() for p in records}
    if REQUIRED - present:
        raise ValueError(f"Missing run records: {sorted(REQUIRED - present)}")
    outputs = sum(verify_record(path) for path in records)
    if read_json(PACKAGE / "figures/gallery_v2/run_record.json")["pages"] != 12:
        raise ValueError("Final atlas must contain twelve recorded pages")
    verify_package.main()
    print(f"Nb4 archive passed: {len(records)} run records, {outputs} output hashes, "
          "archived code, configuration hashes and local documentation links.")


if __name__ == "__main__":
    main()
