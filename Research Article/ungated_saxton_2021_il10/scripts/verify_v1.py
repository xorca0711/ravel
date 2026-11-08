"""Independent scalar verification, with no production analysis imports."""
import csv,gzip,hashlib,json,math,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
PKG=Path(__file__).resolve().parents[1]
RUN=ROOT/'analysis/research/runs/sx10_description_v1'
LIBS=['Unt_1','Unt_2','BS30_1','BS30_2','BS65_1','BS65_2','BS45_1','BS45_2']
GROUPS={'PBS':[0,1],'WT':[2,3],'DE':[4,5],'SUPER':[6,7]}
METRICS=['WT-PBS','DE-PBS','SUPER-PBS','DE-WT','SUPER-WT']
def read(p):
    with open(p,encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def close(a,b):
    assert math.isclose(float(a),float(b),rel_tol=1e-10,abs_tol=1e-10),(a,b)
def main():
    raw=[]
    for k in ['readcount','fpkm']:
        with gzip.open(ROOT/f'raw_data/Sx10/GSE160332_070720_10_{k}_genename.txt.gz','rt',encoding='utf-8') as f:raw.append(list(csv.DictReader(f,delimiter='\t')))
    ids=[r['gene_id'] for r in raw[0]];fm={r['gene_id']:r for r in raw[1]};assert len(ids)==len(set(ids))==len(fm) and set(ids)==set(fm)
    counts=[[int(r[l]) for l in LIBS] for r in raw[0]];fpkm=[[float(fm[g][l]) for l in LIBS] for g in ids]
    for r in raw[0]:assert {k:v for k,v in r.items() if k not in LIBS}=={k:v for k,v in fm[r['gene_id']].items() if k not in LIBS}
    sizes=[sum(c[j] for c in counts) for j in range(8)]
    eligible=[sum(c[j]*1e6/sizes[j]>=1 for j in range(8))>=2 for c in counts]
    panels=json.loads((PKG/'sources/figure5_memberships_v1.json').read_text())['panels'];symbols=list(dict.fromkeys(s for ss in panels.values() for s in ss));idx={}
    for s in symbols:
        hits=[i for i,r in enumerate(raw[0]) if r['gene_name']==s];assert len(hits)==1;idx[s]=hits[0]
    bg=[i for i,e in enumerate(eligible) if e and i not in idx.values()];target_set=set(idx.values());universe=sorted(set(bg)|target_set)
    bg_set=set(bg)
    outtarget={(r['scale'],r['view'],r['symbol']):r for r in read(RUN/'target_sensitivity.csv')}
    outfit={(r['scale'],r['view'],r['variant']):r for r in read(RUN/'amplitude_fits.csv')}
    outnorm={(r['view'],r['library']):r for r in read(RUN/'normalization_factors.csv')}
    outpan={(r['scale'],r['view'],r['panel'],r['variant']):r for r in read(RUN/'panel_summaries.csv')}
    outvals={(r['scale'],r['symbol'],r['library']):r for r in read(RUN/'target_library_values.csv')}
    primary=read(RUN/'all_gene_primary.csv');assert [r['gene_id'] for r in primary]==ids
    for view in ['full']+['omit_'+l for l in LIBS]:
        keep=[j for j,l in enumerate(LIBS) if view!='omit_'+l];positive=[c for c in counts if all(c[j]>0 for j in keep)]
        geos=[math.exp(statistics.mean(math.log(c[j]) for j in keep)) for c in positive]
        sf={j:statistics.median(c[j]/g for c,g in zip(positive,geos)) for j in keep};sfgeo=math.exp(statistics.mean(math.log(v) for v in sf.values()));lg=math.exp(statistics.mean(math.log(sizes[j]) for j in keep));den={j:sf[j]/sfgeo*lg for j in keep}
        for j in keep:
            r=outnorm[view,LIBS[j]];close(den[j],r['effective_library_size']);close(sf[j]/sfgeo,r['median_ratio_factor']);assert int(r['positive_reference_rows'])==len(positive)
        for scale in ['CPM','MR_CPM','FPKM']:
            calculations={};vectors={}
            needed=range(len(ids)) if scale=='CPM' and view=='full' else universe
            for i in needed:
                abund={j:(fpkm[i][j] if scale=='FPKM' else counts[i][j]*1e6/(sizes[j] if scale=='CPM' else den[j])) for j in keep}
                expr={j:math.log2(a+1) for j,a in abund.items()};means={g:statistics.mean(expr[j] for j in js if j in keep) for g,js in GROUPS.items()}
                v={m:means[m.split('-')[0]]-means[m.split('-')[1]] for m in METRICS};calculations[i]=v
                if i in target_set:vectors[i]=(abund,expr)
                if scale=='CPM' and view=='full':
                    r=primary[i];assert (r['eligible']=='True')==eligible[i] and (r['background']=='True')==(i in bg_set)
                    for j in keep:close(expr[j],r[LIBS[j]+'_log2_CPM_plus_1'])
                    for m in METRICS:close(v[m],r[m])
            for variant in ['DE','SUPER']:
                xx=math.fsum(calculations[i]['WT-PBS']**2 for i in bg);xy=math.fsum(calculations[i]['WT-PBS']*calculations[i][variant+'-PBS'] for i in bg);beta=xy/xx
                r=outfit[scale,view,variant];close(beta,r['beta']);close(xx,r['sum_x_squared']);close(xy,r['sum_xy']);assert int(r['background_rows'])==len(bg)
                close(math.sqrt(statistics.mean((calculations[i][variant+'-PBS']-beta*calculations[i]['WT-PBS'])**2 for i in bg)),r['rms_residual'])
                for v in calculations.values():v[variant+'_residual']=v[variant+'-PBS']-beta*v['WT-PBS']
            for s,i in idx.items():
                r=outtarget[scale,view,s]
                for k,v in calculations[i].items():close(v,r[k])
                if view=='full':
                    for j in keep:
                        r=outvals[scale,s,LIBS[j]];close(vectors[i][0][j],r['abundance']);close(vectors[i][1][j],r['log2_plus_1'])
            for panel,ss in panels.items():
                ii=[idx[s] for s in ss if eligible[idx[s]]]
                for variant in ['DE','SUPER']:
                    r=outpan[scale,view,panel,variant];assert int(r['eligible_members'])==len(ii)
                    for field,m in [('median_WT_PBS','WT-PBS'),('median_variant_PBS',variant+'-PBS'),('median_direct',variant+'-WT'),('median_residual',variant+'_residual')]:close(statistics.median(calculations[i][m] for i in ii),r[field])
                    x=[calculations[i]['WT-PBS'] for i in ii];y=[calculations[i][variant+'-PBS'] for i in ii]
                    expected={'closer_to_PBS':sum(abs(b)<abs(a) for a,b in zip(x,y)),'same_direction':sum(a*b>0 for a,b in zip(x,y)),'weaker_same_direction':sum(a*b>0 and abs(b)<abs(a) for a,b in zip(x,y)),'opposite_direction':sum(a*b<0 for a,b in zip(x,y))}
                    for k,v in expected.items():assert int(r[k])==v
    for r in read(RUN/'target_ranges.csv'):
        cases=[v for (scale,view,s),v in outtarget.items() if scale==r['scale'] and s==r['symbol']];m=r['metric']
        close(r['full'],next(v[m] for v in cases if v['view']=='full'));close(r['omission_min'],min(float(v[m]) for v in cases if v['view']!='full'));close(r['omission_max'],max(float(v[m]) for v in cases if v['view']!='full'))
    print('PASS: 58735 primary rows; all raw ID joins, 64 MR factors, 552 target library values, 621 target cases, 54 amplitude fits, 162 panel cases, 483 plotted/exported ranges; tolerance 1e-10')
if __name__=='__main__':main()
