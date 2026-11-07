"""Descriptive interaction with fixed-universe library and pseudocount sensitivities."""
import argparse,csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

S0=Path('analysis/research/runs/dupage_s0_qualification_v1')
S1=Path('analysis/research/runs/dupage_s1_reconstruction_v1')
GROUPS=['HET_hi','HET_lo','KO_hi','KO_lo']
def read(p):
    with p.open(newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows):
    with p.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
def estimate(raw,group,pseudo=1,omit=None):
    means=np.array([np.log2(raw[:,[j for j,g in enumerate(group) if g==name and j!=omit]]+pseudo).mean(axis=1) for name in GROUPS]).T
    high=means[:,2]-means[:,0];low=means[:,3]-means[:,1]
    return high,low,low-high
def summary(h,l,i):
    return {'high_rms':float(np.sqrt(np.mean(h*h))),'low_rms':float(np.sqrt(np.mean(l*l))),
            'rms_low_high_ratio':float(np.sqrt(np.mean(l*l)/np.mean(h*h))),
            'high_median_absolute':float(np.median(abs(h))),'low_median_absolute':float(np.median(abs(l))),
            'interaction_median':float(np.median(i)),'interaction_median_absolute':float(np.median(abs(i))),
            'interaction_rms':float(np.sqrt(np.mean(i*i)))}
def main():
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);out=a.parse_args().output
    m=[x for x in read(S0/'sample_manifest.tsv') if x['retained']=='True'];group=[x['genotype']+'_'+x['state'] for x in m]
    src={r['gene_id']:r for r in read(S0/'common_fpkm.tsv')};s1=read(S1/'gene_contrasts.tsv')
    raw=np.array([[float(src[r['gene_id']][x['gsm']+'_FPKM']) for x in m] for r in s1]);h,l,i=estimate(raw,group)
    assert np.allclose(h,[float(r['delta_high']) for r in s1],rtol=0,atol=1e-12)
    assert np.allclose(l,[float(r['delta_low']) for r in s1],rtol=0,atol=1e-12)
    loo=np.array([estimate(raw,group,omit=j)[2] for j in range(len(m))])
    low05=estimate(raw,group,pseudo=.5);low2=estimate(raw,group,pseudo=2)
    same=((np.sign(loo)==np.sign(i)).all(axis=0))
    records=[]
    for j,r in enumerate(s1):
        records.append({k:r[k] for k in ['gene_id','gene_short_name','locus','activation_HET','activation_KO']} | {
            'delta_high':h[j],'delta_low':l[j],'interaction':i[j],
            'leave_one_library_min':loo[:,j].min(),'leave_one_library_max':loo[:,j].max(),
            'sign_stable_all_leave_one_library':bool(same[j]),'interaction_pseudocount_0_5':low05[2][j],
            'interaction_pseudocount_2':low2[2][j]})
    sensitivities=[{'sensitivity':'primary',**summary(h,l,i)},
                   {'sensitivity':'pseudocount_0.5',**summary(*low05)},
                   {'sensitivity':'pseudocount_2',**summary(*low2)}]
    for j,x in enumerate(m):sensitivities.append({'sensitivity':'omit_'+x['gsm'],**summary(*estimate(raw,group,omit=j))})
    design=np.array([[1,int(x['genotype']=='KO'),int(x['state']=='lo'),int(x['genotype']=='KO' and x['state']=='lo')] for x in m])
    stats={'eligible_loci':len(i),'primary':summary(h,l,i),'positive_interactions':int((i>0).sum()),
           'negative_interactions':int((i<0).sum()),'zero_interactions':int((i==0).sum()),
           'sign_stable_all_leave_one_library':int(same.sum()),
           'sign_stable_both_pseudocounts':int(((np.sign(low05[2])==np.sign(i))&(np.sign(low2[2])==np.sign(i))).sum()),
           'leave_one_library_rms_ratio_range':[min(x['rms_low_high_ratio'] for x in sensitivities[3:]),max(x['rms_low_high_ratio'] for x in sensitivities[3:])],
           'design_rank':int(np.linalg.matrix_rank(design)),'nominal_library_residual_df':len(m)-int(np.linalg.matrix_rank(design)),
           'inferential_residual_df':'not qualified: independent biological units unknown',
           'scope':'Fixed 11,614 S1 loci; descriptive interaction. Omission extrema are sensitivity ranges, not confidence intervals.'}
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    ax[0].hist(i,bins=100,color='#0072B2');ax[0].axvline(0,color='black',lw=.7)
    ax[0].set(xlabel='(KO − HET)low − (KO − HET)high',ylabel='Number of eligible loci',title='Signed interaction, log₂(FPKM + 1)')
    ys=np.arange(len(sensitivities)); ax[1].scatter([x['rms_low_high_ratio'] for x in sensitivities],ys,color='#D55E00')
    ax[1].set_yticks(ys,[x['sensitivity'].replace('omit_GSM14236','omit …') for x in sensitivities],fontsize=8)
    ax[1].axvline(1,color='gray',ls='--');ax[1].set(xlabel='RMS genotype contrast: low / high',title='Library omission and zero-handling sensitivity');ax[1].invert_yaxis()
    fig.suptitle('Dp1-S2 · Descriptive state dependence; no population tests or confidence intervals')
    fig.savefig(out/'state_dependence.png',dpi=180);fig.savefig(out/'state_dependence.pdf');plt.close(fig)
    write(out/'interaction.tsv',records);write(out/'sensitivity.tsv',sensitivities)
    (out/'summary.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf8');print(json.dumps(stats))
if __name__=='__main__':main()
