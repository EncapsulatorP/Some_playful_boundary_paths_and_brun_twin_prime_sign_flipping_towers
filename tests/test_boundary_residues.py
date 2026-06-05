from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


from boundary_residues.brun_bridge import BRUN_ESTIMATE, brun_deficit
from boundary_residues.collatz_bay import COLLATZ_BAY_CONSTANT, collatz_bay_log_ratio, collatz_deficit
from boundary_residues.diagnostics import solve_base_for_target_residue, stability_bundle, tower_residue_derivative
from boundary_residues.profile_library import compute_profiles
from boundary_residues.repunit_tower import DEFAULT_BASE, lower_fixed_point, tower_residue, tower_residue_series, upper_fixed_point


class BoundaryResidueTests(unittest.TestCase):
    def test_repunit_fixed_points_match_note(self) -> None:
        lower = lower_fixed_point(DEFAULT_BASE)
        upper = upper_fixed_point(DEFAULT_BASE)
        self.assertTrue(lower.converged)
        self.assertTrue(upper.converged)
        self.assertAlmostEqual(lower.value, 0.8917774506448141)
        self.assertAlmostEqual(upper.value, 1.0975340696153890)
        self.assertAlmostEqual(tower_residue(DEFAULT_BASE), 0.0975340696153890)

    def test_series_tracks_numeric_branch(self) -> None:
        self.assertAlmostEqual(
            tower_residue_series(DEFAULT_BASE),
            tower_residue(DEFAULT_BASE),
            delta=5e-6,
        )

    def test_reference_deficits_match_note(self) -> None:
        self.assertAlmostEqual(BRUN_ESTIMATE, 1.9021605831040000)
        self.assertAlmostEqual(brun_deficit(), 0.0978394168960000)
        self.assertAlmostEqual(COLLATZ_BAY_CONSTANT, 1.9086708647584145)
        self.assertAlmostEqual(collatz_deficit(), 0.0913291352415855)
        self.assertAlmostEqual(collatz_bay_log_ratio(), 1.07230747, places=8)

    def test_tunability_solver_and_sensitivity_match_note(self) -> None:
        target = brun_deficit()
        tuned_c = solve_base_for_target_residue(target)
        sensitivity = tower_residue_derivative(DEFAULT_BASE)
        self.assertAlmostEqual(tuned_c, 1.1103954628296591)
        self.assertAlmostEqual(sensitivity, 0.772531, places=6)

    def test_stability_bundle_is_attracting(self) -> None:
        bundle = stability_bundle(DEFAULT_BASE)
        self.assertLess(bundle.abs_multiplier, 1.0)
        self.assertLess(bundle.lyapunov, 0.0)

    def test_profile_library_contains_phase_zero_entries(self) -> None:
        profiles = compute_profiles()
        self.assertEqual(
            [profile.name for profile in profiles],
            ["repunit_upper_tower", "brun_deficit", "collatz_bay_deficit"],
        )


if __name__ == "__main__":
    unittest.main()
