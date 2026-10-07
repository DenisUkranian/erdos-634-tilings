# Fixed-class density, local matrices and the remaining geometry

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
Universal arguments received separate internal reviews where indicated;
this is not external peer review, formal verification or a priority claim.

**Erdős 634 is not completely solved here. The counts 154 and 4830 remain
unresolved.** This continuation combines the prior repository results with
a fresh primary-source audit and records the strongest resulting deductions.

## Fixed-class density and a quantitative geometric remainder

For each fixed squarefree d, let A_d be the odd multipliers admitted by
the primitive F3 divisor-and-square test, F_d the actual odd F3
multipliers, and C_d the multipliers supplied by the existing explicit
constructive tails. Then C_d is contained in F_d, which is contained in
A_d, and

\[
\#((\mathcal A_d\setminus\mathcal C_d)\cap[1,X])
=O_d\!\left(X^{1/3}(1+\log X)^{r_d/2}\right),
\qquad r_d=\operatorname{rank}(Y^2=X^3+(3d)^3).
\]

All three sets have the same natural density relative to odd integers.
That density has a finite inclusion–exclusion approximation from the
primitive coefficients, whose reciprocal sum converges. The proof
combines the elliptic height bound with the geometric threshold
`T_s=O_d(sqrt(s))`; neither rank nor a full basis needs to be computed
for the theoretical conclusion. See [the complete proof](F3_FIXED_CLASS_DENSITY.md)
and [independent internal review](DENSITY_AUDIT.md).

**In square class 38 this is a global result for the odd sector:**
all other branches are excluded, the density exists and satisfies
`0<delta_38<=1/3`, and the same sparse bound contains the undecided
multipliers. No numerical density, explicit error constant, uniformity
in d, or classification of every small multiplier is claimed.

## New arithmetic and structural results

1. **A full linear local test for the odd sector of `6R m²`.** For odd
   squarefree R, with `3∤R` and `R≡5 mod8`, the relevant quartic covers'
   local conditions at 2, 3 and every prime dividing R are exactly a
   system over F₂. Inconsistency excludes every odd multiplier, with a
   short row-sum certificate. See [theorem and proof](arithmetic/FULL_LOCAL_MATRIX.md),
   [independent review](arithmetic/FULL_LOCAL_AUDIT.md), and
   [exact checks](arithmetic/full-verification.json). Consistency does
   not imply a rational point or a tiling.
2. **Flexible infinite exclusions extending 78.** If every prime factor
   of a squarefree cofactor Q is a quadratic residue modulo 13,
   `Q≡1 mod8` and `gcd(Q,39)=1`, then all odd multipliers in class
   `78Q` are excluded. Examples include 1326, 8814, 18174 and 20046.
   In particular this applies to any squarefree product of primes
   `q≡1 mod104`, with no quartic-residue condition on those primes.
   See [the selected-prime matrix and corollaries](arithmetic/MATRIX_OBSTRUCTION.md).
3. **No eventual congruence classification in square class 38.** For
   every modulus M, some residue class contains infinitely many odd
   realizable multipliers and infinitely many odd impossible ones.
   The new negative input is `342q^(2k)` for every odd prime q and
   `k≥0`; the positive input is the prior prime-avoidance construction.
   See [proof](STRUCTURAL_AUDIT.md) and [independent audit](CLASS38_AUDIT.md).

## What the geometry checks establish

- The [W/beta boundary-word theorem](w-beta/BOUNDARY_FILTER_BARRIER.md)
  shows that whole boundary sides, adjacent long edges, corner-angle
  inventories and straight-junction angle completions all pass at every
  scale `m≥2`. They also pass at scale one in the remaining interior
  parameter range. This prevents claiming that those filters alone
  finish W or beta. The formal directional inventory in the same package
  is explicitly a reproduction of an earlier repository result.
- The [reflected-corner investigation](f3/README.md) reduces one sufficient
  route to 4830 to a quadrilateral of 792 tile areas. The elementary
  parity obstruction rules out at most four integer-grid macrotriangles
  at every integer scale. The [rationalization argument](f3/FOUR_PIECE_OBSTRUCTION.md)
  extends that restricted obstruction to four similar triangles at
  arbitrary positive real scales. It does not rule out a unit tiling.
- The [I120 investigation](i120/README.md) checks a natural transfer from
  the new F3 constructions, but proves its output scales already lie
  above a prior constructive tail. Its resource-limited geometric search
  does not provide a negative certificate for 154.

## Source synthesis and limits

The [literature audit](LITERATURE.md) inspected Harries, Zhang,
Beeson–Laczkovich–Zhang, corrected Beeson manuscripts, Bonfioli, and other
public proof repositories. It identifies exact uses of retracted lemmas,
conditional formalizations, and a confusion between side lengths and
tile counts. No inspected external source supplies the missing general
small-scale geometric converse. This is a bounded search report, not a
proof that every source on the internet has been exhausted.

The enduring distinction is

    constructed tiling => realizability => necessary arithmetic data.

A valid local cover, formal edge inventory, or complete checker for a
supplied disk does not prove existence of a globally compatible disk.
The new exclusions and structural theorems do not change that implication.

## Reproduction

From the repository root:

```sh
python research/final-synthesis-oct7/check_class38_nonperiodic.py
python research/final-synthesis-oct7/check_f3_height_density.py
python research/final-synthesis-oct7/arithmetic/check_matrix.py
python research/final-synthesis-oct7/arithmetic/check_full_matrix.py
python research/final-synthesis-oct7/w-beta/check_boundary_filter.py
python research/final-synthesis-oct7/w-beta/check_formal_direction.py
python research/final-synthesis-oct7/i120/check_transfer.py
```

These exact finite checks support the written proofs. Exploratory search
limits and internal proof audits have separate scopes; no search timeout
is recorded as a proof of nonexistence. Historical repository replay
reports retain their original scope and are not relabelled as fresh runs.
