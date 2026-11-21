"""Prospective empty-record adapter; reuse the four already checked HDF5 libraries."""
from collections import Counter
import argparse,csv,gzip,json,math
from pathlib import Path
import numpy as np
import qualify_v1 as prior

ROOT=prior.ROOT
PACKAGE=prior.PACKAGE


def nonempty(path,counts,key):
    counts[key]=0
    with gzip.open(path,'rt',encoding='utf-8') as stream:
        for line in stream:
            text=line.rstrip('\r\n')
            if not text.strip():counts[key]+=1;continue
            yield text


def inspect_mtx(matrix_path,feature_path,barcode_path):
    blanks={}
    records=[line.split('\t') for line in nonempty(feature_path,blanks,'feature_empty_records')]
    prior.require(all(len(r)>=3 and r[2] for r in records),'Malformed nonempty feature record: explicit type required')
    ids=[r[0] for r in records];names=[r[1] for r in records];types=[r[2] for r in records]
    barcodes=list(nonempty(barcode_path,blanks,'barcode_empty_records'))
    prior.require(all(b.strip()==b and not any(c.isspace() for c in b) for b in barcodes),'Malformed nonempty barcode record')
    info,features=prior.feature_info(ids,names,types,barcodes)
    seen={t:np.zeros(len(barcodes),bool) for t in features};count=0;last_col=last_row=-1;col_order=row_order=True
    lines=iter(nonempty(matrix_path,blanks,'matrix_empty_records'))
    header=next(lines);prior.require(header.lower() in ['%%matrixmarket matrix coordinate integer general','%%matrixmarket matrix coordinate real general'],'Unexpected MatrixMarket schema')
    line=next(lines);comments=0
    while line.startswith('%'):comments+=1;line=next(lines)
    nr,nc,nnz=map(int,line.split());prior.require((nr,nc)==(len(ids),len(barcodes)),'MatrixMarket dimensions disagree after empty-record removal')
    for line in lines:
        parts=line.split();prior.require(len(parts)==3,'Malformed nonempty MatrixMarket entry')
        r,c=map(int,parts[:2]);value=float(parts[2])
        prior.require(1<=r<=nr and 1<=c<=nc and math.isfinite(value) and value>=0 and value.is_integer(),'Invalid sparse entry')
        colkey=(c-1)*nr+r-1;rowkey=(r-1)*nc+c-1
        col_order &= colkey>last_col;row_order &= rowkey>last_row;last_col=colkey;last_row=rowkey;count+=1
        if value>0:seen[types[r-1]][c-1]=True
    prior.require(count==nnz,'MatrixMarket entry count mismatch')
    info.update(n_stored_entries=nnz,coordinate_uniqueness='verified_strict_column_order' if col_order else 'verified_strict_row_order' if row_order else 'not_verified_unsorted',
        numeric_integrity='finite_nonnegative_integer',barcode_axis='one shared matrix column axis',
        observed_both_RNA_ATAC=int((seen.get('Gene Expression',np.zeros(nc,bool))&seen.get('Peaks',np.zeros(nc,bool))).sum()))
    blanks.update(nonempty_feature_records=len(records),feature_record_widths=json.dumps(dict(Counter(len(r) for r in records)),sort_keys=True),
                  nonempty_barcode_records=len(barcodes),matrix_comment_records=comments,nonempty_matrix_entries=count)
    return info,features,barcodes,blanks


def table(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);out=Path(parser.parse_args().output).resolve()
    prior.require(out.parent==ROOT/'analysis/research/runs' and out.is_dir(),'Fresh runner directory required')
    prior.require(all(p.name in ['receipt.json','stdout.log','stderr.log'] for p in out.iterdir()),'Existing output artifacts')
    old=ROOT/'analysis/research/runs/arz1_source_qualification_v1';receipt=json.loads((old/'receipt.json').read_text())
    prior.require(receipt['status']=='executed' and receipt['analysis_id']=='Arz1.source_qualification_v1','Expected preserved v1 receipt')
    manifest=json.loads((PACKAGE/'sources/intake_v1.json').read_text());previous={r['library']:r for r in table(old/'matrix_inventory.csv')}
    matrices=[];feature_rows=[];empty_rows=[];feature_sets={};barcodes={};holds=[]
    for spec in manifest['multiome_libraries']:
        name=spec['id']
        if spec['format']=='h5':
            row=dict(previous[name]);prior.require(row['status']=='structure_checked','Prior HDF5 qualification unavailable')
            # Identifier reads establish the cross-format overlap universe; do not rerun counts/QC.
            with prior.h5py.File(ROOT/spec['paths'][0],'r') as f:
                ids=f['matrix/features/id'].asstr()[:].tolist();types=f['matrix/features/feature_type'].asstr()[:].tolist();bc=f['matrix/barcodes'].asstr()[:].tolist()
            prior.require(prior.fingerprint(ids)==row['feature_id_sha256'] and prior.fingerprint(bc)==row['barcode_sha256'],'Prior identifier fingerprint disagreement')
            ft={typ:{ids[i] for i,t in enumerate(types) if t==typ} for typ in set(types)}
            feature_sets[name]=ft;barcodes[name]=bc;matrices.append(row)
        else:
            row=dict(library=name,accession=spec['accession'],condition=spec['condition'],source_format=spec['format'],rna_sample=spec['rna_sample'],atac_sample=spec['atac_sample'])
            try:
                info,ft,bc,blanks=inspect_mtx(*[ROOT/p for p in spec['paths']]);feature_sets[name]=ft;barcodes[name]=bc
                row.update(status='structure_checked',**{k:v for k,v in info.items() if k!='feature_types'})
                empty_rows.append(dict(library=name,**blanks))
            except (ValueError,KeyError,OSError,StopIteration) as exc:
                row.update(status='held_input_structure',error=str(exc));holds.append(dict(library=name,error_type=type(exc).__name__,error=str(exc)))
            matrices.append(row);print('Amended metadata inspected: '+name,flush=True)
    for name,types in feature_sets.items():
        for typ,ids in sorted(types.items()):feature_rows.append(dict(library=name,feature_type=typ,n_features=len(ids),identifier_set_sha256=prior.fingerprint(sorted(ids))))
    fields=['library','accession','condition','source_format','rna_sample','atac_sample','status','n_features','n_barcodes','feature_id_sha256','barcode_sha256','n_stored_entries','coordinate_uniqueness','numeric_integrity','barcode_axis','observed_both_RNA_ATAC','error']
    prior.write_csv(out/'matrix_inventory.csv',matrices,fields)
    prior.write_csv(out/'empty_record_counts.csv',empty_rows,['library','feature_empty_records','barcode_empty_records','matrix_empty_records','nonempty_feature_records','feature_record_widths','nonempty_barcode_records','matrix_comment_records','nonempty_matrix_entries'])
    prior.write_csv(out/'feature_types.csv',feature_rows,['library','feature_type','n_features','identifier_set_sha256'])
    overlap=[];fo=[]
    for a in feature_sets:
        for b in feature_sets:
            ba=set(barcodes[a]);bb=set(barcodes[b])
            overlap.append(dict(first=a,second=b,first_n=len(ba),second_n=len(bb),shared_barcodes=len(ba&bb),exact_order_match=barcodes[a]==barcodes[b],interpretation='Cross-library whitelist reuse does not identify common cells or animals'))
            for typ in sorted(set(feature_sets[a])|set(feature_sets[b])):
                x=feature_sets[a].get(typ,set());y=feature_sets[b].get(typ,set())
                fo.append(dict(first=a,second=b,feature_type=typ,first_n=len(x),second_n=len(y),shared_ids=len(x&y),identical_sets=x==y))
    prior.write_csv(out/'barcode_overlap.csv',overlap,['first','second','first_n','second_n','shared_barcodes','exact_order_match','interpretation'])
    prior.write_csv(out/'feature_overlap.csv',fo,['first','second','feature_type','first_n','second_n','shared_ids','identical_sets'])
    common=[]
    if len(feature_sets)==len(manifest['multiome_libraries']):
        for typ in sorted(set.intersection(*[set(x) for x in feature_sets.values()])):
            shared=set.intersection(*[x[typ] for x in feature_sets.values()])
            common += [dict(feature_type=typ,stable_id=i) for i in sorted(shared)]
    prior.write_csv(out/'common_feature_ids.csv',common,['feature_type','stable_id'])
    summary=dict(scope='Empty-record metadata adapter; no biological endpoints',prior_receipt=(old/'receipt.json').relative_to(ROOT).as_posix(),
        reused_HDF5_libraries=4,n_multiome_libraries=len(matrices),n_structurally_checked=sum(r['status']=='structure_checked' for r in matrices),
        structural_holds=holds,common_feature_counts=dict(Counter(r['feature_type'] for r in common)),
        source_bytes='unchanged',state_assignment='not_performed',biological_independence='unknown',scientific_acceptance='not_assessed')
    prior.write_json(out/'summary.json',summary);print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
