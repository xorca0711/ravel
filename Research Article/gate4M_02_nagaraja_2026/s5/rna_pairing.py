"""Audit actual RNA barcodes and library/line-compatible candidates without assigning a state."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
import zlib

import pandas as pd

RAW=Path("raw_data/nagaraja_s0")
S5=Path("raw_data/nagaraja_s5")
BARCODE=re.compile(r"R1[._](\d+)[,_]R2[._](\d+)[,_]R3[._](\d+)[,_]P1[._](\d+)")


def code(text):
    match=BARCODE.fullmatch(text)
    if not match:
        raise ValueError(text)
    return tuple(map(int,match.groups()))


def audit(members):
    try:
        import pyfive
    except ImportError:
        sys.path.insert(0,str((RAW/"hdf_reader").resolve()))
        import pyfive
    with pyfive.File(str(RAW/"rna/IGVFFI1250KMMT.h5")) as h:
        group=h["unknown"]
        fields=sorted(list(group))
        assert fields==sorted(["barcodes","data","gene_names","genes","indices","indptr","shape"])
        raw_cells={code(v.decode()) for v in group["barcodes"][:]}
        genes={v.decode() for v in group["gene_names"][:]}
    lookup=pd.read_csv("analysis/research/runs/ng26_s0_v2/barcode_lookup.tsv.gz",sep="\t",dtype=str,keep_default_na=False)
    lookup=lookup.loc[lookup.dataset.eq("organoid") & lookup.input.eq("RNA")]
    line_lookup={code(r.indexed_cell):r.specimen_matches for r in lookup.itertuples()}
    assert raw_cells==set(line_lookup) and len(raw_cells)==len(lookup)
    by_rounds=defaultdict(list)
    for k in sorted(raw_cells):
        by_rounds[k[:3]].append(k)
    organoid=json.loads((RAW/"IGVFDS5536ZQMO.json").read_bytes())
    accessions={x["accession"] for x in organoid["input_file_sets"]}
    pools=defaultdict(dict);info=[]
    for acc in sorted(accessions):
        j=json.loads((S5/(acc+".json")).read_bytes())
        related={v["accession"] for series in j["related_measurement_sets"] if series["series_type"]=="multiome"
                 for v in series["measurement_sets"]}
        assert accessions-{acc}<=related
        f,=[f for f in j["files"] if f.get("submitted_file_name","").endswith("barcode.fastq.gz")]
        name=f["submitted_file_name"].split("/")[-1]
        pool,assay=name.split(".barcode")[0].rsplit("-",1)
        blob=zlib.decompressobj(31).decompress((S5/(f["accession"]+".prefix64k")).read_bytes())
        lines=blob.split(b"\n")[:-1]
        counts=Counter()
        for i in range(0,len(lines)-3,4):
            if not lines[i].startswith(b"@") or not lines[i+2].startswith(b"+"):
                raise ValueError("Malformed technical read")
            ident=re.search(rb"R1_\d+_R2_\d+_R3_\d+_P1_(\d+)",lines[i])
            if ident:
                counts[int(ident[1])]+=1
        assert counts and assay not in pools[pool]
        pools[pool][assay]=set(counts)
        for p1,n in sorted(counts.items()):
            info.append(dict(pool=pool,modality=assay,measurement_set=acc,barcode_file=f["accession"],
                             source_url=f["s3_uri"].replace("s3://igvf-public/","https://igvf-public.s3.amazonaws.com/"),
                             prefix_bytes=65536,p1=p1,complete_indexed_headers=n,raw_basename=name))
    adapter_pool={p1:pool for pool,v in pools.items() for p1 in v["ATAC"]}
    assert len(adapter_pool)==sum(len(v["ATAC"]) for v in pools.values())
    candidates=[];pair_counts=Counter();eligible=members.loc[members.in_score_table].drop_duplicates("atac_cell")
    for row in eligible.itertuples():
        k=code(row.atac_cell);pool=adapter_pool.get(k[3])
        allowed=pools[pool]["RNA"] if pool else set()
        same_pool=[u for u in by_rounds[k[:3]] if u[3] in allowed]
        same_line=[u for u in same_pool if line_lookup[u]==row.specimen]
        for u in same_line:pair_counts[(pool,k[3],u[3])]+=1
        one_by_one=(len(allowed)==1 and len(pools[pool]["ATAC"])==1) if pool else False
        candidates.append(dict(atac_cell=row.atac_cell,organoid_line=row.organoid_line,specimen=row.specimen,
                               pool=pool,atac_p1=k[3],exact_four_round_rna_key=k in raw_cells,
                               clone_assay_key_in_rna=code(row.clone_assay_cell) in raw_cells,
                               same_r123_pool_candidates=len(same_pool),same_r123_pool_specimen_candidates=len(same_line),
                               singleton_adapter_pool=one_by_one,
                               singleton_pool_unique_same_line=one_by_one and len(same_line)==1))
    cross=[dict(pool=p,atac_p1=a,rna_p1=r,same_rounds_same_specimen_pairs=pair_counts[(p,a,r)])
           for p,v in pools.items() for a in sorted(v["ATAC"]) for r in sorted(v["RNA"])]
    metadata=dict(rna_barcodes=len(raw_cells),matrix_fields=",".join(fields),
                  Car1_gene_in_matrix="Car1" in genes,scored_atac_cells=len(eligible),
                  RNA_adapters_in_full_matrix=",".join(map(str,sorted({k[3] for k in raw_cells}))),
                  ATAC_adapters_among_scored=",".join(map(str,sorted({code(k)[3] for k in eligible.atac_cell}))),
                  linked_state_labels=0)
    return pd.DataFrame(info),pd.DataFrame(candidates),pd.DataFrame(cross),pd.DataFrame([metadata])
