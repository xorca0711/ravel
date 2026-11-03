import io
import numpy as np
import pandas as pd
from screen_resolution_v1 import read_counts, interval, summarize, GENES

def test_stream():
    raw=b"%%MatrixMarket matrix coordinate integer general\n% synthetic\n3 2 4\n1 1 2\n3 1 4\n2 2 7\n3 2 1\n"
    totals,nf,panel,nnz=read_counts(io.BytesIO(raw),3,2,[2,0])
    assert totals.tolist()==[6,8] and nf.tolist()==[2,2] and panel.tolist()==[[4,1],[2,0]] and nnz==4
    try: read_counts(io.BytesIO(raw.replace(b'2 2 7',b'2 2 -1')),3,2,[0])
    except ValueError: pass
    else: raise AssertionError('Negative counts accepted')

def test_intervals_and_missing_support():
    effect,lo,hi,df=interval([1,2,3],[0,1,2])
    assert abs(effect-1)<1e-12 and abs(lo-(-1.2669579355275231))<1e-10 and abs(hi-3.266957935527523)<1e-10 and df==4
    degenerate=interval([0,0,0],[0,0,0]);assert degenerate[0]==0 and np.isnan(degenerate[1:]).all()
    mice=pd.DataFrame([dict(mice=f'm{i}',capture='YoungD14',age_group='Young',stage_day=14,condition='PBS' if i<3 else 'Bleo') for i in range(6)])
    m=pd.DataFrame([dict(mice=f'm{i}',celltype='AM1') for i in range(6) for _ in range(10 if i!=5 else 9)])
    counts=np.ones((len(GENES),len(m)),dtype=np.int64);totals=np.full(len(m),100,dtype=np.int64)
    s,e,c=summarize(m,mice,counts,totals)
    am=c[(c.state=='AM1')&(c.gene=='Arg1')].iloc[0]
    assert am.n_BLM==2 and am.n_PBS==3 and not am.estimated and np.isnan(am.effect_log2CPM)
    assert len(s)==6*14 and len(e)==6*51 and (s[s.state=='AT1'].n_cells==0).all()
    assert e[e.state=='AT1'].log2_CPM_plus1.isna().all()

if __name__=='__main__':
    test_stream();test_intervals_and_missing_support();print('PASS: original-count stream arithmetic, invalid count rejection, Welch reference, complete-arm eligibility and zero/low-support retention')
