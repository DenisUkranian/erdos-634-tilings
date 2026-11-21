# Both two-cell native roles survive the full continuous endpoint model

21 November 2026. This is an exact limitation of a necessary relaxation for
the remaining 215 odd-tile mode of 5063. It is not a tiling construction,
and no integral individual tile multiplicities or nonoverlapping placements
are supplied.

**Theorem.** In the two-cell form with one native 215-node in the increasing
tree and a balanced 86-node plus a charged 129-node in the decreasing tree,
the full periodic endpoint model has a strictly positive rational solution
for each possible native role in the split tree. In both solutions:

* Cell sign populations are exactly `(43,43)` and `(86,43)`.
* Every cell gate current is an integer.
* Complete-node gate currents have the required exterior offsets modulo 22.
* Every positive and negative individual gate population satisfies its
  sign-specific bound, including the positive cap 51 in the charged cell.

Thus no additional valid linear dual inequality of this same continuous
periodic endpoint model can exclude either recorded current profile.
Stronger models may still exclude them; in particular the theorem leaves
integer individual columns, actual supporting lines, geometric matching,
and nonoverlap unresolved.

## 1. The two exact current profiles

Call the balanced cell `A` and the charged cell `B`. They share their
increasing-tree node, so that node's upward list is `Q_A+Q_B`.
Each decreasing-tree node contains only its indicated cell.
Every gate current not listed below is zero.

### Native balanced node

| Cell and hand | Gate 0 | Gates 9 and 11, each | Gates 2, 5, 12, 23, 27, 29 and 33, each |
|---|---:|---:|---:|
| A upward | 10 | -2 | -1 |
| A downward | 1 | 0 | 0 |
| B upward | 32 | 2 | 1 |
| B downward | 0 | 0 | 0 |

The complete upward current is 42 at gate 0. The native balanced downward
node has current 1 at gate 0, and the remote charged downward node has
zero current. Thus the nonzero whole-node charge units are

\[
E_{\rm up,native}(0)=-2,\qquad
E_{\rm down,native}(0)=2,
\]

because `42=86+22(-2)` and `1=-43+22(2)`.

### Native charged node

| Cell and hand | Gate 0 | Gate 11 | Gate 26 |
|---|---:|---:|---:|
| A upward | 1 | -2 | 1 |
| A downward | 0 | 0 | 0 |
| B upward | 19 | 2 | 21 |
| B downward | 1 | 0 | 0 |

The complete upward currents are 20 at gate 0 and 22 at gate 26. The
native charged downward node has current 1 at gate 0; the remote balanced
downward node has zero current. The nonzero whole-node charge units are

\[
E_{\rm up,native}(0)=-3,\qquad
E_{\rm up,native}(26)=1,\qquad
E_{\rm down,native}(0)=2.
\]

In both cases their total is zero, as required. These are equations for
complete nodes. The individual cell upward lists are not incorrectly
required to have the whole-node exterior offset or to be multiples of 22.

## 2. Exact rational correction certificate

Let `M` be the integer matrix with all 22,188 oriented residue tile columns,
three 43-by-43 endpoint tables, two 43-entry gate lists, and total population.
It has 5,634 displayed rows. For each of the four cell points above, the
certificate stores a rational approximate point `x_0` with common
denominator `D=10^12`. A uniform kernel distribution supplies a strictly
positive margin before rounding.

The target `b` has zero endpoint entries, the corresponding exact integer
gate list, and population 86 or 129. The earlier independently audited
[native 215 rational certificate](../../global-closure-next/five-block-two-heights/N5063_NATIVE_215_RATIONAL_REPLAY.json)
provides a bound for the same matrix, independent of this new right-hand
side:

\[
\|M^\dagger r\|_2^2\le3\|r\|_2^2
\quad\text{for every }r\text{ in the image of }M. \tag{1}
\]

The exact Fourier replay checks all 1,849 frequencies. The only omitted
endpoint modes are the 129 identically zero rows, and this new target has
zero entries there. The retained blocks have full row rank, so every
specified gate vector and population, with zero endpoint target, belongs
to the image. Therefore the residual `r=b-Mx_0` is in the image as well.

Define

\[
x^*=x_0+M^\dagger(b-Mx_0). \tag{2}
\]

The Moore–Penrose inverse of a rational matrix is rational, so (2) is an
exact rational vector and satisfies `Mx*=b`. No decimal solution is being
identified with the exact witness. Write `R=D^2 ||r||_2^2` and let `m` be
the smallest numerator of `x_0`. The checker proves `3R<m^2` for each cell.
By (1), every coordinate of the correction has absolute value below
`m/D`, proving strict positivity of (2).

The checker also reconstructs every positive and negative gate bin.
Each bin has 129 coordinates. If `s/D` is its smallest remaining slack to
the applicable cap, the exact inequality `129^2*3R<s^2` proves that the
correction preserves every cap. Total population together with signed
gate sum fixes the stated positive and negative masses exactly.

The endpoint columns used for these checks are reconstructed from actual
counterclockwise triangles. The verifier identifies short edges from
their exact squared lengths and does not import the LP discovery code.

## 3. Files and replay

The deterministic compressed
[`TWO_CELL_RATIONAL_CERTIFICATE.json.gz`](TWO_CELL_RATIONAL_CERTIFICATE.json.gz)
contains both native roles. It references the previously published Fourier
bound certificate by its repository path and SHA-256 digest, avoiding a
duplicate copy of all inverse blocks. The new replay recomputes that
bound; it does not merely trust the earlier report.

```sh
python3 verify_two_cell_rational_witness.py
```

This uses only the Python standard library and exact integer/Fraction
arithmetic. The recorded output is
[`TWO_CELL_RATIONAL_REPLAY.json`](TWO_CELL_RATIONAL_REPLAY.json).
`build_two_cell_rational_witness.py` documents how the approximate rational
points were packaged from the saved LP discovery supports; the build step
is not needed to verify the certificate.

The [ten new cell duals](SHARED_NODE_DUALS.md) remain valid useful cuts and
exclude their individual earlier candidate profiles. They cannot exclude
these new exact rational points, because every one of their inequalities
is valid on the full endpoint model just certified feasible. The earlier
65-certificate contradiction for an isolated 129-cell remains valid: both
complete gate lists there belong to one cell, a condition not present in
these two-cell configurations.
