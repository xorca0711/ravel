"""Metadata-only extension qualification. No expression values are extracted."""
import argparse, csv, gzip, json, re, sys
from collections import Counter, defaultdict
from common_v1 import ROOT, EXT, RUNS, CACHE, read_csv, save_csv, save_json, sha

def soft(path):
    records = defaultdict(list)
    key = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('!') and ' = ' in line:
            key, value = line.split(' = ', 1); records[key].append(value)
        elif key and line and not line.startswith(('^','!','#')):
            records[key][-1] += line
    return dict(records)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    out=ROOT/a.output;out.mkdir(exist_ok=True,parents=True)
    spec=json.loads((EXT/'config/x2_spec_v1.json').read_text())
    contract=json.loads((EXT/'config/x0_contract_v1.json').read_text())
    inventory=[dict(path=i['path'],bytes=(ROOT/i['path']).stat().st_size,sha256=sha(ROOT/i['path'])) for i in contract['inputs']]
    for i,v in zip(contract['inputs'],inventory):assert i['sha256']==v['sha256']
    save_json(out/'input_inventory.json',inventory)
    old=[]
    for rec in sorted(RUNS.glob('Yd1_*/receipt.json')):
        if rec.parent.name.startswith('Yd1_extension_'):continue
        obj=json.loads(rec.read_text())
        for f in obj['outputs']:
            path=ROOT/f['path']
            assert sha(path)==f['sha256'],str(path)
        old.append(dict(receipt=rec.relative_to(ROOT).as_posix(),sha256=sha(rec),outputs_verified=len(obj['outputs']),git_commit=obj['git_commit']))
    table={(r['sheet'],r['cell']):r for r in read_csv(ROOT/spec['source_inventory'],'\t')}
    assigned={};groups=[]
    for panel in spec['panels']:
        for group in panel['groups']:
            for cell in group['cells']:
                key=(panel['sheet'],cell);assert key not in assigned
                assert table[key]['type']=='n'
                float(table[key]['source_value'])
                assigned[key]=(panel['id'],group['id'])
            groups.append(dict(panel=panel['id'],sheet=panel['sheet'],pdf_page=spec['source_pages'][panel['sheet']],group=group['id'],condition=group['label'].replace('\n',' '),cells=';'.join(group['cells']),n_supplied=len(group['cells']),endpoint=panel['endpoint'].replace('\n',' '),biological_unit=panel['biological_unit'],pairing='unknown; no row pairing',limit=panel['limit']))
    cells=[]
    for sheet,(nrow,ncol) in spec['rectangles'].items():
        for row in range(1,nrow+1):
            for col in range(1,ncol+1):
                cell=chr(64+col)+str(row);key=(sheet,cell);item=table.get(key)
                role='blank'
                if item:
                    role='source_label'
                    if item['type']=='n':
                        assert key in assigned, key
                        role='observation'
                panel,group=assigned.get(key,('',''))
                cells.append(dict(sheet=sheet,cell=cell,role=role,source_value=item['source_value'] if item else '',source_type=item['type'] if item else '',panel=panel,group=group,blank_rule='structural spacing/unequal tail; not zero' if not item else ''))
        assert all(re.fullmatch('[A-Z][0-9]+',c) and int(c[1:])<=nrow and ord(c[0])-64<=ncol for sh,c in table if sh==sheet)
    save_csv(out/'panel_cells.csv',cells);save_csv(out/'panel_groups.csv',groups)
    with gzip.open(CACHE/'GSM6428697_metadata.csv.gz','rt',encoding='utf-8',newline='') as f:
        meta=list(csv.DictReader(f))
    with gzip.open(CACHE/'GSM6428697_barcodes.tsv.gz','rt') as f:barcodes=[x.strip() for x in f]
    with gzip.open(CACHE/'GSM6428697_genes.tsv.gz','rt') as f:genes=[x.strip().split('\t') for x in f]
    keys=[r[''] for r in meta]
    assert len(set(keys))==len(keys) and len(set(barcodes))==len(barcodes)
    assert set(keys)==set(barcodes), 'X3 barcode join failed'
    samples=Counter((r['sample'],r['orig.ident'],r['Day'],r['treatment']) for r in meta)
    coverage=[dict(sample=s,orig_ident=o,day=d,treatment=t,pre_filter_barcodes=n,biological_unit='reported source sample; CMO number-to-sample-suffix mapping not explicit in CSV') for (s,o,d,t),n in sorted(samples.items())]
    save_csv(out/'x3_sample_coverage.csv',coverage)
    feature_support={g:[r for r in genes if g in r] for g in ['Il6','P2rx4','Col1a1','Acta2']}
    assert all(len(v)==1 for v in feature_support.values())
    save_json(out/'x3_qualification.json',dict(metadata_columns=list(meta[0]),barcode_rows=len(barcodes),metadata_rows=len(meta),unique_sample_labels=len(samples),barcode_set_match=True,barcode_order_match=keys==barcodes,feature_rows=len(genes),feature_support=feature_support,state_annotation_present=False,known_state_fields=[],expression_read=False,cmotag_day_groups={'Day0':[301,302,303],'Day7':[304,305,306],'Day14':[307,308,309],'Day21':[310,311,312]},cmo_to_csv_sample_suffix='not explicitly mapped; do not infer tag from suffix',remaining=['author post-QC retained barcodes and state labels','demultiplex assignment confidence/ambiguity status','independent animal/preparation identity','subset/export of author object and raw matrix after design review']))
    x4=[]
    for path in sorted(CACHE.glob('GSM9739*.txt')):
        r=soft(path);title=r['!Sample_title'][0]
        x4.append(dict(gsm=path.stem,title=title,tissue='human lung',assay='10x Fixed RNA; tissue FFPE per series/methods',donor_identity='not established by filename',culture_passage='not supplied',state_barcode_map='not supplied',files=';'.join(v for k,vs in r.items() if k.startswith('!Sample_supplementary_file') for v in vs)))
    assert len(x4)==9
    save_csv(out/'x4_sample_map.csv',x4)
    tree=json.loads((CACHE/'SCAHN_tree.json').read_text())
    paths={r['path'] for r in tree['tree']}
    required=['data/samplemeta.csv','results/annotation/SCAHN.cellmeta.csv','results/annotation/SCAHN.subsetproportion.rds','data/cellnumber.rds','results/tables/SCAHN.tableS1.csv','results/annotation/SCAHN.selectedgenes.mat.expr.integrated.rds']
    save_json(out/'x5_code_qualification.json',dict(repository='Khatri-Lab/SCAHN',revision=tree['sha'],tree_truncated=tree['truncated'],dependencies=[dict(path=v,present_in_tree=v in paths) for v in required],source_table_status='generator available; generated table absent from repository tree',donor_identity_status='sampleid.pid joins sample and publication ID; neither proves donor identity',author_sample_filter='01_load_data.R lines 47-49 retains >=30 cells/sample',author_pid_normalization='01_load_data.R line 55 strips a/b/c/d suffixes; preserve original source identifiers before overlap assessment',raw_gene_counts='not qualified; integrated selected-gene matrix cannot substitute',publisher_access='HTTP 200 client challenge, not article content',expression_read=False))
    save_json(out/'qualification_checks.json',dict(prior_receipts=old,prior_outputs_unchanged=True,panel_mapping='all numeric occupied cells mapped; all rectangular blanks preserved',x3_barcode_join='passed',x3_expression_extraction=False,x4_expression_extraction=False,x5_expression_extraction=False,scientific_acceptance='not assessed',python=sys.version))
    print('X0 source inventory, rectangular panel/blank map, barcode/sample qualification and code dependency audit complete')
if __name__=='__main__':main()
