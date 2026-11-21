"""Source-figure diagnostic, using physical tick positions and individual vector symbols."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pymupdf
from scipy.stats import ttest_ind

PDF = Path("raw_data/nagaraja_s0/article.pdf")
RUN = Path("analysis/research/runs/ng26_s2_v1")


def extract():
    doc = pymupdf.open(PDF)
    page = doc[3]
    bounds = pymupdf.Rect(170, 365, 266, 490)
    drawings = [d for d in page.get_drawings() if bounds.contains(d["rect"])]
    ticks = sorted(d["rect"].y0 for d in drawings if d["type"] == "s"
                   and abs(d["rect"].x1 - 202.735) < .02 and abs(d["rect"].width - 1.57) < .02)
    assert len(ticks) == 7
    y0, scale = ticks[3], (ticks[5]-ticks[1])/2  # zero, then points per score from +/-1 ticks

    def to_score(y):
        return (y0-y)/scale

    points, crossbars = [], {}
    for path in drawings:
        rect = path["rect"]
        x, y = (rect.x0+rect.x1)/2, (rect.y0+rect.y1)/2
        history = "Control" if x < 228 else "Colitis"
        if path["type"] == "fs" and [i[0] for i in path["items"]] == ["c"]*4:
            assert 1.8 < rect.width < 2.3 and 1.8 < rect.height < 2.3
            points.append(dict(history=history, pdf_x_pt=x, pdf_y_pt=y, pdf_score=to_score(y)))
        elif path["type"] == "s" and abs(rect.width-11.332) < .02 and rect.height < .01:
            assert history not in crossbars
            crossbars[history] = to_score(y)
    assert len(points) == 123 and len(crossbars) == 2
    return pd.DataFrame(points), crossbars


def main(out):
    points, crossbars = extract()
    clones = pd.read_csv(RUN/"fos_clones.tsv", sep="\t").query("variant == 'released'")
    rows, matches = [], []
    for history, group in points.groupby("history"):
        source = group.sort_values("pdf_score").reset_index(drop=True)
        for minimum in (1, 5):
            r = clones.loc[(clones["sample"] == history) & (clones.n >= minimum)].sort_values("fos_median")
            row = dict(history=history, minimum=minimum, glyphs=len(source), released_clones=len(r),
                       pdf_crossbar=crossbars[history], released_median=r.fos_median.median())
            if len(source) == len(r):
                raw = r.fos_median.to_numpy()
                clipped = raw.clip(-1.5,1.5)
                source = source.assign(rank=np.arange(1,len(source)+1), reference_sorted_clone=r.clone.to_numpy(),
                                       released_score=raw, display_capped_score=clipped)
                source["pdf_minus_capped"] = source.pdf_score-clipped
                matches.append(source)
                row.update(max_abs_score_error=source.pdf_minus_capped.abs().max(),
                           median_abs_score_error=source.pdf_minus_capped.abs().median())
            rows.append(row)
    joined = pd.concat(matches,ignore_index=True)
    assert len(joined) == len(points)
    tests = []
    for col in ("released_score","display_capped_score","pdf_score"):
        control = joined.loc[joined.history.eq("Control"),col]
        colitis = joined.loc[joined.history.eq("Colitis"),col]
        tests.append(dict(values=col,n_control=len(control),n_colitis=len(colitis),
                          welch_p=ttest_ind(colitis,control,equal_var=False).pvalue,
                          pooled_p=ttest_ind(colitis,control,equal_var=True).pvalue))
    for name, table in [("panel_counts",pd.DataFrame(rows)),("ranked_glyphs",joined),("panel_tests",pd.DataFrame(tests))]:
        table.to_csv(out/(name+".tsv"),sep="\t",index=False,float_format="%.15g",na_rep="NA",lineterminator="\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
