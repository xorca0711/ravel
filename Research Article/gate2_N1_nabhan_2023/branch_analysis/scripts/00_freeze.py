import argparse
import json
from common import ROOT, REPO, PAPER, OUT, CONFIG, sha, now

p=argparse.ArgumentParser();p.add_argument('--data-root',required=True);args=p.parse_args()
from pathlib import Path
base=Path(args.data_root)
assert not (OUT/'contract.json').exists()
files=[ROOT/'config/extension_v1.json',PAPER/'raw/GSE327565_raw_counts_GEO_YapTaz.csv.gz',
 REPO/'RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE327565.json',
 PAPER/'trials/bulk_v1/tables/normalized_log2CPM.tsv',PAPER/'trials/bulk_v1/tables/gene_effects.tsv.gz',
 PAPER/'metadata/samples.tsv',PAPER/'trials/bulk_v1/contract.json',PAPER/'trials/atlas_v1/contract.json',
 base/'raw_data/msigdb/mh.all.v2024.1.Mm.symbols.gmt',
 base/'Research Article/gate1_01_niethamer_2025/GSE262927/processed/final_clustered.h5ad',
 base/'Research Article/gate1_01_niethamer_2025/GSE262927/myeloid_focus/batch_sensitivity/tables/sample_infection_round.csv']
record=dict(frozen_utc=now(),config=CONFIG,input_files=[dict(path=str(f),bytes=f.stat().st_size,sha256=sha(f)) for f in files],
 scripts={str(f.relative_to(ROOT)):sha(f) for f in (ROOT/'scripts').glob('*') if f.is_file()},
 code_status='Analysis and figure scripts hashed again at completion; contract settings never changed silently')
(OUT/'contract.json').write_text(json.dumps(record,indent=2)+'\n')
print('Frozen',len(files),'inputs')
