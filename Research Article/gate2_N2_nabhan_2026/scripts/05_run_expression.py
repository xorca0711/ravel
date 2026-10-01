"""Validate the frozen contract, materialize R parameters, and record the DE run."""
from pathlib import Path
import csv
import hashlib
import json
import os
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
CACHE = ROOT / "raw_data/GSE307112/Nb3_v1"
OUT = HERE / "runs/R2_v1"

def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()

def r_string(value):
    return json.dumps(str(value).replace("\\", "/"))

def main():
    config = HERE / "config/Nb3_execution_v1.json"
    amendment = HERE / "config/Nb3_panel_amendment_v1.json"
    spec = json.loads(config.read_text())
    spec["programs"]["mouse"].update(json.loads(amendment.read_text())["replace_programs_mouse"])
    r2 = spec["R2"]
    extraction = json.loads((OUT / "extraction_record.json").read_text())
    assert extraction["config_sha256"] == sha(config)
    for species, record in extraction["species"].items():
        assert sha(CACHE / f"{species}_counts.bin") == record["matrix_sha256"]
    intent = OUT / "expression_intent.json"
    if intent.exists() or (CACHE / "DE").exists():
        raise SystemExit("Refusing to overwrite an existing Nb3 expression attempt")
    panels = CACHE / "panels.tsv"
    with panels.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["species", "program", "gene"])
        for species, programs in spec["programs"].items():
            for program, genes in programs.items():
                writer.writerows((species, program, gene) for gene in genes)
            for receptor in ("Egfr", "Erbb2", "Erbb3", "Erbb4"):
                gene = receptor if species == "mouse" else receptor.upper()
                writer.writerow((species, f"receptor_{gene}", gene))
    assignments = {"cache": CACHE, "out": OUT, "de_dir": CACHE / "DE", "panel_file": panels}
    lines = [f"{k} <- {r_string(v)}" for k, v in assignments.items()]
    lines.extend([
        'controls <- c(' + ', '.join(r_string(x) for x in r2["controls"]) + ')',
        'detection_cutoffs <- c(' + ', '.join(f'{k}={v}' for k,v in r2["species_gene_detection_cutoff"].items()) + ')',
        f'min_target <- {r2["min_target_libraries"]}', f'min_control <- {r2["min_control_libraries"]}',
        f'min_df <- {r2["min_residual_df"]}', f'diagnostic_fdr <- {r2["diagnostic_fdr"]}',
        'min_AveExpr <- 1.5', 'panel_pseudocount <- 0.5'])
    params = CACHE / "expression_parameters.R"
    params.write_text("\n".join(lines) + "\n", encoding="utf-8")
    script = HERE / "scripts/05_expression_reproduction.R"
    record = {"analysis_id": "Nb3_R2", "config_sha256": sha(config), "amendment_sha256": sha(amendment),
        "script_sha256": sha(script), "runner_sha256": sha(Path(__file__)), "parameters_sha256": sha(params),
        "panel_manifest_sha256": sha(panels), "status": "running", "started_unix": time.time(),
        "uncertainty": "technical wells; independent-preparation inference not supported"}
    intent.write_text(json.dumps(record, indent=2) + "\n")
    env = os.environ.copy()
    env["R_LIBS_USER"] = str(ROOT / "analysis/corrections/statistics/.tools/R-library")
    executable = ROOT / "analysis/corrections/statistics/.tools/R-portable/app/bin/x64/Rscript.exe"
    result = subprocess.run([str(executable), str(script), str(params)], env=env)
    record.update(status="completed" if result.returncode == 0 else "failed", exit_code=result.returncode,
                  seconds=round(time.time() - record["started_unix"], 2))
    if result.returncode == 0:
        record["outputs"] = {x.name: sha(x) for x in sorted(OUT.glob("*.tsv"))}
    (OUT / "expression_record.json").write_text(json.dumps(record, indent=2) + "\n")
    raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
