"""Distinct source endpoints, observed Ns, fixed references and reported SE."""
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def export(fig,output,name):
    fig.savefig(output/(name+'.png'),dpi=300,bbox_inches='tight')
    fig.savefig(output/(name+'.pdf'),bbox_inches='tight',metadata={'CreationDate':None,'ModDate':None})
    plt.close(fig)


def plot(output,mapping,data):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    endpoints={e['id']:e for e in mapping['endpoints']}
    groups={(g['endpoint'],g['group']):g for g in data['groups']}
    observations={}
    for row in data['observations']:
        if not row['missing']:observations.setdefault((row['endpoint'],row['group']),[]).append(row['value'])
    contrasts={}
    for row in data['contrasts']:contrasts.setdefault(row['endpoint'],[]).append(row)
    colors=['#647481','#247f9d','#aa7840','#80649b']

    def caption(e):
        relation='≥' if e['caption_n_relation']=='at_least' else '='
        return 'caption n'+relation+str(e['caption_n'])

    def point_panel(ax,eid,title,ylabel):
        e=endpoints[eid];labels=[]
        for i,g in enumerate(e['groups']):
            row=groups[eid,g['id']];values=observations[eid,g['id']]
            if g['normalization_reference']:
                ax.hlines(1,i-.20,i+.20,color=colors[i],linewidth=2)
                ax.scatter(i,1,marker='s',facecolors='none',edgecolors=colors[i],s=38,zorder=3)
                label=g['label']+'\nreference=1\n'+str(row['source_n'])+' source cells'
            else:
                offsets=np.linspace(-.16,.16,len(values)) if len(values)>1 else np.array([0.])
                ax.scatter(i+offsets,values,s=25,alpha=.85,color=colors[i],edgecolors='white',linewidths=.35)
                ax.hlines(row['mean'],i-.24,i+.24,color='#222222',linewidth=1.7,zorder=4)
                label=g['label']+'\nn_src='+str(row['source_n'])
            labels.append(label)
        ax.set(xticks=range(len(labels)),xticklabels=labels,ylabel=ylabel,title=title+'\n'+caption(e))
        ax.set_xlim(-.55,len(labels)-.45)
        ax.set_ylim(bottom=0)
        ax.grid(axis='y',color='#ededed',linewidth=.55)
        ax.set_axisbelow(True)

    fig,axes=plt.subplots(2,3,figsize=(14,9),layout='constrained')
    fig.suptitle('F1e: separate epithelial length and EdU-percentage observations\nDots are source records; black marks are group means; no pairing or population intervals',fontsize=14)
    for j,day in enumerate([1,3,5]):
        point_panel(axes[0,j],f'F1e_tongue_D{day}',f'Tongue length, wound day {day}','Length (μm)')
        point_panel(axes[1,j],f'F1e_edu_D{day}',f'EdU-positive fraction, wound day {day}','Source percentage (%)')
    export(fig,output,'fig01_tongue_edu')

    fig,axes=plt.subplots(1,2,figsize=(12,5.6),layout='constrained')
    fig.suptitle('Outgrowth endpoints remain separate by experiment and day\nAll available source records; no individual-cell speed or cross-panel pooling',fontsize=14)
    point_panel(axes[0],'F1g_outgrowth','F1g: day-10 explant outgrowth','Distance (mm)')
    point_panel(axes[1],'F5f_outgrowth','F5f: day-5 K14+ outgrowth','Distance (mm)')
    export(fig,output,'fig02_outgrowth')

    fig,axes=plt.subplots(4,2,figsize=(13,18),layout='constrained')
    fig.suptitle('Source-normalized expression, activity and protein are distinct endpoints\nAll-1 reference controls are normalization constants, not measured zero biological variance',fontsize=14)
    panels=[('F4h_Aim2_qpcr','F4h: Aim2 normalized expression','Normalized arbitrary units'),
            ('F5a_Casp1_qpcr','F5a: Casp1 qPCR','Normalized fold change'),
            ('F5c_Il18_qpcr','F5c: Il18 qPCR','Normalized fold change'),
            ('F5c_Il1b_qpcr','F5c: Il1b qPCR','Normalized fold change'),
            ('F5a_CASP1_activity','F5a: CASP1 activity','U/g total protein'),
            ('F5b_CASP1_activity','F5b: CASP1 activity with YVAD','U/g total protein'),
            ('F5c_IL18_protein','F5c: IL-18 protein','pg/g total protein'),
            ('F5c_IL1beta_protein','F5c: IL-1β protein','pg/g total protein')]
    for ax,(eid,title,unit) in zip(axes.flat,panels):point_panel(ax,eid,title,unit)
    export(fig,output,'fig03_expression_activity_protein')

    fig,axes=plt.subplots(4,2,figsize=(14,19),layout='constrained')
    fig.suptitle('Reported fitted wound-area decay summaries\nPoints ± source-reported SE; source N shown for each group; no raw-rate reconstruction or contrast intervals',fontsize=14)
    panel_ids=['F1b_rate_D30','F1b_rate_D180','F4g_rate','F4h_rate','F5b_rate','F5d_rate','F5e_rate','F5g_rate']
    titles=['F1b: D30 history','F1b: D180 history','F4g: history × Aim2 background','F4h: Aim2 OE in naive background',
            'F5b: history × CASP1 inhibition','F5d: history × Il18 background','F5e: history × Il1r1 background','F5g: Aim2 OE × IL1R1 blockade']
    for ax,eid,title in zip(axes.flat,panel_ids,titles):
        e=endpoints[eid];labels=[]
        for i,g in enumerate(e['groups']):
            row=groups[eid,g['id']]
            ax.errorbar(i,row['mean'],yerr=row['reported_se'],fmt='o',color=colors[i],capsize=4,markersize=6,linewidth=1.3)
            labels.append(textwrap.fill(g['label'],16)+'\nN='+str(row['source_n']))
        cs=contrasts[eid]
        if len(cs)==1:note='Mean difference = '+format(cs[0]['mean_contrast'],'.4g')+' day⁻¹'
        else:
            a,b,c=[format(x['mean_contrast'],'.4g') for x in cs]
            note=('OE effects: Ig '+a+', anti '+b if eid=='F5g_rate' else 'History effects: reference '+a+', altered '+b)+'\nDifference of effects = '+c+' day⁻¹'
        ax.set(xticks=range(len(labels)),xticklabels=labels,xlabel=note,ylabel='Rate constant (day⁻¹)',title=title+'\n'+caption(e),xlim=(-.5,len(labels)-.5))
        ax.axhline(0,color='#aaaaaa',linewidth=.6);ax.grid(axis='y',color='#ededed',linewidth=.55);ax.set_axisbelow(True)
    export(fig,output,'fig04_reported_rates')

    fig,axes=plt.subplots(2,1,figsize=(13,9),layout='constrained')
    fig.suptitle('F1b: sparse D30-history wound-area source observations\nHorizontal black marks are daily means; columns are not established animal trajectories; no refitting',fontsize=14)
    for ax,gid,color,label in zip(axes,['Ctrl','PI'],colors[:2],['Ctrl','D30 PI']):
        ticks=[]
        for day in range(11):
            eid=f'F1b_area_D{day}';values=observations[eid,gid];row=groups[eid,gid]
            ax.scatter(day+np.linspace(-.18,.18,len(values)),values,color=color,s=20,alpha=.8,edgecolors='white',linewidths=.3)
            ax.hlines(row['mean'],day-.26,day+.26,color='#222222',linewidth=1.5)
            ticks.append(str(day)+'\nn_src='+str(len(values)))
        ax.set(xticks=range(11),xticklabels=ticks,xlabel='Days after wounding (counts are daily source records)',ylabel='Wound area (mm²)',title=label,xlim=(-.5,10.5))
        ax.set_ylim(bottom=0);ax.grid(axis='y',color='#ededed',linewidth=.55);ax.set_axisbelow(True)
    export(fig,output,'fig05_daily_wound_area')
