# An exact fractional witness survives in the native 215 model

21 November 2026. The two-height exclusion leaves a hypothetical
5063 tiling with 215 odd tiles at short height one. This note proves
that its **single native class alternative is feasible in the full
fractional periodic endpoint model**. The witness has rational
multiplicities, strictly positive in every residue column. It is not
a physical tiling, and no integer tile-multiplicity witness is asserted.

Thus additional linear inequalities derived only from this same
fractional periodic model cannot exclude the displayed profile.
Actual supporting-line location, integer multiplicities, or other
geometric conditions can still impose stronger restrictions.

## 1. Exact statement and model

Use `(a,b,c)=(35,13,43)`, `d=22`, and normalize the native height-one
class `zR` by dividing by `z`. There are `12c^2=22,188` variables

\[
 x_{u,v,j,s}\ge0,
 \quad u,v\in\mathbb Z/43\mathbb Z,
 \quad 0\le j<6,
 \quad s\in\{-1,+1\}.
\]

They are the fractional multiplicities of all translations and
orientation/hand types of the tile. Write
`q=(u,v)`, `beta=q-a U_j`, `alpha=q+b U_(j+s)`, where
`U_j` are the six standard axial unit vectors, and put
`epsilon=s*(-1)^j`.

An integer matrix `M` records the following quantities:

* The three axis-specific endpoint currents at every residue point.
  A column contributes `+s` at `(j,q)`, `-s` at `(j,beta)`,
  `+s` at `(j+s,alpha)`, and `-s` at `(j+s,q)`, with axis
  labels reduced modulo three and point coordinates modulo 43.
* The 43 upward and 43 downward signed gate currents. A column
  contributes `epsilon` at its hand's gate, whose residue at `beta`
  is `a beta_y-b beta_x` upward and `a beta_x-b beta_y` downward,
  modulo 43.
* Total population, with coefficient one in each column.

There are `3c^2+2c+1=5,634` recorded equations, including their
linear dependencies. The target vector `b` has zero endpoint currents,
total population 215, and gate currents

\[
 Q_+(0)=42=86+22(-2),\qquad
 Q_-(0)=1=-43+22(2),\qquad
 Q_\pm(r)=0\quad(r\ne0).                         \tag{1}
\]

The two exact-node charge integers are therefore `-2,+2`, with
all remote charge integers zero. Their sum vanishes. The total
signed gate current is 43; together with total population 215, this
fixes the positive and negative sign masses at 129 and 86.

**Theorem.** There is an exactly specified rational vector `x_*`
with every coordinate strictly positive, `M x_*=b`, and every
positive gate population strictly less than

\[
 (8\cdot129+35\cdot86)/43=94.                       \tag{2}
\]

Every negative gate population also satisfies its certified capacity
`(8*86+35*129)/43=121`, because its entire negative sign mass is only
86. The theorem is conditional only on the definition of this
fractional relaxation; it does not assert existence of the tiling
from which the necessary model was derived.

## 2. The rational witness

The deterministic compressed certificate
[`N5063_NATIVE_215_RATIONAL_CERTIFICATE.json.gz`](N5063_NATIVE_215_RATIONAL_CERTIFICATE.json.gz)
stores a rational approximate vector `x_0`. All its coordinates have
denominator `D=10^12`; they are one common positive numerator plus
5,029 listed increments. The exact witness is

\[
 \boxed{x_*=x_0+M^\dagger(b-Mx_0),}                 \tag{3}
\]

where `M^dagger` is the Moore--Penrose inverse of the explicitly
defined integer matrix. This formula, the matrix rules above, and
the stored integers specify every coordinate exactly, without
expanding a large matrix of rational numbers.

The pseudoinverse of a rational matrix is rational. For example,
choose a rational full-rank factorization `M=BC`. Then

\[
 M^\dagger=C^{\mathsf T}(CC^{\mathsf T})^{-1}
 (B^{\mathsf T}B)^{-1}B^{\mathsf T}
\]

has rational entries. The remaining obligations are to establish that
`b` belongs to the range of `M` and that the correction in (3) is
small enough to preserve strict positivity and the capacities.

## 3. Range and exact correction bound

We use the parameterized Fourier-block proof from
[`N3431_PROFILE_LIMIT.md`](../../global-invariant/N3431_PROFILE_LIMIT.md)
and its independently reviewed
[`verify_3431_rational_projection.py`](../../global-invariant/verify_3431_rational_projection.py).
The new certificate is recomputed and checked at `c=43`; no numerical
bound from `c=37` is assumed.

Under the unitary two-coordinate transform, precisely the endpoint
rows with frequency perpendicular to their axis vanish identically.
There are `3c=129` such rows, and all their target entries are zero.
Every remaining transformed equation belongs to one of 1,849 blocks.
The gate-output normalizations divide by `sqrt(c)`, and the
zero-frequency population normalization divides by `c`, so these
normalizations cannot enlarge the original residual norm.

For each block the certificate supplies a rational approximate inverse
of its Gram matrix. The exact checker encloses all 43 roots of unity
using rational Machin and Taylor bounds, includes the full root
enclosure error in every Gram entry, and verifies an inverse residual
below one half. The resulting Neumann-series bound proves full row
rank of every nonzero block and gives the uniform inverse norm bound
`K=3`. The block sizes and counts are:

| Rows in a block | Number of blocks |
|---:|---:|
| 2 | 126 |
| 3 | 1,639 |
| 4 | 84 |

Their total row count is 5,505, exactly `5,634-129`. This proves the
required range condition. The same contraction and least-norm
argument as in the cited general proof yields

\[
 \|M^\dagger r\|_2^2\le3\|r\|_2^2,
 \qquad r=b-Mx_0.                                  \tag{4}
\]

The verifier uses only integer and rational arithmetic for this
conclusion. Floating optimization is used solely to discover `x_0`.

## 4. Strict positivity and gate capacities

The checker reconstructs all 22,188 column contributions and all
5,634 equations over the common denominator. Its exact values are

\[
 \min_i D(x_0)_i=1,538,690,768,
 \qquad D^2\|r\|_2^2=26,076,270.
\]

Consequently

\[
 3\cdot26,076,270
 =78,228,810
 <(1,538,690,768)^2
 =2,367,569,279,528,429,824.                         \tag{5}
\]

Every coordinate correction is bounded by the Euclidean norm in
(4), so (5) proves strict positivity of every coordinate in (3).

Each positive gate bin contains `3c=129` variables. Its change is
therefore at most `129*||M^dagger r||_2`, a conservative bound.
The minimum approximate slack below capacity 94 has numerator
`51,801,508,890,894`. The exact replay verifies

\[
 129^2\cdot3\cdot26,076,270
 =1,301,805,627,210
 <(51,801,508,890,894)^2.                           \tag{6}
\]

Thus all positive gate capacities remain strictly satisfied after
correction. The exact equality constraints establish the sign masses
and gate currents stated in Section 1. This completes the proof.

## 5. Reproduction, discovery data, and limits

From the repository root, run

```sh
python3 research/2026-11-21/semiprimes/global-closure-next/five-block-two-heights/verify_native_215_projection.py
```

The exact replay uses Python's standard library and writes
[`N5063_NATIVE_215_RATIONAL_REPLAY.json`](N5063_NATIVE_215_RATIONAL_REPLAY.json).
The certificate's compressed SHA-256 is
`9ef122e71386df768bf0d3930d3826a62addfdba49d1ae14617adb3ced21ebec`.
Its gzip timestamp is zero. The verifier also records the hash of the
parameterized Fourier dependency.

The optional discovery script `probe_native_215.py` solves only this
one fixed continuous profile. Its saved numerical point has population
about 180.85953; adding a uniform vector raises the population to 215
without changing endpoint or signed gate currents. The compressed
discovery output and `build_native_215_projection.py` permit rebuilding
the certificate. Neither the discovery optimizer's status nor its
reported optimum is used as a proof.

This positive witness explains a concrete limit of the previous
profile method at the next population. It supplies no actual tile
coordinates on the board, no disjoint interiors, no complete even
population, and no integer multiplicities for the 215 odd tiles.
It does not negate the two-height exclusion or the exact one-, two-,
and four-cell classification. The single native-class alternative
remains open in the actual geometric problem, as do the other
remaining cases and the count 5063 itself.
