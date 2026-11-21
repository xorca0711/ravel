"""Bounded external-source qualification. No activity or beta contrasts."""
from collections import Counter
import csv
import gzip
import json
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import numpy as np
import pandas as pd

from sources import BARCODES, CACHE, all_sources, digest, libraries


RUNS = Path("analysis/research/runs")
S1 = RUNS / "ng26_jf_methylation_v1"
PROBES = {"cg43259781_BC21", "cg31603876_BC21", "cg41514640_BC21", "cg41514641_TC21",
          "cg41514643_BC21", "cg40106775_BC21", "cg43474386_BC11", "cg43474390_BC21"}
MOTIF = "chr13:52892163-52892175"
COMP = bytes.maketrans(b"ACGT", b"TGCA")


def save(rows, out, name):
    pd.DataFrame(rows).to_csv(out / name, index=False, sep="\t", na_rep="NA")


def reference(archive, row):
    obj = json.loads(archive.read(f"reference/{row.amplicon_row}.json"))
    assert obj["genome"] == "mm10" and obj["chrom"] == row.chrom
    return obj["start"], obj["dna"].upper()


def yin(panel, archive, out):
    focal = panel.loc[MOTIF]
    start, dna = reference(archive, focal)
    i, j = int(focal.scored_start - start), int(focal.scored_end - start)
    words = {"scored_12": dna[i:j], "native_16": dna[i-2:j+2], "CpG_AP1_9": dna[i:i+9]}
    assert words["CpG_AP1_9"] == "CGTGACTCA" and words["scored_12"].count("CG") == 1
    patterns = {}
    for label, word in words.items():
        forward = word.encode()
        patterns[label] = (forward, forward.translate(COMP)[::-1])
    series, support = [], []
    for row in libraries().sort_values("run_accession").itertuples():
        alias = row.sample_alias
        bc = alias.split("_")[-1]
        factor, condition = BARCODES[bc]
        zero = alias.startswith("ZeroCycle_")
        cycle = 0 if zero else int(alias.split("_")[2])
        record = ET.parse(CACHE / (row.experiment_accession + ".xml"))
        protocol = record.findtext(".//LIBRARY_CONSTRUCTION_PROTOCOL")
        assert protocol == ("HT-SELEX" if zero else condition)
        sample_id = record.find(".//SAMPLE_DESCRIPTOR").attrib["accession"]
        fastq = CACHE / (row.run_accession + ".fastq.gz")
        assert fastq.stat().st_size == int(row.fastq_bytes) and digest(fastq, "md5") == row.fastq_md5
        meta = dict(factor_series=factor, selected_construct="full length" if factor == "JUN" else "extended DBD",
                    series_condition=condition, cycle=cycle, input=zero, project=row.project, sample=sample_id,
                    sample_alias=alias, barcode=bc, experiment=row.experiment_accession, run=row.run_accession,
                    library_protocol=protocol, reads=int(row.read_count))
        lengths, eligible, ambiguous = Counter(), 0, 0
        counts = {label: Counter() for label in words}
        inserts = {label: set() for label in words}
        with gzip.open(fastq, "rb") as h:
            for header in h:
                seq, plus, qual = next(h).rstrip(), next(h), next(h).rstrip()
                assert header.startswith(b"@") and plus.startswith(b"+") and len(seq) == len(qual)
                lengths[len(seq)] += 1
                if len(seq) != 40:
                    continue
                if re.search(b"[^ACGT]", seq):
                    ambiguous += 1
                    continue
                eligible += 1
                for label,(fwd,rev) in patterns.items():
                    fw, rv = fwd in seq, rev in seq
                    if fw or rv:
                        counts[label]["any"] += 1
                        counts[label]["forward"] += int(fw)
                        counts[label]["reverse"] += int(rv)
                        counts[label]["both"] += int(fw and rv)
                        inserts[label].add(min(seq, seq.translate(COMP)[::-1]))
        assert sum(lengths.values()) == row.read_count
        series.append(dict(**meta, fastq_bytes=row.fastq_bytes, fastq_md5=row.fastq_md5, url="https://"+row.fastq_ftp,
                           length_counts=json.dumps(dict(sorted(lengths.items()))), ambiguous_40=ambiguous,
                           eligible_ACGT_40=eligible))
        for label,word in words.items():
            count = counts[label]
            support.append(dict(**meta, locus=MOTIF, context=label, sequence_plus=word,
                                sequence_reverse=patterns[label][1].decode(), eligible_ACGT_40=eligible,
                                reads_either=count["any"], reads_forward=count["forward"], reads_reverse=count["reverse"],
                                reads_both=count["both"], distinct_canonical_40mers=len(inserts[label])))
    assert all(sorted(g.cycle)==[0,1,2,3,4] for _,g in pd.DataFrame(series).groupby("barcode"))
    save(series, out, "yin_libraries.tsv")
    save(support, out, "yin_context_coverage.tsv")


def geo_samples():
    text = gzip.decompress((CACHE / "geo.soft.gz").read_bytes()).decode()
    samples = []
    for block in text.split("^SAMPLE = ")[1:]:
        gsm = block.splitlines()[0]
        title = re.search(r"^!Sample_title = (.+)$", block, re.M)[1]
        treatment = re.search(r"^!Sample_characteristics_ch1 = treatment: (.+)$", block, re.M)[1]
        cell = re.search(r"^!Sample_characteristics_ch1 = cell type: (.+)$", block, re.M)[1]
        channels = re.findall(r"^!Sample_supplementary_file = .+?_(\d+_R\d+C\d+)_(Grn|Red)\.idat\.gz", block, re.M)
        assert len(channels)==2 and len({c[0] for c in channels})==1 and {c[1] for c in channels}=={"Grn","Red"}
        samples.append(dict(gsm=gsm, original_sample=title, arm=treatment, cell_type=cell, chip_position=channels[0][0]))
    s=pd.DataFrame(samples)
    assert len(s)==s.chip_position.nunique()==s.original_sample.nunique()==12 and s.groupby("arm").size().eq(3).all()
    return s


def array(panel, archive, out):
    manifest = pd.read_csv(CACHE / "manifest.gz", sep="\t", low_memory=False)
    manifest = manifest[manifest.Probe_ID.isin(PROBES)].copy()
    order = pd.read_csv(CACHE / "ordering.gz", sep="\t", usecols=["Probe_ID"])
    co = pd.read_csv(CACHE / "mm10.coord.gz", sep="\t")
    assert len(order)==len(co) and order.Probe_ID.is_unique
    anno = pd.concat([order,co], axis=1).set_index("Probe_ID")
    samples = geo_samples()
    geom = pd.read_csv(S1 / "mm10_windows.tsv", sep="\t", dtype={"plus_C_positions":"string"})
    geo_sites = {(r.locus, r.window): set() if pd.isna(r.plus_C_positions) else set(map(int,r.plus_C_positions.split("|")))
                 for r in geom.itertuples()}
    native = pd.read_csv(RUNS / "ng26_jf_measurements_v1/methylation_sites.tsv.gz", sep="\t",
                         usecols=["locus","model","gsm","plus_C"])
    cross, strand_coverage, availability = [], [], []
    with gzip.open(CACHE / "matrix.gz","rt",newline="") as f:
        reader = csv.reader(f)
        cols = next(reader)[1:]
        assert len(cols)==len(set(cols))==12 and set(cols)==set(samples.chip_position)
        beta = {}
        for row in reader:
            if row[0] in PROBES:
                assert row[0] not in beta
                beta[row[0]] = dict(zip(cols,row[1:],strict=True))
    assert set(beta)==set(manifest.Probe_ID)==PROBES and len(manifest)==8
    for m in manifest.itertuples():
        chrom, pos, end = m.CpG_chrm, int(m.CpG_beg), int(m.CpG_end)
        assert end==pos+2 and m.target=="CG" and not m.mask
        region = panel[panel.chrom.eq(chrom) & panel.amplicon_start.le(pos) & panel.amplicon_end.ge(end)]
        assert len(region)==1
        l = region.index.item()
        b = region.iloc[0]
        start, seq = reference(archive, b)
        assert seq[pos-start:end-start]=="CG" and pos in geo_sites[l,"amplicon"]
        strand = anno.loc[m.Probe_ID,"strand"]
        assert anno.loc[m.Probe_ID,"CpG_chrm"]==chrom and anno.loc[m.Probe_ID,"CpG_beg"]==pos
        assert strand == {0:"+",16:"-"}[m.mapFlag_A]
        assayed = pos if strand=="+" else pos+1
        windows = [w for w in ["scored_motif","left_flank","right_flank","composite"] if pos in geo_sites[l,w]]
        same = native[native.locus.eq(l) & native.plus_C.eq(pos)]
        for model,g in same.groupby("model"):
            assert len(g)==g.gsm.nunique()==6
            for gsm in g.gsm:
                coords=set()
                for line in archive.read(f"methylation/{gsm}/{b.amplicon_row}.bedGraph").decode().splitlines():
                    cc,left,right,_=line.split()
                    assert cc==chrom
                    coords.update(range(int(left),int(right)))
                strand_coverage.append(dict(probe=m.Probe_ID,locus=l,model=model,gsm=gsm,
                                            native_plus_C_available=pos in coords,native_opposite_available=(pos+1) in coords,
                                            array_strand_base_available=assayed in coords))
        cross.append(dict(probe=m.Probe_ID,locus=l,window="|".join(windows) or "amplicon only",
                          chrom=chrom,dyad_start_0=pos,dyad_end_exclusive=end,plus_C_0=pos,
                          minus_C_on_ref_G_0=pos+1,dyad_1based_inclusive=f"{pos+1}-{end}",
                          interrogated_strand=strand,interrogated_reference_base_0=assayed,
                          mapFlag_A=m.mapFlag_A,mapYD_A=m.mapYD_A,coord_mapQ=int(anno.loc[m.Probe_ID,"mapQ"]),
                          both_base_reference=seq[pos-start:end-start],P4_common_n=sum(same.model.eq("P4 organoid")),
                          tissue_vehicle_common_n=sum(same.model.eq("whole colon")),
                          in_scored_motif=pos in geo_sites[l,"scored_motif"],
                          distance_plus_C_from_single_motif_CpG_bp=pos-52892163 if l==MOTIF else None))
        for s in samples.itertuples():
            v=pd.to_numeric(beta[m.Probe_ID][s.chip_position],errors="coerce")
            ok=bool(np.isfinite(v) and 0<=v<=1)
            availability.append(dict(probe=m.Probe_ID,locus=l,gsm=s.gsm,original_sample=s.original_sample,
                                     arm=s.arm,chip_position=s.chip_position,finite_in_range=ok))
    flags=pd.DataFrame(availability)
    counts=flags.groupby(["probe","locus","arm"],as_index=False).finite_in_range.agg(nominal="size",usable="sum")
    save(cross,out,"array_dyads.tsv")
    save(strand_coverage,out,"native_dyad_coverage.tsv")
    save(samples,out,"array_specimens.tsv")
    save(flags,out,"array_availability.tsv")
    save(counts,out,"array_arm_counts.tsv")


def main(out):
    panel=pd.read_csv(S1/"binding_panel.tsv",sep="\t").set_index("locus")
    with ZipFile(S1/"stage1_sources.zip") as z:
        yin(panel,z,out)
        array(panel,z,out)
    save([dict(cache_file=k,url=v,bytes=(CACHE/k).stat().st_size,sha256=digest(CACHE/k))
          for k,v in all_sources().items()],out,"public_sources.tsv")


if __name__=="__main__":
    main(Path(sys.argv[1]))
