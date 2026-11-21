# The exact signed integer image of the periodic cell model

21 November 2026. **3431 and 5063 remain OPEN.**

This package settles a possible arithmetic route to those targets. For both
tile shapes, the **complete periodic endpoint model**, with zero endpoint
currents, has no hidden linear integer congruence beyond the established
charge divisibility. This statement concerns **signed integer coefficients**.
It does not establish a nonnegative integer solution, a packing, or a tiling.

The distinction matters: the published rational points do not themselves
settle integrality. The theorem below now settles the weaker integer-lattice
question exactly, including every possible prime-power congruence. The
remaining obstruction must use nonnegativity, limited populations, actual
positions, gate interactions beyond this cell projection, or a combination
of those requirements.

## 1. Model and theorem

Let `(a,b,c)` be either `(33,7,37)` or `(35,13,43)`. A periodic tile column is
indexed by an anchor `(x,y)` in `(Z/cZ)^2`, an orientation `j` in `Z/6Z`, and
a hand `s` in `{−1,+1}`. Put

\[
U_j=(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1),
\]

\[
u=q-aU_j,\qquad w=q+bU_{j+s},\qquad
\varepsilon=s(-1)^j.
\]

Its short-edge endpoint vector has four contributions:

\[
s[e_{j,q}-e_{j,u}+e_{j+s,w}-e_{j+s,q}],
\]

where axes are reduced modulo three and coordinates modulo `c`. It contributes
`ε` to upward gate `a u_y−b u_x` when `s=+1`, or to downward gate
`a u_x−b u_y` when `s=−1`. A positive-sign column contributes one to `P`; a
negative-sign column contributes one to `N`.

**Theorem.** For arbitrary integer gate vectors

\[
Q^+,Q^-\in\mathbb Z^c
\]

and arbitrary integers `P,N`, there is a **signed integer** combination of all
`12c²` periodic tile columns with zero complete endpoint vector and those exact
gate/sign totals if and only if

\[
\sum_r Q^+_r+\sum_r Q^-_r=P-N,
\qquad c\mid(P-N).
\tag{1}
\]

The coefficients in this theorem may be negative. Even when the prescribed
`P,N` are nonnegative, their representation need not be.

This is an image theorem for **zero-endpoint kernels**. It does not
characterize the integer image with arbitrary nonzero endpoint targets, nor
does it classify all endpoint kernels themselves.

## 2. Necessity

The gate/sign identity in (1) holds for every individual tile column.

For divisibility, set `t=(a−b)^{-1}` in `F_c` and use the endpoint potentials

\[
f_0(x,y)=tx,\quad f_1(x,y)=-ty,\quad f_2(x,y)=ty.
\]

Their pairing with each tile endpoint column equals `ε` modulo `c`.
Translations cancel inside each same-axis endpoint pair, so it suffices to
check the twelve oriented columns at one anchor. Therefore zero endpoint
current forces `P−N=0` modulo `c`, for signed as well as nonnegative integer
multiplicities.

This is the same charge potential used in the earlier
[small balanced cell analysis](../../continued-rigidity/integer3431/SMALL_BALANCED_CELLS.md).

## 3. Sufficiency by a finite lattice-index certificate

Use the integral coordinates

\[
(Q^+,Q^-,P)\in\mathbb Z^{2c+1}.
\]

The omitted coordinate is recovered integrally as

\[
N=P-\sum Q^+-\sum Q^-.
\]

Let `L` be the feature image of all signed integer endpoint kernels. Necessity
gives

\[
L\subseteq D_c
=\{(Q^+,Q^-,P):\ \sum Q^++\sum Q^-\equiv0\pmod c\},
\]

where `[Z^{2c+1}:D_c]=c`.

The certificate supplies a finite family of **nonnegative integer endpoint
kernels**. These are translated six-column kernels, uniform charged `3c`
fans, and uniform single-orientation kernels with `c²` columns. Every one of
these kernels is reconstructed and its complete endpoint current is checked
directly. Spatial containment and nonoverlap are not asserted for the kernels.

Let `L_0` be the integer span of their feature vectors. Then

\[
L_0\subseteq L\subseteq D_c.
\]

The selected square minors have these absolute determinants:

| Shape | Feature dimension | Kernel vectors checked | Absolute determinants | Gcd |
|---|---:|---:|---|---:|
| `(33,7,37)` | 75 | 78 | `999`, `666`, `32856`, `138687914` | 37 |
| `(35,13,43)` | 87 | 89 | `387`, `454854`, `294016886` | 43 |

Each nonzero determinant gives a full-rank sublattice of `L_0`, so
`[Z^{2c+1}:L_0]` divides every listed determinant. Hence this index divides `c`.
The inclusion `L_0⊆D_c` makes the same index a multiple of `c`. Consequently

\[
[\mathbb Z^{2c+1}:L_0]=c,
\qquad L_0=D_c,
\qquad L=D_c.
\]

This proves sufficiency. It does **not** require an assumption that the supplied
kernel family generates every endpoint kernel. Its feature image already
has the largest possible integer lattice allowed by the necessary charge
condition.

The replay evaluates every square determinant with integer Bareiss elimination,
asserting each exact division. It does not use floating rank calculations,
SciPy, SymPy, or a solver status.

## 4. Native profiles: explicit signed witnesses

Separate exact witnesses are supplied for the profiles that earlier integer
searches could not decide:

| Target | Gate support at residue zero | Prescribed sign totals |
|---|---|---|
| 3431 | `Q⁺=22δ₀`, `Q⁻=15δ₀` | `P=74`, `N=37` |
| 5063 | `Q⁺=42δ₀`, `Q⁻=δ₀` | `P=129`, `N=86` |

All other gate entries are zero. The independent replay reconstructs the
complete `3c²` endpoint rows, all `2c` gate rows, and both sign totals from the
saved **signed tile multiplicities**. It also asserts that negative
multiplicities actually occur, preventing these witnesses from being
mistaken for nonnegative integer points.

The witnesses show why a new modular identity alone cannot rule out these
profiles. They say nothing about whether the same profiles have nonnegative
integer representations of the prescribed population.

## 5. Scope for the original tiling problems

The theorem applies to every integer cell gate profile satisfying (1), not
only to the two displayed native profiles. It therefore rules out a further
Smith-normal-form or prime-power torsion obstruction **within this periodic
endpoint/gate/sign-count projection**.

It does not weaken the need for whole tiles. It identifies the extra content
of that requirement: tile coefficients must be **nonnegative integers**, and
actual placements must satisfy the full physical boundary/current and board
conditions. An integer span allows cancellation of formal tiles; a real
packing does not.

In particular, this result does not prove that the suggestion “integer rigid
tiles automatically close 3431” is true or false for the full geometric
problem. It proves that integer linear congruences in this periodic model
cannot, by themselves, supply that closure.

## 6. Exact replay and discovery provenance

```sh
python3 research/2026-11-21/semiprimes/integer-closure/arithmetic/verify_integer_gate_image.py
```

Input certificates:

- [`GATE_IMAGE_INDEX_CERTIFICATE.json.gz`](GATE_IMAGE_INDEX_CERTIFICATE.json.gz):
  the kernel descriptions and exact square-minor selections;
- [`FULL_INTEGER_IMAGE_3431.json.gz`](FULL_INTEGER_IMAGE_3431.json.gz) and
  [`FULL_INTEGER_IMAGE_5063.json.gz`](FULL_INTEGER_IMAGE_5063.json.gz): explicit
  signed periodic tile vectors for the native profiles.

Output: [`INTEGER_GATE_IMAGE_REPLAY.json`](INTEGER_GATE_IMAGE_REPLAY.json).

The standard-library verifier is independent of the discovery elimination.
Discovery programs use NumPy/SciPy/SymPy as available:

- `probe_integer_image.py` first settles the weaker additive marginal image
  and exports exact signed witnesses. Sparse unit-pivot elimination is
  followed by a small residual Smith calculation when necessary.
- `probe_full_kernel_image.py` uses whole known endpoint kernels to construct
  the explicit full signed witnesses. An optional small integer optimization
  reduces coefficient sizes; every returned vector is verified exactly.
- `build_image_index_certificate.py` searches the exact residual minors and
  exports the much smaller independently replayable determinant certificate.

The saved `MARGINAL_INTEGER_IMAGE_*` files are supporting provenance. The
theorem and replay do not rely on the weaker marginal model or on numerical
optimization.
