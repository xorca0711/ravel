"""Strict triplet validation. No network, raw dense conversion or duplicate summation."""
from __future__ import annotations
import gzip,hashlib,json,re,pathlib

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def checked_lines(path,item,columns):
 """Read complete gzip to verify CRC and bind exact decompressed ordering."""
 rows=[];h=hashlib.sha256()
 with gzip.open(path,'rb') as f:
  for line in f:
   if len(line)>4096:raise ValueError('oversized TSV line')
   h.update(line);parts=line.decode('utf-8').rstrip('\r\n').split('\t')
   if len(parts) not in columns or not all(parts[:2] if len(parts)>1 else parts):raise ValueError('malformed TSV')
   rows.append(parts)
   if len(rows)>item['lines']:raise ValueError('excess TSV rows')
 if len(rows)!=item['lines']:raise ValueError('TSV length mismatch')
 if item.get('uncompressed_sha256') and h.hexdigest()!=item['uncompressed_sha256']:raise ValueError('TSV content/order mismatch')
 return rows,h.hexdigest()

def load_triplet(root,files,gsm):
 import numpy as np,pandas as pd,scipy.sparse as sp
 chosen=[x for x in files if x['gsm']==gsm]
 if len(chosen)!=3:raise ValueError('exact triplet required')
 items={('matrix' if x['filename'].endswith('.mtx.gz') else 'features' if x['filename'].endswith('_gene.tsv.gz') else 'barcodes'):x for x in chosen}
 if set(items)!={'matrix','features','barcodes'}:raise ValueError('triplet roles ambiguous')
 paths={k:pathlib.Path(root)/v['path'] for k,v in items.items()}
 for k,v in items.items():
  if paths[k].is_symlink() or paths[k].stat().st_size!=v['bytes'] or sha256(paths[k])!=v['sha256']:raise ValueError('compressed hash/size mismatch: '+k)
 features,feature_hash=checked_lines(paths['features'],items['features'],(2,3));barcodes,barcode_hash=checked_lines(paths['barcodes'],items['barcodes'],(1,))
 ids=[x[0] for x in features];bc=[x[0] for x in barcodes]
 if len(set(ids))!=len(ids) or len(set(bc))!=len(bc):raise ValueError('duplicate feature IDs/barcodes')
 m=items['matrix'];nnz=m['stored_entries'];n_genes=m['rows'];n_cells=m['columns']
 if len(features)!=n_genes or len(bc)!=n_cells or nnz>20_000_000 or n_cells>737280 or n_genes>27998:raise ValueError('dimensions/expansion bound')
 row=np.empty(nnz,dtype=np.int32);col=np.empty(nnz,dtype=np.int32);value=np.empty(nnz,dtype=np.int64)
 with gzip.open(paths['matrix'],'rt',encoding='ascii') as f:
  if f.readline().strip()!='%%MatrixMarket matrix coordinate integer general':raise ValueError('unsupported MatrixMarket header')
  line=f.readline()
  while line.startswith('%'):line=f.readline()
  if not re.fullmatch(r'\s*\d+\s+\d+\s+\d+\s*',line):raise ValueError('invalid dimensions')
  if tuple(map(int,line.split()))!=(n_genes,n_cells,nnz):raise ValueError('MatrixMarket dimensions mismatch')
  seen=0
  for line in f:
   if len(line)>128 or not re.fullmatch(r'\s*\d+\s+\d+\s+\d+\s*',line):raise ValueError('non-integer coordinate/count record')
   if seen>=nnz:raise ValueError('excess coordinate records')
   g,c,v=map(int,line.split())
   if not (1<=g<=n_genes and 1<=c<=n_cells and 1<=v<=2147483647):raise ValueError('coordinate/count out of bounds')
   row[seen]=c-1;col[seen]=g-1;value[seen]=v;seen+=1
  if seen!=nnz:raise ValueError('coordinate line count mismatch')
 # No sparse constructor can silently sum duplicates: check keys first.
 keys=row.astype(np.uint64)*np.uint64(n_genes)+col.astype(np.uint64);keys.sort()
 if keys.size>1 and np.any(keys[1:]==keys[:-1]):raise ValueError('duplicate matrix coordinates')
 del keys
 X=sp.coo_matrix((value,(row,col)),shape=(n_cells,n_genes)).tocsr()
 if X.nnz!=nnz or not X.has_canonical_format:raise ValueError('sparse invariant failure')
 var=pd.DataFrame({'gene_id':ids,'gene_symbol':[x[1] for x in features],'feature_type':[x[2] if len(x)==3 else '' for x in features]})
 prefixed=np.array([gsm+'::'+s for s in bc]);assert len(set(prefixed))==len(prefixed)
 for k,v in items.items():
  if sha256(paths[k])!=v['sha256']:raise ValueError('input changed during validation')
 audit={'gsm':gsm,'orientation':'cells x genes; source genes x cells','shape':list(X.shape),'stored_entries':nnz,'duplicates':0,'explicit_zeros':0,'feature_order_sha256':feature_hash,'barcode_order_sha256':barcode_hash,'compressed_hashes':{k:v['sha256'] for k,v in items.items()},'cell_id_prefix':gsm+'::','gzip_crc':'verified by complete EOF reads'}
 return X,var,prefixed,audit
