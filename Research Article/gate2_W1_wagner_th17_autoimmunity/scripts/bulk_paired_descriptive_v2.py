"""Bounded R3 animal-paired expression estimates and figures; no DEG calls."""
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd

SERIES=['GSE162300','GSE162382']
# Exact source identifiers; only figure typography uses mouse-style capitalization.
GENES=['ODC1','SRM','SMS','SAT1','SMOX','PGAM1','LDHA','TPI1','FOXP3','RORC','IL17A','KDM6B']
DISPLAY={g:g.capitalize() for g in GENES}
COLORS={'Th17p':'#287DB8','Th17n':'#8657A3','iTreg':'#26866D'}
GROUPS=[('A: Th17p, WT','GSE162300','Th17p','WT'),('A: Th17n, WT','GSE162300','Th17n','WT'),
        ('A: iTreg, WT','GSE162300','iTreg','WT'),('B: Th17n, WT','GSE162382','Th17n','WT'),
        ('B: Th17n, KO','GSE162382','Th17n','JMJD3_KO'),('B: iTreg, WT','GSE162382','iTreg','WT'),
        ('B: iTreg, KO','GSE162382','iTreg','JMJD3_KO')]

def save_tsv(frame,path):
    frame.to_csv(path,sep='\t',index=False,float_format='%.14g',lineterminator='\n')

def collapse_counts(frame,mapping):
    if set(frame.columns)!=set(mapping.source_title):raise ValueError('Counts/map column mismatch')
    ids=sorted(mapping.library_id.unique())
    counts=np.column_stack([frame.loc[:,mapping.loc[mapping.library_id==x,'source_title'].tolist()].sum(axis=1).to_numpy() for x in ids])
    if not np.isfinite(counts).all() or (counts<0).any():raise ValueError('Invalid counts')
    if (counts.sum(axis=0)<=0).any():raise ValueError('Empty library')
    return ids,counts

def paired_difference(logs,libraries,cell,genotype):
    subset=libraries[(libraries.cell_type==cell)&(libraries.genotype==genotype)]
    animals=sorted(subset.animal_id.unique());deltas=[]
    for animal in animals:
        positions={r.treatment:i for i,r in libraries.iterrows() if r.animal_id==animal and r.cell_type==cell and r.genotype==genotype}
        if set(positions)!=set(['control','DFMO']):raise ValueError('Incomplete animal pair')
        deltas.append(logs[:,positions['DFMO']]-logs[:,positions['control']])
    return animals,np.column_stack(deltas)

def summarize(genes,delta,series,contrast):
    return pd.DataFrame(dict(series=series,contrast=contrast,gene=genes,n_animal_labels=delta.shape[1],
        mean_delta=delta.mean(axis=1),median_delta=np.median(delta,axis=1),sd_delta=delta.std(axis=1,ddof=1),
        minimum_delta=delta.min(axis=1),maximum_delta=delta.max(axis=1),
        n_positive=(delta>0).sum(axis=1),n_negative=(delta<0).sum(axis=1),n_zero=(delta==0).sum(axis=1)))

def independent_check(raw,ids,counts,logs,mapping,all_deltas,libraries):
    # Read the original file with the standard csv module, distinct from the production dataframe parser.
    import csv
    with gzip.open(raw,'rt',encoding='utf-8-sig',newline='') as f:
        reader=csv.reader(f);header=next(reader);rows=list(reader)
    groups={x:[header.index(t) for t in mapping.loc[mapping.library_id==x,'source_title']] for x in ids}
    alternative=np.asarray([[math.fsum(float(row[j]) for j in groups[x]) for x in ids] for row in rows])
    if not np.allclose(alternative,counts,rtol=1e-13,atol=1e-10):raise ValueError('Independent count collapse disagreement')
    totals=[math.fsum(alternative[:,i]) for i in range(len(ids))]
    independent_logs=np.asarray([[math.log2(1+row[i]*1e6/totals[i]) for i in range(len(ids))] for row in alternative])
    log_error=float(np.max(np.abs(independent_logs-logs)))
    if log_error>1e-10:raise ValueError('Independent log CPM disagreement')
    max_delta_error=0.0
    for cell,genotype,animals,delta in all_deltas:
        for j,animal in enumerate(animals):
            lookup={(r.animal_id,r.cell_type,r.treatment):i for i,r in libraries.iterrows()}
            a=lookup[(animal,cell,'DFMO')];b=lookup[(animal,cell,'control')]
            max_delta_error=max(max_delta_error,float(np.max(np.abs(independent_logs[:,a]-independent_logs[:,b]-delta[:,j]))))
    if max_delta_error>1e-10:raise ValueError('Independent paired difference disagreement')
    return {'count_collapse_verified':True,'maximum_logCPM_absolute_error':log_error,'maximum_paired_delta_absolute_error':max_delta_error,
            'tolerance_absolute':1e-10,'physical_independence_verified':False}

def make_figures(data,selected,pca,output):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,
                         'axes.titlesize':11,'axes.labelsize':9,'svg.fonttype':'none','pdf.fonttype':42})
    figures=[]
    fig,axes=plt.subplots(1,2,figsize=(11.8,5.5))
    fig.subplots_adjust(top=.77,bottom=.21,wspace=.32)
    fig.suptitle('Bulk RNA context after source-library qualification',x=.06,ha='left',y=.98,fontsize=15,fontweight='bold')
    fig.text(.06,.915,'68-hour in-vitro mouse CD4 T-cell cultures | untreated control versus DFMO\nPCA of all nonconstant deposited genes on log₂(deposited-gene CPM + 1)',fontsize=10,va='top')
    for ax,series,letter in zip(axes,SERIES,'AB'):
        d=pca[pca.series==series]
        for (_,cell),pair in d.groupby(['animal_id','cell_type'],sort=False):
            if len(pair)!=2:raise ValueError('PCA pair incomplete')
            ax.plot(pair.PC1,pair.PC2,color='#999999',linewidth=.6,zorder=1,alpha=.6)
        for row in d.itertuples():
            color=COLORS[row.cell_type]
            ax.scatter(row.PC1,row.PC2,s=44,marker='o' if row.genotype=='WT' else '^',
                       facecolor=color if row.treatment=='DFMO' else 'white',edgecolor=color,linewidth=1.2,zorder=2)
        exp=data[series]['explained']
        ax.set(xlabel=f'PC1 ({exp[0]*100:.1f}% variance)',ylabel=f'PC2 ({exp[1]*100:.1f}% variance)')
        ax.set_title(f'{letter}   {series}\n'+('3 WT animals; 18 libraries' if series==SERIES[0] else '4 WT + 3 KO animals; 28 libraries'),loc='left')
        ax.margins(.14)
    handles=[Line2D([],[],color=c,marker='o',linestyle='',label=k) for k,c in COLORS.items()]
    handles += [Line2D([],[],color='#555555',marker='o',markerfacecolor='white',linestyle='',label='Control (open)'),
                Line2D([],[],color='#555555',marker='o',linestyle='',label='DFMO (filled)'),
                Line2D([],[],color='#555555',marker='^',linestyle='',label='JMJD3 KO (triangle)')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.073),ncol=3,frameon=False)
    fig.text(.06,.018,'Lines connect paired cultures from the same source animal. Studies are analyzed separately; axes are not shared. No DEG-selected PCA or fate inference.',fontsize=8)
    figures.append(('figure_4_bulk_context',fig))

    fig,axes=plt.subplots(3,4,figsize=(14,10.8))
    fig.subplots_adjust(left=.135,right=.98,top=.855,bottom=.1,wspace=.23,hspace=.47)
    fig.suptitle('Prespecified genes: paired response to DFMO',x=.035,ha='left',y=.985,fontsize=16,fontweight='bold')
    fig.text(.035,.942,'Each circle is one source animal’s DFMO − control difference; black diamonds are unweighted means.\nA = GSE162300 (3 WT); B = GSE162382 (4 WT, 3 JMJD3 KO). Lineages and genotypes remain separate.\nEndpoint: Δlog₂(deposited-gene CPM + 1), 68-hour bulk RNA. No p values, DEG calls or biological importance cutoff.',fontsize=10,va='top')
    labels=[x[0]+(' (n=4)' if x[1]==SERIES[1] and x[3]=='WT' else ' (n=3)') for x in GROUPS]
    for index,(ax,gene) in enumerate(zip(axes.flat,GENES)):
        part=selected[selected.gene==gene]
        ax.axvline(0,color='#9CA3AF',linewidth=.7)
        ax.axhline(2.5,color='#D6D6D6',linewidth=.8)
        for row,(label,series,cell,genotype) in enumerate(GROUPS):
            values=part[(part.series==series)&(part.cell_type==cell)&(part.genotype==genotype)].sort_values('animal_id').delta.to_numpy()
            ax.scatter(values,row+np.linspace(-.13,.13,len(values)),s=23,color=COLORS[cell],alpha=.82,zorder=2)
            ax.scatter([values.mean()],[row],s=29,marker='D',color='#111111',zorder=3)
        ax.set_yticks(range(7),labels if index%4==0 else ['']*7)
        ax.set_ylim(6.6,-.6);ax.tick_params(axis='y',length=0,labelsize=8)
        ax.set_title(f'{chr(65+index)}  {DISPLAY[gene]}',loc='left',fontstyle='italic',fontweight='bold')
        ax.set_xlabel('Δlog₂(CPM + 1)',fontsize=8);ax.tick_params(axis='x',labelsize=8)
        ax.margins(x=.18)
    fig.text(.035,.03,'Positive: greater normalized abundance after DFMO. Negative: lower after DFMO. Panel x-axis ranges differ.\nCounts from two technical runs are summed in A. Bulk abundance cannot separate within-cell change from selection, survival or mixture changes.',fontsize=9)
    figures.append(('figure_5_bulk_paired_genes',fig))
    with PdfPages(output/'Wagner_R3_initial_figures.pdf') as pdf:
        for name,fig in figures:
            for ext in ['png','pdf','svg']:fig.savefig(output/f'{name}.{ext}',dpi=300,facecolor='white')
            pdf.savefig(fig,facecolor='white');plt.close(fig)

def main(source,qualification,output):
    save_tsv(pd.DataFrame([{'source_symbol':g,'display_symbol':DISPLAY[g],'mapping':'explicit exact uppercase identifier; no ortholog conversion'} for g in GENES]),output/'gene_identity_map.tsv')
    mapping=pd.read_csv(qualification/'source_sample_map.tsv',sep='\t',keep_default_na=False)
    library_map=pd.read_csv(qualification/'library_design.tsv',sep='\t',keep_default_na=False)
    data={};summaries=[];selected=[];baseline_selected=[];pca_rows=[];library_qc=[];checks={};interactions=[]
    for series,stem in zip(SERIES,['DFMO_RNA','DFMO_JMJD3']):
        raw=source/f'{series}_{stem}_est_counts.csv.gz'
        frame=pd.read_csv(raw,index_col=0,keep_default_na=False,float_precision='round_trip')
        if not set(GENES)<=set(frame.index):raise ValueError('Prespecified gene absent; do not substitute')
        samplemap=mapping[mapping.series==series]
        ids,counts=collapse_counts(frame,samplemap)
        libraries=library_map[library_map.series==series].set_index('library_id').loc[ids].reset_index()
        cpm=counts/counts.sum(axis=0)*1e6;logs=np.log2(cpm+1)
        genes=frame.index.to_numpy(dtype=str);parts=[];deltas={}
        for _,which,cell,genotype in GROUPS:
            if which!=series:continue
            animals,delta=paired_difference(logs,libraries,cell,genotype)
            contrast=f'{cell}.{genotype}.DFMO_minus_control';deltas[contrast]=delta
            summaries.append(summarize(genes,delta,series,contrast));parts.append((cell,genotype,animals,delta))
            for gene in GENES:
                g=frame.index.get_loc(gene)
                for j,animal in enumerate(animals):
                    record=dict(series=series,cell_type=cell,genotype=genotype,gene=gene,animal_id=animal,delta=float(delta[g,j]))
                    for treatment in ['control','DFMO']:
                        i=libraries.index[(libraries.cell_type==cell)&(libraries.animal_id==animal)&(libraries.treatment==treatment)].item()
                        record[treatment+'_log2CPM1']=float(logs[g,i]);record[treatment+'_counts']=float(counts[g,i])
                    selected.append(record)
        if series==SERIES[0]:
            animals=['WT1','WT2','WT3'];baseline=[]
            for animal in animals:
                p=libraries.index[(libraries.animal_id==animal)&(libraries.cell_type=='Th17p')&(libraries.treatment=='control')].item()
                n=libraries.index[(libraries.animal_id==animal)&(libraries.cell_type=='Th17n')&(libraries.treatment=='control')].item()
                baseline.append(logs[:,p]-logs[:,n])
            baseline=np.column_stack(baseline);deltas['WT.control.Th17p_minus_Th17n']=baseline
            summaries.append(summarize(genes,baseline,series,'WT.control.Th17p_minus_Th17n'))
            for gene in GENES:
                g=frame.index.get_loc(gene)
                for j,animal in enumerate(animals):baseline_selected.append(dict(gene=gene,animal_id=animal,delta=float(baseline[g,j])))
        else:
            for cell in ['Th17n','iTreg']:
                wt=deltas[f'{cell}.WT.DFMO_minus_control'];ko=deltas[f'{cell}.JMJD3_KO.DFMO_minus_control']
                interactions.append(pd.DataFrame(dict(gene=genes,cell_type=cell,WT_n=4,KO_n=3,
                    WT_mean_delta=wt.mean(axis=1),KO_mean_delta=ko.mean(axis=1),KO_minus_WT_response=ko.mean(axis=1)-wt.mean(axis=1))))
        checks[series]=independent_check(raw,ids,counts,logs,samplemap,parts,libraries)
        centered=logs-logs.mean(axis=1,keepdims=True);nonconstant=np.ptp(logs,axis=1)>0
        u,s,vh=np.linalg.svd(centered[nonconstant],full_matrices=False)
        coords=vh[:2].T*s[:2];explained=s*s/np.sum(s*s)
        gram=centered[nonconstant].T@centered[nonconstant]
        eigenvalues=np.linalg.eigvalsh(gram)[::-1]
        if not np.allclose(s[:2]**2,eigenvalues[:2],rtol=1e-10):raise ValueError('PCA eigenvalue verification failed')
        checks[series]['pca_svd_gram_agree']=True
        for i,r in libraries.iterrows():
            pca_rows.append(dict(**r.to_dict(),PC1=coords[i,0],PC2=coords[i,1]))
            library_qc.append(dict(series=series,library_id=r.library_id,animal_id=r.animal_id,
                estimated_count_total=float(counts[:,i].sum()),positive_genes=int((counts[:,i]>0).sum())))
        np.savez_compressed(output/f'{series}_expression_arrays.npz',genes=genes,library_ids=np.asarray(ids),counts=counts,log2CPM1=logs,**deltas)
        data[series]={'genes':len(genes),'nonconstant_pca_genes':int(nonconstant.sum()),'libraries':len(ids),'explained':explained[:2].tolist()}
    summaries=pd.concat(summaries,ignore_index=True);selected=pd.DataFrame(selected);pca=pd.DataFrame(pca_rows)
    with gzip.open(output/'all_gene_paired_summaries.tsv.gz','wt',encoding='utf-8',newline='') as f:save_tsv(summaries,f)
    interactions=pd.concat(interactions,ignore_index=True)
    with gzip.open(output/'all_gene_genotype_response_differences.tsv.gz','wt',encoding='utf-8',newline='') as f:save_tsv(interactions,f)
    save_tsv(selected,output/'prespecified_gene_animal_changes.tsv')
    save_tsv(summaries[summaries.gene.isin(GENES)],output/'prespecified_gene_summaries.tsv')
    save_tsv(interactions[interactions.gene.isin(GENES)],output/'prespecified_genotype_response_differences.tsv')
    save_tsv(pd.DataFrame(baseline_selected),output/'prespecified_baseline_p_vs_n.tsv')
    save_tsv(pca,output/'pca_coordinates.tsv');save_tsv(pd.DataFrame(library_qc),output/'collapsed_library_qc.tsv')
    make_figures(data,selected,pca,output)
    captions='''# Wagner R3 initial descriptive figures

Both plates: exposed descriptive reanalysis of 68-hour in-vitro mouse CD4 T-cell bulk RNA. A denotes GSE162300, WT Th17p/Th17n/iTreg, vehicle versus DFMO, three source animal labels with paired cultures. Two sequencing runs of each library are summed as fractional expected counts. B denotes GSE162382, Th17n/iTreg, control versus DFMO, four WT and three JMJD3 conditional-KO animal labels; no Th17p is deposited. Series are kept separate. The source figure legend states n=4, but the deposited KO allocation is three; no replicate is imputed.

Figure 4: PCA uses every nonconstant deposited gene, centered across libraries on log2(deposited-gene CPM + 1), without variance scaling or source DEG selection. Points are libraries; grey lines connect within-animal cultures. Color denotes lineage, fill denotes treatment, and triangles denote KO. Each study has its own fit and axes. This is exploratory transcriptome context, not the source figure's PCA on 3,414 selected genes. Variance fractions describe these data only.

Figure 5: All twelve genes named in the frozen contract are shown, with no effect-dependent selection: Odc1, Srm, Sms, Sat1 and Smox (polyamine context); Pgam1, Ldha and Tpi1 (glycolytic context); Foxp3, Rorc and Il17a (lineage context); Kdm6b (JMJD3 transcript). Each point is the paired DFMO-minus-control difference for one animal label; vertical jitter only separates points. Diamonds show unweighted means, not confidence limits. X-axis ranges differ, so read tick values. No p values or biologically meaningful cutoff is supplied. Transcript abundance is not enzyme catalytic activity; Kdm6b abundance does not confirm deletion of the targeted functional exon. Separate tables report baseline Th17p-minus-Th17n vehicle differences and the direct KO-minus-WT difference of average DFMO responses.

CPM uses the sum of the deposited protein-coding expected counts. It is a relative compositional scale, not absolute RNA per cell, TPM, TMM/voom normalization or a source limma reconstruction. The +1 CPM offset limits the interpretation of near-zero genes. Animal-level observed spread is shown; small source groups and unverified physical preparation independence restrict inference. Bulk changes cannot discriminate within-cell reprogramming from selection, survival, proliferation or mixture changes. Neither plate establishes fate, suppression, pathogenicity, demethylation or mediation.
'''
    (output/'CAPTIONS.md').write_text(captions,encoding='utf-8')
    report={'scope':'Exposed animal-paired descriptive bulk RNA analysis; no differential-expression significance or source-program reconstruction',
            'series':data,'genes_prespecified':GENES,'summary_rows':len(summaries),'selected_animal_changes':len(selected),
            'endpoint':'DFMO minus control in log2(deposited-gene CPM + 1); within-animal pairing, mean and observed spread. Additional untreated Th17p minus Th17n and KO minus WT average-response contrasts.',
            'biological_unit_limit':'Source animal labels; preparation independence not physically audited. Technical runs never count as animals.',
            'independent_verification':checks,'source_limma_reproduction':'not performed; R/limma runtime and exact source analysis choices remain to qualify',
            'environment':{'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,'matplotlib':matplotlib.__version__}}
    (output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.suffix in ['.png','.pdf','.svg']}
    (output/'figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'series':data,'independent_checks':checks,'figures':len(manifest)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--qualification',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.source,a.qualification,a.output)
