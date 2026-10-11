"""Inert helpers for new versioned outputs and cooperative checkpoint verification."""
import json,pathlib,hashlib,sys
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONFIG=HERE.parent/'config'
def write_json(path,value):
 def convert(v):
  if hasattr(v,'item'):return v.item()
  raise TypeError(type(v).__name__)
 with pathlib.Path(path).open('x') as f:json.dump(value,f,indent=2,default=convert,allow_nan=False);f.write('\n')
def require_reviewed_job(path,stage):
 if not path:raise ValueError('HOLD: root-reviewed manual checkpoint/job receipt required')
 job=json.loads(pathlib.Path(path).read_text());contract=CONFIG/(stage+'.contract.json');spec=json.loads(contract.read_text())
 if spec['status']!='frozen':raise ValueError('HOLD: contract remains draft')
 if job.get('stage')!=stage or job.get('approved') is not True or not job.get('job_id') or not job.get('before_backup_verified'):raise ValueError('HOLD: incomplete reviewed checkpoint')
 if job.get('contract_sha256')!=hashlib.sha256(contract.read_bytes()).hexdigest():raise ValueError('HOLD: checkpoint contract binding mismatch')
 if stage=='figure1' and not job.get('metadata_loader_memory_pass'):raise ValueError('HOLD: metadata/sparse-loader memory readiness unqualified')
 return job
class BoundsRecorder:
 def __init__(self):self.bounds={}
 def set(self,key,value):self.bounds[key]=value

def counts_and_fractions(obs):
 """Exact partition invariants, not a biological reproduction tolerance."""
 rows=[]
 if obs[['library','state']].isna().any().any():raise ValueError('missing library/state assignment')
 for library,sub in obs.groupby('library',observed=True):
  count=sub['state'].astype(str).value_counts();total=len(sub);cont=int(sum(v for k,v in count.items() if k.startswith('contaminant_')));alveolar=total-cont
  if int(count.sum())!=total:raise ValueError('state partition invariant')
  numerator=sum(int(v) for k,v in count.items() if not k.startswith('contaminant_'))
  if numerator!=alveolar:raise ValueError('alveolar denominator invariant')
  if alveolar and sum((Fraction(int(n),alveolar) for state,n in count.items() if not state.startswith('contaminant_')),Fraction(0))!=1:raise ValueError('exact rational fraction invariant')
  for state,n in count.items():
   rows.append({'library':str(library),'state':state,'count':int(n),'post_doublet_cells':total,'contaminant_cells':cont,'alveolar_including_unassigned':alveolar,'fraction_all':int(n)/total if total else None,'fraction_alveolar':int(n)/alveolar if alveolar and not state.startswith('contaminant_') else None})
 return rows


def fresh_output(path,stage):
 out=pathlib.Path(path).resolve()
 expected=(ROOT/'analysis/research/runs').resolve()
 if not out.is_relative_to(expected) or not out.name.startswith('p001_'+stage+'_v1_'):raise ValueError('HOLD: fresh scoped runner output required')
 out.mkdir(parents=True,exist_ok=True)
 if any(x.name not in {'receipt.json','stdout.log','stderr.log'} for x in out.iterdir()):raise ValueError('HOLD: output directory already contains artifacts')
 return out
