"""S5 conditional cell permutations in line-qualified, exclusive organoid clones."""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

from rna_pairing import audit
from plot_conditional import render

RAW=Path("raw_data/nagaraja_s0")
RUNS=Path("analysis/research/runs")
SCHEMES=("global","line","line_hnf4g")
DRAWS=5000


def write(out,name,table):
    table.to_csv(out/(name+".tsv"),index=False,sep="\t",float_format="%.15g",na_rep="NA",lineterminator="\n")


def load_cells(out):
    key=pd.read_csv(RUNS/"ng26_s0_keys_v1/cell_clone_line_mouse.tsv",sep="\t")
    for name,table in zip(("barcode_prefixes","rna_candidates","adapter_pair_counts","rna_inventory"),audit(key)):
        write(out,name,table)
    released=key.loc[key.in_score_table].rename(columns={"clone_id":"clone","history":"sample"}).copy()
    chunks=pd.read_csv(RAW/"moesm4.txt",sep="\t",chunksize=120000)
    scores=pd.concat([chunk.loc[chunk.feature.isin(["Fos","Hnf4g"])] for chunk in chunks],ignore_index=True)
    ids=["atac_cell","clone","sample"]
    wide=scores.pivot(index=ids,columns="feature",values="score").reset_index()
    data=released.merge(wide,on=ids,how="outer",validate="one_to_one",indicator=True)
    assert data._merge.eq("both").all() and len(data)==4815 and data.atac_cell.nunique()==4193
    assert np.isfinite(data[["Fos","Hnf4g"]]).all().all()
    assert data.groupby("atac_cell")[["Fos","Hnf4g"]].nunique().eq(1).all().all()
    keys=["organoid_line","clone"]
    sizes=data.groupby(keys,as_index=False).agg(released_memberships=("atac_cell","size"),
                    clean_exclusive_memberships=("clean_memberships_of_cell",lambda s:s.eq(1).sum()))
    write(out,"clone_size_ambiguity",sizes)
    clean=data.loc[data.clean_memberships_of_cell.eq(1)].merge(sizes,on=keys,validate="many_to_one")
    assert clean.atac_cell.is_unique
    cells=clean.loc[clean.clean_exclusive_memberships.ge(2)].sort_values([*keys,"atac_cell"]).reset_index(drop=True)
    assert len(cells)==3572 and cells.groupby(keys).ngroups==121 and cells.organoid_line.nunique()==6
    cuts=[]
    for line,idx in cells.groupby("organoid_line").groups.items():
        values=cells.loc[idx,"Hnf4g"]
        low,high=np.quantile(values,[1/3,2/3],method="linear")
        band=np.where(values<=low,1,np.where(values<=high,2,3))
        cells.loc[idx,"Hnf4g_band"]=band
        cuts.append(dict(line=line,tertile1=low,tertile2=high,cells=len(values),distinct_values=values.nunique()))
    cells["Hnf4g_band"]=cells.Hnf4g_band.astype(int)
    write(out,"hnf4g_cutpoints",pd.DataFrame(cuts))
    write(out,"exclusive_cells",cells[["atac_cell","organoid_line","mouse_donor","sample","clone","Fos","Hnf4g",
                                       "Hnf4g_band","released_memberships","clean_exclusive_memberships"]])
    return cells


def simulate(data,floor,omitted,scheme,seed):
    d=data.reset_index(drop=True)
    y=d.Fos.to_numpy()
    clone=d.groupby(["organoid_line","clone"],sort=False).ngroup().to_numpy()
    counts=np.bincount(clone);offset=np.r_[0,np.cumsum(counts)[:-1]]
    assert np.all(counts>=floor) and np.array_equal(clone,np.repeat(np.arange(len(counts)),counts))
    observed=np.median([np.var(y[a:a+n],ddof=1) for a,n in zip(offset,counts)])
    strata={"global":[],"line":["organoid_line"],"line_hnf4g":["organoid_line","Hnf4g_band"]}[scheme]
    partitions=d.groupby(strata,sort=True).indices if strata else {"all":np.arange(len(d))}
    opportunities=[]
    for label,slots in partitions.items():
        comp=np.unique(clone[slots],return_counts=True)[1].astype(np.int64)
        n=len(slots)
        opportunities.append(dict(min_clone_size=floor,omitted_line=omitted,scheme=scheme,
                           stratum=" / ".join(map(str,label)) if isinstance(label,tuple) else str(label),
                           cells=n,clones=len(comp),largest_clone_slots=comp.max(),
                           cross_clone_pairs=int((n**2-np.sum(comp**2))//2),
                           same_clone_pairs=int(np.sum(comp*(comp-1))//2),
                           expected_cells_switch_clone=n-np.sum(comp**2)/n))
    rng=np.random.default_rng(seed);samples=np.empty(DRAWS)
    # Each ID is a unique physical cell. Reassign complete IDs into fixed clone slots within each stratum.
    identity=np.arange(len(d))
    for first in range(0,DRAWS,32):
        b=min(32,DRAWS-first)
        asign=np.broadcast_to(identity,(b,len(d))).copy()
        for slots in partitions.values():
            if len(slots)>1 and len(np.unique(clone[slots]))>1:
                asign[:,slots]=rng.permuted(np.broadcast_to(slots,(b,len(slots))),axis=1)
        if first==0:
            assert np.all(np.sort(asign,axis=1)==identity)
            for slots in partitions.values():
                assert np.all(np.sort(asign[:,slots],axis=1)==np.sort(slots))
        shuffled=y[asign]
        total=np.add.reduceat(shuffled,offset,axis=1)
        sq=np.add.reduceat(shuffled**2,offset,axis=1)
        var=np.maximum(sq-total**2/counts,0)/(counts-1)
        samples[first:first+b]=np.median(np.sqrt(var),axis=1)**2
    avg=samples.mean();sd=samples.std(ddof=1)
    stat=dict(min_clone_size=floor,omitted_line=omitted,scheme=scheme,cells=len(d),clones=len(counts),
              lines=d.organoid_line.nunique(),observed=observed,null_mean=avg,null_sd=sd,null_mcse=sd/np.sqrt(DRAWS),
              null_q025=np.quantile(samples,.025),null_q975=np.quantile(samples,.975),observed_minus_null=observed-avg,
              percent_below_null=100*(avg-observed)/avg if avg>0 else np.nan,
              lower_tail_mc_p=(1+np.count_nonzero(samples<=observed))/(DRAWS+1),
              n_permutations=DRAWS,strata=len(partitions),exchangeable_strata=sum(s["clones"]>1 for s in opportunities),
              expected_cells_switch_clone=sum(s["expected_cells_switch_clone"] for s in opportunities),
              cross_clone_pairs=sum(s["cross_clone_pairs"] for s in opportunities))
    return stat,opportunities,samples


def main(out):
    cells=load_cells(out)
    stats=[];opps=[];nulls={}
    lines=sorted(cells.organoid_line.unique())
    for floor in (2,5):
        d=cells.loc[cells.clean_exclusive_memberships.ge(floor)]
        for omit_no,omitted in enumerate(["none",*lines] if floor==2 else ["none"]):
            eligible=d.loc[d.organoid_line.ne(omitted)]
            for s,scheme in enumerate(SCHEMES):
                seed=np.random.SeedSequence([20261120,floor,omit_no,s])
                result,opportunity,draws=simulate(eligible,floor,omitted,scheme,seed)
                stats.append(result);opps.extend(opportunity)
                nulls[f"size{floor}_{omitted}_{scheme}"]=draws
    table=pd.DataFrame(stats)
    s2=pd.read_csv(RUNS/"ng26_s2_v1/dispersion.tsv",sep="\t")
    prior=s2.loc[s2.feature.eq("Fos"),["variant","observed","null_mean","null_sd","delta","p","fdr"]].copy()
    same=table.loc[table.min_clone_size.eq(2)&table.omitted_line.eq("none")&table.scheme.eq("global")].iloc[0]
    ref=prior.loc[prior.variant.eq("clean_exclusive")].iloc[0]
    assert abs(ref.observed-same.observed)<1e-10
    prior["comparison_to_new_global"]="different eligibility"
    prior.loc[prior.variant.eq("clean_exclusive"),"comparison_to_new_global"]="same cells and clone slots"
    write(out,"s2_ambiguity_reference",prior)
    write(out,"conditional_estimates",table)
    write(out,"permutation_opportunities",pd.DataFrame(opps))
    np.savez_compressed(out/"conditional_nulls.npz",**nulls)
    render(out,table,lines)


if __name__=="__main__":
    main(Path(sys.argv[1]))
