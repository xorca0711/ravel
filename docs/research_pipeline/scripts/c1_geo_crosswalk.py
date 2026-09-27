"""C1, GEO half: persist the sample, donor, condition and assay crosswalk from series metadata.

This is the half of C1 that does not need the count object. It reads the series metadata an
earlier task already saved and hashed, and writes one row per GEO record with the fields a
contrast would have to join on.

It resolves nothing the metadata does not state. In particular it keeps the distinction the
handoff asks for: the control libraries name their medium in the treatment field, while the
infected libraries do not, so pairing an infected library to a medium-matched control rests on
the source protocol rather than on the record. The crosswalk reports that rather than choosing.

The object half of C1, verifying these joins against the saved count object, is separate. A
crosswalk built from metadata is a hypothesis about the object, not a check of it.

Standard library only. Refuses to overwrite.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
METADATA = REPO / "docs/roadmap_runs/2026-09-27-followthrough/metadata/GSE198864.json"
OUTPUTS = ["geo_sample_crosswalk.tsv", "geo_crosswalk_run.json"]

# The treatment field carries either a pathogen or, for the control libraries, the medium.
MEDIA = {"BSA", "FCS"}
PATHOGEN_CANON = {
    "iav": "IAV", "h3n2": "IAV", "influenza": "IAV",
    "sars-cov-2": "SARS-CoV-2", "scov2": "SARS-CoV-2",
    "sars-cov-1": "SARS-CoV-1", "scov1": "SARS-CoV-1",
    "mers-cov": "MERS-CoV", "mers": "MERS-CoV",
    "nl63-cov": "NL63-CoV", "nl63": "NL63-CoV",
    "229e-cov": "229E-CoV", "229e": "229E-CoV",
}
# The source protocol, as recorded in the handoff: influenza in BSA, coronaviruses in FCS.
PROTOCOL_MEDIUM = {"IAV": "BSA", "SARS-CoV-2": "FCS", "SARS-CoV-1": "FCS",
                   "MERS-CoV": "FCS", "NL63-CoV": "FCS", "229E-CoV": "FCS"}


def sha256(path: Path) -> str:
    d = hashlib.sha256()
    with path.open("rb") as h:
        for b in iter(lambda: h.read(1 << 24), b""):
            d.update(b)
    return d.hexdigest()


def flat(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ; ".join(str(v) for v in value)
    return str(value)


def characteristic(rec: dict, key: str) -> str:
    raw = rec.get("!Sample_characteristics_ch1", "")
    items = [raw] if isinstance(raw, str) else list(raw)
    for item in items:
        name, sep, val = item.partition(":")
        if sep and name.strip().lower() == key:
            return val.strip()
    return ""


def donor_of(title: str) -> str:
    """Titles are lung_<donor>_<arm> for explants and AM<donor>_<arm> for macrophages."""
    m = re.match(r"^lung_([A-Za-z0-9]+)_", title)
    if m:
        return m.group(1)
    m = re.match(r"^AM([A-Za-z0-9]+?)_", title)
    if m:
        return m.group(1)
    m = re.match(r"^([A-Za-z0-9]+?)_", title)
    return m.group(1) if m else "unclear"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    out = ap.parse_args().out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    existing = [n for n in OUTPUTS if (out / n).exists()]
    if existing:
        raise SystemExit("Refusing to overwrite: %s" % existing)

    samples = json.loads(METADATA.read_text(encoding="utf-8"))["samples"]
    rows = []
    for rec in samples:
        title = flat(rec.get("!Sample_title")).strip("[]'\" ")
        tissue = characteristic(rec, "tissue")
        treatment = characteristic(rec, "treatment")
        condition = characteristic(rec, "condition")
        supp = " ".join(flat(v) for k, v in rec.items() if "supplementary" in k.lower())
        low = treatment.strip().lower()

        if treatment.strip().upper() in MEDIA:
            arm, medium, medium_source = "control", treatment.strip().upper(), "stated in the treatment field"
        elif low in PATHOGEN_CANON:
            arm = PATHOGEN_CANON[low]
            medium = PROTOCOL_MEDIUM.get(arm, "not named")
            medium_source = "inferred from the source protocol, not stated in the record"
        elif low in {"control", "mock", "ctrl"}:
            arm, medium, medium_source = "control", "not named", "record says control without a medium"
        else:
            arm, medium, medium_source = (treatment or "not stated"), "not named", "not determinable from the record"

        rows.append({
            "accession": rec["accession"],
            "title": title,
            "tissue": tissue or "not stated",
            "treatment_field": treatment or "not stated",
            "condition": condition or "not stated",
            "donor": donor_of(title),
            "arm": arm,
            "medium": medium,
            "medium_source": medium_source,
            "single_cell_h5": "yes" if re.search(r"\.h5(\b|$)", supp, re.IGNORECASE) else "no",
        })
    rows.sort(key=lambda r: r["accession"])
    with open(out / OUTPUTS[0], "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    def tally(field: str, subset=None) -> dict:
        counts: dict[str, int] = {}
        for r in (subset if subset is not None else rows):
            counts[r[field]] = counts.get(r[field], 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))

    explant_sc = [r for r in rows if r["single_cell_h5"] == "yes" and "explant" in r["tissue"].lower()]
    donors = sorted({r["donor"] for r in explant_sc})
    by_donor = {}
    for d in donors:
        arms = {r["arm"] for r in explant_sc if r["donor"] == d}
        controls = sorted({r["medium"] for r in explant_sc if r["donor"] == d and r["arm"] == "control"})
        by_donor[d] = {"arms": sorted(arms), "control_media_present": controls}

    # Which infected arms have a medium-matched control in the same donor, by the protocol rule.
    matched = {}
    for arm, need in PROTOCOL_MEDIUM.items():
        ok = [d for d in donors
              if arm in by_donor[d]["arms"] and need in by_donor[d]["control_media_present"]]
        matched[arm] = {"required_control_medium": need, "donors_with_arm_and_matched_control": sorted(ok),
                        "count": len(ok)}

    record = {
        "task": "C1, GEO half",
        "scope": "series metadata only; the count object is not read and no join is verified here",
        "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script": "docs/research_pipeline/scripts/c1_geo_crosswalk.py",
        "script_sha256": sha256(Path(__file__).resolve()),
        "input": {"path": "docs/roadmap_runs/2026-09-27-followthrough/metadata/GSE198864.json",
                  "sha256": sha256(METADATA)},
        "superseded_attempt": "geo_attempt1_parser_defect/, whose donor parser did not fit the explant titles",
        "records": len(rows),
        "tissue_tally": tally("tissue"),
        "single_cell_explant_records": len(explant_sc),
        "single_cell_explant_donors": donors,
        "explant_arms_and_controls_by_donor": by_donor,
        "medium_matched_donor_counts_by_arm": matched,
        "unresolved": [
            "Only the control libraries state a medium. An infected library's medium is taken from the source protocol, so a medium-matched pairing is a protocol inference and not a recorded fact.",
            "Donor is parsed from the title and is a metadata reading, not an object-verified identity.",
            "Nothing here establishes which libraries the count object actually contains, nor its cell labels.",
        ],
        "joins_verified_against_object": False,
    }
    (out / OUTPUTS[1]).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print("records %d; single-cell explant %d across donors %s" % (len(rows), len(explant_sc), donors))
    print("tissues: %s" % record["tissue_tally"])
    for d in donors:
        print("  %-7s arms %-58s controls %s"
              % (d, ",".join(by_donor[d]["arms"]), by_donor[d]["control_media_present"]))
    print()
    print("donors with an infected arm AND its protocol-matched control medium:")
    for arm, info in sorted(matched.items(), key=lambda kv: -kv[1]["count"]):
        print("  %-12s needs %-4s -> %d donors %s"
              % (arm, info["required_control_medium"], info["count"],
                 info["donors_with_arm_and_matched_control"]))


if __name__ == "__main__":
    main()
