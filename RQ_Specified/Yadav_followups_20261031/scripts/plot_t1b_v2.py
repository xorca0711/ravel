"""Layout-only correction from frozen T1-B tables; no workbook or mean calculation."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from textwrap import wrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parents[1]


def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))


def draw(job,measure,out):
    run=ROOT/f'analysis/research/runs/Wg_P06_followup_t1b_{job}_v1'
    spec=json.loads((HERE/f'config/t1b_{job}_spec_v1.json').read_text())
    values=read(run/'source_values.csv');summaries=read(run/'summaries.csv');vectors=read(run/'vector_qc.csv')
    blocks=spec['blocks'];nrows=math.ceil(len(blocks)/3)
    fig,axes=plt.subplots(nrows,3,figsize=(18,19),squeeze=False)
    colors={'UT':'#216b91','TGF-beta':'#b95320'}
    for ax,b in zip(axes.flat,blocks):
        metas=[m for m in b['measures'] if m['name']==measure]
        heading='\n'.join(wrap(b['id']+' | '+b['metabolite'],48))
        if not metas:
            ax.text(.5,.5,'Fraction map held\nDuplicated source isotope headers',ha='center',va='center',transform=ax.transAxes,fontsize=11)
            ax.set_title(heading,loc='left',fontsize=10,pad=10);ax.set_axis_off();continue
        m=metas[0];isotopes=list(m['isotope_headers'].values())
        ss=[s for s in summaries if s['block']==b['id'] and s['measure']==measure]
        held=sum(s['status']!='qualified' for s in ss)
        if measure=='reported_channel_percent':
            q=[v for v in vectors if v['block']==b['id']]
            complete=sum(v['completeness']=='complete_supplied_valid_channels' for v in q)
            subtitle=f'Complete supplied vectors: {complete}/{len(q)}\nNormalization not validated; held summaries: {held}'
        else:subtitle=m['unit_literal']+f'\nHeld channel summaries: {held}'
        ax.set_title(heading+'\n'+subtitle,loc='left',fontsize=9.5,pad=10)
        for i,iso in enumerate(isotopes):
            for condition,offset in [('UT',-.17),('TGF-beta',.17)]:
                s=next(s for s in ss if s['isotope']==iso and s['reported_condition']==condition)
                rr=[r for r in values if r['block']==b['id'] and r['measure']==measure and r['isotope']==iso and r['reported_condition']==condition]
                vv=[float(r['numeric_value']) for r in rr if r['value_status']=='valid' and r['header_status']=='qualified']
                if vv:
                    xx=[i+offset+(j-(len(vv)-1)/2)*.035 for j in range(len(vv))]
                    ax.scatter(xx,vv,s=15,color=colors[condition],alpha=.7,zorder=3)
                if s['status']=='qualified':
                    ax.vlines(i+offset,float(s['minimum']),float(s['maximum']),color=colors[condition],lw=1)
                    ax.hlines(float(s['mean']),i+offset-.10,i+offset+.10,color=colors[condition],lw=1.6)
                else:
                    ax.text(i+offset,.035,'×',ha='center',va='center',color=colors[condition],transform=ax.get_xaxis_transform(),fontsize=12)
        ax.set_xticks(range(len(isotopes)),isotopes,rotation=55,ha='right',fontsize=8)
        ax.set_xlim(-.55,len(isotopes)-.45)
        ax.set_ylabel('Source-reported channel (%)' if measure=='reported_channel_percent' else 'Native uncalibrated peak area',fontsize=9)
        if measure=='reported_channel_percent':ax.set_ylim(-3,108)
        ax.grid(axis='y',alpha=.14);ax.spines[['top','right']].set_visible(False);ax.tick_params(axis='y',labelsize=9)
    for ax in list(axes.flat)[len(blocks):]:ax.set_axis_off()
    title='Hamanaka | '+('R1 reported-channel companion' if job=='r1' else 'R2 '+('reported percentages' if measure=='reported_channel_percent' else 'native peak areas'))
    caption='Unstacked supplied dots; means and observed ranges only at full supplied n. × marks a held summary, not zero.\nNo biological inference. '+('Four source labels per condition.' if job=='r1' else '4F retains three source labels per condition; other panels retain four.')
    fig.suptitle(title+'\n'+caption,fontsize=14,y=.987,linespacing=1.4)
    handles=[plt.Line2D([],[],marker='o',ls='',color=c,label=l) for l,c in colors.items()]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.015),ncol=2,frameon=False,fontsize=11)
    fig.subplots_adjust(left=.055,right=.985,top=.905,bottom=.07,hspace=.75,wspace=.25)
    stem=job+('_reported_percent_channels_v2' if measure=='reported_channel_percent' else '_native_area_channels_v2')
    fig.savefig(out/(stem+'.png'),dpi=170);fig.savefig(out/(stem+'.pdf'));plt.close(fig)
    return {'job':job,'measure':measure,'stem':stem,'panels':len(blocks),'held_map_panels':sum(not any(m['name']==measure for m in b['measures']) for b in blocks),
            'source_tables':[{ 'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [run/'source_values.csv',run/'summaries.csv',run/'vector_qc.csv']],
            'supersedes_figure':(run/('reported_percent_channels.png' if measure=='reported_channel_percent' else 'native_area_channels.png')).relative_to(ROOT).as_posix(),
            'change':'Layout only: wrapped/multiline panel titles, fixed subplot spacing, padded x limits for held marks, annotation outside data region. No source/summary/QC changes.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();out=ROOT/args.output;out.mkdir(parents=True,exist_ok=True)
    manifest=[draw(j,m,out) for j,m in [('r1','reported_channel_percent'),('r2','reported_channel_percent'),('r2','reported_area')]]
    with (out/'figure_manifest.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,indent=2);f.write('\n')
    print(json.dumps({'ok':True,'figures':3,'numerical_tables':'reused unchanged'}))
