import argparse
import json
import numpy as np
import pandas as pd
from scipy.stats import t
from common import *

p=argparse.ArgumentParser();p.add_argument('--data-root',type=Path,required=True);args=p.parse_args()
guard('bulk_complete.json')
g=load('gaona_gene_effects.tsv.gz');g['symbol']=g.symbol.map(canon)
z=g[g.medium.eq('SFFFM')].dropna(subset=['symbol']).copy()
z=z[~z.symbol.duplicated(keep=False)]
selected=[]
for direction in [1,-1]:
    q=z[(z['adj.P.Val']<.05)&(z.logFC*direction>.5)].sort_values(['P.Value','gene_id']).head(50).copy()
    q['direction']=direction;selected.append(q)
s=pd.concat(selected,ignore_index=True)
cycle=set()
gmt=args.data_root/'raw_data/msigdb/mh.all.v2024.1.Mm.symbols.gmt'
for line in gmt.read_text().splitlines():
    fields=line.split('\t')
    if fields[0] in ['HALLMARK_E2F_TARGETS','HALLMARK_G2M_CHECKPOINT']: cycle.update(fields[2:])
overlap=set(sum(CONFIG['panels'].values(),[]))|cycle
s['retained_disjoint']=~s.symbol.isin(overlap)
adm=g[g.medium.eq('ADM')].set_index('gene_id')
s['ADM_logFC']=s.gene_id.map(adm.logFC);s['ADM_same_direction']=np.sign(s.ADM_logFC)==s.direction
write(s,'frozen_gaona_signature.tsv')
panels={**CONFIG['panels']}
for label,sel in [('Gaona_YT',s),('Gaona_YT_disjoint',s[s.retained_disjoint])]:
    for d,suffix in [(1,'up'),(-1,'down')]: panels[label+'_'+suffix]=sel.loc[sel.direction.eq(d),'symbol'].tolist()
(OUT/'derived_panels.json').write_text(json.dumps(panels,indent=2)+'\n')
done('signature_freeze.json',source_effects_sha256=sha(OUT/'tables/gaona_gene_effects.tsv.gz'),
     signature_sha256=sha(OUT/'tables/frozen_gaona_signature.tsv'),derived_panels_sha256=sha(OUT/'derived_panels.json'),
     rule=CONFIG['gaona']['signature'],counts=s.groupby('direction').size().to_dict())

def score_matrix(df,meta,study):
    x=symbol_matrix(df);records=[];membership=[]
    for panel,genes in panels.items():
        mapped=[g for g in genes if g in x.index]
        eligible=len(mapped)>=max(5 if panel.startswith('Gaona') else 2,np.ceil(.6*len(genes)))
        for gene in genes: membership.append(dict(study=study,panel=panel,gene=gene,mapped=gene in mapped,panel_eligible=eligible))
        if not eligible: continue
        vals=x.loc[mapped,meta['sample']].mean(axis=0)
        records.extend(dict(study=study,panel=panel,sample=r['sample'],arm=r['arm'],score=vals[r['sample']],genes=len(mapped)) for r in meta.to_dict('records'))
    result=pd.DataFrame(records)
    for label in ['Gaona_YT','Gaona_YT_disjoint']:
        a=result[result.panel.eq(label+'_up')].set_index('sample');b=result[result.panel.eq(label+'_down')].set_index('sample')
        if len(a)==len(meta) and len(b)==len(meta):
            c=a.copy();c['score']=a.score-b.score;c['panel']=label;c['genes']=a.genes+b.genes
            result=pd.concat([result,c.reset_index()],ignore_index=True)
    return result,pd.DataFrame(membership)

nmeta=pd.read_csv(PAPER/'metadata/samples.tsv',sep='\t')
bc=json.loads((PAPER/'trials/bulk_v1/contract.json').read_text())
nmeta=pd.DataFrame(dict(sample=nmeta.accession,arm=nmeta.condition.map(bc['condition_labels'])))
n,mi=score_matrix(pd.read_csv(PAPER/'trials/bulk_v1/tables/normalized_log2CPM.tsv',sep='\t'),nmeta,'Nb2')
gm=load('gaona_samples.tsv');gm['sample']=gm['column'];gm['arm']=gm.genotype+'_'+gm.medium
a,mg=score_matrix(load('gaona_log2CPM.tsv'),gm,'Gaona')
scores=pd.concat([n,a]);write(scores,'bulk_program_scores.tsv');write(pd.concat([mi,mg]),'bulk_panel_membership.tsv')
effects=[];influences=[]
for study,contrasts in [('Nb2',bc['contrasts']),('Gaona',{'YT_vs_WT_SFFFM':['YT_SFFFM','WT_SFFFM'],'YT_vs_WT_ADM':['YT_ADM','WT_ADM']})]:
    for panel,frame in scores[scores.study.eq(study)].groupby('panel'):
        for name,(arm_a,arm_b) in contrasts.items():
            aa=frame[frame.arm.eq(arm_a)].set_index('sample').score;bb=frame[frame.arm.eq(arm_b)].set_index('sample').score
            assert len(aa)>=3 and len(bb)>=3
            av,bv=aa.var(ddof=1)/len(aa),bb.var(ddof=1)/len(bb);se=np.sqrt(av+bv)
            df=(av+bv)**2/(av**2/(len(aa)-1)+bv**2/(len(bb)-1));delta=aa.mean()-bb.mean();crit=t.ppf(.975,df)
            one=[];both=[]
            for sample in aa.index:
                value=aa.drop(sample).mean()-bb.mean();one.append(value)
                influences.append(dict(study=study,panel=panel,contrast=name,removed_a=sample,removed_b='',delta=value))
            for sample in bb.index:
                value=aa.mean()-bb.drop(sample).mean();one.append(value)
                influences.append(dict(study=study,panel=panel,contrast=name,removed_a='',removed_b=sample,delta=value))
            for sa in aa.index:
                for sb in bb.index:
                    value=aa.drop(sa).mean()-bb.drop(sb).mean();both.append(value)
                    influences.append(dict(study=study,panel=panel,contrast=name,removed_a=sa,removed_b=sb,delta=value))
            effects.append(dict(study=study,panel=panel,contrast=name,n_a=len(aa),n_b=len(bb),delta=delta,SE=se,df=df,CI_low=delta-crit*se,CI_high=delta+crit*se,
                single_drop_min=min(one),single_drop_max=max(one),paired_drop_min=min(both),paired_drop_max=max(both),all_single_drop_same_sign=all(np.sign(one)==np.sign(delta)),
                all_paired_drop_same_sign=all(np.sign(both)==np.sign(delta)),inference='conditional_independence; influence ranges not CIs'))
write(pd.DataFrame(effects),'bulk_program_effects.tsv');write(pd.DataFrame(influences),'bulk_library_influence.tsv')
# No fitting or direction selection in Nb2; preserve all receptor/feedback gene contrasts.
ng=pd.read_csv(PAPER/'trials/bulk_v1/tables/gene_effects.tsv.gz',sep='\t')
write(ng[ng.symbol.isin(CONFIG['additional_genes'])],'nb2_receptor_feedback_effects.tsv')
done('bulk_complete.json',scores=len(scores),effects=len(effects),signature_up=int(sum(s.direction==1)),signature_down=int(sum(s.direction==-1)),scope='exploratory fixed-normalization program and influence analysis')
print('Bulk extensions complete:',len(effects),'program contrasts; signature',s.groupby('direction').size().to_dict())
