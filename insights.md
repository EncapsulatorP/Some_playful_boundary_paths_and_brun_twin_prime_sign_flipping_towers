# Insights

## Surface geometry

### Mandelbulb
The power-8 Mandelbulb is the most commonly studied 3D analogue of the Mandelbrot set, obtained by applying the escape-time iteration in spherical coordinates:

```
r^n * (sin(n*phi)*cos(n*theta), sin(n*phi)*sin(n*theta), cos(n*phi))
```

The boundary is found per direction via a coarse linear probe (48 steps) followed by a 7-step binary search — enough precision for path projection but not for high-resolution rendering. The coloring mixes escape radius and escape iteration to produce the warm-to-cool gradient across the fractal boundary.

### Fermat surface
The real Fermat surface `|x|^n + |y|^n + |z|^n = 1` has an analytic solution for the boundary radius along any unit direction `d`:

```
r = (sum(|d_i|^n))^(-1/n)
```

This is orders of magnitude faster than the Mandelbulb boundary search and produces smooth, convex shapes. At `n=2` the surface is the unit sphere; large `n` converges toward a cube. Paths on Fermat surfaces are easier to read visually because the surface has no concavities to hide segments.

## Path generators

### Fibonacci fill
Golden-angle ordering of the sphere gives near-uniform point density with no visible clustering. It is the most effective single-path fill in terms of coverage uniformity for a fixed point count.

### Hilbert path
A 2D Hilbert curve of order `k` covers a `4^k`-point grid, which is unwrapped onto the sphere via a longitude/latitude mapping. The curve is space-filling in 2D but the projection introduces non-uniform density — equatorial regions are oversampled relative to the poles. Order 4 (256 points) shows a clear space-filling structure; order 5 (1024 points) approaches uniform coverage at the cost of significant render time on the Mandelbulb.

### Spiral sweep
A constant-pitch spherical spiral parametrized by `z = 0.98 - 1.96*t`. Coverage becomes denser near the poles and sparser at mid-latitudes for a fixed turn count. The current implementation deliberately stops at `z = ±0.98` to avoid degenerate polar segments.

### Pythagorean tower path
Uses the nested-radical defect `2 - sqrt(2 + sqrt(2 + ...))` and the cosine signal `2 - 2*cos(pi/2^n)` to modulate azimuth and elevation. The sequence converges rapidly toward 2, so the path is concentrated at low depths and spreads thinly at large `n`. The defect drives the hover offset, lifting the path slightly above the surface as it converges.

### Z_p compression path
Uses `log(p - 1)` as a compression proxy for the prime `p`, with prime gaps modulating the azimuth. The resulting path is deliberately irregular: large prime gaps produce visible jumps that expose the gap structure visually. This irregularity distinguishes it from every other path mode, which are all smooth.

## Key observations

- **Polyline length as a coverage proxy**: `scripts/pathfilling.py` reports path length `L` in the legend. A larger `L` for the same number of control points generally indicates better coverage, though it also depends on how evenly the length is distributed.

- **Fibonacci dominates for uniform coverage**: Among the paths, Fibonacci sphere ordering consistently produces the most uniform scatter. The Hilbert path approaches similar uniformity only at order 5+, which multiplies point count by 4×.

- **Fermat surfaces isolate path geometry**: Because Fermat surfaces are convex and smooth, all paths are fully visible from any camera angle. The Mandelbulb's concavities can hide portions of a path, making Fermat a cleaner substrate for comparing path shapes.

- **Arithmetic paths are sparse by design**: The Z_p and Pythagorean paths use only ~30–50 control points. They are not meant to fill the surface — they are meant to trace a structured arithmetic signal over it. The densification step interpolates between control points to produce a smooth curve, but the underlying signal still determines the path's global shape.

- **Power parameter sensitivity**: The Mandelbulb changes shape significantly between `--power 4` (rounder, fewer lobes) and `--power 8` (canonical, complex boundary). Paths projected at `power 8` can look very different from the same paths at `power 4` because the boundary radius varies more sharply with direction.

## p-adic packet drift (Witt–Teichmüller carry diagnostics)

For a sequence of base-p digits, the carry-wheel window at rank n with length L is:

```
W(n, L, p) = sum_{j=0}^{L-1} d[n+j] * p^j
```

This is a local p-adic packet. The diagnostic triple `C_p(n, L)` decomposes it into three independent layers:

### Layer 1 — carry depth
`r = v_p(W)`: the largest power of p dividing the packet. Measures pure divisibility. A window of all-zero digits except one non-zero entry has r = index of that entry.

### Layer 2 — Teichmüller label
The unit part `U = W / p^r` lies in `Z_p^×`. Its Teichmüller representative is:
- Odd p: `ω = U mod p`, in `{1, ..., p-1}` — the residue identity.
- p=2: `σ = ±1` based on `U mod 4` — the sign component of `Z_2^× ≅ {±1} × (1 + 4Z_2)`.

The Teichmüller label names the "orbit" the unit belongs to.

### Layer 3 — drift depth
After stripping the Teichmüller label, the remaining principal-unit drift is:
- Odd p: `Δ = v_p(U^{p-1} - 1)`. By Fermat, `Δ ≥ 1` always; large Δ means U is close to its Teichmüller representative.
- p=2: `Δ = v_2(U-1)` if `U ≡ 1 (mod 4)`, else `v_2(U+1)`. Minimum is 2 (since the principal part lives in `1 + 4Z_2`).

The p-adic norm of the drift is `D_p = p^{-Δ}` — small means stable.

### Practical formula
The drift depth needs no explicit Teichmüller lift:

```
Δ_p(n, L) = v_p(U^{p-1} - 1)      (odd p)
```

because raising to `p-1` kills the Teichmüller part exactly (it is a `(p-1)`-th root of unity).

### Observations from `padic_viz.py`
- The prime digit sequence has predominantly low drift (Δ = 1) at small window lengths, but isolated windows with deeper drift appear when the packet happens to agree with its Teichmüller representative to higher p-adic order.
- The Pythagorean tower sequence has more variable drift because the large scaling factor (`10^7`) produces digits that are less uniformly distributed in base p.
- The heatmap shows that drift depth is not monotone in L: a longer window can be more or less stable than a shorter one depending on how the extra digits shift the unit part.
- For p=2, drift depth is always ≥ 2 because the principal unit lives in `1 + 4Z_2`. This is visible as the floor line in the p=2 heatmap.
