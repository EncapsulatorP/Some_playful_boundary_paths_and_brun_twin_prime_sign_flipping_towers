"""Repunit inverse-tower fixed points and residue expansions."""

from __future__ import annotations

import math

from .core import FixedPointResult, evaluate_series, iterate_fixed_point


DEFAULT_BASE = 1.11
SERIES_COEFFICIENTS = (1.0, -0.5, -4.0 / 3.0, 7.0 / 8.0, 14.0 / 5.0)


def log_base(c: float) -> float:
    if isinstance(c, bool) or not math.isfinite(float(c)) or float(c) <= 1:
        raise ValueError("base must be finite and greater than 1")
    return math.log(float(c))


def lower_step(c: float, y: float) -> float:
    L = log_base(c)
    if not math.isfinite(y) or not 0 <= y <= 1:
        raise ValueError("lower-branch state must lie in [0,1]")
    return math.exp(-L * math.exp(L * y))


def upper_step(c: float, z: float) -> float:
    L = log_base(c)
    if not math.isfinite(z) or z < 1:
        raise ValueError("upper-branch state must be finite and >= 1")
    return math.exp(L * math.exp(-L * z))


def lower_fixed_point(
    c: float,
    *,
    start: float = 1.0,
    tol: float = 1e-15,
    max_iter: int = 10_000,
) -> FixedPointResult:
    return iterate_fixed_point(
        lambda y: lower_step(c, y),
        start,
        tol=tol,
        max_iter=max_iter,
    )


def upper_fixed_point(
    c: float,
    *,
    start: float = 1.0,
    tol: float = 1e-15,
    max_iter: int = 10_000,
) -> FixedPointResult:
    return iterate_fixed_point(
        lambda z: upper_step(c, z),
        start,
        tol=tol,
        max_iter=max_iter,
    )


def tower_residue(c: float) -> float:
    result = upper_fixed_point(c)
    if not result.converged:
        raise ArithmeticError("tower fixed point did not converge")
    return result.value - 1.0


def upper_fixed_point_series(c: float, *, order: int = 5) -> float:
    if order < 0 or order > len(SERIES_COEFFICIENTS):
        raise ValueError(f"order must be between 0 and {len(SERIES_COEFFICIENTS)}")
    return evaluate_series(log_base(c), SERIES_COEFFICIENTS[:order], constant=1.0)


def tower_residue_series(c: float, *, order: int = 5) -> float:
    return upper_fixed_point_series(c, order=order) - 1.0
