"""Post-pilot source-completeness sensitivity using published labels and raw matrices."""
import csv,datetime,hashlib,importlib.util,json,tarfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];RQ=ROOT/'RQ_Specified/A23_slc34a2_transition_homeostasis';RUN='published_cell_audit_v1'
SPEC=importlib.util.spec_from_file_location('pilot',RQ/'scripts/02_external_pilot.py');M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)
def run():
 import h5py,numpy as np,openpyxl
 from scipy.sparse import csc_matrix
 out=RQ/'tables'/RUN;meta=RQ/'metadata'/RUN
 if out.exists() or meta.exists():raise FileExistsError('Run already exists')
 cfg=M.read(RQ/'config/external_pilot_v2.json'); contract=M.read(RQ/'config/published_cell_audit_v1.json');prefix=M.read(RQ/'config/external_pilot_v1_annotation_addendum.json')['prefix_map']
 acq=RQ/'metadata/external_acquisition_v1';inputs=[Path(__file__),RQ/'scripts/02_external_pilot.py',RQ/'config/external_pilot_v2.json',RQ/'config/published_cell_audit_v1.json',acq/'raw_matrices.json',RQ/'config/external_pilot_v1_annotation_addendum.json']
 workbook=ROOT/'raw_data/GSE199329/41467_2023_36810_MOESM9_ESM.xlsx';inputs.append(workbook)
 book=openpyxl.load_workbook(workbook,read_only=True,data_only=True);ann=M.annotation_map(list(book['Fig 2a'].values)[1:],prefix);book.close()
 out.mkdir(parents=True);meta.mkdir(parents=True)
 coverage=[];summaries=[];profiles=[]
 records=M.read(acq/'raw_matrices.json')
 # Replay extraction if needed, using exact recorded outer and inner member names.
 for r in records:
  p=ROOT/r['path']
  if not p.exists():
   with tarfile.open(ROOT/'raw_data/GSE199329/GSE199329_RAW.tar') as outer:
    with tarfile.open(fileobj=outer.extractfile(r['outer_member']),mode='r:gz') as inner:
     with inner.extractfile(r['inner_member']) as src,p.open('wb') as dst:shutil.copyfileobj(src,dst)
  if M.digest(p)!=r['sha256']:raise ValueError('Changed raw source')
  inputs.append(p);lib=r['library'];expected={b:label for (l,b),label in ann.items() if l==lib}
  with h5py.File(p,'r') as f:
   g=f['hg19'];barcodes=[b.decode() for b in g['barcodes'][:]];names=[b.decode() for b in g['gene_names'][:]]
   if len(set(barcodes))!=len(barcodes):raise ValueError('Duplicate raw barcodes')
   jj=[j for j,b in enumerate(barcodes) if M.annotation_key(lib,b)[1] in expected]
   kept=[barcodes[j] for j in jj];labels=np.array([expected[M.annotation_key(lib,b)[1]] for b in kept])
   x=csc_matrix((g['data'][:],g['indices'][:],g['indptr'][:]),shape=tuple(g['shape'][:]))[:,jj].tocsr()
  x.sum_duplicates();x.eliminate_zeros();total=np.asarray(x.sum(axis=0)).ravel();ng=np.asarray((x>0).sum(axis=0)).ravel();mt=np.asarray(x[[i for i,gene in enumerate(names) if gene.startswith('MT-')]].sum(axis=0)).ravel()/np.maximum(total,1)
  coverage.append(dict(library=lib,published_cells=len(expected),matched_raw=len(jj),missing_raw=len(expected)-len(jj),published_AT2_raw=int((labels=='AT2').sum())))
  selections={'published_AT2_all':(labels=='AT2') & (total>0)}
  for qc,q in cfg['qc'].items():selections['published_AT2_'+qc]=(labels=='AT2')&(ng>=q['min_genes'])&(ng<=q['max_genes'])&(total<=q['max_counts'])&(mt<=q['max_mito_fraction'])
  for group,mask in selections.items():
   for role,genes in cfg['readouts'].items():
    for gene in genes:
     if names.count(gene)!=1:raise ValueError('Unresolved readout '+gene)
     v=x[names.index(gene)].toarray().ravel();n=int(mask.sum())
     summaries.append(dict(library=lib,group=group,role=role,gene=gene,n=n,n_detected=int((v[mask]>0).sum()),fraction_detected=float((v[mask]>0).mean()),mean_log1p_10k=float(np.log1p(v[mask]*10000/total[mask]).mean())))
  for j,b in enumerate(kept):profiles.append(dict(library=lib,barcode=b,published_label=labels[j],umi=int(total[j]),n_genes=int(ng[j]),mito_fraction=float(mt[j]),AT2_all=bool(selections['published_AT2_all'][j]),AT2_primary=bool(selections['published_AT2_primary'][j]),AT2_strict=bool(selections['published_AT2_strict'][j])))
  print(coverage[-1],flush=True)
 diff=[]
 for group in selections:
  for role,genes in cfg['readouts'].items():
   for gene in genes:
    a=next(r for r in summaries if (r['library'],r['group'],r['gene'])==('GSM5970468',group,gene));b=next(r for r in summaries if (r['library'],r['group'],r['gene'])==('GSM5970470',group,gene))
    diff.append(dict(group=group,role=role,gene=gene,pam_n=a['n'],control_n=b['n'],mean_log1p_difference=a['mean_log1p_10k']-b['mean_log1p_10k'],detection_percentage_point_difference=100*(a['fraction_detected']-b['fraction_detected'])))
 for name,rr in [('coverage',coverage),('marker_summaries',summaries),('marker_differences',diff),('cell_selection',profiles)]:M.write_table(out/(name+'.tsv'),rr)
 rec={'status':'post-pilot descriptive sensitivity, same case and same control','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':[dict(path=p.relative_to(ROOT).as_posix(),sha256=M.digest(p)) for p in inputs],'outputs':[dict(path=p.relative_to(ROOT).as_posix(),sha256=M.digest(p)) for p in sorted(out.glob('*.tsv'))]}
 (meta/'run_record.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8')
 for r in diff:
  if r['gene'] in ['KRT8','SPRR1A','CLU','SLC34A2']:print(r)
if __name__=='__main__':run()
