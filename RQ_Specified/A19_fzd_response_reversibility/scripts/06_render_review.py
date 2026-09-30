"""Rasterize exported PDFs into ignored cache for visual review; no data edits."""
from pathlib import Path
import pymupdf
B=Path(__file__).resolve().parents[1]
out=B/'cache/figure_review';out.mkdir(exist_ok=True)
for p in sorted((B/'figures/exploratory_v1').glob('*.pdf')):
    d=pymupdf.open(p)
    assert len(d)==1
    d[0].get_pixmap(matrix=pymupdf.Matrix(1.6,1.6)).save(out/(p.stem+'.png'))
    d.close()
print('Rendered four exported PDFs for visual review.')
