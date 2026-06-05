"""Collatz Bay reference constants used by the working note."""

from __future__ import annotations

import math

from .core import BoundaryResidueProfile, make_profile


COLLATZ_BAY_CONSTANT = 1.9086708647584145


def collatz_bay_log_ratio(constant: float = COLLATZ_BAY_CONSTANT) -> float:
    return math.log(2.0) / math.log(constant)


def collatz_deficit(*, anchor: float = 2.0, constant: float = COLLATZ_BAY_CONSTANT) -> float:
    return float(anchor - constant)


def collatz_profile(*, anchor: float = 2.0, constant: float = COLLATZ_BAY_CONSTANT) -> BoundaryResidueProfile:
    return make_profile(
        "collatz_bay_deficit",
        attractor=constant,
        anchor=anchor,
    )
