#!/usr/bin/env python3
"""Reproduce the published values from the boundary-residue working note."""

from __future__ import annotations

import argparse
from pathlib import Path

from boundary_residue_viz import make_curve_figure
from boundary_residues.brun_bridge import BRUN_ESTIMATE, brun_deficit
from boundary_residues.collatz_bay import (
    COLLATZ_BAY_CONSTANT,
    collatz_bay_log_ratio,
    collatz_deficit,
)
from boundary_residues.core import relative_gap
from boundary_residues.diagnostics import solve_base_for_target_residue, stability_bundle, tower_residue_derivative
from boundary_residues.repunit_tower import (
    DEFAULT_BASE,
    lower_fixed_point,
    tower_residue,
    tower_residue_series,
    upper_fixed_point,
    upper_fixed_point_series,
)


def format_float(value: float) -> str:
    return f"{value:.16f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reproduce the note's boundary-residue constants.")
    parser.add_argument("--c", type=float, default=DEFAULT_BASE, help="Base c for the inverse tower.")
    parser.add_argument(
        "--save-plot",
        type=Path,
        default=None,
        help="Optional path for the L_tower(c) curve.",
    )
    parser.add_argument("--dpi", type=int, default=180, help="Saved image DPI.")
    parser.add_argument("--no-show", action="store_true", help="Do not open the plot window.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    c = args.c

    lower = lower_fixed_point(c)
    upper = upper_fixed_point(c)
    residue = tower_residue(c)
    brun_gap = brun_deficit()
    collatz_gap = collatz_deficit()
    bundle = stability_bundle(c, upper.value)
    tuned_c = solve_base_for_target_residue(brun_gap)
    sensitivity = tower_residue_derivative(c, upper.value)
    upper_series = upper_fixed_point_series(c)
    residue_series = tower_residue_series(c)

    print("Boundary Residue Notes Reproduction")
    print(f"base c = {c:.16f}")
    print(f"lower branch y_- = {format_float(lower.value)}")
    print(f"upper branch z_+ = {format_float(upper.value)}")
    print(f"L_tower(c) = {format_float(residue)}")
    print(f"L_tower series(c) = {format_float(residue_series)}")
    print(f"z_+ series(c) = {format_float(upper_series)}")
    print()
    print(f"Brun estimate B2 = {format_float(BRUN_ESTIMATE)}")
    print(f"L_Brun = {format_float(brun_gap)}")
    print(f"Collatz Bay constant c* = {format_float(COLLATZ_BAY_CONSTANT)}")
    print(f"log(2) / log(c*) = {format_float(collatz_bay_log_ratio())}")
    print(f"L_Collatz = {format_float(collatz_gap)}")
    print()
    print(f"L_tower(c) - L_Brun = {format_float(residue - brun_gap)}")
    print(f"relative gap = {relative_gap(residue, brun_gap):.6f}")
    print(f"tuned c for Brun match = {format_float(tuned_c)}")
    print(f"dL_tower/dc at c = {sensitivity:.6f}")
    print(f"fixed-point multiplier = {bundle.multiplier:.6f}")
    print(f"|multiplier| = {bundle.abs_multiplier:.6f}")
    print(f"local Lyapunov exponent = {bundle.lyapunov:.6f}")

    if args.save_plot is not None:
        fig = make_curve_figure(1.06, 1.16, 240)
        fig.savefig(args.save_plot, dpi=args.dpi, facecolor=fig.get_facecolor())
        if not args.no_show:
            from matplotlib import pyplot as plt

            plt.show()


if __name__ == "__main__":
    main()
