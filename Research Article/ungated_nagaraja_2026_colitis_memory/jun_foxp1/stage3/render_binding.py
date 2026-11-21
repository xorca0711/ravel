"""Re-export the saved binding figure with room for all legends."""
from pathlib import Path
import json
import sys

import matplotlib as mpl
import pandas as pd
import pymupdf

from figures import binding_figure


def main(out):
    source = Path("analysis/research/runs/ng26_jf_association_v1")
    tables = [pd.read_csv(source / n, sep="\t") for n in ["associations.tsv", "locus_pairs.tsv.gz", "omission_ranges.tsv"]]
    with mpl.rc_context({"savefig.bbox": "tight", "savefig.pad_inches": .20}):
        binding_figure(*tables, out)
    with pymupdf.open(out / "binding_associations.pdf") as doc:
        page = doc[0]
        spans = [s for b in page.get_text("dict")["blocks"] if b["type"] == 0 for l in b["lines"] for s in l["spans"]]
        assert all(page.rect.contains(pymupdf.Rect(s["bbox"])) for s in spans)
        assert all(s["color"] == 0 for s in spans)
        fonts = sorted({s["font"] for s in spans})
        assert fonts == ["DejaVuSans", "DejaVuSans-Bold"]
        text = " ".join(page.get_text().split())
        for legend in ["Raw difference", "Paired fold", "Omit one locus", "Omit one mouse/line"]:
            assert legend in text
        checks = dict(all_text_inside_page=True, all_text_black=True, fonts=fonts,
                      page_width_pt=page.rect.width, page_height_pt=page.rect.height,
                      visible_text_spans=len(spans))
    (out / "render_checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
