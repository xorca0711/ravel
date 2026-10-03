"""Prospective P06 correction using the pinned author's young-cell name rule."""
from pathlib import Path
import argparse,json
from collections import Counter
import pandas as pd,numpy as np
from openpyxl import load_workbook
from scipy.stats import hypergeom
from nb5_io import write_tsv,write_json

def read(w,s):
    it=w[s].values;return pd.DataFrame(it,columns=next(it))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--table',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output);out.mkdir(exist_ok=True)
    w=load_workbook(args.table,read_only=True,data_only=True);meta=read(w,'metadata');allcells=[];audit=[]
    for age in [3,18,24]:
        source=read(w,f'cell_data_tracer_{age}m');key='cell_name_3m' if age==3 else 'cell_name_18m_24m'
        d=source[['cell_name','clonal_group','group_size']].copy();d['age_months']=age;d['join_key']=d.cell_name.str.replace('-','.',regex=False)+'-1-1' if age==3 else d.cell_name
        m=meta[meta.age==f'{age}m'][[key,'mouse.id','tissue']].rename(columns={key:'join_key','mouse.id':'mouse_id'})
        if m.join_key.duplicated().any() or d.join_key.duplicated().any():raise ValueError('Nonunique qualified repertoire join')
        d=d.merge(m,on='join_key',how='left',validate='one_to_one');d['original_source_in_clone']=pd.to_numeric(d.group_size,errors='coerce').fillna(1)>1
        matched=d.dropna(subset=['mouse_id']);sizes=matched.dropna(subset=['clonal_group']).groupby(['mouse_id','clonal_group']).size()
        direct=Counter(zip(matched.loc[matched.clonal_group.notna(),'mouse_id'],matched.loc[matched.clonal_group.notna(),'clonal_group']))
        assert all(direct[k]==int(v) for k,v in sizes.items())
        d['within_mouse_clone_size']=[int(sizes.get((x.mouse_id,x.clonal_group),1)) if pd.notna(x.mouse_id) and pd.notna(x.clonal_group) else 1 for x in d.itertuples()]
        d['within_mouse_in_clone']=d.within_mouse_clone_size>1
        n=len(matched);clones=int(d.loc[d.mouse_id.notna(),'within_mouse_in_clone'].sum())
        audit.append(dict(age_months=age,source_rows=len(d),source_group_size_clone_cells=int(d.original_source_in_clone.sum()),mapped_rows=n,unmapped_rows=int(d.mouse_id.isna().sum()),source_clone_cells=clones,pooled_fraction=clones/n,paper_denominator={3:1895,18:2056,24:1780}[age],paper_clone_cells={3:55,18:479,24:348}[age]))
        allcells.append(d)
    w.close();cells=pd.concat(allcells,ignore_index=True);mapped=cells.dropna(subset=['mouse_id']);depth=int(mapped.groupby(['age_months','mouse_id']).size().min());rows=[];tissues=[]
    for (age,mouse),g in mapped.groupby(['age_months','mouse_id'],observed=True):
        groups=Counter(g.clonal_group.dropna());sizes=list(groups.values())+[1]*int(g.clonal_group.isna().sum());n=len(g);assert sum(sizes)==n
        expected=sum(k/n*(1-hypergeom.pmf(0,n-1,k-1,depth-1)) for k in sizes)
        rows.append(dict(age_months=int(age),mouse_id=mouse,reconstructed_cells=n,source_clone_cells=int(g.within_mouse_in_clone.sum()),source_clone_fraction=float(g.within_mouse_in_clone.mean()),within_mouse_clone_fraction=float(g.within_mouse_in_clone.mean()),common_depth=depth,expected_fraction_at_common_depth=float(expected),tissues=';'.join(sorted(g.tissue.unique()))))
        for tissue,h in g.groupby('tissue'):tissues.append(dict(age_months=int(age),mouse_id=mouse,tissue=tissue,reconstructed_cells=len(h),clone_cells=int(h.within_mouse_in_clone.sum())))
    write_tsv(out/'repertoire_cells.tsv',cells);write_tsv(out/'repertoire_mouse.tsv',pd.DataFrame(rows));write_tsv(out/'repertoire_source.tsv',pd.DataFrame(audit));write_tsv(out/'repertoire_tissue.tsv',pd.DataFrame(tissues))
    write_json(out/'verification.json',{'passed':True,'source_conversion':'3m: replace every hyphen with period, then append -1-1; exact pinned author notebook rule. Older cell names unchanged.','arithmetic':'Independent Counter and pandas groupby agree on every matched animal-clone size. Unmatched source rows retained.','common_depth':depth,'limits':'Updated source tables need not equal the final paper denominator. Matched subset is source-selection dependent; tissue mixture and reconstruction selection unresolved. All inference descriptive.'})
    print(json.dumps({'common_depth':depth,'ages':audit}))

if __name__=='__main__':main()
