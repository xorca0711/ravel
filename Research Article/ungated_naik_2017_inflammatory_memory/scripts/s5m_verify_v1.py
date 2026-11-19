"""Independent standard-library reconstruction of joins and finite associations."""
import argparse
from collections import Counter
import csv
import gzip
import itertools
import json
import math
from pathlib import Path

ANCHORS = [('Aim2', 'ENSMUSG00000037860.15'), ('Casp1', 'ENSMUSG00000025888.5'), ('Il1b', 'ENSMUSG00000027398.13'),
           ('Il1r1', 'ENSMUSG00000026072.12'), ('Il18', 'ENSMUSG00000039217.12')]
GSMS = ['GSM' + str(i) for i in range(2441001, 2441009)]
MEASURES = [
    ('S2_D6', 'D6', 's2', 'D6_log2_effect_', 'S2 D6'), ('S2_D30', 'D30', 's2', 'D30_log2_effect_', 'S2 D30 (same B0 libraries)'),
    ('S4_B0_primary', 'D30', 's4', 'B0_log2_effect_', 'S4 B0 primary'),
    ('S4_W6_post', 'D30', 's4', 'W6_log2_effect_', 'S4 W6 unadjusted'), ('S4_W12_post', 'D30', 's4', 'W12_log2_effect_', 'S4 W12 unadjusted'),
    ('S4_W6_primary', 'D30', 's4', 'W6_adjusted_', 'S4 W6 adjusted primary'), ('S4_W12_primary', 'D30', 's4', 'W12_adjusted_', 'S4 W12 adjusted primary'),
    ('S4B_B0_c2_h2', 'D30', 's4b', 'B0_c2_h2_', 'S4B B0 C2/H2 reference'),
    ('S4B_W6_c2_h2', 'D30', 's4b', 'W6_c2_h2_', 'S4B W6 adjusted C2/H2'), ('S4B_W12_c2_h2', 'D30', 's4b', 'W12_c2_h2_', 'S4B W12 adjusted C2/H2'),
    ('S4B_B0_c1_h1', 'D30', 's4b', 'B0_c1_h1_', 'S4B B0 C1/H1 reference'),
    ('S4B_W6_c1_h1', 'D30', 's4b', 'W6_c1_h1_', 'S4B W6 adjusted C1/H1'), ('S4B_W12_c1_h1', 'D30', 's4b', 'W12_c1_h1_', 'S4B W12 adjusted C1/H1')]


def rows(path):
    opener = gzip.open if path.name.endswith('.gz') else open
    with opener(path, 'rt', encoding='utf-8', newline='') as f: yield from csv.DictReader(f, delimiter='\t')


def indexed(path, key='gene_id'):
    result = {}
    for row in rows(path):
        assert row[key] not in result, 'duplicate source key'
        result[row[key]] = row
    return result


def ranks(values):
    result = [None] * len(values); count = 0
    for unused, group in itertools.groupby(sorted(enumerate(values), key=lambda x: x[1]), key=lambda x: x[1]):
        members = list(group); rank = count + (len(members)+1)/2
        for position, value in members: result[position] = rank
        count += len(members)
    return result


def statistics(x, y, weights):
    n = len(x)
    if n < 2: return dict(coefficient=None, covariance=None, variance_x=None, variance_y=None, reason='fewer_than_two_features')
    sw = math.fsum(weights); mx = math.fsum(w*a for w,a in zip(weights,x))/sw; my = math.fsum(w*b for w,b in zip(weights,y))/sw
    vx = math.fsum(w*(a-mx)**2 for w,a in zip(weights,x))/sw; vy = math.fsum(w*(b-my)**2 for w,b in zip(weights,y))/sw
    covariance = math.fsum(w*(a-mx)*(b-my) for w,a,b in zip(weights,x,y))/sw
    cx, cy = len(set(x)) == 1, len(set(y)) == 1
    if cx: vx, covariance = 0.0, 0.0
    if cy: vy, covariance = 0.0, 0.0
    reason = 'constant_x_and_y' if cx and cy else ('constant_x' if cx else ('constant_y' if cy else 'defined'))
    return dict(coefficient=None if reason != 'defined' else covariance/math.sqrt(vx*vy), covariance=covariance,
                variance_x=vx, variance_y=vy, reason=reason)


def verify(contract_path, output):
    root = Path(__file__).resolve().parents[3]; contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    inputs = {Path(x['path']).name: root/x['path'] for x in contract['inputs']}; checks, maximum = 0, 0.0
    def equal(actual, expected, label):
        nonlocal checks, maximum
        checks += 1
        if expected is None: assert actual is None or actual == 'NA', (label, actual, expected)
        elif isinstance(expected, bool): assert actual == str(expected) or (isinstance(actual, bool) and actual is expected), (label, actual, expected)
        elif isinstance(expected, (float, int)):
            value = float(actual); assert math.isfinite(value) and math.isfinite(expected), (label, actual, expected)
            error = abs(value-expected)/max(1,abs(expected)); maximum = max(maximum,error)
            assert error <= 1e-10, (label, actual, expected, error)
        else: assert actual == expected, (label, actual, expected)
    sources = {prefix: indexed(inputs[name]) for prefix,name in [('s2','gene_effects.tsv'),('s4','gene_effects.tsv.gz'),('s4b','reference_effects.tsv.gz')]}
    columns = {prefix: list(next(iter(source.values()))) for prefix,source in sources.items()}
    maps = {}
    for row in rows(inputs['gene_window_map.tsv.gz']):
        key = (row['gene_id'],row['flank']); assert key not in maps; maps[key] = row
    windows = indexed(inputs['window_effects.tsv.gz'], 'window_id'); window_columns = list(next(iter(windows.values())))
    annotation = {}
    with gzip.open(inputs['gencode.vM9.annotation.gtf.gz'],'rt') as handle:
        for line in handle:
            if line.startswith('#'): continue
            f = line.rstrip().split('\t')
            if len(f) != 9 or f[2] != 'gene': continue
            attr = {}
            for entry in f[8].split(';'):
                if entry.strip():
                    key,value = entry.strip().split(' ',1); attr[key] = value.strip('"')
            assert attr['gene_id'] not in annotation
            annotation[attr['gene_id']] = dict(gene_name=attr['gene_name'],gene_type=attr['gene_type'],chrom=f[0])
    genes = sorted(set().union(*(set(v) for v in sources.values()), {g for g,f in maps})); metadata = {}
    def finite(value): return value not in ['', 'NA'] and math.isfinite(float(value))
    def warn(gene, kind):
        selected = []
        for prefix,source in sources.items():
            for field,value in source.get(gene,{}).items():
                match = 'zero' in field if kind == 'zero' else ('low' in field or 'regularization_sensitive' in field)
                if match and value not in ['', 'NA', 'False']: selected.append(value == 'True' or float(value) != 0)
        return any(selected)
    for gene in genes:
        a = annotation.get(gene); assayed = (gene,'1000') in maps; assert assayed == ((gene,'2000') in maps)
        present = {prefix: gene in source for prefix,source in sources.items()}; complete = all(present.values())
        required = complete and all(finite(sources[prefix][gene][field+norm]) for name,phase,prefix,field,label in MEASURES for norm in ['mor','total'])
        qualified = False
        if complete:
            s2,s4,s4b = [sources[k][gene] for k in ['s2','s4','s4b']]
            assert s2['eligible_both'] == str(s2['D6_qualified_cpm']=='True' and s2['D30_qualified_cpm']=='True')
            assert s4['all_three_qualified'] == str(all(s4[t+'_qualified_cpm']=='True' for t in ['B0','W6','W12']))
            assert s4b['all_three_qualified'] == s4['all_three_qualified']
            qualified = s2['eligible_both']=='True' and s4['all_three_qualified']=='True'
        if assayed:
            assert a and a['gene_type']=='protein_coding' and maps[(gene,'1000')]['gene_name']==a['gene_name']
            assert maps[(gene,'1000')]['anchor_id']==maps[(gene,'2000')]['anchor_id']
            status,anchor = 'assayed_TSS_proxy',maps[(gene,'1000')]['anchor_id']
        else: status,anchor = ('unassayed_annotation' if not a else ('unassayed_non_protein_coding' if a['gene_type']!='protein_coding' else 'unassayed_chromosome')),'NA'
        reasons=([] if assayed else [status])+['missing_'+p for p,ok in present.items() if not ok]
        if complete and not required: reasons.append('nonfinite_required_rna')
        primary_reasons=reasons+(['frozen_expression_not_qualified'] if complete and not qualified else [])
        item = dict(gene_id=gene,annotation_present=a is not None,gene_name=a['gene_name'] if a else 'NA',gene_type=a['gene_type'] if a else 'NA',chrom=a['chrom'] if a else 'NA',
                    atac_assayed=assayed,atac_status=status,anchor_id=anchor,finite_required_rna=required,frozen_expression_qualified=qualified,
                    universe_primary=assayed and required and qualified,universe_all_mapped=assayed and required,rna_any_zero_flag=warn(gene,'zero'),rna_any_low_or_regularization_flag=warn(gene,'low'),
                    all_mapped_eligibility_reason='|'.join(reasons) if reasons else 'eligible',primary_eligibility_reason='|'.join(primary_reasons) if primary_reasons else 'eligible')
        item.update({prefix+'_present':value for prefix,value in present.items()})
        for flank in ['1000','2000']: item['window_id_'+flank] = maps[(gene,flank)]['window_id'] if assayed else 'NA'
        metadata[gene] = item
    universes = {u:[g for g in genes if metadata[g]['universe_'+u]] for u in ['primary','all_mapped']}
    counts = {u:Counter(metadata[g]['anchor_id'] for g in ids) for u,ids in universes.items()}
    for gene,item in metadata.items():
        for u in universes:
            number = counts[u][item['anchor_id']] if item['universe_'+u] else None
            item['anchor_multiplicity_'+u] = number; item['weight_'+u] = 1/number if number else None
    actual_ids=[]; anchor_join={}
    for row in rows(output/'gene_join.tsv.gz'):
        gene=row['gene_id'];actual_ids.append(gene);expected=metadata[gene]
        for field,value in expected.items(): equal(row[field],value,'join:'+field)
        for prefix,source in sources.items():
            for field in columns[prefix]:
                if field!='gene_id': equal(row[prefix+'__'+field],source.get(gene,{}).get(field,'NA'),'source field:'+prefix+':'+field)
        if gene in {g for n,g in ANCHORS}: anchor_join[gene]=row
    equal(actual_ids,genes,'complete ordered exact-ID outer join')
    def atac_expected(gene,flank):
        m=metadata[gene]; result=dict(gene_id=gene,flank=flank,atac_status=m['atac_status']); assayed=m['atac_assayed']
        source=windows[m['window_id_'+flank]] if assayed else {}
        for field in window_columns: result['atac__'+field]=source.get(field,'NA')
        for gsm in GSMS: result[gsm+'__zero_mean']=(float(source[gsm+'__mean'])==0) if assayed else None
        for phase,group in [('D6',GSMS[:4]),('D30',GSMS[4:])]:
            result[phase+'_any_zero_means']=any(result[g+'__zero_mean'] for g in group) if assayed else None
            result[phase+'_all_zero_means']=all(result[g+'__zero_mean'] for g in group) if assayed else None
        return result
    actual_features=[]; anchor_features={}
    for row in rows(output/'gene_atac.tsv.gz'):
        gene,flank=row['gene_id'],row['flank']; actual_features.append((gene,flank))
        for field,value in atac_expected(gene,flank).items(): equal(row[field],value,'ATAC join:'+field)
        if gene in anchor_join: anchor_features[(gene,flank)]=row
    equal(actual_features,[(g,f) for g in genes for f in ['1000','2000']],'complete gene-by-width table')
    def xvalues(ids,flank,phase): return [float(windows[metadata[g]['window_id_'+flank]][phase+'_delta']) for g in ids]
    def yvalues(ids,prefix,field): return [float(sources[prefix][g][field]) for g in ids]
    associations=list(rows(output/'association_results.tsv')); expected_keys=set(); observed_keys=set()
    for row in associations:
        u,flank,norm,name,stat=[row[k] for k in ['universe','flank','normalization','measurement','statistic']]
        key=(u,flank,norm,name,stat);assert key not in observed_keys;observed_keys.add(key)
        measure=next(m for m in MEASURES if m[0]==name); unused,phase,prefix,field,label=measure;ids=universes[u]
        x,y=xvalues(ids,flank,phase),yvalues(ids,prefix,field+norm)
        if stat=='spearman': x,y=ranks(x),ranks(y)
        weights=[metadata[g]['weight_'+u] for g in ids] if stat=='inverse_anchor_pearson' else [1]*len(ids)
        equal(row['label'],label,'association label');equal(row['atac_time'],phase,'association ATAC time');equal(row['rna_field'],prefix+'__'+field+norm,'normalization/source context')
        equal(row['genes'],len(ids),'association genes');equal(row['unique_anchors'],len(counts[u]),'association anchors');equal(row['weight_sum'],math.fsum(weights),'association weight sum')
        for field,value in statistics(x,y,weights).items(): equal(row[field],value,'association:'+field)
    expected_keys={(u,f,n,m[0],s) for u in universes for f in ['1000','2000'] for n in ['mor','total'] for m in MEASURES for s in ['pearson','spearman','inverse_anchor_pearson']}
    equal(observed_keys,expected_keys,'all 312 declared associations')
    identities=list(rows(output/'covariance_identity.tsv'));observed_keys=set();max_identity=0.0
    for row in identities:
        u,f,n,ref,t,weighting=[row[k] for k in ['universe','flank','normalization','reference','wound_time','weighting']]
        key=(u,f,n,ref,t,weighting);assert key not in observed_keys;observed_keys.add(key);ids=universes[u]
        x=xvalues(ids,f,'D30');w=[metadata[g]['weight_'+u] for g in ids] if weighting=='inverse_anchor' else [1]*len(ids)
        baseline=yvalues(ids,'s4' if ref=='primary' else 's4b',('B0_log2_effect_' if ref=='primary' else 'B0_'+ref+'_')+n)
        post=yvalues(ids,'s4',t+'_log2_effect_'+n)
        adjusted=yvalues(ids,'s4' if ref=='primary' else 's4b',(t+'_adjusted_' if ref=='primary' else t+'_'+ref+'_')+n)
        for a,p,b in zip(adjusted,post,baseline): equal(a,p-b,'frozen RNA baseline identity')
        cb,cp,ca=[statistics(x,y,w)['covariance'] for y in [baseline,post,adjusted]]
        difference=cp-cb if cp is not None else None;error=abs(ca-difference)/max(1,abs(ca),abs(difference)) if ca is not None else None
        expected=dict(genes=len(ids),unique_anchors=len(counts[u]),covariance_baseline=cb,covariance_post=cp,covariance_adjusted=ca,
                      post_minus_baseline_covariance=difference,scaled_identity_error=error,reason='defined' if error is not None else 'fewer_than_two_features')
        for field,value in expected.items(): equal(row[field],value,'covariance identity:'+field)
        if error is not None: assert error<=1e-10;max_identity=max(max_identity,error)
    equal(observed_keys,{(u,f,n,r,t,w) for u in universes for f in ['1000','2000'] for n in ['mor','total'] for r in ['primary','c2_h2','c1_h1'] for t in ['W6','W12'] for w in ['ordinary','inverse_anchor']},'all 96 covariance identities')
    summary=json.loads((output/'universe_summary.json').read_text());equal(summary['analysis_id'],contract['analysis_id'],'analysis ID')
    equal(summary['gene_records'],len(genes),'all gene records');equal(summary['atac_status_counts'],dict(Counter(v['atac_status'] for v in metadata.values())),'assay statuses')
    equal(summary['finite_feature_description_only'],True,'description only');equal(summary['independent_biological_replication'],False,'shared source')
    for u,ids in universes.items():
        b=summary['universes'][u]
        expected=dict(genes=len(ids),unique_anchors=len(counts[u]),additional_gene_mappings=len(ids)-len(counts[u]),inverse_multiplicity_weight_sum=math.fsum(metadata[g]['weight_'+u] for g in ids),
                      rna_any_zero_genes=sum(metadata[g]['rna_any_zero_flag'] for g in ids),rna_any_low_or_regularization_genes=sum(metadata[g]['rna_any_low_or_regularization_flag'] for g in ids))
        for field,value in expected.items(): equal(b[field],value,'universe:'+field)
        for f in ['1000','2000']:
            for phase,group in [('D6',GSMS[:4]),('D30',GSMS[4:])]:
                zero_arrays=[[float(windows[metadata[g]['window_id_'+f]][gsm+'__mean'])==0 for gsm in group] for g in ids]
                equal(b['atac_zero_flags'][f+'_'+phase]['any_zero_mean_genes'],sum(any(v) for v in zero_arrays),'ATAC zero flags')
                equal(b['atac_zero_flags'][f+'_'+phase]['all_zero_mean_genes'],sum(all(v) for v in zero_arrays),'ATAC zero flags')
    manifest=json.loads((output/'anchor_manifest.json').read_text());equal(len(manifest),5,'fixed anchors')
    for slot,((name,gene),item) in enumerate(zip(ANCHORS,manifest),1):
        equal(annotation[gene]['gene_name'],name,'fixed M9 ID');equal(item['gene_id'],gene,'anchor ID');equal(item['gene_name'],name,'anchor name');equal(item['plot_slot'],slot,'anchor order')
        equal(item['selection'],'published pathway anchor; exposed','exposure');equal(item['source_record_present'],gene in metadata,'anchor presence')
        if gene in metadata:
            for field in ['atac_status','universe_primary','universe_all_mapped','rna_any_zero_flag','rna_any_low_or_regularization_flag','primary_eligibility_reason','all_mapped_eligibility_reason']: equal(item[field],metadata[gene][field],'anchor flags')
        else:
            equal(item['atac_status'],'unassayed_no_source_record','absent anchor');equal(item['universe_primary'],False,'absent eligibility');equal(item['universe_all_mapped'],False,'absent eligibility')
    anchor_rows=list(rows(output/'anchor_values.tsv'));equal(len(anchor_rows),2*len(anchor_join),'anchor row count');seen=set()
    for row in anchor_rows:
        key=(row['gene_id'],row['flank']);assert key not in seen;seen.add(key)
        expected=dict(anchor_join[key[0]],**anchor_features[key]);expected['plot_slot']=next(i for i,(n,g) in enumerate(ANCHORS,1) if g==key[0])
        for field,value in expected.items(): equal(row[field],value,'anchor copied data')
    result=dict(status='passed',checks=checks,maximum_scaled_error=maximum,maximum_covariance_identity_error=max_identity,
                genes=len(genes),universe_genes={u:len(ids) for u,ids in universes.items()},associations=len(associations),covariance_identities=len(identities),
                scope='independent exact-ID outer joins, all copied RNA/ATAC fields and flags, universes, weights, associations, covariance identity and fixed anchors',
                independent_biological_replication=False)
    (output/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--contract',type=Path,required=True);parser.add_argument('--run-dir',type=Path,required=True)
    args=parser.parse_args();verify(args.contract,args.run_dir)
