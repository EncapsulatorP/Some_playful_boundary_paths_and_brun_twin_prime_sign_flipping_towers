"""Constructive tower solver and a provisional Rudin-Shapiro research adapter.

The adapter uses the classical P,Q recurrence. It does not assert that the
user's still unspecified 'Shapiro outliers' are this particular object.
Floating point results are not outward-rounded certificates.
"""
import math

UNIFORM_CONTRACTION_BOUND = 4 * math.exp(1/math.e - 2)


def solve_real_signflip(base, *, tolerance=1e-12, max_iterations=10000):
    """Unique real upper branch for base > 1; see notes/real_tower_theorem.md."""
    if isinstance(base, bool):
        raise ValueError("base must be a real number greater than 1")
    base = float(base)
    if not math.isfinite(base) or base <= 1:
        raise ValueError("base must be finite and greater than 1")
    if not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if not isinstance(max_iterations, int) or isinstance(max_iterations, bool) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    log_base, value = math.log(base), 1.0
    q = UNIFORM_CONTRACTION_BOUND
    for iteration in range(1, max_iterations + 1):
        next_value = math.exp(log_base * math.exp(-log_base * value))
        iteration_bound = q / (1-q) * abs(next_value-value)
        value = next_value
        if iteration_bound <= tolerance:
            break
    if iteration_bound > tolerance:
        raise ArithmeticError("fixed-point iteration budget exhausted")
    return {"upper": value, "lower": math.exp(-log_base*value),
            "iterations": iteration, "converged": iteration_bound <= tolerance,
            "exact_arithmetic_iteration_bound_estimate": iteration_bound,
            "rounding_error_included": False, "certified": False}


def _check_level(level):
    if not isinstance(level, int) or isinstance(level, bool) or not 0 <= level <= 18:
        raise ValueError("level must be an integer in [0,18]")


def rudin_shapiro_pair(level):
    """Return exact integer coefficient tuples (ascending degree), P_0=Q_0=1.

    P_(k+1)=P_k+z^(2^k) Q_k; Q_(k+1)=P_k-z^(2^k) Q_k.
    """
    _check_level(level)
    p = q = (1,)
    for _ in range(level):
        p, q = p+q, p+tuple(-a for a in q)
    return p, q


def evaluate_rudin_shapiro_pair(level, z):
    """O(level) arithmetic operations per point; floating evaluation."""
    _check_level(level)
    p = q = 1+0j
    power = complex(z)
    for _ in range(level):
        p, q = p+power*q, p-power*q
        power *= power
    return p, q
