"""Independent arithmetic, provenance, sample-unit and figure checks."""
from pathlib import Path
import csv,hashlib,json,math,statistics
BASE=Path(__file__).resolve().parents[1];A20=BASE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(name):
 with (BASE/'tables'/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter=chr(9)))
n=0
def check(v,msg):
 global n
 if not v:raise AssertionError(msg)
 n+=1
cfg=json.loads((BASE/'config/analysis_contract.json').read_text());check(sha(BASE/'cache'/cfg['source_file'])==cfg['source_sha256'],'frozen counts')
run=json.loads((BASE/'reports/analysis_complete.json').read_text());check(run['config_sha256']==sha(BASE/'config/analysis_contract.json'),'frozen config')
with (BASE/'cache'/cfg['source_file']).open(newline='') as f:
 reader=csv.DictReader(f,delimiter=chr(9));samples=reader.fieldnames[1:];totals={s:0 for s in samples};raw={}
 for r in reader:
  vals={s:int(r[s]) for s in samples};check(all(v>=0 for v in vals.values()),'integer count bounds');raw[r['probe']]=vals
  for s,v in vals.items():totals[s]+=v
mapping={r['gene']:r for r in table('gene_mapping.tsv')};check(mapping['FZD10']['mapped']=='False','FZD10 unmeasured, not zero');check(sum(r['mapped']=='True' for r in mapping.values())==44,'mapped genes')
meta=table('samples.tsv');check(len(meta)==16 and len({m['donor'] for m in meta})==4,'biological units')
for donor in range(1,5):check({m['condition'] for m in meta if int(m['donor'])==donor}==set(cfg['conditions']),'complete donor block')
norm={r['sample']:r for r in table('normalization.tsv')}
for s in samples:
 check(totals[s]==int(norm[s]['library_size']),'full-source denominator')
 check(math.isclose(float(norm[s]['effective_library_size']),totals[s]*float(norm[s]['TMM_factor']),rel_tol=1e-12),'effective library size')
features={}
for r in table('sample_features.tsv'):
 genes=cfg['panels'].get(r['feature'],[r['feature']]);den=float(norm[r['sample']]['effective_library_size']) if r['normalization']=='TMM' else totals[r['sample']]
 value=statistics.mean(math.log2(raw[mapping[g]['ensembl']][r['sample']]/den*1e6+1) for g in genes)
 check(math.isclose(float(r['value']),value,abs_tol=1e-9),'independent normalized feature')
 features[(r['normalization'],r['feature'],r['donor'],r['condition'])]=float(r['value'])
groups={}
for r in table('donor_contrasts.tsv'):
 expected=sum(features[(r['normalization'],r['feature'],r['donor'],condition)]*weight for condition,weight in cfg['contrasts'][r['contrast']].items())
 check(math.isclose(float(r['delta']),expected,abs_tol=1e-9),'direct donor contrast')
 key=(r['normalization'],r['feature'],r['contrast']);groups.setdefault(key,[]).append(float(r['delta']))
for r in table('contrast_summary.tsv'):
 v=groups[(r['normalization'],r['feature'],r['contrast'])];check(len(v)==4,'four donors not 16 replicates')
 for label,fn in [('mean',statistics.mean),('median',statistics.median),('minimum',min),('maximum',max)]:check(math.isclose(float(r[label]),fn(v),abs_tol=1e-9),label)
 leave=[statistics.mean(v[:i]+v[i+1:]) for i in range(4)]
 check(math.isclose(float(r['leave_one_mean_min']),min(leave),abs_tol=1e-9) and math.isclose(float(r['leave_one_mean_max']),max(leave),abs_tol=1e-9),'leave-one-donor range')
 check(int(r['positive'])==sum(x>0 for x in v) and int(r['negative'])==sum(x<0 for x in v),'donor directions')
for r in table('gene_coverage.tsv'):
 if r['mapped']=='False':check(r['total_counts']=='','missing gene has no imputed count');continue
 vals=raw[r['ensembl']];num=sum(v>=10 for v in vals.values());check(num==int(float(r['libraries_ge10'])),'count coverage');check(r['adequately_detected']==str(num>=4),'low detection flag')
figs=json.loads((BASE/'reports/figure_manifest.json').read_text());check(len(figs)==9,'nine figure exports')
for r in figs:check(sha(BASE/r['file'])==r['sha256'],'figure hash')
previous=json.loads((BASE/'history/a20_pre_extension_manifest.json').read_text())['files']
archived=json.loads((BASE/'history/document_snapshots.json').read_text()) if (BASE/'history/document_snapshots.json').exists() else {};unchanged=0
for r in previous:
 path=BASE/'history'/archived[r['file']] if r['file'] in archived else A20/r['file'];check(sha(path)==r['sha256'],'prior A20 preserved: '+r['file']);unchanged+=r['file'] not in archived
prior_a19=json.loads((A20/'metadata/a19_preservation.json').read_text())
for name,h in prior_a19.items():check(sha(A20.parent/'A19_fzd_response_reversibility'/name)==h,'A19 preserved')
report=dict(checks_passed=n,source_donors=4,source_libraries=16,mapped_genes=44,missing_gene='FZD10',figure_exports=9,prior_A20_files_unchanged=unchanged,prior_A20_documents_archived=len(archived),A19_files_unchanged=len(prior_a19),scope='Arithmetic/provenance only; functional Fzd1/Fzd2 hypotheses remain untested')
(BASE/'reports/verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
