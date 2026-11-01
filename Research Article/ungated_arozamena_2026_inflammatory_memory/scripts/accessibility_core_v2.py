"""Two reviewed source-record definitions; unchanged M33 region/RNA helpers."""
from collections import Counter,defaultdict
import gzip,re
import numpy as np
from accessibility_core_v1 import (TARGETS,FAMILIES,NUCLEAR,require,attrs,stable,
    merge_intervals,tss0,overlap_once,read_regions,FragmentFailure,aggregate)

DEFINITIONS=['strand_records','coordinate_groups']

def count_fragments(path,barcodes,regions,expected_headers,progress=None):
    """Both definitions share one validated stream; no release before EOF/CRC."""
    lookup={b:i for i,b in enumerate(barcodes)};require(len(lookup)==len(barcodes),'Duplicate RNA barcodes')
    depth={d:np.zeros(len(barcodes),dtype=np.int64) for d in DEFINITIONS}
    counts={d:np.zeros((len(barcodes),len(TARGETS),2),dtype=np.int64) for d in DEFINITIONS}
    candidates=defaultdict(list)
    for j,target in enumerate(TARGETS):
        r=regions[target]
        if r['status']=='qualified':
            for k,family in enumerate(FAMILIES):
                intervals=r['regions'][family];candidates[r['chrom']].append((j,k,intervals,intervals[0][0],intervals[-1][1]))
    diag=dict(status='held',path=str(path),rows=0,canonical_rows=0,canonical_allowlisted_rows=0,canonical_nonallowlisted_rows=0,noncanonical_rows=0,headers={},excluded_contigs={},opposite_strand_coordinate_groups=0,canonical_opposite_strand_groups=0,canonical_allowlisted_opposite_strand_groups=0,noncanonical_opposite_strand_groups=0)
    headers=defaultdict(list);excluded=Counter();closed_contigs=set();chrom_prev=None;start_prev=-1;group={};seen_data=False;physical_line=0
    collisions=defaultdict(lambda:[0,0,0]);locus_collisions=np.zeros((len(TARGETS),2),np.int64);allowed_locus_collisions=locus_collisions.copy()
    barcode_pattern=re.compile(r'[ACGT]+-\d+')
    try:
        with gzip.open(path,'rt',encoding='utf-8') as f:
            for physical_line,line in enumerate(f,1):
                if line.startswith('#'):
                    require(not seen_data,'Header after fragment data')
                    if '=' in line:
                        key,value=line[1:].strip().split('=',1);headers[key].append(value)
                    continue
                if not seen_data:
                    for key,value in expected_headers.items():require(headers.get(key)==[value],'Fragment header mismatch: '+key)
                    seen_data=True
                fields=line.rstrip('\r\n').split('\t');require(len(fields)==6,'Expected six fragment fields')
                chrom,a,b,barcode,support,strand=fields
                require(a.isdigit() and b.isdigit() and support.isdigit(),'Non-integer fragment coordinates/support')
                start,end,read_support=int(a),int(b),int(support)
                require(chrom and 0<=start<end and read_support>=1 and strand in ['+','-'] and barcode_pattern.fullmatch(barcode),'Invalid fragment coordinate/barcode/support/strand')
                if chrom!=chrom_prev:
                    require(chrom not in closed_contigs,'Non-contiguous chromosome blocks')
                    if chrom_prev is not None:closed_contigs.add(chrom_prev)
                    chrom_prev=chrom;start_prev=-1;group={}
                require(start>=start_prev,'Decreasing fragment start coordinate')
                if start!=start_prev:group={};start_prev=start
                key=(end,barcode);bit=1 if strand=='+' else 2;previous=group.get(key,0)
                require(not previous&bit,'Duplicate (chrom,start,end,barcode,strand) fragment key')
                group[key]=previous|bit;collision=bool(previous);canonical=chrom in NUCLEAR;i=lookup.get(barcode)
                diag['rows']+=1
                if collision:
                    diag['opposite_strand_coordinate_groups']+=1
                    diag['canonical_opposite_strand_groups' if canonical else 'noncanonical_opposite_strand_groups']+=1
                    collisions[barcode][0]+=1;collisions[barcode][1 if canonical else 2]+=1
                    if canonical and i is not None:diag['canonical_allowlisted_opposite_strand_groups']+=1
                if progress and diag['rows']%5000000==0:progress(diag['rows'])
                if not canonical:diag['noncanonical_rows']+=1;excluded[chrom]+=1;continue
                diag['canonical_rows']+=1
                if i is None:diag['canonical_nonallowlisted_rows']+=1
                else:
                    diag['canonical_allowlisted_rows']+=1;depth['strand_records'][i]+=1
                    if not collision:depth['coordinate_groups'][i]+=1
                if i is not None or collision:
                    for j,k,intervals,lo,hi in candidates.get(chrom,[]):
                        if start<hi and end>lo and overlap_once(start,end,intervals):
                            if collision:locus_collisions[j,k]+=1
                            if i is not None:
                                counts['strand_records'][i,j,k]+=1
                                if not collision:counts['coordinate_groups'][i,j,k]+=1
                                else:allowed_locus_collisions[j,k]+=1
        require(seen_data,'Empty fragment body')
        require(np.array_equal(depth['strand_records']>0,depth['coordinate_groups']>0),'Positive fragment populations differ between definitions')
        require(int(depth['strand_records'].sum())==diag['canonical_allowlisted_rows'],'Primary denominator accounting disagreement')
        require(int(depth['coordinate_groups'].sum())==diag['canonical_allowlisted_rows']-diag['canonical_allowlisted_opposite_strand_groups'],'Grouped denominator accounting disagreement')
        require(np.array_equal((counts['strand_records']-counts['coordinate_groups']).sum(axis=0),allowed_locus_collisions),'Locus collision count disagreement')
        diag.update(status='qualified',gzip_eof_crc='passed',n_rna_barcodes=len(barcodes),n_positive_nuclear_fragment_barcodes=int((depth['strand_records']>0).sum()),n_zero_nuclear_fragment_barcodes=int((depth['strand_records']==0).sum()),headers=dict(headers),excluded_contigs=dict(excluded),duplicate_key_rule='Reject repeated chrom,start,end,barcode,strand regardless of readSupport',ordering='contiguous contig blocks; nondecreasing starts; equal-start coordinate/barcode groups',positive_sets_agree_between_definitions=True,collision_affected_barcodes=len(collisions),canonical_collision_affected_barcodes=sum(v[1]>0 for v in collisions.values()),canonical_allowlisted_collision_affected_barcodes=sum(b in lookup and v[1]>0 for b,v in collisions.items()),collision_locus_regions=[dict(target=t,region_family=f,all_barcode_groups=int(locus_collisions[j,k]),allowlisted_groups=int(allowed_locus_collisions[j,k])) for j,t in enumerate(TARGETS) for k,f in enumerate(FAMILIES)],definition_denominators={d:int(depth[d].sum()) for d in DEFINITIONS})
        return depth,counts,diag,{b:dict(opposite_strand_groups=v[0],canonical_groups=v[1],noncanonical_groups=v[2],rna_allowlisted=b in lookup) for b,v in collisions.items()}
    except (ValueError,KeyError,OSError,EOFError) as exc:
        diag.update(error=str(exc),physical_line=physical_line,headers=dict(headers),excluded_contigs=dict(excluded),endpoints_released=False)
        raise FragmentFailure(str(exc),diag) from exc
