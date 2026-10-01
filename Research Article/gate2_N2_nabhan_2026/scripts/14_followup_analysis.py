"""Execute the frozen Nb3 pre-RQ sensitivity, pathway and target checks."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import numpy as np
import pandas as pd
from scipy.stats import t as student_t

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
CACHE = ROOT / "raw_data/GSE307112/Nb3_v1"
OUT = HERE / "runs/followup_v1"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, frame):
    frame.to_csv(OUT / (name+".tsv"), sep="\t", index=False, float_format="%.12g", lineterminator="\n")


def fit(frame, target, controls, gates, covariates=(), omit=None):
    plates = frame.loc[frame.target == target, "plate"].unique()
    d = frame[(frame.target == target) | (frame.target.isin(controls) & frame.plate.isin(plates))].copy()
    if omit is not None: d = d[d.library != omit]
    z = (d.target == target).to_numpy(dtype=float)
    nt, nc = int(z.sum()), int((1-z).sum())
    plate = pd.get_dummies(d.plate, drop_first=True).to_numpy(dtype=float)
    cov = d[list(covariates)].to_numpy(dtype=float) if covariates else np.empty((len(d), 0))
    if covariates: cov = cov-cov.mean(axis=0)
    x = np.column_stack([np.ones(len(d)), plate, cov, z])
    rank = np.linalg.matrix_rank(x) if len(d) else 0
    df = len(d)-rank
    base = dict(target=target, target_wells=nt, control_wells=nc, plates=";".join(sorted(plates)), residual_df=df)
    if nt < gates["min_target_libraries"] or nc < gates["min_control_libraries"] or df < gates["min_residual_df"] or rank != x.shape[1]:
        return dict(**base, status="not_estimable", effect=np.nan, se=np.nan, ci_low=np.nan, ci_high=np.nan)
    y = d.score.to_numpy()
    coef = np.linalg.lstsq(x, y, rcond=None)[0]
    se = np.sqrt(np.sum((y-x@coef)**2)/df*np.linalg.inv(x.T@x)[-1, -1])
    width = student_t.ppf(.975, df)*se
    return dict(**base, status="technical_descriptive", effect=float(coef[-1]), se=float(se), ci_low=float(coef[-1]-width), ci_high=float(coef[-1]+width))


def main():
    path = HERE / "config/Nb3_followup_v1.json"
    spec = json.loads(path.read_text())
    if OUT.exists(): raise SystemExit("Refusing to overwrite followup_v1")
    for relative, expected in spec["inputs"].items():
        assert sha(ROOT / relative) == expected, relative
    OUT.mkdir()
    scripts = [Path(__file__), HERE / "scripts/14b_hallmark_context.R"]
    intent = {"config_sha256": sha(path), "script_sha256": {p.name: sha(p) for p in scripts}, "status": "started_after_input_verification"}
    (OUT / "intent.json").write_text(json.dumps(intent, indent=2)+"\n")
    old = pd.read_csv(HERE / "runs/R4_v1/fixed_panel_effects.tsv", sep="\t").set_index(["species", "program", "target"])
    checks, sensitivity, gene_effects = [], [], []
    scores_all = {}
    for species, programs in spec["programs"].items():
        norm = pd.read_csv(HERE / f"runs/R2_v1/{species}_normalization.tsv", sep="\t")
        cpm = pd.read_csv(CACHE / f"{species}_selected_symbol_cpm.tsv", sep="\t").set_index("gene")
        existing = pd.read_csv(HERE / f"runs/R2_v1/{species}_panel_scores.tsv", sep="\t")
        scores_all[species] = existing
        for program, genes in programs.items():
            # Receptor singletons are not part of the frozen non-receptor panel list.
            assert not program.startswith("receptor_")
            log = np.log2(cpm.loc[genes, norm.library]+.5)
            frame = norm[["library", "target", "plate"]].copy()
            frame["score"] = log.mean(axis=0).to_numpy()
            check = frame.set_index("library").score.reindex(existing[existing.program == program].library)
            err = float(np.max(np.abs(check.to_numpy()-existing[existing.program == program].score.to_numpy())))
            assert err < 1e-10
            checks.append(dict(check="score_recovery", species=species, program=program, target="all", max_abs_difference=err))
            for target in spec["targets"]:
                for variant, controls in spec["B1"]["control_variants"].items():
                    result = fit(frame, target, controls, spec["fit_gates"])
                    sensitivity.append(dict(species=species, program=program, variant=variant, omitted="", **result))
                    if variant == "combined":
                        prior = old.loc[(species, program, target)]
                        err = max(abs(result[k]-prior[k]) for k in ["effect", "se", "ci_low", "ci_high"])
                        assert err < 1e-9
                        checks.append(dict(check="contrast_recovery", species=species, program=program, target=target, max_abs_difference=err))
                for gene in genes:
                    f = frame.copy(); f["score"] = log.loc[gene].to_numpy()
                    gene_effects.append(dict(species=species, program=program, gene=gene, **fit(f, target, ["TIGIT", "TDTOMATO"], spec["fit_gates"])))
                    if len(genes) > 1:
                        f["score"] = log.drop(index=gene).mean(axis=0).to_numpy()
                        sensitivity.append(dict(species=species, program=program, variant="omit_gene", omitted=gene, **fit(f, target, ["TIGIT", "TDTOMATO"], spec["fit_gates"])))
                if len(genes) == 1:
                    sensitivity.append(dict(species=species, program=program, target=target, variant="omit_gene", omitted=genes[0], status="single_gene_panel_not_testable", effect=np.nan))
                for library in frame.loc[frame.target == target, "library"]:
                    sensitivity.append(dict(species=species, program=program, variant="omit_target_well", omitted=library, **fit(frame, target, ["TIGIT", "TDTOMATO"], spec["fit_gates"], omit=library)))
    sens = pd.DataFrame(sensitivity)
    write("panel_sensitivities", sens); write("individual_marker_effects", pd.DataFrame(gene_effects))
    summaries = []
    for (species, program, target), group in sens.groupby(["species", "program", "target"]):
        primary = group[group.variant == "combined"].iloc[0]
        for variant, rows in group[group.variant != "combined"].groupby("variant"):
            valid = rows[rows.status == "technical_descriptive"]
            summaries.append(dict(species=species, program=program, target=target, variant=variant,
                baseline_effect=primary.effect, planned=len(rows), estimable=len(valid),
                effect_min=valid.effect.min(), effect_max=valid.effect.max(),
                same_direction=int((np.sign(valid.effect) == np.sign(primary.effect)).sum()),
                technical_intervals_exclude_zero=int(((valid.ci_low > 0) | (valid.ci_high < 0)).sum())))
    write("panel_sensitivity_summary", pd.DataFrame(summaries))
    paired = pd.read_csv(HERE / "runs/R4_v1/paired_library_QC.tsv", sep="\t")
    for species in ["mouse", "human"]: paired["log_reads_"+species] = np.log2(paired["total_reads_"+species])
    depth_results = []
    for key in spec["B2"]["panels"]:
        species, program = key.split("__")
        score = scores_all[species]
        frame = paired.merge(score[score.program == program][["library", "score"]], on="library", validate="one_to_one")
        assert len(frame) == 771
        for target in sorted(set(frame.target)-{"TIGIT", "TDTOMATO"}):
            for variant, cov in [("paired_baseline", []), ("paired_depth", ["log_reads_mouse", "log_reads_human"])]:
                result = fit(frame, target, ["TIGIT", "TDTOMATO"], spec["fit_gates"], covariates=cov)
                depth_results.append(dict(species=species, program=program, variant=variant, **result))
                if species == "human" and variant == "paired_baseline" and result["status"] == "technical_descriptive":
                    err = abs(result["effect"]-old.loc[(species, program, target), "effect"])
                    assert err < 1e-9
                    checks.append(dict(check="paired_human_recovery", species=species, program=program, target=target, max_abs_difference=err))
    dep = pd.DataFrame(depth_results)
    write("paired_depth_effects", dep)
    dep[dep.target.isin(spec["targets"])].to_csv(OUT/"focal_depth_effects.tsv", sep="\t", index=False, float_format="%.12g", lineterminator="\n")
    assoc = []
    matrices = {}
    for variant, rows in dep.groupby("variant"):
        d = rows[rows.status == "technical_descriptive"].pivot(index="target", columns="species", values="effect").dropna()
        matrices[variant] = d
    common = matrices["paired_baseline"].index.intersection(matrices["paired_depth"].index)
    for variant, d in matrices.items():
        for population in ["all_estimable", "common_estimable", "common_without_NKX21"]:
            z = d if population == "all_estimable" else d.loc[common]
            if population == "common_without_NKX21": z = z.drop(index="NKX21", errors="ignore")
            assoc.append(dict(variant=variant, population=population, targets=len(z), spearman=float(z.mouse.corr(z.human, method="spearman"))))
    write("paired_depth_associations", pd.DataFrame(assoc))
    identities = pd.read_csv(HERE / "runs/00_v1/target_identity.tsv", sep="\t")
    target_rows = []
    for target in spec["targets"]:
        ids = identities[identities.target == target][["source_gene_id", "source_gene_name"]].drop_duplicates()
        assert len(ids) == 1, target
        table = pd.read_csv(CACHE / f"DE/mouse/{target}.tsv.gz", sep="\t")
        row = table[table.ID == ids.source_gene_id.iloc[0]]
        assert len(row) == 1, target
        target_rows.append(dict(target=target, source_gene_id=ids.source_gene_id.iloc[0], source_gene_name=ids.source_gene_name.iloc[0], **row.iloc[0].to_dict()))
    write("target_transcript_checks", pd.DataFrame(target_rows))
    write("recovery_checks", pd.DataFrame(checks))
    # Write simple R inputs; the wrapper verifies config/input hashes before this point.
    pd.DataFrame({"target": spec["targets"]}).to_csv(OUT / "targets.tsv", sep="\t", index=False)
    env = os.environ.copy()
    env["R_LIBS_USER"] = str(ROOT / "analysis/corrections/statistics/.tools/R-library")
    rscript = ROOT / "analysis/corrections/statistics/.tools/R-portable/app/bin/x64/Rscript.exe"
    call = subprocess.run([str(rscript), str(scripts[1]), str(ROOT), str(OUT)], env=env, capture_output=True, text=True)
    (OUT / "R_log.txt").write_text(call.stdout+call.stderr, encoding="utf-8")
    if call.returncode: raise RuntimeError(f"Hallmark stage failed; inspect {OUT/'R_log.txt'}")
    hall = pd.read_csv(OUT / "hallmark_camera.tsv", sep="\t")
    assert set(hall.intergene_correlation) == {0.01, 0.05}
    # Confirm input bytes did not change while computing.
    for relative, expected in spec["inputs"].items(): assert sha(ROOT / relative) == expected, relative
    record = {**intent, "status": "complete_exploratory_followup", "analysis_id": "Nb3",
        "counts": {"sensitivity_rows": len(sens), "estimable_sensitivity_rows": int((sens.status == "technical_descriptive").sum()), "marker_rows": len(gene_effects), "depth_rows": len(dep), "hallmark_rows": len(hall), "recovery_checks": len(checks)},
        "unresolved": ["human numeric S5 discrepancy", "independent preparations/target-guide-position confounding", "spatial design", "exact source embeddings", "independent functional validation"],
        "output_sha256": {p.name: sha(p) for p in sorted(OUT.iterdir()) if p.is_file()}}
    (OUT / "run_record.json").write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps(record["counts"]))


if __name__ == "__main__": main()
