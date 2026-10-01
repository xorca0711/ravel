"""Render the E5 descriptive pilot separately from the frozen Nb3 atlas."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
RUN = HERE / "runs/E5_external_v1"
OUT = HERE / "figures/E5_external_v1"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        raise SystemExit("Refusing to overwrite E5 figure")
    palette_path = ROOT / "analysis/config/palette.json"
    palette = json.loads(palette_path.read_text())
    rec = json.loads((RUN / "run_record.json").read_text())
    for name, expected in rec["output_sha256"].items():
        assert sha(RUN / name) == expected
    effects = pd.read_csv(RUN / "gene_contrasts.tsv", sep="\t")
    values = pd.read_csv(RUN / "selected_normalized_values.tsv", sep="\t")
    design = pd.read_csv(RUN / "sample_design_qc.tsv", sep="\t")
    # v1 retained the GSM keys under pandas' default index-column name.
    assert design.columns[0] == "index" and design["index"].str.fullmatch(r"GSM\d+").all()
    design = design.rename(columns={"index": "GSM"})
    genes = ["IL6", "CXCL8", "CCL2", "CXCL10", "NFKBIA", "SOCS3"]
    at2 = ["SFTPC", "SFTPA1", "SFTPB", "ABCA3", "SLC34A2"]
    order = [("EGFR", "Cyto"), ("ERBB3", "Cyto"), ("EGFR", "IR"), ("ERBB3", "IR")]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 9,
                         "pdf.fonttype": 42, "svg.fonttype": "none", "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.8), gridspec_kw={"width_ratios": [1, 1.4, 1.1]})
    fig.subplots_adjust(left=.075, right=.94, bottom=.30, top=.85, wspace=.66)
    ax = axes[0]
    for i, (target, context) in enumerate(order):
        rows = effects[(effects.target == target) & (effects.context == context) & (effects.gene == target)]
        primary = float(rows.loc[rows.normalization == "CPM", "effect"].iloc[0])
        sensitivity = float(rows.loc[rows.normalization != "CPM", "effect"].iloc[0])
        ax.plot([primary, sensitivity], [i, i], color="0.65", linewidth=1)
        ax.scatter(primary, i, color=palette.get("ink", "#263238"), s=24, zorder=3)
        ax.scatter(sensitivity, i, facecolors="white", edgecolors=palette.get("ink", "#263238"), marker="s", s=18, zorder=3)
    ax.axvline(0, color="0.75", linestyle="--", linewidth=.6)
    ax.set_yticks(range(4), [f"{t} / {c}" for t,c in order]); ax.invert_yaxis()
    ax.set_xlabel("Target RNA contrast\nmean log2(abundance + 1)")
    ax.set_title("A  Target-transcript response", loc="left")
    cmap = LinearSegmentedColormap.from_list("e5_signed", [palette["categorical"]["1"], palette["surface"], palette["categorical"]["2"]])
    mat = np.array([[effects[(effects.normalization == "CPM") & (effects.target == t) & (effects.context == c) & (effects.gene == g)].effect.iloc[0] for t,c in order] for g in genes])
    ax = axes[1]
    im = ax.imshow(mat, cmap=cmap, vmin=-1.5, vmax=1.5, aspect="auto")
    ax.set_yticks(range(len(genes)), genes)
    ax.set_xticks(range(4), [f"{t}\n{c}" for t,c in order], rotation=45, ha="right")
    ax.set_title("B  Inflammatory markers", loc="left")
    for i in range(6):
        for j in range(4):
            ax.text(j,i,f"{mat[i,j]:+.2f}",ha="center",va="center",fontsize=6.5,color="white" if abs(mat[i,j])>1.05 else "black")
    fig.colorbar(im, ax=ax, fraction=.05, pad=.05, label="Target minus matched control")
    controls = design[design.target == "control"].copy()
    fractions = []
    for gene in at2:
        fractions.append([values[(values.normalization == "CPM") & (values.gene == gene) & values.GSM.isin(controls[controls.context == c].GSM)].detected_ge1.mean() for c in ["NoIR", "Cyto", "IR"]])
    ax = axes[2]
    ax.imshow(fractions, vmin=0, vmax=1, cmap="Greys", aspect="auto")
    ax.set_yticks(range(5), at2)
    ax.set_xticks(range(3), ["NoIR", "Cyto", "IR"])
    ax.set_title("C  AT2-marker coverage", loc="left")
    for i in range(5):
        for j in range(3):
            ax.text(j,i,f"{round(2*fractions[i][j])}/2",ha="center",va="center",fontsize=7,color="white" if fractions[i][j]>.6 else "black")
    ax.set_xlabel("Control libraries with CPM ≥ 1")
    fig.text(.075,.10,"GSE306184 · 14 libraries; donor independence unresolved. Cyto is the deposited label.\nFilled circle: CPM; open square: normalization sensitivity. No biological confidence intervals or pathway inference.",fontsize=7)
    OUT.mkdir(parents=True)
    for suffix in ["png", "pdf", "svg"]:
        fig.savefig(OUT / f"Nb3_F09_E5_external_pilot.{suffix}", dpi=300, facecolor="white")
    plt.close(fig)
    receipt = {"script_sha256":sha(Path(__file__)), "palette_sha256":sha(palette_path),
               "source_record_sha256":sha(RUN / "run_record.json"), "outputs":{p.name:sha(p) for p in OUT.iterdir()},
               "size_inches":[9.2,3.8],"dpi":300,"old_atlas_unchanged":True}
    (OUT / "render_record.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("F09: PNG, PDF, SVG; existing atlas unchanged")


if __name__ == "__main__":
    main()
