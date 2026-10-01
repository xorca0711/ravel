"""Fixed-panel descriptive contrasts and paired-compartment sensitivity diagnostics."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, t as student_t

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "runs/R4_v1"
EXT = HERE / "runs/extensions_v1"
R2 = HERE / "runs/R2_v1"

def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()

def rho(x, y):
    paired = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(paired) < 4 or paired.x.nunique() < 2 or paired.y.nunique() < 2:
        return np.nan
    return float(spearmanr(paired.x, paired.y).statistic)

def residual(values, covariates):
    x = np.column_stack([np.ones(len(values)), np.asarray(covariates, dtype=float)])
    return np.asarray(values, dtype=float) - x @ np.linalg.lstsq(x, np.asarray(values, dtype=float), rcond=None)[0]

def fit_contrast(frame, target, spec):
    plates = frame.loc[frame.target == target, "plate"].unique()
    selected = frame[(frame.target == target) | (frame.target.isin(spec["controls"]) & frame.plate.isin(plates))]
    indicator = (selected.target == target).to_numpy(dtype=float)
    nt, nc = int(indicator.sum()), int((1-indicator).sum())
    plate = pd.get_dummies(selected.plate, drop_first=True).to_numpy(dtype=float)
    x = np.column_stack([np.ones(len(selected)), plate, indicator])
    rank = np.linalg.matrix_rank(x)
    df = len(selected)-rank
    base = dict(target=target, target_wells=nt, control_wells=nc, plates=";".join(sorted(plates)), residual_df=df)
    if nt < spec["min_target_libraries"] or nc < spec["min_control_libraries"] or df < spec["min_residual_df"] or rank < x.shape[1]:
        return dict(**base, status="not_estimable")
    y = selected.score.to_numpy()
    coef = np.linalg.lstsq(x,y,rcond=None)[0]
    variance = np.sum((y-x@coef)**2)/df
    se = float(np.sqrt(variance*np.linalg.inv(x.T@x)[-1,-1]))
    width = student_t.ppf(.975,df)*se
    return dict(**base, status="technical_well_descriptive", effect=float(coef[-1]), se=se,
                ci_low=float(coef[-1]-width), ci_high=float(coef[-1]+width))

def main():
    spec_path = HERE / "config/Nb3_execution_v1.json"
    spec = json.loads(spec_path.read_text())
    if OUT.exists() or EXT.exists():
        raise SystemExit("Refusing to overwrite existing programme/extension run")
    # R writes both normalized panels before its per-target DE loop. These
    # completed inputs do not depend on the remaining whole-transcriptome fits.
    run = json.loads((R2 / "expression_intent.json").read_text())
    assert run["config_sha256"] == sha(spec_path)
    assert run["script_sha256"] == sha(HERE / "scripts/05_expression_reproduction.R")
    input_paths = [R2 / f"{s}_{name}.tsv" for s in ("mouse", "human") for name in ("normalization", "panel_scores", "panel_eligibility")]
    input_paths += [ROOT / "raw_data/GSE307112/Nb3_v1" / f"{s}_selected_symbol_cpm.tsv" for s in ("mouse", "human")]
    input_record = {"analysis_id": "Nb3_R4", "dependency_phase": "both species normalization and fixed panels complete; full DE may continue independently",
                    "config_sha256": sha(spec_path), "input_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in input_paths}}
    scores = pd.concat([pd.read_csv(R2 / f"{s}_panel_scores.tsv", sep="\t") for s in ("mouse", "human")], ignore_index=True)
    for species in ("mouse", "human"):
        norm = pd.read_csv(R2 / f"{species}_normalization.tsv", sep="\t")
        eligibility = pd.read_csv(R2 / f"{species}_panel_eligibility.tsv", sep="\t")
        group = scores[scores.species == species]
        assert not group.duplicated(["library", "program"]).any()
        assert set(group.library) == set(norm.library)
        assert len(group) == len(norm) * int(eligibility.eligible.sum())
    effects = []
    for (species, program), frame in scores.groupby(["species", "program"]):
        assert frame.library.is_unique and np.isfinite(frame.score).all()
        for target in sorted(set(frame.target)-set(spec["R2"]["controls"])):
            effects.append(dict(species=species, program=program, **fit_contrast(frame,target,spec["R2"])))
    effects = pd.DataFrame(effects)
    OUT.mkdir(); EXT.mkdir()
    (OUT / "panel_input_record.json").write_text(json.dumps(input_record, indent=2) + "\n")
    effects.to_csv(OUT / "fixed_panel_effects.tsv", sep="\t", index=False)
    focal = ["NKX21"] + spec["R4_extensions"]["comparison_targets"]
    effects[effects.target.isin(focal)].to_csv(EXT / "focal_target_panels.tsv", sep="\t", index=False)
    # Paired library intersection, preserving the species-specific QC decisions.
    normalization = {s: pd.read_csv(R2 / f"{s}_normalization.tsv", sep="\t") for s in ("mouse", "human")}
    paired = normalization["mouse"].merge(normalization["human"], on="library", suffixes=("_mouse", "_human"), validate="one_to_one")
    assert (paired.target_mouse == paired.target_human).all() and (paired.plate_mouse == paired.plate_human).all()
    paired["target"] = paired.target_mouse
    paired["plate"] = paired.plate_mouse
    paired[["library", "target", "plate", "total_reads_mouse", "total_reads_human"]].to_csv(OUT / "paired_library_QC.tsv", sep="\t", index=False)
    depth = []
    for (species, program), group in scores.groupby(["species", "program"]):
        group = group[["library", "score"]].merge(paired, on="library", validate="one_to_one")
        for subset in ("all_paired", "controls_only"):
            selected = group if subset == "all_paired" else group[group.target.isin(spec["R2"]["controls"])]
            plate = pd.get_dummies(selected.plate, drop_first=True).to_numpy(dtype=float)
            for depth_species in ("mouse", "human"):
                log_reads = np.log2(selected[f"total_reads_{depth_species}"])
                depth.append(dict(species=species, program=program, subset=subset, depth_species=depth_species, paired_wells=len(selected),
                    spearman=rho(selected.score,log_reads), plate_residual_spearman=rho(residual(selected.score,plate),residual(log_reads,plate))))
    pd.DataFrame(depth).to_csv(EXT / "paired_depth_diagnostics.tsv", sep="\t", index=False)
    # Associations of target contrasts; target count is not independent biological n.
    eligible = effects[effects.status == "technical_well_descriptive"].copy()
    eligible["key"] = eligible.species + "__" + eligible.program
    wide = eligible.pivot(index="target", columns="key", values="effect")
    imaging = pd.read_csv(HERE / "runs/R1_v1/imaging_effects.tsv", sep="\t")
    coverage = imaging[(imaging.variant == "all_wells_scaling") & (imaging.day == "day14") & (imaging.endpoint == "organoids_area_prop")].set_index("target").effect
    wide["growth_coverage"] = coverage
    mouse_programs = [x for x in wide if x.startswith("mouse__") and "receptor_" not in x]
    human_programs = [x for x in wide if x.startswith("human__") and "receptor_" not in x]
    comparisons = [(a,b) for a in mouse_programs for b in human_programs] + [("growth_coverage", b) for b in human_programs]
    associations, leaveouts = [], []
    for left,right in comparisons:
        columns = list(dict.fromkeys([left,right,"growth_coverage"]))
        data = wide[columns].dropna()
        observed = rho(data[left],data[right])
        conditioned = np.nan if left == "growth_coverage" else rho(residual(data[left],data[["growth_coverage"]]),residual(data[right],data[["growth_coverage"]]))
        associations.append(dict(left=left, right=right, eligible_targets=len(data), spearman=observed, growth_residual_spearman=conditioned))
        for omitted in focal:
            remaining = data.drop(index=omitted, errors="ignore")
            leaveouts.append(dict(left=left, right=right, omitted=omitted, omitted_present=omitted in data.index, eligible_targets=len(remaining), spearman=rho(remaining[left],remaining[right])))
    pd.DataFrame(associations).to_csv(EXT / "target_associations.tsv", sep="\t", index=False)
    pd.DataFrame(leaveouts).to_csv(EXT / "leave_target_out.tsv", sep="\t", index=False)
    activities = pd.read_csv(HERE / "runs/R3_v1/source_ICA_activities.tsv", sep="\t")
    activities[activities.target.isin(focal)].to_csv(EXT / "focal_source_ICA.tsv", sep="\t", index=False)
    wide.loc[wide.index.isin(focal)].to_csv(EXT / "focal_effect_matrix.tsv", sep="\t")
    # Receptor abundance is a compartment expression check, not receptor function.
    receptors = []
    for species in ("mouse", "human"):
        table = pd.read_csv(ROOT / "raw_data/GSE307112/Nb3_v1" / f"{species}_selected_symbol_cpm.tsv", sep="\t").set_index("gene")
        n = normalization[species]
        controls = n.loc[n.target.isin(spec["R2"]["controls"]), "library"]
        for base in ("Egfr", "Erbb2", "Erbb3", "Erbb4"):
            gene = base if species == "mouse" else base.upper()
            values = table.loc[gene, controls]
            receptors.append(dict(species=species, gene=gene, control_libraries=len(controls), median_TMM_CPM=values.median(), q25_TMM_CPM=values.quantile(.25), q75_TMM_CPM=values.quantile(.75), fraction_positive=float((values>0).mean())))
    pd.DataFrame(receptors).to_csv(EXT / "receptor_expression.tsv", sep="\t", index=False)
    record = {"analysis_ids": ["Nb3_R4"] + [f"Nb3_E{i}" for i in range(1,9)], "status": "executed_descriptive_with_explicit_mechanistic_holds",
        "config_sha256": sha(spec_path), "script_sha256": sha(Path(__file__)), "panel_input_record_sha256": sha(OUT / "panel_input_record.json"), "paired_QC_libraries": len(paired),
        "panel_contrasts": len(effects), "estimable_panel_contrasts": int((effects.status == "technical_well_descriptive").sum()),
        "uncertainty": "technical-well CIs; no biological p-values for panels or cross-target associations; source compartments and target position/guide confounding persist",
        "E1_E8": "shared contrast/programme analysis; no immune recruitment, lung specificity or causal pathway conclusion",
        "E2": "IFN/hypoxia/gastric/AT2 contrasts; no single-cell trajectory or fate inference",
        "E3_E4": "fixed panels and deposited component activities; no molecular mechanism identification",
        "E5_E6": "compartment receptor expression and source effects; no protein editing/function, DepMap fit or clinical causality inference",
        "E7": "paired bulk/growth association only; cell-type heterogeneity not estimable"}
    record["output_sha256"] = {f"{p.parent.name}/{p.name}": sha(p) for folder in (OUT,EXT) for p in sorted(folder.glob("*.tsv"))}
    (EXT / "run_record.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k:record[k] for k in ("paired_QC_libraries", "panel_contrasts", "estimable_panel_contrasts")}))

if __name__ == "__main__":
    main()
