"""Fixed descriptive displays; ranges describe observed omission sensitivity."""
import io
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

LABELS = ['6B tissue protection','6B DNA-damage response','6B anti-inflammatory',
          '6D interferon response','6D TNF/Trail','6D Il1rn',
          '6C qPCR targets (RNA)','6E qPCR targets (RNA)','Hallmark IFN-alpha','Hallmark IFN-gamma']
COLORS = {'CPM':'#007e87','TMM':'#c26621','FPKM':'#7055a3'}


def save(fig, output, name):
    for extension in ('png','svg'):
        path=Path(output)/(name+'.'+extension)
        if path.exists(): raise FileExistsError(path)
    for extension in ('png','svg'):
        buffer=io.BytesIO()
        fig.savefig(buffer,format=extension,dpi=170,facecolor='white')
        data=buffer.getvalue()
        if extension=='svg':
            data=('\n'.join(line.rstrip() for line in data.decode('utf-8').splitlines())+'\n').encode('utf-8')
        with (Path(output)/(name+'.'+extension)).open('xb') as stream: stream.write(data)
    plt.close(fig)


def render(output, annotations, sets, mapping, expression, values, background, beta, summaries, ranges):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none',
                         'axes.spines.top':False,'axes.spines.right':False})
    index={r['geneID']:i for i,r in enumerate(annotations)}
    published=[];seen=set()
    for row in mapping:
        if row['source_kind']=='author_selected' and row['symbol'] not in seen:
            seen.add(row['symbol']);published.append(row)
    rows=[index[r['stable_ids']] if r['status']=='unique' else None for r in published]
    left=np.array([expression[i] if i is not None else np.full(6,np.nan) for i in rows])
    right=np.array([values[i] if i is not None else np.full(3,np.nan) for i in rows])
    labels=[r['symbol']+(' *' if not r['eligible_for_summary'] else '') for r in published]
    fig,(a,b)=plt.subplots(1,2,figsize=(12,13),gridspec_kw={'width_ratios':[2,1]})
    fig.subplots_adjust(left=.14,right=.96,top=.88,bottom=.15,wspace=.25)
    im=a.imshow(left,aspect='auto',interpolation='nearest',cmap='viridis',vmin=0)
    finite=np.abs(right[np.isfinite(right)]);limit=max(float(finite.max()) if finite.size else 0, .1)
    im2=b.imshow(right,aspect='auto',interpolation='nearest',cmap='RdBu_r',vmin=-limit,vmax=limit)
    a.set_yticks(range(len(labels)),labels);b.set_yticks(range(len(labels)),['']*len(labels))
    a.set_xticks(range(6),['PBS 1','PBS 2','WT 1','WT 2','B3 1','B3 2'],rotation=45,ha='right')
    b.set_xticks(range(3),['WT − PBS','B3 − PBS','B3 − WT'],rotation=45,ha='right')
    a.set_title('Each deposited library',pad=12);b.set_title('Difference of group means',pad=12)
    fig.colorbar(im,ax=a,location='bottom',fraction=.035,pad=.12,label='log₂(CPM + 1)')
    fig.colorbar(im2,ax=b,location='bottom',fraction=.035,pad=.12,label='Difference on log-expression scale')
    fig.suptitle('Published Figure 6 targets in the deposited RNA data',fontsize=17,y=.96)
    fig.text(.14,.925,'Fixed source order; all six libraries retained; no gene-wise significance tests.',fontsize=11)
    fig.text(.14,.035,'Author-selected panels and qPCR targets overlap; each symbol is shown once. Cxcl1 is qPCR-only in the source.\n'
             '* Below fixed CPM filter or not uniquely mapped; blank = unavailable. Colors are not pathway activity or function.\n'
             'WT = published WT IL-22; B3 = published 22-B3. Independent animal/preparation keys remain unverified.',fontsize=9,linespacing=1.6)
    save(fig,output,'published_targets')

    fig,(a,b)=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[1,1.1]})
    fig.subplots_adjust(left=.08,right=.97,top=.81,bottom=.20,wspace=.65)
    x,y=values[background,0],values[background,1]
    a.scatter(x,y,s=4,color='#73858e',alpha=.3,rasterized=True,linewidths=0)
    lo=min(float(x.min()),float(y.min()),0) if len(x) else -1
    hi=max(float(x.max()),float(y.max()),0) if len(x) else 1
    if hi==lo: hi=lo+1
    line=np.array([lo,hi]);a.plot(line,line,ls=':',color='#444444',lw=1,label='Identity guide')
    if beta is not None: a.plot(line,beta*line,color=COLORS['CPM'],lw=2,label=f'Through-origin β = {beta:.3f}')
    else: a.text(.05,.9,'Amplitude fit unavailable',transform=a.transAxes)
    a.axhline(0,color='#bbbbbb',lw=.5);a.axvline(0,color='#bbbbbb',lw=.5)
    a.set(xlabel='WT − PBS',ylabel='B3 − PBS',title=f'Fixed background: {int(background.sum()):,} gene rows')
    a.legend(fontsize=9,loc='lower right')
    full=[next(r for r in summaries if r['scale']=='CPM' and r['view']=='full' and r['membership']==s['id']) for s in sets]
    for i,r in enumerate(full):
        value=r['amplitude_residual']
        if value is None: b.text(.02,i,'NA',transform=b.get_yaxis_transform())
        else: b.plot(value,i,'o',color=COLORS['CPM'],ms=7)
    b.axvline(0,color='#999999',lw=1);b.set_yticks(range(len(sets)),[f'{label} (n={r["n_eligible"]})' for label,r in zip(LABELS,full)])
    b.set_ylim(len(sets)-.5,-.5);b.set(xlabel='Median [B3 − PBS − β × (WT − PBS)]',title='Fixed membership residuals')
    fig.suptitle('How much resembles a common response-amplitude change?',fontsize=17,y=.96)
    fig.text(.08,.88,'Primary log₂(CPM + 1); tested membership union excluded from the background fit.',fontsize=11)
    fig.text(.08,.045,'Both axes reuse the same PBS libraries and contain measurement noise. β is an unclamped descriptive reference.\n'
             'Gene rows and overlapping memberships are not independent biological replicates. Residuals do not identify STAT causality.\n'
             'n counts eligible, uniquely mapped member rows; no confidence intervals or equivalence claim.',fontsize=10,linespacing=1.5)
    save(fig,output,'amplitude_reference')

    fig,axes=plt.subplots(1,2,figsize=(15,9),sharey=True)
    fig.subplots_adjust(left=.22,right=.97,top=.82,bottom=.20,wspace=.18)
    for ax,metric,title in zip(axes,['B3_minus_WT','amplitude_residual'],['Direct B3 − WT','Residual from scale-specific amplitude fit']):
        for j,scale in enumerate(COLORS):
            for i,item in enumerate(sets):
                row=next(r for r in ranges if r['scale']==scale and r['membership']==item['id'] and r['metric']==metric)
                pos=i+(j-1)*.19
                if row['n_omission_views']:
                    ax.plot([row['omission_min'],row['omission_max']],[pos,pos],color=COLORS[scale],lw=2,alpha=.7)
                if row['full_data'] is not None: ax.plot(row['full_data'],pos,'o',color=COLORS[scale],ms=5,label=scale if i==0 else None)
                else: ax.text(.02,pos,scale+' unavailable',transform=ax.get_yaxis_transform(),fontsize=7,color=COLORS[scale])
        ax.axvline(0,color='#999999',lw=1);ax.grid(axis='y',alpha=.15)
        ax.set_title(title,pad=12);ax.set_xlabel('Median member contrast (scale-specific log units)')
    axes[0].set_yticks(range(len(sets)),LABELS);axes[0].set_ylim(len(sets)-.5,-.5)
    axes[1].legend(title='Expression scale',loc='best',fontsize=9)
    fig.suptitle('Sensitivity to one omitted library and expression scale',fontsize=17,y=.96)
    fig.text(.22,.88,'Dot: all six libraries. Line: minimum–maximum over six single-library omissions.',fontsize=11)
    fig.text(.22,.06,'Observed sensitivity ranges are not confidence intervals. All views retain the full-data CPM eligibility filter.\n'
             'TMM factors are re-estimated per view. Deposited FPKM is a separate scale, not an exact author replay.\n'
             'Published category names are source labels; qPCR targets are measured here only in deposited RNA.',fontsize=10,linespacing=1.5)
    save(fig,output,'sensitivity_ranges')
