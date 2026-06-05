"""Boundary-residue diagnostics for iterative maps and anchor deficits."""

from .brun_bridge import BRUN_ESTIMATE, brun_deficit, brun_profile
from .collatz_bay import COLLATZ_BAY_CONSTANT, collatz_deficit, collatz_profile
from .core import BoundaryResidueProfile, FixedPointResult
from .diagnostics import (
    StabilityBundle,
    solve_base_for_target_residue,
    stability_bundle,
    tower_residue_derivative,
)
from .profile_library import compute_profiles
from .repunit_tower import (
    lower_fixed_point,
    tower_residue,
    tower_residue_series,
    upper_fixed_point,
    upper_fixed_point_series,
)

__all__ = [
    "BRUN_ESTIMATE",
    "COLLATZ_BAY_CONSTANT",
    "BoundaryResidueProfile",
    "FixedPointResult",
    "StabilityBundle",
    "brun_deficit",
    "brun_profile",
    "collatz_deficit",
    "collatz_profile",
    "compute_profiles",
    "lower_fixed_point",
    "solve_base_for_target_residue",
    "stability_bundle",
    "tower_residue",
    "tower_residue_derivative",
    "tower_residue_series",
    "upper_fixed_point",
    "upper_fixed_point_series",
]
