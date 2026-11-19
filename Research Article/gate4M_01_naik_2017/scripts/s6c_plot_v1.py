"""Complete-universe rank displays and all five fixed anchors, without pairing lines."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OLD=['GSM'+str(i) for i in range(2441001,2441009)]
NEW=['GSM'+str(i) for i in range(2652413,2652417)]
PHASES={'D6':(OLD[:2],OLD[2:4]),'D30':(OLD[4:6],OLD[6:]),'D180':(NEW[2:],NEW[:2])}
COLORS={'D6':'#0072B2','D30':'#D55E00','D180':'#009E73'}


def finish(fig,output,name):
    fig.savefig(output/(name+'.png'),dpi=220,bbox_inches='tight')
    fig.savefig(output/(name+'.pdf'),bbox_inches='tight',metadata={'CreationDate':None,'ModDate':None})
    plt.close(fig)


def plot(output,frame,cases):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,'pdf.fonttype':42})
    limit=max(5.,5*np.ceil(np.abs(frame[['D6_delta','D30_delta','D180_delta']].to_numpy()).max()/5))
    fig=plt.figure(figsize=(17,9),layout='constrained');grid=fig.add_gridspec(2,4,width_ratios=[1,1,1,1.05])
    fig.suptitle('D180 on the exact S3 TSS-proxy universe: finite relative-rank differences\nD6: acute inflamed; D30/D180: prior inflammation · every window retained\nCross-time platform difference; pool membership unresolved; ranks do not measure absolute accessibility',fontsize=13)
    for r,flank in enumerate([1000,2000]):
        f=frame.loc[frame.flank==flank]
        for c,phase in enumerate(['D30','D6']):
            ax=fig.add_subplot(grid[r,c]);ax.hexbin(f[phase+'_delta'],f.D180_delta,gridsize=42,bins='log',mincnt=1,cmap='cividis',extent=(-limit,limit,-limit,limit))
            ax.plot([-limit,limit],[-limit,limit],color='#777777',lw=.8,ls='--')
            ax.axhline(0,color='#bbbbbb',lw=.6);ax.axvline(0,color='#bbbbbb',lw=.6)
            ax.set(xlim=(-limit,limit),ylim=(-limit,limit),xlabel=f'{phase} exposed − Ctrl rank (pp)',ylabel='D180 PI − Ctrl rank (pp)',
                title=f'±{flank//1000} kb · {len(f):,} windows\nD180 versus {phase}; log-density shading')
        ax=fig.add_subplot(grid[r,2])
        for phase in PHASES:
            values=np.sort(np.abs(f[phase+'_delta'].to_numpy()))
            ax.plot(values,np.arange(1,len(values)+1)/len(values),color=COLORS[phase],label=phase,lw=1.5)
        ax.set(xlim=(0,limit),ylim=(0,1),xlabel='|Exposed − Ctrl rank| (pp)',ylabel='Cumulative fraction of all windows',title=f'±{flank//1000} kb · absolute displacement')
        ax.legend(frameon=False,loc='lower right');ax.grid(alpha=.15)
    ax=fig.add_subplot(grid[:,3]);a=frame.loc[frame.flank==1000].set_index('anchor_id');b=frame.loc[frame.flank==2000].set_index('anchor_id').loc[a.index]
    ax.hexbin(a.D180_delta,b.D180_delta,gridsize=42,bins='log',mincnt=1,cmap='cividis',extent=(-limit,limit,-limit,limit))
    ax.plot([-limit,limit],[-limit,limit],ls='--',color='#777777',lw=.8);ax.axhline(0,color='#bbbbbb',lw=.6);ax.axvline(0,color='#bbbbbb',lw=.6)
    ax.set(xlim=(-limit,limit),ylim=(-limit,limit),xlabel='D180 ±1 kb rank difference (pp)',ylabel='D180 ±2 kb rank difference (pp)',
        title=f'Width sensitivity\n{len(a):,} exact shared anchors\nlog-density shading',aspect='equal')
    for ax in fig.axes: ax.spines[['top','right']].set_visible(False)
    finish(fig,output,'fig01_D180_universe')

    fig,axes=plt.subplots(5,2,figsize=(12,16),layout='constrained',sharex=True,sharey=True)
    fig.suptitle('All five fixed paper anchors · all twelve library ranks\nFilled blue circles: control; open orange squares: exposed · no animal matching\nD6 is acute inflamed; D30/D180 are prior-inflammation sources',fontsize=14)
    for row,name in enumerate(['Aim2','Casp1','Il1b','Il1r1','Il18']):
        for col,flank in enumerate([1000,2000]):
            ax=axes[row,col];record=cases.loc[(cases.gene_name==name)&(cases.flank==flank)].iloc[0]
            for phase_index,(phase,(control,history)) in enumerate(PHASES.items()):
                for rep,gsm in enumerate(control):
                    ax.scatter(phase_index-.15+rep*.07,record[gsm+'__percentile'],s=32,color='#0072B2',zorder=3)
                for rep,gsm in enumerate(history):
                    ax.scatter(phase_index+.08+rep*.07,record[gsm+'__percentile'],s=36,facecolors='none',edgecolors='#D55E00',marker='s',zorder=3)
                delta=record[phase+'_delta'];lo=record[phase+'_range_min'];hi=record[phase+'_range_max']
                ax.text(phase_index,-9,f'Δ {delta:+.2f}\n[{lo:+.2f}, {hi:+.2f}]',ha='center',va='top',fontsize=8)
            ax.set(xlim=(-.5,2.5),ylim=(-32,104),xticks=[0,1,2],xticklabels=list(PHASES),yticks=[0,25,50,75,100],
                title=f'{name} · ±{flank//1000} kb · {record.anchor_id}',ylabel='Within-library percentile rank')
            ax.grid(axis='y',alpha=.17);ax.spines[['top','right','bottom']].set_visible(False)
            ax.tick_params(axis='x',labelbottom=True)
    fig.supxlabel('Δ: mean exposed − mean control rank (pp); brackets: all four unpaired contrasts [min, max], not a CI',fontsize=11)
    finish(fig,output,'fig02_five_fixed_anchors')
