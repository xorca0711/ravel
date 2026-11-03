"""Frozen A5 99/57/53-member attribution; stream original Matrix Market counts."""
import argparse
import csv
import gzip
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import gammaln
from scipy.stats import hypergeom

HOME = Path("RQ_Specified/A5_developmental_programme_reuse")
PREREQ = Path("docs/research_reviews/2026-11-03-full-priority-screening/prerequisites")
MODULES = ("Guo_AT1_AT2_external", "Guo_minus_identity", "Guo_minus_identity_and_controls")


def probability(n, k, budget=500):
    n, k = np.broadcast_arrays(np.asarray(n, float), np.asarray(k, float))
    if not (np.isfinite(n).all() and np.isfinite(k).all() and (n>=budget).all() and (k>=0).all() and (k<=n).all()):
        raise ValueError("Invalid hypergeometric domain")
    result = np.ones(n.shape)
    use = n-k>=budget
    nn, kk = n[use], k[use]
    logp = gammaln(nn-kk+1)-gammaln(nn-kk-budget+1)-gammaln(nn+1)+gammaln(nn-budget+1)
    result[use] = -np.expm1(np.minimum(logp, 0))
    result[k==0] = 0
    return result


def load_counts(cache, genes, barcodes, targets):
    mapping = {gene: i for i, gene in enumerate(genes)}
    if len(mapping)!=len(genes) or len(set(barcodes))!=len(barcodes):
        raise ValueError("Duplicated source identifiers")
    selector = np.full(len(genes), -1, dtype=np.int64)
    for j,gene in enumerate(targets):
        selector[mapping[gene]] = j
    counts = np.zeros((len(targets),len(barcodes)), dtype=np.int64)
    totals = np.zeros(len(barcodes), dtype=np.int64)
    with gzip.open(cache/"GSE141259_HighResolution_rawcounts.mtx.gz", "rt") as handle:
        if not handle.readline().startswith("%%MatrixMarket matrix coordinate"):
            raise ValueError("Unexpected matrix format")
        line = handle.readline()
        while line.startswith("%"):
            line = handle.readline()
        nr,nc,nnz = map(int,line.split())
        transpose = (nr,nc)==(len(barcodes),len(genes))
        if (nr,nc)!=(len(genes),len(barcodes)) and not transpose:
            raise ValueError("Matrix/identifier dimensions differ")
        seen = 0
        for chunk in pd.read_csv(handle,sep=r"\s+",names=["r","c","v"],dtype={"r":"int64","c":"int64","v":"float64"},chunksize=500000):
            rr,cc = chunk.r.to_numpy()-1,chunk.c.to_numpy()-1
            if transpose:
                rr,cc = cc,rr
            values = chunk.v.to_numpy()
            if not (np.isfinite(values).all() and (values>=0).all() and (values==np.floor(values)).all()):
                raise ValueError("Noninteger/negative/nonfinite counts")
            if not ((rr>=0).all() and (rr<len(genes)).all() and (cc>=0).all() and (cc<len(barcodes)).all()):
                raise ValueError("Out-of-range coordinates")
            values=values.astype(np.int64)
            np.add.at(totals,cc,values)
            mapped=selector[rr];keep=mapped>=0
            np.add.at(counts,(mapped[keep],cc[keep]),values[keep])
            seen+=len(chunk)
        if seen!=nnz or (totals<=0).any():
            raise ValueError("NNZ/library conflict")
    return counts,totals,nnz


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True)
    out=Path(parser.parse_args().output);out.mkdir(parents=True,exist_ok=True)
    config=json.loads((HOME/"config/strunz_test_contract.json").read_text())
    modules=json.loads((HOME/"tables/external_test_modules.json").read_text())["modules"]
    modules={key:modules[key] for key in MODULES};targets=modules[MODULES[0]]
    if [len(modules[k]) for k in MODULES]!=[99,57,53] or targets!=sorted(set(targets)):
        raise ValueError("Fixed memberships changed")
    roles=pd.read_csv(PREREQ/"A5_ROLE_TABLE_V1.tsv",sep="\t",keep_default_na=False).set_index("gene")
    if list(roles.index)!=targets:
        raise ValueError("Role/member mismatch")
    for flag,module in zip(["in_99","in_57","in_53"],MODULES):
        if set(roles.index[roles[flag].eq(1)])!=set(modules[module]):
            raise ValueError("Role membership conflict")
    cache=HOME/"cache"
    with gzip.open(cache/"GSE141259_HighResolution_genes.txt.gz","rt") as f:genes=[x.strip() for x in f]
    with gzip.open(cache/"GSE141259_HighResolution_barcodes.txt.gz","rt") as f:barcodes=[x.strip() for x in f]
    meta=pd.read_csv(cache/"GSE141259_HighResolution_cellinfo.csv.gz",sep="\t").set_index("cell_barcode")
    if not meta.index.is_unique or set(meta.index)!=set(barcodes):raise ValueError("Metadata barcode mismatch")
    meta=meta.loc[barcodes].copy()
    if meta.groupby("identifier").sample_id.nunique().max()!=1 or meta.groupby("sample_id").identifier.nunique().max()!=1:raise ValueError("Mouse identity mismatch")
    x,totals,nnz=load_counts(cache,genes,barcodes,targets)
    meta["raw_umi"]=totals;meta["day"]=meta.time_point.str.extract(r"(\d+)").astype(int)
    labels=[config["case_label"],config["reference_label"]]
    window=meta.day.between(config["day_min"],config["day_max"]) & ~meta.sample_id.str.startswith(config["exclude_sample_prefix"]) & meta.cell_type.isin(labels)
    support=[]
    for (mouse,day,label),group in meta[window].groupby(["sample_id","day","cell_type"]):
        support.append(dict(sample_id=mouse,day=int(day),label=label,cells_before_depth=len(group),cells_after_depth=int(group.raw_umi.ge(500).sum())))
    support=pd.DataFrame(support)
    sets=[set(support.loc[support.label.eq(label)&support.cells_after_depth.ge(30),"sample_id"]) for label in labels]
    eligible=sorted(sets[0]&sets[1]);oldpair=pd.read_csv(HOME/"tables/test_v1/paired_differences.tsv",sep="\t")
    oldpair=oldpair[oldpair.reference.eq(labels[1])&oldpair.module.isin(MODULES)]
    if len(eligible)!=24 or set(eligible)!=set(oldpair.sample_id):raise ValueError("Original mouse roster changed")
    support["paired_eligible"]=support.sample_id.isin(eligible);support.to_csv(out/"unit_support.tsv",sep="\t",index=False)
    selected=window & meta.raw_umi.ge(500) & meta.sample_id.isin(eligible)
    indices=np.flatnonzero(selected.to_numpy());chosen=meta.loc[selected].copy()
    chosen[targets]=x[:,indices].T
    chosen[["sample_id","day","cell_type","raw_umi"]+targets].to_csv(out/"cell_target_counts.tsv.gz",sep="\t",index_label="cell_barcode",compression={"method":"gzip","mtime":0})
    gene_rows=[]
    for (mouse,day,label),group in chosen.groupby(["sample_id","day","cell_type"]):
        probs=probability(group.raw_umi.to_numpy()[:,None],group[targets].to_numpy())
        for j,gene in enumerate(targets):
            gene_rows.append(dict(sample_id=mouse,day=int(day),label=label,gene=gene,n_cells=len(group),full_library_sum=int(group.raw_umi.sum()),gene_count_sum=int(group[gene].sum()),mean_detection_probability=float(probs[:,j].mean())))
    gene_table=pd.DataFrame(gene_rows);gene_table.to_csv(out/"unit_gene_expectations.tsv",sep="\t",index=False)
    oldunit=pd.read_csv(HOME/"tables/test_v1/unit_scores.tsv",sep="\t")
    oldunit=oldunit[oldunit.sample_id.isin(eligible)&oldunit.label.isin(labels)&oldunit.module.isin(MODULES)]
    parity=[]
    for row in oldunit.itertuples(index=False):
        v=gene_table[gene_table.sample_id.eq(row.sample_id)&gene_table.label.eq(row.label)&gene_table.gene.isin(modules[row.module])]
        new=float(v.mean_detection_probability.sum()*100/len(modules[row.module]));error=abs(new-row.score)
        if len(v)!=len(modules[row.module]) or not v.n_cells.eq(row.cells).all() or error>1e-8:raise ValueError("Unit/module parity failed")
        parity.append(dict(sample_id=row.sample_id,label=row.label,module=row.module,old=row.score,reconstructed=new,absolute_error=error))
    paired=[]
    for mouse in eligible:
        v=gene_table[gene_table.sample_id.eq(mouse)].pivot(index="gene",columns="label",values="mean_detection_probability")
        delta=100*(v[labels[0]]-v[labels[1]])
        for gene in targets:
            row=dict(sample_id=mouse,gene=gene,delta_detection_pp=float(delta[gene]),roles=roles.loc[gene,"roles"])
            row.update({module:float(delta[gene]/len(gs)) if gene in gs else 0.0 for module,gs in modules.items()});paired.append(row)
    paired=pd.DataFrame(paired);paired.to_csv(out/"member_contributions.tsv",sep="\t",index=False)
    for row in oldpair.itertuples(index=False):
        value=float(paired.loc[paired.sample_id.eq(row.sample_id),row.module].sum());error=abs(value-row.difference_pp)
        if error>1e-8:raise ValueError("Paired/module parity failed")
        parity.append(dict(sample_id=row.sample_id,label="ADI-minus-activated-AT2",module=row.module,old=row.difference_pp,reconstructed=value,absolute_error=error))
    pd.DataFrame(parity).to_csv(out/"aggregate_parity.tsv",sep="\t",index=False)
    role_rows=[]
    for role in sorted({v for value in roles.roles for v in value.split(";")}):
        members=set(roles.index[roles.roles.str.split(";").apply(lambda x:role in x)])
        for module,gs in modules.items():
            by_mouse=paired[paired.gene.isin(members)].groupby("sample_id")[module].sum()
            role_rows.append(dict(role=role,module=module,annotated_members_in_module=len(members&set(gs)),module_denominator=len(gs),n_mice=len(by_mouse),mean_contribution_pp=float(by_mouse.mean()),additivity="non-additive across overlapping roles"))
    pd.DataFrame(role_rows).to_csv(out/"role_contributions.tsv",sep="\t",index=False)
    nn=np.array([500,501,1000,2000,10000]);kk=np.array([0,1,50,250,1]);err=float(np.max(abs(probability(nn,kk)-hypergeom.sf(0,nn,kk,500))))
    if err>1e-8:raise ValueError("Independent hypergeometric parity failed")
    result=dict(ok=True,mice=len(eligible),genes=len(targets),cell_count=len(chosen),nnz=nnz,aggregate_checks=len(parity),max_aggregate_error=max(r["absolute_error"] for r in parity),independent_hypergeometric_max_error=err,role_annotated=18,role_unreviewed=81,limit="Exposed fixed-component attribution; annotations are partial/non-additive and do not demonstrate repair function or independent replication.")
    (out/"verification.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8");print(json.dumps(result))


if __name__=="__main__":main()
