"""Frozen descriptive reconstructions of qualified published source values."""
import argparse,csv,json,math,platform,statistics,sys
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import t as student_t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'analysis/research/runs/Yd1_source_qualification_v1/workbook_cells.tsv'

def csv_write(path,rows):
    with path.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n')
        w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--spec',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    spec=json.loads((ROOT/a.spec).read_text());out=a.output;out.mkdir(exist_ok=True,parents=True)
    with SOURCE.open(encoding='utf-8') as f: source={(r['sheet'],r['cell']):r for r in csv.DictReader(f,delimiter='\t')}
    obs,sums,contrasts=[],[],[];lookup={}
    for panel in spec['panels']:
        for group in panel['groups']:
            values=[]
            for cell in group['cells']:
                r=source.get((panel['sheet'],cell))
                if r is None:
                    assert (panel['sheet'],cell)==('5d','D2'),(panel['sheet'],cell)
                    value='';status='missing_in_source'
                else:
                    assert r['type']=='n',(panel['sheet'],cell)
                    value=float(r['source_value']);assert math.isfinite(value);status='observed';values.append(value)
                obs.append(dict(job=spec['job'],panel=panel['id'],sheet=panel['sheet'],donor=group['donor'],
                    condition=group['id'],source_cell=cell,value=value,status=status,unit=panel['unit']))
            assert len(values)>1
            s=dict(job=spec['job'],panel=panel['id'],donor=group['donor'],condition=group['id'],
                n_expected=len(group['cells']),n_observed=len(values),mean=statistics.mean(values),
                sd=statistics.stdev(values),minimum=min(values),maximum=max(values),unit=panel['unit'])
            sums.append(s);lookup[(panel['id'],group['donor'],group['id'])]=(s,values)
        for donor in dict.fromkeys(g['donor'] for g in panel['groups']):
            for target,reference in panel['pairs']:
                ts,tv=lookup[(panel['id'],donor,target)];rs,rv=lookup[(panel['id'],donor,reference)]
                delta=ts['mean']-rs['mean'];se=df=critical=lower=upper=''
                if spec.get('welch'):
                    x=ts['sd']**2/ts['n_observed'];y=rs['sd']**2/rs['n_observed']
                    se=math.sqrt(x+y);df=(x+y)**2/(x*x/(ts['n_observed']-1)+y*y/(rs['n_observed']-1))
                    critical=float(student_t.ppf(.975,df));lower=delta-critical*se;upper=delta+critical*se
                contrasts.append(dict(job=spec['job'],panel=panel['id'],donor=donor,target=target,reference=reference,
                    mean_difference=delta,standard_error=se,welch_df=df,t_critical=critical,ci95_lower=lower,ci95_upper=upper,
                    interval_scope='independent-source-animal assumption' if spec.get('welch') else 'not estimated',
                    unit=panel['unit']))
    csv_write(out/'observations.csv',obs);csv_write(out/'group_summaries.csv',sums);csv_write(out/'contrasts.csv',contrasts)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
        'pdf.fonttype':42,'svg.fonttype':'none','axes.titleweight':'bold'})
    n=len(spec['panels']);cols=2;rows=(n+1)//2
    fig,axes=plt.subplots(rows,cols,figsize=(11.4,4.1*rows+1.1),squeeze=False)
    colors=['#226B96','#C65E27']
    for ax,panel in zip(axes.flat,spec['panels']):
        ids=list(dict.fromkeys(g['id'] for g in panel['groups']))
        donors=list(dict.fromkeys(g['donor'] for g in panel['groups']))
        labels={g['id']:g['label'] for g in panel['groups']}
        for di,donor in enumerate(donors):
            offset=(di-(len(donors)-1)/2)*.26
            for i,gid in enumerate(ids):
                s,v=lookup[(panel['id'],donor,gid)];x=i+offset
                ax.scatter(x+np.linspace(-.055,.055,len(v)),v,s=26,color=colors[di],edgecolor='white',linewidth=.45,
                    label=donor if i==0 and donor!='source' else None,zorder=3)
                ax.hlines(s['mean'],x-.12,x+.12,color=colors[di],linewidth=2.6,zorder=4)
        ax.set_xticks(range(len(ids)),[labels[k] for k in ids],fontsize=9)
        ax.set_ylabel(panel['unit']);ax.set_title(panel['title'],loc='left',fontsize=11,pad=12)
        ax.set_xlim(-.5,len(ids)-.5);ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.17)
        if len(donors)>1:ax.legend(frameon=False,fontsize=8,loc='upper left')
        if spec.get('welch'):
            c=next(c for c in contrasts if c['panel']==panel['id'])
            ax.set_title(panel['title']+f"\nDifference: {c['mean_difference']:.3g}; 95% interval [{c['ci95_lower']:.3g}, {c['ci95_upper']:.3g}]",loc='left',fontsize=10,pad=12)
        if panel['id']=='5D':ax.text(.98,.98,'Donor 1 / Fib alone: 2 supplied values',transform=ax.transAxes,ha='right',va='top',fontsize=8)
    for ax in list(axes.flat)[n:]:ax.axis('off')
    fig.suptitle(spec['title'],x=.06,ha='left',fontsize=15,fontweight='bold')
    fig.text(.06,.02,spec['footnote']+'\nSource: Yadav et al., JCI 2025;135:e188734, official Supporting Data Values. Outcome-exposed reconstruction.',fontsize=8)
    fig.tight_layout(rect=(.015,.07,.99,.93),h_pad=2.8,w_pad=2.6)
    fig.savefig(out/'figure.png',dpi=200);fig.savefig(out/'figure.pdf');plt.close(fig)
    runtime=dict(python=sys.version,platform=platform.platform(),numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,
        manuscript_source='JCI188734',job=spec['job'],hypothesis_tests=False,scientific_acceptance='not_assessed')
    (out/'runtime.json').write_text(json.dumps(runtime,indent=2)+'\n',encoding='utf-8')
    print(f"{spec['job']}: {len(spec['panels'])} panels, {len(obs)} source slots, {sum(o['status']=='missing_in_source' for o in obs)} missing, {len(contrasts)} fixed contrasts.")
if __name__=='__main__':main()

