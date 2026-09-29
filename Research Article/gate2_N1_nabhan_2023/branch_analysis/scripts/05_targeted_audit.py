"""Post hoc rival checks prompted by the observed CAP1 Fzd4-cycling association."""
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from common import *

guard('targeted_audit_complete.json')
done('targeted_audit_contract.json',exposure='All extension_v1 summaries inspected; CAP1 rho0.738 selected for a confounding check, not a confirmatory test',
    checks='Compare original receptor CPM/detection and expected detection at500 UMI with cycling/junction programs in day42 CAP1/CAP2; report pooled and each source round; no p-values or adequacy claims for n4 rounds',
    input_files={str(f.relative_to(REPO)):sha(f) for f in [PAPER/'trials/atlas_v1/tables/unit_receptor_context.tsv.gz',OUT/'tables/mouse_program_scores.tsv',OUT/'tables/mouse_sample_context.tsv']})
a=pd.read_csv(PAPER/'trials/atlas_v1/tables/unit_receptor_context.tsv.gz',sep='\t',low_memory=False)
a=a[(a.dataset=='Niethamer2025')&(a['mode']=='doublets_removed')&(a.cells>=50)&(a.gene=='Fzd4')].copy();a['day']=pd.to_numeric(a.day)
a=a[a.day.eq(42)&a.state.isin(['CAP1','CAP2'])]
p=load('mouse_program_scores.tsv');p=p[(p['mode']=='doublets_removed')&(p.cells>=50)&p.day.eq(42)&p.panel.isin(['cycling','endothelial_junction'])]
m=load('mouse_sample_context.tsv')[['unit','round']]
j=a.merge(p,on=['unit','state','day'],suffixes=('_receptor','_program'),validate='one_to_many').merge(m,on='unit',validate='many_to_one')
write(j[['unit','state','day','round','panel','score','cpm','detection','detection_depth500','cells_depth500']],'vascular_rival_inputs.tsv')
rows=[]
for (state,program),df in j.groupby(['state','panel']):
    for scope,group in [('pooled',df)]+list(df.groupby('round')):
        for measurement in ['cpm','detection','detection_depth500']:
            z=group if measurement!='detection_depth500' else group[group.cells_depth500>=50]
            rho=spearmanr(z[measurement],z.score).statistic if len(z)>=3 and z[measurement].nunique()>1 and z.score.nunique()>1 else np.nan
            rows.append(dict(state=state,program=program,scope=scope,measurement=measurement,units=len(z),rho=rho,interpretation='posthoc descriptive rival audit; trace window/genotype/sex unresolved'))
write(pd.DataFrame(rows),'vascular_depth_round_audit.tsv')
done('targeted_audit_complete.json',comparisons=len(rows),scope='posthoc confounding sensitivity; no validation')
print(pd.DataFrame(rows).query("state == 'CAP1' and program == 'cycling'")[['scope','measurement','units','rho']].round(3).to_string(index=False))
