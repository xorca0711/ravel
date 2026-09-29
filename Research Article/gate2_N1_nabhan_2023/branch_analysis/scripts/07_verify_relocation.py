"""Check relocation integrity and path resolution without rerunning analyses."""
import ast
import csv
import json
from common import ROOT, REPO, PAPER, OUT, sha, now, historical_input, frozen_script

record=json.loads((ROOT/'metadata/relocation.json').read_text())
checks=[]
def check(name,value):
    checks.append(dict(name=name,passed=bool(value)))
    assert value,name

check('paper_location',ROOT==REPO/'Research Article/gate2_N1_nabhan_2023/branch_analysis')
check('paper_path',PAPER==REPO/'Research Article/gate2_N1_nabhan_2023')
check('no_premature_workspace',not (REPO/'RQ_Specified/Nb2_fzd_response_context').exists())
for relative,digest in record['preserved_files'].items():
    check('unchanged:'+relative,sha(ROOT/relative)==digest)
for relative,item in record['archived_scripts'].items():
    check('original_script:'+relative,sha(frozen_script(relative))==item['sha256'])
for item in json.loads((OUT/'contract.json').read_text())['input_files']:
    path=historical_input(item['path'])
    check('resolved_input:'+path.name,path.exists() and path.stat().st_size==item['bytes'])
for path in (ROOT/'scripts').glob('*.py'):
    ast.parse(path.read_text(encoding='utf-8'))
check('R_source_path',"paper<-dirname(root);repo<-dirname(dirname(paper))" in (ROOT/'scripts/01_gaona.R').read_text())
with (ROOT/'metadata/branch_registry.tsv').open(encoding='utf-8') as handle:
    records=list(csv.DictReader(handle,delimiter='\t'))
check('eight_paper_candidates',len(records)==8 and all((ROOT/item['card']).exists() for item in records))
for name in ['README.md','FIGURES.md']:
    check('RQ_index_clean:'+name,'Nb2_fzd_response_context' not in (REPO/'RQ_Specified'/name).read_text())
result=dict(checked_utc=now(),passed=len(checks),failed=0,checks=checks,
    scope='Relocation, preserved bytes, syntax and path resolution only; prior scientific verification remains unchanged')
(ROOT/'metadata/relocation_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS:',len(checks),'relocation checks;45 frozen artifacts unchanged;no scientific reanalysis')
