"""Core abstractions shared by the boundary-residue modules."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence


ScalarStep = Callable[[float], float]


@dataclass(frozen=True)
class FixedPointResult:
    """Numerical fixed-point iteration result."""

    value: float
    iterations: int
    converged: bool
    delta: float


@dataclass(frozen=True)
class BoundaryResidueProfile:
    """Stable residue data for one attracting object and boundary anchor."""

    name: str
    anchor: float
    attractor: float
    residue: float
    parameter: float | None = None
    multiplier: float | None = None
    lyapunov: float | None = None

    @property
    def stable(self) -> bool | None:
        if self.multiplier is None:
            return None
        return abs(self.multiplier) < 1.0


def iterate_fixed_point(
    step: ScalarStep,
    start: float,
    *,
    tol: float = 1e-15,
    max_iter: int = 10_000,
) -> FixedPointResult:
    """Iterate ``step`` until convergence or iteration exhaustion."""

    value = float(start)
    delta = math.inf
    for iteration in range(1, max_iter + 1):
        next_value = float(step(value))
        delta = abs(next_value - value)
        value = next_value
        if delta <= tol:
            return FixedPointResult(value=value, iterations=iteration, converged=True, delta=delta)
    return FixedPointResult(value=value, iterations=max_iter, converged=False, delta=delta)


def boundary_residue(attractor: float, anchor: float) -> float:
    """Signed distance from an attractor to its reference anchor."""

    return float(attractor - anchor)


def relative_gap(lhs: float, rhs: float) -> float:
    """Relative gap using ``rhs`` as the scale."""

    if rhs == 0.0:
        raise ValueError("rhs must be non-zero for a relative gap")
    return abs(lhs - rhs) / abs(rhs)


def evaluate_series(x: float, coefficients: Sequence[float], *, constant: float = 0.0) -> float:
    """Evaluate ``constant + sum(coefficients[k-1] * x**k)``."""

    total = float(constant)
    power = float(x)
    for coefficient in coefficients:
        total += coefficient * power
        power *= x
    return total


def bisection_root(
    func: Callable[[float], float],
    lo: float,
    hi: float,
    *,
    tol: float = 1e-15,
    max_iter: int = 256,
) -> float:
    """Solve ``func(x) = 0`` on a bracket with opposite-sign endpoints."""

    f_lo = float(func(lo))
    f_hi = float(func(hi))
    if f_lo == 0.0:
        return lo
    if f_hi == 0.0:
        return hi
    if f_lo * f_hi > 0.0:
        raise ValueError("bisection_root requires a sign-changing bracket")

    left = float(lo)
    right = float(hi)
    for _ in range(max_iter):
        mid = 0.5 * (left + right)
        f_mid = float(func(mid))
        if abs(f_mid) <= tol or (right - left) <= tol:
            return mid
        if f_lo * f_mid < 0.0:
            right = mid
            f_hi = f_mid
        else:
            left = mid
            f_lo = f_mid
    return 0.5 * (left + right)


def multiplier_lyapunov(multiplier: float | None) -> float | None:
    """Local Lyapunov exponent for a fixed-point multiplier."""

    if multiplier is None:
        return None
    magnitude = abs(multiplier)
    if magnitude == 0.0:
        return float("-inf")
    return math.log(magnitude)


def make_profile(
    name: str,
    attractor: float,
    anchor: float,
    *,
    parameter: float | None = None,
    multiplier: float | None = None,
) -> BoundaryResidueProfile:
    """Build a standard residue profile object."""

    return BoundaryResidueProfile(
        name=name,
        anchor=float(anchor),
        attractor=float(attractor),
        residue=boundary_residue(attractor, anchor),
        parameter=parameter,
        multiplier=multiplier,
        lyapunov=multiplier_lyapunov(multiplier),
    )
