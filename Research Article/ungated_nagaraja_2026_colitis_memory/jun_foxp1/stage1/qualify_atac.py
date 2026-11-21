"""Resolve full native export coverage against the frozen locus and source inventories."""
import sys
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
from native_atac import audit

def main(out):
    prior=Path("analysis/research/runs/ng26_jf_methylation_v1")
    windows=pd.read_csv(prior/"mm10_windows.tsv",sep="\t")
    assert len(windows)==63*7 and windows.applicable.dtype==bool
    with ZipFile(prior/"stage1_sources.zip") as bundle:
        audit(out,bundle,windows)

if __name__=="__main__":
    main(Path(sys.argv[1]))
