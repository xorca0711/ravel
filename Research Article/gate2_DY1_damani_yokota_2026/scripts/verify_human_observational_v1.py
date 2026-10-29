"""Independent groupby arithmetic and source-field checks on human observations."""
import math
import numpy as np
import pandas as pd
from scipy.stats import spearmanr


def verify(meta,selected,total,symbols,panels,table,pb,donors,abundance,effects,associations):
    checks=0
    def same(a,b):
        nonlocal checks
        if not np.allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True):raise ValueError('Independent arithmetic mismatch')
        checks+=1
    same(total,meta.nUMI.to_numpy())
    if table.duplicated(['donor','population']).any() or donors.donor.duplicated().any():raise ValueError('Nonunique donor join')
    gene_frame=pd.DataFrame(selected,columns=symbols);gene_frame['donor']=meta.Subject_Identity.to_numpy()
    gene_frame['total']=meta.nUMI.to_numpy()
    # Independently reconstruct source-label and marker-detection subsets.
    broad=meta.Manuscript_Identity.isin(['Macrophage','Macrophage_Alveolar'])
    detection=np.count_nonzero(gene_frame[panels['identity_markers']].to_numpy(),axis=1)
    for scope in table.population.unique():
        if scope=='AllMacrophages':mask=broad
        elif scope.startswith('Proxy'):mask=broad&(detection>=int(scope[-1]))
        elif scope=='AllFibroblasts':mask=meta.Manuscript_Identity.isin(['Fibroblast','Myofibroblast'])
        else:mask=meta.Manuscript_Identity==scope
        f=gene_frame.loc[mask]
        grouped=f.groupby('donor')[symbols+['total']].sum()
        cells=f.groupby('donor').size()
        for index,row in table[table.population==scope].iterrows():
            if row.donor in grouped.index:
                independent=grouped.loc[row.donor]
                same(independent[symbols].to_numpy(),pb[index]);same(independent['total'],row.all_gene_counts);same(cells[row.donor],row.n_cells)
                for panel,genes in panels['panels'].items():
                    direct=sum(math.log2(1+float(independent[g])*1e6/float(independent['total'])) for g in genes)/len(genes)
                    same(direct,row[panel])
                expected_positive=int((f.loc[f.donor==row.donor,'ARG1']>0).sum())
                same(expected_positive,row.ARG1_positive_cells)
            else:same(pb[index],np.zeros(len(symbols)));same(row.n_cells,0)
    for row in abundance.itertuples():
        d=donors[donors.donor==row.donor].iloc[0]
        same(row.denominator_cells,d['n_'+row.denominator])
        numerator=table[(table.donor==row.donor)&(table.population==row.population)].n_cells.iloc[0]
        same(row.numerator,numerator);same(row.fraction,numerator/row.denominator_cells if row.denominator_cells else np.nan)
    for row in effects.itertuples():
        if row.kind=='abundance':f=abundance[(abundance.population==row.population)&(abundance.denominator==row.denominator)]
        else:f=table[(table.population==row.population)&(table.n_cells>=row.floor)]
        first,second=row.contrast.split('-');a=f.loc[f.disease==first,row.measure].dropna().tolist();b=f.loc[f.disease==second,row.measure].dropna().tolist()
        same(len(a),row.n_first);same(len(b),row.n_second)
        same(sum(a)/len(a)-sum(b)/len(b) if a and b else np.nan,row.mean_difference)
    # Primary-population/floor correlation endpoints are independently joined.
    f=table[(table.population=='Macrophage')&(table.n_cells>=20)].set_index('donor')
    ctx=donors.set_index('donor')
    fibro=table[table.population=='AllFibroblasts'].set_index('donor')
    fibro_only=table[table.population=='Fibroblast'].set_index('donor')
    verified_pairs=0
    for row in associations[(associations.population=='Macrophage')&(associations.floor==20)].itertuples():
        pairs=[]
        for donor,unit in f.iterrows():
            if row.disease!='pooled_diagnostic' and unit.disease!=row.disease:continue
            if row.y in ['aberrant_fraction','at2_fraction']:
                if ctx.loc[donor,'n_epithelial']<20:continue
                y=ctx.loc[donor,row.y]
            elif row.y in ['fibro_matrix_panel','fibro_only_matrix_panel']:
                source=fibro if row.y=='fibro_matrix_panel' else fibro_only
                if source.loc[donor,'n_cells']<20:continue
                y=source.loc[donor,'fibro_matrix_panel']
            else:y=unit[row.y]
            x=unit[row.x]
            if math.isfinite(x) and math.isfinite(y):pairs.append((x,y))
        same(len(pairs),row.n_donors)
        if row.status=='estimated':
            a,b=zip(*pairs);same(spearmanr(a,b).statistic,row.rho)
        verified_pairs+=1
    return {'ok':True,'scalar_or_array_checks':checks,'primary_correlation_rows_verified':verified_pairs,
            'method':'Pandas groupby versus production bincount; direct math.log2 scores; source nUMI parity; independent donor contrast sums and SciPy primary Spearman joins.',
            'limit':'Same-source computational verification, not independent biological replication; bootstrap procedures are tested synthetically.'}
