"""Render only frozen results; no model fitting or updated inference."""
import argparse,json,csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})

def main(owner,out):
    out.mkdir(exist_ok=True)
    if owner=='A25':
        root=Path('analysis/research/runs/cut_fill_a25_models_v1_20261103');s=json.loads((root/'summary.json').read_text());rows=list(csv.DictReader((root/'heldout_losses.csv').open()))
        mice=sorted({r['mouse'] for r in rows},key=lambda x:(int(x.split('_')[0]),x));x=np.arange(len(mice));fig,ax=plt.subplots(1,2,figsize=(11.5,4.6),gridspec_kw={'width_ratios':[1.35,1]})
        for j,(base,label,color) in enumerate([('endpoint_mixture','vs endpoint mixture','#287991'),('continuous_age','vs flexible age','#bd6b32')]):
            vals=[s['additional_component_gains'][base]['per_mouse'][m] for m in mice];ax[0].scatter(x+(j-.5)*.17,vals,label=label,color=color,s=40)
        ax[0].axhline(0,color='#555555',lw=.8);ax[0].set_xticks(x,mice,rotation=45,ha='right');ax[0].set_ylabel('Held-out loss reduction (nats / cell)');ax[0].set_title('Every held-out mouse');ax[0].legend(frameon=False)
        models=['endpoint_mixture','continuous_age','additional_component'];labels=['Endpoint\nmixture','Flexible\nage','Additional\ncomponent']
        for mouse,color in [('18_45_M','#287991'),('18_53_M','#bd6b32')]:
            vals=[float(next(r['mean_nll'] for r in rows if r['mouse']==mouse and r['model']==m)) for m in models];ax[1].plot(range(3),vals,'o-',label=mouse,color=color)
        ax[1].set_xticks(range(3),labels);ax[1].set_ylabel('Mean held-out negative log density');ax[1].set_title('Only two middle-age mice');ax[1].legend(frameon=False)
        fig.suptitle('A25 | Male cortex: gain over endpoint mixture, mixed gain over flexible age',fontsize=13,y=.98)
        fig.text(.02,.015,'2,129 cells; 3 / 2 / 4 mice at 3 / 18 / 24 months. Train-only five-PC representation.\nInternal exposed prediction; no distinct-state or functional claim. Positive loss reduction favors the additional component.',fontsize=9,color='#444444')
        fig.tight_layout(rect=(0,.12,1,.93));stem='a25_heldout_models_v1'
    else:
        root=Path('analysis/research/runs/cut_fill_a17_recoverability_v1_20261103');p=json.loads((root/'probabilities.json').read_text());s=json.loads((root/'recoverability.json').read_text());fig,ax=plt.subplots(2,3,figsize=(11.5,6.2),sharex=True,sharey=True)
        names=s['cases'];labels=['Persistent: script','Persistent: manuscript variant','Switching: S start','Switching: F start','Combined'];colors=['#287991','#77a4b4','#bd6b32','#dfa969','#775b91']
        for j,t in enumerate([1,2,4]):
            for name,label,color in zip(names,labels,colors):
                q=p[f'{name}_week{t}']['q'];ax[0,j].plot(np.arange(2,66),q,color=color,label=label,lw=1.2)
            q=s['weeks'][str(t)]['common_selected_law'];ax[1,j].plot(np.arange(2,66),q,color='#252525',lw=1.8)
            ax[0,j].set_title(f'Week {t}');ax[1,j].set_xlabel('Size (last bin = 65 or more)')
            for a in ax[:,j]:a.set_yscale('log');a.set_ylim(1e-5,1);a.grid(alpha=.15)
        ax[0,0].set_ylabel('Uniform detection\nretained-size probability');ax[1,0].set_ylabel('Unknown detection\ncommon observed probability')
        fig.legend(*ax[0,0].get_legend_handles_labels(),loc='lower center',ncol=3,bbox_to_anchor=(.5,.04),frameon=False,fontsize=9)
        fig.suptitle('A17 | Different model laws can share one observed retained-size law',fontsize=14,y=.98)
        fig.text(.02,.012,'Synthetic observation counterexample, not an empirical clone fit. Actual 11-mouse schedule; complete tail bin retained.\nUnknown detection is an admissible sensitivity, not a recovered process. Uniform-detection models are not declared indistinguishable.',fontsize=9,color='#444444')
        fig.tight_layout(rect=(0,.17,1,.94));stem='a17_observation_ambiguity_v1'
    fig.savefig(out/(stem+'.png'),dpi=160,facecolor='white');fig.savefig(out/(stem+'.svg'),facecolor='white');plt.close(fig)
    (out/'render.json').write_text(json.dumps({'owner':owner,'source_run':root.as_posix(),'no_refit':True,'png':stem+'.png','svg':stem+'.svg'},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--owner',choices=['A17','A25'],required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.owner,a.output)
