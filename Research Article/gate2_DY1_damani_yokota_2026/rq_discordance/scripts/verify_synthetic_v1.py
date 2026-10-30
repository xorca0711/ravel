"""Analytic verification; no random draws and no simulated probability reuse."""
import math
from statistics import NormalDist


def expectations(scenario, alpha):
    cdf = NormalDist().cdf
    cutoff = NormalDist().inv_cdf(1 - alpha / 2)
    signal_a = scenario['truth_a'] / scenario['se_a']
    signal_b = scenario['truth_b'] / scenario['se_b']
    detect_a = cdf(-cutoff - signal_a) + 1 - cdf(cutoff - signal_a)
    detect_b = cdf(-cutoff - signal_b) + 1 - cdf(cutoff - signal_b)
    positive_a, positive_b = cdf(signal_a), cdf(signal_b)
    same = positive_a * positive_b + (1 - positive_a) * (1 - positive_b)
    return dict(
        detect_a=detect_a, detect_b=detect_b,
        both_detect=detect_a * detect_b,
        only_a=detect_a * (1 - detect_b), only_b=(1 - detect_a) * detect_b,
        neither_detect=(1 - detect_a) * (1 - detect_b),
        detection_label_mismatch=detect_a * (1 - detect_b) + (1 - detect_a) * detect_b,
        same_sign=same, opposite_sign=1 - same,
        coverage_a=1 - alpha, coverage_b=1 - alpha)


def verify(config, rows, events):
    results = []
    exact = []
    for scenario, row in zip(config['scenarios'], rows, strict=True):
        expected = expectations(scenario, config['alpha'])
        n = config['draws_per_scenario']
        for event, probability in expected.items():
            observed = next(x for x in events if x['scenario'] == scenario['id'] and x['event'] == event)
            tolerance = config['monte_carlo_standard_errors'] * math.sqrt(probability * (1 - probability) / n) + config['monte_carlo_count_allowance'] / n
            error = abs(observed['fraction'] - probability)
            results.append(dict(scenario=scenario['id'], check=event, passed=error <= tolerance, error=error, tolerance=tolerance))
            exact.append(dict(scenario=scenario['id'], event=event, expected_probability=probability, monte_carlo_tolerance=tolerance))
        for assay in ['a', 'b']:
            mean_error = abs(row['mean_' + assay] - scenario['truth_' + assay])
            mean_tolerance = config['monte_carlo_standard_errors'] * scenario['se_' + assay] / math.sqrt(n)
            results.append(dict(scenario=scenario['id'], check='mean_' + assay, passed=mean_error <= mean_tolerance, error=mean_error, tolerance=mean_tolerance))
            expected_width = 2 * NormalDist().inv_cdf(1 - config['alpha'] / 2) * scenario['se_' + assay]
            results.append(dict(scenario=scenario['id'], check='interval_width_' + assay, passed=math.isclose(row['ci_width_' + assay], expected_width, rel_tol=1e-12), expected=expected_width))
    return exact, dict(ok=all(x['passed'] for x in results), checks=results,
        method='Independent normal-CDF probabilities and known-SE interval widths; six binomial standard errors plus two counts for each event. Same synthetic specification, not biological replication.')
