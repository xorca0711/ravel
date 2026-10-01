"""Verify Nb3 records and selected effects independently using the standard library."""
from pathlib import Path
import csv
import gzip
import hashlib
import json
import math
import statistics
import argparse

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parents[1]
CACHE=ROOT/"raw_data/GSE307112/Nb3_v1"

def sha(path):
    with path.open("rb") as handle: return hashlib.file_digest(handle,"sha256").hexdigest()

def read_json(path): return json.loads(path.read_text(encoding="utf-8"))
def read_rows(path):
    opener=gzip.open if path.suffix==".gz" else open
    with opener(path,"rt",encoding="utf-8-sig",newline="") as handle:
        return list(csv.DictReader(handle,delimiter="\t" if ".tsv" in path.name else ","))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path)
    parser.add_argument("--full-de-hashes",action="store_true")
    args=parser.parse_args()
    if args.out and args.out.exists(): raise SystemExit("Refusing to overwrite verification record")
    checks=[]
    def check(condition,label):
        if not condition: raise AssertionError(label)
        checks.append(label)
    spec=read_json(HERE/"config/Nb3_execution_v1.json")
    config_sha=sha(HERE/"config/Nb3_execution_v1.json")
    for entry in read_json(HERE/"reports/Nb3_acquisition.json")["files"]:
        check(sha(ROOT/entry["path"])==entry["sha256"],f"acquired input {entry['path']}")
    expression=read_json(HERE/"runs/R2_v1/expression_record.json")
    check(expression["status"]=="completed","R2 completed")
    for filename,key in [("05_expression_reproduction.R","script_sha256"),("05_run_expression.py","runner_sha256")]:
        check(sha(HERE/"scripts"/filename)==expression[key],f"recorded code {filename}")
    check(expression["config_sha256"]==config_sha,"frozen execution contract")
    check(expression["amendment_sha256"]==sha(HERE/"config/Nb3_panel_amendment_v1.json"),"frozen marker amendment")
    check(expression["parameters_sha256"]==sha(CACHE/"expression_parameters.R"),"materialized R parameters")
    for name,digest in expression["outputs"].items(): check(sha(HERE/"runs/R2_v1"/name)==digest,f"R2 output {name}")
    r1=read_json(HERE/"runs/R1_v1/run_record.json")
    check(r1["output_sha256"]==sha(HERE/"runs/R1_v1/imaging_effects.tsv"),"R1 output integrity")
    check(r1["script_sha256"]==sha(HERE/"scripts/04_imaging_reproduction.py"),"R1 code integrity")
    check(r1["config_sha256"]==config_sha,"R1 contract integrity")
    imaging=read_rows(ROOT/spec["inputs"]["imaging"]["path"])
    effects=read_rows(HERE/"runs/R1_v1/imaging_effects.tsv")
    # Independent standard-library recomputation from deposited measurements.
    for variant in ("all_wells_scaling","exclude_tdTomato_scaling"):
        for endpoint in spec["R1"]["endpoints"]:
            rows=[r for r in imaging if r["day"]=="day14"]
            stats={}
            for plate in {r["plate"] for r in rows}:
                values=[float(r[endpoint]) for r in rows if r["plate"]==plate and r[endpoint] not in ("","NA","NaN","nan") and (variant=="all_wells_scaling" or r["crispr_target"].upper()!="TDTOMATO")]
                stats[plate]=(statistics.mean(values),statistics.stdev(values))
            for target in ("NKX21","ERBB3","CTNNB1"):
                plates={r["plate"] for r in rows if r["crispr_target"].upper()==target}
                a,b=[],[]
                for row in rows:
                    if row["plate"] not in plates or row[endpoint] in ("","NA","NaN","nan"): continue
                    mean,sd=stats[row["plate"]]; value=(float(row[endpoint])-mean)/sd
                    if row["crispr_target"].upper()==target: a.append(value)
                    elif row["crispr_target"].upper()=="TIGIT": b.append(value)
                effect=statistics.mean(a)-statistics.mean(b)
                variance=((len(a)-1)*statistics.variance(a)+(len(b)-1)*statistics.variance(b))/(len(a)+len(b)-2)
                se=math.sqrt(variance*(1/len(a)+1/len(b)))
                observed=next(r for r in effects if r["variant"]==variant and r["day"]=="day14" and r["endpoint"]==endpoint and r["target"]==target)
                check(math.isclose(effect,float(observed["effect"]),abs_tol=1e-9) and math.isclose(se,float(observed["se"]),abs_tol=1e-9),f"independent imaging effect/SE {variant}/{endpoint}/{target}")
    ext=read_json(HERE/"runs/extensions_v1/run_record.json")
    check(ext["script_sha256"]==sha(HERE/"scripts/08_fixed_panel_extensions.py"),"extension code integrity")
    panel_input_path=HERE/"runs/R4_v1/panel_input_record.json"
    check(ext["panel_input_record_sha256"]==sha(panel_input_path),"extension input record integrity")
    for name,digest in read_json(panel_input_path)["input_sha256"].items(): check(sha(ROOT/name)==digest,f"extension input {name}")
    for name,digest in ext["output_sha256"].items(): check(sha(HERE/"runs"/name)==digest,f"extension output {name}")
    source_activities=read_rows(ROOT/"raw_data/nabhan_2026_sources/pnas.2606113123.sd06.csv")
    recovered_activities=read_rows(HERE/"runs/R3_v1/source_ICA_activities.tsv")
    indexed={row["source_target"]:row for row in recovered_activities}
    check(len(indexed)==len(source_activities)==200,"all source ICA target profiles retained")
    for source_row in source_activities:
        output_row=indexed[source_row[""]]
        check(all(math.isclose(float(source_row[f"ICA_{i:02d}"]),float(output_row[f"ICA_{i:02d}"]),abs_tol=1e-12) for i in range(1,21)),f"source ICA values {source_row['']}")
    for name in ("manifest.json","layout_revision.json"):
        manifest_figures=read_json(HERE/"figures"/name)
        for file,digest in manifest_figures["files"].items(): check(sha(HERE/"figures"/file)==digest,f"figure integrity {file}")
    panel_effects=read_rows(HERE/"runs/R4_v1/fixed_panel_effects.tsv")
    for species in ("mouse","human"):
        scores=read_rows(HERE/f"runs/R2_v1/{species}_panel_scores.tsv")
        for program in {r["program"] for r in scores}:
            group=[r for r in scores if r["program"]==program]
            plates={r["plate"] for r in group if r["target"]=="NKX21"}
            check(len(plates)==1,f"NKX21 one-plate direct-mean check {species}/{program}")
            a=[float(r["score"]) for r in group if r["target"]=="NKX21"]
            b=[float(r["score"]) for r in group if r["target"] in spec["R2"]["controls"] and r["plate"] in plates]
            observed=next(r for r in panel_effects if r["target"]=="NKX21" and r["species"]==species and r["program"]==program)
            check(math.isclose(statistics.mean(a)-statistics.mean(b),float(observed["effect"]),abs_tol=1e-9),f"independent NKX21 panel contrast {species}/{program}")
    summary=read_rows(HERE/"runs/R2_v1/DE_summary.tsv")
    expected={f"DE/{r['species']}/{r['target']}.tsv.gz" for r in summary if r["eligible"]=="TRUE"}
    manifest=read_json(HERE/"runs/R2_v1/DE_manifest.json")
    check(set(manifest["files"])==expected,"DE files exactly match eligible designs")
    if args.full_de_hashes:
        for name,digest in manifest["files"].items(): check(sha(CACHE/name)==digest,f"DE hash {name}")
    auth=read_json(HERE/"config/Nb3_authorization.json")
    check(sha(HERE/auth["prior_pipeline_path"])==auth["prior_pipeline_sha256"],"historical pipeline preserved")
    result={"analysis_id":"Nb3","status":"PASS","checks":len(checks),"full_de_hashes":args.full_de_hashes,
      "implementation_history":"Initial verification stopped before writing a result because a .gz suffix was compared without the dot; corrected gzip dispatch, with no scientific output changed",
      "independent_recalculations":"18 imaging effects/SEs and all eligible NKX21 fixed-panel effects directly from saved inputs",
      "scientific_limit":"Verification of computations and provenance does not establish independent biological replication",
      "script_sha256":sha(Path(__file__))}
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result))

if __name__=="__main__": main()
