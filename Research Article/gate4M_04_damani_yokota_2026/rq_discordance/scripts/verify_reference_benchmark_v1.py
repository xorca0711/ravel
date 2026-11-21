"""Scalar arithmetic checks of prespecified feature positions; shared source parser."""
import itertools
import math
import statistics
from scipy.stats import t


def scalar_intervals(a, b, level, se_tolerance=1e-12):
    delta = statistics.fmean(b) - statistics.fmean(a)
    va, vb = statistics.variance(a), statistics.variance(b)
    qa, qb = va / len(a), vb / len(b)
    se = math.sqrt(qa + qb)
    if se > se_tolerance:
        df = (qa + qb) ** 2 / (qa * qa / (len(a) - 1) + qb * qb / (len(b) - 1))
        half = t.ppf((1 + level) / 2, df) * se
        lo, hi = delta - half, delta + half
    else: lo = hi = float('nan')
    lower, upper, paired_ses = [], [], []
    degenerate = 0
    for order in itertools.permutations(range(len(a))):
        differences = [b[i] - a[order[i]] for i in range(len(a))]
        pair_se = statistics.stdev(differences) / math.sqrt(len(a))
        paired_ses.append(pair_se)
        if pair_se <= se_tolerance: degenerate += 1; continue
        half = t.ppf((1 + level) / 2, len(a) - 1) * pair_se
        lower.append(delta - half); upper.append(delta + half)
    pair_lo = min(lower) if lower else float('nan'); pair_hi = max(upper) if upper else float('nan')
    return dict(mean_delta=delta, control_sd=math.sqrt(va), condition_sd=math.sqrt(vb),
        welch_lower=lo, welch_upper=hi, paired_lower_min=pair_lo, paired_upper_max=pair_hi,
        paired_se_min=min(paired_ses), paired_se_max=max(paired_ses), paired_degenerate_models=degenerate)


def verify_features(counts, totals, controls, treated, results, offset, level, positions, se_tolerance=1e-12):
    checks = []
    for position in positions:
        transformed = [math.log2(offset + 1e6 * int(counts[position, j]) / int(totals[j])) for j in range(counts.shape[1])]
        a, b = [transformed[j] for j in controls], [transformed[j] for j in treated]
        expected = scalar_intervals(a, b, level, se_tolerance)
        observed = results.iloc[position]
        for name, value in expected.items():
            actual = float(observed[name])
            passed = (math.isnan(value) and math.isnan(actual)) or math.isclose(value, actual, rel_tol=2e-8, abs_tol=2e-10)
            checks.append(dict(position=int(position), field=name, passed=passed, expected=value if math.isfinite(value) else None, actual=actual if math.isfinite(actual) else None))
    return checks
