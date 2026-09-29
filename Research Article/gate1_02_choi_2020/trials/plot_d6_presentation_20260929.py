#!/usr/bin/env python
"""Replot tracked D6 means with correct scale/units and readable headings."""
from pathlib import Path
import hashlib
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "d6_programmes" / "revision_20260929"
PROGRAMMES = ["p53", "arrest", "hypoxia", "hypoxia_without_Ndrg1", "ifng_response", "glycolysis"]


def main():
    OUT.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), constrained_layout=True)
    inputs = []
    for ax, label in zip(axes, ["invivo", "organoid"]):
        path = HERE / "d6_programmes" / f"d6_scores_{label}.csv"
        inputs.append(path)
        table = pd.read_csv(path).set_index("state")
        means = table[["score_" + p for p in PROGRAMMES]]
        scaled = (means - means.min()) / (means.max() - means.min() + 1e-12)
        im = ax.imshow(scaled, aspect="auto", cmap="Blues", vmin=0, vmax=1)
        ax.set_xticks(range(len(PROGRAMMES)), [p.replace("_", " ") for p in PROGRAMMES], rotation=40, ha="right", fontsize=8)
        ax.set_yticks(range(len(table)), [f"{state} ({int(table.loc[state, 'n']):,} cells)" for state in table.index], fontsize=9)
        for i in range(len(table)):
            for j in range(len(PROGRAMMES)):
                ax.text(j, i, f"{means.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8,
                        color="white" if scaled.iloc[i, j] > .6 else "black")
        ax.set_title("In vivo" if label == "invivo" else "Organoid", fontsize=12)
    fig.suptitle("D6 | Mean program scores by assigned state\nColor: each program column scaled across states within each dataset. Text: raw mean score.\nCounts are cells; the display does not estimate uncertainty across animals or preparations.", fontsize=10)
    fig.colorbar(im, ax=axes, label="Within-program scaled mean (0–1)", shrink=.72, pad=.025)
    path = OUT / "d6_programme_scores.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    record = {"scope": "Presentation only; original scores and trial files preserved.",
              "inputs_sha256": {p.name: digest(p) for p in inputs},
              "script_sha256": digest(Path(__file__)), "outputs_sha256": {path.name: digest(path)}}
    (OUT / "figure_run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("Rendered one versioned D6 correction from tracked means.")


if __name__ == "__main__":
    main()
