"""Bounded descriptive gene classes and independently sourced chromatin context."""
import argparse,csv,gzip,json,re
from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RAW=Path('raw_data/dupage_20261107')
S1=Path('analysis/research/runs/dupage_s1_reconstruction_v1')
S2=Path('analysis/research/runs/dupage_s2_state_contrast_v1')
def read(path):
    with path.open(newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(path,rows,fields=None):
    with path.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
def rank(x):
    u,inv,count=np.unique(x,return_inverse=True,return_counts=True)
    return (np.cumsum(count)-(count-1)/2)[inv]
def rho(x,y):
    return float(np.corrcoef(rank(x),rank(y))[0,1]) if len(x)>2 and np.std(x)>0 and np.std(y)>0 else None
def main():
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);out=a.parse_args().output
    s1=read(S1/'gene_contrasts.tsv');s2=read(S2/'interaction.tsv');assert [r['gene_id'] for r in s1]==[r['gene_id'] for r in s2]
    expr=np.array([float(r['HET_hi_mean_log2_fpkm1']) for r in s1]);bins=np.minimum(4,((rank(expr)-1)*5/len(expr)).astype(int))
    transcripts=defaultdict(list);gene_chroms=defaultdict(set)
    with gzip.open(RAW/'mm9_refGene.txt.gz','rt') as f:
        for fields in csv.reader(f,delimiter='\t'):
            assert len(fields)==16
            chrom,start,end,gene=fields[2],int(fields[4]),int(fields[5]),fields[12]
            if not re.fullmatch(r'chr(?:[1-9]|1[0-9]|X|Y|M)',chrom):continue
            transcripts[chrom].append((start,end,gene));gene_chroms[gene].add(chrom)
    tx={ch:(np.array([x[0] for x in rs]),np.array([x[1] for x in rs]),np.array([x[2] for x in rs])) for ch,rs in transcripts.items()}
    with gzip.open(RAW/'GSE55773_h3k27me3_qn.txt.gz','rt') as f:
        reader=csv.reader(f,delimiter='\t');header=next(reader);peakrows=[r for r in reader if r]
    assert header[0]=='' and len(set(header))==len(header)
    columns=[header.index(x) for x in ['atr.rep1','atr.rep2','rtr.rep1','rtr.rep2']]
    assert len({r[0] for r in peakrows})==len(peakrows)
    edge_records=[];domains=[];bygene=defaultdict(list);single=defaultdict(list);boundary=0
    for row in peakrows:
        assert len(row)==len(header)
        loc=row[0];match=re.fullmatch(r'(chr[^:]+):(\d+)-(\d+)',loc);assert match
        ch,start,end=match[1],int(match[2]),int(match[3]);assert start<end
        values=np.array([float(row[j]) for j in columns]);assert np.isfinite(values).all()
        change=float(values[:2].mean()-values[2:].mean())
        if ch in tx:
            starts,ends,genes=tx[ch]
            g0=set(genes[(starts<end)&(ends>start)])
            g1=set(genes[(starts<end)&(ends>start-1)])
            boundary+=len(g0^g1);assigned=g0&g1
        else:assigned=set()
        assigned={g for g in assigned if len(gene_chroms[g])==1}
        domains.append({'domain':loc,'arvey_mean_aTreg':float(values[:2].mean()),'arvey_mean_rTreg':float(values[2:].mean()),
                        'arvey_activation_delta':change,'genes_assigned':len(assigned)})
        for gene in sorted(assigned):
            bygene[gene].append(change)
            if len(assigned)==1:single[gene].append(change)
            edge_records.append({'domain':loc,'gene_id':gene,'chromosome':ch,'genes_in_domain':len(assigned),'arvey_activation_delta':change})
    gene_records=[]
    for j,(r1,r2) in enumerate(zip(s1,s2)):
        gene=r1['gene_id'];ch=r1['locus'].split(':')[0];mapped=gene in bygene and gene_chroms[gene]=={ch}
        x=float(np.median(bygene[gene])) if mapped else None
        sx=float(np.median(single[gene])) if mapped and gene in single else None
        gene_records.append({'gene_id':gene,'locus_mm10':r1['locus'],'expression_bin_1_to_5':int(bins[j])+1,
            'HET_hi_mean_log2_fpkm1':expr[j],'activation_HET':float(r1['activation_HET']),
            'activation_class':'HET_down' if float(r1['activation_HET'])<0 else 'HET_up' if float(r1['activation_HET'])>0 else 'HET_zero',
            'delta_high':float(r2['delta_high']),'delta_low':float(r2['delta_low']),'interaction':float(r2['interaction']),
            'sign_stable_loo':r2['sign_stable_all_leave_one_library']=='True',
            'chromatin_class':'uncovered' if x is None else 'positive' if x>0 else 'nonpositive',
            'arvey_activation_delta_median':x if x is not None else '',
            'domain_count':len(bygene[gene]) if mapped else 0,
            'single_gene_domain_delta_median':sx if sx is not None else '',
            'single_gene_domain_count':len(single[gene]) if sx is not None else 0})
    class_stats=[]
    for field in ['activation_class','chromatin_class']:
        for label in sorted({r[field] for r in gene_records}):
            for bn in [0,1,2,3,4,5]:
                rs=[r for r in gene_records if r[field]==label and (bn==0 or r['expression_bin_1_to_5']==bn)]
                if not rs:continue
                class_stats.append({'family':field,'class':label,'expression_bin':bn or 'all','n_loci':len(rs),
                    'median_interaction':float(np.median([r['interaction'] for r in rs])),
                    'median_delta_low':float(np.median([r['delta_low'] for r in rs])),
                    'median_delta_high':float(np.median([r['delta_high'] for r in rs])),
                    'positive_interaction_fraction':float(np.mean([r['interaction']>0 for r in rs])),
                    'loo_stable_fraction':float(np.mean([r['sign_stable_loo'] for r in rs]))})
    mapped=[r for r in gene_records if r['domain_count']];unique=[r for r in gene_records if r['single_gene_domain_count']]
    assert mapped
    assoc={name:{target:rho([r[column] for r in rs],[r[target] for r in rs]) for target in ['delta_high','delta_low','interaction']} for name,rs,column in [('all_domain_gene_overlap',mapped,'arvey_activation_delta_median'),('single_gene_domains',unique,'single_gene_domain_delta_median')]}
    stats={'source_domains':len(domains),'gene_domain_edges':len(edge_records),'domains_multiple_genes':sum(r['genes_assigned']>1 for r in domains),
           'boundary_sensitive_pairs_excluded':boundary,'eligible_rna_loci':len(gene_records),'mapped_rna_loci':len(mapped),
           'single_gene_domain_rna_loci':len(unique),'uncovered_rna_loci':len(gene_records)-len(mapped),
           'descriptive_spearman':assoc,'class_summaries':[r for r in class_stats if r['expression_bin']=='all'],
           'chromatin_scale':'mean activated minus mean resting, source log2(RPKM+0.3) quantile-normalized signal; no further log transform',
           'limits':'Adapted mm9 RefGene body-overlap mapping then exact same-chromosome symbols to mm10 RNA. Multi-gene domains and unknown unit nesting preclude target/mediation and population inference. Internal HET classes are mathematically coupled.'}
    fig,ax=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    hb=ax[0].hexbin([r['arvey_activation_delta_median'] for r in mapped],[r['interaction'] for r in mapped],gridsize=40,mincnt=1,bins='log',cmap='viridis')
    fig.colorbar(hb,ax=ax[0],label='Loci per hexbin')
    ax[0].axhline(0,color='gray',lw=.7);ax[0].axvline(0,color='gray',lw=.7)
    ax[0].set(xlabel='Arvey activated − resting chromatin signal',ylabel='DuPage RNA interaction',title='External chromatin context; mapped loci only')
    for label,color in [('positive','#D55E00'),('nonpositive','#0072B2'),('uncovered','#999999')]:
        rs=[r for r in class_stats if r['family']=='chromatin_class' and r['class']==label and r['expression_bin']!='all']
        ax[1].plot([r['expression_bin'] for r in rs],[r['median_interaction'] for r in rs],marker='o',label=label,color=color)
    ax[1].axhline(0,color='gray',lw=.7);ax[1].set(xlabel='HET/high expression quintile',ylabel='Median RNA interaction',title='Detectability context, not causal adjustment',xticks=[1,2,3,4,5]);ax[1].legend(title='Chromatin change')
    fig.suptitle('Dp1-S3 · Cross-study descriptive association; no matched KO chromatin or gene-wise tests')
    fig.savefig(out/'regulatory_context.png',dpi=180);fig.savefig(out/'regulatory_context.pdf');plt.close(fig)
    write(out/'domain_signal.tsv',domains);write(out/'gene_domain_edges.tsv',edge_records);write(out/'gene_context.tsv',gene_records);write(out/'class_summary.tsv',class_stats)
    (out/'summary.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf8');print(json.dumps(stats))
if __name__=='__main__':main()
