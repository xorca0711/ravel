"""Audit the deposited day-4 libraries and the semantics of their count matrix."""

import argparse
import csv
import gzip
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

RAW = Path("raw_data/wang_20261112")
COUNTS = RAW / "GSE114298_counts.STARMOUSE.GEO_05_08_2018.txt.gz"
SOFT = RAW / "GSE114298_family.soft.gz"
ENA = RAW / "PRJNA470833-ENA.tsv"
BIOSAMPLES = RAW / "biosamples.xml"
GENOTYPES = {"fl/fl": "deficient", "fl/+": "flox_het", "+/+": "wild_type"}


def write_tsv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t",
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_counts():
    with gzip.open(COUNTS, "rt", encoding="utf-8", newline="") as stream:
        records = csv.reader(stream, delimiter="\t")
        identifier, *columns = next(records)
        if identifier != "Ensembl_ID" or len(columns) != len(set(columns)):
            raise ValueError("Unexpected identifier or duplicate count columns")
        counts = {}
        for line, (gene, *values) in enumerate(records, 2):
            if (not re.fullmatch(r"ENSMUSG\d+", gene) or gene in counts
                    or len(values) != len(columns)
                    or any(not re.fullmatch(r"[0-9]+", value) for value in values)):
                raise ValueError(f"Invalid count record on line {line}")
            counts[gene] = [int(value) for value in values]
    return columns, counts


def read_manifest(columns):
    with gzip.open(SOFT, "rt", encoding="utf-8") as stream:
        sample_blocks = re.split(r"(?m)^\^SAMPLE = ", stream.read())[1:]
    with ENA.open(encoding="utf-8", newline="") as stream:
        runs = list(csv.DictReader(stream, delimiter="\t"))
    if len({run["run_accession"] for run in runs}) != len(runs):
        raise ValueError("Duplicate ENA run accession")
    biosample_genotypes = {
        record.attrib["accession"]: {
            attribute.text for attribute in record.iter("Attribute")
            if attribute.get("attribute_name") == "genotype"
        }
        for record in ET.parse(BIOSAMPLES).iter("BioSample")
    }
    samples = {}
    for block in sample_blocks:
        gsm = block.splitlines()[0]
        column, = re.findall(r"(?m)^!Sample_title = (.+)$", block)
        genotype, = re.findall(r"(?m)^!Sample_characteristics_ch1 = genotype: (.+)$", block)
        allele = genotype.rsplit("Ezh2-", 1)[1]
        biosample, = set(re.findall(r"SAMN\d+", block))
        if biosample_genotypes[biosample] != {genotype}:
            raise ValueError(f"BioSample genotype disagrees with GEO for {gsm}")
        experiment, = set(re.findall(r"SRX\d+", block))
        run, = [record for record in runs if record["experiment_accession"] == experiment]
        if (run["sample_accession"], run["experiment_alias"], run["sample_title"]) != (
                biosample, gsm, column) or column in samples:
            raise ValueError(f"Inconsistent source join for {gsm}")
        samples[column] = dict(
            column=column, gsm=gsm, biosample=biosample, experiment=experiment,
            run=run["run_accession"], layout=run["library_layout"],
            reported_genotype=genotype, group=GENOTYPES[allele],
            mouse_or_pool="unknown", batch="unknown",
        )
    if not len(samples) == len(runs) == len(biosample_genotypes) or set(samples) != set(columns):
        raise ValueError("Count columns, GEO samples and ENA experiments disagree")
    for key in ("gsm", "biosample", "experiment", "run"):
        if len({sample[key] for sample in samples.values()}) != len(samples):
            raise ValueError(f"Nonunique {key} in manifest")
    return [samples[column] for column in columns]


def main(output):
    columns, counts = read_counts()
    samples = read_manifest(columns)
    totals = [sum(values) for values in zip(*counts.values(), strict=True)]
    if not all(totals):
        raise ValueError("Zero count-library total")
    qc = [
        dict(column=column, assigned_gene_counts=totals[index],
             detected_genes=sum(row[index] > 0 for row in counts.values()),
             genes_ge_10=sum(row[index] >= 10 for row in counts.values()))
        for index, column in enumerate(columns)
    ]
    write_tsv(output / "sample_manifest.tsv", samples)
    write_tsv(output / "library_qc.tsv", qc)
    summary = dict(
        libraries=len(samples), genes=len(counts),
        genotype_counts=dict(Counter(sample["group"] for sample in samples)),
        all_zero_genes=sum(not any(row) for row in counts.values()),
        annotation="Ensembl GRCm38 release 78",
        count_scale="uniquely assigned STAR counts aggregated by gene per GEO",
        biological_independence="unknown",
        eligible_scope="deposited-library description with control-allele sensitivity",
    )
    (output / "qualification.json").write_text(json.dumps(summary, indent=2) + "\n",
                                                encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args().output)
