"""Frozen conservative annotation without evaluating Arg1 or Il6."""
import argparse,csv,json,sys,tarfile
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from count_integrity_v1 import read_library,ROOT,ARCHIVE,INVENTORY
ART=ROOT/'Research Article/gate2_W3_yadav_2025'
QC=ROOT/'analysis/research/runs/Yd1_count_integrity_v1/cell_qc.csv'

def save_csv(p,rows):
    with p.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output;out.mkdir(exist_ok=True,parents=True)
    spec=json.loads((ART/'config/annotation_spec_v1.json').read_text());samples=json.loads(INVENTORY.read_text())
    qcs={(r['gsm'],r['barcode']):r for r in csv.DictReader(QC.open())}
    markers=sorted(set(spec['fibroblast_markers']+spec['macrophage_markers']+
        sum(spec['heldout'].values(),[])+sum(spec['other_pairs'],[])))
    assert not set(markers)&set(spec['endpoint_genes_excluded_from_annotation'])
    cells=[];composition=[];support=[];marker_rows=[]
    with tarfile.open(ARCHIVE) as tar:
        for sample in samples:
            m,features,barcodes,check=read_library(tar,sample)
            index={gene:[i for i,f in enumerate(features) if f[1]==gene] for gene in markers}
            assert all(len(v)==1 for v in index.values()),index
            counts={gene:np.asarray(m[ix[0]].toarray()).ravel() for gene,ix in index.items()}
            yes={g:counts[g]>=spec['marker_count_min'] for g in markers}
            score=lambda gs:np.sum([yes[g] for g in gs],axis=0)
            fs=score(spec['fibroblast_markers']);ms=score(spec['macrophage_markers'])
            fib=(fs>=3)&(score(spec['fibroblast_core'])>=2)
            mac=(ms>=3)&(score(spec['macrophage_anchors'])>=1)
            other=np.any([yes[x]&yes[y] for x,y in spec['other_pairs']],axis=0)
            labels=np.full(len(barcodes),'unassigned',dtype=object)
            labels[fib&~mac]='fibroblast_like';labels[mac&~fib]='macrophage_like'
            labels[fib&mac]='mixed_fibroblast_macrophage';labels[other]='other_or_mixed'
            qs=[qcs[(sample['gsm'],bc)] for bc in barcodes]
            total=np.array([int(q['total_counts']) for q in qs]);genes=np.array([int(q['detected_genes']) for q in qs]);mito=np.array([float(q['mitochondrial_percent']) for q in qs])
            assert np.array_equal(total,np.asarray(m.sum(axis=0)).ravel())
            masks={}
            for mode,key in [('primary','qc_primary'),('broad','qc_broad')]:
                rule=spec[key];keep=(genes>=rule['minimum_genes'])&(mito<=rule['maximum_mitochondrial_percent'])
                if rule['maximum_genes'] is not None:keep&=genes<=rule['maximum_genes']
                masks[mode]=keep
            for i,bc in enumerate(barcodes):
                cells.append(dict(gsm=sample['gsm'],barcode=bc,label=labels[i],fibroblast_marker_count=int(fs[i]),macrophage_marker_count=int(ms[i]),
                    other_lineage_flag=int(other[i]),qc_primary=int(masks['primary'][i]),qc_broad=int(masks['broad'][i]),
                    total_counts=int(total[i]),detected_genes=int(genes[i]),mitochondrial_percent=float(mito[i])))
            for mode,keep in masks.items():
                for label in spec['labels']+['qc_excluded']:
                    mask=keep&(labels==label) if label!='qc_excluded' else ~keep;n=int(mask.sum())
                    composition.append(dict(gsm=sample['gsm'],title=sample['title'],qc_mode=mode,label=label,n=n,total_deposited=len(barcodes),fraction_deposited=n/len(barcodes),fraction_qc_passed=n/int(keep.sum()) if label!='qc_excluded' else ''))
                    if label in spec['heldout']:
                        fraction=float(np.mean(np.any([yes[g][mask] for g in spec['heldout'][label]],axis=0))) if n else 0.
                        eligible=n>=spec['minimum_class_cells'] and fraction>=spec['minimum_heldout_fraction']
                        support.append(dict(gsm=sample['gsm'],title=sample['title'],qc_mode=mode,label=label,n=n,
                            heldout_marker_fraction=fraction,eligible=int(eligible),hold_reason='' if eligible else 'class coverage or heldout compatibility below fixed descriptive threshold'))
                    for gene in markers:
                        marker_rows.append(dict(gsm=sample['gsm'],qc_mode=mode,label=label,gene=gene,n=n,
                            fraction_ge2=float(np.mean(yes[gene][mask])) if n else '',
                            mean_log1p_per10k=float(np.mean(np.log1p(counts[gene][mask]/total[mask]*1e4))) if n else ''))
            print(sample['gsm'],'annotation and two fixed QC views complete',flush=True)
    save_csv(out/'cell_labels.csv',cells);save_csv(out/'composition.csv',composition);save_csv(out/'class_eligibility.csv',support);save_csv(out/'marker_support.csv',marker_rows)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axes=plt.subplots(1,2,figsize=(13,5.4),gridspec_kw={'width_ratios':[1,1.3]})
    ax=axes[0];bottom=np.zeros(6);palette=['#226B96','#C65E27','#9B7CA5','#8DAD8E','#B9B9B9','#E5E5E5']
    for label,color in zip(spec['labels']+['qc_excluded'],palette):
        v=np.array([next(r['fraction_deposited'] for r in composition if r['gsm']==s['gsm'] and r['qc_mode']=='primary' and r['label']==label) for s in samples])
        ax.bar(range(6),v,bottom=bottom,color=color,label=label.replace('_',' '));bottom+=v
    ax.set_xticks(range(6),['Fib1','WT co1','KO co1','Fib2','WT co2','KO co2'],rotation=45,ha='right');ax.set_ylabel('Fraction of deposited barcodes');ax.set_ylim(0,1)
    ax.set_title('Primary QC: conservative class composition',loc='left',fontsize=10)
    ax.legend(loc='upper left',bbox_to_anchor=(0,-.31),ncol=2,frameon=False,fontsize=7)
    display=spec['fibroblast_markers'][:2]+['Dcn','Pdgfra']+spec['macrophage_anchors']+['Cd68']+spec['heldout']['fibroblast_like']+spec['heldout']['macrophage_like']
    rowids=[(s['gsm'],c) for s in samples for c in ['fibroblast_like','macrophage_like']]
    z=np.array([[next(float(r['fraction_ge2']) if r['fraction_ge2']!='' else np.nan for r in marker_rows if r['gsm']==gsm and r['label']==c and r['gene']==g and r['qc_mode']=='primary') for g in display] for gsm,c in rowids])
    ax=axes[1];im=ax.imshow(z,aspect='auto',vmin=0,vmax=1,cmap='Blues')
    ax.set_xticks(range(len(display)),display,rotation=60,ha='right',fontsize=8)
    ax.set_yticks(range(len(rowids)),[g[-3:]+(' Fib' if c=='fibroblast_like' else ' Mac') for g,c in rowids],fontsize=8)
    ax.set_title('Marker compatibility (fraction with >=2 counts)',loc='left',fontsize=10);fig.colorbar(im,ax=ax,fraction=.04,pad=.02)
    fig.suptitle('Conservative marker adaptation: class support before endpoint analysis',x=.07,ha='left',fontsize=14)
    fig.subplots_adjust(left=.07,right=.98,top=.84,bottom=.29,wspace=.42)
    fig.text(.07,-.03,'Ambiguous/other/unassigned cells are retained. Arg1 and Il6 are excluded from annotation.\nNo exact SingleR reproduction, validated lineage, doublet exclusion or independent-preparation claim.',fontsize=8)
    fig.savefig(out/'annotation.png',dpi=200,bbox_inches='tight');fig.savefig(out/'annotation.pdf',bbox_inches='tight');plt.close(fig)
    (out/'runtime.json').write_text(json.dumps(dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,endpoint_genes_used_or_summarized=False,scientific_acceptance='not_assessed'),indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
