"""Prespecified paired expression contrasts and source-block RNA responses."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
from scipy import stats
B=Path(__file__).resolve().parents[1];T=B/'tables/exploratory_v1'
def save(df,name):df.to_csv(T/name,sep='\t',index=False,na_rep='NA',float_format='%.9g')
def main():
 cfg=json.loads((B/'config/exploratory_v1.json').read_text(encoding='utf-8'));raw=pd.read_csv(T/'qpcr_source_rows.tsv',sep='\t');effects=[];audit=[];summary=[]
 for sheet,contrasts in cfg['qpcr']['contrasts'].items():
  data=raw[raw.sheet==sheet.strip()]
  for compare,reference in contrasts:
   for gene,g in data.groupby('gene',sort=False):
    a=g[g.condition==compare].set_index('donor');r=g[g.condition==reference].set_index('donor');vals=[]
    for donor in sorted(set(a.index)|set(r.index)):
     status='complete' if donor in a.index and donor in r.index else 'missing_arm'
     if status=='complete' and (pd.isna(a.loc[donor,'delta_ct']) or pd.isna(r.loc[donor,'delta_ct'])):status='nonquantified_Ct'
     audit.append({'sheet':sheet.strip(),'gene':gene,'comparison':compare,'reference':reference,'donor':donor,'status':status})
     if status=='complete':
      value=float(r.loc[donor,'delta_ct']-a.loc[donor,'delta_ct']);vals.append(value);effects.append({'sheet':sheet.strip(),'gene':gene,'comparison':compare,'reference':reference,'donor':donor,'effect_log2':value})
    n=len(vals);mean=np.mean(vals) if n else np.nan;se=stats.sem(vals) if n>=2 else np.nan;half=stats.t.ppf(.975,n-1)*se if n>=2 else np.nan
    summary.append({'sheet':sheet.strip(),'gene':gene,'comparison':compare,'reference':reference,'n_pairs':n,'mean_log2':mean,'median_log2':np.median(vals) if n else np.nan,'ci95_low':mean-half,'ci95_high':mean+half,'min_log2':min(vals) if n else np.nan,'max_log2':max(vals) if n else np.nan})
 save(pd.DataFrame(effects),'qpcr_paired_effects.tsv');save(pd.DataFrame(audit),'qpcr_pairing_audit.tsv');save(pd.DataFrame(summary),'qpcr_effect_summary.tsv')
 meta=pd.read_csv(T/'bulk_samples.tsv',sep='\t');lookup=json.loads((B/'metadata/human_marker_lookup.json').read_text())['records'];members=[];expressions=[];scores=[];effects=[];interactions=[]
 for method,filename in [('TMM','bulk_tmm_log2cpm.tsv.gz'),('total_count','bulk_total_log2cpm.tsv.gz')]:
  x=pd.read_csv(B/'cache'/filename,sep='\t',index_col=0);stable=x.index.str.replace(r'\.\d+$','',regex=True);assert not stable.duplicated().any();x.index=stable
  for panel,genes in cfg['bulk']['panels'].items():
   ids=[]
   for gene in genes:
    gid=lookup[gene]['id'];mapped=gid in x.index
    if method=='TMM':members.append({'panel':panel,'gene':gene,'ensembl_id':gid,'in_filtered_matrix':mapped})
    if mapped:ids.append(gid)
   eligible=len(ids)>=2 and len(ids)/len(genes)>=.6
   if not eligible:continue
   for m in meta.itertuples():scores.append({'method':method,'sample':m.title,'block':m.block,'background':m.background,'input':m.input,'panel':panel,'score':x.loc[ids,m.title].mean(),'n_genes':len(ids)})
  for gene in sorted(set(sum(cfg['bulk']['panels'].values(),[])+cfg['bulk']['sentinels'])):
   gid=lookup[gene]['id']
   if gid in x.index:
    for m in meta.itertuples():expressions.append({'method':method,'sample':m.title,'block':m.block,'background':m.background,'input':m.input,'gene':gene,'log2cpm':x.loc[gid,m.title]})
 sdf=pd.DataFrame(scores)
 for (method,panel,block,bg),g in sdf.groupby(['method','panel','block','background'],sort=False):
  val=g.set_index('input').score;effects.append({'method':method,'panel':panel,'block':block,'background':bg,'absence_effect':val['no_CHIR']-val['CHIR']})
 edf=pd.DataFrame(effects)
 for (method,panel,block),g in edf.groupby(['method','panel','block'],sort=False):
  val=g.set_index('background').absence_effect;interactions.append({'method':method,'panel':panel,'block':block,'GSK3KD_minus_control_response':val['GSK3KD']-val['control']})
 save(pd.DataFrame(members),'bulk_panel_membership.tsv');save(pd.DataFrame(expressions),'bulk_marker_expression.tsv');save(sdf,'bulk_program_scores.tsv');save(edf,'bulk_program_effects.tsv');save(pd.DataFrame(interactions),'bulk_response_interactions.tsv')
 # Gene-wise expression changes are retained for all nominated markers, not discoveries.
 ge=[]
 for key,g in pd.DataFrame(expressions).groupby(['method','gene','block','background'],sort=False):
  val=g.set_index('input').log2cpm;ge.append(dict(zip(['method','gene','block','background'],key))|{'absence_effect':val['no_CHIR']-val['CHIR']})
 save(pd.DataFrame(ge),'bulk_marker_effects.tsv')
 print('qPCR effects:');print(pd.DataFrame(summary).to_string(index=False))
 print('Bulk program absence effects (TMM):');print(edf[edf.method=='TMM'].to_string(index=False))
 print('Pairing audit:',pd.DataFrame(audit).status.value_counts().to_dict())
if __name__=='__main__':main()
