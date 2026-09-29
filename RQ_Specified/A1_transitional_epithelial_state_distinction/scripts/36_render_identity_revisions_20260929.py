"""Versioned presentation revisions from saved tables; no scientific analyses rerun.

The 25 September identity closures supersede labels in the older HPCS and
CD44 displays. Historical images, scripts, numerical tables and run records
remain untouched. Mouse identity recovery does not remove library/chase aliasing.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "figures/revision_20260929"
INPUTS, OUTPUTS = {}, {}
plt.rcParams.update({"font.size": 9, "svg.fonttype": "none",
                     "svg.hashsalt": "a1-identity-revision-20260929",
                     "axes.spines.top": False, "axes.spines.right": False})


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(relative):
    path = BASE / relative
    INPUTS[relative] = digest(path)
    return pd.read_csv(path, sep="\t")


def save(fig, stem):
    for ext in ("png", "svg"):
        path = OUT / f"{stem}.{ext}"
        fig.savefig(path, dpi=200, bbox_inches="tight",
                    **({"metadata": {"Date": None}} if ext == "svg" else {}))
        if ext == "svg":
            path.write_text("\n".join(s.rstrip() for s in path.read_text().splitlines()) + "\n",
                            encoding="utf-8")
        OUTPUTS[path.relative_to(BASE).as_posix()] = digest(path)
    plt.close(fig)


def hpcs(crosswalk, groups):
    table = read("tables/hpcs_source_composition/source_state_counts.tsv")
    manifest = read("tables/hpcs_source_composition/source_manifest.tsv")
    assert len(crosswalk) == 22 and crosswalk.mouse_tag.is_unique
    assert crosswalk.source_label.is_unique and manifest.source_label.is_unique
    assert set(table.source_label) == set(crosswalk.source_label) == set(manifest.source_label)
    indexed = crosswalk.set_index("source_label")
    counts = table.groupby("source_label").numerator.sum().sort_index()
    pd.testing.assert_series_equal(counts, indexed.retained_cells.sort_index(), check_names=False)
    assert counts.sum() == 5333
    np.testing.assert_allclose(table.groupby("source_label").fraction.sum(), 1)
    states = ["HPCS", "AT1-like", "AT2-like", "Lung endoderm-like", "Hybrid lung/gastric-like",
              "Highly proliferative", "EMT", "Ribosome"]
    colors = ["#a64e80", "#4b9c85", "#447da8", "#caa044", "#8165a3", "#db7859", "#78816d", "#b6b8bb"]
    fig, axes = plt.subplots(3, 2, figsize=(13, 11), sharey=True)
    for ax, (group, info) in zip(axes.flat, groups.items()):
        pivot = table[table.group.eq(group)].pivot(index="source_label", columns="state", values="fraction")[states]
        bottom = np.zeros(len(pivot))
        for state, color in zip(states, colors):
            ax.bar(range(len(pivot)), pivot[state], bottom=bottom, color=color, label=state, width=.72)
            bottom += pivot[state].to_numpy()
        labels = [f"{indexed.loc[s, 'mouse_tag']}\nN={indexed.loc[s, 'retained_cells']}" for s in pivot.index]
        ax.set_xticks(range(len(pivot)), labels)
        ax.set(ylim=(0, 1), ylabel="Fraction of retained cells in each mouse")
        ax.set_title(f"{info['driver']} | {info['chase_days']}-day chase | {group}")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(.5, .94), ncol=4, frameon=False)
    fig.suptitle("HPCS tracing: descendant RNA-state composition in 22 verified mice", fontsize=15, y=.98)
    fig.text(.5, .025, "Exact animal tags and library/driver crosswalk verified; N = retained traced cells per mouse.\n"
             "Chase and source library remain confounded; current mScarlet is unavailable. No transition rates or temporal p-values.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .075, 1, .875))
    save(fig, "a1_hpcs_source_composition")

    summary = read("tables/robustness_2026-09-25/hpcs/group_influence_summary.tsv")
    partitions = read("tables/robustness_2026-09-25/hpcs/partition_agreement.tsv")
    read("tables/robustness_2026-09-25/hpcs/design_rank_audit.tsv")
    d = summary.query("annotation == 'cell type' and category == 'HPCS'").set_index("group").loc[list(groups)]
    assert d.sources.to_dict() == crosswalk.groupby("group").size().to_dict()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    y = np.arange(len(d))
    for offset, name, color in [(-.1, "equal", "#235789"), (.1, "pooled", "#c96a2b")]:
        center = d["equal_source" if name == "equal" else "cell_pooled"] * 100
        axes[0].hlines(y + offset, d[f"loo_{name}_min"] * 100, d[f"loo_{name}_max"] * 100, color=color, lw=2)
        axes[0].scatter(center, y + offset, c=color, label="Equal-mouse" if name == "equal" else "Cell-pooled", s=35, zorder=3)
    axes[0].set_yticks(y, d.index)
    axes[0].invert_yaxis()
    axes[0].set(xlabel="Author HPCS label (% of retained cells)", title="Leave-one-mouse-out sensitivity")
    axes[0].legend(loc="lower right", frameon=False)
    d = partitions.query("level == 'group'").copy()
    d["pair"] = d.left + " / " + d.right
    matrix = d.pivot(index="unit", columns="pair", values="adjusted_rand").reindex(list(groups))
    matrix = matrix[["cell type / clusterK12", "cell type / clusterK12_stringent", "clusterK12 / clusterK12_stringent"]]
    im = axes[1].imshow(matrix.to_numpy(), vmin=-1, vmax=1, cmap="coolwarm", aspect="auto")
    axes[1].set_xticks(range(3), ["State / K12", "State / stringent", "K12 / stringent"], rotation=20, ha="right")
    axes[1].set_yticks(y, matrix.index)
    axes[1].set_title("Partition agreement (ARI)")
    for (i, j), value in np.ndenumerate(matrix.to_numpy()):
        axes[1].text(j, i, f"{value:.2f}", ha="center", va="center")
    fig.colorbar(im, ax=axes[1], fraction=.04, pad=.02)
    fig.suptitle("HPCS: mouse influence and annotation agreement", fontsize=15)
    fig.text(.5, .025, "22 source labels now map to 22 distinct mice. Bars are omission ranges, not confidence intervals.\n"
             "Related labels are not independent validation; chase and unrestricted source-library effects remain inseparable.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .13, 1, .93))
    save(fig, "a1_hpcs_robustness")


def deposited_pca():
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5))
    identity = read("tables/evidence_closure/cd44_sample_manifest.tsv")
    assert identity.sample_id.is_unique and len(identity) == 16
    assert identity.groupby(["genotype", "mouse"]).size().eq(2).all()
    for ax, accession, label in zip(axes, ["GSE154966", "GSE273123"], ["TIGIT ATAC", "CD44 RNA"]):
        meta = read(f"tables/descriptive/{accession}_source_PCA_QC.tsv")
        var = read(f"tables/descriptive/{accession}_PCA_variance.tsv").variance_fraction
        if accession == "GSE273123":
            meta = meta.merge(identity[["sample_id", "mouse", "genotype"]], on="sample_id", validate="one_to_one")
            assert len(meta) == 16 and meta.mouse.nunique() == 8
            key = "mouse"
        else:
            key = "source_alias"
        for _, block in meta.groupby(key):
            ax.plot(block.PC1, block.PC2, color="#CBCFD2", lw=.8, zorder=1)
        for gate, color, marker in [("Neg", "#64717C", "o"), ("Pos", "#AA5B8A", "^")]:
            g = meta[meta.sort_gate.eq(gate)]
            ax.scatter(g.PC1, g.PC2, c=color, marker=marker, label=gate, s=45, zorder=2)
        ax.set(xlabel=f"PC1 ({var.iloc[0]:.1%})", ylabel=f"PC2 ({var.iloc[1]:.1%})", title=f"{accession} | {label}")
        ax.legend(frameon=False, fontsize=9)
    axes[0].text(.5, -.24, "Lines join source aliases; ATAC pool independence unresolved", transform=axes[0].transAxes, ha="center", fontsize=8)
    axes[1].text(.5, -.24, "Lines join verified mice; 4 paired WT and 4 paired mutant mice", transform=axes[1].transAxes, ha="center", fontsize=8)
    fig.suptitle("Deposited-count PCA with current source-identity evidence", fontsize=14)
    fig.text(.5, .025, "Original CPM/log2 coordinates and selected features retained; PCA is descriptive, with no significance test.\n"
             "CD44 mouse/genotype mapping is resolved; TIGIT pool membership remains unavailable.", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .17, 1, .93))
    save(fig, "a1_deposited_source_PCA")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    preserved = [BASE / "scripts" / name for name in ["09_descriptive_input_audit.py", "10_render_audited_figures.py",
                  "21_reconstruct_hpcs_source_composition.py", "23_analyze_hpcs_robustness.py"]]
    for stem in ["hpcs_source_composition/a1_hpcs_source_composition", "robustness_2026-09-25/a1_hpcs_robustness", "a1_deposited_source_PCA"]:
        preserved.extend(BASE / "figures" / f"{stem}.{ext}" for ext in ("png", "svg"))
    original = {p.relative_to(BASE).as_posix(): digest(p) for p in preserved}
    cfg = BASE / "config/hpcs_descendant_reconstruction.json"
    INPUTS[cfg.relative_to(BASE).as_posix()] = digest(cfg)
    groups = json.loads(cfg.read_text())["groups"]
    hpcs(read("tables/regulatory_fate/hpcs_mouse_crosswalk.tsv"), groups)
    deposited_pca()
    assert all(digest(BASE / p) == h for p, h in {**original, **INPUTS}.items())
    record = {"scope": "Three identity-label presentation revisions; unchanged scientific tables and coordinates",
              "generated_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": digest(Path(__file__)),
              "input_sha256": INPUTS, "preserved_historical_sha256": original, "output_sha256": OUTPUTS,
              "checks": ["22 unique HPCS mice; exact retained-cell totals; 5333 cells", "Group mouse counts match omission summaries",
                         "16 CD44 samples join uniquely to 8 paired mice", "All input and historical artifact hashes unchanged"]}
    (OUT / "run_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("Rendered three presentation revisions; input tables and historical outputs unchanged.")


if __name__ == "__main__":
    main()
