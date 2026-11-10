"""Prespecified fixed-feature leave-one-block-out diagnostic, not confirmation."""
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


def read(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


def write(path,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
    subprocess.run([shutil.which('Rscript'),'--vanilla','Research Article/gate3_11_zhang_2026_nk/scripts/block_sensitivity_v1.R',str(out)],check=True)
    src=Path('analysis/research/runs/zh26_s1_reproduction_v1')
    data=read(src/'logTPM.csv');key=next(iter(data[0]));samples=list(data[0])[1:]
    y={r[key]:np.array([float(r[s]) for s in samples]) for r in data}
    meta=read('raw_data/zhang_2026/source_v1/author/input_files/sample_info_NK.csv')
    assert [r[next(iter(r))] for r in meta]==samples
    full={}
    for contrast in ['itdt_vs_pbs','itdt_acd4_vs_itdt']:
        rows=read(src/(contrast+'_nk.csv'));k=next(iter(rows[0]));full[contrast]={r[k]:float(r['logFC']) for r in rows}
    loo=read(out/'leave_one_block_out.csv');errors=[];lookup={}
    for row in loo:
        high,low=('ITDT','PBS') if row['contrast']=='itdt_vs_pbs' else ('ITDT_aCD4','ITDT')
        hi=[i for i,m in enumerate(meta) if m['replicate']!=row['omitted_block'] and m['condition']==high]
        lo=[i for i,m in enumerate(meta) if m['replicate']!=row['omitted_block'] and m['condition']==low]
        independent=y[row['gene']][hi].mean()-y[row['gene']][lo].mean()
        errors.append(abs(float(row['logFC'])-independent));lookup[(row['contrast'],row['gene'],row['omitted_block'])]=float(row['logFC'])
    assert max(errors)<1e-8
    summaries=[];allrows=[]
    for contrast,fc in full.items():
        for gene,value in fc.items():
            vals=[lookup[(contrast,gene,b)] for b in ['rep1','rep2','rep3']]
            allrows.append(dict(contrast=contrast,gene=gene,full_logFC=value,omit_rep1=vals[0],omit_rep2=vals[1],omit_rep3=vals[2],min_logFC=min(vals),max_logFC=max(vals),sign_agreement=sum(np.sign(v)==np.sign(value) for v in vals)))
        current=[r for r in allrows if r['contrast']==contrast]
        summaries.append(dict(contrast=contrast,genes=len(current),all_three_signs_agree=sum(r['sign_agreement']==3 for r in current),some_sign_change=sum(r['sign_agreement']<3 for r in current)))
    write(out/'gene_stability.csv',allrows)
    panel=read(src/'fixed_panels.csv');membership=list(dict.fromkeys((r['panel'],r['gene']) for r in panel))
    bykey={(r['contrast'],r['gene']):r for r in allrows}
    fixed=[dict(panel=p,**bykey[c,g]) for c in full for p,g in membership]
    write(out/'fixed_panel_stability.csv',fixed)
    report={'independent_arithmetic_checks':len(errors),'max_error':max(errors),'global_summary':summaries,
            'fixed_panel_rows':len(fixed),'fixed_panel_sign_changes':[{'contrast':r['contrast'],'panel':r['panel'],'gene':r['gene'],'full_logFC':r['full_logFC'],'omission_range':[r['min_logFC'],r['max_logFC']]} for r in fixed if r['sign_agreement']<3],
            'interpretation':'Two blocks retained per omission, residual df=2. Magnitude/direction diagnostic on the fixed full-data feature set; no significance testing, population CI or stability cutoff.'}
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    fig,axes=plt.subplots(1,2,figsize=(12,12),sharey=True,layout='constrained')
    colors=['#307CA0','#C55A32','#42977B']
    for ax,c in zip(axes,full):
        for i,(panel,g) in enumerate(membership):
            r=bykey[c,g]
            ax.plot([r['min_logFC'],r['max_logFC']],[i,i],color='#AAAAAA',lw=2)
            for j,b in enumerate(['rep1','rep2','rep3']):ax.scatter(r['omit_'+b],i+(j-1)*.13,color=colors[j],s=24,label='Omit '+b if i==0 else None)
            ax.scatter(r['full_logFC'],i,marker='|',s=100,color='black',label='Full model' if i==0 else None)
        ax.axvline(0,color='gray',lw=.8);ax.set_title(c.replace('_',' '));ax.set_xlabel('Model log2 transcript difference')
        ax.set_yticks(range(len(membership)),[p.replace('_',' ')+' / '+g for p,g in membership],fontsize=8);ax.invert_yaxis();ax.legend(fontsize=8,loc='lower right')
    fig.suptitle('Fixed source panels · leave one reported experimental block out\nPoints are diagnostic refits; connecting ranges are not confidence intervals',fontsize=13)
    fig.savefig(out/'block_stability.png',dpi=170);plt.close(fig)
    print(json.dumps({'checks':len(errors),'max_error':max(errors),'fixed_panel_sign_changes':len(report['fixed_panel_sign_changes'])}))


if __name__=='__main__':main()
