"""Render corrected frozen score tables; no new statistical testing."""
import argparse
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--runs-root',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args(); runs=Path(a.runs_root); out=Path(a.output)
    out.mkdir(parents=True,exist_ok=True)
    inputs=[runs/'wp_compass_orientation_v3/named_reactions.csv',runs/'wp_human_signature_transfer_v3/donor_scores.csv',runs/'wp_human_signature_transfer_v3/paired_tissue.csv']
    corr=pd.read_csv(inputs[0]).set_index('reaction'); donor=pd.read_csv(inputs[1]); paired=pd.read_csv(inputs[2]).set_index('score')
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
    fig,ax=plt.subplots(1,2,figsize=(12,5.6),gridspec_kw={'wspace':.40})
    fig.suptitle('Wp score corrections: direction and library-size normalization',fontsize=16,x=.07,ha='left',y=.97)
    names=['PGM_pos','PGCD_pos']; yy=np.arange(len(names))
    rho=corr.loc[names,'rho_pathogenicity_authors'].to_numpy()
    ax[0].scatter(-rho,yy,color='#999999',s=65,label='Earlier raw-penalty correlation')
    ax[0].scatter(rho,yy,color='#176b87',s=80,label='Corrected consistency correlation')
    for y,r,name in zip(yy,rho,names):
        ax[0].plot([-r,r],[y,y],color='#cccccc',zorder=0)
        ax[0].annotate(f'+{r:.3f}; BH q={corr.loc[name,"bh_pathogenicity"]:.3f}',(r,y),xytext=(-5,12),textcoords='offset points',ha='right',fontsize=10)
    ax[0].set(yticks=yy,yticklabels=['PGAM (PGM_pos)','PHGDH (PGCD_pos)'],xlim=(-.42,.42),ylim=(-.6,1.65),xlabel='Spearman correlation with pathogenicity RNA score',title='A  Compass: consistency = −log(1 + penalty)')
    ax[0].axvline(0,color='#dddddd',lw=1); ax[0].legend(loc='upper left',fontsize=9,frameon=False)
    for x,(score,label,color) in enumerate([('proinflammatory_authors','Inflammatory arm','#9a3f73'),('proregulatory_authors','Regulatory arm','#267f68')]):
        wide=donor.pivot(index='donor',columns='tissue',values=score).dropna()
        delta=wide.CSF-wide.PBMCs
        ax[1].scatter(x+np.linspace(-.08,.08,len(delta)),delta,s=32,color=color,alpha=.85)
        med=paired.loc[score,'median_difference']
        ax[1].plot([x-.22,x+.22],[med,med],lw=2.5,color=color)
        ax[1].text(x,.28,f'median {med:+.3f}',ha='center',fontsize=10)
    ax[1].set(xticks=[0,1],xticklabels=['Inflammatory arm','Regulatory arm'],ylabel='Paired donor mean score: CSF − blood',title='B  Human scores: full-gene CP10K denominator',xlim=(-.55,1.55),ylim=(-.13,.33))
    ax[1].axhline(0,color='#cccccc',lw=1)
    fig.subplots_adjust(left=.14,right=.98,bottom=.26,top=.79)
    fig.text(.07,.13,'A: 60 computational pools / 4 libraries / 2 animals; nominal pool tests are not animal inference.\nB: 10 paired donors; dots are donor differences. A nonsignificant regulatory contrast is not equivalence.\nBoth panels describe RNA-derived scores, not metabolic flux, cytokine protein, lineage or causal mechanism.',fontsize=10,linespacing=1.5)
    for ext in ('png','svg','pdf'):
        fig.savefig(out/f'corrected_scores.{ext}',dpi=220,facecolor='white')
    manifest={'inputs':{str(p.relative_to(runs)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('corrected_scores.*')},'limit':'Generated from corrected repository tables, not a reproduction of a published figure.'}
    (out/'figure_manifest.json').write_bytes((json.dumps(manifest,indent=2)+'\n').encode())


if __name__=='__main__': main()
