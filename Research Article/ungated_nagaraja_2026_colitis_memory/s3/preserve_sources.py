"""Archive, without conversion, the four frozen source tables used by S3."""
from pathlib import Path
from shutil import copyfile
import sys

source = Path(__file__).resolve().parent / "source"
for name in ("ed6_tissue_slices.tsv", "ed6_tissue_sources.tsv",
             "thbs1_track_slices.tsv", "thbs1_track_sources.tsv"):
    copyfile(source / name, Path(sys.argv[1]) / name)
