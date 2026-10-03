"""Read deposited legacy AnnData without silently changing labels or scales."""
from pathlib import Path
import json
import h5py
import numpy as np
import pandas as pd
from scipy import sparse

def strings(values):
    return np.array([v.decode('utf-8') if isinstance(v,bytes) else str(v) for v in values])

def read_obs(handle):
    node=handle['obs']
    if isinstance(node,h5py.Dataset):
        rec=node[()]
        data={}
        for field in rec.dtype.names:
            vals=rec[field]
            category=field+'_categories'
            if 'uns' in handle and category in handle['uns']:
                cats=strings(handle['uns'][category][()])
                if np.any(vals < -1) or np.any(vals >= len(cats)):
                    raise ValueError('Invalid categorical code: '+field)
                vals=np.array([cats[int(v)] if v>=0 else '' for v in vals])
            elif vals.dtype.kind in {'O','S','U'}:
                vals=strings(vals)
            data[field]=vals
        df=pd.DataFrame(data)
        df=df.rename(columns={'index':'cell_id','mouse.id':'mouse_id'})
    else:
        data={}
        for field in node:
            item=node[field]
            if isinstance(item,h5py.Group) and 'codes' in item:
                cats=strings(item['categories'][()]);codes=item['codes'][()]
                data[field]=[cats[int(c)] if c>=0 else '' for c in codes]
            else:
                vals=item[()];data[field]=strings(vals) if vals.dtype.kind in {'O','S','U'} else vals
        df=pd.DataFrame(data).rename(columns={'_index':'cell_id','index':'cell_id','mouse.id':'mouse_id'})
    if 'cell_id' not in df or df.cell_id.duplicated().any():
        raise ValueError('Missing/duplicate observation index')
    return df

def read_matrix(handle,key='raw.X'):
    item=handle[key]
    if isinstance(item,h5py.Dataset):return sparse.csr_matrix(item[()])
    shape=tuple(item.attrs.get('h5sparse_shape',item.attrs.get('shape')))
    fmt=item.attrs.get('h5sparse_format',item.attrs.get('encoding-type','csr_matrix'))
    if isinstance(fmt,bytes):fmt=fmt.decode()
    cls=sparse.csc_matrix if str(fmt).startswith('csc') else sparse.csr_matrix
    return cls((item['data'][()],item['indices'][()],item['indptr'][()]),shape=shape).tocsr()

def read_genes(handle,key='raw.var'):
    item=handle[key]
    if isinstance(item,h5py.Dataset):return strings(item[()]['index'])
    return strings(item[item.attrs.get('_index','_index')][()])

def write_json(path,data):
    Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')

def write_tsv(path,data):
    data.to_csv(path,sep='\t',index=False,lineterminator='\n')
