# Independent audit of the 3431 cylinder and packing lift

21 November 2026. **Audit passed. Neither original tiling question is
settled by this result.** This note audits the separate
[cylinder theorem](../exact-lines-3431/CYLINDER_LIMIT.md) and its
[exact verifier](../exact-lines-3431/verify_cylinder_lift.py).

The completed proof supplies a fractional 111-tile point satisfying
every actual-line cylinder equation, the prescribed sign and gate
data, and every linear inequality valid for all contained integral
nonoverlapping partial packings of exactly 111 height-one tiles.
It does not supply an individual integral packing with those same
sign, gate, and cylinder data. A constraint derived jointly from
packing and the required sign/contact profile may still be stronger.

## 1. The finite lift and its normalization

With `c=37`, let `X,Y,K` range independently through `0,...,36` and
set `q=(800,-36)+X U_0+Y U_1+K U_2`. For every residue `r mod cR`,
choosing `K` fixes unique `X,Y` producing that residue. Therefore the
convolution multiplicities satisfy `sum_(q congruent r) m(q)=c`.
The weight `m(q)x_r/c` consequently preserves each original residue
column, including its orientation, hand, sign, and gate labels.

For a fixed axis and a fixed actual transverse line, the parameter
in that axis direction is still uniform through all longitudinal
residues. The other two parameters determine the transverse line.
The conditional mass is therefore independent of the longitudinal
residue. Every short-edge endpoint offset is longitudinal to the
axis of its own row; it does not change this transverse conditional
mass. This proves the stated operator identity

\[
 A_{\rm cylinder}L=E A_{\rm torus}.
\]

Conversely, aggregation of actual transverse coordinates by residue
recovers the torus rows. Thus the nonnegative projections coincide
for this contained lift. This equality concerns continuous weights;
it is not a statement about integer projections.

The actual short-edge coordinates, signs, and axis conventions in
the checker agree with the polygon `(q-aU_j,q,q+bU_(j+s))`, reversed
when necessary to make it counterclockwise. Its axial determinant
is `ab`. The scaled board and all containment tests use the same
path frame divided by `z`.

## 2. Why translation averaging gives valid packing marginals

The support hexagon has radius 36, and the convex hull of all tile
vertices at its anchors has radius `36+a=69`. The verifier enumerates
all 133 translations of this enclosing hexagon by `cR` that lie
strictly inside the board. The finite centre box used for this search
contains every possible accepted translation.

For a resulting anchor `q`, the preimages `q-ct` from distinct
translations are distinct members of one residue class. Their total
original convolution multiplicity is at most 37. Hence the averaged
multiplicity satisfies `0<=mbar(q)<=37` and its weight is
`mbar(q)x_r/(37*133)`.

At fixed residue, orientation and hand, different anchors differ by
a nonzero vector of `cR`, of length at least `c`. The tile diameter
is `c`, and any two interior points of a nondegenerate triangle are
at distance strictly less than its diameter. Thus all tiles in that
fixed family have disjoint interiors. This validates the pointwise
coverage bound `111/133<1`, the conflict-clique bound, and the
threshold decomposition into integral partial packings.

## 3. The exact-111 decomposition is also valid

Let `D=37*133=4921` and, within a residue family, use integer interval
lengths `w_q=111*mbar(q)`. They satisfy

\[
 0<w_q\le4107<D,\qquad\sum_q w_q=111D.
\]

Partition the integer positions in `[0,111D)` into these successive
intervals. Each sampling residue `t mod D` occurs exactly 111 times
in the whole range. Because an interval has length less than `D`,
these 111 positions belong to 111 different intervals. Selecting
their anchors gives a genuine contained nonoverlapping 111-tile
partial packing. Each anchor occurs in exactly `w_q` samples.

Uniform sampling within the family gives marginal `w_q/D`. Choosing
the residue/orientation family with weight `x_r/111` gives final
marginal `x_r*mbar(q)/D`, exactly the averaged cylinder lift. The
family weights sum to one because the torus population is 111.
This proves convex-hull membership without any numerical optimizer
or unproved rounding assertion.

Each component has a single orientation and sign. The prescribed
74/37 sign split and all contact/gate equations hold in the mixture,
not in its components. This distinction is essential: intersection
with those affine constraints does not select an integral component.

## 4. Exact replay

The final supplied checker was independently rerun successfully. It
replays the original rational torus certificate, then verifies:

* all 16,428 torus columns of the operator identity and all 4,107
  axis/residue conditional marginal identities;
* all 47,964 placements of the initial finite lift, strictly contained
  with minimum board-side determinant 143,854,520;
* the 133 strictly contained translates, producing 226,663 anchors
  and 2,719,956 oriented columns;
* all 6,736,849 residue/sampling-offset cardinalities, each exactly
  111, defining 80,842,188 packing components with repetitions;
* the separate initial lift's explicit packing violation, which is
  repaired by averaging and is not an exclusion of the cylinder cone.

The audited files have SHA-256 hashes:

| File | SHA-256 |
|---|---|
| `CYLINDER_LIMIT.md` | `d63cab28c534dc5ae08c82c22bdf1019b4c752e2345cd0d71a9e5d5da0dc305f` |
| `verify_cylinder_lift.py` | `0db3647dbb4f6954eca7c3c5824966b9c00f9e082dc459fcab9018db8ff2d3a0` |
| `CYLINDER_LIFT_REPLAY.json` | `1fc4d6687fd7add868098a99a9df99f7c5a024a707944b893582bbf6ed3a28a6` |

No floating-point infeasibility claim is used. The optional full-catalogue
pricing calculation is not needed for, and was not part of, this
independent lift audit.

## 5. Consequence for the proposed immediate rigid-body exclusion

These results do not show that the complete integer physical model
is feasible. They show that passing from periodic residue currents
to all actual supporting lines, then adding arbitrarily strong linear
inequalities for 111-tile rigid packings alone, still leaves this
fractional point. Any further exclusion must use additional coupled
sign/contact information, actual longitudinal endpoint positions,
integrality, or another constraint absent from this precise relaxation.

The [full-current theorem](FULL_CURRENT_AND_NONOVERLAP.md) explains
the complementary positive criterion: once all actual physical currents
close with nonnegative integer placement multiplicities, nonoverlap
and coverage already follow. Establishing that such an integer system
has no solution remains a separate proof obligation.
