"""Build the annotation and published D6 covariate inventory. Does not open any BigWig."""
import bisect
import csv
import gzip
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import openpyxl


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RAW = ROOT / "raw_data"
STEP1 = RAW / "naik_distal_step1_20261119"
ANNOTATION = RAW / "naik2017_s2_sources/gencode.vM9.annotation.gtf.gz"
SIZES = RAW / "naik2017_s3_sources/mm10.chrom.sizes"
CORE = [f"chr{i}" for i in range(1, 20)] + ["chrX"]
PRIMARY = ("Memory", "Resolved")


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def write_tsv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: ("NA" if value == "" else value) for name,value in row.items()})


def workbook_rows(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        values = wb.active.values
        header = next(values)
        for row_num, row in enumerate(values, 2):
            yield row_num, dict(zip(header, row, strict=True))
    finally:
        wb.close()


def read_transcripts(sizes):
    tss = defaultdict(list)
    transcripts = set()
    genes = set()
    bio = Counter()
    counts = Counter()
    strands = Counter()
    header = []
    attr_re = re.compile(r'(\w+) "([^"]+)"')
    with gzip.open(ANNOTATION, "rt", encoding="utf8") as handle:
        for line in handle:
            if line.startswith("#"):
                header.append(line.strip())
                continue
            chrom, _, feature, a, b, _, strand, _, attributes = line.rstrip().split("\t")
            if feature != "transcript":
                continue
            counts[chrom] += 1
            if chrom not in CORE:
                continue
            start, end = int(a), int(b)
            assert strand in ("+", "-") and 1 <= start <= end <= sizes[chrom]
            attrs = dict(attr_re.findall(attributes))
            ident = attrs["transcript_id"]
            assert ident not in transcripts
            transcripts.add(ident)
            genes.add(attrs["gene_id"])
            strands[strand] += 1
            bio[attrs["transcript_type"]] += 1
            tss[chrom].append((start if strand == "+" else end) - 1)
    assert set(tss) == set(CORE)
    tss = {k: sorted(v) for k, v in tss.items()}
    unique = {k: sorted(set(v)) for k, v in tss.items()}
    # An independent lookup representation using merged, chromosome-clipped promoters.
    merged = {}
    for chrom, sites in unique.items():
        intervals = []
        for site in sites:
            a, b = max(0, site - 2000), min(sizes[chrom], site + 2001)
            if intervals and a <= intervals[-1][1]:
                intervals[-1] = (intervals[-1][0], max(intervals[-1][1], b))
            else:
                intervals.append((a, b))
        merged[chrom] = ([a for a, _ in intervals], [b for _, b in intervals])
    return tss, unique, merged, dict(header=header, transcript_features_by_chromosome=counts,
        eligible_transcripts=len(transcripts), eligible_genes=len(genes), eligible_strands=strands,
        transcript_types=bio, unique_tss_by_chromosome={c: len(v) for c,v in unique.items()},
        unique_tss_total=sum(map(len, unique.values())),
        merged_promoter_intervals=sum(len(v[0]) for v in merged.values()))


def qualify_regions(sizes):
    all_tss, unique_tss, promoters, annotation = read_transcripts(sizes)
    regions = {}
    counts = Counter()
    for row_num, row in workbook_rows(STEP1 / "Cowley_S2.xlsx"):
        chrom, start, end, kind = (row[k] for k in ("Chromosome", "Start", "End", "Type"))
        key = (chrom, start, end)
        assert key not in regions and chrom in CORE and 0 <= start < end <= sizes[chrom]
        unique = unique_tss[chrom]
        sites = all_tss[chrom]
        lower, upper = start - 2000, end - 1 + 2000
        hits = bisect.bisect_right(sites, upper) - bisect.bisect_left(sites, lower)
        unique_hits = bisect.bisect_right(unique, upper) - bisect.bisect_left(unique, lower)
        starts, ends = promoters[chrom]
        candidate = bisect.bisect_right(ends, start)
        assert (hits > 0) == (candidate < len(starts) and starts[candidate] < end)
        i = bisect.bisect_left(unique, start)
        distance = min(([start - unique[i-1]] if i else []) +
                       ([max(0, unique[i] - end + 1)] if i < len(unique) else []))
        assert (distance <= 2000) == (hits > 0)
        regions[key] = dict(s2_excel_row=row_num, chromosome=chrom, start0=start, end0=end, width_bp=end-start,
            source_class=kind, overlapping_transcript_promoters=hits, overlapping_unique_tss_promoters=unique_hits,
            nearest_tss_base_distance_bp=distance, distal=int(not hits), primary=int(kind in PRIMARY and not hits),
            s3_excel_row="", s3_start1="", s3_end1="", s3_baseMean="", s3_D6_log2FoldChange="",
            s3_lfcSE="", s3_stat="", s3_padj="")
        counts[kind] += 1
    assert counts == Counter({"Memory":934, "Resolved":933, "Unchanged":934})
    all_s3 = set()
    for n, row in workbook_rows(STEP1 / "Cowley_S3.xlsx"):
        key = (row["seqnames"], row["start"] - 1, row["end"])
        assert key not in all_s3
        all_s3.add(key)
        if key not in regions:
            continue
        record = regions[key]
        assert record["s3_excel_row"] == "" and all(math.isfinite(row[f]) for f in ("baseMean","log2FoldChange","lfcSE","stat","padj"))
        record.update(s3_excel_row=n,s3_start1=row["start"],s3_end1=row["end"],
            s3_baseMean=row["baseMean"],s3_D6_log2FoldChange=row["log2FoldChange"],
            s3_lfcSE=row["lfcSE"],s3_stat=row["stat"],s3_padj=row["padj"])
    assert len(all_s3)==75642
    assert all(r["s3_excel_row"] and r["s3_padj"]<0.05 and r["s3_D6_log2FoldChange"]>0
               for r in regions.values() if r["source_class"] in PRIMARY)
    overlaps = 0
    for chrom in CORE:
        previous_ends = []
        for c, a, b in sorted(k for k in regions if k[0] == chrom):
            previous_ends = [e for e in previous_ends if e > a]
            overlaps += len(previous_ends)
            previous_ends.append(b)
    return list(regions.values()), dict(annotation=annotation, n_unique_s3=len(all_s3),
        n_unique_s2=len(regions), s2_duplicate_triples=0, overlapping_distinct_s2_pairs=overlaps)


def describe_support(primary_rows):
    # Feasibility only: pooled empirical quartiles use no M24 data and do not select primary members.
    fields = ("s3_D6_log2FoldChange","s3_baseMean","width_bp")
    cuts = {f:np.quantile([r[f] for r in primary_rows],[.25,.5,.75]).tolist() for f in fields}
    by_class = {}
    for kind in PRIMARY:
        selected = [r for r in primary_rows if r["source_class"] == kind]
        by_class[kind] = {f:np.quantile([r[f] for r in selected],[0,.25,.5,.75,1]).tolist() for f in fields}
    diagnostics = []
    for axes in [fields[:2],fields]:
        cells = defaultdict(Counter)
        for row in primary_rows:
            cell = tuple(bisect.bisect_right(cuts[f],row[f]) + 1 for f in axes)
            cells[cell][row["source_class"]] += 1
        shared = [c for c in cells.values() if all(c[k] for k in PRIMARY)]
        diagnostics.append(dict(axes=axes, occupied_cells=len(cells), shared_cells=len(shared),
            members_in_shared_cells={k:sum(c[k] for c in shared) for k in PRIMARY},
            maximum_coarse_one_to_one_pairs=sum(min(c[k] for k in PRIMARY) for c in shared),
            cell_counts=[dict(bin=list(key), Memory=cells[key]["Memory"], Resolved=cells[key]["Resolved"]) for key in sorted(cells)]))
    return dict(quantiles_order=[0,.25,.5,.75,1], class_covariate_quantiles=by_class,
                pooled_quartile_cuts=cuts, bins="Left-closed at each inner cut, tie goes to higher bin.", diagnostics=diagnostics)


def main():
    selection = json.loads((HERE/"selection_v1.json").read_text())
    hashes = {p.name:sha(p) for p in (ANNOTATION,SIZES,STEP1/"Cowley_S2.xlsx",STEP1/"Cowley_S3.xlsx")}
    assert hashes[ANNOTATION.name] == "93406cb8e6835339b0e64d0ad904a6d3e4527333f62a3a24f9a53c16083ca9fa"
    assert hashes[SIZES.name] == "55463d59f400b2c8260d100f4b521800ee773fa9711fe3f6dad9c7887db2574f"
    assert hashes["Cowley_S2.xlsx"] == selection["source"]["sha256"]
    assert hashes["Cowley_S3.xlsx"] == "7f54569f34f787c07f63d8dedcc654bb5b65e3f839dec8f33d6dbfe4dc681fde"
    sizes = {c:int(n) for c,n in (l.split() for l in SIZES.read_text().splitlines())}
    rows, summary = qualify_regions(sizes)
    write_tsv(HERE/"regions.tsv",rows)
    summary.update(source_sha256=hashes, classes={k:dict(deposited=sum(r["source_class"]==k for r in rows),
        distal=sum(r["distal"] for r in rows if r["source_class"]==k),
        primary=sum(r["primary"] for r in rows if r["source_class"]==k),
        s3_coordinate_matches=sum(bool(r["s3_excel_row"]) for r in rows if r["source_class"]==k))
        for k in ("Memory","Resolved","Unchanged")})
    summary["acute_covariate_support"]=describe_support([r for r in rows if r["primary"]])
    (HERE/"region_qualification.json").write_text(json.dumps(summary,indent=2,allow_nan=False)+"\n",encoding="utf8")
    print(summary["classes"],summary["overlapping_distinct_s2_pairs"])

if __name__ == "__main__":
    main()
