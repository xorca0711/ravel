"""Presentation-only unit labels for the frozen A5/A11 paired estimates.

Reads saved inference tables; does not recompute fits, intervals or decisions.
The original figure and its analysis/report producer remain unchanged.
"""
from pathlib import Path
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
OUT = HERE / 'figures/revision_20260929'
SOURCES = [ROOT/'RQ_Specified/A5_developmental_programme_reuse/tables/test_v1/inference.tsv',
           ROOT/'RQ_Specified/A11_lesion_programme_addition/tables/test_v2/inference.tsv']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False})
    r5, r11 = [pd.read_csv(p, sep='\t') for p in SOURCES]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.7), layout='constrained')
    labels5 = ['Full external signature','Without Guo identity genes','Without identity + controls','Full signature vs resting AT2']
    labels11 = ['Lesion-derived primary','Lesion change minus shared','Lesion, stress genes excluded','Injury-lesion pair']
    for ax, rs, labels, value, lo, hi, color, title, unit in [
        (axes[0],r5,labels5,'mean','mean_low','mean_high','#176B70','A5: developmental-gene recruitment','mice'),
        (axes[1],r11,labels11,'HL','low','high','#8356A1','A11: lesion-associated expression','patient pairs')]:
        y = np.arange(len(rs))[::-1]
        ax.errorbar(rs[value],y,xerr=np.vstack([rs[value]-rs[lo],rs[hi]-rs[value]]),fmt='o',color=color,capsize=4,markersize=7)
        ax.axvline(0,color='#7D8992',lw=1)
        ax.set_yticks(y,[f'{label}\n(n={int(n)} {unit})' for label,n in zip(labels,rs.n)])
        ax.set_ylim(-.6,3.6)
        ax.set_title(title,loc='left',fontweight='bold',pad=16)
        ax.grid(axis='x',alpha=.15)
    axes[0].set_xlabel('Mean within-mouse paired difference (detection percentage points)\n95% t intervals; 500-UMI expectation')
    axes[1].set_xlabel('Within-patient paired location shift (log2 CPM)\nHodges-Lehmann; exact 95% intervals')
    axes[1].axvline(.1,color='#C88938',ls=':',lw=1,label='Primary planning margin 0.10')
    axes[1].legend(loc='lower right',fontsize=8,frameon=False)
    fig.suptitle('Distinct questions and measurement scales; expression does not establish lineage or function',fontsize=12)
    outputs = []
    for suffix in ['png','svg']:
        path = OUT/f'a5_a11_results.{suffix}'
        fig.savefig(path,dpi=180,metadata={'Creator':'scRNA_seq presentation revision'})
        outputs.append(path)
    plt.close(fig)
    record={'mode':'presentation_only_from_saved_estimates','script_sha256':sha(Path(__file__)),
            'inputs':{p.relative_to(ROOT).as_posix():sha(p) for p in SOURCES},
            'outputs':{p.name:sha(p) for p in outputs},
            'change':'Label A5 n as mice and A11 n as patient pairs; original estimates, intervals and historical outputs preserved.'}
    (OUT/'render_record.json').write_text(json.dumps(record,indent=2)+'\n')
    print('Rendered A5/A11 unit-label revision from two saved inference tables')

if __name__ == '__main__':
    main()
