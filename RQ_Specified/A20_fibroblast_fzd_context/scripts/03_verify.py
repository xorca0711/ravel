"""Independent table arithmetic, eligibility, export, and preservation checks."""
from pathlib import Path
import csv,hashlib,json,math,statistics
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
def read(name):
 with (BASE/'tables'/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=0
def check(ok,label):
 global checks
 if not ok:raise AssertionError(label)
 checks+=1
cfg=json.loads((BASE/'config/exploratory_v1.json').read_text());expr=read('unit_expression.tsv');lookup={}
for r in expr:
 check(int(r['counts'])>=0 and int(r['counts'])<=int(r['total_umi']),'count bounds')
 cpm=int(r['counts'])/int(r['total_umi'])*1e6
 check(math.isclose(float(r['cpm']),cpm,rel_tol=1e-10,abs_tol=1e-9),'CPM')
 check(math.isclose(float(r['log2cpm']),math.log2(cpm+1),rel_tol=1e-10,abs_tol=1e-9),'log2')
 check(math.isclose(float(r['detection']),int(r['detected_cells'])/int(r['cells']),abs_tol=1e-10),'detection')
 key=(r['mode'],r['unit'],r['state'],r['gene']);check(key not in lookup,'unique observation');lookup[key]=r
features={}
for r in read('unit_features.tsv'):
 key=(r['mode'],r['unit'],r['state'],r['feature']);genes=cfg['panels'].get(r['feature'],[r['feature']]);expected=statistics.mean(float(lookup[key[:3]+(g,)]['log2cpm']) for g in genes)
 check(math.isclose(float(r['value']),expected,abs_tol=1e-9),'feature arithmetic');features[key]=float(r['value'])
pairs=read('paired_differences.tsv');groups={}
for r in pairs:
 check(float(r['day'])==cfg['day'],'fixed day');check(min(int(r['cells_AF1']),int(r['cells_AF2']))>=int(r['cell_floor']),'pair floor')
 a=features[(r['mode'],r['unit'],'AF1',r['feature'])];b=features[(r['mode'],r['unit'],'AF2',r['feature'])]
 check(math.isclose(float(r['delta']),a-b,abs_tol=1e-9),'pair arithmetic')
 groups.setdefault((r['mode'],r['cell_floor'],r['feature']),[]).append(float(r['delta']))
for r in read('paired_summary.tsv'):
 vals=groups[(r['mode'],r['cell_floor'],r['feature'])];check(len(vals)==int(r['n']),'n')
 for name,fn in [('median',statistics.median),('minimum',min),('maximum',max)]:check(math.isclose(float(r[name]),fn(vals),abs_tol=1e-9),name)
 check(int(r['positive'])==sum(v>0 for v in vals) and int(r['negative'])==sum(v<0 for v in vals),'sign counts')
cov=read('unit_coverage.tsv')
for r in read('eligibility.tsv'):
 sets={s:{v['unit'] for v in cov if v['mode']==r['mode'] and float(v['day'])==float(r['day']) and v['state']==s and int(v['cells'])>=int(r['cell_floor'])} for s in ['AF1','AF2']}
 check(int(r['paired_units'])==len(sets['AF1']&sets['AF2']),'eligible pairs including zero')
check(all(int(r['paired_units'])==0 for r in read('eligibility.tsv') if float(r['day'])==42 and r['cell_floor']=='100'),'empty strict floor preserved')
exports=json.loads((BASE/'reports/figure_manifest.json').read_text());check(len(exports)==9,'all exports')
for r in exports:check(sha(BASE/r['file'])==r['sha256'],'figure hash')
prior=json.loads((BASE/'metadata/a19_preservation.json').read_text())
for name,h in prior.items():check(sha(ROOT/'RQ_Specified/A19_fzd_response_reversibility'/name)==h,'A19 preserved: '+name)
run=json.loads((BASE/'reports/analysis_complete.json').read_text());check(run['source_sha256_unchanged'],'source unchanged');check(run['config_sha256']==sha(BASE/'config/exploratory_v1.json'),'frozen config');check(run['overlap_rows_reconciled']==1000,'independent prior extraction')
report=dict(checks_passed=checks,figure_exports=len(exports),a19_files_byte_identical=len(prior),prior_extraction_rows_reconciled=1000,scope='Arithmetic and provenance; biological H1/H2 remain untested')
(BASE/'reports/verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
