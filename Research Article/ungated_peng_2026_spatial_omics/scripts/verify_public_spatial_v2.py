"""Independent list-based geometry, regression and spatial statistic checks."""
import math
import numpy as np
from scipy.linalg import lstsq

def verify_section(frame,results):
    checks=0;failures=[];max_error=0.
    def check(ok,label):
        nonlocal checks
        checks+=1
        if not bool(ok):failures.append(label)
    def close(x,y,label,tol=1e-8):
        nonlocal max_error
        if np.isnan(x) and np.isnan(y):check(True,label);return
        e=abs(float(x)-float(y));max_error=max(max_error,e);check(e<tol,label)
    points=list(zip(frame.array_row.astype(int),frame.array_col.astype(int)));lookup={p:i for i,p in enumerate(points)}
    neighbors=[]
    for row,col in points:
        ns=[]
        for dr in [-1,0,1]:
            for dc in [-2,-1,1,2]:
                if (dr==0 and abs(dc)==2) or (abs(dr)==1 and abs(dc)==1):
                    j=lookup.get((row+dr,col+dc))
                    if j is not None:ns.append(j)
        neighbors.append(ns)
    seen=set();groups=[]
    for i in range(len(points)):
        if i in seen:continue
        pending=[i];seen.add(i);group=[]
        while pending:
            j=pending.pop();group.append(j)
            for k in neighbors[j]:
                if k not in seen:seen.add(k);pending.append(k)
        groups.append(group)
    keep=set()
    for group in groups:
        check(len(set(frame.iloc[group].component))==1,'component connected')
        check(frame.iloc[group].endpoint_included.eq(len(group)>=20).all(),'component eligibility')
        if len(group)>=20:keep.update(group)
    check(set(np.flatnonzero(frame.endpoint_included))==keep,'retained mask')
    indexes=sorted(keep)
    for result in results:
        mode=result['mode'];z=np.full((len(frame),2),np.nan)
        for group in groups:
            if len(group)<20:continue
            a=frame.iloc[group];columns=[np.ones(len(group))]
            if mode!='centered':columns.extend([np.log1p(a.total_counts),np.log1p(a.detected_genes)])
            if mode=='depth_composition':columns.extend([a.C1QA,a.COL1A1,a.KRT8])
            design=np.array(columns).T;values=a[['IL1B','CLDN4']].to_numpy()
            # Pivoted QR is separate from the producer's NumPy SVD solver.
            beta=lstsq(design,values,cond=max(design.shape)*np.finfo(float).eps,lapack_driver='gelsy')[0]
            z[group]=values-design@beta
        z=z/np.sqrt(np.nanmean(z*z,axis=0))
        saved=frame[[mode+'_z_IL1B',mode+'_z_CLDN4']].to_numpy()
        close(np.nanmax(np.abs(z-saved)),0,'independent residual normalization',2e-7)
        products=[];second=[];mx=[];my=[];interior=[];local_values=frame[mode+'_local_cross'].to_numpy()
        for i in indexes:
            ns=neighbors[i];check(all(j in keep for j in ns),'no excluded neighbor')
            x,y=z[i];nx=math.fsum(z[j,0] for j in ns)/len(ns);ny=math.fsum(z[j,1] for j in ns)/len(ns)
            value=(x*ny+y*nx)/2;products.append(value);mx.append(x*nx);my.append(y*ny)
            close(value,local_values[i],'local cross',2e-7)
            if len(ns)==6:interior.append(value)
            two=set(k for j in ns for k in neighbors[j])-set(ns)-{i}
            second.append((x*math.fsum(z[k,1] for k in two)+y*math.fsum(z[k,0] for k in two))/(2*len(two)) if two else 0.)
        mean=lambda values:math.fsum(values)/len(values) if values else np.nan
        expected={'same_spot':mean([z[i,0]*z[i,1] for i in indexes]),'lag1':mean(products),'lag2':mean(second),'lag1_minus_lag2':mean(products)-mean(second),'moran_IL1B':mean(mx),'moran_CLDN4':mean(my),'interior_lag1':mean(interior),'interior_spots':len(interior)}
        for key,value in expected.items():close(result[key],value,key,2e-7)
    return {'checks':checks,'failures':failures,'max_absolute_error':max_error}

def verify_aggregation(section,patient,paired):
    checks=0;failures=[];max_error=0.
    def close(x,y,label):
        nonlocal checks,max_error
        checks+=1
        if np.isnan(x) and np.isnan(y):return
        e=abs(x-y);max_error=max(max_error,e)
        if not e<1e-10:failures.append(label)
    for r in patient.itertuples():
        rows=section[(section.patient==r.patient)&(section.histology==r.histology)&(section['mode']==r.mode)]
        rows=rows[rows[r.metric].notna()]
        weights=[1. if r.weighting=='equal_section' else float(x) for x in rows.retained_spots]
        expected=math.fsum(w*v for w,v in zip(weights,rows[r.metric]))/math.fsum(weights) if weights else np.nan
        close(r.value,expected,'patient aggregation')
    for r in paired.itertuples():
        rows=patient[(patient.patient==r.patient)&(patient['mode']==r.mode)&(patient.weighting==r.weighting)&(patient.metric==r.metric)].set_index('histology')
        close(r.delta,rows.loc['LUAD','value']-rows.loc[r.comparison.split('-')[1],'value'],'patient paired delta')
    return {'checks':checks,'failures':failures,'max_absolute_error':max_error}
