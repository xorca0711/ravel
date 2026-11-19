"""Four vehicle-control library ranks for the frozen distal M24 comparison."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from itertools import combinations, product
from pathlib import Path

import numpy as np

PREVIOUS = Path(__file__).resolve().parent.parent / "distal_m24_outcome_v1"
sys.path.insert(0, str(PREVIOUS))
from m24_analysis import WEIGHTED, summarize
from m24_reader import CLASSES, ROOT, load_cohort, read_rows, write_json, write_rows

CONTROLS = ("SRX2448172", "SRX2448173", "SRX10528425", "SRX10528426")
OLD = "D6_width"
BRIDGE = "D6_width_on_retained_regions"
NEW = "D6_width_baseline"
METHODS = (OLD, BRIDGE, NEW)


def sparse_mean(track, chrom, start, end):
    """Decode a qualified genomecov -bg track. Keep storage and fetch masks separate."""
    width = end - start
    if chrom not in track.chromsizes or not 0 <= start < end <= track.chromsizes[chrom]:
        raise ValueError("Undeclared chromosome or invalid bounds")
    seen = np.zeros(width, dtype=bool)
    values = np.zeros(width, dtype=np.float64)
    for name, a, b, value in track.fetch_intervals(chrom, start, end, iterator=True):
        if name != chrom or not 0 <= a < b <= track.chromsizes[chrom]:
            raise ValueError("Invalid native record")
        lo, hi = max(a, start) - start, min(b, end) - start
        if lo >= hi or np.any(seen[lo:hi]):
            raise ValueError("Outside query or overlapping native records")
        if not np.isfinite(value) or value < 0:
            raise ValueError("Nonfinite or negative native signal")
        values[lo:hi] = value
        seen[lo:hi] = True
    raw = np.asarray(track.fetch(chrom, start, end, bins=-1, missing=np.nan, oob=np.inf))
    if raw.shape != (width,) or not np.array_equal(raw[seen], values[seen]):
        raise ValueError("Unbinned fetch disagrees on stored depth or width")
    if not np.all(np.isnan(raw[~seen])):
        raise ValueError("Unbinned missing mask differs from native records")
    return dict(stored_bp=int(seen.sum()), explicit_zero_bp=int(np.sum(seen & (values == 0))),
                sparse_zero_bp=int((~seen).sum()), mean_rpm=float(values.sum(dtype=np.float64)/width))


def extract(regions, sources, paths, out):
    import bbi
    rows, qc, failed = [], {}, False
    if (bbi.__version__, np.__version__) != ("0.4.2", "2.5.5"):
        raise ValueError("Unexpected qualified reader version")
    if tuple(s["srx"] for s in sources) != CONTROLS:
        raise ValueError("Unexpected control libraries or order")
    for s in sources:
        srx = s["srx"]
        path = paths[srx+".bw"]
        diagnostics = dict(gsm=s["gsm"], srx=srx, status="held", valid=0, held=0,
                           stored_bp=0, explicit_zero_bp=0, sparse_zero_bp=0)
        qc[srx] = diagnostics
        try:
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            if digest != s["sha256"] or path.stat().st_size != s["bytes"]:
                raise ValueError("Source bytes differ")
            with bbi.open(str(path)) as handle:
                if (not handle.is_bigwig or handle.chromsizes != s["chromosomes"]
                        or handle.info["summary"]["basesCovered"] != s["header_bases_covered"]):
                    raise ValueError("Source type or chromosome dictionary differs")
                for r in regions:
                    row = {k:r[k] for k in ("s2_excel_row", "source_class", "chromosome", "start0", "end0", "width_bp")}
                    row.update(gsm=s["gsm"], srx=srx, status="held", stored_bp="", explicit_zero_bp="",
                               sparse_zero_bp="", mean_rpm="", error="")
                    try:
                        row.update(sparse_mean(handle, r["chromosome"], int(r["start0"]), int(r["end0"])))
                        row["status"] = "valid"
                        diagnostics["valid"] += 1
                        for key in ("stored_bp", "explicit_zero_bp", "sparse_zero_bp"):
                            diagnostics[key] += row[key]
                    except Exception as exc:
                        row["error"] = f"{type(exc).__name__}: {exc}"
                        diagnostics["held"] += 1
                    rows.append(row)
                if diagnostics["held"] == 0:
                    diagnostics["status"] = "valid"
        except Exception as exc:
            diagnostics["source_error"] = f"{type(exc).__name__}: {exc}"
        failed |= diagnostics["status"] != "valid"
    if rows:
        write_rows(out/"baseline_intervals.tsv", rows)
    write_json(out/"coverage.json", dict(libraries=qc, expected=len(regions)*4,
                                          observed_rows=len(rows), status="held" if failed else "complete"))
    if failed or len(rows) != 4*len(regions):
        raise ValueError("Incomplete D6 source or interval read. See coverage diagnostics.")
    return np.array([[v["mean_rpm"] for v in rows if v["srx"] == s] for s in CONTROLS], dtype=float)


def midranks(values):
    values = np.asarray(values, dtype=np.float64)
    if not len(values) or not np.isfinite(values).all() or np.any(values < 0):
        raise ValueError("Invalid full-width control means")
    _, inverse, counts = np.unique(values, return_inverse=True, return_counts=True)
    twice_centered_rank = 2*np.cumsum(counts) - counts
    return twice_centered_rank[inverse], dict(distinct=len(counts), zero_regions=int(np.sum(values == 0)),
                              largest_tie=int(counts.max()), regions_in_ties=int(counts[counts > 1].sum()),
                              mean_rpm_quantiles=np.quantile(values, [0,.25,.5,.75,1]).tolist())


def rank_design(matrix):
    if matrix.ndim != 2 or matrix.shape[0] != len(CONTROLS):
        raise ValueError("Expected all four control libraries")
    records = [midranks(row) for row in matrix]
    numerators = np.stack([r for r, _ in records])
    ranks = numerators / (2 * matrix.shape[1])
    qc = dict(libraries={s:q for s, (_, q) in zip(CONTROLS, records, strict=True)}, correlations=[])
    for x, y in combinations(range(4), 2):
        scored = records[x][1]["distinct"] > 1 and records[y][1]["distinct"] > 1
        qc["correlations"].append(dict(first=CONTROLS[x], second=CONTROLS[y],
            spearman=float(np.corrcoef(ranks[x],ranks[y])[0,1]) if scored else None,
            mean_absolute_rank_difference=float(np.abs(ranks[x]-ranks[y]).mean())))
    consensus = numerators.sum(axis=0) / (2 * matrix.shape[1] * len(CONTROLS))
    qc["consensus_distinct"] = len(np.unique(consensus))
    qc["status"] = "estimable" if all(q["distinct"] > 1 for _, q in records) and qc["consensus_distinct"] > 1 else "unresolved_constant_rank"
    return ranks, consensus, qc


def weighting(regions, previous, ranks, consensus):
    ids = [r["s2_excel_row"] for r in regions]
    by_id = {r["s2_excel_row"]:r for r in previous}
    if set(ids) != set(by_id) or len(ids) != len(set(ids)) or len(previous) != len(ids):
        raise ValueError("Prior weight rows do not match the cohort")
    classes = np.array([r["source_class"] for r in regions])
    old_cells, old = [], []
    for r in regions:
        p = by_id[r["s2_excel_row"]]
        if (p["source_class"] != r["source_class"] or int(p["width_bp"]) != int(r["width_bp"])
                or float(p["D6_log2FC"]) != float(r["s3_D6_log2FoldChange"])):
            raise ValueError("Frozen two-way covariates differ")
        cell = (int(p["D6_bin"]), int(p["width_bin"]))
        if any(v not in range(1,5) for v in cell):
            raise ValueError("Unknown two-way cell")
        old_cells.append(cell)
        old.append(float(p["overlap_weight"]))
    old = np.array(old)
    if not np.isfinite(old).all() or np.any(old <= 0):
        raise ValueError("Expected positive prior weights across the entire frozen cohort")
    cuts = np.quantile(consensus, [.25,.5,.75], method="linear")
    baseline_bins = np.searchsorted(cuts, consensus, side="right") + 1
    cells = [(*c, int(b)) for c, b in zip(old_cells, baseline_bins, strict=True)]
    counts = Counter(zip(cells, classes))
    shared = {c:min(counts[c,k] for k in CLASSES) for c in product(range(1,5), repeat=3)}
    total = sum(shared.values())
    keep = np.array([shared[c] > 0 for c in cells])
    strata = [dict(D6_bin=c[0], width_bin=c[1], baseline_bin=c[2],
                   Memory=counts[c,CLASSES[0]], Resolved=counts[c,CLASSES[1]], overlap=shared[c],
                   new_mass=shared[c]/total if total else 0.) for c in shared]
    weights = {OLD:old, BRIDGE:np.zeros_like(old), NEW:np.zeros_like(old)}
    if total:
        weights[NEW] = np.array([shared[c]/(total*counts[c,k]) for c,k in zip(cells,classes)])
    summary = {"cutpoints":cuts.tolist(), "strata":strata, "overlap_units":total, "classes":{}, "balance":[]}
    for k in CLASSES:
        mask = classes == k
        if not np.isclose(old[mask].sum(),1,rtol=0,atol=1e-12):
            raise ValueError("Prior weights do not sum to one")
        prior_mass = float(old[mask & keep].sum())
        if total:
            weights[BRIDGE][mask & keep] = old[mask & keep]/prior_mass
            if not all(np.isclose(w[mask].sum(), 1, rtol=0, atol=1e-12) for w in weights.values()):
                raise ValueError("Class weights do not sum to one")
        summary["classes"][k] = dict(full=int(mask.sum()), retained=int((mask & keep).sum()),
            old_mass_retained=prior_mass, old_to_new_total_variation=float(np.abs(old[mask]-weights[NEW][mask]).sum()/2) if total else None,
            weight_diagnostics={m:dict(maximum=float(w[mask].max()), regional_ESS=float(1/(w[mask]@w[mask])))
                                for m,w in weights.items() if np.any(w[mask])})
    occupied = sorted({int(b) for b in baseline_bins[keep]})
    summary["original_strata"] = []
    for ab in product(range(1,5), repeat=2):
        mask = np.array([c == ab for c in old_cells])
        summary["original_strata"].append(dict(D6_bin=ab[0], width_bin=ab[1],
            prior_mass={k:float(old[mask & (classes==k)].sum()) for k in CLASSES},
            prior_mass_retained={k:float(old[mask & keep & (classes==k)].sum()) for k in CLASSES},
            new_mass=sum(shared[(*ab,b)] for b in range(1,5))/total if total else None))
    summary.update(shared_baseline_bins=occupied, shared_three_way_cells=sum(v>0 for v in shared.values()),
                   old_cells_with_new_mass=len({c[:2] for c in shared if shared[c]}),
                   status="estimable" if len(occupied)>=2 else "insufficient_shared_baseline_support")
    metrics = {k:np.array([float(r[k]) for r in regions]) for k in ("s3_D6_log2FoldChange","width_bp")}
    metrics.update(zip(CONTROLS, ranks, strict=True))
    metrics["baseline_consensus"] = consensus
    for name, v in metrics.items():
        parts = [v[classes==k] for k in CLASSES]
        sd = np.sqrt(sum(np.sum((p-p.mean())**2) for p in parts)/(len(v)-2))
        for method, w in {"unweighted":np.ones(len(v)), **weights}.items():
            if not w.any():
                continue
            means = [float(np.average(v[classes==k], weights=w[classes==k])) for k in CLASSES]
            diff = means[0]-means[1]
            summary["balance"].append(dict(covariate=name, method=method, Memory=means[0], Resolved=means[1],
                                           difference=diff, full_pooled_sd=float(sd), standardized=diff/sd if sd else None))
    rows = [dict(s2_excel_row=i, source_class=k, D6_bin=c[0], width_bin=c[1], baseline_bin=c[2],
                 **{s:float(ranks[j,n]) for j,s in enumerate(CONTROLS)}, baseline_consensus=float(consensus[n]),
                 **{m:float(w[n]) for m,w in weights.items()}) for n,(i,k,c) in enumerate(zip(ids,classes,cells))]
    return rows, summary


def effects(regions, samples, late, design_rows, reference):
    pools, changes, pairs = [], [], []
    for method in METHODS:
        w = [dict(s2_excel_row=r["s2_excel_row"], overlap_weight=r[method]) for r in design_rows]
        tables = summarize(regions, samples, late, w)
        for dest, table in zip((pools,changes,pairs), tables, strict=True):
            dest.extend(r | {"method":method} for r in table if r["method"] == WEIGHTED)
    old, bridge, new = changes
    previous, = [r for r in reference if r["method"] == WEIGHTED]
    delta = {}
    for metric in ("Memory","Resolved","gap"):
        if not np.isclose(old[metric],float(previous[metric]),atol=1e-12,rtol=1e-12):
            raise ValueError("Previous two-way weighted change did not reproduce")
        delta[metric] = dict(support_restriction=bridge[metric]-old[metric],
                             redistribution=new[metric]-bridge[metric], total=new[metric]-old[metric])
    return pools, changes, pairs, delta


def run(contract, out):
    specs = json.loads(contract.read_bytes())["inputs"]
    paths = {Path(s["path"]).name: ROOT/s["path"] for s in specs}
    regions, samples = load_cohort(paths)
    info = json.loads(paths["SOURCES_V1.json"].read_bytes())
    matrix = extract(regions, info["libraries"], paths, out)
    ranks, consensus, qc = rank_design(matrix)
    write_json(out/"rank_qc.json", qc)
    if qc["status"] != "estimable":
        raise ValueError(qc["status"])
    rows, support = weighting(regions, read_rows(paths["region_weights.tsv"]), ranks, consensus)
    write_rows(out/"region_weights.tsv", rows)
    write_json(out/"support.json", support)
    if support["status"] != "estimable":
        raise ValueError(support["status"])
    tables = effects(regions, samples, read_rows(paths["intervals.tsv"]), rows, read_rows(paths["history_changes.tsv"]))
    for name, table in zip(("pool_summaries","history_changes","cross_pool"),tables[:3],strict=True):
        write_rows(out/(name+".tsv"),table)
    write_json(out/"change_decomposition.json",tables[3])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    runtime = "raw_data/naik2017_s3_runtime_v1/venv/bin/python"
    rel = [p.resolve().relative_to(ROOT).as_posix() for p in (Path(__file__), args.contract, args.output)]
    if os.name == "nt":
        wsl = ["wsl.exe","-d","Ubuntu","--exec"]
        root = subprocess.check_output(wsl+["wslpath","-a",str(ROOT)],text=True).strip()
        subprocess.run(wsl+[root+"/"+runtime,"-B",root+"/"+rel[0],"--contract",root+"/"+rel[1],"--output",root+"/"+rel[2]],check=True)
    elif Path(sys.executable).absolute() != ROOT/runtime:
        subprocess.run([str(ROOT/runtime),"-B",str(ROOT/rel[0]),"--contract",str(args.contract),"--output",str(args.output)],check=True)
    else:
        run(args.contract,args.output)
