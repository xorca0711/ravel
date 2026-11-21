"""Inventory the paired Table 6 rows, mm10 geometry and native CpG coverage."""
import ast
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd

RUNS=Path("analysis/research/runs")
S0=Path("raw_data/nagaraja_s0")
REF=RUNS/"ng26_s3_sources_v1"

def write(out,name,rows):
    frame=rows if isinstance(rows,pd.DataFrame) else pd.DataFrame(rows)
    opt={"method":"gzip","mtime":0} if name.endswith(".gz") else None
    frame.to_csv(out/name,sep="\t",index=False,na_rep="NA",compression=opt,lineterminator="\n")

def geometry(bundle):
    reg=pd.read_csv(S0/"code/7_inVitroFootprinting/Regions.csv")
    with ZipFile(S0/"moesm5.zip") as z:
        sheet,=[n for n in z.namelist() if "Table6_" in n]
        assay=pd.read_excel(io.BytesIO(z.read(sheet)),sheet_name="Raw in vitro binding score")
    # Physical Excel row, including one header row. Do not compute a score contrast.
    assay["excel_row"]=assay.index+2
    grouped=assay.set_index(["Chromosome","Start","End","TF"])
    assert grouped.index.is_unique and len(reg)==63
    regions=[]; windows=[]; sites={}
    for i,r in enumerate(reg.itertuples(index=False),1):
        chrom=r.Chromosome
        a,b,lo,hi=map(int,[r.amplicon_start,r.amplicon_end,r.motif_start,r.motif_end])
        mid=(lo+hi)//2
        obj=json.loads(bundle.read(f"reference/{i}.json"))
        assert (obj["genome"],obj["chrom"],obj["start"],obj["end"])==("mm10",chrom,a-1,b+1)
        seq=obj["dna"].upper()
        assert len(seq)==b-a+2 and a<lo<hi<b
        cpg={a-1+j for j in range(len(seq)-1) if seq[j:j+2]=="CG"}
        loc=f"{chrom}:{lo}-{hi}"
        key=(chrom,lo,hi)
        scores={}
        for tf in ("JUN","JUNFOXP1"):
            row=grouped.loc[(*key,tf)]
            assert row.label==r.label and np.isfinite(row.meanfootprintscore)
            scores[tf+"_excel_row"]=int(row.excel_row)
        intervals={"amplicon":(a,b),"scored_motif":(lo,hi),"composite":None,"fox_core":None,"annotated_ap1_core":None}
        if r.label=="AP1 + Fox":
            left,right=ast.literal_eval(r.composite_match_loc)
            cs,ce=mid+left,mid+right
            assert ce-cs==18 and r.composite_orientation in ("forward","reverse")
            fox=(cs,cs+7) if r.composite_orientation=="forward" else (ce-7,ce)
            ap=(ce-7,ce) if r.composite_orientation=="forward" else (cs,cs+7)
            intervals.update(composite=(cs,ce),fox_core=fox,annotated_ap1_core=ap)
            corelo,corehi=min(lo,cs),max(hi,ce)
        else:
            assert r.label=="AP1 only" and pd.isna(r.composite_match_loc)
            corelo,corehi=lo,hi
        intervals.update(left_flank=(a,corelo),right_flank=(corehi,b))
        regions.append(dict(locus=loc,amplicon_row=i,motif_class=r.label,chrom=chrom,amplicon_start=a,amplicon_end=b,
                            scored_start=lo,scored_end=hi,composite_orientation=r.composite_orientation,
                            composite_offset=r.composite_match_loc,**scores))
        for name,coords in intervals.items():
            pos=sorted(p for p in cpg if coords and coords[0]<=p and p+2<=coords[1])
            sites[(loc,name)]=pos
            windows.append(dict(locus=loc,window=name,chrom=chrom,start=coords[0] if coords else None,
                                end=coords[1] if coords else None,reference_CpGs=len(pos),
                                applicable=coords is not None,plus_C_positions="|".join(map(str,pos)) or None))
    assert len({r["locus"] for r in regions})==63
    assert (assay.TF.isin(["JUN","JUNFOXP1"])).sum()==126
    return pd.DataFrame(regions),pd.DataFrame(windows),sites

def track_manifest():
    t=pd.read_csv(REF/"ed6_tissue_sources.tsv",sep="\t")
    t["model"]="whole colon"; t["audit"]="Dcaf5";t["audit_hash"]=t.Dcaf5_bedgraph_sha256
    o=pd.read_csv(REF/"thbs1_track_sources.tsv",sep="\t")
    o["model"]="P4 organoid";o["audit"]="Thbs1";o["audit_hash"]=o.bedgraph_sha256
    o["arm"]=o.history;o["mouse"]=o.mouse_label
    cols=["gsm","model","arm","mouse","url","audit","audit_hash"]
    return pd.concat([t[cols],o[cols]],ignore_index=True)

def methylation(out,bundle,regions,windows,sites):
    tracks=track_manifest()
    details=[];specimen_rows=[];present={}; hashes=[]
    for t in tracks.itertuples(index=False):
        key=f"methylation/{t.gsm}/"
        audit=bundle.read(key+"audit_"+t.audit+".bedGraph")
        assert hashlib.sha256(audit).hexdigest()==t.audit_hash,(t.gsm,"S3 regional audit")
        for region in regions.itertuples(index=False):
            loc=region.locus
            payload=bundle.read(key+str(region.amplicon_row)+".bedGraph")
            hashes.append(dict(gsm=t.gsm,locus=loc,bytes=len(payload),sha256=hashlib.sha256(payload).hexdigest()))
            vals={}
            for line in payload.splitlines():
                chr_,st,en,val=line.split();start,end,value=int(st),int(en),float(val)
                assert chr_.decode()==region.chrom and 0<=value<=1
                assert region.amplicon_start-1<=start<end<=region.amplicon_end+1
                for pos in range(start,end):
                    assert pos not in vals
                    vals[pos]=value
            for p in sites[(loc,"amplicon")]:
                status="missing" if p not in vals else "reported zero" if vals[p]==0 else "reported nonzero"
                details.append(dict(gsm=t.gsm,locus=loc,plus_C=p,plus_C_status=status,G_position_reported=p+1 in vals))
            for row in windows.loc[windows.locus.eq(loc)].itertuples(index=False):
                cp=sites[(loc,row.window)]
                seen=set(cp).intersection(vals)
                present[t.gsm,loc,row.window]=seen
                zeros=sum(vals[p]==0 for p in seen)
                status=("not annotated" if not row.applicable else "no reference CpG" if not cp else
                        "all reference sites missing" if not seen else "all sites represented" if len(seen)==len(cp) else "partial")
                specimen_rows.append(dict(model=t.model,arm=t.arm,mouse=t.mouse,gsm=t.gsm,locus=loc,window=row.window,
                                          reference=len(cp),represented=len(seen),missing=len(cp)-len(seen),reported_zero=zeros,
                                          reported_nonzero=len(seen)-zeros,status=status))
    contrasts={"organoid_history":tracks.model.eq("P4 organoid"),
               "tissue_vehicle_history":tracks.arm.isin(["Control vehicle","Recovered vehicle"]),
               "tissue_recovered_drug":tracks.arm.isin(["Recovered vehicle","Recovered T5224"]),
               "tissue_four_arms":tracks.model.eq("whole colon")}
    coverage=[]
    for contrast,mask in contrasts.items():
        keep=list(tracks.loc[mask,"gsm"]);assert len(keep)==(12 if contrast=="tissue_four_arms" else 6)
        for w in windows.itertuples(index=False):
            shared=set.intersection(*(present[g,w.locus,w.window] for g in keep))
            coverage.append(dict(contrast=contrast,locus=w.locus,window=w.window,specimens=len(keep),
                                 applicable=w.applicable,reference_CpGs=w.reference_CpGs,common_CpGs=len(shared),
                                 eligible=bool(shared),common_plus_C="|".join(map(str,sorted(shared))) or None))
    write(out,"methylation_sources.tsv",tracks)
    write(out,"methylation_slices.tsv",hashes)
    write(out,"methylation_dyads.tsv.gz",details)
    write(out,"methylation_sample_windows.tsv.gz",specimen_rows)
    write(out,"methylation_contrast_coverage.tsv",coverage)
