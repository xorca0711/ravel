"""Check BigWig structure only at prespecified queries outside every S2 interval."""
import csv
import hashlib
import importlib.metadata
import json
import platform
import struct
import sys
from collections import defaultdict
from pathlib import Path

import bbi
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RAW = ROOT / "raw_data/naik_distal_m24_sources_20261119"
CORE = [f"chr{i}" for i in range(1, 20)] + ["chrX"]


def probes():
    regions = defaultdict(list)
    with (HERE / "regions.tsv").open() as stream:
        for r in csv.DictReader(stream, delimiter="\t"):
            regions[r["chromosome"]].append((int(r["start0"]), int(r["end0"])))
    assert sum(map(len,regions.values())) == 2801
    for chrom in ("chr1","chr2","chrX"):
        for start in (0,5_000_000,25_000_000,50_000_000):
            end = start + 10_000
            yield chrom,start,end,any(a < end and start < b for a,b in regions[chrom])


def check_probe(handle, chrom, start, end):
    # Store structural counts only. Never call on a locus overlapping a research interval.
    n = end-start
    reported = np.zeros(n,dtype=bool)
    explicit_zeros = np.zeros(n,dtype=bool)
    for c, a, b, value in handle.fetch_intervals(chrom,start,end,iterator=True):
        assert c == chrom and np.isfinite(value) and value >= 0
        lo, hi = max(start,a)-start, min(end,b)-start
        assert 0 <= lo < hi <= n and not reported[lo:hi].any()
        reported[lo:hi] = True
        explicit_zeros[lo:hi] = value == 0
    bases = handle.fetch(chrom,start,end,bins=-1,missing=np.nan,oob=np.inf)
    assert len(bases)==n and not np.isinf(bases).any()
    assert np.array_equal(~np.isnan(bases),reported)
    assert np.array_equal(bases == 0, explicit_zeros)
    return dict(chrom=chrom,start0=start,end0=end,explicit_zero_bp=int(explicit_zeros.sum()),
                stored_nonzero_bp=int((reported & ~explicit_zeros).sum()),absent_bp=int((~reported).sum()))


def main():
    selection = json.loads((HERE/"selection_v1.json").read_text())
    genome = {c:int(n) for c,n in (l.split() for l in (ROOT/"raw_data/naik2017_s3_sources/mm10.chrom.sizes").read_text().splitlines())}
    fixture=ROOT/"raw_data/naik2017_s3_runtime_v1/test.bw"
    with fixture.open("rb") as stream:
        fixture_sha=hashlib.file_digest(stream,"sha256").hexdigest()
    assert fixture_sha == "cfbf15ba7e9559db9841b246a12a79b51c44b2215137b652dc8f35b100b7ae86"
    fixture_bases=bbi.fetch(str(fixture),"1",0,4,bins=-1,missing=np.nan,oob=np.inf)
    assert np.isfinite(fixture_bases[:3]).all() and np.isnan(fixture_bases[3])
    candidates = list(probes())
    tracks = {}
    for gsm,expected in zip(selection["control"]+selection["post_IMQ"],selection["expected_bytes"],strict=True):
        receipt = json.loads((RAW/(gsm+"_receipt.json")).read_text())
        path=ROOT/receipt["path"]
        assert path.stat().st_size==expected==receipt["bytes"]
        with path.open("rb") as stream:
            assert hashlib.file_digest(stream,"sha256").hexdigest() == receipt["sha256"]
            stream.seek(0)
            magic=stream.read(4)
            stream.seek(44)
            total_summary_offset=struct.unpack("<Q",stream.read(8))[0]
            stream.seek(total_summary_offset)
            raw_bases_covered=struct.unpack("<Q",stream.read(8))[0]
            stream.seek(-4,2)
            footer=stream.read(4)
            assert magic == footer == bytes.fromhex("26fc8f88")
        assert bbi.is_bigwig(str(path))
        with bbi.open(str(path)) as handle:
            chromosomes=handle.chromsizes
            agreed = {c:n for c,n in chromosomes.items() if genome.get(c) == n}
            assert all(c in agreed for c in CORE)
            aliases={}
            for name,length in chromosomes.items():
                if name in agreed:
                    continue
                accession=name.split(".",1)[0]
                candidates_by_name=[c for c,n in genome.items() if accession in c.split("_") and n==length]
                if len(candidates_by_name)==1:
                    aliases[name]=candidates_by_name[0]
            assert len(set(aliases.values()))==len(aliases)
            info=handle.info
            metadata={k:v for k,v in info.items() if k!="summary"}
            metadata["basesCovered"]=info["summary"]["basesCovered"]
            assert metadata["basesCovered"]==raw_bases_covered
            metadata["sum_chromosome_lengths"]=sum(chromosomes.values())
            records=[check_probe(handle,c,a,b) for c,a,b,overlap in candidates if not overlap]
            tracks[gsm]=dict(header=metadata,zoom_reductions=handle.zooms,chromosome_sizes=chromosomes,unused_aliases_matching_accession_and_length=aliases,
                             dictionary_matches_ucsc=len(agreed),nonmatching={c:[n,genome.get(c)] for c,n in chromosomes.items() if c not in agreed},
                             missing_reference_contigs=sorted(set(genome)-set(chromosomes)),probes=records)
    result=dict(reader={"python":sys.version.split()[0],"system":platform.system(),"machine":platform.machine(),
                        "pybbi":importlib.metadata.version("pybbi"),"numpy":np.__version__},
                sparse_fixture={"sha256":fixture_sha,"chrom":"1","start0":0,"end0":4,"stored_bp":3,"absent_bp":1,"absent_returned_nan":True},
                skipped_overlapping_probes=[[c,a,b] for c,a,b,overlap in candidates if overlap],
                same_dictionary=all(t["chromosome_sizes"]==next(iter(tracks.values()))["chromosome_sizes"] for t in tracks.values()),
                tracks=tracks)
    (HERE/"track_structure.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf8")
    print([(k,len(v["chromosome_sizes"]),len(v["probes"])) for k,v in tracks.items()])

if __name__ == "__main__":
    main()
