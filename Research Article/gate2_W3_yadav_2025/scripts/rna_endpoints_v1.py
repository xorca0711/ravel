"""Library-level descriptive endpoints using frozen conservative annotations."""
import argparse,csv,json,math,sys,tarfile
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from count_integrity_v1 import read_library,ROOT,ARCHIVE,INVENTORY
from verify_rna_counts_v1 import stream_library,independent_summary
ART=ROOT/'Research Article/gate2_W3_yadav_2025';ANNOT=ROOT/'analysis/research/runs/Yd1_annotation_v1'

def read_csv(p):return list(csv.DictReader(p.open(encoding='utf-8')))
def save_csv(p,rows):
    with p.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output;out.mkdir(exist_ok=True,parents=True)
    spec=json.loads((ART/'config/rna_endpoints_spec_v1.json').read_text());samples=json.loads(INVENTORY.read_text())
    labels={(r['gsm'],r['barcode']):r for r in read_csv(ANNOT/'cell_labels.csv')}
    support={(r['gsm'],r['qc_mode'],r['label']):r for r in read_csv(ANNOT/'class_eligibility.csv')}
    conditions={gsm:c for c,gsms in spec['conditions'].items() for gsm in gsms}
    metrics=[spec['primary_metric']]+spec['companion_metrics'];summaries=[];cells=[];checks=[];lookup={}
    with tarfile.open(ARCHIVE) as tar:
        for s in samples:
            m,features,barcodes,integrity=read_library(tar,s)
            total=np.asarray(m.sum(axis=0)).ravel().astype(np.int64);gs=np.asarray((m>0).sum(axis=0)).ravel()
            labs=[labels[(s['gsm'],bc)] for bc in barcodes]
            target={}
            for endpoint in spec['endpoints']:
                indices=[i for i,f in enumerate(features) if f[1]==endpoint['gene']];assert len(indices)==1
                target[endpoint['gene']]=np.asarray(m[indices[0]].toarray()).ravel()
            independent_total,independent_genes,independent_target,entries=stream_library(tar,s,list(target))
            assert np.array_equal(total,independent_total) and np.array_equal(gs,independent_genes)
            for gene in target:assert np.array_equal(target[gene],independent_target[gene])
            for i,bc in enumerate(barcodes):
                lab=labs[i];assert int(lab['total_counts'])==total[i]
                cells.append(dict(gsm=s['gsm'],condition=conditions[s['gsm']],barcode=bc,label=lab['label'],
                    qc_primary=lab['qc_primary'],qc_broad=lab['qc_broad'],total_counts=int(total[i]),
                    Arg1_counts=int(target['Arg1'][i]),Il6_counts=int(target['Il6'][i])))
            for mode in spec['qc_modes']:
                for endpoint in spec['endpoints']:
                    mask=np.array([r['label']==endpoint['cell_class'] and r['qc_'+mode]=='1' for r in labs])
                    sup=support[(s['gsm'],mode,endpoint['cell_class'])];n=int(mask.sum());assert n==int(sup['n'])
                    row=dict(gsm=s['gsm'],condition=conditions[s['gsm']],qc_mode=mode,endpoint=endpoint['id'],cell_class=endpoint['cell_class'],
                        gene=endpoint['gene'],eligible=int(sup['eligible']),n_cells=n,gene_counts='',total_counts='',detection_fraction='',
                        mean_per10k='',mean_log1p_per10k='',pseudobulk_cpm='')
                    if row['eligible']:
                        counts=target[endpoint['gene']][mask];den=total[mask];norm=counts/den*1e4
                        row.update(gene_counts=int(counts.sum()),total_counts=int(den.sum()),detection_fraction=float(np.mean(counts>0)),
                            mean_per10k=float(np.mean(norm)),mean_log1p_per10k=float(np.mean(np.log1p(norm))),pseudobulk_cpm=float(counts.sum()/den.sum()*1e6))
                        verified=independent_summary(independent_target[endpoint['gene']],independent_total,mask)
                        for key,value in verified.items():assert math.isclose(value,row[key],rel_tol=1e-11,abs_tol=1e-12),(s['gsm'],mode,key)
                    summaries.append(row);lookup[(s['gsm'],mode,endpoint['id'])]=row
            checks.append(dict(gsm=s['gsm'],independent_entries=entries,all_cell_totals_match=True,detected_genes_match=True,
                all_cell_Arg1_Il6_counts_match=True,independent_summary_arithmetic='passed'))
            print(s['gsm'],'descriptive endpoints and independent stream verification complete',flush=True)
    comparisons=[];crossed=[]
    for mode in spec['qc_modes']:
        for comp in spec['comparisons']:
            aa=[lookup[(gsm,mode,comp['endpoint'])] for gsm in spec['conditions'][comp['target']]]
            bb=[lookup[(gsm,mode,comp['endpoint'])] for gsm in spec['conditions'][comp['reference']]]
            eligible=all(r['eligible'] for r in aa+bb) and len(aa)>=spec['minimum_eligible_libraries_per_condition'] and len(bb)>=spec['minimum_eligible_libraries_per_condition']
            for metric in metrics:
                delta=low=high=''
                if eligible:
                    differences=[x[metric]-y[metric] for x in aa for y in bb]
                    delta=float(np.mean([x[metric] for x in aa])-np.mean([y[metric] for y in bb]));low=min(differences);high=max(differences)
                    for x in aa:
                        for y in bb:crossed.append(dict(qc_mode=mode,comparison=comp['id'],metric=metric,target_library=x['gsm'],reference_library=y['gsm'],difference=x[metric]-y[metric]))
                comparisons.append(dict(qc_mode=mode,comparison=comp['id'],endpoint=comp['endpoint'],target=comp['target'],reference=comp['reference'],
                    metric=metric,eligible=int(eligible),equal_library_mean_difference=delta,crossed_difference_min=low,crossed_difference_max=high,
                    uncertainty='descriptive crossed-library range; not confidence interval or independent replication'))
    save_csv(out/'cell_endpoints.csv',cells);save_csv(out/'library_endpoints.csv',summaries);save_csv(out/'condition_contrasts.csv',comparisons);save_csv(out/'crossed_library_differences.csv',crossed)
    (out/'independent_verification.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axes=plt.subplots(2,3,figsize=(12,8));colors={'primary':'#226B96','broad':'#C65E27'}
    names={'Fib_alone':'Fib\nalone','WT_coculture':'WT\ncoculture','KO_coculture':'KO Fib\ncoculture'}
    titles=['Macrophage-like Arg1\nKO versus WT fibroblast coculture','Fibroblast-like Il6\nKO versus WT fibroblast coculture','Fibroblast-like Il6\nWT coculture versus fibroblast alone']
    for j,comp in enumerate(spec['comparisons']):
        for row,metric in enumerate(['mean_log1p_per10k','detection_fraction']):
            ax=axes[row,j]
            for i,condition in enumerate([comp['reference'],comp['target']]):
                for mode in spec['qc_modes']:
                    rows=[lookup[(gsm,mode,comp['endpoint'])] for gsm in spec['conditions'][condition]]
                    values=[r[metric] for r in rows if r['eligible']]
                    off=-.09 if mode=='primary' else .09
                    if values:
                        ax.scatter(i+off+np.linspace(-.025,.025,len(values)),values,s=35,color=colors[mode],label=mode+' QC' if i==0 else None,zorder=3)
                        ax.hlines(np.mean(values),i+off-.055,i+off+.055,color=colors[mode],linewidth=2)
                    for k,r in enumerate(rows):
                        if mode=='primary' and r['eligible']:
                            ax.annotate(r['gsm'][-3:],(i+off+(-.025 if k==0 else .025),r[metric]),xytext=(-5,6 if k==0 else -12),textcoords='offset points',fontsize=7)
            ax.set_xticks([0,1],[names[comp['reference']],names[comp['target']]])
            ax.set_xlim(-.45,1.45);ax.grid(axis='y',alpha=.15)
            ax.set_ylabel('Mean log1p(counts per 10,000)' if row==0 else 'Fraction with nonzero counts')
            if row==0:ax.set_title(titles[j],loc='left',fontsize=10,pad=10)
            if row==1:ax.set_ylim(-.025,1.025)
            else:
                lo,hi=ax.get_ylim();ax.set_ylim(bottom=min(-.02,lo),top=hi*1.15+.03)
            if j==0 and row==0:ax.legend(frameon=False,fontsize=8)
    fig.suptitle('Coculture RNA: library-level descriptions on nonintegrated counts',x=.07,ha='left',fontsize=14)
    fig.subplots_adjust(left=.07,right=.98,top=.82,bottom=.18,wspace=.43,hspace=.55)
    fig.text(.07,.045,'Each point is one library summary; bars give equal-library means. Labels are GEO suffixes, not preparation IDs.\nPrimary and broad QC are prespecified sensitivity views. Core classes are marker adaptations; composition is reported separately.\nNo cell-based population tests, suffix pairing, flux or independent-replication claim.',fontsize=8)
    fig.savefig(out/'rna.png',dpi=200,bbox_inches='tight');fig.savefig(out/'rna.pdf',bbox_inches='tight');plt.close(fig)
    (out/'runtime.json').write_text(json.dumps(dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,population_tests=False,independent_preparations=False,scientific_acceptance='not_assessed'),indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
