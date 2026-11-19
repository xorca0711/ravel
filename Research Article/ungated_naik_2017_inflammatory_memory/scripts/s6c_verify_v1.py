"""Independent stdlib verification of complete D180 ranks, source joins and summaries."""
import argparse
import collections
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path

from s3_rank_verify_v1 import rank_points, quantile, opposite

TOL=1e-10
OLD=['GSM'+str(i) for i in range(2441001,2441009)]
NEW=['GSM'+str(i) for i in range(2652413,2652417)]
ANCHORS=[('Aim2','ENSMUSG00000037860.15','chr1:173350878'),('Casp1','ENSMUSG00000025888.5','chr9:5298516'),
         ('Il1b','ENSMUSG00000027398.13','chr2:129371138'),('Il1r1','ENSMUSG00000026072.12','chr1:40225079'),
         ('Il18','ENSMUSG00000039217.12','chr9:50575272')]
PHASES={'D6':(OLD[:2],OLD[2:4]),'D30':(OLD[4:6],OLD[6:]),'D180':(NEW[2:],NEW[:2])}
QUANTILES=[0,.25,.5,.75,.9,.95,1]


def rows(path):
    opener=gzip.open if path.name.endswith('.gz') else open
    with opener(path,'rt',encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))


def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


class Checks:
    def __init__(self):self.count=0;self.maximum=0.
    def equal(self,a,b,label=''):
        self.count+=1
        if isinstance(b,bool): assert a == str(b) or (isinstance(a,bool) and a is b),(label,a,b)
        elif isinstance(b,(float,int)):
            value=float(a);assert math.isfinite(value) and math.isfinite(b),(label,a,b)
            error=abs(value-b)/max(1,abs(b));self.maximum=max(self.maximum,error)
            assert error <= TOL,(label,a,b,error)
        else:assert a == b,(label,a,b)
    def exact(self,a,b,label=''):
        self.count+=1;assert a == b,(label,a,b)
    def tree(self,a,b,label='summary'):
        if isinstance(b,dict):
            self.exact(set(a),set(b),label+' keys')
            for k,v in b.items():self.tree(a[k],v,label+'.'+k)
        else:self.equal(a,b,label)


def verify_data(output,windows,mappings,old,expected_windows=21760,expected_genes=21775):
    check=Checks();signal=rows(output/'window_signal.tsv.gz');actual=rows(output/'window_effects.tsv.gz')
    diagnostics=rows(output/'library_diagnostics.tsv');summary=json.loads((output/'summary.json').read_text())
    anchors=json.loads((output/'anchor_manifest.json').read_text());cases=rows(output/'fixed_anchors.tsv')
    check.exact(len(windows),2*expected_windows);check.exact(len(mappings),2*expected_genes)
    check.exact(rows(output/'windows.tsv'),windows);check.exact(rows(output/'gene_window_map.tsv.gz'),mappings)
    ids=[w['window_id'] for w in windows];check.exact(len(set(ids)),len(ids))
    check.exact([r['window_id'] for r in actual],ids);check.exact([r['window_id'] for r in old],ids)
    for w,o,a in zip(windows,old,actual):
        for k,v in w.items():check.exact(o[k],v);check.exact(a[k],v)
        chrom,tss=w['anchor_id'].split(':');tss=int(tss);flank=int(w['flank'])
        check.exact(chrom,w['chrom']);check.exact(int(w['start']),tss-flank);check.exact(int(w['end']),tss+flank)
        check.exact(w['clipped'],'False');check.exact(w['window_id'],f'{flank}:{chrom}:{tss-flank}-{tss+flank}')
        for k,v in o.items():
            if k in ['window_id','anchor_id','chrom','clipped'] or v in ['True','False']:check.exact(a[k],v,'frozen S3 '+k)
            else:check.exact(float(a[k]),float(v),'frozen S3 binary value '+k)
    lookup={r['window_id']:r for r in windows}
    for flank in [1000,2000]:
        w=[r for r in windows if int(r['flank'])==flank];m=[r for r in mappings if int(r['flank'])==flank]
        check.exact(len(w),expected_windows);check.exact(len(m),expected_genes)
        check.exact(len({r['gene_id'] for r in m}),expected_genes)
        check.exact({r['window_id'] for r in m},{r['window_id'] for r in w})
        for r in m:
            check.exact(r['gene_type'],'protein_coding');check.exact(r['anchor_id'],lookup[r['window_id']]['anchor_id'])
            check.exact(int(r['tss']),int(lookup[r['window_id']]['start'])+flank)
    signal_map={(r['gsm'],r['window_id']):r for r in signal}
    check.exact(len(signal),len(windows)*4);check.exact(len(signal_map),len(signal))
    check.exact({r['gsm'] for r in signal},set(NEW))
    calculated={};by_flank={};all_diagnostics={}
    for flank in [1000,2000]:
        indices=[i for i,w in enumerate(windows) if int(w['flank'])==flank];n=len(indices)
        ranks={}
        for gsm in OLD+NEW:
            means=[];zeros=[]
            for i in indices:
                source=signal_map[gsm,ids[i]] if gsm in NEW else old[i]
                mean=float(source['mean_signal'] if gsm in NEW else source[gsm+'__mean'])
                zero=int(source['encoded_zero_bases'] if gsm in NEW else source[gsm+'__zero_bases'])
                assert math.isfinite(mean) and 0 <= zero <= 2*flank
                means.append(mean);zeros.append(zero)
                check.exact(float(actual[i][gsm+'__mean']),mean)
                check.exact(int(actual[i][gsm+'__zero_bases']),zero)
                check.equal(actual[i][gsm+'__mean_zero'],mean==0)
                check.equal(actual[i][gsm+'__all_bases_zero'],zero==2*flank)
            ranks[gsm]=rank_points(means)
            for i,p in zip(indices,ranks[gsm]):check.equal(actual[i][gsm+'__percentile'],p,'independent rank')
            if gsm in NEW:
                counts=collections.Counter(means);tied=sum(v for v in counts.values() if v>1)
                all_diagnostics[gsm,flank]=dict(gsm=gsm,flank=flank,windows=n,mean_percentile=math.fsum(ranks[gsm])/n,
                    zero_mean_windows=sum(v==0 for v in means),unique_means=len(counts),tied_windows=tied,
                    tied_window_fraction=tied/n,largest_tie_group=max(counts.values()))
        effects={};spreads={};touches={}
        for phase,(control,history) in PHASES.items():
            deltas=[];widths=[];includes=[]
            for pos,i in enumerate(indices):
                c=[ranks[g][pos] for g in control];h=[ranks[g][pos] for g in history]
                d=math.fsum(h)/2-math.fsum(c)/2;combos=[x-y for x in h for y in c]
                lo,hi=min(combos),max(combos);touch=lo<=TOL and hi>=-TOL
                check.equal(actual[i][phase+'_delta'],d)
                for k,v in zip(['h1_c1','h1_c2','h2_c1','h2_c2'],combos):check.equal(actual[i][phase+'_'+k],v)
                for k,v in [('range_min',lo),('range_max',hi),('range_width',hi-lo),('range_touches_zero',touch),('computational_zero',abs(d)<=TOL)]:
                    check.equal(actual[i][phase+'_'+k],v)
                deltas.append(d);widths.append(hi-lo);includes.append(touch)
            effects[phase]=deltas;spreads[phase]=widths;touches[phase]=includes
        calculated[flank]={windows[i]['anchor_id']:effects['D180'][pos] for pos,i in enumerate(indices)}
        def qs(values):return {str(q):quantile(values,q) for q in QUANTILES}
        d=effects['D180']
        block=dict(windows=n,D180_delta_quantiles=qs(d),D180_absolute_delta_quantiles=qs([abs(v) for v in d]),
            D180_range_width_quantiles=qs(spreads['D180']),D180_fraction_range_touches_zero=sum(touches['D180'])/n,
            D180_fraction_computational_zero=sum(abs(v)<=TOL for v in d)/n,D180_mean_delta_constrained_zero=math.fsum(d)/n,comparisons={})
        assert abs(math.fsum(d)/n)<=TOL
        for phase in ['D30','D6']:
            other=effects[phase];difference=[abs(a)-abs(b) for a,b in zip(d,other)]
            block['comparisons'][phase]=dict(signed_shift_quantiles=qs([a-b for a,b in zip(d,other)]),
                absolute_magnitude_difference_quantiles=qs(difference),fraction_absolute_smaller=sum(v < -TOL for v in difference)/n,
                fraction_absolute_larger=sum(v > TOL for v in difference)/n,
                fraction_absolute_within_computational_rule=sum(abs(v)<=TOL for v in difference)/n,
                fraction_opposite_signs=sum(opposite(a,b) for a,b in zip(d,other))/n,
                fraction_computational_zero_status_change=sum((abs(a)<=TOL)!=(abs(b)<=TOL) for a,b in zip(d,other))/n)
        by_flank[str(flank)]=block
    check.tree(summary['by_flank'],by_flank)
    check.exact(set(calculated[1000]),set(calculated[2000]));keys=list(calculated[1000])
    a=[calculated[1000][k] for k in keys];b=[calculated[2000][k] for k in keys];shift=[y-x for x,y in zip(a,b)]
    check.tree(summary['width_sensitivity'],dict(anchors=len(a),signed_shift_quantiles=qs(shift),absolute_shift_quantiles=qs([abs(x) for x in shift]),
        fraction_sign_flip=sum(opposite(x,y) for x,y in zip(a,b))/len(a),
        fraction_computational_zero_status_change=sum((abs(x)<=TOL)!=(abs(y)<=TOL) for x,y in zip(a,b))/len(a)))
    for key,value in dict(units='within-library rank percentile points',population_inference=False,
        original_memory_domain_classification=False,global_mean_rank_is_constrained=True,old_tracks_reextracted=False,
        matched_animals=False,comparator_priority=['D30','D6']).items():check.equal(summary[key],value)
    check.exact(len(diagnostics),8)
    for row in diagnostics:check.tree(row,all_diagnostics[row['gsm'],int(row['flank'])])
    expected_anchors=[]
    for slot,(name,gene,anchor) in enumerate(ANCHORS,1):
        for flank in [1000,2000]:
            match=[r for r in mappings if r['gene_id']==gene and int(r['flank'])==flank]
            check.exact(len(match),1);check.exact(match[0]['gene_name'],name);check.exact(match[0]['anchor_id'],anchor)
            expected_anchors.append(dict(slot=slot,gene_name=name,gene_id=gene,anchor_id=anchor,flank=flank,
                window_id=match[0]['window_id'],selection='fixed published anchor; exposed'))
    check.exact(anchors,expected_anchors);check.exact(len(cases),10)
    effect_map={r['window_id']:r for r in actual}
    for case,anchor in zip(cases,expected_anchors):
        for k,v in anchor.items():check.equal(case[k],v)
        for k,v in effect_map[anchor['window_id']].items():check.exact(case[k],v,'complete fixed anchor '+k)
    expected_selection=[]
    for flank in [1000,2000]:
        w=[r for r in windows if int(r['flank'])==flank];spaced={int(i*(len(w)-1)//31) for i in range(32)}
        fixed={r['window_id'] for r in expected_anchors if r['flank']==flank}
        for i,row in enumerate(w):
            why=(['annotation_order_spaced'] if i in spaced else [])+(['fixed_anchor'] if row['window_id'] in fixed else [])
            if why:expected_selection.append(dict(window_id=row['window_id'],flank=str(flank),selection_reason='|'.join(why)))
    check.exact(rows(output/'verification_windows.tsv'),expected_selection)
    return check


def verify(contract_path,output):
    root=Path(__file__).resolve().parents[3];contract=json.loads(contract_path.read_text(encoding='utf-8-sig'))
    inputs={Path(x['path']).name:root/x['path'] for x in contract['inputs']}
    windows,mappings,old=[rows(inputs[n]) for n in ['windows.tsv','gene_window_map.tsv.gz','window_effects.tsv.gz']]
    check=verify_data(output,windows,mappings,old)
    receipt=json.loads(inputs['receipt.json'].read_text());hashes={Path(r['path']).name:r['sha256'] for r in receipt['outputs']}
    check.exact(receipt['analysis_id'],'Nk17-P01.s3_tss_rank_v1');check.exact(receipt['status'],'executed')
    for name in ['windows.tsv','gene_window_map.tsv.gz','window_effects.tsv.gz']:check.exact(sha(inputs[name]),hashes[name])
    for name in ['windows.tsv','gene_window_map.tsv.gz']:check.exact(sha(inputs[name]),sha(output/name))
    crosswalk={r['gsm']:r for r in rows(inputs['library_crosswalk.tsv'])}
    acquired=json.loads(inputs['acquisition_manifest_v1.json'].read_text())['files']
    source=json.loads((output/'source_manifest.json').read_text());check.exact([r['gsm'] for r in source['files']],NEW)
    expected_hashes={r['path']:r['sha256'] for r in contract['inputs']}
    for i,(s,original) in enumerate(zip(source['files'],acquired)):
        gsm=NEW[i];check.exact(s['gsm'],gsm)
        for k,v in original.items():check.exact(s[k],v)
        check.exact(s['source_identity'],crosswalk[gsm]);meta=crosswalk[gsm]
        history='prior_inflammation' if i<2 else 'control';group='PI' if i<2 else 'Ctrl'
        for key,value in dict(assay='ATAC-seq',day_label='180',history_label=history,wound_hour_label='',label_conflicts='',
            runs='SRR'+str(5657347+i),biosamples=['SAMN07203513','SAMN07203512','SAMN07203511','SAMN07203514'][i],
            instrument_models='Illumina HiSeq 2500',library_layouts='PAIRED',organism='Mus musculus',source_compartment='Skin',
            replicate_label=str(i%2+1),wound_status_label='no wound stated in selected metadata').items():check.exact(meta[key],value)
        name=f'{gsm}_{group}_D180_mm10_ATAC_Rep_{i%2+1}_.bw';check.exact(s['path'],'raw_data/naik2017_s6_d180_sources_v1/'+name)
        check.exact(s['url'],f'https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2652nnn/{gsm}/suppl/{name}')
        check.exact(s['sha256'],expected_hashes[s['path']]);check.exact(s['bytes'],s['expected_bytes'])
        check.exact((root/s['path']).stat().st_size,s['bytes']);check.exact(s['group'],group)
    sizes={s.split()[0]:int(s.split()[1]) for s in inputs['mm10.chrom.sizes'].read_text().splitlines()}
    headers=json.loads((output/'header_metadata.json').read_text());q=json.loads((output/'qualification.json').read_text())
    check.exact(headers['research_window_values_read'],False);check.exact([t['gsm'] for t in headers['tracks']],NEW)
    check.exact(q['status'],'qualified_headers');check.exact(q['all_four_headers_qualified'],True);check.exact(q['failures'],[])
    check.exact(q['full_window_signal_qualified'],False);check.exact(q['signal_units'],'unresolved')
    check.exact(q['between_track_raw_signal_comparison'],False);check.exact(q['population_inference'],False)
    required=sorted({w['chrom'] for w in windows});check.exact(q['required_chromosomes'],required)
    old_header=json.loads(inputs['header_metadata.json'].read_text())['tracks'][0]['chromosomes']
    check.exact(len(q['tracks']),4)
    for t,decision in zip(headers['tracks'],q['tracks']):
        check.exact(t['is_bigwig'],True);check.exact(decision['gsm'],t['gsm']);chroms=t['chromosomes']
        need={c:dict(track=chroms.get(c),mm10=sizes[c],matches=chroms.get(c)==sizes[c]) for c in required}
        check.exact(decision['required_chromosomes'],need);check.exact(all(x['matches'] for x in need.values()),True)
        unused={c:dict(track=chroms[c],mm10=sizes.get(c),matches=chroms[c]==sizes.get(c)) for c in sorted(set(chroms)-set(required))}
        check.exact(decision['unused_track_chromosomes'],unused);check.exact(decision['qualified_for_window_extraction'],True)
        check.exact(decision['mm10_chromosomes_not_in_track'],sorted(set(sizes)-set(chroms)))
        check.exact(decision['differences_from_S3_dictionary'],{c:dict(D180=chroms.get(c),S3=old_header.get(c))
            for c in sorted(set(chroms)|set(old_header)) if chroms.get(c)!=old_header.get(c)})
    progress=json.loads((output/'extraction_progress.json').read_text());check.exact(progress['status'],'completed')
    check.exact(progress['rows_written'],len(windows)*4);check.exact(progress['completed_libraries'],NEW)
    assert progress['peak_rss_mib']<=2048
    chosen={r['window_id'] for r in rows(output/'verification_windows.tsv')};readbacks=rows(output/'mean_readback.tsv')
    expected_pairs={(g,w) for g in NEW for w in chosen};check.exact({(r['gsm'],r['window_id']) for r in readbacks},expected_pairs)
    check.exact(len(readbacks),len(expected_pairs));signals={(r['gsm'],r['window_id']):r for r in rows(output/'window_signal.tsv.gz')}
    maximum=0.
    for r in readbacks:
        s=signals[r['gsm'],r['window_id']];mean=float(s['mean_signal']);value=float(r['interval_weighted_mean'])
        check.exact(float(r['base_array_mean']),mean);check.exact(int(r['encoded_zero_bases']),int(s['encoded_zero_bases']))
        error=abs(value-mean)/max(1,abs(mean));check.equal(r['scaled_error'],error);check.equal(value,mean)
        assert int(r['intervals'])>0;maximum=max(maximum,error)
    back=json.loads((output/'readback_progress.json').read_text());check.exact(back['status'],'completed')
    check.exact(back['checks'],len(expected_pairs));check.equal(back['maximum_scaled_error'],maximum);assert back['peak_rss_mib']<=2048
    result=dict(status='passed',checks=check.count,maximum_scaled_error=check.maximum,interval_readback_checks=len(readbacks),
        interval_readback_maximum_scaled_error=maximum,arithmetic='independent stdlib grouping/sorting/math.fsum/linear quantiles',
        exact_S3_outputs_preserved=True,independent_biological_replication=False,same_binary_decoder_for_readback=True)
    (output/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--contract',type=Path,required=True);p.add_argument('--run-dir',type=Path,required=True)
    a=p.parse_args();verify(a.contract,a.run_dir)
