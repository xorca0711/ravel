"""Resolve native fragment barcodes and donor denominators independently of panel signal."""
import ast
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
import re
import zlib

import numpy as np
import pandas as pd
from methylation import write, S0, RUNS

SCAN=RUNS/"ng26_jf_fragment_scan_v1"
SETS={"extended":"IGVFDS0502QEQJ","main":"IGVFDS0237MRDL"}
ID=re.compile(r"R1[._](\d+)[,_]R2[._](\d+)[,_]R3[._](\d+)[,_]P1[._](\d+)([-].+)?")
TIERS=(1,300,500)

def dictionary():
    names=("R1","R2","R3","P5revcomp")
    result={}
    for node in ast.parse((S0/"upstream/fastq.process.py3.v0.9.py").read_bytes()).body:
        if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name):
            name=node.targets[0].id
            if name in names:
                values=ast.literal_eval(node.value)
                result[name]={int(label.split(".")[1]):seq.encode() for seq,label in values.items()}
                assert len(result[name])==len(values)
    return [result[n] for n in names]

def header_p1(payload):
    buf=bytearray()
    while payload:
        inflater=zlib.decompressobj(31)
        buf.extend(inflater.decompress(payload))
        payload=inflater.unused_data
    lines=buf.split(b"\n")[:-1]
    p1=Counter()
    for idx in range(0,len(lines)-3,4):
        assert lines[idx].startswith(b"@") and lines[idx+2].startswith(b"+")
        match=re.search(rb"R1[._]\d+[,_]R2[._]\d+[,_]R3[._]\d+[,_]P1[._](\d+)(-\d+)?(?=$|[ /\t]|_[ACGTN]+(?:$|[ /\t]))",lines[idx])
        if match: p1[(int(match[1]),(match[2] or b"").decode())]+=1
    assert p1
    return p1

def provenance(bundle,series,label):
    def obj(name): return json.loads(bundle.read(name))
    ds=obj("records/"+series+".json")
    pools={};specimens={};tech=[];adapters=defaultdict(set)
    for p in ds["samples"]:
        pid=p["accession"];pool=obj("records/"+pid+".json")
        mapid=pool["barcode_map"].split("/")[2]
        alias=pool["aliases"][0]
        time=next((str(i) for i in (50,79,102) if f"{i}d" in alias),"main")
        if label=="extended": assert time!="main"
        children=set()
        for child in pool["multiplexed_samples"]:
            sid=child["accession"];sp=obj("records/"+sid+".json")
            donor,=[d["accession"] for d in sp["donors"]]
            name=sp["aliases"][0].split(":")[-1]
            condition="control" if re.search("control",name,re.I) else "colitis"
            rec=(donor,name,time,condition)
            assert sid not in specimens or specimens[sid]==rec
            specimens[sid]=rec;children.add(sid)
        pools[pid]=(mapid,children)
    for m in ds["input_file_sets"]:
        rec=obj("sets/"+m["accession"]+".json")
        assay=rec["assay_term"]["term_name"]
        pid,=[p["accession"] for p in rec["samples"]]
        mp,children=pools[pid]
        files=[f for f in rec["files"] if "barcode.fastq" in f.get("submitted_file_name","").lower()]
        assert files
        for f in files:
            for (adapter,suffix),reads in sorted(header_p1(bundle.read("prefix/"+f["accession"]+".64k")).items()):
                if "ATAC" in assay: adapters[adapter,suffix].add(pid)
                tech.append(dict(export=label,measurement=rec["accession"],assay=assay,pool=pid,map_file=mp,
                                 barcode_file=f["accession"],technical_basename=Path(f["submitted_file_name"]).name,
                                 public_uri=f["s3_uri"],prefix_bytes=65536,p1=adapter,raw_suffix=suffix or "none",complete_headers=reads,
                                 specimens="|".join(sorted(children)),biological_donors=len({specimens[s][0] for s in children})))
    return pools,specimens,tech,adapters

def decode(barcode,books):
    match=ID.fullmatch(barcode)
    if not match: return None,None,"unrecognized",None
    parts=tuple(int(x) for x in match.groups()[:4])
    suffix=match[5] or ""
    try: dna=b"".join(book[num] for book,num in zip(books,parts))
    except KeyError: dna=None
    return dna,parts[-1],suffix,parts

def map_cells(label,pools,specimens,adapters):
    depth=pd.read_csv(SCAN/(label+"_depth.tsv.gz"),sep="\t")
    assert depth.barcode.is_unique
    books=dictionary()
    codes=[decode(b,books) for b in depth.barcode]
    wanted={r[0] for r in codes if r[0] is not None}
    exact_cores={r[3] for r in codes if r[2]==""}
    suffix_aliases=Counter(r[3] for r in codes if r[2] and r[3] is not None)
    hits={}; labels=defaultdict(set); map_stats=[]
    for mp in sorted({x[0] for x in pools.values()}):
        matches={};freq=Counter()
        with gzip.open(S0/"maps"/(mp+".tsv.gz"),"rb") as f:
            header=next(f).strip().replace(b" ",b"_").lower().split(b"\t")
            assert header==[b"barcode",b"sample_accession",b"sample_description"]
            for line in f:
                seq,sp,hist=line.rstrip(b"\r\n").split(b"\t")
                freq[(sp,hist)]+=1
                if seq in wanted:
                    sid=sp.decode()
                    if seq not in matches: matches[seq]=sid
                    elif sid not in matches[seq].split("|"): matches[seq]+="|"+sid
        hits[mp]=matches
        for (sp,hist),n in freq.items():
            sid=sp.decode();labels[sid].add(hist.decode())
            map_stats.append(dict(export=label,map_file=mp,specimen=sid,map_history=hist.decode(),deposited_map_rows=n))
    assignments=[]
    for dna,p1,suffix,core in codes:
        candidates=set()
        supported=set()
        if dna:
            for mp,matches in hits.items():
                if dna in matches:
                    found=set(matches[dna].split("|"));candidates.update(found)
                    for pid in adapters.get((p1,suffix),()):
                        m,children=pools[pid]
                        if m==mp: supported.update(children.intersection(found))
        if dna is None: why="unrecognized or untranslatable"
        elif suffix and (p1,suffix) not in adapters: why="export suffix unresolved"
        elif not candidates: why="no exact map row"
        elif len(candidates)>1: why="ambiguous across maps"
        elif candidates!=supported: why="exact map lacks technical pool support"
        elif suffix and (core in exact_cores or suffix_aliases[core]>1): why="documented suffix, shared core"
        elif suffix: why="qualified documented suffix"
        else: why="qualified"
        sid=next(iter(candidates)) if why in {"qualified","qualified documented suffix","documented suffix, shared core"} else None
        if sid is not None: assert sid in specimens
        assignments.append((why,p1,suffix or "none",len(candidates),"|".join(sorted(candidates)) or None,
                            "|".join(sorted(supported)) or None,core in exact_cores,sid))
    ids=pd.DataFrame(assignments,columns=["mapping","p1","raw_suffix","candidate_count","core_map_candidates",
                                          "pool_supported_candidates","unsuffixed_core_observed","specimen"])
    return pd.concat([depth,ids],axis=1),labels,map_stats

def summarize(label,mapping,specimens,labels,windows):
    panel=pd.read_csv(SCAN/(label+"_panel.tsv.gz"),sep="\t")
    joined=panel.merge(mapping[["barcode","specimen","autosomal_unique","mapping"]],on="barcode",how="left",validate="many_to_one")
    assert len(joined)==len(panel) and joined.autosomal_unique.notna().all()
    library=[];results=[]
    primary=["qualified","qualified documented suffix"]
    qualified=mapping[mapping.mapping.isin(primary)]
    for floor in TIERS:
        use=qualified.loc[qualified.autosomal_unique.ge(floor)]
        eligible=joined.loc[joined.mapping.isin(primary)&joined.autosomal_unique.ge(floor)]
        for sid,(donor,name,time,condition) in sorted(specimens.items()):
            selected=use[use.specimen.eq(sid)]
            subset=eligible[eligible.specimen.eq(sid)]
            totals=int(selected.autosomal_unique.sum())
            library.append(dict(export=label,time=time,specimen=sid,donor=donor,source_alias=name,
                                condition=condition,map_history="|".join(sorted(labels[sid])) or None,
                                min_autosomal_per_barcode=floor,barcodes=len(selected),autosomal_unique=totals,
                                accepted_suffix_only_barcodes=int(selected.mapping.eq("qualified documented suffix").sum()),
                                held_suffix_alias_barcodes=int((mapping.specimen.eq(sid)&mapping.mapping.eq("documented suffix, shared core")&mapping.autosomal_unique.ge(floor)).sum()),
                                all_unique=int(selected.unique_fragments.sum()),mitochondrial_unique=int(selected.mitochondrial_unique.sum()),
                                read_support=int(selected.read_support.sum()),repeat_rows=int(selected.duplicate_rows.sum()),
                                normalization="autosomal unique fragments" if totals else "no denominator"))
            for chrom,wins in windows.groupby("chrom",sort=False):
                sub=subset[subset.chrom.eq(chrom)]
                starts=sub.start.to_numpy();ends=sub.end.to_numpy()
                for w in wins.itertuples(index=False):
                    n=ends_in=None
                    if w.applicable and totals:
                        n=int(((starts<w.end)&(ends>w.start)).sum())
                        ends_in=int(((starts>=w.start)&(starts<w.end)).sum()+((ends-1>=w.start)&(ends-1<w.end)).sum())
                    results.append((label,time,sid,donor,condition,floor,w.locus,w.window,totals,n,ends_in))
    columns=["export","time","specimen","donor","condition","min_autosomal_per_barcode","locus","window",
             "autosomal_denominator","unique_fragment_overlaps","native_fragment_ends"]
    return library,pd.DataFrame(results,columns=columns)

def audit(out,bundle,windows):
    libraries=[];counts=[];technical=[];maps=[];statuses=[];specimen_maps=[]
    for label,series in SETS.items():
        pools,specimens,tech,adapters=provenance(bundle,series,label)
        mapped,labels,source_maps=map_cells(label,pools,specimens,adapters)
        for pid,(mp,children) in pools.items():
            for sid in sorted(children):
                donor,name,time,condition=specimens[sid]
                specimen_maps.append(dict(export=label,pool=pid,map_file=mp,specimen=sid,donor=donor,source_alias=name,
                                          time=time,condition=condition,map_history="|".join(sorted(labels[sid])) or None))
        sample,rows=summarize(label,mapped,specimens,labels,windows)
        by=mapped.groupby(["mapping","raw_suffix","p1","candidate_count","unsuffixed_core_observed"],dropna=False).agg(
            barcodes=("barcode","size"),unique_fragments=("unique_fragments","sum"),autosomal_unique=("autosomal_unique","sum"),
            duplicate_rows=("duplicate_rows","sum"),read_support=("read_support","sum")).reset_index()
        by.insert(0,"export",label)
        statuses.append(by);libraries+=sample;counts.append(rows);technical+=tech;maps+=source_maps
        write(out,label+"_barcode_assignments.tsv.gz",mapped)
    libs=pd.DataFrame(libraries)
    # Multiple pool records reduce to one row per biological specimen, including a missing control.
    assert not libs.duplicated(["export","donor","min_autosomal_per_barcode"]).any()
    avail=libs.assign(usable=libs.autosomal_unique.gt(0)).groupby(
        ["export","time","condition","min_autosomal_per_barcode"],as_index=False).agg(
        nominal_donors=("donor","nunique"),usable_donors=("usable","sum"),barcodes=("barcodes","sum"),
        autosomal_unique=("autosomal_unique","sum"))
    write(out,"atac_measurements.tsv",technical)
    write(out,"atac_pool_specimens.tsv",specimen_maps)
    write(out,"atac_map_inventory.tsv",maps)
    write(out,"atac_barcode_status.tsv",pd.concat(statuses,ignore_index=True))
    write(out,"atac_donor_depth.tsv",libs)
    write(out,"atac_timepoint_eligibility.tsv",avail)
    write(out,"atac_sample_windows.tsv.gz",pd.concat(counts,ignore_index=True))
