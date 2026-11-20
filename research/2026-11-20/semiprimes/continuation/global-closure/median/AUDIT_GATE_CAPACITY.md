# Independent audit of the Euclidean-class gate capacity

21 November 2026. Mathematical and code review, followed by an exact
standard-library certificate replay. No optimization or geometric
tiling search was performed.

| Reviewed file | SHA256 |
|---|---|
| `NATIVE_GATE_CAPACITY.md` | `53c68ecbb3c3537b9f01272d591e88374137dd39c3e7d16c800829ab8cc77baa` |
| `gate_capacity_certificates.json` | `da57da6086a51e01fd618c2c3afbdef32181c6af55a930e02b0af2eac0a6b38b` |
| `verify_gate_capacity.py` | `cdedcf765eda3358cf6f3d94a4d64f99711f00401e32313f23786e5a7783ff84` |

**Assessment:** the corrected single-class gate theorem and its
minimal-odd-population application are sound. The statement requires
the exterior weight hypotheses explicitly retained in the final note.
Neither whole-board native localization nor a bounded placement
catalogue is needed for the single-class theorem.

## Isolation of one Euclidean class

After translating by `q_0` and dividing by `z^h`, all selected-class
vertices lie in `R`. The upward gate is exactly `u/z in R`, equivalent
to `a*u_y-b*u_x=0 mod c`. Shifting the representative `q_0` within
the same class covers every one of its possible upward gates; this
uses the surjectivity of the displayed linear form modulo `c`.

The endpoint potential is defined at every actual point, with value
zero outside the selected class. Every whole long side of height `h`
has displacement `c*z^h*rho^j`, so either both endpoints are outside
the class or both are inside with equal residues. Such a side has
weight zero. Other short-height-`h` classes have zero weight as well.
Telescoping and reversal therefore isolate exactly the selected
class's short-edge weights from the entire tiling. Partial contacts
and disconnected class components do not change the argument.

## Finite inequalities and exact controls

The checker reconstructs the CCW triangles and their two short-edge
contributions from integer coordinates without importing an LP model.
The certificate is exhaustive over the residue lattice: every
translation changes the weight and gate only through its residue,
and every hand and rotation is checked.

The independent replay passed all 588 control columns, 16,428 columns
for `(33,7,37)`, and 22,188 columns for `(35,13,43)`. Every integer
slack was nonnegative, with minimum zero. Summing the checked
inequality and using the stated zero boundary weight gives exactly

`222*P_g <= 43*n_+ + 179*n_-`

and

`43*P_g <= 8*n_+ + 35*n_-`.

Both complete positive 143 controls were also retained. Their actual
height-one signs are `(56,49)` and `(49,42)`; each has 14 positive
tiles through the chosen native upward gate. The endpoint sums are
exactly zero, and the bounds are respectively `105/2` and `91/2`.
These are checks against already verified complete tilings, not
assumptions about target completions.

## Exterior-weight correction and symmetries

One issue in the initial draft was corrected before this audit was
finalized. Zero outer weight for the original table does not by
itself imply zero outer weight for its reflected or half-turned
pullback. The supplied tables are not generally even or odd.

The final note now correctly requires the corresponding boundary
term to vanish for each symmetry variant used. Absence of exterior
sides at the chosen height is sufficient for all variants and applies
to every height-one application here. Otherwise the appropriate
boundary correction must remain in the inequality.

The geometric symmetries themselves are correct. A half-turn reverses
the sign and preserves the selected gate. In normalized coordinates,
`w -> -conjugate(w)` exchanges upward and downward gates and maps
`(j,s)` to `(3-j,-s)`, preserving the sign.

## Bank bound and the surviving minimal case

Under both sign-specific zero-boundary hypotheses, apply the two
capacities to the positive and negative subsets of a specified bank.
Writing its size as `m`, its signed sum as `K`, and the full class
charge as `G_L`, the two inequalities are equivalent to

`n_L-m >= K+beta*G_L` and `n_L-m >= -K-beta*G_L`.

This proves `n_L >= m+|K+beta*G_L|` without adding populations from
different gates or counting neighbors twice.

In the hypothetical `3c` odd-population case, the actual median
localization supplies the single class, signs `(2c,c)`, and the common
native upward gate for all long-height-two bank steps. The current
formulas give `K=2c-d*n`. The exact gate bounds are `265/6` and `51`,
so the integer positive-gate limits 44 and 51 exclude `n=0,1` in
both cases. The remaining parameters are `2,3,4` at 3431 and
`2,3,4,5` at 5063, as stated.

No residual mathematical error was found after the exterior-weight
correction. These exclusions do not remove all `3c` cases or establish
an unrestricted `5c` bound.
