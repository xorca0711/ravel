"""Separate positional-reader verification; shares no production parser helpers."""
import csv
import gzip
import json
import re


def verify(raw, out):
    # Independently enumerate the four compressed source references, not the
    # uncompressed CSVs used by the production parser. No biological joins.
    expected_references = []
    reference_ids = {}
    for accession, suffix in [("GSM9964564", "1"), ("GSM9964565", "2"),
                              ("GSM9964566", "5"), ("GSM9964567", "6")]:
        with gzip.open(raw / f"{accession}_feature_reference_{suffix}.csv.gz",
                       "rt", newline="", encoding="utf-8-sig") as stream:
            table = list(csv.reader(stream))
        columns = [value.strip() for value in table[0]]
        positions = [columns.index(key) for key in ["id", "name", "feature_type", "multiplexed_sample"]]
        filename = f"{accession}_feature_reference.csv"
        reference_ids[filename] = set()
        for row in table[1:]:
            if not row:
                continue
            tag, name, kind, label = [row[index].strip() for index in positions]
            expected_references.append([filename, accession, tag, name, kind, label])
            reference_ids[filename].add(tag)
    expected_tags, feature_ids, feature_counts = [], {}, {}
    for accession, suffix in [("GSM9964560", "1"), ("GSM9964561", "2"),
                              ("GSM9964562", "6"), ("GSM9964563", "5")]:
        filename = f"{accession}_count{suffix}_features.tsv.gz"
        feature_ids[filename], feature_counts[filename] = set(), {}
        with gzip.open(raw / filename, "rt", encoding="utf-8-sig") as stream:
            for line in stream:
                tag, name, kind = [value.strip() for value in line.rstrip("\r\n").split("\t")]
                feature_ids[filename].add(tag)
                feature_counts[filename][kind] = feature_counts[filename].get(kind, 0) + 1
                if kind != "Gene Expression" or re.fullmatch(r"CMO\d+", tag):
                    expected_tags.append([filename, accession, tag, name, kind])
    expected_presence = [
        [feature, reference, tag, str(tag in identifiers).lower()]
        for feature, identifiers in feature_ids.items()
        for reference, tags in reference_ids.items() for tag in sorted(tags)
    ]
    for filename, expected in [("reference_labels.tsv", expected_references),
                               ("feature_tags.tsv", expected_tags),
                               ("reference_presence.tsv", expected_presence)]:
        with (out / filename).open(newline="", encoding="utf-8") as stream:
            actual = list(csv.reader(stream, delimiter="\t"))[1:]
        if sorted(actual) != sorted(expected):
            raise ValueError("Independent verification mismatch: " + filename)
    result = json.loads((out / "source_qualification.json").read_text(encoding="utf-8"))
    for reference in result["cmo_references"]:
        source_rows = [row for row in expected_references if row[0] == reference["file"]]
        if reference["labels"] != sorted({row[5] for row in source_rows}) or reference["tag_ids"] != sorted(row[2] for row in source_rows):
            raise ValueError("Reference summary mismatch: " + reference["file"])
    for feature in result["feature_tables"]:
        counts = feature_counts[feature["file"]]
        cmos = sorted(tag for tag in feature_ids[feature["file"]] if re.fullmatch(r"CMO\d+", tag))
        if feature["feature_type_rows"] != counts or feature["rows"] != sum(counts.values()) or feature["cmo_tag_ids"] != cmos:
            raise ValueError("Feature summary mismatch: " + feature["file"])
    for record in result["accession_records"]:
        text = (raw / (record["accession"] + ".txt")).read_text(encoding="utf-8-sig")
        for source_key, output_key in [("geo_accession", "accession"), ("title", "title")]:
            matches = re.findall(r"^!Sample_" + source_key + r" = (.*)$", text, re.MULTILINE)
            if len(matches) != 1 or matches[0].strip() != record[output_key]:
                raise ValueError("Accession identity/title mismatch")
    return {"ok": True, "method": "Separate positional CSV reader on compressed references; independent feature line/set census; exact TSV multiset and JSON summary comparisons.",
            "reference_rows_checked": len(expected_references), "feature_tag_rows_checked": len(expected_tags),
            "membership_rows_checked": len(expected_presence), "accession_records_checked": len(result["accession_records"]),
            "independence_limit": "Computational verification of the same public sources, not biological replication or independent scientific review."}
