"""Pinned fgsea replay with full-family source comparison and independent ES checks."""
import argparse,csv,json,shutil,subprocess,os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def rows(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);out=parser.parse_args().output
    env=dict(os.environ,CLI_NO_THREAD='true',LANG='C',LC_ALL='C')
    for name in ['gene_sets.csv','ranks_itdt_vs_pbs.csv','ranks_itdt_acd4_vs_itdt.csv','gsea_itdt_vs_pbs.csv','gsea_itdt_acd4_vs_itdt.csv','coverage.csv','R_session.txt','runtime_settings.txt']:
        shutil.copyfile(Path('analysis/research/runs/zh26_s2_enrichment_v1')/name,out/name)
    members={}
    for row in rows(out/'gene_sets.csv'):members.setdefault(row['gs_name'],set()).add(row['gene_symbol'])
    contrasts=['itdt_vs_pbs','itdt_acd4_vs_itdt']
    selected=['HALLMARK_IL2_STAT5_SIGNALING','HALLMARK_TNFA_SIGNALING_VIA_NFKB','HALLMARK_INTERFERON_GAMMA_RESPONSE']
    comparison=[];selected_rows=[];curves={};independent=[]
    for contrast in contrasts:
        ref={r['pathway']:r for r in rows(Path('raw_data/zhang_2026/source_v1/author/output_files')/('gsea_results_std_'+contrast+'.csv'))}
        obs={r['pathway']:r for r in rows(out/('gsea_'+contrast+'.csv'))}
        ranks=rows(out/('ranks_'+contrast+'.csv'));genes=[r['symbol'] for r in ranks];values=np.array([float(r['statistic']) for r in ranks])
        assert len(genes)==len(set(genes))
        for p in sorted(set(ref)|set(obs)):
            row={'contrast':contrast,'pathway':p,'in_source':p in ref,'in_replay':p in obs}
            if p in ref and p in obs:
                for field in ['pval','padj','log2err','ES','NES','size']:
                    a,b=[None if v in ('NA','NaN','') else float(v) for v in (obs[p][field],ref[p][field])];row[field+'_source']=b;row[field+'_replay']=a;row[field+'_difference']=None if a is None or b is None else a-b
                row['leading_edge_set_equal']=set(obs[p]['leadingEdge'].split(','))==set(ref[p]['leadingEdge'].split(','))
                row['leading_edge_order_equal']=obs[p]['leadingEdge']==ref[p]['leadingEdge']
            comparison.append(row)
            if p not in obs:continue
            hit=np.array([g in members[p] for g in genes]);weights=np.abs(values[hit]);denom=weights.sum()
            increments=np.full(len(genes),-1/(len(genes)-int(hit.sum())))
            increments[hit]=weights/denom if denom else 1/int(hit.sum())
            running=np.cumsum(increments);peak=float(running.max());trough=float(running.min());es=peak if peak > -trough else trough
            err=abs(es-float(obs[p]['ES']));assert err<1e-8,(contrast,p,err)
            independent.append(err)
            if p in selected:
                curves[contrast,p]=(running,np.flatnonzero(hit))
                selected_rows.append({'contrast':contrast,**obs[p]})
    allkeys=list(dict.fromkeys(k for row in comparison for k in row))
    with (out/'source_comparison.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=allkeys);w.writeheader();w.writerows(comparison)
    report={'absolute_tolerance':1e-8,'relative_tolerance':1e-7,
            'deterministic_rule':'ES, size and leading-edge gene set must agree; pathway identity differences are reported, never silently dropped.',
            'stochastic_rule':'Report every NES, P, adjusted P and log2err difference. Seed fixed to 42; source backend/R environment unknown, serial backend explicit. No invented stochastic agreement threshold.',
            'tested_comparisons':len(comparison),'independent_ES_checks':len(independent),'max_independent_ES_error':max(independent),
            'pathway_identity_mismatches':[r for r in comparison if not r['in_source'] or not r['in_replay']],
            'ES_mismatches':[{'contrast':r['contrast'],'pathway':r['pathway'],'difference':r.get('ES_difference')} for r in comparison if abs(r.get('ES_difference',0))>1e-8],
            'leading_edge_set_mismatches':[{'contrast':r['contrast'],'pathway':r['pathway']} for r in comparison if r.get('leading_edge_set_equal') is False],
            'max_field_discrepancy':{field:max(abs(r.get(field+'_difference') or 0) for r in comparison) for field in ['ES','NES','pval','padj','size']},
            'unestimated_stochastic_fields':[{'contrast':r['contrast'],'pathway':r['pathway'],'source_pval':r.get('pval_source'),'replay_pval':r.get('pval_replay')} for r in comparison if r.get('pval_source') is None or r.get('pval_replay') is None],
            'selected_source_panels':selected_rows}
    (out/'comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    fig,axes=plt.subplots(2,3,figsize=(14,7.5),layout='constrained')
    for i,c in enumerate(contrasts):
        for j,p in enumerate(selected):
            ax=axes[i,j];running,hit=curves[c,p];row=next(r for r in selected_rows if r['contrast']==c and r['pathway']==p)
            ax.plot(np.arange(1,len(running)+1),running,color=['#307CA0','#C55A32'][i],lw=1.2)
            ax.axhline(0,color='gray',lw=.6);lo,hi=ax.get_ylim();ax.vlines(hit+1,lo,lo+.05*(hi-lo),color='#444444',lw=.2)
            ax.set_title(p.replace('HALLMARK_','').replace('_',' '),fontsize=10)
            ax.set(xlabel=c.replace('_',' ')+' · gene rank',ylabel='Running enrichment score')
            ax.text(.98,.96,f"NES {float(row['NES']):.2f}\nBH {float(row['padj']):.2g}",transform=ax.transAxes,ha='right',va='top',fontsize=9)
    fig.suptitle('Released logFC ranking · fixed source-selected transcript sets\nGene-set association does not measure cytokine secretion or signaling',fontsize=13)
    fig.savefig(out/'enrichment.png',dpi=170);plt.close(fig)
    print(json.dumps({'comparisons':len(comparison),'ES_mismatches':len(report['ES_mismatches']),'leading_edge_set_mismatches':len(report['leading_edge_set_mismatches'])}))


if __name__=='__main__':main()
