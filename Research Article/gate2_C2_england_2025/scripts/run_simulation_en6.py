"""England continuation EN6: audit of the deposited two-population stochastic simulator.

Source: sim_two_pop_model.m inside the Zenodo v1.1 archive (SHA-256 in the contract; member identical to
Git blob 9cf4e967cd19f17b968ff175d129529ac5f40312). Parameters are taken literally from the script; nothing
is fitted. Three implementations (contract + amendment CA1):
  literal          : founder allocation rep <= fs*nclones counted from zero (one extra F founder), event applied
                     after the waiting time even when it crosses t_max, propensities of the old regime used across
                     tau, S-loss branch cumulative (..+wp2+wp2)/w, extinct clones recorded then removed by n>=2.
  literal_fixed_branch : identical except the S-loss branch cumulative is the total propensity (CA1 diagnostic).
  gillespie        : boundary-correct: no event past t_max, regime switch applied exactly at tau (memoryless),
                     round(fs*nclones) F founders, correct branch cumulative.
Each block x time x implementation x seed: 100 replicates x 1,000 clones; CCDF P(N>n | N>=2) averaged over
replicates as in the source's cumulativeProb. The Gillespie implementation is validated against the analytic
one-lineage birth-death law. Batch1 LOMO parameter spread is summarised from its saved table (not refitted).

Outputs: trials/continuation/EN6/*.csv + run_record.json.
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime, platform, zipfile, math
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); p.add_argument('--archive', type=Path, required=True); a = p.parse_args()
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
os.environ.setdefault('NUMBA_NUM_THREADS', '4'); os.environ.setdefault('NUMBA_CACHE_DIR', str(HERE / 'processed/continuation/numba_cache'))
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd
from numba import njit
import importlib.metadata as im
CONTRACT = HERE / 'config/continuation_contract.json'; AMEND = HERE / 'config/continuation_amendments.json'
cfg = json.loads(CONTRACT.read_text(encoding='utf-8')); sim = cfg['simulation']
OUT = HERE / 'trials/continuation/EN6'; OUT.mkdir(parents=True, exist_ok=True)
assert not (OUT / 'run_record.json').exists(), 'Refuse overwrite of completed run'
def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
def git_head(root):
    g = root / '.git'; gitdir = Path(g.read_text().split(':', 1)[1].strip()) if g.is_file() else g
    ref = (gitdir / 'HEAD').read_text().strip()[5:]
    common = (gitdir / (gitdir / 'commondir').read_text().strip()).resolve() if (gitdir / 'commondir').exists() else gitdir
    f = common / ref
    return f.read_text().strip() if f.exists() else [l.split()[0] for l in (common / 'packed-refs').read_text().splitlines() if l.endswith(' ' + ref)][0]
zsha = digest(a.archive); assert zsha == sim['source_archive_sha256'], 'archive hash mismatch'
with zipfile.ZipFile(a.archive) as zf:
    member = [n for n in zf.namelist() if n.endswith('sim_two_pop_model.m')][0]; src = zf.read(member)
blob = hashlib.sha1(b'blob %d\0' % len(src) + src).hexdigest()
record = {'stage': 'EN6 simulator audit', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'contract_sha256': digest(CONTRACT), 'amendments_sha256': digest(AMEND),
          'script_sha256': digest(Path(__file__)), 'git_head': git_head(ROOT), 'interpreter': sys.executable, 'python': platform.python_version(),
          'versions': {m: im.version(m) for m in ['numpy', 'pandas', 'numba']}, 'archive': {'path': str(a.archive), 'sha256': zsha, 'member': member, 'git_blob_sha1': blob},
          'rules': sim, 'rng': 'numba np.random (Mersenne Twister) seeded per replicate as seed*1000+replicate; not MATLAB rand, so no bitwise reproduction is claimed'}
(OUT / 'started.json').write_text(json.dumps(record, indent=2) + '\n')

# ---------------- literal parameter blocks (main script; note the script names the F rate 'sigma_s' and the S rate 'sigma_p')
BLOCKS = {
    'Confetti': dict(model=1, fs=0.16, sigma_f=2 * 0.124 / 7, sigma_s=2 * 0.03 / 7, r=0.5, q=0.5, times=[7 * t for t in (12, 24, 36, 52, 60, 72)], tau=np.inf, tau_sigma_f=np.nan, tau_r=np.nan, tau_sigma_s=np.nan, tau_q=np.nan),
    'Red2Kras_YFP': dict(model=2, fs=0.12, sigma_f=2 * 13.62 / 7, sigma_s=2 * 1.5 / 7, r=0.5, q=0.5, times=[7, 14, 28], tau=7.0, tau_sigma_f=2 * 1.221 / 7, tau_r=0.5, tau_sigma_s=2 * 0.2425 / 7, tau_q=0.5),
    'Red2Kras_RFP': dict(model=2, fs=0.08, r=0.7, q=0.7, sigma_f=3.1 / 7 / (2 * 0.7 - 1), sigma_s=0.9 / 7 / (2 * 0.7 - 1), times=[7, 14, 28], tau=14.0, tau_r=0.7, tau_q=0.7, tau_sigma_f=0.5 / 7 / (2 * 0.7 - 1), tau_sigma_s=0.01 / 7 / (2 * 0.7 - 1)),
}
NREP, NCLONES = sim['replicates'], sim['clones_per_replicate']; SEEDS = sim['seeds']; NMAX = 20000  # numerical cap on n>=2 CCDF support; hard cap on cells to bound runtime (recorded)

@njit(cache=True)
def _run(mode, nclones, fs, sf, r, ss, q, tau, tsf, tr, tss, tq, tmax, ncap, seed):
    """mode 0 literal, 1 literal_fixed_branch, 2 gillespie. Returns final sizes (F+S) and founder type per clone."""
    np.random.seed(seed)
    sizes = np.zeros(nclones, np.int64); founder_F = np.zeros(nclones, np.int64)
    nF_lit = int(math.floor(fs * nclones)) + 1 if fs * nclones == math.floor(fs * nclones) else int(math.floor(fs * nclones)) + 1  # rep <= fs*n for rep=0..: floor(fs*n)+1 founders
    nF_g = int(round(fs * nclones))
    capped = 0
    for rep in range(nclones):
        if mode == 2: isF = rep < nF_g
        else: isF = rep < nF_lit
        F = 1 if isF else 0; S = 0 if isF else 1; t = 0.0
        while t < tmax and (F + S) > 0 and (F + S) < ncap:
            if t < tau: a1 = sf * r * F; a2 = sf * (1 - r) * F; b1 = ss * q * S; b2 = ss * (1 - q) * S
            else: a1 = tsf * tr * F; a2 = tsf * (1 - tr) * F; b1 = tss * tq * S; b2 = tss * (1 - tq) * S
            w = a1 + a2 + b1 + b2
            if w <= 0: break
            dt = -math.log(1.0 - np.random.random()) / w
            if mode == 2:
                if t < tau and t + dt > tau: t = tau; continue      # regime boundary: restart the clock with new rates (memoryless)
                if t + dt > tmax: t = tmax; break                    # no event past the horizon
            t += dt
            u = np.random.random()
            if u <= a1 / w: F += 1
            elif u <= (a1 + a2) / w: F -= 1
            elif u <= (a1 + a2 + b1) / w: S += 1
            else:
                if mode == 0:
                    if u <= (a1 + a2 + b2 + b2) / w: S -= 1          # source branch cumulative (typo); otherwise no event
                else: S -= 1
        if (F + S) >= ncap: capped += 1
        sizes[rep] = F + S; founder_F[rep] = 1 if isF else 0
    return sizes, founder_F, capped

def ccdf_ge2(sizes, nmax):
    s = sizes[sizes >= 2]
    if len(s) == 0: return np.full(nmax - 1, np.nan)
    counts = np.bincount(np.minimum(s, nmax), minlength=nmax + 1)[2:]  # sizes 2..nmax (>=nmax pooled)
    pdf = counts / counts.sum(); return 1 - np.cumsum(pdf)  # P(N > n) for n = 2..nmax, matching cumulativeProb

MODES = {'literal': 0, 'literal_fixed_branch': 1, 'gillespie': 2}
ccdf_rows, summary_rows, diff_rows = [], [], []
ns = np.arange(2, NMAX + 1)
for bname, b in BLOCKS.items():
    for tmax in b['times']:
        pooled = {}
        for mname, mode in MODES.items():
            for seed in SEEDS:
                cc = np.zeros((NREP, NMAX - 1)); frac_ge2 = np.zeros(NREP); mean_ge2 = np.zeros(NREP); p90 = np.zeros(NREP); mx = np.zeros(NREP); ext = np.zeros(NREP); capped_tot = 0; allsz = []
                for k in range(NREP):
                    sz, fF, capped = _run(mode, NCLONES, b['fs'], b['sigma_f'], b['r'], b['sigma_s'], b['q'], b['tau'], b['tau_sigma_f'], b['tau_r'], b['tau_sigma_s'], b['tau_q'], float(tmax), NMAX, seed * 1000 + k)
                    cc[k] = ccdf_ge2(sz, NMAX); ge2 = sz[sz >= 2]; frac_ge2[k] = (sz >= 2).mean(); ext[k] = (sz == 0).mean(); capped_tot += capped
                    mean_ge2[k] = ge2.mean() if len(ge2) else np.nan; p90[k] = np.quantile(ge2, .9) if len(ge2) else np.nan; mx[k] = sz.max(); allsz.append(sz)
                m = np.nanmean(cc, 0); sd = np.nanstd(cc, 0, ddof=1); keep = ns <= min(NMAX, int(np.nanmax(mx)) + 1)
                for n_, mm, ss_ in zip(ns[keep], m[keep], sd[keep]): ccdf_rows.append({'block': bname, 'time_days': tmax, 'implementation': mname, 'seed': seed, 'size_n': int(n_), 'ccdf_mean_P_N_gt_n': float(mm), 'ccdf_sd': float(ss_)})
                summary_rows.append({'block': bname, 'time_days': tmax, 'implementation': mname, 'seed': seed, 'replicates': NREP, 'clones_per_replicate': NCLONES,
                                     'F_founders_per_replicate': int(fF.sum()), 'fraction_extinct_mean': float(ext.mean()), 'fraction_size_ge2_mean': float(frac_ge2.mean()), 'mean_size_ge2_mean': float(np.nanmean(mean_ge2)),
                                     'p90_size_ge2_mean': float(np.nanmean(p90)), 'max_size_mean': float(mx.mean()), 'clones_hitting_cap': int(capped_tot), 'cap': NMAX})
                pooled[(mname, seed)] = np.concatenate(allsz)
        # implementation differences (pooled over replicates, seed 1 vs seed 1; and seed-to-seed within implementation)
        def ks(x, y):
            x = x[x >= 2]; y = y[y >= 2]; grid = np.unique(np.concatenate([x, y])); Fx = np.searchsorted(np.sort(x), grid, 'right') / len(x); Fy = np.searchsorted(np.sort(y), grid, 'right') / len(y)
            return float(np.abs(Fx - Fy).max())
        s1 = SEEDS[0]
        for A, B in [('literal', 'literal_fixed_branch'), ('literal', 'gillespie'), ('literal_fixed_branch', 'gillespie')]:
            diff_rows.append({'block': bname, 'time_days': tmax, 'comparison': f'{A} vs {B}', 'seed': s1, 'ks_distance_conditional_ge2': ks(pooled[(A, s1)], pooled[(B, s1)]),
                              'mean_size_ge2_A': float(pooled[(A, s1)][pooled[(A, s1)] >= 2].mean()), 'mean_size_ge2_B': float(pooled[(B, s1)][pooled[(B, s1)] >= 2].mean()),
                              'fraction_ge2_A': float((pooled[(A, s1)] >= 2).mean()), 'fraction_ge2_B': float((pooled[(B, s1)] >= 2).mean())})
        for mname in MODES: diff_rows.append({'block': bname, 'time_days': tmax, 'comparison': f'{mname}: seed {SEEDS[0]} vs seed {SEEDS[1]}', 'seed': -1, 'ks_distance_conditional_ge2': ks(pooled[(mname, SEEDS[0])], pooled[(mname, SEEDS[1])])})
        print(f'{bname} t={tmax} done', flush=True)
pd.DataFrame(ccdf_rows).to_csv(OUT / 'simulation_ccdf.csv', index=False); pd.DataFrame(summary_rows).to_csv(OUT / 'simulation_summary.csv', index=False); pd.DataFrame(diff_rows).to_csv(OUT / 'implementation_differences.csv', index=False)

# ---------------- analytic validation of the Gillespie implementation: single lineage birth-death from one cell
def analytic_bd(lam, mu, t, nmax):
    if abs(lam - mu) < 1e-12: al = be = lam * t / (1 + lam * t)
    else: e = math.exp((lam - mu) * t); al = mu * (e - 1) / (lam * e - mu); be = lam * (e - 1) / (lam * e - mu)
    n = np.arange(1, nmax + 1); pn = (1 - al) * (1 - be) * be ** (n - 1)
    return al, pn  # P0, P(N=n) n>=1
an_rows = []
for lam_, mu_, t_ in [(0.5, 0.5, 5.0), (0.7, 0.3, 5.0), (0.3, 0.7, 5.0), (2 * 13.62 / 7 * 0.5, 2 * 13.62 / 7 * 0.5, 7.0)]:
    sig = lam_ + mu_; r_ = lam_ / sig; N = 200000
    sz, _, _ = _run(2, N, 1.0, sig, r_, 0.0, 0.5, np.inf, 0.0, 0.5, 0.0, 0.5, t_, NMAX, 4242)
    p0, pn = analytic_bd(lam_, mu_, t_, NMAX); emp0 = (sz == 0).mean(); emp = np.bincount(np.minimum(sz, NMAX), minlength=NMAX + 1)[1:] / N
    cc_an = 1 - np.cumsum(pn[1:]) / pn[1:].sum(); cc_emp = ccdf_ge2(sz, NMAX); ok = ~np.isnan(cc_emp) & (pn[1:] > 1e-6)
    an_rows.append({'birth': lam_, 'death': mu_, 't': t_, 'clones': N, 'P0_analytic': p0, 'P0_empirical': float(emp0), 'max_abs_pmf_error_n1_to_50': float(np.abs(emp[:50] - pn[:50]).max()),
                    'max_abs_ccdf_ge2_error_where_P_gt_1e-6': float(np.abs(cc_emp[ok] - cc_an[ok]).max()), 'mean_analytic': float(math.exp((lam_ - mu_) * t_)), 'mean_empirical': float(sz.mean())})
pd.DataFrame(an_rows).to_csv(OUT / 'analytic_birth_death_check.csv', index=False)

# ---------------- batch1 LOMO parameter spread (saved fits; nothing refitted)
lomo = pd.read_csv(HERE / 'trials/batch1/clones/model_LOMO_by_mouse.csv'); record['inputs'] = [{'path': 'trials/batch1/clones/model_LOMO_by_mouse.csv', 'sha256': digest(HERE / 'trials/batch1/clones/model_LOMO_by_mouse.csv')}]
rows = []
for (ds, ch, sens, model), g in lomo.groupby(['dataset', 'channel', 'sensitivity', 'model']):
    P_ = np.array([json.loads(s) for s in g.parameters_json]); best = g.heldout_mean_NLL
    row = {'dataset': ds, 'channel': ch, 'sensitivity': sens, 'model': model, 'n_heldout_fits': len(g), 'heldout_mean_NLL_min': float(best.min()), 'heldout_mean_NLL_max': float(best.max()),
           'training_NLL_range': float(g.training_equal_mouse_NLL.max() - g.training_equal_mouse_NLL.min())}
    for j in range(P_.shape[1]): row[f'param{j}_min'] = float(P_[:, j].min()); row[f'param{j}_max'] = float(P_[:, j].max()); row[f'param{j}_relative_spread'] = float((P_[:, j].max() - P_[:, j].min()) / max(abs(P_[:, j].mean()), 1e-12))
    if model == 'two_shifted_geometric_mixture': row['mixture_weight_min'] = float(P_[:, 0].min()); row['mixture_weight_max'] = float(P_[:, 0].max()); row['component_geometric_params_overlap'] = bool(P_[:, 1].min() <= P_[:, 2].max() and P_[:, 2].min() <= P_[:, 1].max())
    rows.append(row)
pd.DataFrame(rows).to_csv(OUT / 'lomo_parameter_spread.csv', index=False)
record.update(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), outputs=[{'file': f.name, 'sha256': digest(f)} for f in sorted(OUT.glob('*.csv'))],
              limits=['size cap 20,000 cells per clone bounds runtime; clones hitting the cap are counted per condition', 'MATLAB RNG not reproduced; Monte Carlo seeds independent', 'no fit to data; merger/segmentation of imaged clones not modelled'])
(OUT / 'run_record.json').write_text(json.dumps(record, indent=2) + '\n'); print('EN6 completed', flush=True)
