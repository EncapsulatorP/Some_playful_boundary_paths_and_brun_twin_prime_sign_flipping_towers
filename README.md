# boundary_systems

Mathematical visualization of fractal surfaces with overlaid path trajectories.

## Layout

- `scripts/` contains the Python source files.
- `outputs/` contains pre-rendered images and other generated artifacts.

Two scripts render 3D scatter plots of:
- **Mandelbulb** — the power-8 3D analogue of the Mandelbrot set, sampled via an escape-time boundary search.
- **Fermat surfaces** — the real locus of `|x|^n + |y|^n + |z|^n = 1`, solved analytically.

Paths are generated from arithmetic and space-filling sequences (prime gaps, nested radicals, Hilbert curves, Fibonacci spirals) and projected onto the surfaces to study how different generative algorithms cover 3D space.

## Files

| File | Description |
|------|-------------|
| `scripts/mandelbulb_core.py` | Shared primitives: escape test, surface sampling, signal utilities, densification |
| `scripts/mandelbulb_arithmetic_paths.py` | Z_p prime-compression and Pythagorean radical-tower paths over a Mandelbulb |
| `scripts/pathfilling.py` | Six path modes (fibonacci, hilbert, spiral, pythagorean, zp, all) over Mandelbulb or Fermat surfaces |
| `scripts/padic_drift.py` | p-adic packet drift: valuation, Teichmüller label, and drift depth over digit windows |
| `scripts/padic_viz.py` | Drift visualisation — line plot and heatmap of C_p(n, L) over prime and Pythagorean sequences |

## Requirements

Python 3.10+

```bash
pip install numpy matplotlib
```

## Usage

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
