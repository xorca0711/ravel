"""Qualify Table 6 coordinates and actual native methylation track coverage."""
from pathlib import Path
import hashlib
import shutil
import sys
from zipfile import ZipFile

import pandas as pd
from methylation import geometry,methylation,write

def main(out):
    path=Path("raw_data/nagaraja_jf1/stage1_sources.zip")
    with ZipFile(path) as bundle:
        with bundle.open("source_manifest.tsv") as stream:
            manifest=pd.read_csv(stream,sep="\t")
        assert len(manifest)==len(bundle.namelist())-1 and manifest.member.is_unique
        for item in manifest.itertuples(index=False):
            content=bundle.read(item.member)
            assert len(content)==item.bytes and hashlib.sha256(content).hexdigest()==item.sha256
        regions,windows,sites=geometry(bundle)
        write(out,"binding_panel.tsv",regions)
        write(out,"mm10_windows.tsv",windows)
        methylation(out,bundle,regions,windows,sites)
    shutil.copyfile(path,out/path.name)

if __name__=="__main__":
    main(Path(sys.argv[1]))
