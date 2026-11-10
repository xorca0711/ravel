"""Signed moderated-statistic ranking sensitivity with a fixed source universe."""
import argparse,csv,json,os,shutil,subprocess
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def rows(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


def number(value):
    return None if value in ('NA','NaN','') else float(value)


def curve(ranks,members):
    hit=np.array([r['symbol'] in members for r in ranks]);values=np.array([float(r['statistic']) for r in ranks]);w=np.abs(values[hit]);n=int(hit.sum())
    increments=np.full(len(ranks),-1/(len(ranks)-n));increments[hit]=w/w.sum() if w.sum() else 1/n
    return np.cumsum(increments)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
    subprocess.run([shutil.which('Rscript'),'--vanilla','Research Article/gate3_11_zhang_2026_nk/scripts/ranking_sensitivity_v1.R',str(out)],check=True,env=dict(os.environ,CLI_NO_THREAD='true',LANG='C',LC_ALL='C'))
    s2=Path('analysis/research/runs/zh26_s2_enrichment_v1');members={}
    for r in rows(s2/'gene_sets.csv'):members.setdefault(r['gs_name'],set()).add(r['gene_symbol'])
    contrasts=['itdt_vs_pbs','itdt_acd4_vs_itdt'];selected=['HALLMARK_IL2_STAT5_SIGNALING','HALLMARK_TNFA_SIGNALING_VIA_NFKB','HALLMARK_INTERFERON_GAMMA_RESPONSE']
    result=[];errors=[];curves={}
    for c in contrasts:
        before={r['pathway']:r for r in rows(s2/('gsea_'+c+'.csv'))};after={r['pathway']:r for r in rows(out/('gsea_t_'+c+'.csv'))}
        assert before.keys()==after.keys()
        a=rows(out/('ranks_'+c+'.csv'));b=rows(s2/('ranks_'+c+'.csv'));assert {r['symbol'] for r in a}=={r['symbol'] for r in b}
        for path in after:
            x,y=before[path],after[path];running=curve(a,members[path]);es=float(running.max()) if running.max()>-running.min() else float(running.min())
            error=abs(es-float(y['ES']));assert error<1e-8;errors.append(error)
            leadx=set(x['leadingEdge'].split(','));leady=set(y['leadingEdge'].split(','))
            result.append(dict(contrast=c,pathway=path,logFC_ES=float(x['ES']),moderated_t_ES=float(y['ES']),logFC_NES=number(x['NES']),moderated_t_NES=number(y['NES']),logFC_BH=number(x['padj']),moderated_t_BH=number(y['padj']),ES_sign_agrees=bool(np.sign(float(x['ES']))==np.sign(float(y['ES']))),leading_edge_overlap=len(leadx&leady),leading_edge_union=len(leadx|leady)))
            if path in selected:curves[c,path]=(curve(b,members[path]),running)
    with (out/'ranking_comparison.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
    summary={'independent_ES_checks':len(errors),'max_independent_ES_error':max(errors),
             'ES_sign_changes':[{'contrast':r['contrast'],'pathway':r['pathway']} for r in result if not r['ES_sign_agrees']],
             'source_selected_panels':[r for r in result if r['pathway'] in selected],
             'interpretation':'Exposed ranking-dependence diagnostic on identical genes and pathways; source P thresholds are not new confirmatory decisions; no independent replication.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    fig,axes=plt.subplots(2,3,figsize=(14,7.5),layout='constrained')
    for i,c in enumerate(contrasts):
        for j,path in enumerate(selected):
            ax=axes[i,j];old,new=curves[c,path]
            ax.plot(np.arange(1,len(old)+1),old,label='Released logFC rank',color='#307CA0',lw=1.1)
            ax.plot(np.arange(1,len(new)+1),new,label='Moderated t rank',color='#C55A32',lw=1.1)
            ax.axhline(0,color='gray',lw=.6);ax.set_title(path.replace('HALLMARK_','').replace('_',' '),fontsize=10)
            ax.set(xlabel=c.replace('_',' ')+' · rank within method',ylabel='Running enrichment score');ax.legend(fontsize=8)
    fig.suptitle('Ranking sensitivity · identical source genes and pathway membership\nCurves use different gene orders; neither measures signaling activity',fontsize=13)
    fig.savefig(out/'ranking_sensitivity.png',dpi=170);plt.close(fig)
    print(json.dumps({'ES_checks':len(errors),'ES_sign_changes':len(summary['ES_sign_changes'])}))


if __name__=='__main__':main()
