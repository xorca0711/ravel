"""Exposed observational human-lung description; no infection or causal analysis."""
import argparse
import gzip
import importlib.metadata
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from human_stats_v1 import log_cpm,mean_difference,correlation_summary
from verify_human_observational_v1 import verify

RAW=Path('raw_data/GSE136831')
SPEC=Path(__file__).resolve().parents[1]/'config/human_panels_v1.json'
FLOORS=[10,20,50]
DISEASES=['Control','IPF','COPD']
SCOPES=['Macrophage','Macrophage_Alveolar','AllMacrophages','Proxy1','Proxy2','Proxy3']


def stream_counts(path,n_cells,n_genes,gene_indices):
    lookup=np.full(n_genes,-1,dtype=np.int32);lookup[gene_indices]=np.arange(len(gene_indices))
    selected=np.zeros((n_cells,len(gene_indices)),dtype=np.int64)
    total=np.zeros(n_cells,dtype=np.int64);detected=total.copy();seen=0;start=time.monotonic()
    with gzip.open(path,'rt') as stream:
        if next(stream).strip()!='%%MatrixMarket matrix coordinate integer general':raise ValueError('Matrix convention changed')
        line=next(stream)
        while line.startswith('%'):line=next(stream)
        ng,nc,nnz=map(int,line.split())
        if (ng,nc)!=(n_genes,n_cells):raise ValueError('Matrix dimensions changed')
        reader=pd.read_csv(stream,sep=r'\s+',header=None,names=['g','c','v'],dtype=np.int64,chunksize=2_000_000)
        for chunk in reader:
            g=chunk.g.to_numpy()-1;c=chunk.c.to_numpy()-1;v=chunk.v.to_numpy()
            if g.min()<0 or g.max()>=ng or c.min()<0 or c.max()>=nc or v.min()<=0 or v.max()>=2**31:raise ValueError('Invalid matrix entries')
            total+=np.bincount(c,weights=v,minlength=nc).astype(np.int64)
            detected+=np.bincount(c,minlength=nc)
            target=lookup[g];keep=target>=0
            np.add.at(selected,(c[keep],target[keep]),v[keep])
            seen+=len(chunk)
            if seen%40_000_000==0:print(json.dumps({'matrix_entries':seen,'total_entries':nnz,'seconds':round(time.monotonic()-start,1)}),flush=True)
    if seen!=nnz:raise ValueError('Matrix entry count mismatch')
    return selected,total,detected,seen


def write(out,name,table):
    table.to_csv(out/name,sep='\t',index=False,lineterminator='\n',compression='infer')


def aggregate(meta,selected,total,symbols,panels):
    valid=meta.Manuscript_Identity!='Multiplet'
    donors=sorted(meta.Subject_Identity.unique());dmap={d:i for i,d in enumerate(donors)}
    disease_map=meta.groupby('Subject_Identity').Disease_Identity.first().to_dict()
    dc=meta.Subject_Identity.map(dmap).to_numpy()
    identity=[symbols.index(s) for s in panels['identity_markers']]
    mac=meta.Manuscript_Identity.isin(['Macrophage','Macrophage_Alveolar']).to_numpy()
    hits=(selected[:,identity]>0).sum(axis=1)
    masks={label:(meta.Manuscript_Identity==label).to_numpy() for label in sorted(meta.Manuscript_Identity.unique())}
    masks['AllMacrophages']=mac
    for k in [1,2,3]:masks[f'Proxy{k}']=mac&(hits>=k)
    masks['AllFibroblasts']=meta.Manuscript_Identity.isin(['Fibroblast','Myofibroblast']).to_numpy()
    rows=[];counts=[]
    for group,mask in masks.items():
        n=np.bincount(dc[mask],minlength=len(donors));tot=np.bincount(dc[mask],weights=total[mask],minlength=len(donors)).astype(np.int64)
        pb=np.zeros((len(donors),len(symbols)),dtype=np.int64)
        detection=pb.copy()
        for j in range(len(symbols)):
            pb[:,j]=np.bincount(dc[mask],weights=selected[mask,j],minlength=len(donors)).astype(np.int64)
            detection[:,j]=np.bincount(dc[mask],weights=selected[mask,j]>0,minlength=len(donors)).astype(np.int64)
        for i,donor in enumerate(donors):
            values={'donor':donor,'disease':disease_map[donor],'population':group,
                    'n_cells':int(n[i]),'all_gene_counts':int(tot[i]),'ARG1_positive_cells':int(detection[i,symbols.index('ARG1')])}
            norm=log_cpm(pb[i:i+1],np.array([tot[i]]))[0] if tot[i]>0 else np.full(len(symbols),np.nan)
            for panel,genes in panels['panels'].items():values[panel]=float(np.mean(norm[[symbols.index(s) for s in genes]]))
            values['ARG1_logCPM']=float(norm[symbols.index('ARG1')])
            values['ARG1_detection_fraction']=values['ARG1_positive_cells']/n[i] if n[i] else np.nan
            for j,symbol in enumerate(symbols):values['gene_'+symbol]=float(norm[j])
            rows.append(values);counts.append(pb[i])
    table=pd.DataFrame(rows)
    donor_rows=[];abundance=[]
    for i,donor in enumerate(donors):
        cell=(dc==i)&valid.to_numpy();subset=meta.loc[cell];den={
            'captured':int(cell.sum()),'myeloid':int(((dc==i)&(meta.CellType_Category=='Myeloid').to_numpy()).sum()),
            'macrophages':int(((dc==i)&mac).sum()),'epithelial':int(((dc==i)&(meta.CellType_Category=='Epithelial').to_numpy()).sum())}
        base={'donor':donor,'disease':subset.Disease_Identity.iloc[0],**{'n_'+k:v for k,v in den.items()},
              'mean_UMI':float(total[cell].mean()),'macrophage_fraction':den['macrophages']/den['captured']}
        for label,key in [('Aberrant_Basaloid','aberrant_fraction'),('ATII','at2_fraction')]:
            base[key]=int(((dc==i)&masks[label]).sum())/den['epithelial'] if den['epithelial'] else np.nan
        donor_rows.append(base)
        for group in SCOPES:
            numerator=int(((dc==i)&masks[group]).sum())
            for denominator in ['myeloid','macrophages','captured']:
                abundance.append({'donor':donor,'disease':base['disease'],'population':group,
                                  'denominator':denominator,'numerator':numerator,'denominator_cells':den[denominator],
                                  'fraction':numerator/den[denominator] if den[denominator] else np.nan})
    return table,np.asarray(counts),pd.DataFrame(donor_rows),pd.DataFrame(abundance),masks


def contrasts(table,abundance,panels,rng):
    result=[]
    def compare(frame,measure,context):
        for first,second in [('IPF','Control'),('COPD','Control'),('IPF','COPD')]:
            a=frame.loc[frame.disease==first,measure].dropna().to_numpy();b=frame.loc[frame.disease==second,measure].dropna().to_numpy()
            interval=mean_difference(a,b,rng)
            result.append(dict(context,measure=measure,contrast=first+'-'+second,n_first=len(a),n_second=len(b),
                               mean_first=float(a.mean()) if len(a) else np.nan,mean_second=float(b.mean()) if len(b) else np.nan,
                               median_first=float(np.median(a)) if len(a) else np.nan,median_second=float(np.median(b)) if len(b) else np.nan,
                               mean_difference=float(a.mean()-b.mean()) if len(a) and len(b) else np.nan,**interval,
                               status='estimated_pointwise' if min(len(a),len(b))>=3 else 'fewer_than_3_donors_for_interval'))
    for (scope,denom),frame in abundance.groupby(['population','denominator'],sort=True):
        compare(frame,'fraction',{'population':scope,'floor':0,'denominator':denom,'kind':'abundance'})
    genes=sorted(set(sum([panels['panels'][p] for p in ['FABP4_panel','matrix_mac_panel']],[])+panels['highlighted_genes']))
    for scope in SCOPES:
        for floor in FLOORS:
            frame=table[(table.population==scope)&(table.n_cells>=floor)]
            measures=['FABP4_panel','matrix_mac_panel','ARG1_logCPM','ARG1_detection_fraction']
            if floor==20:measures+=['gene_'+g for g in genes]
            for measure in measures:compare(frame,measure,{'population':scope,'floor':floor,'denominator':'all_gene_UMI','kind':'expression'})
    return pd.DataFrame(result)


def associations(table,donors,abundance,rng):
    results=[]
    fibro=table[table.population=='AllFibroblasts'][['donor','fibro_matrix_panel','n_cells']].rename(columns={'n_cells':'fibro_cells'})
    fibro_only=table[table.population=='Fibroblast'][['donor','fibro_matrix_panel','n_cells']].rename(columns={'n_cells':'fibro_only_cells','fibro_matrix_panel':'fibro_only_matrix_panel'})
    fibro=fibro.merge(fibro_only,on='donor',validate='one_to_one')
    fibro['myofibro_cells']=fibro.fibro_cells-fibro.fibro_only_cells
    fibro['myofibro_share']=fibro.myofibro_cells/fibro.fibro_cells.replace(0,np.nan)
    pairs=[('FABP4_panel','matrix_mac_panel')]+[(x,y) for x in ['FABP4_panel','matrix_mac_panel','ARG1_logCPM']
        for y in ['aberrant_fraction','at2_fraction','fibro_matrix_panel','fibro_only_matrix_panel']]
    for scope in ['Proxy2','Macrophage','AllMacrophages']:
        frame=table[table.population==scope].drop(columns='fibro_matrix_panel').merge(donors,on=['donor','disease'],validate='one_to_one').merge(fibro,on='donor',validate='one_to_one')
        for floor in FLOORS:
            for disease in [*DISEASES,'pooled_diagnostic']:
                base=frame[(frame.n_cells>=floor)&((frame.disease==disease) if disease!='pooled_diagnostic' else True)]
                for x,y in pairs:
                    f=base.copy()
                    if y in ['aberrant_fraction','at2_fraction']:f=f[f.n_epithelial>=floor]
                    if y=='fibro_matrix_panel':f=f[f.fibro_cells>=floor]
                    if y=='fibro_only_matrix_panel':f=f[f.fibro_only_cells>=floor]
                    f=f.dropna(subset=[x,y])
                    cov=np.column_stack([np.log1p(f.n_captured),f.mean_UMI,f.macrophage_fraction])
                    if disease=='pooled_diagnostic':cov=np.column_stack([cov,(f.disease=='IPF').astype(int),(f.disease=='COPD').astype(int)])
                    summary=correlation_summary(f[x],f[y],cov,rng)
                    results.append(dict(population=scope,floor=floor,disease=disease,x=x,y=y,**summary))
    for disease in [*DISEASES,'pooled_diagnostic']:
        frame=abundance[(abundance.population=='Proxy2')&(abundance.denominator=='macrophages')].merge(donors[['donor','mean_UMI','n_captured']],on='donor',validate='one_to_one')
        if disease!='pooled_diagnostic':frame=frame[frame.disease==disease]
        f=frame.dropna(subset=['fraction','mean_UMI'])
        summary=correlation_summary(f.fraction,f.mean_UMI,np.log1p(f.n_captured).to_numpy()[:,None],rng)
        results.append(dict(population='Proxy2',floor=0,disease=disease,x='proxy_fraction_macrophages',y='mean_UMI',**summary))
    return pd.DataFrame(results)


def plot(out,table,abundance,assoc):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    colors={'Control':'#3b6b9c','IPF':'#ba5842','COPD':'#608b66'}
    fig,axes=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
    selections=[('Macrophage','myeloid','Primary: Macrophage / myeloid'),('Proxy2','myeloid','Sensitivity: proxy / myeloid')]
    for ax,(scope,denom,title) in zip(axes,selections):
        for i,disease in enumerate(DISEASES):
            f=abundance[(abundance.population==scope)&(abundance.denominator==denom)&(abundance.disease==disease)]
            y=100*f.fraction.to_numpy();offset=np.linspace(-.15,.15,len(y))
            ax.scatter(i+offset,y,color=colors[disease],s=13,alpha=.75)
            if len(y):ax.plot([i-.2,i+.2],[np.nanmedian(y)]*2,color='black',lw=2)
        ax.set(xticks=range(3),xticklabels=DISEASES,ylabel='Captured cells (%)',title=title)
    ax=axes[2]
    for disease in DISEASES:
        f=table[(table.population=='Macrophage')&(table.n_cells>=20)&(table.disease==disease)]
        ax.scatter(f.FABP4_panel,f.matrix_mac_panel,color=colors[disease],label=f'{disease} (n={len(f)})',s=22,alpha=.8)
    ax.set(xlabel='FABP4-associated panel',ylabel='Matrix-associated macrophage panel',title='Primary: Macrophage; floor 20')
    ax.legend(fontsize=8);fig.suptitle('Human lung atlas: descriptive observations, not validated NAMs',fontsize=12)
    fig.savefig(out/'human_overview.png',dpi=180);plt.close(fig)
    sub=assoc[(assoc.population=='Macrophage')&(assoc.floor==20)&(assoc.x=='matrix_mac_panel')]
    ys=['aberrant_fraction','at2_fraction','fibro_matrix_panel']
    mat=np.full((3,4),np.nan);n=np.zeros((3,4),int)
    for i,y in enumerate(ys):
        for j,d in enumerate([*DISEASES,'pooled_diagnostic']):
            r=sub[(sub.y==y)&(sub.disease==d)].iloc[0];mat[i,j]=r.rho;n[i,j]=r.n_donors
    fig,ax=plt.subplots(figsize=(8,3.3),layout='constrained');im=ax.imshow(np.ma.masked_invalid(mat),vmin=-1,vmax=1,cmap='coolwarm')
    for i in range(3):
        for j in range(4):ax.text(j,i,(f'{mat[i,j]:.2f}' if np.isfinite(mat[i,j]) else 'held')+f'\nn={n[i,j]}',ha='center',va='center',fontsize=9)
    ax.set(xticks=range(4),xticklabels=[*DISEASES,'Pooled diagnostic'],yticks=range(3),yticklabels=['Aberrant basaloid fraction','ATII fraction','Fibroblast matrix panel'],title='Primary Macrophage RNA and same-donor context\nSpearman rho; floor 20; holds retain sparse/constant pairs')
    fig.colorbar(im,ax=ax,label='Spearman rho');fig.savefig(out/'human_associations.png',dpi=180);plt.close(fig)


def main(out):
    panels=json.loads(SPEC.read_text());symbols=panels['symbols']
    meta=pd.read_csv(RAW/'GSE136831_AllCells.Samples.CellType.MetadataTable.txt.gz',sep='\t')
    for category,labels in panels['category_labels'].items():
        if sorted(meta.loc[meta.CellType_Category==category,'Manuscript_Identity'].unique())!=labels:raise ValueError('Denominator category/label mapping changed')
    genes=pd.read_csv(RAW/'GSE136831_AllCells.GeneIDs.txt.gz',sep='\t')
    with gzip.open(RAW/'GSE136831_AllCells.cellBarcodes.txt.gz','rt') as f:barcodes=[line.strip() for line in f]
    if meta.CellBarcode_Identity.tolist()!=barcodes or meta.CellBarcode_Identity.duplicated().any():raise ValueError('Barcode join mismatch')
    gene_indices=[]
    for symbol in symbols:
        hit=genes.index[genes.HGNC_EnsemblAlt_GeneID==symbol].tolist()
        if len(hit)!=1 or genes.loc[hit[0],'Ensembl_GeneID']!=panels['ensembl_ids'][symbol]:raise ValueError('Missing/ambiguous/changed human symbol: '+symbol)
        gene_indices.append(hit[0])
    selected,total,detected,nnz=stream_counts(RAW/'GSE136831_RawCounts_Sparse.mtx.gz',len(meta),len(genes),gene_indices)
    np.savez_compressed(out/'selected_cell_counts.npz',counts=selected,all_gene_counts=total,symbols=np.asarray(symbols),barcodes=np.asarray(barcodes))
    audit={'matrix_nnz':nnz,'n_cells':len(meta),'raw_UMI_mismatched_cells':int((total!=meta.nUMI.to_numpy()).sum()),
           'raw_detected_genes_mismatched_cells':int((detected!=meta.nGene.to_numpy()).sum()),
           'raw_UMI_sum':int(total.sum()),'source_metadata_UMI_sum':int(meta.nUMI.sum()),'selected_genes':len(symbols)}
    (out/'matrix_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    if not np.array_equal(total,meta.nUMI.to_numpy()):raise ValueError('Raw all-gene UMI totals disagree with source nUMI')
    if not np.array_equal(detected,meta.nGene.to_numpy()):raise ValueError('Raw detected-gene counts disagree with source nGene')
    table,pb,donors,abundance,masks=aggregate(meta,selected,total,symbols,panels)
    for scope,key in [('Fibroblast','fibroblast_cells'),('Myofibroblast','myofibroblast_cells')]:
        lookup=table[table.population==scope].set_index('donor').n_cells
        donors[key]=donors.donor.map(lookup)
    donors['myofibroblast_share']=donors.myofibroblast_cells/(donors.fibroblast_cells+donors.myofibroblast_cells).replace(0,np.nan)
    write(out,'donor_expression.tsv.gz',table);write(out,'donor_context.tsv',donors);write(out,'donor_abundance.tsv',abundance)
    np.savez_compressed(out/'donor_selected_counts.npz',counts=pb,symbols=np.asarray(symbols),donors=table.donor.to_numpy(dtype=str),populations=table.population.to_numpy(dtype=str))
    rng=np.random.default_rng(20261029)
    effects=contrasts(table,abundance,panels,rng);assoc=associations(table,donors,abundance,rng)
    write(out,'contrasts.tsv',effects);write(out,'associations.tsv',assoc)
    arg1=table[table.population.isin(meta.Manuscript_Identity.unique())][['donor','disease','population','n_cells','all_gene_counts','ARG1_positive_cells','ARG1_detection_fraction','ARG1_logCPM']].copy()
    arg1['ARG1_raw_counts']=pb[table.population.isin(meta.Manuscript_Identity.unique()),symbols.index('ARG1')]
    arg1['interpretation']='captured annotated population only; Multiplet excluded from source attribution'
    write(out,'arg1_by_annotation.tsv',arg1)
    verification=verify(meta,selected,total,symbols,panels,table,pb,donors,abundance,effects,assoc)
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n',encoding='utf-8')
    plot(out,table,abundance,assoc)
    summary={'analysis_id':'DY1-P01.human_observational_v1','n_donors':len(donors),'matrix_nnz':nnz,'selected_genes':len(symbols),
             'all_cell_UMI_and_gene_detection_match':True,'multiplets_excluded':int((meta.Manuscript_Identity=='Multiplet').sum()),
             'neutrophil_annotation_present':False,'gene_mapping':'all requested native human symbols unique; no orthologue mapping',
             'proxy':'analyst 2-of-5 detection rule; 1/3-marker sensitivity; not validated NAM or author-cluster reproduction',
             'associations_by_status':assoc.status.value_counts().to_dict(),'comparisons':len(effects),
             'versions':{name:importlib.metadata.version(name) for name in ['numpy','pandas','scipy','matplotlib']},
             'scientific_acceptance':'not_assessed','inference':'same-source exposed human observational description; no pathogen, immune-history, activity or causal inference'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
