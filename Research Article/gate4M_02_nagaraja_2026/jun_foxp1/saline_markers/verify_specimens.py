"""Verify inputs without opening the external outcome matrix."""
from pathlib import Path
import csv
from decimal import Decimal
import gzip
import re
import sys
from zipfile import ZipFile


RUNS = Path("analysis/research/runs")
QUAL = RUNS / "ng26_jf_external_qualification_v1"
NATIVE = RUNS / "ng26_jf_methylation_v1"
EXPECTED = {
    "GSE283386": {"control": ["GSM8661258", "GSM8661259", "GSM8661260"],
                  "DSS": ["GSM8661261", "GSM8661262", "GSM8661263"]},
    "GSE316762": {"control": ["GSM9459788", "GSM9459789", "GSM9459790"],
                  "DSS": ["GSM9459782", "GSM9459783", "GSM9459784"]}}


def rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write(path, data):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, data[0].keys(), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(data)


def records(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        blocks = f.read().split("^SAMPLE = ")[1:]
    return {b.splitlines()[0]: b.split("^PLATFORM = ", 1)[0] for b in blocks}


def main(out):
    gse = records(Path("raw_data/nagaraja_s0/GSE316762_family.soft.gz"))
    external = records(Path("raw_data/nagaraja_jf_external/geo.soft.gz"))
    array_mice = {r["gsm"]: r for r in rows(QUAL / "array_specimens.tsv")}
    tissue_mice = {r["gsm"]: r for r in rows(NATIVE / "methylation_sources.tsv") if r["model"]=="whole colon"}
    people = []
    for study, groups in EXPECTED.items():
        for group, accessions in groups.items():
            for gsm in accessions:
                if study=="GSE283386":
                    s = array_mice[gsm]
                    assert s["arm"] == ("Saline+water" if group=="control" else "Saline+2.5% DSS")
                    assert s["chip_position"] in external[gsm] and "14 days post" in external[gsm]
                    name, arm, tissue, chip = s["original_sample"], s["arm"], "isolated colonic epithelium", s["chip_position"]
                else:
                    s = tissue_mice[gsm]
                    assert s["arm"] == ("Control vehicle" if group=="control" else "Recovered vehicle")
                    assert "whole colonic tissue" in gse[gsm] and "from OCT sections" in gse[gsm]
                    assert re.search("23 days following DSS cessation" if group=="DSS" else "healthy control",gse[gsm])
                    name, arm, tissue, chip = s["mouse"], s["arm"], "whole-colon OCT sections", "NA"
                people.append(dict(study=study, gsm=gsm, mouse=name, group=group, source_arm=arm, tissue=tissue,
                                   recovered_day=14 if study=="GSE283386" else 23, chip_position=chip))
    assert len({(s["study"],s["mouse"]) for s in people}) == len(people)==12
    probes = rows(QUAL / "array_dyads.tsv")
    assert len(probes)==len({p["probe"] for p in probes})==8 and len({p["locus"] for p in probes})==5
    valid = {(r["gsm"],r["probe"]) for r in rows(QUAL/"array_availability.tsv") if r["finite_in_range"]=="True"}
    panels = {r["locus"]:r for r in rows(NATIVE/"binding_panel.tsv")}
    native=[]
    with ZipFile(NATIVE/"stage1_sources.zip") as z:
        for p in probes:
            offset=int(p["plus_C_0"])+(p["interrogated_strand"]=="-")
            assert p["both_base_reference"]=="CG" and offset==int(p["interrogated_reference_base_0"])
            assert p["in_scored_motif"]=="False"
            for s in people:
                if s["study"]=="GSE283386":
                    assert (s["gsm"],p["probe"]) in valid
                    continue
                member=f"methylation/{s['gsm']}/{panels[p['locus']]['amplicon_row']}.bedGraph"
                matching=[]
                for line in z.read(member).decode().splitlines():
                    chrom,start,end,frac=line.split()
                    if chrom==p["chrom"] and int(start)<=offset<int(end):
                        matching.append(frac)
                frac,=matching
                assert Decimal(0)<=Decimal(frac)<=Decimal(1)
                native.append(dict(gsm=s["gsm"],mouse=s["mouse"],group=s["group"],probe=p["probe"],
                                   locus=p["locus"],window=p["window"],chrom=p["chrom"],
                                   plus_C_0=p["plus_C_0"],strand=p["interrogated_strand"],
                                   assayed_ref_0=offset,source_fraction=frac,archive_member=member))
    assert len(native)==len({(r["gsm"],r["probe"]) for r in native})==48
    write(out/"specimens.tsv",people)
    write(out/"nagaraja_same_strand.tsv",native)


if __name__=="__main__":
    main(Path(sys.argv[1]))
