"""Prespecified, donor-paired human RNA context; no D25K or aging inference."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import json
import math
from pathlib import Path
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

RAW=Path('raw_data/navarro_2026/followup_20261110')
QUAL=Path('analysis/research/runs/nn26_public_source_followup_v1')
FILES={'GSE318914':'GSE318914_PBMC_Gene_Expression_Count.featureCounts.txt.gz',
       'GSE318915':'GSE318915_Tcell.Gene_Expression_Count.featureCounts.txt.gz'}
GENES=['STAT3','SOCS3','TNF','IFNG','GZMB']
CONTRASTS=[('IL-10','PBS'),('IL-10-Fc','PBS'),('ms-IL10R agonist','PBS'),('ms-IL10R agonist','IL-10')]
LABELS=['IL-10 − PBS','IL-10-Fc − PBS','agonist − PBS','agonist − IL-10']
CONTEXTS=[('GSE318914','Quiescent PBMC','Quiescent PBMC'),
          ('GSE318914','LPS-stimulated PBMC','LPS-stimulated PBMC'),
          ('GSE318915','Tcell','T cells')]


def csv_out(path,rows):
    with path.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True,type=Path)
    out=parser.parse_args().output
    sample_map=list(csv.DictReader((QUAL/'public_sample_crosswalk.csv').open()))
    qualification={x['series']:x for x in json.loads((QUAL/'public_deposit_qualification.json').read_text())}
    measurements=[]; checks=0; types={}
    for series,filename in FILES.items():
        samples={x['library']:x for x in sample_map if x['series']==series}
        with gzip.open(RAW/filename,'rt') as handle:
            reader=csv.reader(handle,delimiter='\t'); header=next(reader)
            rows=list(reader)
        # Independent NumPy read/sum cross-check against streamed metadata-stage totals.
        matrix=np.asarray([x[4:] for x in rows],dtype=np.int64)
        totals=matrix.sum(axis=0)
        assert list(totals)==[int(samples[x]['total_counts']) for x in header[4:]]
        assert np.all(matrix>=0); checks+=len(totals)
        types[series]=dict(Counter(x[2] for x in rows))
        selected={g:[(i,r) for i,r in enumerate(rows) if r[1]==g] for g in GENES}
        assert all(len(x)==1 for x in selected.values())
        for gene in GENES:
            row_index,row=selected[gene][0]
            assert [row[0]]==qualification[series]['marker_ids'][gene]
            values=matrix[row_index,:]
            vector=np.log2(1.+values.astype(float)*1e6/totals)
            for j,library in enumerate(header[4:]):
                cpm=int(row[j+4])*1e6/int(samples[library]['total_counts'])
                scalar=math.log2(1+cpm)
                assert abs(scalar-vector[j])<1e-12; checks+=1
                measurements.append(dict(samples[library],gene=gene,gene_id=row[0],
                    count=int(row[j+4]),cpm=cpm,log2_cpm_plus_one=scalar))
    lookup={tuple(x[k] for k in ('series','condition','timepoint','donor','gene','treatment')):x for x in measurements}
    assert len(lookup)==len(measurements)
    strata=sorted({tuple(x[k] for k in ('series','condition','timepoint','donor','gene')) for x in measurements})
    paired=[]
    for key in strata:
        for treatment,reference in CONTRASTS:
            a,b=lookup[key+(treatment,)],lookup[key+(reference,)]
            difference=a['log2_cpm_plus_one']-b['log2_cpm_plus_one']
            independent=math.log2((a['cpm']+1)/(b['cpm']+1))
            assert abs(difference-independent)<1e-12; checks+=1
            paired.append(dict(zip(('series','condition','timepoint','donor','gene'),key),
                treatment=treatment,reference=reference,treatment_gsm=a['gsm'],reference_gsm=b['gsm'],
                difference_log2_cpm_plus_one=difference))
    grouped=defaultdict(list)
    for row in paired:
        key=tuple(row[x] for x in ('series','condition','timepoint','gene','treatment','reference'))
        grouped[key].append(row)
    summaries=[]
    for key,records in sorted(grouped.items()):
        assert sorted(x['donor'] for x in records)==['D1','D2','D3']
        values=[x['difference_log2_cpm_plus_one'] for x in records]
        median=statistics.median(values)
        assert median==sorted(values)[1]; checks+=1
        summaries.append(dict(zip(('series','condition','timepoint','gene','treatment','reference'),key),
            donors=3,median_difference=median,minimum_difference=min(values),maximum_difference=max(values),
            positive_donors=sum(x>0 for x in values),negative_donors=sum(x<0 for x in values),zero_donors=sum(x==0 for x in values)))
    csv_out(out/'measurements.csv',measurements); csv_out(out/'paired_contrasts.csv',paired)
    csv_out(out/'contrast_summaries.csv',summaries)

    plt.rcParams.update({'font.size':8,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,3,figsize=(16,8.5),layout='constrained')
    limit=max(abs(x['median_difference']) for x in summaries)
    for ax,(series,condition,title) in zip(axes,CONTEXTS):
        times=sorted({x['timepoint'] for x in summaries if x['series']==series and x['condition']==condition},key=lambda x:int(x.removesuffix('Hour')))
        keys=[(t,a,b) for t in times for a,b in CONTRASTS]
        data=np.asarray([[next(x['median_difference'] for x in summaries if (x['series'],x['condition'],x['timepoint'],x['treatment'],x['reference'],x['gene'])==(series,condition,t,a,b,g)) for g in GENES] for t,a,b in keys])
        im=ax.imshow(data,cmap='RdBu_r',vmin=-limit,vmax=limit,aspect='auto')
        ax.set_xticks(range(5),GENES,rotation=40,ha='right')
        ax.set_yticks(range(len(keys)),[t.replace('Hour',' h')+' | '+LABELS[CONTRASTS.index((a,b))] for t,a,b in keys])
        ax.set_title(title+'\n3 reported donors, paired within series')
        for i in range(data.shape[0]):
            for j in range(5): ax.text(j,i,f'{data[i,j]:.2f}',ha='center',va='center',fontsize=7,color='white' if abs(data[i,j])>.65*limit else 'black')
    fig.colorbar(im,ax=axes,shrink=.7,label='Median donor-paired difference in log2(CPM + 1)')
    fig.suptitle('Human IL-10 receptor context | all prespecified markers and contrasts\nCPM denominator: all genes in each deposited count matrix; no population test',fontsize=12)
    fig.savefig(out/'human_context_medians.png',dpi=160); fig.savefig(out/'human_context_medians.svg'); plt.close(fig)

    fig,axes=plt.subplots(2,3,figsize=(16,8.5),layout='constrained')
    colors={'D1':'#0072B2','D2':'#D55E00','D3':'#009E73'}
    for col,(series,condition,title) in enumerate(CONTEXTS):
        times=sorted({x['timepoint'] for x in paired if x['series']==series and x['condition']==condition},key=lambda x:int(x.removesuffix('Hour')))
        keys=[(t,a,b) for t in times for a,b in CONTRASTS]
        for row,gene in enumerate(['IFNG','GZMB']):
            ax=axes[row,col]
            for donor,offset in zip(['D1','D2','D3'],[-.18,0,.18]):
                points=[next(x['difference_log2_cpm_plus_one'] for x in paired if (x['series'],x['condition'],x['timepoint'],x['treatment'],x['reference'],x['gene'],x['donor'])==(series,condition,t,a,b,gene,donor)) for t,a,b in keys]
                ax.scatter(np.arange(len(keys))+offset,points,color=colors[donor],s=20,label=donor)
            ax.axhline(0,color='grey',linewidth=.7)
            ax.set_xticks(range(len(keys)),[t.replace('Hour','h')+' '+LABELS[CONTRASTS.index((a,b))] for t,a,b in keys],rotation=65,ha='right',fontsize=6)
            ax.set_title(title+' | '+gene); ax.set_ylabel('Paired difference, log2(CPM + 1)')
            if row==0 and col==0: ax.legend(frameon=False,ncol=3)
    fig.suptitle('Every reported donor | IFNG and GZMB RNA context\nDonor labels are matched only within each GEO series; no D25K, aging or functional inference',fontsize=12)
    fig.savefig(out/'human_context_donors.png',dpi=160); fig.savefig(out/'human_context_donors.svg'); plt.close(fig)
    report=dict(status='executed',measurement_rows=len(measurements),paired_contrasts=len(paired),
        summary_rows=len(summaries),independent_scalar_checks=checks,source_gene_types=types,
        normalization='log2(1 + 1e6 * gene_count / sum_of_all_deposited_gene_counts)',
        inference='exposed finite-sample, within-series donor-paired description only',
        exclusions='none; all prespecified genes, samples, times, activation conditions and contrasts retained',
        limits=['different engineered agonist, no D25K','human peripheral cells, no aged brain','RNA is not secretion or functional repair','bulk PBMC composition','three reported donors per series','no between-series donor join','library-composition-dependent CPM; no differential-expression model'])
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    (out/'.gitattributes').write_text('* -text whitespace=cr-at-eol\n',encoding='utf-8',newline='\n')
    print(json.dumps(report))


if __name__=='__main__': main()
