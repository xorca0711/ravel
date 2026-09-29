#!/usr/bin/env python
"""Versioned presentation-only corrections from tracked C11/E5 source tables.

Original trial figures, summaries, records and scientific tables remain unchanged.
Run this script from any directory; it only writes revision_20260929/.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "revision_20260929"


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    c11 = load("cardoso_c11_review", "c11_figures_for_the_contradictions.py")
    c5 = load("cardoso_c5_review", "c5_figures_for_the_three_findings.py")
    e5 = load("cardoso_e5_review", "e5_figure_for_the_refutation.py")
    c5.OUT = OUT
    retention = HERE / "c5_figures_for_the_three_findings/c5_fibrotic_retention.csv"
    c5.V.apply(plt)
    c5.figure_fibrotic(pd.read_csv(retention), plt)
    c11.OUT = OUT
    c11.V.apply(plt)
    for function in (c11.fig1_depth_control, c11.fig2_c7_resolution, c11.fig3_c8_amplitudes,
                     c11.fig4_species, c11.fig5_c9, c11.fig6_c10):
        function(plt)
    table = e5.OUT / "e5_retention_against_injury.csv"
    e5.render_figure(pd.read_csv(table), plt, OUT / "e5_retention_against_injury.png")
    sources = list(c11.SRC.values()) + [table, retention]
    scripts = [Path(__file__), HERE / "c5_figures_for_the_three_findings.py", HERE / "c11_figures_for_the_contradictions.py",
               HERE / "e5_figure_for_the_refutation.py", HERE / "viz_style.py"]
    record = {
        "scope": "Presentation only: scoped claims and unit/uncertainty wording; no scientific fits or values changed.",
        "preserved": "Original C11 and E5 images, trial records, tables and summaries.",
        "inputs_sha256": {p.relative_to(HERE).as_posix(): digest(p) for p in sources},
        "scripts_sha256": {p.name: digest(p) for p in scripts},
        "outputs_sha256": {p.name: digest(p) for p in sorted(OUT.glob("*.png"))},
    }
    (OUT / "figure_run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Rendered {len(record['outputs_sha256'])} versioned figure corrections from tracked tables.")


if __name__ == "__main__":
    main()
