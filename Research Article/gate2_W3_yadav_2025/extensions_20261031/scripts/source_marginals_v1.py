"""All qualified X2 workbook source marginals; no inferential tests."""
import argparse, json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common_v1 import ROOT, EXT, RUNS, read_csv, save_csv, save_json
from verify_x2_v1 import verify
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    out=ROOT/a.output;out.mkdir(exist_ok=True,parents=True)
    spec=json.loads((EXT/'config/x2_spec_v1.json').read_text())
    source={(r['sheet'],r['cell']):r for r in read_csv(RUNS/'Yd1_extension_x0_v1/panel_cells.csv')}
    obs=[];groups=[];lookup={};contrasts=[]
    for panel in spec['panels']:
        for group in panel['groups']:
            values=[]
            for cell in group['cells']:
                r=source[(panel['sheet'],cell)]
                assert (r['panel'],r['group'],r['role'])==(panel['id'],group['id'],'observation')
                value=float(r['source_value']);values.append(value)
                obs.append(dict(panel=panel['id'],sheet=panel['sheet'],cell=cell,group=group['id'],value=value,endpoint=panel['endpoint'].replace('\n',' '),biological_unit=panel['biological_unit'],pairing='unknown'))
            row=dict(panel=panel['id'],group=group['id'],n=len(values),mean=float(np.mean(values)),sd=float(np.std(values,ddof=1)),min=min(values),max=max(values),endpoint=panel['endpoint'].replace('\n',' '),biological_unit=panel['biological_unit'])
            groups.append(row);lookup[(panel['id'],group['id'])]=row
        for comp in panel['contrasts']:
            target=lookup[(panel['id'],comp['target'])];ref=lookup[(panel['id'],comp['reference'])]
            contrasts.append(dict(panel=panel['id'],comparison=comp['id'],target=comp['target'],reference=comp['reference'],n_target=target['n'],n_reference=ref['n'],mean_difference=target['mean']-ref['mean'],endpoint=panel['endpoint'].replace('\n',' '),inference='unpaired source-marginal difference; no population uncertainty',limit=panel['limit']))
    save_csv(out/'observations.csv',obs);save_csv(out/'group_summaries.csv',groups);save_csv(out/'contrasts.csv',contrasts)
    save_json(out/'independent_verification.json',verify(out))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    for name,panels,shape in [('arg1_panels',spec['panels'][:4],(2,2)),('il6_panels',spec['panels'][4:],(2,3))]:
        fig,axes=plt.subplots(*shape,figsize=(12 if name=='arg1_panels' else 14,9.5))
        for ax,panel in zip(axes.ravel(),panels):
            for i,g in enumerate(panel['groups']):
                values=[r['value'] for r in obs if (r['panel'],r['group'])==(panel['id'],g['id'])]
                color=['#24678D','#C6642D','#8060AA','#538675'][i]
                ax.scatter(i+np.linspace(-.09,.09,len(values)),values,s=28,alpha=.9,color=color,zorder=3)
                ax.hlines(lookup[(panel['id'],g['id'])]['mean'],i-.22,i+.22,color=color,linewidth=2.5)
                ax.text(i,1.02,'n='+str(len(values)),transform=ax.get_xaxis_transform(),ha='center',fontsize=8)
            ax.set_xticks(range(len(panel['groups'])),[g['label'] for g in panel['groups']]);ax.set_xlim(-.5,len(panel['groups'])-.5)
            ax.set_ylabel(panel['endpoint']);ax.set_title(panel['title'],loc='left',fontsize=11,pad=27)
            ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.15)
            if panel['id']=='6F_qPCR':ax.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
        for ax in axes.ravel()[len(panels):]:ax.axis('off')
        fig.suptitle('Published workbook source marginals · '+('ARG1 readouts' if name=='arg1_panels' else 'IL-6 and knockdown readouts'),x=.07,ha='left',fontsize=15)
        fig.subplots_adjust(left=.10,right=.98,top=.85,bottom=.22,wspace=.55,hspace=.67)
        notes=('4C workbook amplitudes differ visibly from the supplied PDF; exact graph concordance remains unresolved.\n4D retains macrophage-count normalization and the supplied qPCR zero. No inferred pairing across assays.' if name=='arg1_panels' else '6E retains supplied normalization relative to uninjured; it is not absolute pg/mL. ATP = ATPgammaS.\nNo KO untreated (6D), KO uninjured (6E), or KD unstimulated (6F) arm is imputed; no full interaction is estimated.')
        fig.text(.07,.065,'Each dot is one supplied observation; horizontal bars show arithmetic means. SD and full ranges are in the tables.\n'+notes+'\nPublished-source reuse; preparation/donor links to R1 are unknown. No tests, confidence intervals, mediation or flux claim.',fontsize=9)
        fig.savefig(out/(name+'.png'),dpi=180);fig.savefig(out/(name+'.pdf'));plt.close(fig)
    save_json(out/'runtime.json',dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,population_tests=False,scientific_acceptance='not_assessed'))
    print('All qualified X2 marginals reconstructed; workbook/blank/Decimal verification passed')
if __name__=='__main__':main()
