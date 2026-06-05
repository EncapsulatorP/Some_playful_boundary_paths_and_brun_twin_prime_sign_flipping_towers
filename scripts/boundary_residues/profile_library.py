"""Small registry of reproducible residue profiles."""

from __future__ import annotations

from collections.abc import Iterable

from .brun_bridge import brun_profile
from .collatz_bay import collatz_profile
from .core import BoundaryResidueProfile, make_profile
from .diagnostics import stability_bundle
from .repunit_tower import DEFAULT_BASE, upper_fixed_point


def repunit_upper_profile(c: float = DEFAULT_BASE) -> BoundaryResidueProfile:
    upper = upper_fixed_point(c).value
    bundle = stability_bundle(c, upper)
    return make_profile(
        "repunit_upper_tower",
        attractor=upper,
        anchor=1.0,
        parameter=c,
        multiplier=bundle.multiplier,
    )


REGISTRY = {
    "repunit_upper_tower": repunit_upper_profile,
    "brun_deficit": brun_profile,
    "collatz_bay_deficit": collatz_profile,
}


def compute_profiles(
    names: Iterable[str] | None = None,
    *,
    tower_base: float = DEFAULT_BASE,
) -> list[BoundaryResidueProfile]:
    selected = list(names) if names is not None else list(REGISTRY)
    profiles: list[BoundaryResidueProfile] = []
    for name in selected:
        if name not in REGISTRY:
            raise KeyError(f"Unknown profile '{name}'")
        if name == "repunit_upper_tower":
            profiles.append(REGISTRY[name](tower_base))
        else:
            profiles.append(REGISTRY[name]())
    return profiles
