# boundary_systems

Mathematical visualization of fractal surfaces with overlaid path trajectories.

## Layout

- `scripts/` contains the Python source files.
- `outputs/` contains pre-rendered images and other generated artifacts.
- `notes/` contains ported working notes and research write-ups.
- `tests/` contains reproducibility and regression checks.

Two scripts render 3D scatter plots of:
- **Mandelbulb** — the power-8 3D analogue of the Mandelbrot set, sampled via an escape-time boundary search.
- **Fermat surfaces** — the real locus of `|x|^n + |y|^n + |z|^n = 1`, solved analytically.

Paths are generated from arithmetic and space-filling sequences (prime gaps, nested radicals, Hilbert curves, Fibonacci spirals) and projected onto the surfaces to study how different generative algorithms cover 3D space.

## Boundary Residue Profiles

The repo now also contains a small `boundary_residues` package for reproducing the 5 June 2026 boundary-residue note. The Phase 0 implementation focuses on the upper inverse repunit tower branch

```text
T_c(z) = c^(c^(-z))
```

and compares its residue

```text
L_tower(c) = z_+(c) - 1
```

against the Brun deficit `2 - B_2` and the Collatz Bay deficit `2 - c_*`. The code is intentionally diagnostic: it reproduces the numerical match, computes the local sensitivity and multiplier, and highlights the tunability warning instead of claiming a hidden identity.

## Files

| File | Description |
|------|-------------|
| `scripts/mandelbulb_core.py` | Shared primitives: escape test, surface sampling, signal utilities, densification |
| `scripts/mandelbulb_arithmetic_paths.py` | Z_p prime-compression and Pythagorean radical-tower paths over a Mandelbulb |
| `scripts/pathfilling.py` | Six path modes (fibonacci, hilbert, spiral, pythagorean, zp, all) over Mandelbulb or Fermat surfaces |
| `scripts/padic_drift.py` | p-adic packet drift: valuation, Teichmüller label, and drift depth over digit windows |
| `scripts/padic_viz.py` | Drift visualisation — line plot and heatmap of C_p(n, L) over prime and Pythagorean sequences |
| `scripts/boundary_residues/` | Boundary-residue package: core abstractions, tower maps, deficits, diagnostics, and a small profile registry |
| `scripts/reproduce_note.py` | Reproduce the published constants from the boundary-residue note |
| `scripts/boundary_residue_viz.py` | Generate the `L_tower(c)` curve and comparison plots |
| `notes/boundary_residue_notes.md` | Ported working note with the keep/caveat/quarantine table and numerical targets |
| `tests/test_boundary_residues.py` | Regression tests for the Phase 0 reproduction targets |

## Requirements

Python 3.10+

```bash
pip install numpy matplotlib
```

## Usage

**Boundary-residue note reproduction:**
```bash
python scripts/reproduce_note.py
python scripts/reproduce_note.py --save-plot outputs/boundary_residue_L_tower.png --no-show
python scripts/boundary_residue_viz.py --no-show
python -m unittest discover -s tests -p 'test_*.py'
```

**Arithmetic paths over a Mandelbulb:**
```bash
python scripts/mandelbulb_arithmetic_paths.py
python scripts/mandelbulb_arithmetic_paths.py --save outputs/bulb.png --no-show
python scripts/mandelbulb_arithmetic_paths.py --surface-samples 1400 --power 8
```

**Path-filling modes:**
```bash
python scripts/pathfilling.py
python scripts/pathfilling.py --path-mode hilbert --hilbert-order 5
python scripts/pathfilling.py --path-mode all --save outputs/pathfill.png --no-show
python scripts/pathfilling.py --surface-type fermat --fermat-degree 6 --path-mode all --save outputs/fermat6.png --no-show
```

Both scripts support `--help` for a full argument listing.

**p-adic packet drift:**
```bash
python scripts/padic_viz.py
python scripts/padic_viz.py --p 5 --L 4 --sequence-length 80
python scripts/padic_viz.py --p 3 --max-L 8 --save outputs/padic_drift.png --no-show
```

## Output images

Pre-rendered images are included:

| File | Description |
|------|-------------|
| `outputs/bulb.png` | Mandelbulb surface render |
| `outputs/aritmetic_paths_mandelbulbs.png` | Z_p and Pythagorean paths over a Mandelbulb |
| `outputs/fermat_paths.png` | Multiple path modes over a Fermat surface |
| `outputs/fermat_surface_hilbert.png` | Hilbert path on a Fermat surface |
| `outputs/path_filling_fermat_surface.png` | Fibonacci fill on a Fermat surface |
| `outputs/path_filling_fibonnaci.png` | Fibonacci fill on a Mandelbulb |
| `outputs/boundary_residue_L_tower.png` | Residue curve `L_tower(c)` with Brun and Collatz reference levels |
| `outputs/boundary_residue_comparison.png` | Two-panel comparison: residue curve and Phase 0 deficit bars |
