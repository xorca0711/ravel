"""Qualify deposited identifiers and denominators. No biological contrasts."""
import argparse
import ast
import csv
import gzip
import io
import json
import math
import re
import zlib
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import openpyxl
import pandas as pd
import pyfive

CACHE = Path("raw_data/nagaraja_s0")
SETS = {
    "main_tissue": "IGVFDS0237MRDL",
    "extended_tissue": "IGVFDS0502QEQJ",
    "organoid": "IGVFDS5536ZQMO",
}
CELL = re.compile(r"R1[._](\d+)[,_]R2[._](\d+)[,_]R3[._](\d+)[,_]P1[._](\d+)")


def record(name):
    return json.loads((CACHE / name).read_bytes())


def write_rows(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)


def panel_audit(out):
    counts, protein, sheets = [], [], {}
    for number in [7, 8, 9, 10, 11]:
        filename = f"moesm{number}.xlsx"
        book = openpyxl.load_workbook(CACHE / filename, read_only=True, data_only=True)
        for sheet in book:
            values = iter(sheet.values)
            header = next(values)
            rows = [r for r in values if any(v is not None for v in r)]
            sheets[sheet.title] = rows
            groups = Counter()
            for row in rows:
                group = re.sub(r" replicate\s*\d+$", "", str(row[0]), flags=re.I)
                groups[" ".join(group.split())] += 1
            for group, size in sorted(groups.items()):
                counts.append((filename, sheet.title, " | ".join(map(str, header)), group, size))
        book.close()
    for sample, day, denominator, numerator, fraction in sheets["Fig. 1k,l"]:
        assert 0 <= numerator <= denominator and denominator > 0
        assert math.isclose(numerator / denominator, fraction, abs_tol=1e-12, rel_tol=0)
        protein.append((sample, day, denominator, numerator, fraction))
    assert len({r[0] for r in protein}) == len(protein)
    write_rows(out / "protein_counts.tsv", ["source_mouse_label", "protocol_day", "CD44_positive",
               "FOS_CD44_double_positive", "deposited_fraction"], protein)
    write_rows(out / "worksheet_groups.tsv", ["file", "sheet", "fields", "source_group", "rows"], counts)
    gross = dict(sheets["Ext. Data Fig. 9d"])
    assert len(gross) == len(sheets["Ext. Data Fig. 9d"])
    gross_rows = []
    for sample, fraction in sheets["Fig. 4c"]:
        total = gross.get(sample)
        implied = total * fraction if total is not None else None
        gross_rows.append((sample, fraction, total, implied, total is not None and
                           math.isclose(implied, round(implied), abs_tol=1e-9)))
    write_rows(out / "gross_sample_join.tsv", ["source_label", "figure4c_fraction", "ed9d_count",
               "implied_large_count", "integer_compatible"], gross_rows)

    book_info = []
    with ZipFile(CACHE / "moesm5.zip") as archive:
        for name in archive.namelist():
            wb = openpyxl.load_workbook(io.BytesIO(archive.read(name)), read_only=True, data_only=True)
            for ws in wb:
                rows = ws.values
                first = next(rows)
                book_info.append((Path(name).name, ws.title, " | ".join(str(v) for v in first if v is not None)))
            wb.close()
    write_rows(out / "supplement_fields.tsv", ["workbook", "sheet", "first_row"], book_info)
    return {"protein_rows": len(protein), "protein_fraction_checks": "all within 1e-12",
            "microscopic_counts_ed9gh": dict(sheets_to_counts(sheets["Ext. Data Fig. 9g,h"]))}


def sheets_to_counts(rows):
    totals = Counter()
    for sample, count, _ in rows:
        totals[sample.split(" replicate")[0]] += count
    return totals


def clones(out):
    clean = pd.read_table(CACHE / "code/ref/mouse_organoids.cleaned_clone_calls.txt", dtype=str)
    long = pd.read_table(CACHE / "moesm4.txt", dtype={k: "category" for k in
                         ["feature", "clone", "atac_cell", "sample"]})
    assert clean.atac_cell.is_unique and clean.barcode_cell.is_unique
    assert not clean.isna().any().any() and not long.drop(columns="score").isna().any().any()
    raw = clean.assign(clone=clean.clone.str.split(",")).explode("clone")
    keys = ["atac_cell", "clone"]
    assert not raw.duplicated(keys).any()
    scores = long[keys + ["sample"]].drop_duplicates().astype(str)
    assert not scores.duplicated(keys).any()
    joined = raw.merge(scores, how="outer", on=keys, validate="one_to_one", indicator=True)
    grouped = long.groupby(["feature", "atac_cell", "clone"], observed=True)
    dup = int((grouped.size()-1).sum())
    per = long.groupby(["atac_cell", "clone"], observed=True)["feature"].nunique()
    repeated = long.groupby(["atac_cell", "feature"], observed=True).score.nunique(dropna=False)
    feature_counts = long.groupby("feature", observed=True).agg(rows=("clone","size"),
                     cells=("atac_cell","nunique"), clones=("clone","nunique"))
    feature_counts.to_csv(out / "score_feature_coverage.tsv", sep="\t", lineterminator="\n")
    summary = {"clean_rows": len(clean), "clean_pairs": len(raw), "score_rows": len(long),
               "score_features": int(long.feature.nunique()), "score_cells": int(long.atac_cell.nunique()),
               "score_clones": int(long.clone.nunique()), "score_pairs": len(scores),
               "clean_clones": int(raw.clone.nunique()), "join_counts": joined._merge.value_counts().to_dict(),
               "duplicate_score_keys": dup, "nonfinite_scores": int((~np.isfinite(long.score)).sum()),
               "features_per_pair_min_max": [int(per.min()), int(per.max())],
               "overlapping_cells_clean": int((raw.groupby("atac_cell").size() > 1).sum()),
               "overlapping_cells_scored": int((scores.groupby("atac_cell").size() > 1).sum()),
               "score_disagreements_in_overlaps": int((repeated > 1).sum()),
               "multiple_lines_per_clean_clone": int((raw.groupby("clone").replicate.nunique()>1).sum()),
               "multiple_histories_per_scored_clone": int((scores.groupby("clone")["sample"].nunique()>1).sum())}
    return joined, summary


def dictionaries():
    tree = ast.parse((CACHE / "upstream/fastq.process.py3.v0.9.py").read_bytes())
    names = ["R1", "R2", "R3", "P5revcomp"]
    result = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in names:
                original = ast.literal_eval(node.value)
                result[name] = {int(v.split(".")[1]): k.encode() for k, v in original.items()}
                assert len(result[name]) == len(original)
    return [result[k] for k in names]


def matrix_barcodes(acc):
    with pyfive.File(str(CACHE / "rna" / (acc+".h5"))) as handle:
        fields = sorted(handle["unknown"])
        cell_ids = [str(x, "ascii") for x in handle["unknown/barcodes"][:]]
        assert len(cell_ids) == len(set(cell_ids))
    return cell_ids, fields


def fragment_preview(acc):
    # The deposited stream can be BGZF. Consume complete members and complete lines only.
    compressed = (CACHE / (acc + ".prefix64k")).read_bytes()
    data = bytearray()
    while compressed:
        reader = zlib.decompressobj(31)
        data.extend(reader.decompress(compressed))
        compressed = reader.unused_data
    return sorted({line.split(b"\t")[3].decode() for line in data.split(b"\n")[:-1]})


def canonical(cell):
    match = CELL.fullmatch(cell)
    if not match:
        raise ValueError(f"Unrecognized indexed barcode {cell}")
    return tuple(int(x) for x in match.groups())


def barcode_lookup(out, joined):
    dictionaries_by_round = dictionaries()
    specimens, aliases, set_maps, observed, matrix_info = {}, {}, {}, {}, {}
    for name, accession in SETS.items():
        ds = record(accession+".json")
        maps = set()
        for pool in ds["samples"]:
            metadata = record(pool["accession"]+".json")
            file_id = metadata["barcode_map"].split("/")[2]
            maps.add(file_id)
            for child in metadata["multiplexed_samples"]:
                child_id = child["accession"]
                sample = record("specimens/"+child_id+".json")
                donors = sorted(d["accession"] for d in sample["donors"])
                alias = "|".join(sample.get("aliases", []))
                specimens[child_id] = (alias, "|".join(donors))
                if name == "organoid":
                    aliases[alias.split("sample_surya-")[-1]] = (child_id, "|".join(donors))
        set_maps[name] = maps
        ma, frag = (x["accession"] for x in ds["files"])
        barcodes, fields = matrix_barcodes(ma)
        observed[name, "RNA"] = barcodes
        observed[name, "ATAC_preview"] = fragment_preview(frag)
        matrix_info[name] = {"h5_fields":fields, "matrix":ma, "fragments":frag, "barcode_maps":sorted(maps)}
    observed["organoid","clean_or_scored_ATAC"] = sorted(set(joined.atac_cell))
    queries = {}
    for cells in observed.values():
        for cell in cells:
            if cell not in queries:
                parts = canonical(cell)
                queries[cell] = b"".join(d[i] for d,i in zip(dictionaries_by_round,parts))
    wanted = set(queries.values())
    hits, map_rows, desc = {}, {}, defaultdict(set)
    for file_id in sorted(set.union(*set_maps.values())):
        covered = defaultdict(set)
        n = 0
        with gzip.open(CACHE / "maps" / (file_id+".tsv.gz"), "rb") as f:
            header = next(f).strip().lower().replace(b" ",b"_").split(b"\t")
            if header != [b"barcode",b"sample_accession",b"sample_description"]:
                raise ValueError((file_id,header))
            for line in f:
                n += 1
                if line[:32] in wanted:
                    seq, child, label = line.rstrip().decode().split("\t")
                    covered[seq.encode()].add(child)
                    desc[child].add(label)
        hits[file_id] = covered
        map_rows[file_id] = n
    for child, (alias, donor) in specimens.items():
        if not donor:
            raise ValueError(f"Missing donor for {child}")
    write_rows(out / "specimen_key.tsv", ["specimen", "source_alias", "donor", "observed_map_labels"],
               [(k, *specimens[k], "|".join(sorted(desc[k]))) for k in sorted(specimens)])

    def matches(seq, maps):
        return sorted(set().union(*(hits[file_id].get(seq, ()) for file_id in maps)))

    count_rows, assigned, coverage = Counter(), {}, {}
    # Preserve exact per-record outcomes, including ambiguities. A raw RNA barcode does
    # not identify an ATAC singlet or provide the authors' stem/progenitor gate.
    out_file = out / "barcode_lookup.tsv.gz"
    with out_file.open("wb") as raw, gzip.GzipFile(filename="", mode="wb",fileobj=raw,mtime=0) as handle:
        handle.write(b"dataset\tinput\tindexed_cell\tspecimen_matches\tdonor_matches\n")
        for (name, kind), cells in observed.items():
            maps = set_maps[name]
            for cell in cells:
                match = matches(queries[cell], maps)
                donors = sorted({specimens[k][1] for k in match if k in specimens})
                count_rows[name,kind,len(match)] += 1
                handle.write(f"{name}\t{kind}\t{cell}\t{'|'.join(match)}\t{'|'.join(donors)}\n".encode())
                if kind == "clean_or_scored_ATAC":
                    assigned[cell] = "|".join(match)
            coverage[name+"."+kind] = {str(n): count_rows[name,kind,n] for n in
                                       sorted({v[2] for v in count_rows if v[:2] == (name,kind)})}
    main_rna = {queries[cell] for cell in observed["main_tissue","RNA"]}
    ext_rna = {queries[cell] for cell in observed["extended_tissue","RNA"]}
    extended_gaps = [q for q in ext_rna if not matches(q,set_maps["extended_tissue"])]
    fallback = Counter(len(matches(q,set_maps["main_tissue"])) for q in extended_gaps)
    info = {"records_by_number_of_distinct_specimen_matches":coverage, "map_rows_scanned":map_rows,
            "matrices":matrix_info,"same_indexed_barcode_main_extended_RNA":len(ext_rna & main_rna),
            "extended_unmatched_with_main_map_match_counts":dict(fallback)}
    return aliases, assigned, info


def finish_clones(out, joined, aliases, assigned):
    joined["alias_specimen"] = joined.replicate.map({k:v[0] for k,v in aliases.items()})
    joined["donor"] = joined.replicate.map({k:v[1] for k,v in aliases.items()})
    joined["barcode_map_specimen"] = joined.atac_cell.map(assigned)
    joined.rename(columns={"_merge":"join_state"}).sort_values(["replicate","clone","atac_cell"]).to_csv(
        out / "organoid_memberships.tsv",sep="\t",index=False,lineterminator="\n")
    summary = []
    scored = joined[joined._merge != "left_only"]
    for (line,history), sub in scored.groupby(["replicate","sample"],dropna=False):
        sizes = sub.groupby("clone").atac_cell.nunique()
        summary.append((line,history,sub.atac_cell.nunique(),len(sub),len(sizes),
                        (sizes>=5).sum(),(sizes>5).sum(),(sizes>=10).sum(),
                        sub.alias_specimen.nunique(),sub.donor.nunique(),
                        (sub.alias_specimen != sub.barcode_map_specimen).sum()))
    write_rows(out / "organoid_lines.tsv", ["line","history","scored_cells","memberships","clones",
               "clones_ge5","clones_gt5","clones_ge10","alias_specimens","distinct_donors",
               "barcode_disagreements_including_unmapped"],summary)
    sizes = joined.groupby(["clone","replicate"],dropna=False).agg(
        union_cells=("atac_cell","nunique"),scored_cells=("_merge", lambda x:(x!="left_only").sum()),
        clean_cells=("_merge",lambda x:(x!="right_only").sum()))
    sizes.to_csv(out / "clone_sizes.tsv",sep="\t",lineterminator="\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    out = parser.parse_args().output
    report = panel_audit(out)
    members, report["organoid"] = clones(out)
    aliases, assigned, report["lookup"] = barcode_lookup(out,members)
    finish_clones(out,members,aliases,assigned)
    (out / "audit.json").write_text(json.dumps(report,indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
