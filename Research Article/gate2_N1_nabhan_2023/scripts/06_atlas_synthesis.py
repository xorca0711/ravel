"""Post-run descriptive comparisons of predefined receptors; no fitted p-values.

Records direction across units, floors, depth and doublet sensitivities. Reuses
exposed atlas_v1 results; not an independent confirmation or a new preregistration.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]/'trials/atlas_v1'


def main():
    a=pd.read_csv(ROOT/'tables/unit_receptor_context.tsv.gz',sep='\t')
    a['day']=a.day.astype(str)
    keys=['dataset','mode','unit','condition','day','state','lineage']
    c=a[keys+['cells','cells_depth500']].drop_duplicates()
    pairs=[('Fzd6','Fzd1'),('Fzd5','Fzd1'),('Fzd6','Fzd5'),('Fzd1','Fzd2'),('Fzd1','Fzd7'),('Fzd4','Fzd1'),('Fzd4','Fzd5'),('Fzd4','Fzd6')]
    rows=[]
    for metric in ['cpm','detection','detection_depth500']:
        z=a.pivot(index=keys,columns='gene',values=metric).reset_index().merge(c,on=keys,validate='one_to_one')
        for floor in [20,50,100]:
            zz=z[z['cells_depth500' if metric=='detection_depth500' else 'cells'].ge(floor)]
            for name,g in zz.groupby(['dataset','mode','condition','day','state','lineage'],dropna=False):
                for first,second in pairs:
                    delta=g[first]-g[second]
                    rows.append(dict(zip(['dataset','mode','condition','day','state','lineage'],name)) |
                        dict(metric=metric,cell_floor=floor,first=first,second=second,units=len(g),
                             units_positive=int((delta>0).sum()),units_negative=int((delta<0).sum()),units_tied=int((delta==0).sum()),
                             median_difference=float(delta.median()),min_difference=float(delta.min()),max_difference=float(delta.max())))
    pd.DataFrame(rows).to_csv(ROOT/'tables/within_unit_receptor_ordering.tsv.gz',sep='\t',index=False)
    # Descriptive within-subtype association; human IPF only; no pooling of disease diagnoses.
    primary=a[(a.dataset=='Habermann2020') & a.condition.eq('IPF') & a.cells.ge(50)]
    wide=primary.pivot(index=['unit','state'],columns='gene',values='cpm').reset_index()
    correlations=[]
    for state,g in wide.groupby('state'):
        if 'fibro' not in state.lower() or len(g)<5: continue
        module=np.log2(g[['Cthrc1','Lrrc15','Col1a1','Col3a1']]+1).mean(axis=1)
        for receptor in ['Fzd1','Fzd2','Fzd7']:
            correlations.append(dict(state=state,condition='IPF',units=len(g),receptor=receptor,
                spearman_rho=g[receptor].corr(module,method='spearman'),
                interpretation='post-run descriptive association; no adjusted inference; common RNA denominator and severity remain rivals'))
    pd.DataFrame(correlations).to_csv(ROOT/'tables/fibroblast_context_associations.tsv',sep='\t',index=False)
    print('Recorded',len(rows),'descriptive ordering rows and',len(correlations),'within-subtype associations')


if __name__=='__main__': main()
