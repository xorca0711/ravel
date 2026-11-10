"""Run the released numerical core, verify all outputs independently, render diagnostics."""
import argparse
import csv
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HOME = Path('Research Article/gate3_11_zhang_2026_nk')
SOURCE = Path('raw_data/zhang_2026/source_v1/author')
CONTRASTS = ['itdt_vs_pbs', 'itdt_acd4_vs_pbs', 'itdt_acd4_vs_itdt']
ABS_TOL, REL_TOL = 1e-8, 1e-7


def rows(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def indexed(path):
    data = rows(path)
    key = next(iter(data[0]))
    assert len({r[key] for r in data}) == len(data)
    return {r[key]: r for r in data}


def array(path):
    data = indexed(path)
    columns = list(next(iter(data.values())))[1:]
    return list(data), columns, np.array([[float(r[c]) for c in columns] for r in data.values()])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    subprocess.run([shutil.which('Rscript'), '--vanilla', str(HOME/'scripts/reproduce_v1.R'), str(out)], check=True)
    reports = []
    tables = {}
    for contrast in CONTRASTS:
        observed = indexed(out/(contrast+'_nk.csv'))
        reference = indexed(SOURCE/'output_files'/(contrast+'_nk.csv'))
        shared = sorted(observed.keys() & reference.keys())
        fields = ['logFC', 'AveExpr', 't', 'P.Value', 'adj.P.Val', 'B']
        comparison = {}
        for field in fields:
            a = np.array([float(observed[g][field]) for g in shared])
            b = np.array([float(reference[g][field]) for g in shared])
            delta = np.abs(a-b)
            comparison[field] = {'max_absolute_difference': float(delta.max()),
                                 'outside_tolerance': int(np.sum(delta > ABS_TOL+REL_TOL*np.abs(b)))}
        reports.append({'contrast': contrast, 'shared_genes': len(shared),
                        'missing': sorted(reference.keys()-observed.keys()),
                        'excess': sorted(observed.keys()-reference.keys()), 'fields': comparison})
        tables[contrast] = observed
    genes, samples, logtpm = array(out/'logTPM.csv')
    _, _, design = array(out/'design.csv')
    coef = np.linalg.lstsq(design, logtpm.T, rcond=None)[0]
    checks = []
    for contrast, indices in zip(CONTRASTS, [(1, 0), (2, 0), (2, 1)]):
        actual = np.array([float(tables[contrast][g]['logFC']) for g in genes])
        delta = np.max(np.abs(actual-(coef[indices[0]]-coef[indices[1]])))
        assert delta < ABS_TOL
        p = np.array([float(tables[contrast][g]['P.Value']) for g in genes])
        order = np.argsort(p)
        adjusted = np.minimum(1, np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1])
        expected = np.array([float(tables[contrast][g]['adj.P.Val']) for g in genes])[order]
        bh_error = float(np.max(np.abs(adjusted-expected)))
        assert bh_error < ABS_TOL
        checks.append({'contrast': contrast, 'independent_numpy_OLS_max_error': float(delta), 'BH_max_error': bh_error})
    _, _, adjusted = array(out/'block_adjusted_logTPM.csv')
    correction_error = float(np.max(np.abs(adjusted-(logtpm-(design[:,3:]@coef[3:]).T))))
    assert correction_error < ABS_TOL
    comparison = {'absolute_tolerance': ABS_TOL, 'relative_tolerance': REL_TOL,
                  'tolerance_basis': 'Conservative float64/15-significant-digit CSV comparison; not an effect margin.',
                  'all_genes_all_fields': reports, 'independent_checks': checks,
                  'block_correction_max_error': correction_error,
                  'source_concordant': all(not r['missing'] and not r['excess'] and all(v['outside_tolerance']==0 for v in r['fields'].values()) for r in reports)}
    (out/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n',encoding='utf-8')
    summaries = []
    for contrast in CONTRASTS:
        data=tables[contrast]
        summaries.append({'contrast':contrast,'tested_genes':len(data),
                          'BH_lt_0.05':sum(float(r['adj.P.Val'])<0.05 for r in data.values()),
                          'source_display_up':sum(float(r['adj.P.Val'])<0.05 and float(r['logFC'])>1.5 for r in data.values()),
                          'source_display_down':sum(float(r['adj.P.Val'])<0.05 and float(r['logFC'])< -1.5 for r in data.values())})
    (out/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n',encoding='utf-8')
    plt.rcParams.update({'font.size':10, 'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':160})
    labels = ['ITDT − PBS','ITDT+aCD4 − PBS','ITDT+aCD4 − ITDT']
    fig, axes=plt.subplots(1,3,figsize=(15,4.4),layout='constrained')
    for ax,contrast,title in zip(axes,CONTRASTS,labels):
        data=tables[contrast]; g=list(data)
        fc=np.array([float(data[x]['logFC']) for x in g]); p=np.array([float(data[x]['adj.P.Val']) for x in g])
        colors=np.where((p<.05)&(fc>1.5),'#C55A32',np.where((p<.05)&(fc< -1.5),'#307CA0','#BBBBBB'))
        ax.scatter(fc,-np.log10(np.maximum(p,np.finfo(float).tiny)),s=7,c=colors,alpha=.65,rasterized=True)
        ax.axhline(-np.log10(.05),color='gray',ls='--',lw=.7)
        for x in [-1.5,1.5]:ax.axvline(x,color='gray',ls='--',lw=.7)
        for gene in ['Gzma','Gzmb']:
            i=g.index(gene);ax.scatter(fc[i],-np.log10(p[i]),color='#E3B74C',s=40,edgecolor='black',lw=.5);ax.annotate(gene,(fc[i],-np.log10(p[i])),xytext=(4,4),textcoords='offset points',fontsize=9)
        ax.set(title=title,xlabel='Model log2 fold difference',ylabel='−log10(BH adjusted P)')
    fig.suptitle('Released limma-trend model on TPM · pooled NK libraries',fontsize=14)
    fig.savefig(out/'contrasts.png');plt.close(fig)
    scores=rows(out/'pca_scores.csv'); variance=rows(out/'pca_variance.csv')
    fig,axes=plt.subplots(1,2,figsize=(13,4.8),layout='constrained')
    colors={'PBS':'#333333','ITDT':'#307CA0','ITDT_aCD4':'#C55A32'}; markers={'rep1':'o','rep2':'^','rep3':'s'}
    for row in scores:
        axes[0].scatter(float(row['PC1']),float(row['PC2']),color=colors[row['condition']],marker=markers[row['block']],s=65)
        axes[0].annotate(row['sample'],(float(row['PC1']),float(row['PC2'])),fontsize=7,xytext=(4,3),textcoords='offset points')
    axes[0].set(title='Source PCA: gene-centered and scaled log2(TPM+0.5)',xlabel=f"PC1 ({float(variance[0]['fraction']):.1%})",ylabel=f"PC2 ({float(variance[1]['fraction']):.1%})")
    axes[1].boxplot(logtpm,tick_labels=samples,showfliers=False,widths=.65)
    axes[1].tick_params(axis='x',labelrotation=50);axes[1].set(title='Included-feature profiles',ylabel='log2(TPM + 0.5)')
    fig.savefig(out/'diagnostics.png');plt.close(fig)
    panelrows=rows(out/'fixed_panels.csv'); panels=list(dict.fromkeys(r['panel'] for r in panelrows))
    fig,axes=plt.subplots(4,2,figsize=(12,15),gridspec_kw={'width_ratios':[1,3]},layout='constrained')
    for i,panel in enumerate(panels):
        prs=[r for r in panelrows if r['panel']==panel]; pgenes=list(dict.fromkeys(r['gene'] for r in prs))
        lookup={(r['gene'],r['sample']):r for r in prs}
        group=np.array([[float(lookup[g,s]['group_scaled']) for s in samples[:3]] for g in pgenes])
        indiv=np.array([[float(lookup[g,s]['library_scaled']) for s in samples] for g in pgenes])
        lim=max(1.0,float(np.max(np.abs(indiv))))
        for ax,mat,xlabels,title in [(axes[i,0],group,['PBS','ITDT','ITDT+aCD4'],panel.replace('_',' ')+' · means'),(axes[i,1],indiv,samples,'Individual pooled preparations')]:
            im=ax.imshow(mat,aspect='auto',cmap='RdBu_r',vmin=-lim,vmax=lim)
            ax.set_xticks(range(len(xlabels)),xlabels,rotation=50,ha='right',fontsize=8);ax.set_yticks(range(len(pgenes)),pgenes);ax.set_title(title,fontsize=11)
        fig.colorbar(im,ax=axes[i,:],label='Scaled block-adjusted log2(TPM+0.5)',shrink=.75)
    fig.suptitle('Fixed source panels · mean and library values use the same gene-wise group-mean scale',fontsize=13)
    fig.savefig(out/'fixed_panels.png');plt.close(fig)
    print(json.dumps({'source_concordant':comparison['source_concordant'],'included_genes':len(genes)}))


if __name__=='__main__':main()
