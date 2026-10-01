"""Frozen A22 same-screen prediction diagnostics; no biological inference."""
import csv
import datetime
import hashlib
import json
import platform
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
RQ = ROOT / "RQ_Specified/A22_epithelial_identity_niche_response"
NB = ROOT / "Research Article/gate2_N2_nabhan_2026"
RUN = "identity_amount_v2"


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_rows(p):
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_rows(p, rows):
    if not rows:
        raise ValueError("Empty output: " + str(p))
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def unique(rows, key):
    result = {r[key]: r for r in rows}
    if len(result) != len(rows):
        raise ValueError("Nonunique " + key)
    return result


def make_folds(targets, plates, mode, target_universe=None):
    targets = np.asarray(targets)
    plates = np.asarray(plates)
    if mode == "target_holdout":
        ordered = sorted(set(targets if target_universe is None else target_universe), key=lambda t: hashlib.sha256(t.encode()).hexdigest())
        assignment = {t: i % 5 for i, t in enumerate(ordered)}
        for k in range(5):
            test = np.array([assignment[t] == k for t in targets])
            yield str(k + 1), ~test, test
    else:
        for plate in sorted(set(plates)):
            test = plates == plate
            train = (~test) & ~np.isin(targets, targets[test])
            yield str(plate), train, test


def predict(x, y, train, test, targets):
    count = Counter(targets[train])
    weights = np.array([1.0 / count[t] for t in targets[train]])
    mu = np.average(x[train], axis=0, weights=weights)
    sd = np.sqrt(np.average((x[train] - mu) ** 2, axis=0, weights=weights))
    keep = sd > 1e-12
    a = np.column_stack([np.ones(train.sum()), (x[train][:, keep] - mu[keep]) / sd[keep]])
    b = np.column_stack([np.ones(test.sum()), (x[test][:, keep] - mu[keep]) / sd[keep]])
    weighted = a * np.sqrt(weights[:, None])
    rank = int(np.linalg.matrix_rank(weighted))
    if rank != weighted.shape[1]:
        raise ValueError("Rank-deficient model")
    coef = np.linalg.lstsq(weighted, y[train] * np.sqrt(weights), rcond=None)[0]
    return b @ coef, rank


def run():
    contract = RQ / "config/identity_amount_v2.json"
    cfg = json.loads(contract.read_text())
    for r in cfg["inputs"]:
        if digest(ROOT / r["path"]) != r["sha256"]:
            raise ValueError("Changed input: " + r["path"])
    out, meta = RQ / "tables" / RUN, RQ / "metadata" / RUN
    if out.exists() or meta.exists():
        raise FileExistsError("Preserve archived runs")
    pair = unique(read_rows(NB / "runs/R4_v1/paired_library_QC.tsv"), "library")
    image = unique(read_rows(ROOT / "RQ_Specified/A10_organoid_growth_outcome/tables/well_join.tsv"), "library name")
    mouse = unique([r for r in read_rows(NB / "runs/R2_v1/mouse_panel_scores.tsv") if r["program"] == cfg["identity"]], "library")
    human = read_rows(NB / "runs/R2_v1/human_panel_scores.tsv")
    outcomes = {name: unique([r for r in human if r["program"] == name], "library") for name in [cfg["primary_outcome"], cfg["secondary_outcome"]]}
    panel = next(r for r in read_rows(NB / "runs/R2_v1/mouse_panel_eligibility.tsv") if r["program"] == cfg["identity"])["required_genes"].split(";")
    overlap = sorted({r["target"] for r in read_rows(NB / "runs/00_v1/target_identity.tsv") if r["source_gene_name"].lower() in {g.lower() for g in panel}})
    audit, joined = [], []
    fields = [f"organoids_{kind}_day{day}" for kind in ["area_mean", "count", "area_prop"] for day in ["07", "14"]]
    for lib, r in sorted(pair.items()):
        reasons = []
        if r["target"] in cfg["controls"]:
            reasons.append("reference_control_excluded")
        maps = {"imaging": image, "identity": mouse, **outcomes}
        for name, lookup in maps.items():
            if lib not in lookup:
                reasons.append("missing_" + name)
        if all(lib in m for m in maps.values()):
            if image[lib]["crispr_target"] != r["target"] or image[lib]["plate"] != r["plate"]:
                raise ValueError("Imaging join mismatch")
            for lookup in [mouse, *outcomes.values()]:
                if (lookup[lib]["target"], lookup[lib]["plate"]) != (r["target"], r["plate"]):
                    raise ValueError("Panel join mismatch")
            try:
                v = [float(image[lib][f]) for f in fields]
                depth = [float(r["total_reads_" + s]) for s in ["mouse", "human"]]
                if not np.isfinite(v + depth).all() or min(v) < 0 or min(depth) <= 0:
                    reasons.append("invalid_imaging_or_depth")
            except (ValueError, TypeError):
                reasons.append("invalid_imaging_or_depth")
        audit.append(dict(library=lib, target=r["target"], plate=r["plate"], eligible=not reasons, reason=";".join(reasons)))
        if not reasons:
            row = dict(library=lib, target=r["target"], plate=r["plate"], unit=image[lib]["unit"], identity=float(mouse[lib]["score"]))
            row.update({name: float(lookup[lib]["score"]) for name, lookup in outcomes.items()})
            row.update(dict(zip(["area07", "area14", "count07", "count14", "prop07", "prop14"], v)))
            row.update(mouse_reads=depth[0], human_reads=depth[1])
            joined.append(row)
    if not joined:
        raise ValueError("No eligible wells")
    predictions, folds, memberships = [], [], []
    for variant in cfg["variants"]:
        omit = set(overlap) if "identity_panel_targets" in variant else set()
        if "NKX21" in variant:
            omit.add("NKX21")
        rows = [r for r in joined if r["target"] not in omit]
        targets = np.array([r["target"] for r in rows]); plates = np.array([r["plate"] for r in rows])
        baseline = np.array([[r["area07"], r["area14"], np.log1p(r["count07"]), np.log1p(r["count14"]), r["prop07"], r["prop14"], np.log2(r["mouse_reads"]), np.log2(r["human_reads"])] for r in rows])
        identity = np.array([r["identity"] for r in rows])
        for mode in ["target_holdout", "plate_shift"]:
            base = baseline
            if mode == "target_holdout":
                base = np.column_stack([base, *[(plates == p).astype(float) for p in sorted(set(plates))[1:]]])
            for fold, train, test in make_folds(targets, plates, mode, [r["target"] for r in joined]):
                if set(targets[train]) & set(targets[test]):
                    raise AssertionError("Target leakage")
                if len(set(targets[train])) < 20 or len(set(targets[test])) < 5:
                    raise ValueError("Insufficient target coverage")
                if mode == "target_holdout" and len(set(plates[train])) != 4:
                    raise ValueError("Missing training plate")
                folds.append(dict(variant=variant, mode=mode, fold=fold, train_wells=int(train.sum()), test_wells=int(test.sum()), purged_wells=int((~(train | test)).sum()), train_targets=len(set(targets[train])), test_targets=len(set(targets[test]))))
                for i, r in enumerate(rows):
                    memberships.append(dict(variant=variant, mode=mode, fold=fold, library=r["library"], target=r["target"], plate=r["plate"], role="train" if train[i] else "test" if test[i] else "purged"))
                for endpoint in outcomes:
                    y = np.array([r[endpoint] for r in rows])
                    p0, rank0 = predict(base, y, train, test, targets)
                    p1, rank1 = predict(np.column_stack([base, identity]), y, train, test, targets)
                    for k, i in enumerate(np.flatnonzero(test)):
                        predictions.append(dict(variant=variant, mode=mode, fold=fold, endpoint=endpoint, library=rows[i]["library"], target=targets[i], plate=plates[i], observed=y[i], baseline=p0[k], plus_identity=p1[k], baseline_rank=rank0, full_rank=rank1))
    target_errors = []
    buckets = defaultdict(list)
    for r in predictions:
        buckets[tuple(r[k] for k in ["variant", "mode", "endpoint", "target"])].append(r)
    for key, rr in sorted(buckets.items()):
        b = np.mean([(r["observed"] - r["baseline"]) ** 2 for r in rr]); f = np.mean([(r["observed"] - r["plus_identity"]) ** 2 for r in rr])
        target_errors.append(dict(zip(["variant", "mode", "endpoint", "target"], key), wells=len(rr), baseline_mse=float(b), full_mse=float(f), mse_improvement=float(b-f)))
    metrics = []
    for variant in cfg["variants"]:
        for mode in ["target_holdout", "plate_shift"]:
            for endpoint in outcomes:
                rr = [r for r in predictions if (r["variant"], r["mode"], r["endpoint"]) == (variant, mode, endpoint)]
                for fold in ["pooled"] + sorted({r["fold"] for r in rr}):
                    selected = rr if fold == "pooled" else [r for r in rr if r["fold"] == fold]
                    bytarget = defaultdict(list)
                    for r in selected:
                        bytarget[r["target"]].append(r)
                    bm = float(np.mean([np.mean([(r["observed"]-r["baseline"])**2 for r in tt]) for tt in bytarget.values()]))
                    fm = float(np.mean([np.mean([(r["observed"]-r["plus_identity"])**2 for r in tt]) for tt in bytarget.values()]))
                    metrics.append(dict(variant=variant, mode=mode, endpoint=endpoint, fold=fold, wells=len(selected), targets=len(bytarget), baseline_target_mse=bm, full_target_mse=fm, baseline_target_rmse=np.sqrt(bm), full_target_rmse=np.sqrt(fm), relative_target_mse_reduction=1-fm/bm, baseline_well_mse=float(np.mean([(r["observed"]-r["baseline"])**2 for r in selected])), full_well_mse=float(np.mean([(r["observed"]-r["plus_identity"])**2 for r in selected]))))
    out.mkdir(parents=True); meta.mkdir(parents=True)
    for name, rr in [("join_audit", audit), ("joined_wells", joined), ("folds", folds), ("fold_membership", memberships), ("predictions", predictions), ("target_errors", target_errors), ("metrics", metrics)]:
        write_rows(out / (name + ".tsv"), rr)
    summary = dict(paired_wells=len(pair), imaging_wells=len(image), eligible_wells=len(joined), eligible_targets=len({r["target"] for r in joined}), excluded_reason_counts=dict(Counter(r["reason"] for r in audit if not r["eligible"])), identity_panel_overlap_targets=overlap, timing="day14 RNA concurrent with day14 imaging; day7 also post-perturbation")
    (meta / "design_audit.json").write_text(json.dumps(summary, indent=2)+"\n")
    inputs = cfg["inputs"] + [dict(path=p.relative_to(ROOT).as_posix(), sha256=digest(p)) for p in [contract, Path(__file__)]]
    outputs = [dict(path=p.relative_to(ROOT).as_posix(), sha256=digest(p)) for p in sorted(out.glob("*.tsv"))] + [dict(path=(meta/"design_audit.json").relative_to(ROOT).as_posix(), sha256=digest(meta/"design_audit.json"))]
    rec = dict(status="completed descriptive same-screen extension", completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), python=platform.python_version(), numpy=np.__version__, inputs=inputs, outputs=outputs)
    (meta/"run_record.json").write_text(json.dumps(rec,indent=2)+"\n")
    print(json.dumps(summary))
    for r in metrics:
        if r["fold"] == "pooled" and r["endpoint"] == cfg["primary_outcome"]:
            print(r["variant"],r["mode"],round(r["relative_target_mse_reduction"],4))


if __name__ == "__main__":
    run()
