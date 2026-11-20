# Independent review of the single-class gate-capacity theorem

21 November 2026. Internal independent mathematical and integer review.
The general localization, certificate inequality, bank consequence,
and two median-parameter exclusions are sound with the stated exterior
terms retained. They do not decide either complete target problem.

## Localization at an arbitrary joint Euclidean class

For `L=q0+z^hR`, assigning a periodic endpoint value on `L` and zero
off `L` is legitimate on every point of a physical supporting line.
An oriented edge weight is its endpoint difference, so cancellation
under arbitrary subdivision is exact.

A long edge of height `h` differs by an element of `c z^h R`.
Its endpoints therefore either both lie in `L`, in the same residue,
or both lie outside `L`; its weight is zero. A short-height-`h`
tile in a different joint class has all its vertices outside `L`
and also contributes zero. The other short heights receive no
short-side weight. Thus the full-tiling sum isolates precisely the
actual tiles of `L`, with the stated outer-boundary correction.

An affine neighboring gate is covered by changing the representative
`q0` within the same short class. A shared point with that neighboring
joint edge cell can be chosen as the representative. The gate then
has the form `q0+z^(h+1)R` or `q0+z^(h-1)R`. Integral offsets along
the physical run keep all the participating long endpoints in this
same edge cell even when their contacts are partial.

## Symmetries and exterior terms

The 180-degree map changes `(j,s)` to `(j+3,s)` and reverses
`epsilon`. The map `w -> -conjugate(w)` changes `(j,s)` to
`(3-j,-s)`, preserves `epsilon`, and exchanges the two neighboring
gates. These justify the same column coefficients for the sign and
hand variants.

Each variant uses its own transformed endpoint functional. If the
only hypothesis were an accidental zero total for one particular
outer functional, zero for the other variants would not follow.
The final note explicitly requires the appropriate exterior term
to vanish for each variant used. Absence of outer sides at height
`h` is a sufficient common condition; it holds in every height-one
application here. The absolute-value bank bound requires the two
sign versions and hence both of their exterior terms to be zero.

## Independent arithmetic control

I rebuilt short-side endpoint currents using the independent CCW
polygon and exact metric routines of `verify_both_gate_torus.py`,
without importing the gate-capacity generator or its checker.
For each `phi(q)` residue and all 12 shapes, I checked

`W + C_sign - D*1_(positive, upward, gated) >= 0`

using integers. There were 84, 444, and 516 complete one-prime
columns for the 7, 37, and 43 controls respectively. Every minimum
slack was zero. These residues exhaust translations because all
endpoint weights and the gate condition depend only on `phi(q)`.

The coefficients satisfy `C_plus+C_minus=D`. Consequently the
positive and negative gate bounds become

\[
 P_g\le(n_L-\beta G_L)/2,\qquad
 M_g\le(n_L+\beta G_L)/2.
\]

For a subset of `m` distinct actual bank tiles with signed sum `K`,
its positive and negative counts are `(m+K)/2` and `(m-K)/2`.
The two inequalities give exactly

\[
 n_L\ge m+|K+\beta G_L|.
\]

This does not double-count the opposite bank or assume that the
selected subset exhausts its Euclidean class.

In the minimal-odd mode, the known actual-median localization gives
sign populations `(2c,c)` in the height-one class. The resulting
positive gate capacities are `265/6` and `51`, hence at most 44
and 51 actual tiles. The parameter values `n=0,1` require respective
signed path counts `2c` and `2c-d`, both exceeding these capacities
at each target. The remaining listed parameter values are not
excluded. The proof concerns all actual upper median paths, without
a canonical-path assumption.
