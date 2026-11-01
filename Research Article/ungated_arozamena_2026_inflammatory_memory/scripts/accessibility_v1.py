"""Frozen four-locus GRCm39 adaptation on paired finite-library barcodes."""
import argparse,csv,gzip,json,math
from pathlib import Path
import numpy as np
import rna_extension_v1 as rna
from accessibility_core_v1 import TARGETS,FAMILIES,read_regions,count_fragments,FragmentFailure,aggregate,require

ROOT=rna.ROOT;PACKAGE=rna.PACKAGE

def source_features(specs):
    output={t:[] for t in TARGETS}
    for spec in specs:
        with gzip.open(ROOT/spec['paths'][1],'rt',encoding='utf-8') as f:
            rows=[line.rstrip('\r\n').split('\t') for line in f if line.strip()]
        for target in TARGETS:
            found=[x for x in rows if len(x)>=6 and x[1]==target and x[2]=='Gene Expression']
            if len(found)==1:
                x=found[0];output[target].append(dict(library=spec['id'],stable_id=x[0],symbol=x[1],chrom=x[3],start=int(x[4]),end=int(x[5])))
    return output

def load_rna(specs):
    prior=ROOT/'analysis/research/runs/arz1_rna_description_v1';qc={}
    with gzip.open(prior/'barcode_qc.csv.gz','rt',newline='') as f:
        for row in csv.DictReader(f):
            if row['library'].startswith('GSE329778_'):qc[(row['library'],row['barcode'])]=row
    output={}
    for spec in specs:
        lib=spec['id'];m=rna.feature_metadata(spec);n=len(m['barcodes']);counts=np.zeros((n,len(TARGETS)),np.int64);depth=np.zeros(n,np.int64);keep=np.zeros(n,bool);symbol_status={}
        positions={}
        for j,(target,gid) in enumerate(TARGETS.items()):
            found=[i for i,name in enumerate(m['names']) if name==target]
            good=len(found)==1 and m['ids'][found[0]]==gid;symbol_status[target]='qualified' if good else 'held_mapping'
            if good:positions[found[0]]=j
        mito=np.array([name.startswith('mt-') for name in m['names']],bool)
        for c,ix,values in rna.mtx_columns(ROOT/spec['paths'][0],m['mapping'],n):
            d=int(values.sum());mt=int(values[mito[ix]].sum());detected=len(values);passed=rna.qc_pass(d,detected,mt);old=qc[(lib,m['barcodes'][c])]
            require(d==int(old['rna_counts']) and mt==int(old['mitochondrial_counts']) and detected==int(old['detected_rna_genes']) and str(passed)==old['rna_qc_pass'],'Frozen RNA barcode QC disagreement: '+lib)
            depth[c]=d;keep[c]=passed
            for i,v in zip(ix,values):
                j=positions.get(int(i))
                if j is not None:counts[c,j]=int(v)
        output[lib]=dict(barcodes=m['barcodes'],rna_counts=counts,rna_depth=depth,rna_qc=keep,symbol_status=symbol_status)
        print('Verified frozen RNA depths/QC: '+lib,flush=True)
    old_summaries={}
    with gzip.open(prior/'library_gene_summaries.csv.gz','rt',newline='') as f:
        for row in csv.DictReader(f):
            if row['library'] in output and row['stable_id'] in TARGETS.values():old_summaries[(row['library'],row['subset'],row['stable_id'])]=row
    return output,old_summaries

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);out=Path(parser.parse_args().output).resolve()
    require(out.parent==ROOT/'analysis/research/runs' and out.is_dir() and all(p.name in ['receipt.json','stdout.log','stderr.log'] for p in out.iterdir()),'Fresh runner output required')
    config=json.loads((PACKAGE/'config/accessibility_sources_v1.json').read_text());specs=config['rna_libraries']
    regions,gtf_headers=read_regions(ROOT/config['gtf'],source_features(specs));rna.write_json(out/'region_provenance.json',dict(gtf_headers=gtf_headers,loci=regions))
    data,old_summaries=load_rna(specs);validations=[]
    for source in config['fragments']:
        lib=source['library'];d=data[lib]
        try:
            depth,counts,diag=count_fragments(ROOT/source['path'],d['barcodes'],regions,source['expected_headers'],lambda n:print(lib+': '+str(n)+' fragment rows traversed',flush=True))
            d.update(fragment_depth=depth,fragment_counts=counts,fragment_status='qualified')
        except FragmentFailure as exc:diag=exc.details;d['fragment_status']='held'
        diag['library']=lib;diag['path']=source['path'];validations.append(diag);print('Fragment traversal '+lib+': '+diag['status'],flush=True)
    rna.write_json(out/'source_validation.json',validations)
    # Finish every source attempt first; only valid EOF/CRC traversals release endpoints.
    populations=[];rna_rows=[];frag_rows=[];reuse=[];summaries={};holds=[]
    for target,r in regions.items():
        if r['status']!='qualified':holds.append(dict(component=target,reason=r.get('hold_reason','region mapping')))
    with rna.csv_writer(out/'barcode_depths.csv.gz',['library','barcode','rna_depth','nuclear_fragment_depth','prior_rna_qc','paired_all','paired_rna_qc','status']) as dw, rna.csv_writer(out/'barcode_locus_counts.csv.gz',['library','barcode','target','stable_id','rna_count','tss_2kb_union_fragments','gene_body_fragments','rna_status','region_status']) as cw:
        for lib,d in data.items():
            if d['fragment_status']!='qualified':holds.append(dict(component=lib,reason='fragment source validation failed'));continue
            paired=(d['rna_depth']>0)&(d['fragment_depth']>0);subsets={'all':paired,'rna_qc':paired&d['rna_qc']}
            for c,barcode in enumerate(d['barcodes']):
                dw.writerow(dict(library=lib,barcode=barcode,rna_depth=int(d['rna_depth'][c]),nuclear_fragment_depth=int(d['fragment_depth'][c]),prior_rna_qc=bool(d['rna_qc'][c]),paired_all=bool(paired[c]),paired_rna_qc=bool(subsets['rna_qc'][c]),status='qualified_source'))
                for j,(target,gid) in enumerate(TARGETS.items()):
                    good=regions[target]['status']=='qualified';rgood=d['symbol_status'][target]=='qualified'
                    cw.writerow(dict(library=lib,barcode=barcode,target=target,stable_id=gid,rna_count=int(d['rna_counts'][c,j]) if rgood else '',tss_2kb_union_fragments=int(d['fragment_counts'][c,j,0]) if good else '',gene_body_fragments=int(d['fragment_counts'][c,j,1]) if good else '',rna_status=d['symbol_status'][target],region_status=regions[target]['status']))
            for subset,mask in subsets.items():
                original=(d['rna_depth']>0)&(d['rna_qc'] if subset=='rna_qc' else True);same=np.array_equal(mask,original)
                populations.append(dict(library=lib,subset=subset,original_rna_barcodes=int(original.sum()),paired_barcodes=int(mask.sum()),removed_for_zero_nuclear_fragments=int((original&~mask).sum()),unchanged_from_prior_rna=bool(same),paired_rna_denominator=int(d['rna_depth'][mask].sum()),paired_nuclear_fragment_denominator=int(d['fragment_depth'][mask].sum())))
                if not mask.any():holds.append(dict(component=lib+'/'+subset,reason='empty paired population'))
                for j,(target,gid) in enumerate(TARGETS.items()):
                    rr=aggregate(d['rna_counts'][:,j],d['rna_depth'],mask) if d['symbol_status'][target]=='qualified' else aggregate(d['rna_counts'][:,j],d['rna_depth'],np.zeros(len(mask),bool))
                    rna_rows.append(dict(library=lib,subset=subset,target=target,stable_id=gid,**rr));old=old_summaries.get((lib,subset,gid));check='not_identical_selection'
                    if same and old is not None and rr['n']:
                        require(rr['n']==int(old['n_barcodes']) and rr['denominator']==int(old['all_source_rna_denominator']) and rr['count']==int(old['gene_count']),'Prior RNA sum/count mismatch')
                        require(math.isclose(rr['pooled_log'],float(old['pooled_log2_cpm1']),rel_tol=1e-10,abs_tol=1e-10) and math.isclose(rr['equal_log'],float(old['equal_log2_cpm1']),rel_tol=1e-10,abs_tol=1e-10),'Prior RNA transformed summary mismatch');check='matched_prior_same_selection'
                    reuse.append(dict(library=lib,subset=subset,target=target,unchanged_selection=bool(same),check=check,prior_pooled_log2_cpm1=old['pooled_log2_cpm1'] if old else '',current_pooled_log2_cpm1=rr['pooled_log'],prior_equal_log2_cpm1=old['equal_log2_cpm1'] if old else '',current_equal_log2_cpm1=rr['equal_log']))
                    for k,family in enumerate(FAMILIES):
                        fr=aggregate(d['fragment_counts'][:,j,k],d['fragment_depth'],mask) if regions[target]['status']=='qualified' else aggregate(d['fragment_counts'][:,j,k],d['fragment_depth'],np.zeros(len(mask),bool))
                        frag_rows.append(dict(library=lib,subset=subset,target=target,stable_id=gid,region_family=family,**fr));summaries[(lib,subset,target,family)]=(rr,fr)
    for filename,rows in [('paired_populations.csv',populations),('library_rna_summaries.csv',rna_rows),('library_fragment_summaries.csv',frag_rows),('rna_reuse_checks.csv',reuse)]:
        if rows:
            with rna.csv_writer(out/filename,list(rows[0])) as w:w.writerows(rows)
        else:
            with rna.csv_writer(out/filename,['status']) as w:w.writerow(dict(status='held_no_valid_libraries'))
    pairs=[]
    for label in ['LGR5','KRT20']:
        post='GSE329778_'+label;control='GSE329778_CTRL'
        for subset in ['all','rna_qc']:
            for weight in ['pooled','equal']:
                for family in FAMILIES:
                    for target,gid in TARGETS.items():
                        key=(post,subset,target,family);other=(control,subset,target,family);row=dict(contrast=label+'_minus_CTRL',post_library=post,control_library=control,subset=subset,weighting=weight,region_family=family,target=target,stable_id=gid,status='held')
                        if key in summaries and other in summaries:
                            rp,fp=summaries[key];rc,fc=summaries[other];field=weight+'_log'
                            row.update(rna_post_log2_cpm1=rp[field],rna_control_log2_cpm1=rc[field],fragment_post_log2_cpm1=fp[field],fragment_control_log2_cpm1=fc[field],rna_difference=rp[field]-rc[field] if rp[field] is not None and rc[field] is not None else None,fragment_difference=fp[field]-fc[field] if fp[field] is not None and fc[field] is not None else None)
                            if row['rna_difference'] is not None and row['fragment_difference'] is not None:row['status']='defined'
                        pairs.append(row)
    fields=['contrast','post_library','control_library','subset','weighting','region_family','target','stable_id','status','rna_post_log2_cpm1','rna_control_log2_cpm1','fragment_post_log2_cpm1','fragment_control_log2_cpm1','rna_difference','fragment_difference']
    with rna.csv_writer(out/'paired_contrasts.csv',fields) as w:w.writerows(pairs)
    receipt=json.loads((out/'receipt.json').read_text())
    with rna.csv_writer(out/'source_hashes.csv',['path','sha256']) as w:w.writerows({k:v[k] for k in ['path','sha256']} for v in receipt['inputs'])
    from plot_accessibility_v1 import figures
    figures(out,pairs,list(TARGETS))
    summary=dict(analysis='Arz1.accessibility_description_v1',n_fragment_sources=len(validations),n_valid_fragment_sources=sum(v['status']=='qualified' for v in validations),n_qualified_loci=sum(r['status']=='qualified' for r in regions.values()),n_paired_contrast_rows=len(pairs),n_defined_paired_contrasts=sum(r['status']=='defined' for r in pairs),holds=holds,all_valid_sources_reached_eof_before_endpoints=True,biological_independence='unknown',scientific_acceptance='not_assessed',interpretation='GRCm39 finite-library fixed-locus adaptation, not exact author replay, state attribution, promoter validation or causal memory')
    rna.write_json(out/'summary.json',summary);print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
