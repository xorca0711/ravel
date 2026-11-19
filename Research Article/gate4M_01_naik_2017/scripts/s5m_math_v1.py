"""Finite-feature association arithmetic; no population inference."""
import numpy as np


def average_ranks(values):
    x = np.asarray(values, dtype=float)
    if not np.isfinite(x).all(): raise ValueError('nonfinite rank input')
    order = np.argsort(x, kind='stable'); ordered = x[order]
    starts = np.r_[0, np.flatnonzero(ordered[1:] != ordered[:-1]) + 1]
    ends = np.r_[starts[1:], len(x)]
    result = np.empty(len(x)); result[order] = np.repeat((starts + ends + 1) / 2, ends - starts)
    return result


def moments(x, y, weights=None):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    w = np.ones(len(x)) if weights is None else np.asarray(weights, dtype=float)
    if len(x) != len(y) or len(w) != len(x) or not np.isfinite(x).all() or not np.isfinite(y).all() or not np.isfinite(w).all() or (w <= 0).any():
        raise ValueError('invalid association inputs')
    if len(x) < 2: return dict(coefficient=None, covariance=None, variance_x=None, variance_y=None, reason='fewer_than_two_features')
    dx, dy = x - np.average(x, weights=w), y - np.average(y, weights=w)
    covariance = float(np.average(dx * dy, weights=w)); vx = float(np.average(dx * dx, weights=w)); vy = float(np.average(dy * dy, weights=w))
    constant_x, constant_y = bool(np.all(x == x[0])), bool(np.all(y == y[0]))
    if constant_x: vx, covariance = 0.0, 0.0
    if constant_y: vy, covariance = 0.0, 0.0
    reason = 'constant_x_and_y' if constant_x and constant_y else ('constant_x' if constant_x else ('constant_y' if constant_y else 'defined'))
    coefficient = None if reason != 'defined' else covariance / np.sqrt(vx * vy)
    if coefficient is not None:
        assert abs(coefficient) <= 1 + 1e-12
        coefficient = float(coefficient)
    return dict(coefficient=coefficient, covariance=covariance, variance_x=vx, variance_y=vy, reason=reason)
