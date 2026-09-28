#!/usr/bin/env python3
"""Plot A10 follow-up per-plate held-out performance from the tracked table.

Run from the repository root:

    python RQ_Specified/A10_organoid_growth_outcome/scripts/plot_followup_plate_performance.py

Reads only the tracked follow-up table
`RQ_Specified/A10_organoid_growth_outcome/tables/followup_v1/model_absolute_performance.tsv`
and writes the figure plus a run record. No model is fitted and no value is
recomputed from raw data: every plotted number is a cell of that table.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

A10 = Path("RQ_Specified/A10_organoid_growth_outcome")
TABLE = A10 / "tables/followup_v1/model_absolute_performance.tsv"
PNG = A10 / "figures/A10_F_followup_plate_performance.png"
RUN = A10 / "figures/A10_F_followup_plate_performance.run.json"

SETTING = "primary"
SCALE = "inherited_log2"
COMPARATOR = "baseline+proliferation"
GROWTH = "baseline+proliferation+remaining_growth"
PLATES = ["plate1", "plate2", "plate3", "plate4"]

COL_COMPARATOR = "#9aa7b4"
COL_GROWTH = "#1f6f8b"
GREY = "#4d4d4d"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load() -> pd.DataFrame:
    df = pd.read_csv(TABLE, sep="\t")
    sel = df[(df["setting"] == SETTING) & (df["scale"] == SCALE)
             & (df["model"].isin([COMPARATOR, GROWTH]))]
    sel = sel[sel["plate"].isin(PLATES)]
    assert len(sel) == 8, f"expected 8 rows, got {len(sel)}"
    assert sel.duplicated(["plate", "model"]).sum() == 0, "duplicate plate/model rows"
    return sel.set_index(["model", "plate"])


def series(sel: pd.DataFrame, model: str, column: str) -> np.ndarray:
    return np.array([sel.loc[(model, p), column] for p in PLATES], dtype=float)


def main() -> None:
    sel = load()
    wells = [int(sel.loc[(GROWTH, p), "wells"]) for p in PLATES]
    rmse_c = series(sel, COMPARATOR, "rmse")
    rmse_g = series(sel, GROWTH, "rmse")
    r2_c = series(sel, COMPARATOR, "r2_against_heldout_mean")
    r2_g = series(sel, GROWTH, "r2_against_heldout_mean")

    assert (rmse_g < rmse_c).all(), "panel a title asserts lower error on all four plates"
    assert (r2_g < 0).sum() == 3, "panel b title asserts negative R-squared on three plates"

    plt.rcParams.update({
        "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
        "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 7,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": GREY, "text.color": GREY, "axes.labelcolor": GREY,
        "xtick.color": GREY, "ytick.color": GREY, "figure.dpi": 300,
        "savefig.dpi": 300, "font.family": "DejaVu Sans",
    })

    x = np.arange(len(PLATES), dtype=float)
    labels = [f"Plate {p[-1]}\n{n} wells" for p, n in zip(PLATES, wells)]
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(7.2, 3.4))

    for ax, lo, hi in ((axa, rmse_g, rmse_c), (axb, r2_c, r2_g)):
        ax.vlines(x, lo, hi, color="#c8cfd6", linewidth=1.4, zorder=1)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlim(-0.5, len(PLATES) - 0.5)

    axa.plot(x, rmse_c, "o", color=COL_COMPARATOR, markersize=7,
             markeredgecolor="white", markeredgewidth=0.6, zorder=3,
             label="E2F/G2M comparator (baseline + 2 scores)")
    axa.plot(x, rmse_g, "o", color=COL_GROWTH, markersize=7,
             markeredgecolor="white", markeredgewidth=0.6, zorder=3,
             label="Six-score growth block (baseline + 6 scores)")
    axa.set_ylabel("Held-out root mean squared error\n(log2 deposited area scale)")
    axa.set_title("Adding the four remaining growth scores lowers\nheld-out error on every plate", loc="left")
    axa.set_ylim(0.025, 0.064)
    axa.text(0.02, 0.02, "lower = better", transform=axa.transAxes,
             fontsize=6, color=GREY, ha="left", va="bottom")
    axa.legend(frameon=False, loc="upper right", handletextpad=0.3,
               bbox_to_anchor=(1.02, 1.0))

    axb.axhline(0.0, color=GREY, linewidth=0.8, linestyle=(0, (4, 3)), zorder=2)
    axb.plot(x, r2_c, "o", color=COL_COMPARATOR, markersize=7,
             markeredgecolor="white", markeredgewidth=0.6, zorder=3)
    axb.plot(x, r2_g, "o", color=COL_GROWTH, markersize=7,
             markeredgecolor="white", markeredgewidth=0.6, zorder=3)
    axb.set_ylabel("R-squared against the held-out plate mean")
    axb.set_title("Yet the six-score block still predicts worse than that\nplate's own mean on three of four plates", loc="left")
    axb.set_ylim(-9.8, 1.8)
    axb.text(0.02, 0.98, "higher = better; 0 = held-out plate mean",
             transform=axb.transAxes, fontsize=6, color=GREY, ha="left", va="top")
    for xi, val in zip(x, r2_g):
        axb.annotate(f"{val:.3f}", (xi, val), textcoords="offset points",
                     xytext=(0, 9), ha="center", fontsize=7, color=COL_GROWTH)

    for ax, letter in ((axa, "a"), (axb, "b")):
        ax.text(-0.24, 1.06, letter, transform=ax.transAxes, fontsize=11,
                fontweight="bold", color="black", ha="left", va="bottom")

    fig.tight_layout(w_pad=2.6)
    PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG, bbox_inches="tight")
    plt.close(fig)

    script = Path(__file__).resolve()
    record = {
        "figure": PNG.as_posix(),
        "script": "RQ_Specified/A10_organoid_growth_outcome/scripts/plot_followup_plate_performance.py",
        "script_sha256": sha256(script),
        "inputs": [{"path": TABLE.as_posix(), "sha256": sha256(TABLE)}],
        "selection": {"setting": SETTING, "scale": SCALE,
                      "models": [COMPARATOR, GROWTH], "plates": PLATES},
        "plotted_values": {
            "wells": dict(zip(PLATES, wells)),
            "rmse": {COMPARATOR: dict(zip(PLATES, rmse_c.tolist())),
                     GROWTH: dict(zip(PLATES, rmse_g.tolist()))},
            "r2_against_heldout_mean": {COMPARATOR: dict(zip(PLATES, r2_c.tolist())),
                                        GROWTH: dict(zip(PLATES, r2_g.tolist()))},
        },
        "matplotlib": matplotlib.__version__,
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "generated_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "note": "Presentation of tracked follow-up values only; no model was fitted or rescored.",
    }
    RUN.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(PNG.as_posix())
    print(RUN.as_posix())


if __name__ == "__main__":
    main()
