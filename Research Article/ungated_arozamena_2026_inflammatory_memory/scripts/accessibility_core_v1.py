"""Source-qualified GRCm39 regions and bounded full-fragment streaming."""
from collections import Counter,defaultdict
import gzip,math,re
import numpy as np

TARGETS={'Cd74':'ENSMUSG00000024610','Tiam1':'ENSMUSG00000002489','Cd83':'ENSMUSG00000015396','Ciita':'ENSMUSG00000022504'}
FAMILIES=['tss_2kb_union','gene_body']
NUCLEAR={f'chr{i}' for i in range(1,20)}|{'chrX','chrY'}

def require(ok,message):
    if not ok:raise ValueError(message)

def attrs(text):
    values=defaultdict(list)
    for key,value in re.findall(r'(\w+) "([^"]*)"',text):values[key].append(value)
    return dict(values)

def stable(value):return re.sub(r'\.\d+$','',value)

def merge_intervals(intervals):
    merged=[]
    for a,b in sorted(intervals):
        require(0<=a<b,'Invalid region')
        if merged and a<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],b)
        else:merged.append([int(a),int(b)])
    return merged

def tss0(start,end,strand):
    require(start>=1 and end>=start and strand in ['+','-'],'Invalid GTF coordinates/strand')
    return start-1 if strand=='+' else end-1

def overlap_once(start,end,intervals):return any(start<b and end>a for a,b in intervals)

def read_regions(path,source_features):
    genes=defaultdict(list);transcripts=defaultdict(list);headers=[];all_ids=set(TARGETS.values())
    with gzip.open(path,'rt',encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):headers.append(line.rstrip());continue
            parts=line.rstrip('\r\n').split('\t');require(len(parts)==9,'Malformed GTF record')
            if parts[2] not in ['gene','transcript']:continue
            a=attrs(parts[8]);gid=stable(a.get('gene_id',[''])[0])
            if gid not in all_ids:continue
            record=dict(chrom=parts[0],start=int(parts[3]),end=int(parts[4]),strand=parts[6],attributes=a)
            (genes if parts[2]=='gene' else transcripts)[gid].append(record)
    require(any('GRCm39' in s for s in headers) and any('M33' in s for s in headers),'GTF assembly/release header mismatch')
    result={}
    for target,gid in TARGETS.items():
        row=dict(target=target,stable_id=gid,status='held',source_features=source_features.get(target,[]))
        try:
            require(len(genes[gid])==1,'Unique M33 gene record required');gene=genes[gid][0]
            require(gene['attributes'].get('gene_name')==[target] and gene['strand'] in ['+','-'] and gene['chrom'] in NUCLEAR,'M33 identity/chromosome/strand mismatch')
            tx=transcripts[gid];require(tx,'No M33 transcripts')
            require(all(t['chrom']==gene['chrom'] and t['strand']==gene['strand'] and gene['start']<=t['start']<=t['end']<=gene['end'] and t['attributes'].get('gene_name')==[target] for t in tx),'Inconsistent transcript identity or boundaries')
            basic=[t for t in tx if 'basic' in t['attributes'].get('tag',[])];selected=basic or tx
            positions=[tss0(t['start'],t['end'],t['strand']) for t in selected];span=[min(positions),max(positions)+1]
            src=source_features.get(target,[])
            require(len(src)==3 and all(r['stable_id']==gid and r['symbol']==target and r['chrom']==gene['chrom'] and gene['start']-1<=r['start']<r['end']<=gene['end'] for r in src),'Source RNA feature identity/chromosome/TSS-span incoherence')
            windows=merge_intervals([(max(0,t-2000),t+2000) for t in positions])
            row.update(status='qualified',chrom=gene['chrom'],strand=gene['strand'],gene_start_1based=gene['start'],gene_end_1based=gene['end'],n_transcripts=len(tx),n_basic_transcripts=len(basic),fallback_all_transcripts=not bool(basic),selected_transcript_ids=[t['attributes']['transcript_id'][0] for t in selected],selected_tss_0based=positions,m33_tss_span=span,source_span_exact=all([r['start'],r['end']]==span for r in src),regions={'tss_2kb_union':windows,'gene_body':[[gene['start']-1,gene['end']]]})
        except (ValueError,KeyError) as exc:row['hold_reason']=str(exc)
        result[target]=row
    return result,headers

class FragmentFailure(ValueError):
    def __init__(self,message,details):super().__init__(message);self.details=details

def count_fragments(path,barcodes,regions,expected_headers,progress=None):
    """No summary endpoint here. Return counts only after valid gzip EOF/CRC."""
    lookup={b:i for i,b in enumerate(barcodes)};require(len(lookup)==len(barcodes),'Duplicate RNA barcodes')
    depth=np.zeros(len(barcodes),dtype=np.int64);counts=np.zeros((len(barcodes),len(TARGETS),2),dtype=np.int64)
    candidates=defaultdict(list)
    for j,target in enumerate(TARGETS):
        r=regions[target]
        if r['status']=='qualified':
            for k,family in enumerate(FAMILIES):
                intervals=r['regions'][family];candidates[r['chrom']].append((j,k,intervals,intervals[0][0],intervals[-1][1]))
    diag=dict(status='held',path=str(path),rows=0,canonical_rows=0,canonical_allowlisted_rows=0,canonical_nonallowlisted_rows=0,noncanonical_rows=0,headers={},excluded_contigs={})
    headers=defaultdict(list);excluded=Counter();closed_contigs=set();chrom_prev=None;start_prev=-1;group=set();seen_data=False;physical_line=0
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
                require(chrom and 0<=start<end and read_support>=1 and strand in ['+','-'] and re.fullmatch(r'[ACGT]+-\d+',barcode),'Invalid fragment coordinate/barcode/support/strand')
                if chrom!=chrom_prev:
                    require(chrom not in closed_contigs,'Non-contiguous chromosome blocks')
                    if chrom_prev is not None:closed_contigs.add(chrom_prev)
                    chrom_prev=chrom;start_prev=-1;group=set()
                require(start>=start_prev,'Decreasing fragment start coordinate')
                if start!=start_prev:group=set();start_prev=start
                key=(end,barcode)
                require(key not in group,'Duplicate (chrom,start,end,barcode) fragment key');group.add(key)
                diag['rows']+=1
                if chrom not in NUCLEAR:diag['noncanonical_rows']+=1;excluded[chrom]+=1;continue
                diag['canonical_rows']+=1;i=lookup.get(barcode)
                if i is None:diag['canonical_nonallowlisted_rows']+=1;continue
                diag['canonical_allowlisted_rows']+=1;depth[i]+=1
                for j,k,intervals,lo,hi in candidates.get(chrom,[]):
                    if start<hi and end>lo and overlap_once(start,end,intervals):counts[i,j,k]+=1
                if progress and diag['rows']%5000000==0:progress(diag['rows'])
        require(seen_data,'Empty fragment body');diag.update(status='qualified',gzip_eof_crc='passed',n_rna_barcodes=len(barcodes),n_positive_nuclear_fragment_barcodes=int((depth>0).sum()),n_zero_nuclear_fragment_barcodes=int((depth==0).sum()),headers=dict(headers),excluded_contigs=dict(excluded),duplicate_key_rule='chrom,start,end,barcode; readSupport and strand do not make a repeated key independent',ordering='contiguous contig blocks; nondecreasing starts; exact duplicate detection within equal-start groups')
        require(int(depth.sum())==diag['canonical_allowlisted_rows'],'Denominator accounting disagreement')
        return depth,counts,diag
    except (ValueError,KeyError,OSError,EOFError) as exc:
        diag.update(error=str(exc),physical_line=physical_line,headers=dict(headers),excluded_contigs=dict(excluded),endpoints_released=False)
        raise FragmentFailure(str(exc),diag) from exc

def aggregate(counts,depth,mask):
    valid=np.asarray(mask,bool)&(depth>0);n=int(valid.sum())
    if not n:return dict(n=0,denominator=0,count=None,detected=None,detection_fraction=None,pooled_cpm=None,equal_cpm=None,pooled_log=None,equal_log=None)
    x=counts[valid];d=depth[valid];total=int(x.sum());denom=int(d.sum());pooled=1e6*total/denom;equal=float(np.mean(1e6*x/d));detected=int((x>0).sum())
    return dict(n=n,denominator=denom,count=total,detected=detected,detection_fraction=detected/n,pooled_cpm=pooled,equal_cpm=equal,pooled_log=math.log2(pooled+1),equal_log=math.log2(equal+1))
