"""Frozen A32 RNA context screen from original GEO counts, never stripped assays."""
import argparse, gzip, hashlib, io, json, platform, re, sys, tarfile, tempfile, shutil, subprocess
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

META = Path('analysis/research/runs/A32_resolution_metadata_v1_20261103/source_metadata.tsv')
RAW = Path('raw_data/A32_GSE234197_v1/GSE234197_RAW.tar')
MYELOID = ['AM1','AM2','AM3','Prolif. AM','IM','LCM','cMonocytes','ncMonocytes','Neutrophil-like Monocytes','Neutrophils']
EP = ['Krt8','Cldn4','Sftpc','Abca3','Ager','Hopx','Aqp5']
PANELS = {s:['Arg1','Spp1','Trem2'] for s in MYELOID}
PANELS.update(Fibroblasts=['Col1a1','Col3a1','Fn1','Cthrc1'],AT1=EP,AT2=EP,AM_all=['Arg1','Spp1','Trem2'])
GENES = list(dict.fromkeys(g for gs in PANELS.values() for g in gs))
FLOOR = 10
AM = ['AM1','AM2','AM3','Prolif. AM']
CAPTURES = [a+'D'+str(d) for a in ['Young','Old'] for d in [14,28,60]]

def require(ok, message):
    if not bool(ok): raise ValueError(message)

def read_counts(f, n_genes, n_cells, selected):
    """Stream coordinate records; keep only panel vectors and all-gene cell QC."""
    head=f.readline().decode().strip().lower().split()
    require(head[:3]==['%%matrixmarket','matrix','coordinate'] and head[3] in ['real','integer'] and head[4]=='general','Unsupported MatrixMarket header')
    line=f.readline()
    while line.startswith(b'%'): line=f.readline()
    dims=list(map(int,line.split()))
    require(dims[:2]==[n_genes,n_cells],'Matrix/barcode/feature shape mismatch')
    totals=np.zeros(n_cells,dtype=np.int64); features=np.zeros(n_cells,dtype=np.int64)
    panel=np.zeros((len(selected),n_cells),dtype=np.int64)
    lookup=np.full(n_genes,-1,dtype=np.int64)
    lookup[np.asarray(selected,dtype=int)]=np.arange(len(selected))
    nnz=0
    for block in pd.read_csv(f,sep=r'\s+',header=None,names=['gene','cell','count'],dtype={'gene':np.int64,'cell':np.int64,'count':np.float64},chunksize=500000):
        gi=block.gene.to_numpy()-1;ci=block.cell.to_numpy()-1;v=block['count'].to_numpy()
        require(np.isfinite(v).all() and (v>0).all() and (v==np.floor(v)).all(),'Invalid UMI count')
        require((gi>=0).all() and (gi<n_genes).all() and (ci>=0).all() and (ci<n_cells).all(),'Coordinate outside dimensions')
        totals += np.bincount(ci,weights=v,minlength=n_cells).astype(np.int64)
        features += np.bincount(ci,minlength=n_cells)
        pi=lookup[gi];take=pi>=0
        np.add.at(panel,(pi[take],ci[take]),v[take].astype(np.int64))
        nnz+=len(block)
    require(nnz==dims[2],'Declared nonzero count mismatch')
    return totals,features,panel,nnz

def interval(case, control):
    a=np.asarray(case,float);b=np.asarray(control,float)
    effect=float(a.mean()-b.mean());va=float(a.var(ddof=1)/len(a));vb=float(b.var(ddof=1)/len(b));se=(va+vb)**.5
    if se==0: return effect,np.nan,np.nan,np.nan
    df=(va+vb)**2/(va**2/(len(a)-1)+vb**2/(len(b)-1))
    half=float(t.ppf(.975,df)*se)
    return effect,effect-half,effect+half,df

def qualify(m):
    require(m.cell_id.is_unique and (m.cell_id==m.barcode).all(),'Nonunique/disagreeing barcode')
    c=m.cell_id.str.extract(r'^(Young|Old)_D(14|28|60)\.([ACGT]{16})$')
    u=m.mice.str.extract(r'^(Young|Old)_D(14|28|60)\.(A030[1-6])_(PBS|Bleo)$')
    require(c.notna().all().all() and u.notna().all().all(),'Unrecognized source identity')
    m=m.copy();m['capture']=c[0]+'D'+c[1];m['raw_barcode']=c[2];m['stage_day']=c[1].astype(int);m['age_group']=c[0]
    require(((u[0]+'D'+u[1])==m.capture).all() and (u[3]==m.condition).all(),'Capture/mouse/treatment disagreement')
    require(((u[2].str[-1].astype(int)<=3)==(m.condition=='PBS')).all(),'HTO workbook condition disagreement')
    require((m['orig.ident'].str.replace(' ','',regex=False)==m.capture).all(),'Source capture disagreement')
    require((m.nUMIs==m.nCount_RNA).all(),'Source total count fields disagree')
    mice=m[['mice','capture','age_group','stage_day','condition']].drop_duplicates()
    require(len(m)==45311 and len(mice)==36 and mice.mice.is_unique,'Source size/units mismatch')
    require((mice.groupby(['capture','condition']).size()==3).all(),'Not three mice/arm/capture')
    require(set(PANELS)-{'AM_all'}<=set(m.celltype),'Missing source state')
    return m,mice

def summarize(m, mice, counts, totals):
    support=[];expression=[]
    for u in mice.sort_values(['age_group','stage_day','condition','mice']).itertuples(index=False):
        base=dict(mouse=u.mice,capture=u.capture,age=u.age_group,day=u.stage_day,condition=u.condition)
        all_mask=(m.mice==u.mice).to_numpy();all_n=int(all_mask.sum())
        for state,genes in PANELS.items():
            st=m.celltype.isin(AM).to_numpy() if state=='AM_all' else (m.celltype==state).to_numpy()
            ix=np.flatnonzero(all_mask & st);n=len(ix);umi=int(totals[ix].sum());eligible=n>=FLOOR
            require(n==0 or umi>0,'Nonempty zero-library state')
            common={**base,'state':state,'context':'composition-sensitive secondary' if state=='AM_all' else 'source state','n_cells':n,'all_source_cells':all_n,'relative_recovery_pct':100*n/all_n,'total_RNA_UMI':umi,'eligible':eligible}
            support.append(common)
            for gene in genes:
                v=counts[GENES.index(gene),ix];raw=int(v.sum());pos=int((v>0).sum())
                cpm=1e6*raw/umi if eligible else np.nan
                expression.append({**common,'gene':gene,'gene_UMI':raw,'positive_cells':pos,'detection_pct':100*pos/n if eligible else np.nan,'CPM':cpm,'log2_CPM_plus1':np.log2(cpm+1) if eligible else np.nan})
    support=pd.DataFrame(support);expr=pd.DataFrame(expression);contrasts=[]
    for (capture,state,gene),g in expr.groupby(['capture','state','gene'],sort=False):
        case=g[(g.condition=='Bleo') & g.eligible].log2_CPM_plus1.to_numpy()
        ctrl=g[(g.condition=='PBS') & g.eligible].log2_CPM_plus1.to_numpy()
        ok=len(case)==3 and len(ctrl)==3
        eff,lo,hi,df=interval(case,ctrl) if ok else (np.nan,)*4
        contrasts.append(dict(capture=capture,age=g.age.iloc[0],day=int(g.day.iloc[0]),state=state,gene=gene,context=g.context.iloc[0],n_BLM=int(len(case)),n_PBS=int(len(ctrl)),estimated=ok,effect_log2CPM=eff,lower95=lo,upper95=hi,welch_df=df,interval_status=('unestimated: incomplete support' if not ok else 'unestimated: zero observed variance' if not np.isfinite(df) else 'pointwise Welch-t; small n'),status='estimated; pointwise descriptive' if ok else 'unestimated: incomplete 3-versus-3 cell support'))
    return support,expr,pd.DataFrame(contrasts)

def figures(support,expr,con,out):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    mice=[u for c in CAPTURES for cond in ['PBS','Bleo'] for u in sorted(support.loc[(support.capture==c)&(support.condition==cond),'mouse'].unique())]
    states=list(PANELS)
    tab=support.pivot(index='state',columns='mouse',values='n_cells').reindex(index=states,columns=mice)
    fig,ax=plt.subplots(figsize=(15,6.5),layout='constrained')
    im=ax.imshow(np.log10(tab.to_numpy()+1),cmap='Blues',aspect='auto')
    for i in range(len(states)):
        for j in range(len(mice)):ax.text(j,i,str(tab.iloc[i,j]),ha='center',va='center',fontsize=6,color='white' if tab.iloc[i,j]>100 else '#152238')
    ax.set_yticks(range(len(states)),[s+(' (secondary)' if s=='AM_all' else '') for s in states]);ax.set_xticks(range(36),[('P' if '_PBS' in u else 'B')+u.split('A030')[1][0] for u in mice],fontsize=7)
    for x in [5.5,11.5,17.5,23.5,29.5]:ax.axvline(x,color='white',lw=2)
    for j,c in enumerate(CAPTURES):ax.text(j*6+2.5,-1,c,ha='center',fontsize=10,weight='bold')
    ax.set_title('Deposited cell support per mouse and source state',pad=32,loc='left',fontsize=15)
    ax.set_xlabel('Distinct mouse in each capture: P = PBS; B = bleomycin. Floor = 10 cells; complete 3 versus 3 required.\nAT1/AT2 effects remain unestimated. Relative recovery is not absolute tissue abundance.')
    fig.colorbar(im,ax=ax,shrink=.7,label='log10(cells + 1)');fig.savefig(out/'cell_support.png',dpi=180);plt.close(fig)
    pairs=[(s,g) for s,genes in PANELS.items() for g in genes]
    tab=con.pivot(index=['state','gene'],columns='capture',values='effect_log2CPM').reindex(index=pd.MultiIndex.from_tuples(pairs),columns=CAPTURES)
    mat=np.ma.masked_invalid(tab.to_numpy());bound=max(1,float(np.nanmax(np.abs(tab.to_numpy()))))
    fig,ax=plt.subplots(figsize=(9,16),layout='constrained');cmap=plt.get_cmap('RdBu_r').copy();cmap.set_bad('#e6e8eb')
    im=ax.imshow(mat,cmap=cmap,vmin=-bound,vmax=bound,aspect='auto')
    for i in range(len(pairs)):
        for j in range(6):
            if np.isfinite(tab.iloc[i,j]):ax.text(j,i,f'{tab.iloc[i,j]:+.1f}',ha='center',va='center',fontsize=7,color='white' if abs(tab.iloc[i,j])>.6*bound else '#111111')
    ax.set_yticks(range(len(pairs)),[f'{s} | {g}'+(' *' if s=='AM_all' else '') for s,g in pairs],fontsize=8);ax.set_xticks(range(6),CAPTURES,rotation=30,ha='right')
    ax.set_title('Injury-associated RNA contrasts\nEqual-mouse mean BLM minus PBS: log2(CPM + 1)',loc='left',fontsize=13)
    ax.set_xlabel('Gray = unestimated, not a null effect. * AM_all is composition-sensitive secondary context.\nAge/day are confounded with capture; no functional or mediation inference.')
    fig.colorbar(im,ax=ax,shrink=.35,label='Difference in mean log2(CPM + 1)');fig.savefig(out/'rna_contrasts.png',dpi=160);plt.close(fig)
    focus=[('AM1','Arg1'),('AM_all','Arg1'),('cMonocytes','Arg1'),('ncMonocytes','Arg1'),('Neutrophils','Arg1')]+[('Fibroblasts',g) for g in PANELS['Fibroblasts']]
    fig,axes=plt.subplots(3,3,figsize=(15,10),layout='constrained')
    for ax,(state,gene) in zip(axes.flat,focus):
        rows=expr[(expr.state==state)&(expr.gene==gene)&expr.eligible]
        for j,c in enumerate(CAPTURES):
            for cond,color,shift in [('PBS','#397bad',-.16),('Bleo','#c36a32',.16)]:
                vals=rows[(rows.capture==c)&(rows.condition==cond)].sort_values('mouse').log2_CPM_plus1.to_numpy()
                if len(vals):ax.scatter(j+shift+np.linspace(-.07,.07,len(vals)),vals,color=color,s=23,label=cond if j==0 else None)
        ax.set_title(state+' | '+gene+(' (secondary)' if state=='AM_all' else ''),loc='left');ax.set_xticks(range(6),['Y14','Y28','Y60','O14','O28','O60']);ax.set_ylabel('log2(CPM + 1)');ax.grid(axis='y',alpha=.15)
    axes[0,0].legend(frameon=False,fontsize=8)
    fig.suptitle('Individual mouse RNA values with at least 10 source-state cells\nMissing/low-support mice are retained in tables; plotted subsets do not create a group contrast.',fontsize=14)
    fig.savefig(out/'mouse_values.png',dpi=170);plt.close(fig)

def main(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    m,mice=qualify(pd.read_csv(META,sep='\t'));counts=np.zeros((len(GENES),len(m)),dtype=np.int64);totals=np.zeros(len(m),dtype=np.int64);checks=[]
    with tarfile.open(RAW) as tar:
        names=tar.getnames()
        for capture in CAPTURES:
            idx=np.flatnonzero((m.capture==capture).to_numpy());g=m.iloc[idx]
            prefix=next(n[:-len('barcodes.tsv.gz')] for n in names if n.endswith('_'+capture+'_barcodes.tsv.gz'))
            def gz(name): return gzip.GzipFile(fileobj=tar.extractfile(prefix+name))
            with gz('barcodes.tsv.gz') as f:bc=pd.read_csv(f,sep='\t',header=None)[0].str.replace(r'-.*','',regex=True)
            with gz('features.tsv.gz') as f:ft=pd.read_csv(f,sep='\t',header=None)
            require(bc.is_unique and ft[0].is_unique,'Duplicate source feature/barcode')
            selection=[]
            for gene in GENES:
                hits=np.flatnonzero((ft[1]==gene).to_numpy());require(len(hits)==1,'Missing/ambiguous gene '+gene);selection.append(int(hits[0]))
            take=pd.Index(bc).get_indexer(g.raw_barcode);require((take>=0).all(),'Unmatched retained barcode')
            with gz('matrix.mtx.gz') as f:ct,nf,panel,nnz=read_counts(f,len(ft),len(bc),selection)
            require(np.array_equal(ct[take],g.nCount_RNA.to_numpy()),'Raw/source UMI mismatch '+capture)
            require(np.array_equal(nf[take],g.nFeature_RNA.to_numpy()),'Raw/source detected-feature mismatch '+capture)
            counts[:,idx]=panel[:,take];totals[idx]=ct[take]
            checks.append(dict(capture=capture,source_cells=len(bc),retained_cells=len(g),source_genes=len(ft),nonzero_records=nnz,barcode_join='exact',UMI_parity='all retained cells exact',feature_count_parity='all retained cells exact'))
            print('Qualified original counts:',capture,len(g),'retained cells',flush=True)
    support,expr,con=summarize(m,mice,counts,totals)
    source_counts=pd.crosstab(m.mice,m.celltype).reindex(index=sorted(m.mice.unique()),columns=sorted(m.celltype.unique()),fill_value=0)
    support.to_csv(out/'cell_support.tsv',sep='\t',index=False,na_rep='NA');expr.to_csv(out/'mouse_expression.tsv',sep='\t',index=False,na_rep='NA');con.to_csv(out/'condition_contrasts.tsv',sep='\t',index=False,na_rep='NA');source_counts.to_csv(out/'all_source_state_counts.tsv',sep='\t')
    pd.DataFrame(checks).to_csv(out/'source_checks.tsv',sep='\t',index=False)
    # Original-matrix verification uses a second implementation and native R.
    rscript=shutil.which('Rscript');require(rscript is not None,'Independent verifier requires Rscript')
    with tempfile.TemporaryDirectory(prefix='a32_verify_',dir=out) as tmp:
        with tarfile.open(RAW) as tar:
            for suffix in ['barcodes.tsv.gz','features.tsv.gz','matrix.mtx.gz']:
                name='GSM7454030_YoungD14_'+suffix
                with tar.extractfile(name) as src,open(Path(tmp)/name,'wb') as dst:shutil.copyfileobj(src,dst)
        subprocess.run([rscript,'--vanilla',str(Path(__file__).with_name('verify_resolution_v1.R')),tmp,str(out),str(META)],check=True)
    figures(support,expr,con,out)
    summary=dict(source_cells=len(m),source_mice=len(mice),genes=GENES,cell_floor=FLOOR,planned_contrasts=len(con),estimated_contrasts=int(con.estimated.sum()),unestimated_contrasts=int((~con.estimated).sum()),epithelial_contrasts_estimated=int(con[con.state.isin(['AT1','AT2'])].estimated.sum()),fibroblast_supported_captures=sorted(con[(con.state=='Fibroblasts')&con.estimated].capture.unique()),inference='Exploratory RNA context; no joint three-compartment resolution conclusion or ARG1 functional effect.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    (out/'runtime.json').write_text(json.dumps(dict(python=sys.version,platform=platform.platform(),numpy=np.__version__,pandas=pd.__version__,matplotlib=matplotlib.__version__),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);main(ap.parse_args().output)
