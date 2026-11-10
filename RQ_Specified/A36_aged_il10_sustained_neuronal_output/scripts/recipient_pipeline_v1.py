"""Governed A36 sparse extraction and independently reconstructed decomposition."""
import argparse
from collections import defaultdict
import csv
import gzip
import json
import math
from pathlib import Path
import platform
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def read(path):
    with path.open(encoding='utf-8') as f: return list(csv.DictReader(f, delimiter='\t'))


def write(path,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)


def main():
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();cfg=json.loads(Path(a.config).read_text());out=Path(a.output)
    subprocess.run([sys.executable,cfg['bounded_launcher'],'--script',cfg['R_script'],'--config',a.config,'--output',str(out)],check=True)
    cells=read(out/'cell_denominators.tsv');bycell={int(r['cell_index']):r for r in cells}
    assert len(bycell)==len(cells)==len({r['barcode'] for r in cells})
    groups=defaultdict(list)
    for cell,r in bycell.items():groups[(r['celltype'],r['condition'])].append(cell)
    recovery={(r['celltype'],r['condition']):int(r['cells']) for r in read(Path(cfg['recovery_table']))}
    for t in cfg['celltypes']:
        for c in cfg['conditions']:assert len(groups[t,c])==recovery[t,c]
    present={r['gene']:r['present']=='TRUE' for r in read(out/'marker_availability.tsv')}
    assert set(present)==set(cfg['genes'])
    values=defaultdict(list);raws=defaultdict(list);seen=set();maxerr=0
    with gzip.open(out/'selected_entries.tsv.gz','rt') as f:
        for r in csv.DictReader(f,delimiter='\t'):
            cell=int(r['cell_index']);gene=r['gene'];info=bycell[cell]
            assert gene in present and present[gene] and (cell,gene) not in seen;seen.add((cell,gene))
            raw=float(r['raw_count']);norm=float(r['normalized']);total=float(info['library_total'])
            assert raw>0 and raw==int(raw) and total>=raw and math.isfinite(norm)
            calculated=math.log1p(cfg['scale_factor']*raw/total);error=abs(norm-calculated);maxerr=max(maxerr,error)
            assert error<=cfg['tolerance']
            key=(info['celltype'],info['condition'],gene);values[key].append(calculated);raws[key].append(raw)
    summaries=[];checks=0
    def equal(x,y):
        nonlocal checks
        checks+=1
        if y is None:assert x=='NA'
        else:assert math.isclose(float(x),y,rel_tol=cfg['tolerance'],abs_tol=cfg['tolerance'])
    rsum=read(out/'summaries_R.tsv');assert len(rsum)==len(cfg['celltypes'])*len(cfg['conditions'])*len(cfg['genes'])
    assert len({(r['celltype'],r['condition'],r['gene']) for r in rsum})==len(rsum)
    for r in rsum:
        key=(r['celltype'],r['condition'],r['gene']);n=len(groups[key[:2]]);is_present=present[key[2]]
        assert (r['present']=='TRUE')==is_present;equal(r['n_cells'],n)
        vals=dict(total_raw=math.fsum(raws[key]) if is_present else None,
                  n_detected=len(raws[key]) if is_present else None,
                  mean_log_expression=math.fsum(values[key])/n if n and is_present else None,
                  detection_fraction=len(raws[key])/n if n and is_present else None)
        for field,value in vals.items():equal(r[field],value)
        summaries.append(dict(celltype=key[0],condition=key[1],gene=key[2],present=is_present,n_cells=n,**vals))
    write(out/'summaries.tsv',summaries)
    lut={(r['celltype'],r['condition'],r['gene']):r for r in summaries};contrasts=[];decomp=[]
    for left,right in cfg['contrasts']:
        for t in cfg['celltypes']:
            for g in cfg['genes']:
                l,r=lut[t,left,g],lut[t,right,g]
                contrasts.append(dict(contrast=left+'-'+right,celltype=t,gene=g,n_left=l['n_cells'],n_right=r['n_cells'],
                    mean_log_difference=None if l['mean_log_expression'] is None or r['mean_log_expression'] is None else l['mean_log_expression']-r['mean_log_expression'],
                    detection_difference=None if l['detection_fraction'] is None or r['detection_fraction'] is None else l['detection_fraction']-r['detection_fraction']))
        for g in cfg['ifn_genes']:
            for metric in ['mean_log_expression','detection_fraction']:
                nl=sum(len(groups[t,left]) for t in cfg['lineage_bins']);nr=sum(len(groups[t,right]) for t in cfg['lineage_bins'])
                if not present[g] or any(not groups[t,c] for t in cfg['lineage_bins'] for c in [left,right]):
                    decomp.append(dict(contrast=left+'-'+right,gene=g,metric=metric,total_difference=None,representation=None,within_bin=None,n_left=nl,n_right=nr));continue
                ps=[len(groups[t,left])/nl for t in cfg['lineage_bins']];qs=[len(groups[t,right])/nr for t in cfg['lineage_bins']]
                x=[lut[t,left,g][metric] for t in cfg['lineage_bins']];y=[lut[t,right,g][metric] for t in cfg['lineage_bins']]
                representation=math.fsum((p-q)*(a+b)/2 for p,q,a,b in zip(ps,qs,x,y))
                within=math.fsum((a-b)*(p+q)/2 for p,q,a,b in zip(ps,qs,x,y))
                total=math.fsum(p*a-q*b for p,q,a,b in zip(ps,qs,x,y))
                # Independent direct pooling of reconstructed entries, including implicit zeros.
                totals=[]
                for c,n in [(left,nl),(right,nr)]:
                    if metric=='mean_log_expression':totals.append(math.fsum(v for t in cfg['lineage_bins'] for v in values[t,c,g])/n)
                    else:totals.append(sum(len(values[t,c,g]) for t in cfg['lineage_bins'])/n)
                equal(total,totals[0]-totals[1]);equal(representation+within,total)
                decomp.append(dict(contrast=left+'-'+right,gene=g,metric=metric,total_difference=total,representation=representation,within_bin=within,n_left=nl,n_right=nr))
    write(out/'contrasts.tsv',contrasts);write(out/'decomposition.tsv',decomp)
    fig,axes=plt.subplots(2,2,figsize=(11,7));colors=['#367388','#bc7856','#6b8d60']
    for ax,(left,right) in zip(axes.flat,cfg['contrasts']):
        records=[r for r in decomp if r['contrast']==left+'-'+right and r['metric']=='mean_log_expression']
        for j,field in enumerate(['representation','within_bin','total_difference']):
            ax.bar([i+(j-1)*.24 for i in range(len(records))],[r[field] if r[field] is not None else float('nan') for r in records],width=.23,label=field.replace('_',' '),color=colors[j])
        ax.axhline(0,color='gray',linewidth=.7);ax.set_xticks(range(len(records)),[r['gene'] for r in records]);ax.set_title(left+' minus '+right);ax.set_ylabel('Mean log-RNA difference');ax.spines[['right','top']].set_visible(False)
    axes.flat[0].legend(fontsize=8)
    fig.suptitle('A36: arithmetic decomposition across three original lineage-associated bins',fontsize=12)
    fig.text(.5,.015,'Within-bin retains unresolved state mixture. Condition pools; no mouse-level inference or survival measurement.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.045,1,.96));fig.savefig(out/'decomposition.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(11,7))
    for ax,t in zip(axes.flat,cfg['celltypes']):
        for c,color in zip(cfg['conditions'],['#708da6','#9a9a9a','#c28262','#56978b']):
            ax.plot(cfg['ifn_genes'],[lut[t,c,g]['mean_log_expression'] for g in cfg['ifn_genes']],marker='o',label=c,color=color)
        ax.set_title(t);ax.set_ylabel('Mean log-RNA');ax.spines[['right','top']].set_visible(False)
    axes.flat[0].legend(fontsize=8);fig.suptitle('A36: measured markers within original broad bins; no aggregate IFN score',fontsize=12)
    fig.tight_layout();fig.savefig(out/'recipient_markers.png',dpi=180);plt.close(fig)
    (out/'independent_verification.json').write_text(json.dumps(dict(status='passed',cells=len(cells),sparse_entries=len(seen),summary_and_decomposition_checks=checks,max_log_reconstruction_error=maxerr,same_source_not_replication=True,
      methods='R summaries compared with Python math.fsum reconstructed from integer counts and complete cell denominators; decomposition sum checked against independently pooled entries.'),indent=2)+'\n')
    (out/'scope.json').write_text(json.dumps(dict(conditions=cfg['conditions'],original_bins=cfg['celltypes'],no_relabeling=True,no_population_inference=True,no_later_survival_endpoint=True,python=platform.python_version(),matplotlib=matplotlib.__version__),indent=2)+'\n')
    print(json.dumps(dict(status='complete',cells=len(cells),checks=checks)))


if __name__=='__main__':main()
