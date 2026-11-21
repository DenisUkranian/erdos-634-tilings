# Independent audit of exact long-bank completion

The implementation under review is
[`long_bank_completion.py`](../long-banks/long_bank_completion.py).
This audit concerns the exact reconstruction and finite geometric choice
problem. It does not enumerate all odd packings or exclude either target.

## Findings

**No correctness defect was found in the reviewed implementation.**

The canonical primitive direction on a support line is independent of the
edge orientation. Its normalized vector has physical length `c` in the axial
metric `x²+xy+y²`. Rational translation along that line gives a unique exact
coordinate `t`; reduction by the integer floor, including for negative `t`,
correctly identifies every actual `c`-step orbit. No extra longitudinal period
or lattice cutoff is imposed.

If `f_n` is the short-edge endpoint current in an orbit, the reconstructed
long-edge coefficient satisfies

\[
k_n-k_{n-1}=-f_n.
\]

Its finite-support solution is unique and is exactly the negative prefix
sum used by the implementation. Existence requires zero total `f` in each
orbit. Distinct residues remain separate even when their physical intervals
overlap.

The apex formula uses the axial perpendicular
`(-v_x−2v_y,2v_x+v_y)`. Its determinant with `v` is `2c²`, so the prescribed
coefficient gives the correct area `ab/2` in axial coordinates. Swapping the
two short side lengths yields precisely the two triangles on the required
side of a long segment. Exact edge lengths and side orientation are checked
in the implementation and independently against the positive control.

The convex separation and containment tests use non-strict inequalities for
boundary contact. Thus touching edges are allowed, while positive interior
overlap is excluded. Two same-side mandatory base intervals with positive
overlap force overlapping triangles; opposite-side intervals do not have
that implication. The capacity test makes this distinction correctly.

The 2-SAT encoding forbids an invalid apex choice by `u→¬u`, and forbids a
conflicting pair by `u→¬v` and `v→¬u`. The iterative Kosaraju traversal and
component ordering return valid assignments. A complementary pair in one
strongly connected component is the exact unsatisfiability criterion.

## Essential scope: net edges and neutral pairs

The reconstruction determines **net signed long-edge multiplicities**. A
pair of opposite-side triangles with the identical long edge cancels and
is invisible to this net current. Such neutral pairs may still be needed
in a full tiling.

This causes no defect in a necessary mandatory-bank test. In a nonoverlapping
packing, each bank of a given physical base can contain at most one triangle;
therefore a nonzero net coefficient forces the corresponding single tile.
But satisfiability of the mandatory bank does not certify the placement of
neutral pairs or the rest of the tiling.

The input must contain **every odd tile**. Applying the same rejection test
to an arbitrary unfinished odd subset would not be a valid exclusion of its
possible later odd extensions.

## Independent replay

```sh
python3 research/2026-11-21/semiprimes/integer-closure/arithmetic/verify_long_bank_audit.py
```

The standard-library audit checks:

- **28,933 small 2-SAT formulas** against complete truth-table enumeration:
  all unary and cross-variable binary clauses on at most two variables, plus
  every cross-variable binary-clause subset on three variables with either
  no forbidden literal or one forbidden literal;
- satisfiable and contradictory implication chains with **2,000 variables**;
- independent decoding, exact full current cancellation, and exact area of
  the complete **143-tile positive control**;
- recovery of all net even-long edges from its complete 105-tile odd packing,
  under the identity and under rotations `z^{-3}` and `z^4` with nonintegral,
  partly negative translations;
- inclusion of every actual mandatory even triangle among the two generated
  apex choices;
- the complete contained mandatory-bank choice problem for that positive
  control, plus exact touching, opposite-bank, same-bank overlap and
  multiplicity cases.

All cases pass. In the positive control the reconstruction recovers **two**
mandatory long edges out of **38** even tiles; the remaining **36** even tiles
form **18 neutral long-edge pairs**. Both mandatory triangles pass the full
geometric choice test. This is a useful positive control for the intended
net-current interpretation.

Output: [`LONG_BANK_AUDIT_REPLAY.json`](LONG_BANK_AUDIT_REPLAY.json).
