# The 3431 minimal mode survives the full periodic endpoint relaxation

21 November 2026. **Theorem.** For `(a,b,c)=(33,7,37)`, the full
periodic endpoint model admits a strictly positive **rational** placement
weight vector with:

\[
 n=111=3c,\qquad n_+=74,
 \qquad n_-=37,
\]

\[
 Q_0^+=22,\qquad Q_0^-=15,
 \qquad Q_r^+=Q_r^-=0\quad(r\ne0).
\]

Every positive gate population is below 44. The corresponding exact
neighboring-node charge units are

\[
 g_0^+=-2,\qquad g_0^-=2,
 \qquad g_r^+=g_r^-=0\quad(r\ne0).
\]

Thus the finite-profile endpoint exclusion used for 5063 cannot exclude
every 3431 profile merely by adding further valid linear certificates
from **this same relaxation**. This is not a physical tiling, a packing,
or an assertion that a 3431 tiling exists. Positions, individual real
supporting lines, nonoverlap, integrality of individual tile counts,
and the full geometry of balanced branches are not retained by the
periodic relaxation.

The theorem is certified by integer and rational arithmetic. The proof
does not treat a numerical feasible point or a small numerical residual
as an exact solution.

## 1. An explicit rational witness formula

Let `M` be the integer matrix with one column for each of the
`12c^2=16428` tile residue classes `(q,j,s)`. It records all `3c^2`
two-coordinate short-edge endpoint rows, all `2c` signed gate rows,
and one total-population row. Thus it has 4182 rows.

The endpoint and gate columns are exactly those of
[the complete residue formulation](../../../2026-11-20/semiprimes/continuation/global-closure/median/PER_GATE_INTEGRALITY.md).
For clarity, with `u=q-aU_j`, `w=q+bU_(j+s)`, the endpoint entries
are `+s` at `(j,q)`, `-s` at `(j,u)`, `+s` at `(j+s,w)`, and
`-s` at `(j+s,q)`, with axis indices modulo three and point coordinates
modulo `c`. The gate entry is `epsilon=s(-1)^j`, at `phi(u)` for
`s=+1` and at `psi(u)` for `s=-1`.

Let `b_0` have zero endpoint entries, gate entries 22 and 15 at the
two native gates and zero at all remote gates, and population entry
111. The certificate supplies a rational vector `x_0` with common
denominator `D=10^12`. Define

\[
 \boxed{x_*=x_0+M^\dagger(b_0-Mx_0),}
 \tag{1}
\]

where `M^dagger` is the Moore--Penrose inverse. Formula (1), the
explicit integer matrix rules, and the stored rational vector specify
the witness exactly. The certificate proves both that `b_0` is in
the image of `M` and that the correction is smaller than every
coordinate of `x_0`.

The witness is rational, despite the Fourier analysis used to bound
it. Indeed choose a rational full-rank factorization `M=BC`, with
`B` of full column rank and `C` of full row rank. Then

\[
 M^\dagger=C^T(CC^T)^{-1}(B^TB)^{-1}B^T
\]

has rational entries. The verifier does not need to expand this large
rational matrix: a finite, independently checked inverse-norm bound
certifies (1) directly.

## 2. The finite Fourier blocks

Let `zeta=exp(2*pi*i/c)`. For a two-coordinate field use the unitary
transform

\[
 \widehat f(k)=\frac1c\sum_{q\in(\mathbb Z/c\mathbb Z)^2}
 f(q)\zeta^{k\cdot q}.
\]

There are twelve tile orientation fields. The endpoint operator is
translation invariant, so at frequency `k=(k_x,k_y)` its row for
axis `i` has coefficient

\[
 s\,\mathbf1_{i=j}(1-\zeta^{k\cdot(-aU_j)})
 +s\,\mathbf1_{i=j+s}(\zeta^{k\cdot bU_{j+s}}-1)
 \tag{2}
\]

on orientation `(j,s)`.

If `k dot U_i=0 mod c`, the entire axis row is identically zero;
it is omitted. The desired endpoint right side is zero, so all these
omitted equations are satisfied. There are exactly `3c=111` such
zero Fourier endpoint rows, counting axes separately.

The upward gate field has Fourier components only on the frequency
line `k=r(-b,a)`; the downward field has them only on `k=r(a,-b)`.
At a nonzero frequency on either line, add the corresponding gate
row

\[
 \epsilon\,\mathbf1_{\text{matching hand}}
 \zeta^{k\cdot(-aU_j)}.
 \tag{3}
\]

To obtain (3), transform each gate field unitarily in its one residue
coordinate and divide that output by `sqrt(c)`. At frequency zero,
use the two gate-total rows and the population row, all divided by
`c` in physical coordinates. Their coefficients are respectively
`epsilon*1_(s=+1)`, `epsilon*1_(s=-1)`, and one.

The two gate-frequency lines are distinct: `b^2-a^2` is nonzero
modulo 37. The resulting blocks `B_k` have twelve columns and at
most four rows. The exact replay checks:

| Number of rows | Number of blocks |
|---:|---:|
| 2 | 108 |
| 3 | 1189 |
| 4 | 72 |

All 1369 blocks have full row rank. This is certified below, rather
than inferred from floating singular values. Consequently the only
row restrictions on `M` are the omitted zero endpoint modes. Since
`b_0` satisfies them, `b_0` lies in the image of `M`.

## 3. A rigorous inverse bound, with no floating proof step

For every block the certificate supplies a rational approximate inverse
`C_k` to `G_k=B_k B_k^*`. The checker proves

\[
 \|I-C_kG_k\|_\infty<\tfrac12,
 \qquad 2\|C_k\|_\infty\le3.
 \tag{4}
\]

The matrix norm uses the upper estimate `|Re z|+|Im z|` for the
absolute value of each complex entry. It is submultiplicative and
dominates the usual complex row-sum norm. The Neumann-series bound
therefore gives `||G_k^(-1)||_infinity <= 3`. Since the true Gram
matrix is Hermitian positive semidefinite and is invertible by (4),

\[
 \lambda_{\min}(G_k)\ge\tfrac13.
 \tag{5}
\]

All root-of-unity estimates in (4) are enclosed rigorously. The checker
uses Machin's formula

`pi = 16 arctan(1/5) - 4 arctan(1/239)`

with alternating-series rational bounds, followed by sine and cosine
Taylor bounds. Every stored real and imaginary root component has
error at most `10^(-12)`. With `Q=10^12`, each block entry error
is at most `2/Q` in `|Re|+|Im|`, and each approximate entry has
size at most three. Summing twelve products bounds a Gram entry's
error by `200/Q`. Integer matrix multiplication and this error bound
establish (4). The floating inverse computation used in discovery is
not called during verification.

The endpoint transforms are unitary. The gate transforms followed
by division by `sqrt(c)`, and population division by `c`, can only
decrease the output norm. Equations (2)--(5) therefore provide, for
every consistent real residual `r`, a real correction of norm at
most `sqrt(3)*||r||_2`. One may take the real part of the Fourier
correction if necessary. The least-norm correction `M^dagger r`
has no larger norm. In particular,

\[
 \|M^\dagger(b_0-Mx_0)\|_2^2
 \le3\|b_0-Mx_0\|_2^2.
 \tag{6}
\]

## 4. Exact positivity and gate-capacity checks

The stored point has

\[
 \min_i(x_0)_i=\frac{346672370}{10^{12}},
 \qquad
 \|b_0-Mx_0\|_2^2=\frac{988020}{10^{24}}.
\]

The following strict integer inequality proves every coordinate of
(1) positive:

\[
 3\cdot988020=2964060
 <346672370^2=120181732121416900.
\]

Thus (1) is an exact nonnegative solution of all full two-coordinate
endpoint equations and the specified gate and population equations.
Its total signed tile count is the sum of all signed gate currents,
namely `22+15=37`. Combining this with its population 111 gives
positive and negative masses exactly 74 and 37.

There are `3c=111` positive tile columns in each gate bin. Each
coordinate correction is bounded by the norm in (6), so a bin's
change is at most 111 times that norm. The minimum gate-capacity
slack of `x_0`, measured in numerator units with denominator
`10^12`, is `21961519366946`. The verifier checks

\[
 111^2\cdot3\cdot988020
 =36520183260
 <21961519366946^2.
\]

Every positive gate mass of the corrected witness therefore remains
strictly below 44. The neighboring charges are exactly integral:
`(22-2*37)/26=-2`, `(15+37)/26=2`, and all remote entries zero.
They also satisfy the signed population and remote-charge reserve
bounds used in the finite-profile method.

## 5. Consequence and exact scope

Because the rational witness satisfies every inequality obtained by
linear combination of the full periodic endpoint equations and
nonnegative tile columns, no collection of such valid dual cuts can
exclude this profile at population 111. Adding the gate-current
integrality and positive gate caps used here does not remove it.

A stronger method may still exclude a 3431 tiling by retaining
individual supporting lines, requiring integral individual placements,
controlling actual contacts or empty-gate mates, or imposing additional
geometric consequences on balanced branches. None of these conditions
is claimed for the witness. The original existence question remains
**OPEN**.

## 6. Reproduction and data

Run:

```sh
python3 verify_3431_rational_projection.py
```

This uses only the Python standard library and reads
`N3431_RATIONAL_PROJECTION_CERTIFICATE.json`. It writes
`N3431_RATIONAL_PROJECTION_REPLAY.json`, checking the root enclosures,
every Fourier inverse certificate, all rational endpoint and gate
residuals, positivity, exact sign totals, and gate capacities.

`build_3431_projection_certificate.py` is the optional NumPy discovery
script. Its numerical source point is recorded separately in
`N3431_NATIVE_PROFILE_IPM.json`; no numerical feasibility status is
used as a proof. The earlier dual-simplex timeout in
`N3431_NATIVE_PROFILE_PROBE.json` is also explicitly inconclusive and
has no role in the certificate.
