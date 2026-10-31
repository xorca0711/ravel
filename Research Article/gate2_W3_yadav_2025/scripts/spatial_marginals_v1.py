"""Exposed Fig. 5B marginal source description; no spatial reconstruction."""
import argparse,csv,json,statistics,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3]
def write(p,rows):
    with p.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output;out.mkdir(parents=True,exist_ok=True)
    spec=json.loads((ROOT/'Research Article/gate2_W3_yadav_2025/config/spatial_marginals_spec_v1.json').read_text())
    with (ROOT/spec['source']).open(encoding='utf-8') as f:cells={(r['sheet'],r['cell']):r for r in csv.DictReader(f,delimiter='\t')}
    obs=[];summaries=[];groups={}
    for group in spec['groups']:
        assert cells[('5b',group['header'])]['source_value'].replace('\u00a0',' ')==group['source_label']
        values=[]
        for cell in group['cells']:
            r=cells[('5b',cell)];assert r['type']=='n';value=float(r['source_value'])
            assert np.isfinite(value);values.append(value)
            obs.append(dict(sheet='5b',source_cell=cell,group=group['id'],published_label=group['source_label'],value=value,
                patient_id='unknown',pair_id='unknown',endpoint='published probability ratio at 25 micrometres'))
        assert len(values)==9
        groups[group['id']]=values
        summaries.append(dict(group=group['id'],n_source_values=len(values),mean=statistics.mean(values),median=statistics.median(values),minimum=min(values),maximum=max(values),
            unit='published probability ratio',precision='not estimated; missing source-to-patient and pairing map'))
    lookup={r['group']:r for r in summaries};target=spec['target'];reference=spec['reference']
    contrast=[dict(target=target,reference=reference,mean_difference=lookup[target]['mean']-lookup[reference]['mean'],
        estimand='difference between published marginal means',pairing='not inferred',interval='not estimated',test='none')]
    write(out/'observations.csv',obs);write(out/'marginal_summaries.csv',summaries);write(out/'contrast.csv',contrast)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,ax=plt.subplots(figsize=(8,5.4));colors=['#226B96','#C65E27']
    for i,g in enumerate(spec['groups']):
        v=groups[g['id']];ax.scatter(i+np.linspace(-.06,.06,len(v)),v,color=colors[i],s=34,zorder=3)
        ax.hlines(lookup[g['id']]['mean'],i-.15,i+.15,color=colors[i],linewidth=2.7)
    ax.axhline(1,color='#777777',linestyle='--',linewidth=.8,zorder=1)
    ax.set_xticks([0,1],['IL6+ fibroblasts','IL6- fibroblasts']);ax.set_xlim(-.5,1.5);ax.set_ylim(0,1.25)
    ax.set_ylabel('Published probability ratio at 25 micrometres')
    ax.set_title('Fig. 5B: published marginal source values',loc='left',fontsize=14,pad=22)
    ax.text(0,1.01,f"IL6+ minus IL6- marginal mean: {contrast[0]['mean_difference']:.4f}",transform=ax.transAxes,fontsize=10)
    fig.subplots_adjust(left=.12,right=.97,top=.80,bottom=.25)
    fig.text(.12,.045,'Nine source values per labeled group; bars are means, dashed line is ratio 1.\nSource coordinates are provenance, not recovered patient or pair identities.\nNo connecting lines, paired test, patient-effect interval or raw spatial reconstruction.',fontsize=9)
    fig.savefig(out/'spatial_marginals.png',dpi=200,bbox_inches='tight');fig.savefig(out/'spatial_marginals.pdf',bbox_inches='tight');plt.close(fig)
    (out/'runtime.json').write_text(json.dumps(dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,exposure='exposed',spatial_reconstruction=False,paired_analysis=False,scientific_acceptance='not_assessed'),indent=2)+'\n',encoding='utf-8')
    print('S1 marginal description: all 18 source values; two marginal summaries; one fixed mean difference; no tests or intervals.')
if __name__=='__main__':main()
