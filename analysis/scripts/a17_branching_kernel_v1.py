"""Numerical kernel for a proposed two-type branching model, not a fitted model.

Rates: fast birth, fast loss, slow birth, slow loss, fast-to-slow, slow-to-fast.
Piecewise regimes change at their specified end time. Extinction is absorbing.
Reaching a numerical cap raises, rather than inventing a terminal observation.
"""
from __future__ import annotations
import math
import random

CHANGES = ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (1, -1))

def validate_schedule(schedule):
    prior = 0.0
    if not schedule:
        raise ValueError('Empty schedule')
    for end, rates in schedule:
        if not math.isfinite(end) or end <= prior or len(rates) != 6:
            raise ValueError('Invalid regime boundary or rate dimension')
        if any(not math.isfinite(x) or x < 0 for x in rates):
            raise ValueError('Rates must be finite and nonnegative')
        prior = end

def simulate(initial, schedule, rng, cap=100000, event_limit=1000000):
    validate_schedule(schedule)
    if len(initial) != 2 or any(type(x) is not int or x < 0 for x in initial):
        raise ValueError('Initial counts must be nonnegative integers')
    if type(cap) is not int or cap < 2 or type(event_limit) is not int or event_limit < 1:
        raise ValueError('Invalid numerical limit')
    f, s = initial
    if f + s >= cap:
        raise RuntimeError('Initial size meets numerical cap')
    t, events = 0.0, 0
    for end, rates in schedule:
        while t < end and f + s:
            weights = (rates[0]*f, rates[1]*f, rates[2]*s, rates[3]*s, rates[4]*f, rates[5]*s)
            total = sum(weights)
            if not total:
                t = end
                break
            event_time = t + rng.expovariate(total)
            if event_time >= end:
                t = end
                break
            if events >= event_limit:
                raise RuntimeError('Numerical event limit reached')
            threshold, cumulative, selected = rng.random()*total, 0.0, None
            for index, weight in enumerate(weights):
                cumulative += weight
                if weight > 0 and threshold < cumulative:
                    selected = index
                    break
            if selected is None:
                raise ArithmeticError('No event selected')
            df, ds = CHANGES[selected]
            f, s = f + df, s + ds
            if min(f, s) < 0:
                raise ArithmeticError('Negative cell count')
            events += 1
            t = event_time
            if f + s >= cap:
                raise RuntimeError('Numerical size cap reached; not a censored observed size')
        t = end
    return f, s

def founder_initial(probability_fast, rng):
    if not math.isfinite(probability_fast) or not 0 <= probability_fast <= 1:
        raise ValueError('Invalid founder probability')
    return (1, 0) if rng.random() < probability_fast else (0, 1)

def birth_death_reference(birth, death, time):
    if min(birth, death, time) < 0 or not all(math.isfinite(x) for x in (birth, death, time)):
        raise ValueError('Invalid reference parameters')
    r = birth - death
    mean = math.exp(r*time)
    if abs(r) < 1e-12:
        variance = 2*birth*time
        extinction = birth*time/(1+birth*time)
    else:
        variance = (birth+death)*mean*math.expm1(r*time)/r
        extinction = death * (-math.expm1(-r*time))/(birth-death*math.exp(-r*time))
    return mean, variance, extinction

def conditional_log_score(probabilities, observed_sizes, lower=2):
    """One clone-size log score; caller must aggregate within mouse before across mice.

    Missing model mass is an error. No epsilon clipping or observed-maximum
    renormalization is permitted. This finite-support helper is for known toy
    distributions; an empirical PMF cannot substitute for model probabilities.
    """
    if not probabilities or any(n < 0 or type(n) is not int or not math.isfinite(p) or p < 0 for n,p in probabilities.items()):
        raise ValueError('Invalid probability support')
    if not math.isclose(sum(probabilities.values()), 1.0, abs_tol=1e-12, rel_tol=0):
        raise ValueError('Model probability mass must sum to one')
    if not observed_sizes or any(type(n) is not int or n < lower for n in observed_sizes):
        raise ValueError('Invalid observed support')
    normalizer = sum(p for n,p in probabilities.items() if n >= lower)
    if normalizer <= 0:
        raise ValueError('No eligible model mass')
    values = [probabilities.get(n, 0) for n in observed_sizes]
    if any(p == 0 for p in values):
        return -math.inf
    return sum(math.log(p/normalizer) for p in values)/len(values)
