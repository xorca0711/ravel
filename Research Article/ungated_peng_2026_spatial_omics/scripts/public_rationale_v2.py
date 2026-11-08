"""Rendering-only correction; exact displayed scalars come from frozen run tables."""
import argparse,json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch

ROOT=Path(__file__).resolve().parents[3]

def main(out):
    a=pd.read_csv(ROOT/'analysis/research/runs/A12_public_cells_v1_20261108/paired_summary.csv')
    d=pd.read_csv(ROOT/'analysis/research/runs/A12_public_cells_v1_20261108/depth_standardized_deltas.csv')
    s=pd.read_csv(ROOT/'analysis/research/runs/Pg1_public_spatial_v3_20261108/paired_summary.csv')
    values=[]
    def av(gene,metric):
        r=a[a.population.eq('AT2_u20')&a.feature.eq(gene)&a.metric.eq(metric)]
        assert len(r)==1;v=float(r.iloc[0]['mean']);values.append(dict(source='A12 paired_summary',population='AT2_u20',feature=gene,metric=metric,value=v,n=int(r.iloc[0]['n'])));return v
    def sv(mode):
        r=s[s['mode'].eq(mode)&s.weighting.eq('equal_section')&s.comparison.eq('LUAD-AAH')&s.metric.eq('lag1')]
        assert len(r)==1;v=float(r.iloc[0]['mean']);values.append(dict(source='Pg1 paired_summary',population=mode,feature='IL1B__CLDN4',metric='LUAD-AAH lag1',value=v,n=int(r.iloc[0]['n'])));return v
    rap=av('IL1RAP','fraction_detected');intensity=av('IL1RAP','positive_mean_log');joint=av('IL1R1__IL1RAP','joint_fraction')
    z=d[d.feature.eq('IL1R1__IL1RAP')];depthjoint=float(z.delta.mean());values.append(dict(source='A12 depth_standardized_deltas',population='AT2_u20',feature='IL1R1__IL1RAP',metric='joint_fraction',value=depthjoint,n=len(z)))
    spatial=sv('depth');composition=sv('depth_composition')
    pd.DataFrame(values).to_csv(out/'figure_values.csv',index=False)
    plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42})
    fig,ax=plt.subplots(figsize=(13,8));fig.subplots_adjust(left=.025,right=.975,bottom=.025,top=.975);ax.set(xlim=(0,13),ylim=(0,8));ax.axis('off')
    boxes=[(.35,5.15,5.95,2.15,'MEASURED: A12 candidate nuclei',
        f'12 paired patients, LUAD minus normal\nIL1RAP detection: {100*rap:+.2f} percentage points\nIntensity among detected nuclei: {intensity:+.3f} log2 units\nIL1R1 / IL1RAP co-detection: {100*joint:+.2f} points\nAfter common-depth standardization: {100*depthjoint:+.2f} points','#DCEAF4'),
        (6.7,5.15,5.95,2.15,'MEASURED: Visium RNA organization',
        f'10 paired patients, LUAD minus AAH\nIL1B / CLDN4 one-hop statistic: {spatial:+.4f}\nWith broad RNA-composition covariates: {composition:+.4f}\nLattice adjacency only; spots contain mixtures\nPatient-level description, not a spot significance test','#DCEAF4'),
        (2.0,3.3,9.,1.15,'WHAT THESE RESULTS CHANGE',
        'The aggregate RNA pattern has detection and spatial components.\nDepth, candidate selection and broad composition remain consequential.','#E4EFE9'),
        (.35,.65,5.95,1.8,'ALTERNATIVE EXPLANATIONS RETAINED',
        'Transferred-label selection and epithelial mixtures\nRNA depth and background RNA\nTissue geometry and other inflammatory inputs\nSensitivity checks do not identify a unique cause.','#FFF0DA'),
        (6.7,.65,5.95,1.8,'FUNCTIONAL HYPOTHESIS STILL UNTESTED',
        'Does recipient configuration alter an IL-1 response?\nNeeds independently established state identity\nand protein / functional response measurements.\nRNA co-detection is not receptor assembly or signaling.','#F0E9F5')]
    text_bounds=[]
    for x,y,w,h,title,body,color in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.04',facecolor=color,edgecolor='#55616B',lw=1.1))
        title_artist=ax.text(x+w/2,y+h-.23,title,ha='center',va='center',fontsize=11,weight='bold')
        body_artist=ax.text(x+w/2,y+(h-.45)/2,body,ha='center',va='center',fontsize=10.4,linespacing=1.45)
        text_bounds.extend([(title_artist,(x+.08,y+.06,x+w-.08,y+h-.06)),(body_artist,(x+.08,y+.06,x+w-.08,y+h-.4))])
    for begin,end in [((3.3,5.05),(4.2,4.55)),((9.7,5.05),(8.8,4.55)),((4.2,3.2),(3.3,2.55)),((8.8,3.2),(9.7,2.55))]:ax.add_patch(FancyArrowPatch(begin,end,arrowstyle='->',mutation_scale=15,color='#66717A',linestyle='--',lw=1.2))
    ax.text(6.5,7.75,'Public-data results and biological rationale',ha='center',fontsize=17,weight='bold')
    ax.text(6.5,7.47,'Same source lineage; exposed descriptive analyses',ha='center',fontsize=11,color='#45525B')
    ax.text(6.5,.17,'Dashed arrows represent interpretation, not demonstrated causation. No accepted mechanism or independent validation.',ha='center',fontsize=9.5)
    fig.canvas.draw();renderer=fig.canvas.get_renderer();checks=[]
    for artist,bounds in text_bounds:
        b=artist.get_window_extent(renderer).transformed(ax.transData.inverted());ok=b.x0>=bounds[0] and b.y0>=bounds[1] and b.x1<=bounds[2] and b.y1<=bounds[3]
        checks.append({'text':artist.get_text(),'fits_box':bool(ok)})
    assert all(x['fits_box'] for x in checks),checks
    for ext in ['png','pdf']:fig.savefig(out/f'public_data_rationale_v2.{ext}',dpi=300)
    plt.close(fig)
    (out/'layout_verification.json').write_text(json.dumps({'checks':checks,'all_text_fits':True,'display_values':len(values),'analysis_recomputed':False,'supersedes_render_only':'Pg1_public_spatial_v3_20261108/public_data_rationale'},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();main(args.output)
