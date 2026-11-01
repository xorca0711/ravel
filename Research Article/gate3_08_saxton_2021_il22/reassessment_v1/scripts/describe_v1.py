"""Finite-library descriptive contrasts; no population inference or ligand design."""
from __future__ import annotations
import argparse
from collections import defaultdict
import csv
import gzip
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
PACKAGE = Path(__file__).resolve().parents[1]
LIBRARIES = ('PBS_1','PBS_2','LH5_1','LH5_2','LH30_1','LH30_2')
GROUPS = np.array(['PBS','PBS','WT','WT','B3','B3'])
VIEWS = ('full',) + tuple('omit_'+lib for lib in LIBRARIES)
SCALES = ('CPM','TMM','FPKM')
EXTERNAL = ('HALLMARK_INTERFERON_ALPHA_RESPONSE','HALLMARK_INTERFERON_GAMMA_RESPONSE')
ANNOTATIONS = ('geneID','Gene_name','Chrom','Strand','Start','End','GeneLength','Gene_type','Description')
METRICS = ('WT_minus_PBS','B3_minus_PBS','B3_minus_WT','amplitude_residual')


def require(ok, message):
    if not ok: raise ValueError(message)


def scalar(value):
    if isinstance(value, np.generic): value=value.item()
    if isinstance(value, float) and not np.isfinite(value): return None
    return value


def write_csv(path, rows, fields=None):
    if fields is None: fields=list(rows[0])
    with path.open('x', newline='', encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        writer.writerows({k:scalar(v) for k,v in row.items()} for row in rows)


def read_source(path):
    annotations=[]; values=[]
    with gzip.open(path,'rt',encoding='utf-8',newline='') as stream:
        reader=csv.DictReader(stream,delimiter='\t')
        require(len(reader.fieldnames)==len(ANNOTATIONS+LIBRARIES) and set(ANNOTATIONS+LIBRARIES)==set(reader.fieldnames), 'Unexpected deposited columns')
        for row in reader:
            annotations.append({key:row[key] for key in ANNOTATIONS})
            values.append([float(row[lib]) for lib in LIBRARIES])
    matrix=np.asarray(values,dtype=np.float64)
    require(matrix.ndim==2 and matrix.shape[1]==6 and np.isfinite(matrix).all() and (matrix>=0).all(), 'Invalid deposited numeric table')
    require(len({r['geneID'] for r in annotations})==len(annotations), 'Nonunique stable IDs')
    return annotations,matrix


def primary_scale(counts):
    require(np.equal(counts,np.floor(counts)).all(), 'Noninteger deposited counts')
    sizes=counts.sum(axis=0,dtype=np.float64)
    require((sizes>0).all(), 'Zero full-library count sum')
    cpm=counts/sizes*1e6
    eligible=(cpm>=1).sum(axis=1)>=2
    return sizes,cpm,np.log2(cpm+1),eligible


def contrasts(expression, keep):
    require(expression.shape[1]==int(keep.sum()), 'View expression dimensions disagree')
    groups=GROUPS[keep]
    require(all(np.count_nonzero(groups==g)>0 for g in ('PBS','WT','B3')), 'Missing group in view')
    means={g:expression[:,groups==g].mean(axis=1) for g in ('PBS','WT','B3')}
    return np.column_stack((means['WT']-means['PBS'],means['B3']-means['PBS'],means['B3']-means['WT']))


def amplitude_reference(values, background):
    x,y=values[background,0],values[background,1]
    denominator=float(np.dot(x,x));numerator=float(np.dot(x,y))
    if len(x)==0 or denominator==0:
        return None,denominator,numerator,'held_empty_background' if len(x)==0 else 'held_zero_denominator'
    beta=numerator/denominator
    require(np.isfinite(beta), 'Nonfinite descriptive amplitude coefficient')
    return beta,denominator,numerator,'descriptive_reference'


def memberships():
    manifest=json.loads((PACKAGE/'sources/memberships_v1.json').read_text())
    require(tuple(manifest['external_sets'])==EXTERNAL, 'External membership family changed')
    sets=[dict(p,source_kind='author_selected') for p in manifest['panels']]
    found={}
    for line in (PACKAGE/'sources/mh.all.v2026.1.Mm.symbols.gmt').read_text().splitlines():
        fields=line.split('\t')
        if fields[0] in EXTERNAL:
            require(fields[0] not in found, 'Duplicate external set')
            found[fields[0]]=dict(id=fields[0],locator=fields[1],label=fields[0].replace('HALLMARK_',''),
                                  role='external_IFN_membership',members=fields[2:],source_kind='MSigDB_2026.1.Mm')
    require(set(found)==set(EXTERNAL), 'Authoritative external memberships unavailable')
    sets += [found[name] for name in EXTERNAL]
    for item in sets:
        require(len(item['members'])>0 and len(set(item['members']))==len(item['members']), 'Empty/duplicate membership')
    return sets


def map_members(annotations, sets, eligible):
    index=defaultdict(list)
    for i,row in enumerate(annotations): index[row['Gene_name']].append(i)
    mapping=[]; resolved={}; selected={}; tested=set()
    for item in sets:
        all_unique=[]; chosen=[]
        for position,symbol in enumerate(item['members'],1):
            hits=index.get(symbol,[]);tested.update(hits)
            status='unique' if len(hits)==1 else 'unmapped' if not hits else 'ambiguous'
            allowed=status=='unique' and bool(eligible[hits[0]])
            if status=='unique': all_unique.append(hits[0])
            if allowed: chosen.append(hits[0])
            mapping.append(dict(membership=item['id'],source_kind=item['source_kind'],role=item['role'],
                locator=item['locator'],member_order=position,symbol=symbol,status=status,
                stable_ids=';'.join(annotations[i]['geneID'] for i in hits),n_exact_matches=len(hits),
                eligible_for_summary=allowed,reason='eligible' if allowed else 'below_fixed_CPM_filter' if status=='unique' else status))
        resolved[item['id']]=set(all_unique);selected[item['id']]=np.array(chosen,dtype=int)
    return mapping,resolved,selected,tested


def run_tmm(output, sizes):
    rscript=os.environ.get('SX22_RSCRIPT','X:/GitHub/ravel/analysis/corrections/statistics/.tools/R-portable/app/bin/Rscript.exe')
    library=os.environ.get('SX22_R_LIBRARY','X:/GitHub/ravel/analysis/corrections/statistics/.tools/R-library')
    env=os.environ.copy();env['LC_ALL']='C'
    try:
        process=subprocess.run([rscript,'--vanilla',str(PACKAGE/'scripts/tmm_v1.R'),str(output/'counts_for_tmm.csv'),library],
                               capture_output=True,timeout=120,env=env,check=False)
        stdout=process.stdout.decode('utf-8',errors='replace');stderr=process.stderr.decode('utf-8',errors='replace')
        error='' if process.returncode==0 else f'R exit code {process.returncode}: {stderr}'
    except (OSError,subprocess.TimeoutExpired) as exc:
        stdout='';stderr=str(exc);error=f'{type(exc).__name__}: {exc}'
    (output/'tmm_stdout.log').write_text(stdout,encoding='utf-8')
    (output/'tmm_stderr.log').write_text(stderr,encoding='utf-8')
    rows=[]; factors={}
    if not error:
        try:
            rows=list(csv.DictReader(io.StringIO(stdout)))
            require(len(rows)==36,'Unexpected TMM factor coverage')
            for view in VIEWS:
                expected=[lib for lib in LIBRARIES if view!='omit_'+lib]
                subset=[r for r in rows if r['view']==view]
                require([r['library'] for r in subset]==expected,'TMM factor library order mismatch')
                f=np.array([float(r['tmm_factor']) for r in subset])
                require(np.isfinite(f).all() and (f>0).all() and abs(np.log(f).sum())<1e-10,'Invalid TMM factor normalization')
                for row in subset:
                    total=sizes[LIBRARIES.index(row['library'])]
                    require(float(row['library_size'])==total,'TMM full-count denominator changed')
                    require(np.isclose(float(row['effective_library_size']),total*float(row['tmm_factor']),rtol=1e-12),'TMM effective size mismatch')
                factors[view]=f
        except (ValueError,KeyError) as exc:
            error=f'TMM output qualification failed: {exc}';rows=[];factors={}
    fields=['view','library','library_size','tmm_factor','effective_library_size','R_version','edgeR_version']
    write_csv(output/'normalization_factors.csv',rows,fields)
    return factors,dict(status='qualified' if not error else 'held_runtime',error=error,rscript=rscript,library=library,
                        reference='edgeR automatic refColumn=NULL; TMM factors re-estimated per view',
                        parameters=dict(logratioTrim=.3,sumTrim=.05,doWeighting=True,Acutoff=-1e10))


def summarize_case(item, indices, mapping, values, residual, scale, view, fit_status):
    own=[r for r in mapping if r['membership']==item['id']]
    row=dict(scale=scale,view=view,membership=item['id'],label=item['label'],role=item['role'],
             n_source_members=len(own),n_unique=sum(r['status']=='unique' for r in own),
             n_unmapped=sum(r['status']=='unmapped' for r in own),n_ambiguous=sum(r['status']=='ambiguous' for r in own),
             n_eligible=len(indices),status='held_runtime' if values is None else 'observed_members' if len(indices) else 'no_eligible_members',
             amplitude_status=fit_status)
    for j,key in enumerate(METRICS[:3]): row[key]=float(np.median(values[indices,j])) if values is not None and len(indices) else None
    row[METRICS[3]]=float(np.median(residual[indices])) if residual is not None and len(indices) else None
    return row


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    output=Path(parser.parse_args().output).resolve()
    require(output.parent==ROOT/'analysis/research/runs' and output.is_dir(),'Fresh runner directory required')
    require(all(p.name in {'receipt.json','stdout.log','stderr.log'} for p in output.iterdir()),'Existing output artifacts')
    annotations,counts=read_source(ROOT/'raw_data/Sx22/GSE160217_060120_22_readcount_genename.xls.gz')
    f_annotations,fpkm=read_source(ROOT/'raw_data/Sx22/GSE160217_060120_22_fpkm_genename.xls.gz')
    require(annotations==f_annotations and counts.shape==(35275,6),'Source annotation/shape disagreement')
    sizes,cpm,primary,eligible=primary_scale(counts)
    sets=memberships();mapping,resolved,selected,tested=map_members(annotations,sets,eligible)
    background=eligible.copy();background[list(tested)]=False
    inventory=[dict(row_index=i+1,**r,primary_eligible=bool(eligible[i]),libraries_CPM_ge_1=int((cpm[i]>=1).sum()),
                    tested_membership_row=i in tested,amplitude_background=bool(background[i])) for i,r in enumerate(annotations)]
    write_csv(output/'gene_inventory.csv',inventory)
    write_csv(output/'counts_for_tmm.csv',[dict(geneID=r['geneID'],**{lib:int(counts[i,j]) for j,lib in enumerate(LIBRARIES)}) for i,r in enumerate(annotations)])
    write_csv(output/'member_mapping.csv',mapping)
    overlap=[]
    for a in sets:
        for b in sets:
            overlap.append(dict(first=a['id'],second=b['id'],shared_source_symbols=len(set(a['members'])&set(b['members'])),
                                shared_unique_rows=len(resolved[a['id']]&resolved[b['id']]),
                                shared_eligible_rows=len(set(selected[a['id']])&set(selected[b['id']]))))
    write_csv(output/'membership_overlap.csv',overlap)
    factors,tmm_status=run_tmm(output,sizes)
    fits=[];summaries=[];tested_rows=[];primary_rows=[];primary_values=None;primary_beta=None
    for scale in SCALES:
        for view in VIEWS:
            keep=np.array([view!='omit_'+lib for lib in LIBRARIES])
            missing=scale=='TMM' and view not in factors
            if missing:
                values=residual=None;beta=None;denominator=numerator=None;fit_status='held_TMM_runtime'
            else:
                expression=(primary[:,keep] if scale=='CPM' else np.log2(counts[:,keep]/(sizes[keep]*factors[view])*1e6+1)
                            if scale=='TMM' else np.log2(fpkm[:,keep]+1))
                values=contrasts(expression,keep)
                beta,denominator,numerator,fit_status=amplitude_reference(values,background)
                residual=values[:,1]-beta*values[:,0] if beta is not None else None
            fits.append(dict(scale=scale,view=view,n_background=int(background.sum()),sum_x_squared=denominator,
                             sum_x_y=numerator,beta=beta,status=fit_status,
                             n_PBS=int(np.sum(GROUPS[keep]=='PBS')),n_WT=int(np.sum(GROUPS[keep]=='WT')),n_B3=int(np.sum(GROUPS[keep]=='B3'))))
            for item in sets:
                summaries.append(summarize_case(item,selected[item['id']],mapping,values,residual,scale,view,fit_status))
            if values is not None:
                for i in sorted(tested):
                    row=dict(scale=scale,view=view,geneID=annotations[i]['geneID'],symbol=annotations[i]['Gene_name'],primary_eligible=bool(eligible[i]),
                             **{key:float(values[i,j]) for j,key in enumerate(METRICS[:3])})
                    row['amplitude_residual']=float(residual[i]) if residual is not None else None;tested_rows.append(row)
            if scale=='CPM' and view=='full':
                primary_values=values;primary_beta=beta
                for i,annotation in enumerate(annotations):
                    row=dict(geneID=annotation['geneID'],symbol=annotation['Gene_name'],primary_eligible=bool(eligible[i]))
                    row.update({lib+'_CPM':float(cpm[i,j]) for j,lib in enumerate(LIBRARIES)})
                    row.update({lib+'_log2_CPM_plus_1':float(primary[i,j]) for j,lib in enumerate(LIBRARIES)})
                    row.update({key:float(values[i,j]) for j,key in enumerate(METRICS[:3])})
                    row['amplitude_residual']=float(residual[i]) if residual is not None else None;primary_rows.append(row)
    write_csv(output/'primary_gene_expression.csv',primary_rows)
    write_csv(output/'amplitude_fits.csv',fits);write_csv(output/'panel_set_summaries.csv',summaries)
    write_csv(output/'tested_gene_sensitivity.csv',tested_rows,
              ['scale','view','geneID','symbol','primary_eligible',*METRICS])
    ranges=[]
    for scale in SCALES:
        for item in sets:
            cases=[r for r in summaries if r['scale']==scale and r['membership']==item['id']]
            full=next(r for r in cases if r['view']=='full')
            for metric in METRICS:
                values=[r[metric] for r in cases if r['view']!='full' and r[metric] is not None]
                ranges.append(dict(scale=scale,membership=item['id'],metric=metric,full_data=full[metric],
                                   n_omission_views=len(values),omission_min=min(values) if values else None,
                                   omission_max=max(values) if values else None,interpretation='Observed sensitivity range, not a confidence interval'))
    write_csv(output/'sensitivity_ranges.csv',ranges)
    from plot_v1 import render
    render(output,annotations,sets,mapping,primary,primary_values,background,primary_beta,summaries,ranges)
    report=dict(scope='Exposed finite-library description; no population inference',libraries=list(LIBRARIES),
                source_rows=len(annotations),primary_eligible_rows=int(eligible.sum()),tested_union_rows=len(tested),
                amplitude_background_rows=int(background.sum()),membership_count=len(sets),mapping_rows=len(mapping),
                summary_rows=len(summaries),scales=list(SCALES),views=list(VIEWS),tmm=tmm_status,
                primary_beta=primary_beta,python=sys.version,numpy=np.__version__,
                endpoint='Differences of group means of per-library log2(normalized expression + 1)',
                shared_control_limit='Both vehicle-relative axes share PBS; noisy axes and unknown units prevent population or mechanistic inference',
                held_jobs={'Q5_R2b':'Independent biological units remain unverified',
                           'Q6':'Original author gene/filter/zero-handling/aggregation choices not recovered',
                           'Q7':'Raw signaling/function values, replicate/nesting keys and panel identities unqualified',
                           'Q8':'Animal-resolved exposure/cessation/later-function joins unqualified'},
                scientific_acceptance='not_assessed')
    with (output/'summary.json').open('x',encoding='utf-8') as stream:
        json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps({key:report[key] for key in ['source_rows','primary_eligible_rows','membership_count','summary_rows']}))


if __name__=='__main__':main()
