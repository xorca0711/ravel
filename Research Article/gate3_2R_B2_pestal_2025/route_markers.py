"""Report the frozen Han marker correspondence in deposited transfer libraries."""
import argparse
from pathlib import Path

import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("output", type=Path)
args = parser.parse_args()
source = Path("analysis/research/runs/pestal_transfer_v1/markers.tsv")
markers = pd.read_csv(source, sep="\t", index_col="gene")
genes = ["Nt5e", "Lyve1", "Timd4", "Gata6", "Icam2"]
columns = ["WT_KO_day0", "WT_KO_day7", "day7_minus_day0"]
columns.extend(markers.filter(regex="^KLF2").columns)
result = markers.loc[genes, columns]
if result.isna().any().any():
    raise ValueError("A frozen route marker is missing a required measurement")
result.to_csv(args.output / "route_markers.tsv", sep="\t", index_label="gene")
