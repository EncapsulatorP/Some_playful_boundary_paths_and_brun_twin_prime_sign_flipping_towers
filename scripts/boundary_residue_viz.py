#!/usr/bin/env python3
"""Plot boundary-residue curves and the Phase 0 comparison panel."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path

import numpy as np

if "MPLCONFIGDIR" not in os.environ:
    mpl_dir = Path(tempfile.gettempdir()) / "boundary_residue_mplconfig"
    mpl_dir.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(mpl_dir)

if not os.environ.get("DISPLAY") and os.name != "nt":
    import matplotlib

    matplotlib.use("Agg")

import matplotlib.pyplot as plt

from boundary_residues.brun_bridge import brun_deficit
from boundary_residues.collatz_bay import collatz_deficit
from boundary_residues.diagnostics import solve_base_for_target_residue
from boundary_residues.repunit_tower import DEFAULT_BASE, tower_residue


def compute_residue_curve(c_min: float, c_max: float, samples: int) -> tuple[np.ndarray, np.ndarray]:
    cs = np.linspace(c_min, c_max, samples)
    residues = np.array([tower_residue(c) for c in cs], dtype=float)
    return cs, residues


def plot_curve_axes(ax: plt.Axes, c_min: float, c_max: float, samples: int) -> None:
    cs, residues = compute_residue_curve(c_min, c_max, samples)
    brun_level = brun_deficit()
    collatz_level = collatz_deficit()
    crossing = solve_base_for_target_residue(brun_level, c_min=c_min, c_max=c_max)

    ax.set_facecolor("#f6f1e8")
    ax.plot(cs, residues, color="#204b57", linewidth=2.3, label=r"$L_{tower}(c)$")
    ax.axhline(brun_level, color="#cc6f30", linewidth=1.5, linestyle="--", label=r"$L_{Brun}$")
    ax.axhline(
        collatz_level,
        color="#7d8c4f",
        linewidth=1.5,
        linestyle=":",
        label=r"$L_{Collatz}$",
    )
    ax.scatter([DEFAULT_BASE], [tower_residue(DEFAULT_BASE)], color="#17313b", s=45, zorder=3)
    ax.scatter([crossing], [brun_level], color="#cc6f30", s=50, zorder=4)
    ax.annotate(
        f"crossing c = {crossing:.12f}",
        xy=(crossing, brun_level),
        xytext=(10, 10),
        textcoords="offset points",
        fontsize=9,
        color="#5d2c13",
    )
    ax.annotate(
        f"c = {DEFAULT_BASE:.2f}",
        xy=(DEFAULT_BASE, tower_residue(DEFAULT_BASE)),
        xytext=(10, -15),
        textcoords="offset points",
        fontsize=9,
        color="#17313b",
    )

    ax.set_title("Boundary Residue Profile of the Inverse Repunit Tower")
    ax.set_xlabel("tower base c")
    ax.set_ylabel("residue")
    ax.grid(alpha=0.18, color="#5f5f5f", linewidth=0.8)
    ax.legend(frameon=False)


def make_curve_figure(c_min: float, c_max: float, samples: int) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8.5, 5.2), constrained_layout=True)
    fig.patch.set_facecolor("#fbfaf7")
    plot_curve_axes(ax, c_min, c_max, samples)
    return fig


def make_comparison_figure() -> plt.Figure:
    tower_level = tower_residue(DEFAULT_BASE)
    brun_level = brun_deficit()
    collatz_level = collatz_deficit()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), constrained_layout=True)
    fig.patch.set_facecolor("#fbfaf7")

    curve_ax, bar_ax = axes
    plot_curve_axes(curve_ax, 1.06, 1.16, 240)

    bar_ax.set_facecolor("#f6f1e8")
    labels = ["Tower", "Brun", "Collatz"]
    values = [tower_level, brun_level, collatz_level]
    colors = ["#204b57", "#cc6f30", "#7d8c4f"]
    bar_ax.bar(labels, values, color=colors, width=0.62)
    bar_ax.set_title("Boundary Residue Comparison")
    bar_ax.set_ylabel("residue")
    for idx, value in enumerate(values):
        bar_ax.text(idx, value + 0.0015, f"{value:.6f}", ha="center", va="bottom", fontsize=9)
    bar_ax.set_ylim(0.0, max(values) + 0.02)
    bar_ax.grid(axis="y", alpha=0.18, color="#5f5f5f", linewidth=0.8)
    return fig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot residue curves from the boundary-residue note.")
    parser.add_argument("--c-min", type=float, default=1.06, help="Minimum c value for the curve.")
    parser.add_argument("--c-max", type=float, default=1.16, help="Maximum c value for the curve.")
    parser.add_argument("--samples", type=int, default=240, help="Number of c samples on the curve.")
    parser.add_argument(
        "--save-curve",
        type=Path,
        default=Path("outputs/boundary_residue_L_tower.png"),
        help="Output path for the L_tower(c) curve.",
    )
    parser.add_argument(
        "--save-comparison",
        type=Path,
        default=Path("outputs/boundary_residue_comparison.png"),
        help="Output path for the comparison figure.",
    )
    parser.add_argument("--dpi", type=int, default=180, help="Saved image DPI.")
    parser.add_argument("--no-show", action="store_true", help="Do not open interactive windows.")
    return parser.parse_args()


def maybe_show(no_show: bool) -> None:
    if not no_show:
        plt.show()


def main() -> None:
    args = parse_args()

    curve_fig = make_curve_figure(args.c_min, args.c_max, args.samples)
    curve_fig.savefig(args.save_curve, dpi=args.dpi, facecolor=curve_fig.get_facecolor())

    comparison_fig = make_comparison_figure()
    comparison_fig.savefig(
        args.save_comparison,
        dpi=args.dpi,
        facecolor=comparison_fig.get_facecolor(),
    )

    maybe_show(args.no_show)
    plt.close(curve_fig)
    plt.close(comparison_fig)


if __name__ == "__main__":
    main()
