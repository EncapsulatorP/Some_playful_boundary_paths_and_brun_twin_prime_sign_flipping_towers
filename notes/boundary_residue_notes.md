# Boundary Residue Notes

Repunit Inverse Towers, Brun Deficit, and a Collatz Bay  
Conversation wrap / editable working note  
5 June 2026

## Abstract

This note wraps the chat into a modifiable mathematical sketch. The central observation is not a PSLQ-style identity. It is a shared boundary-residue pattern: an upper branch of an inverse repunit tower produces a residue just above `1`, while Brun's constant and the proposed Collatz Bay snap-back constant sit just below `2`.

The strongest numerical match in the note is:

```text
z_+(1.11) - 1 ~= 2 - B_2
```

The implemented code treats that as a reproducible diagnostic coincidence, not as an identity claim.

## Status

| Status | Statement |
| --- | --- |
| Keep | The repunit iteration has a clean attracting fixed point branch, and its upper residue can be defined exactly as a function of `c`. |
| Caveat | The closeness to Brun's constant is numerically real but tunable; it is not evidence of an identity by itself. |
| Quarantine | Any claim that Brun's constant, the Collatz Bay constant, and the repunit tower are the same hidden object. |
| Next test | Treat the pattern as a boundary-shape diagnostic: compare residual profiles, derivatives, stability exponents, and cycle structure across families of iterative maps. |

## The Code Fragment

The original numerical experiment was:

```python
c = 1.11
y = 1.0
for _ in range(1000):
    y = c ** (-(c ** y))
print("Lower bound (starts with neg):", y)

z = 1.0
for _ in range(1000):
    z = c ** (c ** (-z))
print("Upper bound (starts with pos):", z)
```

With `c = 1.11`, this converges numerically to:

```text
y_- ~= 0.8917774506448141
z_+ ~= 1.0975340696153890
```

The upper branch is the branch used for the Brun comparison because:

```text
z_+(1.11) - 1 ~= 0.0975340696153890
```

## Upper Inverse-Tower Branch

The upper iteration is the dynamical system:

```text
T_c(z) = c^(c^(-z))
```

An attracting fixed point satisfies:

```text
z_+(c) = c^(c^(-z_+(c)))
```

Define the tower boundary residue by:

```text
L_tower(c) = z_+(c) - 1
```

For `c = 1.11`:

```text
L_tower(1.11) ~= 0.0975340696153890
```

Let `L = log(c)`. Since `c = 1.11` is close to `1`, `L` is small:

```text
L = log(1.11) ~= 0.1043600153242429
```

The fixed-point equation can be rewritten as:

```text
z = exp(L * exp(-L z))
```

The small-`L` expansion of the attracting branch is:

```text
z_+(c) = 1 + L - L^2/2 - 4L^3/3 + 7L^4/8 + 14L^5/5 + O(L^6)
```

This explains why the residue naturally lands near, but below, `log(1.11)`.

## Brun Deficit

Let `B_2` denote Brun's constant:

```text
B_2 = sum_(p, p+2 twin primes) (1/p + 1/(p+2))
```

A commonly quoted estimate is:

```text
B_2 ~= 1.902160583104
```

This gives the Brun boundary deficit:

```text
L_Brun = 2 - B_2 ~= 0.0978394168960000
```

Key comparison:

```text
L_tower(1.11) - L_Brun ~= -0.0003053472806109
```

Relative gap:

```text
|L_tower(1.11) - L_Brun| / L_Brun ~= 0.003121
```

So the match is visually real at the scale of the note, but the implementation treats it as a diagnostic coincidence until a structural bridge is found.

## Collatz Bay Input

The note uses a proposed Collatz Bay snap-back constant:

```text
c_* ~= 1.9086708647584145
```

with

```text
log(2) / log(c_*) ~= 1.07230747
```

The corresponding deficit from the anchor `2` is:

```text
L_Collatz = 2 - c_* ~= 0.0913291352415855
```

This sits in the same broad residual band near `0.1`, but is a weaker match than Brun's deficit:

```text
L_tower(1.11) ~= 0.09753
L_Brun ~= 0.09784
L_Collatz ~= 0.09133
```

## Numerical Table

| Object | Definition | Value |
| --- | --- | ---: |
| Lower repunit branch | `y = c^(-c^y)` at `c = 1.11` | `0.8917774506448141` |
| Upper repunit branch | `z = c^(c^(-z))` at `c = 1.11` | `1.0975340696153890` |
| Tower residue | `z_+(1.11) - 1` | `0.0975340696153890` |
| Brun estimate | `B_2` | `1.9021605831040000` |
| Brun deficit | `2 - B_2` | `0.0978394168960000` |
| Collatz Bay constant | `c_*` | `1.9086708647584145` |
| Collatz deficit | `2 - c_*` | `0.0913291352415855` |
| Reciprocal Brun | `1 / B_2` | `0.5257179698089272` |
| Reciprocal Collatz | `1 / c_*` | `0.5239247994318668` |

## Boundary Residue Function

The implemented framework uses an `L`-like boundary-residue profile:

```text
L_partial(M_c; b) = dist(A_c, b)
```

Where:

- `M_c` is an iterative system.
- `A_c` is an attracting fixed point or cycle.
- `b` is a reference boundary anchor.

Examples:

```text
L_partial(T_c; 1) = z_+(c) - 1
L_partial(Brun; 2) = 2 - B_2
L_partial(Collatz Bay; 2) = 2 - c_*
```

This keeps the framework flexible: compare stable boundary residues directly instead of forcing hidden identities.

## Why The Closeness Happens

The repunit tower branch is close because `c = 1.11` makes `log(c)` small. The map

```text
z -> c^(c^(-z))
```

acts almost like the identity near `1`, then pulls the fixed point to

```text
z_+ ~= 1 + 0.0975
```

Brun's constant lives near:

```text
B_2 ~= 2 - 0.0978
```

So the comparison is a residual match:

```text
upper tower excess above 1 ~= Brun deficit below 2
```

The Collatz Bay constant has the same general shape but a looser deficit:

```text
c_* ~= 2 - 0.0913
```

## Tunability Warning

Because `L_tower(c)` varies continuously with `c`, nearby bases can be chosen to match the Brun deficit almost exactly. Numerically:

```text
c ~= 1.1103954628296591
```

solves:

```text
L_tower(c) = 2 - B_2
```

The local sensitivity near `c = 1.11` is:

```text
dL_tower / dc ~= 0.772531
```

That is the main reason not to overclaim. The closeness is useful as a detector, not a proof.

## Shape Plot

The `L_tower(c)` curve crosses the Brun-deficit level near `c ~= 1.110395`. This confirms that the match is part of a smooth boundary profile rather than an isolated special point.

Generated artifacts:

- `outputs/boundary_residue_L_tower.png`
- `outputs/boundary_residue_comparison.png`

## Research Program

Safe next development path:

1. Define a library of maps `M_c` with attracting fixed points or cycles.
2. Compute `L_partial(M_c; b)` and its derivative profile.
3. Compare boundary residues only after normalizing the boundary anchor `b`.
4. Add stability data: multiplier, Lyapunov exponent, basin size, and period of the attracting cycle.
5. Only then test whether arithmetic constants land on non-tunable special points of the profile.

## Minimal Conclusion

The plausible object here is a boundary-residue `L`-profile for iterative systems. It is not a Dirichlet-style `L`-function. The honest claim remains:

```text
L_tower(1.11) ~= L_Brun
L_Collatz is nearby but weaker
```

# Truncation

Alright — I’ll make this **finite**, **right-associated**, and with **explicit sign rules** so it’s actually computable.

## 1) “Euler theta” tetration with alternating exponent signs (2 starts negative vs positive)

I’m interpreting “Euler teta/theta” as the classical **Jacobi theta** value
[
a_n=\theta_3(0,q_n),\quad q_n=e^{-\pi n},\quad \theta_3(0,q)=\sum_{k\in\mathbb Z} q^{k^2},
]
(which some sources casually call “Euler theta” in physics/math contexts). ([Wikipedia][1])

Using **depth (N=10)**, the first few (a_n) are:

* (a_1\approx 1.086434811213308)
* (a_2\approx 1.003734885487739)
* (a_3\approx 1.000161399035141)
* (a_4\approx 1.000006974684712)
  (then it’s basically (1+ \text{tiny}).)

Define the finite signed tower (right-associated) by:
[
T = a_1^{,s_2,a_2^{,s_3,a_3^{,s_4,\cdots^{,s_{10} a_{10}}}}}
]
where (s_k\in{+1,-1}) is the sign applied at level (k).

### A) “2 is negative, 3 positive, 4 negative, …”

So (s_2=-, s_3=+, s_4=-,\dots)

**Value (depth 10):**
[
T \approx \mathbf{0.9201568837551976}
]

### B) “2 is positive, 3 negative, 4 positive, …”

So (s_2=+, s_3=-, s_4=+,\dots)

**Value (depth 10):**
[
T \approx \mathbf{1.08609967033555}
]

---

## 2) Same theta bases, but “positive exponents at golden-ratio rate”

To make “+ signs appear with golden-ratio density”, I used the Beatty/Wythoff idea:

Let (\varphi=\frac{1+\sqrt5}{2}).
Set (s_k=+1) iff (k \in {\lfloor m\varphi\rfloor : m=1,2,3,\dots}), else (s_k=-1).
This gives +’s with asymptotic frequency (1/\varphi \approx 0.618).

**Value (depth 10):**
[
T_{\text{golden-sign}} \approx \mathbf{0.9201567916239852}
]

(Note: it lands extremely close to the alternating “start negative” case because almost all deeper (a_n) are ~1.)

---

## 3) Totient tower where exponent sign follows the Möbius function

Here we switch to:

* **Euler totient** (\varphi(n)) ([Wikipedia][2])
* **Möbius** (\mu(n)\in{-1,0,1}) ([Wikipedia][3])

To avoid the “(\mu(n)=0)” square factor case killing the fun, I used **only squarefree** (n) (so (\mu(n)=\pm1)).

### 3A) Raw totients (starting at (n=3) so the first base isn’t (\varphi(2)=1))

Squarefree (n): (3,5,6,7,10,11,13,14,15,17)
Bases: (\varphi(n)=2,4,2,6,4,10,12,6,8,16)
Signs: (s_k=\mu(n_k)) (applied as the sign at that level).

**Value (depth 10):**
[
T_{\varphi,\mu} \approx \mathbf{0.4924683288151911}
]

### 3B) Normalized totients (more “theta-like” stability)

If you want it to behave more like your “Collatz bay” numerics (bases near 1–2), use
[
b_k = 1+\frac{\varphi(n_k)}{n_k}.
]
With squarefree (n=2,3,5,6,7,10,11,13,14,15,17,19):

**Value (depth 12):**
[
T_{1+\varphi/n,\mu} \approx \mathbf{0.8219203647109268}
]

---



[1]: https://en.wikipedia.org/wiki/Theta_function?utm_source=chatgpt.com "Theta function"
[2]: https://en.wikipedia.org/wiki/Euler%27s_totient_function?utm_source=chatgpt.com "Euler's totient function"
[3]: https://en.wikipedia.org/wiki/M%C3%B6bius_function?utm_source=chatgpt.com "Möbius function"


## References

1. E. W. Weisstein, "Brun's Constant", MathWorld.
2. D. Platt and T. Trudgian, "Improved bounds on Brun's constant", arXiv:1803.01925, 2018.
3. P. Sebah and P. Demichel, "Introduction to twin primes and Brun's constant computation", 2002.
