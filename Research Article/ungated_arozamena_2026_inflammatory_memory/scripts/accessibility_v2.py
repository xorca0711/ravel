"""Prospective dual-definition fixed-locus finite-library description."""
import argparse,json,math
from pathlib import Path
import numpy as np
import rna_extension_v1 as rna
from accessibility_v1 import source_features,load_rna
from accessibility_core_v2 import TARGETS,FAMILIES,DEFINITIONS,read_regions,count_fragments,FragmentFailure,aggregate,require

ROOT=rna.ROOT;PACKAGE=rna.PACKAGE

def write_rows(out,name,rows,fields=None):
    with rna.csv_writer(out/name,fields or (list(rows[0]) if rows else ['status'])) as w:
        w.writerows(rows if rows else [dict(status='held_no_valid_libraries')])

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);out=Path(parser.parse_args().output).resolve()
    require(out.parent==ROOT/'analysis/research/runs' and out.is_dir() and all(p.name in ['receipt.json','stdout.log','stderr.log'] for p in out.iterdir()),'Fresh runner output required')
    config=json.loads((PACKAGE/'config/accessibility_sources_v1.json').read_text());specs=config['rna_libraries']
    regions,gtf_headers=read_regions(ROOT/config['gtf'],source_features(specs));rna.write_json(out/'region_provenance.json',dict(gtf_headers=gtf_headers,loci=regions))
    data,old_summaries=load_rna(specs);validations=[]
    for source in config['fragments']:
        lib=source['library'];d=data[lib]
        try:
            depth,counts,diag,collisions=count_fragments(ROOT/source['path'],d['barcodes'],regions,source['expected_headers'],lambda n:print(lib+': '+str(n)+' fragment rows traversed',flush=True))
            d.update(fragment_depth=depth,fragment_counts=counts,fragment_status='qualified',collisions=collisions)
        except FragmentFailure as exc:diag=exc.details;d['fragment_status']='held'
        diag['library']=lib;diag['path']=source['path'];validations.append(diag);print('Fragment traversal '+lib+': '+diag['status'],flush=True)
    rna.write_json(out/'source_validation.json',validations)
    # Every source attempt finishes before any measurement endpoint is released.
    populations=[];rna_rows=[];frag_rows=[];reuse=[];summaries={};holds=[];locus_collision_rows=[]
    for target,r in regions.items():
        if r['status']!='qualified':holds.append(dict(component=target,reason=r.get('hold_reason','region mapping')))
    with rna.csv_writer(out/'collision_barcodes.csv.gz',['library','barcode','opposite_strand_groups','canonical_groups','noncanonical_groups','rna_allowlisted']) as w:
        for lib,d in data.items():
            if d['fragment_status']=='qualified':
                for barcode,row in sorted(d['collisions'].items()):w.writerow(dict(library=lib,barcode=barcode,**row))
    for v in validations:
        if v['status']=='qualified':
            for row in v['collision_locus_regions']:locus_collision_rows.append(dict(library=v['library'],**row))
    write_rows(out,'collision_locus_regions.csv',locus_collision_rows)
    with rna.csv_writer(out/'barcode_depths.csv.gz',['count_definition','library','barcode','rna_depth','nuclear_fragment_depth','prior_rna_qc','paired_all','paired_rna_qc','status']) as dw, rna.csv_writer(out/'barcode_locus_counts.csv.gz',['count_definition','library','barcode','target','stable_id','rna_count','tss_2kb_union_fragments','gene_body_fragments','rna_status','region_status']) as cw:
        for lib,d in data.items():
            if d['fragment_status']!='qualified':holds.append(dict(component=lib,reason='fragment source validation failed'));continue
            paired_primary=(d['rna_depth']>0)&(d['fragment_depth']['strand_records']>0)
            paired_grouped=(d['rna_depth']>0)&(d['fragment_depth']['coordinate_groups']>0)
            require(np.array_equal(paired_primary,paired_grouped),'Paired populations differ between count definitions')
            for definition in DEFINITIONS:
                fd=d['fragment_depth'][definition];fc=d['fragment_counts'][definition]
                paired=(d['rna_depth']>0)&(fd>0);subsets={'all':paired,'rna_qc':paired&d['rna_qc']}
                for c,barcode in enumerate(d['barcodes']):
                    dw.writerow(dict(count_definition=definition,library=lib,barcode=barcode,rna_depth=int(d['rna_depth'][c]),nuclear_fragment_depth=int(fd[c]),prior_rna_qc=bool(d['rna_qc'][c]),paired_all=bool(paired[c]),paired_rna_qc=bool(subsets['rna_qc'][c]),status='qualified_source'))
                    for j,(target,gid) in enumerate(TARGETS.items()):
                        good=regions[target]['status']=='qualified';rgood=d['symbol_status'][target]=='qualified'
                        cw.writerow(dict(count_definition=definition,library=lib,barcode=barcode,target=target,stable_id=gid,rna_count=int(d['rna_counts'][c,j]) if rgood else '',tss_2kb_union_fragments=int(fc[c,j,0]) if good else '',gene_body_fragments=int(fc[c,j,1]) if good else '',rna_status=d['symbol_status'][target],region_status=regions[target]['status']))
                for subset,mask in subsets.items():
                    original=(d['rna_depth']>0)&(d['rna_qc'] if subset=='rna_qc' else True);same=np.array_equal(mask,original)
                    populations.append(dict(count_definition=definition,library=lib,subset=subset,original_rna_barcodes=int(original.sum()),paired_barcodes=int(mask.sum()),removed_for_zero_nuclear_fragments=int((original&~mask).sum()),unchanged_from_prior_rna=bool(same),positive_sets_agree_between_definitions=True,paired_rna_denominator=int(d['rna_depth'][mask].sum()),paired_nuclear_fragment_denominator=int(fd[mask].sum())))
                    if not mask.any():holds.append(dict(component=lib+'/'+subset,reason='empty paired population'))
                    for j,(target,gid) in enumerate(TARGETS.items()):
                        rr=aggregate(d['rna_counts'][:,j],d['rna_depth'],mask) if d['symbol_status'][target]=='qualified' else aggregate(d['rna_counts'][:,j],d['rna_depth'],np.zeros(len(mask),bool))
                        rna_rows.append(dict(count_definition=definition,library=lib,subset=subset,target=target,stable_id=gid,rna_reuse='same paired RNA across count definitions and region families',**rr));old=old_summaries.get((lib,subset,gid));check='not_identical_selection'
                        if same and old is not None and rr['n']:
                            require(rr['n']==int(old['n_barcodes']) and rr['denominator']==int(old['all_source_rna_denominator']) and rr['count']==int(old['gene_count']),'Prior RNA sum/count mismatch')
                            require(math.isclose(rr['pooled_log'],float(old['pooled_log2_cpm1']),rel_tol=1e-10,abs_tol=1e-10) and math.isclose(rr['equal_log'],float(old['equal_log2_cpm1']),rel_tol=1e-10,abs_tol=1e-10),'Prior RNA transformed summary mismatch');check='matched_prior_same_selection'
                        reuse.append(dict(count_definition=definition,library=lib,subset=subset,target=target,unchanged_selection=bool(same),check=check,prior_pooled_log2_cpm1=old['pooled_log2_cpm1'] if old else '',current_pooled_log2_cpm1=rr['pooled_log'],prior_equal_log2_cpm1=old['equal_log2_cpm1'] if old else '',current_equal_log2_cpm1=rr['equal_log']))
                        for k,family in enumerate(FAMILIES):
                            fr=aggregate(fc[:,j,k],fd,mask) if regions[target]['status']=='qualified' else aggregate(fc[:,j,k],fd,np.zeros(len(mask),bool))
                            frag_rows.append(dict(count_definition=definition,library=lib,subset=subset,target=target,stable_id=gid,region_family=family,**fr));summaries[(definition,lib,subset,target,family)]=(rr,fr)
    for filename,rows in [('paired_populations.csv',populations),('library_rna_summaries.csv',rna_rows),('library_fragment_summaries.csv',frag_rows),('rna_reuse_checks.csv',reuse)]:write_rows(out,filename,rows)
    pairs=[]
    for definition in DEFINITIONS:
        for label in ['LGR5','KRT20']:
            post='GSE329778_'+label;control='GSE329778_CTRL'
            for subset in ['all','rna_qc']:
                for weight in ['pooled','equal']:
                    for family in FAMILIES:
                        for target,gid in TARGETS.items():
                            key=(definition,post,subset,target,family);other=(definition,control,subset,target,family);row=dict(count_definition=definition,contrast=label+'_minus_CTRL',post_library=post,control_library=control,subset=subset,weighting=weight,region_family=family,target=target,stable_id=gid,status='held',rna_reuse='identical across count definitions and region families')
                            if key in summaries and other in summaries:
                                rp,fp=summaries[key];rc,fc=summaries[other];field=weight+'_log'
                                row.update(rna_post_log2_cpm1=rp[field],rna_control_log2_cpm1=rc[field],fragment_post_log2_cpm1=fp[field],fragment_control_log2_cpm1=fc[field],rna_difference=rp[field]-rc[field] if rp[field] is not None and rc[field] is not None else None,fragment_difference=fp[field]-fc[field] if fp[field] is not None and fc[field] is not None else None)
                                if row['rna_difference'] is not None and row['fragment_difference'] is not None:row['status']='defined'
                            pairs.append(row)
    fields=['count_definition','contrast','post_library','control_library','subset','weighting','region_family','target','stable_id','status','rna_reuse','rna_post_log2_cpm1','rna_control_log2_cpm1','fragment_post_log2_cpm1','fragment_control_log2_cpm1','rna_difference','fragment_difference']
    write_rows(out,'paired_contrasts.csv',pairs,fields)
    lookup={(r['count_definition'],r['contrast'],r['subset'],r['weighting'],r['region_family'],r['target']):r for r in pairs};deltas=[]
    for r in pairs:
        if r['count_definition']!='strand_records':continue
        s=lookup[('coordinate_groups',r['contrast'],r['subset'],r['weighting'],r['region_family'],r['target'])]
        delta={k:r[k] for k in ['contrast','subset','weighting','region_family','target']};delta['status']='defined' if r['status']==s['status']=='defined' else 'held'
        for field in ['rna_difference','fragment_difference','fragment_post_log2_cpm1','fragment_control_log2_cpm1']:
            delta[field+'_groups_minus_records']=s[field]-r[field] if r.get(field) is not None and s.get(field) is not None else None
        if delta['status']=='defined':require(delta['rna_difference_groups_minus_records']==0,'RNA changed between count definitions')
        deltas.append(delta)
    write_rows(out,'count_definition_deltas.csv',deltas)
    receipt=json.loads((out/'receipt.json').read_text());write_rows(out,'source_hashes.csv',[{k:v[k] for k in ['path','sha256']} for v in receipt['inputs']],['path','sha256'])
    from plot_accessibility_v2 import figures
    figures(out,pairs,list(TARGETS))
    summary=dict(analysis='Arz1.accessibility_description_v2',n_fragment_sources=len(validations),n_valid_fragment_sources=sum(v['status']=='qualified' for v in validations),n_qualified_loci=sum(r['status']=='qualified' for r in regions.values()),count_definitions=DEFINITIONS,n_paired_contrast_rows=len(pairs),n_defined_paired_contrasts=sum(r['status']=='defined' for r in pairs),n_count_definition_deltas=len(deltas),holds=holds,all_valid_sources_reached_eof_before_endpoints=True,biological_independence='unknown',scientific_acceptance='not_assessed',interpretation='GRCm39 finite-library source-record/group overlap; neither definition certifies physical molecules; not ARC cut-site matrix counts, exact author replay, state attribution or causal memory')
    rna.write_json(out/'summary.json',summary);print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
