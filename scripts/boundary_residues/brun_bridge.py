"""Static Brun reference values used by the note reproduction scripts."""

from __future__ import annotations

from .core import BoundaryResidueProfile, make_profile


BRUN_ESTIMATE = 1.902160583104


def brun_deficit(*, anchor: float = 2.0, brun_constant: float = BRUN_ESTIMATE) -> float:
    return float(anchor - brun_constant)


def brun_profile(*, anchor: float = 2.0, brun_constant: float = BRUN_ESTIMATE) -> BoundaryResidueProfile:
    return make_profile(
        "brun_deficit",
        attractor=brun_constant,
        anchor=anchor,
    )
