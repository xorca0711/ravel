"""Fixed mixed-class inclusion sensitivity on frozen target count tables."""
import argparse, json, math, sys
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common_v1 import ROOT, EXT, RUNS, read_csv, save_csv, save_json
from verify_x1_v1 import verify
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    out=ROOT/a.output;out.mkdir(exist_ok=True,parents=True)
    spec=json.loads((EXT/'config/x1_spec_v1.json').read_text())
    original=json.loads((ROOT/spec['original_spec']).read_text())
    ann=RUNS/'Yd1_annotation_v1';rna=RUNS/'Yd1_rna_endpoints_v1'
    cells=read_csv(rna/'cell_endpoints.csv');labels=read_csv(ann/'cell_labels.csv')
    key=lambda r:(r['gsm'],r['barcode'])
    labs={key(r):r for r in labels};assert len(labs)==len(labels)==len(cells)==spec['expected_barcodes']
    assert len(set(map(key,cells)))==len(cells) and set(map(key,cells))==set(labs)
    conditions={gsm:condition for condition,gsms in original['conditions'].items() for gsm in gsms}
    for r in cells:
        assert r['condition']==conditions[r['gsm']]
        assert r['label'] in spec['labels']
        for field in ['label','qc_primary','qc_broad','total_counts']:assert r[field]==labs[key(r)][field]
        assert int(r['total_counts'])>0 and all(int(r[g+'_counts'])>=0 for g in ['Arg1','Il6'])
    support={(r['gsm'],r['qc_mode'],r['label']):r for r in read_csv(ann/'class_eligibility.csv')}
    composition={(r['gsm'],r['qc_mode'],r['label']):r for r in read_csv(ann/'composition.csv')}
    old={(r['gsm'],r['qc_mode'],r['endpoint']):r for r in read_csv(rna/'library_endpoints.csv')}
    membership=[dict(gsm=r['gsm'],barcode=r['barcode'],label=r['label'],qc_primary=r['qc_primary'],qc_broad=r['qc_broad'],in_mac_core=int(r['label']=='macrophage_like'),in_mac_plus_mixed=int(r['label'] in ['macrophage_like',spec['mixed_label']]),in_fib_core=int(r['label']=='fibroblast_like'),in_fib_plus_mixed=int(r['label'] in ['fibroblast_like',spec['mixed_label']])) for r in cells]
    attribution=[];summaries=[];lookup={};core_checks=0
    metrics=[original['primary_metric']]+original['companion_metrics']
    for gsm in sorted(conditions):
        cc=[r for r in cells if r['gsm']==gsm]
        for mode in original['qc_modes']:
            retained=[r for r in cc if r['qc_'+mode]=='1']
            for gene in ['Arg1','Il6']:
                all_target=sum(int(r[gene+'_counts']) for r in retained)
                for label in spec['labels']:
                    rr=[r for r in retained if r['label']==label];n=len(rr)
                    assert n==int(composition[(gsm,mode,label)]['n'])
                    count=sum(int(r[gene+'_counts']) for r in rr)
                    attribution.append(dict(gsm=gsm,condition=conditions[gsm],qc_mode=mode,label=label,gene=gene,n_cells=n,target_count_total=count,detected_cells=sum(int(r[gene+'_counts'])>0 for r in rr),detection_fraction=sum(int(r[gene+'_counts'])>0 for r in rr)/n if n else '',all_qc_target_counts=all_target,share_all_qc_target_counts=count/all_target if all_target else '',share_status='defined' if all_target else 'undefined_zero_target_total',qc_excluded_cells=len(cc)-len(retained)))
            for endpoint in original['endpoints']:
                for inclusion in spec['inclusion_sets']:
                    included=[endpoint['cell_class']]+([spec['mixed_label']] if inclusion=='core_plus_mixed' else [])
                    rr=[r for r in retained if r['label'] in included]
                    sup=support[(gsm,mode,endpoint['cell_class'])];eligible=int(sup['eligible'])
                    if inclusion=='core':assert len(rr)==int(sup['n'])
                    row=dict(gsm=gsm,condition=conditions[gsm],qc_mode=mode,endpoint=endpoint['id'],cell_class=endpoint['cell_class'],gene=endpoint['gene'],inclusion_set=inclusion,core_eligible=eligible,n_cells=len(rr),gene_counts='',total_counts='',detection_fraction='',mean_per10k='',mean_log1p_per10k='',pseudobulk_cpm='')
                    if eligible:
                        counts=np.array([int(r[endpoint['gene']+'_counts']) for r in rr],dtype=np.int64)
                        totals=np.array([int(r['total_counts']) for r in rr],dtype=np.int64)
                        norm=counts/totals*10000.
                        row.update(gene_counts=int(counts.sum()),total_counts=int(totals.sum()),detection_fraction=float(np.mean(counts>0)),mean_per10k=float(np.mean(norm)),mean_log1p_per10k=float(np.log1p(norm).mean()),pseudobulk_cpm=float(counts.sum()/totals.sum()*1e6))
                        if inclusion=='core':
                            prev=old[(gsm,mode,endpoint['id'])]
                            for field in metrics+['gene_counts','total_counts','n_cells']:
                                assert math.isclose(float(row[field]),float(prev[field]),rel_tol=1e-11,abs_tol=1e-12),(gsm,mode,field)
                                core_checks+=1
                    summaries.append(row);lookup[(gsm,mode,endpoint['id'],inclusion)]=row
    contrasts=[];crossed=[]
    for mode in original['qc_modes']:
        for comp in original['comparisons']:
            for inclusion in spec['inclusion_sets']:
                target=[lookup[(gsm,mode,comp['endpoint'],inclusion)] for gsm in original['conditions'][comp['target']]]
                ref=[lookup[(gsm,mode,comp['endpoint'],inclusion)] for gsm in original['conditions'][comp['reference']]]
                eligible=all(r['core_eligible'] for r in target+ref) and len(target)==len(ref)==2
                for metric in metrics:
                    d=lo=hi=''
                    if eligible:
                        differences=[x[metric]-y[metric] for x in target for y in ref]
                        d=float(np.mean([x[metric] for x in target])-np.mean([y[metric] for y in ref]));lo=min(differences);hi=max(differences)
                        for x in target:
                            for y in ref:crossed.append(dict(qc_mode=mode,comparison=comp['id'],inclusion_set=inclusion,metric=metric,target_library=x['gsm'],reference_library=y['gsm'],difference=x[metric]-y[metric]))
                    contrasts.append(dict(qc_mode=mode,comparison=comp['id'],inclusion_set=inclusion,endpoint=comp['endpoint'],metric=metric,eligible=int(eligible),equal_library_mean_difference=d,crossed_difference_min=lo,crossed_difference_max=hi,uncertainty='four crossed differences; no interval or independent replication'))
    save_csv(out/'barcode_membership.csv',membership);save_csv(out/'target_attribution.csv',attribution)
    save_csv(out/'library_endpoints.csv',summaries);save_csv(out/'condition_contrasts.csv',contrasts);save_csv(out/'crossed_library_differences.csv',crossed)
    check=verify(out);check.update(core_saved_value_checks=core_checks,all_barcode_label_QC_count_joins=True)
    save_json(out/'independent_verification.json',check)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axes=plt.subplots(2,3,figsize=(13.5,8))
    titles=['Macrophage-like Arg1\nKO minus WT coculture','Fibroblast-like Il6\nKO minus WT coculture','Fibroblast-like Il6\nWT coculture minus alone']
    views=[('primary','core'),('broad','core'),('primary','core_plus_mixed'),('broad','core_plus_mixed')]
    for j,comp in enumerate(original['comparisons']):
        for k,metric in enumerate(['mean_log1p_per10k','detection_fraction']):
            ax=axes[k,j];ax.axvline(0,color='#999999',linewidth=1)
            for i,(mode,inclusion) in enumerate(views):
                row=next(r for r in contrasts if (r['comparison'],r['qc_mode'],r['inclusion_set'],r['metric'])==(comp['id'],mode,inclusion,metric))
                if row['eligible']:
                    color='#24678D' if inclusion=='core' else '#C6642D'
                    ax.hlines(i,row['crossed_difference_min'],row['crossed_difference_max'],color=color,linewidth=2)
                    ax.scatter(row['equal_library_mean_difference'],i,color=color,marker='o' if mode=='primary' else 's',zorder=3)
            ax.set_yticks(range(4),['Core / primary','Core / broad','+ Mixed / primary','+ Mixed / broad']);ax.invert_yaxis();ax.set_ylim(3.5,-.5)
            ax.set_xlabel('Difference in mean log1p(counts per 10,000)' if k==0 else 'Difference in detection fraction')
            ax.grid(axis='x',alpha=.15)
            if k==0:ax.set_title(titles[j],loc='left',fontsize=11,pad=12)
    fig.suptitle('Fixed mixed-cell inclusion: library-level sensitivity',x=.05,ha='left',fontsize=15)
    fig.subplots_adjust(left=.15,right=.98,top=.83,bottom=.19,wspace=.72,hspace=.48)
    fig.text(.05,.055,'Dots/squares: difference of equal-weight means of two libraries per condition. Lines: all four crossed-library differences.\nBoth cell sets and QC masks overlap; lines are descriptive ranges, not confidence intervals. Mixed cells are not reassigned to a lineage.\nUnknown preparations, ambient RNA and cell selection remain unresolved. All four metrics and all barcodes are in the accompanying tables.',fontsize=9)
    fig.savefig(out/'inclusion.png',dpi=180);fig.savefig(out/'inclusion.pdf');plt.close(fig)
    colors=['#24678D','#C6642D','#8060AA','#999999','#D9D9D9']
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    for i,mode in enumerate(original['qc_modes']):
        for j,gene in enumerate(['Arg1','Il6']):
            ax=axes[i,j];bottom=np.zeros(6);gsms=sorted(conditions)
            for label,color in zip(spec['labels'],colors):
                vals=[]
                for gsm in gsms:
                    r=next(r for r in attribution if (r['gsm'],r['qc_mode'],r['gene'],r['label'])==(gsm,mode,gene,label))
                    vals.append(float(r['share_all_qc_target_counts']) if r['share_status']=='defined' else 0.)
                ax.bar(range(6),vals,bottom=bottom,color=color,label=label);bottom+=vals
            for idx,gsm in enumerate(gsms):
                if any(r['gsm']==gsm and r['qc_mode']==mode and r['gene']==gene and r['share_status']=='undefined_zero_target_total' for r in attribution):
                    ax.text(idx,.5,'undefined',rotation=90,ha='center',va='center',fontsize=8)
            ax.set_title(gene+' raw-count attribution · '+mode+' QC',loc='left')
            ax.set_xticks(range(6),[g[-3:] for g in gsms]);ax.set_xlabel('GSM7764 suffix (not preparation ID)');ax.set_ylabel('Share of all retained target counts');ax.set_ylim(0,1.02)
    handles,labels_=axes[0,0].get_legend_handles_labels()
    fig.legend(handles,labels_,loc='lower center',ncol=3,frameon=False,fontsize=8,bbox_to_anchor=(.5,.07))
    fig.suptitle('Original labels retain all QC-passed target counts',x=.07,ha='left',fontsize=15)
    fig.subplots_adjust(top=.88,bottom=.23,hspace=.55,wspace=.25)
    fig.text(.07,.025,'Transcript shares depend on depth and capture; they are not protein-source fractions. All original labels and excluded-cell counts remain visible.',fontsize=8)
    fig.savefig(out/'attribution.png',dpi=180);fig.savefig(out/'attribution.pdf');plt.close(fig)
    save_json(out/'runtime.json',dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,population_tests=False,scientific_acceptance='not_assessed'))
    print('Fixed inclusion diagnostic complete; independent arithmetic and saved-core checks passed')
if __name__=='__main__':main()
