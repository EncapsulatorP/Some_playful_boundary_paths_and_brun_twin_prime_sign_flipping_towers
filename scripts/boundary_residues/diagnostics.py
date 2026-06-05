"""Sensitivity, stability, and tuning utilities for residue profiles."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .core import bisection_root
from .repunit_tower import tower_residue, upper_fixed_point


@dataclass(frozen=True)
class StabilityBundle:
    multiplier: float
    abs_multiplier: float
    lyapunov: float
    convergence_ratio: float


def upper_multiplier(c: float, z: float | None = None) -> float:
    if z is None:
        z = upper_fixed_point(c).value
    log_c = math.log(c)
    return -z * (log_c**2) * math.exp(-log_c * z)


def tower_residue_derivative(c: float, z: float | None = None) -> float:
    """
    Analytic derivative of ``L_tower(c) = z_+(c) - 1`` with respect to ``c``.

    The fixed point solves ``z = exp(L * exp(-L z))`` for ``L = log(c)``.
    Differentiating implicitly yields the closed form used here.
    """

    if z is None:
        z = upper_fixed_point(c).value
    log_c = math.log(c)
    alpha = z * math.exp(-log_c * z)
    dz_dlogc = alpha * (1.0 - log_c * z) / (1.0 + alpha * log_c * log_c)
    return dz_dlogc / c


def stability_bundle(c: float, z: float | None = None) -> StabilityBundle:
    multiplier = upper_multiplier(c, z)
    abs_multiplier = abs(multiplier)
    lyapunov = float("-inf") if abs_multiplier == 0.0 else math.log(abs_multiplier)
    return StabilityBundle(
        multiplier=multiplier,
        abs_multiplier=abs_multiplier,
        lyapunov=lyapunov,
        convergence_ratio=abs_multiplier,
    )


def solve_base_for_target_residue(
    target_residue: float,
    *,
    c_min: float = 1.01,
    c_max: float = 1.25,
    samples: int = 256,
    tol: float = 1e-15,
) -> float:
    """
    Solve ``L_tower(c) = target_residue`` on a nearby positive interval.

    The bracket is found by scanning for a sign change before bisection.
    """

    if c_min <= 1.0:
        raise ValueError("c_min must be greater than 1.0")
    if c_max <= c_min:
        raise ValueError("c_max must be greater than c_min")

    def objective(c: float) -> float:
        return tower_residue(c) - target_residue

    prev_c = c_min
    prev_v = objective(prev_c)
    if prev_v == 0.0:
        return prev_c

    step = (c_max - c_min) / samples
    for idx in range(1, samples + 1):
        current_c = c_min + idx * step
        current_v = objective(current_c)
        if current_v == 0.0 or prev_v * current_v < 0.0:
            return bisection_root(
                objective,
                prev_c,
                current_c,
                tol=tol,
            )
        prev_c = current_c
        prev_v = current_v

    raise ValueError("Could not bracket the target residue in the requested interval")
