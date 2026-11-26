"""Render the four published Ravel PDF figures for the Mu Markdown gallery."""
from pathlib import Path
import sys

import pymupdf


def main(output):
    runs = Path(__file__).resolve().parents[2] / "analysis/research/runs"
    figures = {
        "mu2026_s1_v1/source_values.pdf": "cytokine_recall.png",
        "mu2026_s2_v1/source_values.pdf": "aging_and_liver.png",
        "mu2026_s3_v1/source_values.pdf": "transfer_and_physiology.png",
        "mu2026_s4_rna_figure_v1/hsc_library_counts.pdf": "hsc_rna.png",
    }
    print(f"PyMuPDF {pymupdf.VersionBind}, RGB, 144 dpi")
    for source, filename in figures.items():
        with pymupdf.open(runs / source) as document:
            if len(document) != 1:
                raise ValueError(f"Expected one figure page in {source}")
            page = document[0]
            image = page.get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
            image.save(output / filename)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
