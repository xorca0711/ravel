"""Verify the new E5 arithmetic, reviewed documentation, IDs and preserved atlas."""
from pathlib import Path
import ast
from collections import defaultdict
import hashlib
import io
import json
import math
import re
import subprocess
import sys
import tarfile
import xml.etree.ElementTree as ET
import zipfile
import numpy as np
import pandas as pd
import fitz
from PIL import Image

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
OUT = ROOT / "docs/audits/2026-10-01-cross-article-rq-review/verification.json"
RUN = HERE / "runs/E5_external_v1"
checks, failures = 0, []


def require(condition, label):
    global checks
    checks += 1
    if not condition:
        failures.append(label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(actual, expected, label, atol=1e-8):
    require(bool(np.allclose(actual, expected, atol=atol, rtol=1e-10)), label)


def xml_counts(raw):
    """Independent XLSX extraction without openpyxl or dataframe readers."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared = ["".join(si.itertext()) for si in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
        tree = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        output = defaultdict(float)
        for row in tree.findall("m:sheetData/m:row", ns)[1:]:
            cells = {}
            for cell in row.findall("m:c", ns):
                key = re.sub(r"\d", "", cell.attrib["r"])
                value = cell.find("m:v", ns)
                if cell.attrib.get("t") == "s":
                    cells[key] = shared[int(value.text)]
                elif cell.attrib.get("t") == "inlineStr":
                    cells[key] = "".join(cell.find("m:is", ns).itertext())
                else:
                    cells[key] = value.text if value is not None else ""
            if cells.get("A", "").strip():
                output[cells["A"]] += float(cells["B"])
        return dict(output)


def main():
    if OUT.exists() and json.loads(OUT.read_text()).get("status") == "PASS":
        raise SystemExit("Verification already passed; do not overwrite")
    OUT.write_text(json.dumps({"status": "RUNNING"})+"\n")
    spec_path = HERE / "config/Nb3_E5_external_v1.json"
    spec = json.loads(spec_path.read_text())
    receipt = json.loads((RUN / "run_record.json").read_text())
    require(sha(spec_path) == receipt["config_sha256"], "E5 contract unchanged")
    require(sha(HERE / "scripts/19_e5_external_pilot.py") == receipt["script_sha256"], "E5 analysis script unchanged")
    for item in receipt["input_hashes"]:
        require(sha(ROOT / item["path"]) == item["sha256"], "source hash "+item["path"])
    for name, expected in receipt["output_sha256"].items():
        require(sha(RUN / name) == expected, "E5 output hash "+name)
    independent = {}
    with tarfile.open(ROOT / "raw_data/GSE306184/GSE306184_RAW.tar") as archive:
        for member in archive.getmembers():
            if member.isfile():
                independent[member.name.split("_")[0]] = xml_counts(archive.extractfile(member).read())
    full = pd.DataFrame(independent).sort_index(axis=1)
    require(full.shape == (46425, 14), "independent unique symbols and samples")
    design = pd.read_csv(RUN / "sample_design_qc.tsv", sep="\t").rename(columns={"index": "GSM"}).set_index("GSM")
    close(full.sum().reindex(design.index), design.count_total, "14 independent XML library totals", atol=0)
    selected = pd.read_csv(RUN / "selected_source_counts.tsv", sep="\t").set_index("gene")
    close(full.loc[selected.index, selected.columns], selected, "266 independent XML selected counts", atol=0)
    require(design.groupby(["target", "context"]).size().tolist() == [2]*7, "seven groups with two libraries")
    require(not ((design.target != "control") & (design.context == "NoIR")).any(), "no invented uninjured knockdown")
    require((full.loc[["SFTPC", "SFTPA1"]] == 0).all().all(), "reported zero surfactant transcripts")
    positive = full.where(full > 0)
    eligible = (full > 0).sum(axis=1) >= 7
    geom = np.exp(np.log(positive.loc[eligible]).mean(axis=1))
    factors = positive.loc[eligible].divide(geom, axis=0).median()
    factors /= np.exp(np.log(factors).mean())
    close(factors.reindex(design.index), design.positive_median_ratio_factor, "median-ratio factors recovered")
    mats = {"CPM": full.divide(full.sum(), axis=1)*1e6,
            "positive_median_ratio_CPM": full.divide(factors, axis=1)/np.median(full.sum())*1e6}
    values = pd.read_csv(RUN / "selected_normalized_values.tsv", sep="\t")
    for row in values.itertuples():
        value = mats[row.normalization].loc[row.gene, row.GSM]
        close(value, row.normalized_abundance, "abundance "+row.GSM+" "+row.gene)
        close(math.log2(value+1), row.log2_abundance_plus_1, "log abundance "+row.GSM+" "+row.gene)
    effects = pd.read_csv(RUN / "gene_contrasts.tsv", sep="\t")
    for row in effects.itertuples():
        t = design.index[(design.target == row.target) & (design.context == row.context)]
        c = design.index[(design.target == "control") & (design.context == row.context)]
        y = np.log2(mats[row.normalization].loc[row.gene]+1)
        close(y[t].mean()-y[c].mean(), row.effect, "gene contrast "+row.target+row.context+row.gene)
    panels = pd.read_csv(RUN / "panel_contrasts.tsv", sep="\t")
    for row in panels.itertuples():
        d = effects[(effects.normalization == row.normalization) & (effects.target == row.target) & (effects.context == row.context)]
        close(d.set_index("gene").loc[spec["genes"][row.panel], "effect"].mean(), row.effect, "panel "+row.target+row.context+row.panel)
    for version in ["E5_external_v1", "E5_external_v2"]:
        folder = HERE / "figures" / version
        rec = json.loads((folder / "render_record.json").read_text())
        for name, expected in rec["outputs"].items():
            require(sha(folder / name) == expected, version+" export "+name)
    png = HERE / "figures/E5_external_v2/Nb3_F09_E5_external_pilot.png"
    require(Image.open(png).size == (2760,1140), "300 dpi F09 dimensions")
    with fitz.open(png.with_suffix(".pdf")) as pdf:
        require(len(pdf) == 1, "F09 PDF page count")
        for block in pdf[0].get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    x0,y0,x1,y1 = span["bbox"]
                    require(x0 >= 0 and y0 >= 0 and x1 <= pdf[0].rect.width and y1 <= pdf[0].rect.height, "F09 unclipped text "+span["text"])
    old = json.loads((HERE / "figures/publication_v1/S03_layout_v2/layout_revision.json").read_text())
    atlas = "figures/Nb3_complete_figure_atlas_v2.pdf"
    require(sha(HERE / atlas) == old["outputs"][atlas], "original 11-page atlas unchanged")
    for path in HERE.glob("scripts/1[89]_*.py"):
        ast.parse(path.read_text()); require(True, "syntax "+path.name)
    for path in HERE.glob("scripts/2[012]_*.py"):
        ast.parse(path.read_text()); require(True, "syntax "+path.name)
    text = (ROOT / "RESEARCH_QUESTIONS.md").read_text(encoding="utf-8")
    require(text.count('<a id="a22"></a>') == text.count('<a id="a23"></a>') == 1, "unique A22/A23 anchors")
    for oldname in ["A19_epithelial_identity_niche_response", "A20_slc34a2_transition_homeostasis"]:
        require(not (ROOT / "RQ_Specified" / oldname).exists(), "old folder absent "+oldname)
        require(oldname not in text, "old register path absent "+oldname)
    remote = subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=ROOT).decode().strip()
    correction = json.loads((HERE / "reports/RQ_ID_CORRECTION_2026-10-01.json").read_text())
    require(remote == correction["verified_remote_main"], "verified main commit preserved")
    remote_card = subprocess.check_output(["git", "show", "origin/main:RESEARCH_QUESTIONS.md"], cwd=ROOT).decode()
    for n in [19,20,21]:
        require(f"### A{n}. " in remote_card, f"main owns A{n}")
    require("### A22. " not in remote_card and "### A23. " not in remote_card, "no collision on checked main")
    sys.path.insert(0,str(ROOT / "analysis/scripts"))
    import validate_repository as v
    names = subprocess.check_output(["git", "diff", "--name-only", "--", "*.md"],cwd=ROOT).decode().splitlines()
    docs = {ROOT / x for x in names}
    docs.update(HERE.rglob("*.md"))
    docs.update((ROOT / "Research Article").glob("*/RQ_RETROSPECTIVE_REVIEW.md"))
    docs.update((ROOT / "RQ_Specified/A22_epithelial_identity_niche_response").rglob("*.md"))
    docs.update((ROOT / "RQ_Specified/A23_slc34a2_transition_homeostasis").rglob("*.md"))
    docs.add(ROOT / "RQ_Specified/A8_maturation_component_at1_contribution/RELATED_CANDIDATES_2026-10-01.md")
    docs.add(ROOT / "Research Article/Primary/README.md")
    docs.add(OUT.with_name("README.md"))
    docs = sorted(p for p in docs if p.is_file())
    v.markdown_files = lambda: docs
    links = v.Validation(); v.check_markdown_links(links)
    require(not links.failures, "changed Markdown links")
    whitespace = subprocess.run(["git", "-c", "core.safecrlf=false", "diff", "--check"],cwd=ROOT,capture_output=True)
    require(whitespace.returncode == 0, "git diff --check")
    result = {"status": "FAIL" if failures or links.failures else "PASS", "checks":checks,
              "failures":failures, "markdown_files":len(docs), "markdown_link_checks":links.checks,
              "markdown_link_failures":links.failures, "independent_xml_libraries":14,
              "selected_count_entries_verified":266, "scientific_scope":"descriptive only",
              "visual_QA":"F09 v2 visually inspected; left labels readable; PDF text bounds checked",
              "original_atlas_sha256":sha(HERE / atlas), "remote_main":remote,
              "full_repository_tests":"not repeated; old unrelated audit failures excluded; no old analysis rerun",
              "verifier_sha256":sha(Path(__file__))}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
