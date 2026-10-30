"""Neutral file-format QC in the full N. brasiliensis-history/IAV study context."""
import argparse,csv,gzip,hashlib,json,math,statistics
from pathlib import Path
from verify_baseline_file_qc_v1 import verify

ARTICLE=Path('Research Article/gate2_DY1_damani_yokota_2026')

def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def exon_qc(path):
    ids=[];features=[];zero=set();summaries=[]
    r=dict(file=path.name,rows=0,bad_fields=0,invalid_integer=0,negative_counts=0,feature_rows=0,zero_feature_rows=0,feature_count_sum=0,summary_count_sum=0,unknown_feature_ids=0)
    with gzip.open(path,'rt',newline='') as f:
        for row in csv.reader(f,delimiter='\t'):
            r['rows']+=1
            if len(row)!=2:r['bad_fields']+=1;continue
            ident,value=row;ids.append(ident)
            try:count=int(value)
            except ValueError:r['invalid_integer']+=1;continue
            if count<0:r['negative_counts']+=1
            if ident.startswith('_'):
                summaries.append(dict(file=path.name,category=ident,count=count));r['summary_count_sum']+=count
            else:
                features.append(ident);r['feature_rows']+=1;r['feature_count_sum']+=count
                if not ident.startswith('ENSMUSG') or ':' not in ident:r['unknown_feature_ids']+=1
                if count==0:r['zero_feature_rows']+=1;zero.add(ident)
    r.update(unique_ids=len(set(ids)),duplicate_id_occurrences=len(ids)-len(set(ids)),summary_rows=len(summaries),ordered_id_sha256=hashlib.sha256(('\n'.join(ids)+'\n').encode()).hexdigest(),feature_universe_sha256=hashlib.sha256(('\n'.join(sorted(set(features)))+'\n').encode()).hexdigest())
    return r,summaries,set(features),zero

def exon_universe(records,universes,zeros):
    same=all(u==universes[0] for u in universes)
    valid=all(not any(r[k] for k in ['bad_fields','invalid_integer','negative_counts','duplicate_id_occurrences','unknown_feature_ids']) and r['feature_count_sum']>0 for r in records)
    return dict(files=len(records),same_feature_universe=same,same_ordered_ids=len({r['ordered_id_sha256'] for r in records})==1,union_features=len(set.union(*universes)),intersection_features=len(set.intersection(*universes)),all_zero_feature_ids=len(set.intersection(*zeros)) if same and valid else None,count_format_eligible=bool(same and valid),limit='Exon-hit sums are not unique gene/fragment counts. This is file eligibility, not independent-unit or biological-model qualification.')

def peak_qc(path):
    r=dict(file=path.name,rows=0,bad_fields=0,invalid_coordinates=0,invalid_summit=0,invalid_strand=0,invalid_numeric_fields=0,missing_signal=0,missing_p_field=0,missing_q_field=0)
    intervals=[];widths=[];chroms=set()
    with gzip.open(path,'rt',newline='') as f:
        for row in csv.reader(f,delimiter='\t'):
            r['rows']+=1
            if len(row)!=10:r['bad_fields']+=1;continue
            try:start,end,summit=int(row[1]),int(row[2]),int(row[9])
            except ValueError:r['invalid_coordinates']+=1;continue
            if not row[0] or start<0 or end<=start:r['invalid_coordinates']+=1;continue
            width=end-start;widths.append(width);intervals.append((row[0],start,end));chroms.add(row[0])
            if summit!=-1 and not 0<=summit<width:r['invalid_summit']+=1
            if row[5] not in {'.','+','-'}:r['invalid_strand']+=1
            for idx,key in [(4,None),(6,'missing_signal'),(7,'missing_p_field'),(8,'missing_q_field')]:
                value=row[idx]
                if key and value.strip().lower() in {'','na','nan','-1'}:r[key]+=1;continue
                try:v=float(value)
                except ValueError:r['invalid_numeric_fields']+=1;continue
                if key and v==-1:r[key]+=1;continue
                if not math.isfinite(v) or v<0:r['invalid_numeric_fields']+=1
    r.update(unique_intervals=len(set(intervals)),duplicate_interval_occurrences=len(intervals)-len(set(intervals)),chromosome_labels=len(chroms),width_min=min(widths) if widths else None,width_median=statistics.median(widths) if widths else None,width_max=max(widths) if widths else None)
    return r

def write(out,name,rows):
    with (out/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

def main(out):
    manifest=json.loads((ARTICLE/'config/baseline_file_qc_inputs_v1.json').read_text())
    exon=[];summary=[];universes=[];zeros=[];peaks=[]
    for item in manifest['files']:
        p=Path(item['path'])
        if digest(p)!=item['sha256']:raise ValueError('Input hash mismatch: '+p.name)
        if item['kind']=='exon_counts':
            row,s,u,z=exon_qc(p);exon.append(row);summary.extend(s);universes.append(u);zeros.append(z)
        elif item['kind']=='narrowPeak':peaks.append(peak_qc(p))
        else:raise ValueError('Unknown input kind')
    universe=exon_universe(exon,universes,zeros)
    write(out,'exon_files.tsv',exon);write(out,'exon_summary_categories.tsv',summary);write(out,'peak_files.tsv',peaks)
    (out/'exon_universe.json').write_text(json.dumps(universe,indent=2)+'\n')
    verification=verify(manifest,exon,summary,peaks,universe)
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    bad_peak=any(any(r[k] for k in ['bad_fields','invalid_coordinates','invalid_summit','invalid_strand','invalid_numeric_fields']) for r in peaks)
    result=dict(analysis_id='DY1-P01.baseline_file_qc_v1',context='N. brasiliensis-history / later IAV-challenge study; these files are baseline host measurements, not history-free controls.',exon_files=len(exon),peak_files=len(peaks),exon_count_format_eligible=universe['count_format_eligible'],peak_basic_format_eligible=not bad_peak,peak_check_limit='Only listed field, finite/nonnegative numeric, interval ordering and summit/strand checks. Score integer0..1000 conformance, chromosome-size/build concordance, full BED specification, read depth and FRiP are not checked.',scope='Per-file structural/count-format QC only; no group effects, selected loci, enrichment, infection-response prediction or intervention prioritization.',unresolved=['Animal/pool identity and independence','Unique gene/fragment count semantics','Common-region ATAC read counts and read-level QC','Source/article ATAC pipeline and documented exclusion identity','Cross-assay/functional-cohort linkage'],scientific_acceptance='not_assessed')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
