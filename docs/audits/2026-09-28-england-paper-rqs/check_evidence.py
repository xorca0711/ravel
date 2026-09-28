"""Bounded England audit; read existing evidence, never refit the atlas.

Usage: python check_evidence.py --source-root PATH --paper-dir PATH
Writes audit evidence beside this script. All diagnostic analyses are post hoc.
Requires numpy/pandas; does not import or execute the source analysis scripts.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
PAPER_REL = Path("Research Article/gate2_C2_england_2025")
SNAPSHOT = "d485507"
LIBS = ["GSM7890835", "GSM7890836"]
EPS = ["priming_associated", "AT2_identity", "AT1_identity", "Itga2",
       "shared_gate_cycle_stress_disjoint", "lesion_gate_cycle_stress_disjoint", "cycling"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def smd(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    sd = np.sqrt(((len(x)-1)*x.var(ddof=1)+(len(y)-1)*y.var(ddof=1))/(len(x)+len(y)-2))
    return float((x.mean()-y.mean())/sd) if sd > 0 else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--paper-dir", type=Path, required=True)
    args = parser.parse_args()
    base = args.source_root / PAPER_REL
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", SNAPSHOT, "--", PAPER_REL.as_posix()],
        cwd=REPO, text=True).splitlines() + ["RESEARCH_QUESTIONS.md", "CLAIMS.md"]
    snapshot_checks = []
    for name in paths:
        committed = subprocess.check_output(["git", "show", f"{SNAPSHOT}:{name}"], cwd=REPO)
        current = (args.source_root / name).read_bytes()
        same = committed.replace(b"\r\n", b"\n") == current.replace(b"\r\n", b"\n")
        snapshot_checks.append({"path": name, "committed_sha256": hashlib.sha256(committed).hexdigest(),
                                "live_matches_after_newline_normalization": same})
    # Another chat may be editing the source worktree. Tracked evidence is read
    # from the pinned commit below; record live differences without overwriting.

    inputs = []
    def read(name):
        p = base / name
        rel = (PAPER_REL / name).as_posix()
        if rel in paths:
            data = subprocess.check_output(["git", "show", f"{SNAPSHOT}:{rel}"], cwd=REPO)
            inputs.append({"path": name, "sha256": hashlib.sha256(data).hexdigest(), "source": SNAPSHOT})
            return pd.read_csv(io.BytesIO(data), low_memory=False)
        inputs.append({"path": name, "sha256": sha(p), "source": "existing ignored cache"})
        return pd.read_csv(p, low_memory=False)

    a = read("trials/followup/FU_A_verdicts.csv")
    retention = []
    for _, row in a[a.endpoint.isin(EPS)].iterrows():
        for lib in LIBS:
            u = float(row[f"{lib}_unadjusted"])
            r = float(row[f"{lib}_depth_residualized"])
            retention.append({"endpoint": row.endpoint, "library": lib, "original_smd": u,
                              "residual_smd": r, "smd_ratio": r/u})
    pd.DataFrame(retention).to_csv(OUT / "depth_effect_ratios.csv", index=False)

    cells = read("processed/continuation/cells_table.csv.gz")
    labels = []
    for exp in (1, 2):
        d = read(f"processed/followup/experiment{exp}_round2.csv.gz")
        d["audit_experiment"] = exp
        labels.append(d)
    labels = pd.concat(labels, ignore_index=True)
    assert not labels.duplicated(["gsm", "barcode"]).any()
    joined = labels.merge(cells, on=["gsm", "barcode"], how="left", validate="one_to_one", indicator=True)
    assert joined._merge.eq("both").all()
    orig = read("trials/followup/FU_C_within_subcluster_cd177.csv")
    col = lambda ep: "raw_Itga2_log1p" if ep == "Itga2" else f"raw_{ep}"
    errors = []
    for (exp, cluster), g in joined[joined.primary_include].groupby(["audit_experiment", "sub_r1.0"]):
        p, n = g[g.Cd177_umi >= 1], g[g.Cd177_umi < 1]
        if min(len(p), len(n)) < 30:
            continue
        expected = orig[(orig.experiment == exp) & (orig.cluster == cluster)]
        for ep in EPS:
            errors.append(abs(smd(p[col(ep)], n[col(ep)])-float(expected[expected.endpoint == ep].smd.iloc[0])))
    assert max(errors) < 1e-10

    # Preserve the original EN5/FU_A libraries, inclusion and transition gate.
    # Existing clusters still contain endpoint information: this is a diagnostic,
    # not gene-disjoint validation and not a causal decomposition.
    eligible = joined[joined.primary_include & joined.gate_transition & joined.gsm.isin(LIBS)]
    coverage, effects = [], []
    for (gsm, cluster), g in eligible.groupby(["gsm", "sub_r1.0"]):
        p, n = g[g.Cd177_umi >= 1], g[g.Cd177_umi < 1]
        ok = min(len(p), len(n)) >= 30
        coverage.append({"library": gsm, "cluster": cluster, "n_pos": len(p), "n_neg": len(n), "eligible_30_per_side": ok})
        if ok:
            for ep in EPS:
                effects.append({**coverage[-1], "endpoint": ep, "smd": smd(p[col(ep)], n[col(ep)])})
    pd.DataFrame(coverage).to_csv(OUT / "a16_same_population_coverage.csv", index=False)
    pd.DataFrame(effects, columns=["library", "cluster", "n_pos", "n_neg", "eligible_30_per_side", "endpoint", "smd"]).to_csv(
        OUT / "a16_same_population_effects.csv", index=False)

    archive = REPO / "raw_data/england_continuation_inputs/zenodo_v1.1.zip"
    assert sha(archive) == "404697263ca941b1b74dee9feb4c4680ff3077d9e20bb7105482d17f14e96a70"
    with zipfile.ZipFile(archive) as z:
        member = next(n for n in z.namelist() if n.endswith("sim_two_pop_model.m"))
        source = z.read(member)
    assert b"(ws1+ws2+wp2+wp2)/w" in source
    assert b"(wf1+wf2+ws2+ws2)/w" in source
    # Pure S founder, q=.7: birth threshold .7, erroneous loss threshold .6.
    # elif loss branch cannot fire; .3 of candidate events become null events.
    bug = {"q": .7, "birth_threshold": .7, "literal_loss_threshold": 2*(1-.7),
           "loss_branch_reachable": bool(2*(1-.7) > .7), "archive_sha256": sha(archive),
           "member_sha256": hashlib.sha256(source).hexdigest()}
    diffs = read("trials/continuation/EN6/implementation_differences.csv")
    sim = diffs[(diffs.block == "Red2Kras_RFP") & (diffs.comparison == "literal vs literal_fixed_branch")]
    clones = read("trials/batch1/clones/clone_summary_by_mouse.csv")
    # Manually transcribed from visually checked mmc1.pdf p16, Table S1.
    # These are source values, not corrected values. Archive values come from
    # the existing, pinned batch1 decoding, not a fresh MAT-file reanalysis.
    source_counts = [
        ("kras4d", "YFP", [892, 7, 38], 937),
        ("kras1w", "YFP", [4532, 1586, 4848], 12073),
        ("kras2w", "YFP", [4155, 342, 1142], 10464),
        ("kras4w", "YFP", [3107, 1811, 2051], 6969),
        ("kras4d", "RFP", [886, 11, 25], 10464),
        ("kras1w", "RFP", [2967, 138, 4800], 8756),
        ("kras2w", "RFP", [1253, 252, 613], 4857),
        ("kras4w", "RFP", [1086, 544, 870], 2500),
    ]
    count_audit = []
    for dataset, channel, printed, total in source_counts:
        g = clones[(clones.dataset == dataset) & (clones.channel == channel)].sort_values("mouse_id")
        count_audit.append({"dataset": dataset, "channel": channel, "printed_mouse_counts": json.dumps(printed),
                            "printed_mouse_sum": sum(printed), "printed_total": total,
                            "archive_mouse_count": len(g), "archive_mouse_counts": json.dumps(g.proliferative_clones.astype(int).tolist()),
                            "archive_total": int(g.proliferative_clones.sum()), "printed_total_matches_printed_sum": sum(printed) == total})
    pd.DataFrame(count_audit).to_csv(OUT / "table_s1_reconciliation.csv", index=False)
    spatial = read("trials/batch1/clones/spatial_identity_gate.csv")
    slopes = read("trials/followup/FU_W_distance_slopes.csv")
    cfg = json.loads(subprocess.check_output(["git", "show", f"{SNAPSHOT}:{PAPER_REL.as_posix()}/config/followup_contract.json"], cwd=REPO))
    future = cfg["FU_S_simulator_refit"]
    source_files = [{"name": p.name, "bytes": p.stat().st_size, "sha256": sha(p)}
                    for p in sorted(args.paper_dir.glob("*.pdf"))]
    result = {
        "audit_date": "2026-09-28", "main_snapshot": "bbfa4e7", "england_snapshot": SNAPSHOT,
        "scope": "source/code/table audit plus post-hoc A16 same-population diagnostic; no new atlas or simulator fit",
        "snapshot_file_count": len(snapshot_checks), "snapshot_checks": snapshot_checks,
        "primary_sources": source_files, "cached_inputs": inputs,
        "fu_a_frozen_verdicts": a.verdict.value_counts().to_dict(),
        "fu_c_original_numeric_checks": len(errors), "fu_c_max_numeric_error": max(errors),
        "fu_c_original_estimated_clusters": orig[orig.status == "estimated"][["experiment", "cluster"]].drop_duplicates().to_dict("records"),
        "a16_same_population_eligible_strata": [r for r in coverage if r["eligible_30_per_side"]],
        "simulator_branch_audit": bug,
        "recorded_implementation_differences": json.loads(sim.to_json(orient="records")),
        "clone_units_by_dataset_channel": clones.groupby(["dataset", "channel"]).size().reset_index(name="mice").to_dict("records"),
        "table_s1_source_reconciliation": count_audit,
        "spatial_identity": json.loads(spatial.to_json(orient="records")),
        "fu_w_slope_columns": slopes.columns.tolist(),
        "fu_s_current_contract": future,
        "limitations": ["Cell cache and labels are existing exposed outputs, not independent data.",
                        "Same-population diagnostic keeps outcome-informed clusters and does not resolve overconditioning.",
                        "SMD ratios use different denominators; they are not fractions of signal explained.",
                        "No official claim grade was changed."]
    }
    (OUT / "evidence.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf8")
    print(json.dumps({"snapshot_files": len(snapshot_checks), "original_FU_C_checks": len(errors),
                      "max_error": max(errors), "same_population_eligible": result["a16_same_population_eligible_strata"],
                      "frozen_depth_verdicts": result["fu_a_frozen_verdicts"]}, indent=2))


if __name__ == "__main__":
    main()
