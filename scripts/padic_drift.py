#!/usr/bin/env python3
"""
p-adic packet drift: Witt–Teichmüller carry diagnostics over digit windows.

For a sequence of base-p digits d_0, d_1, ..., the carry-wheel window at
rank n with length L is the integer packet:

    W(n, L, p) = sum_{j=0}^{L-1} d[n+j] * p^j

The carry-wheel diagnostic triple at rank n is:

    C_p(n, L) = (carry_depth, teichmuller_label, drift_depth)

where, writing U = W / p^{v_p(W)} for the unit part:

  carry_depth      r = v_p(W)
                   — pure p-power divisibility depth

  teichmuller      omega = U mod p   (odd p: element of {1, ..., p-1})
                   sigma = ±1        (p=2: sign from U mod 4)
                   — Teichmüller residue label

  drift_depth      Δ = v_p(U^{p-1} - 1)             (odd p)
                   Δ = v_2(U-1) or v_2(U+1)          (p=2, by sign)
                   — principal-unit drift after Teichmüller label is stripped

  norm             D = p^{-Δ}
                   — p-adic size of the drift

Interpretation
--------------
Large Δ  →  small drift  →  stable packet (U close to its Teichmüller rep)
Small Δ  →  large drift  →  unstable packet (Δ=1 is the worst possible for odd p)

Reference: teichmuller_carry_drift.md in the repo root.
"""

from __future__ import annotations

from dataclasses import dataclass

_LARGE_DEPTH = 30  # cap returned when unit part is trivially 1 (drift = 0 / depth = ∞)


# ---------------------------------------------------------------------------
# Core arithmetic
# ---------------------------------------------------------------------------

def p_adic_valuation(x: int, p: int) -> int:
    """Largest k such that p^k divides x. Returns 0 if x == 0 (convention)."""
    if x == 0:
        return 0
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k


def teichmuller_label(u: int, p: int) -> int:
    """
    Teichmüller representative of the p-adic unit u.

    Odd p: u mod p, in {1, ..., p-1}.
    p=2:  +1 if u ≡ 1 (mod 4),  -1 if u ≡ 3 (mod 4).
    """
    if p == 2:
        return 1 if u % 4 == 1 else -1
    return u % p


def drift_depth(u: int, p: int, max_depth: int = _LARGE_DEPTH) -> int:
    """
    Principal-unit drift depth Δ_p of the p-adic unit u.

    Odd p:  Δ = v_p(u^{p-1} - 1).
            Computed via modular exponentiation to avoid large integers.
    p=2:    Δ = v_2(u - 1)  if u ≡ 1 (mod 4)
              = v_2(u + 1)  if u ≡ 3 (mod 4)

    Returns max_depth when u == 1 (drift is zero; depth is infinite).
    """
    if u % p == 0:
        raise ValueError(f"u={u} is not a p-adic unit (divisible by {p}).")
    if u == 1:
        return max_depth
    if p == 2:
        return p_adic_valuation(u - 1, 2) if u % 4 == 1 else p_adic_valuation(u + 1, 2)
    # Odd p: find largest k with p^k | u^{p-1} - 1 using pow(u, p-1, p^k).
    depth = 0
    pk = 1
    for k in range(1, max_depth + 1):
        pk *= p
        if pow(u, p - 1, pk) != 1:
            return depth
        depth = k
    return depth


# ---------------------------------------------------------------------------
# Window packet and diagnostic
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CarryDiagnostic:
    """Full carry-wheel diagnostic triple C_p(n, L)."""
    n: int            # window start rank
    L: int            # window length
    p: int            # base / prime
    packet: int       # W_{n,L}^{(p)}
    carry_depth: int  # r = v_p(W)
    teichmuller: int  # omega_p(U) — residue label or sign
    drift: int        # Δ_p(n, L) — principal-unit drift depth
    norm: float       # D_p = p^{-Δ}


def window_packet(digits: list[int], n: int, L: int, p: int) -> int:
    """W_{n,L}^{(p)} = sum_{j=0}^{L-1} digits[n+j] * p^j."""
    total = 0
    pk = 1
    for j in range(L):
        total += digits[n + j] * pk
        pk *= p
    return total


def carry_diagnostic(
    digits: list[int], n: int, L: int, p: int
) -> CarryDiagnostic | None:
    """
    Compute the full diagnostic triple at rank n.
    Returns None when n+L exceeds the sequence length or the packet is 0.
    """
    if n + L > len(digits):
        return None
    w = window_packet(digits, n, L, p)
    if w == 0:
        return None
    r = p_adic_valuation(w, p)
    u = w // (p ** r)
    omega = teichmuller_label(u, p)
    delta = drift_depth(u, p)
    return CarryDiagnostic(
        n=n,
        L=L,
        p=p,
        packet=w,
        carry_depth=r,
        teichmuller=omega,
        drift=delta,
        norm=float(p) ** (-delta),
    )


def scan_drift(digits: list[int], L: int, p: int) -> list[CarryDiagnostic]:
    """Slide the length-L window across all valid positions and return diagnostics."""
    result = []
    for n in range(len(digits) - L + 1):
        d = carry_diagnostic(digits, n, L, p)
        if d is not None:
            result.append(d)
    return result


# ---------------------------------------------------------------------------
# Digit-sequence helpers
# ---------------------------------------------------------------------------

def int_to_base_digits(x: int, p: int) -> list[int]:
    """Base-p digit expansion of x, least-significant first."""
    if x == 0:
        return [0]
    digits: list[int] = []
    while x > 0:
        digits.append(x % p)
        x //= p
    return digits


def sequence_to_digits(values: list[int], p: int) -> list[int]:
    """Concatenate the base-p digit expansions of a list of non-negative integers."""
    result: list[int] = []
    for v in values:
        result.extend(int_to_base_digits(abs(v), p))
    return result
