"""Measured figures from fixed source order and explicit immutable value tables."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
COLORS=['#777777','#0072B2','#D55E00']
def save(fig,out,name):
    fig.savefig(out/(name+'.png'),dpi=300);fig.savefig(out/(name+'.pdf'));plt.close(fig)
def render(out,panels,values,tested,ranges,fits,cv,background):
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    symbols=list(dict.fromkeys(panels['Figure5A_up']+panels['Figure5A_down']))
    libraries=['Unt_1','Unt_2','BS30_1','BS30_2','BS65_1','BS65_2','BS45_1','BS45_2']
    primary={r['symbol']:r for r in tested if r['view']=='full' and r['scale']=='CPM'}
    mat=np.array([[next(r['log2_plus_1'] for r in values if r['symbol']==s and r['library']==l and r['scale']=='CPM') for l in libraries] for s in symbols])
    metrics=['WT-PBS','DE-PBS','SUPER-PBS','DE-WT','SUPER-WT'];effects=np.array([[primary[s][m] for m in metrics] for s in symbols])
    fig,axs=plt.subplots(1,2,figsize=(11,9),layout='constrained',gridspec_kw={'width_ratios':[1.35,1]})
    im=axs[0].imshow(mat,aspect='auto',cmap='viridis',vmin=0);fig.colorbar(im,ax=axs[0],shrink=.55,label='log2(CPM + 1)')
    limit=max(abs(effects.min()),abs(effects.max()));im=axs[1].imshow(effects,aspect='auto',cmap='RdBu_r',vmin=-limit,vmax=limit);fig.colorbar(im,ax=axs[1],shrink=.55,label='Difference of group means')
    labels=[s+(' *' if not primary[s]['eligible'] else '') for s in symbols]
    for ax in axs:
        ax.set_yticks(range(len(symbols)),labels);ax.axhline(len(panels['Figure5A_up'])-.5,color='black',lw=.8)
    axs[0].set_xticks(range(8),['PBS 1','PBS 2','WT 1','WT 2','10-DE 1','10-DE 2','super-10 1','super-10 2'],rotation=55,ha='right')
    axs[1].set_xticks(range(5),['WT−PBS','10-DE−PBS','super-10−PBS','10-DE−WT','super-10−WT'],rotation=55,ha='right')
    for i in range(len(symbols)):
        for j in range(5):axs[1].text(j,i,f'{effects[i,j]:.2f}',ha='center',va='center',fontsize=7,color='white' if abs(effects[i,j])>.65*limit else 'black')
    axs[0].set_title('A  Every library, published Figure 5A order');axs[1].set_title('B  Fixed direct and PBS contrasts')
    fig.suptitle('Activated CD8 RNA • 24 h • source-selected targets\n* IL2 below fixed expression filter; displayed, excluded from panel medians')
    save(fig,out,'fixed_targets')
    fig,axs=plt.subplots(1,2,figsize=(10,4.7),layout='constrained')
    for ax,variant,label in zip(axs,['DE','SUPER'],['10-DE','super-10']):
        x=cv['WT-PBS'];y=cv[variant+'-PBS'];b=next(r['beta'] for r in fits if r['scale']=='CPM' and r['view']=='full' and r['variant']==variant)
        ax.scatter(x[background],y[background],color='#999999',s=4,alpha=.15,rasterized=True)
        for panel,color,marker in [('Figure5A_up','#D55E00','o'),('Figure5A_down','#0072B2','s')]:
            rows=[primary[s] for s in panels[panel] if primary[s]['eligible']]
            ax.scatter([r['WT-PBS'] for r in rows],[r[variant+'-PBS'] for r in rows],color=color,marker=marker,s=28,label=panel.replace('Figure5A_','5A '))
        z=max(np.max(np.abs(x[background])),np.max(np.abs(y[background])),max(abs(primary[s]['WT-PBS']) for s in symbols),max(abs(primary[s][variant+'-PBS']) for s in symbols))*1.08
        ax.plot([-z,z],[-z,z],color='black',ls=':',lw=1,label='Equal responses');ax.plot([-z,z],[-z*b,z*b],color='#009E73',lw=1.5,label=f'Background beta={b:.3f}')
        ax.axhline(0,color='#cccccc',lw=.6);ax.axvline(0,color='#cccccc',lw=.6);ax.set(xlim=(-z,z),ylim=(-z,z),xlabel='WT − PBS',ylabel=label+' − PBS',title=label+' response pattern');ax.legend(frameon=False,fontsize=8)
    fig.suptitle('Primary log2(CPM + 1) contrasts • fixed background excludes all Figure 5 targets\nNoisy axes share PBS; fitted amplitude is descriptive, not a causal fraction')
    save(fig,out,'response_pattern')
    fig,axs=plt.subplots(1,2,figsize=(11,5.5),layout='constrained')
    for ax,variant,label in zip(axs,['DE','SUPER'],['10-DE − WT','super-10 − WT']):
        for i,s in enumerate(panels['Figure5B']):
            for k,scale in enumerate(['CPM','MR_CPM','FPKM']):
                r=next(r for r in ranges if r['symbol']==s and r['scale']==scale and r['metric']==variant+'-WT');y=i+(k-1)*.22
                ax.plot([r['omission_min'],r['omission_max']],[y,y],color=COLORS[k],lw=1.5)
                ax.scatter(r['full'],y,color=COLORS[k],marker=['o','s','^'][k],s=24,label=scale.replace('_',' ') if i==0 else None,zorder=3)
        ax.axvline(0,color='#aaaaaa',lw=.8);ax.set_yticks(range(len(panels['Figure5B'])),panels['Figure5B']);ax.invert_yaxis();ax.set(title=label,xlabel='Difference of mean log2(expression + 1)');ax.legend(frameon=False,fontsize=8)
    fig.suptitle('Fixed Figure 5B targets • full-data symbols and eight single-library omission ranges\nRanges are observed sensitivity, not confidence intervals')
    save(fig,out,'omission_sensitivity')
