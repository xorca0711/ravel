"""Inventory retained evidence and test a depth-estimand identity, without scientific reruns."""
import ast
import csv
import hashlib
import json
import math
import re
import statistics
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def git(*args):
    return subprocess.check_output(["git", "-c", f"safe.directory={ROOT.as_posix()}", *args],
                                   cwd=ROOT, text=True, encoding="utf-8", errors="replace").strip()


def detection(n, k, budget):
    assert all(isinstance(x, int) for x in (n, k, budget))
    assert 0 <= k <= n and 0 <= budget <= n
    return 1.0 - (math.comb(n-k, budget)/math.comb(n, budget) if n-k >= budget else 0.0)


def main():
    tracked = [p for p in git("ls-files", "-z").split("\0") if p]
    census, failures, documents = Counter(), [], []
    for name in tracked:
        path = ROOT/name
        if not path.is_file():
            failures.append(f"Missing tracked file: {name}")
            continue
        census[(name.split("/")[0] if "/" in name else "root", path.suffix)] += 1
        try:
            if path.suffix == ".py":
                ast.parse(path.read_text(encoding="utf-8-sig"), filename=name)
            elif path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8-sig"))
            elif path.suffix == ".md" and name.startswith("RQ_Specified/") and "/execution_sources/" not in name:
                body = path.read_text(encoding="utf-8-sig")
                documents.append({"path":name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                                  "headings":re.findall(r"^#{1,3} (.+)$",body,re.M)})
        except (SyntaxError, UnicodeError, ValueError) as exc:
            failures.append(f"{name}: {exc}")
    rq_ids = re.findall(r"^### (A\d+)\.", (ROOT/"RESEARCH_QUESTIONS.md").read_text(encoding="utf-8"), re.M)
    assert rq_ids == [f"A{i}" for i in range(16)], rq_ids
    # Conditional finite-population detection differs from its marginal expectation.
    # K~Binomial(N,p), followed by a B-molecule sample, yields Binomial(B,p).
    probes = []
    p, budget = .2, 10
    for n in (10,20,40,80):
        marginal = sum(math.comb(n,k)*p**k*(1-p)**(n-k)*detection(n,k,budget) for k in range(n+1))
        expected = 1-(1-p)**budget
        assert abs(marginal-expected) < 1e-12
        probes.append({"N":n,"B":budget,"p":p,"marginal_detection":marginal,
                       "binomial_detection":expected,"conditional_K_equals_Np":detection(n,round(n*p),budget)})
    schemas, numerical = {}, {}
    for name in [
        "RQ_Specified/A0_conserved_epithelial_transition_program/tables/pilot_v1/transfer_unit_differences.tsv",
        "RQ_Specified/A2_areg_source_delivery/tables/leg2_depth_correlations.tsv",
        "RQ_Specified/A2_areg_source_delivery/tables/stage3_contrasts.tsv",
    ]:
        with (ROOT/name).open(encoding="utf-8-sig", newline="") as handle:
            values = list(csv.DictReader(handle,delimiter="\t"))
        schemas[name] = {"columns":list(values[0]),"rows":len(values),"preview":values[:2]}
        if name.endswith("transfer_unit_differences.tsv"):
            by_endpoint = {}
            for endpoint in ("start", "destination"):
                effects = [float(r["difference"]) for r in values if r["role"]=="V1" and r["endpoint"]==endpoint]
                assert len(effects)==3
                loo = [statistics.median(effects[:i]+effects[i+1:]) for i in range(3)]
                passed = statistics.median(effects)>0 and sum(v>0 for v in effects)>=2 and min(loo)>0
                by_endpoint[endpoint] = {"mice":3,"median_score_points":100*statistics.median(effects),
                                         "positive_mice":sum(v>0 for v in effects),"decision":passed}
            assert by_endpoint["start"]["decision"] and not by_endpoint["destination"]["decision"]
            numerical["A0_V1"] = by_endpoint
        elif name.endswith("stage3_contrasts.tsv"):
            effects = [float(r["effect_vs_depth_matched_controls"]) for r in values
                       if r["endpoint"]=="activation_score" and r["target"]=="ITGB6" and r["interpretable"]=="yes"]
            assert len(effects)==3
            numerical["A2_ITGB6"] = {"readable_units":len(effects),"median_effect":statistics.median(effects)}
        elif name.endswith("leg2_depth_correlations.tsv"):
            chosen = [r for r in values if r["budget"]=="1000" and r["stratum"]=="pooled"
                      and r["x"]=="machinery" and r["y"]=="activation"]
            assert len(chosen)==1
            numerical["A2_primary_correlation"] = chosen[0]
    result = {"created_utc":datetime.now(timezone.utc).isoformat(),"baseline_commit":git("rev-parse","HEAD"),
              "scope":"Tracked-file census; Python syntax and JSON parse checks; RQ document inventory; exact depth-estimand probe. No raw-matrix rerun.",
              "tracked_files":len(tracked),"census":[{"root":k[0],"suffix":k[1],"files":v} for k,v in sorted(census.items())],
              "python_files_parsed":sum(v for (r,s),v in census.items() if s==".py"),
              "json_files_parsed":sum(v for (r,s),v in census.items() if s==".json"),
              "research_questions":rq_ids,"enabling_question":"A12-S1","rq_document_inventory":documents,
              "finite_population_probes":probes,"table_schemas":schemas,"numerical_reaggregations":numerical,"failures":failures}
    (HERE/"evidence.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ["baseline_commit","tracked_files","python_files_parsed","json_files_parsed","failures"]}))
    print(json.dumps(numerical))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
