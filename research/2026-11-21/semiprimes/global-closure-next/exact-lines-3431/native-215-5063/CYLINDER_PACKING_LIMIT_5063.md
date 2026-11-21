# The native 215 cylinder profile survives the exact packing hull

21 November 2026. **Exact limitation theorem. The original count 5063
remains open.**

The full native height-one cylinder model for `(a,b,c)=(35,13,43)`
has an exact rational feasible point with

\[
 n_1=215,\quad n_1^+=129,\quad n_1^-=86,\quad
 Q_0^+=42,\quad Q_0^-=1,
\]

all other signed gate currents zero, and positive gate capacities 94.
This point lies in the convex hull of actual contained, integral,
nonoverlapping **partial packings of exactly 215 height-one tiles**.
It therefore satisfies every linear inequality valid for that entire
packing set, including all point-packing and conflict-clique inequalities.

The required signs, gate currents, and cylinder endpoint equations hold
in the mixture. They are not asserted for any one integral component.
No integral configuration with the complete required profile, no full
physical endpoint solution, and no 5063 tiling is constructed.

The new five-block theorem leaves all 215 odd tiles at height one but
allows multiple phase classes. This note concerns one surviving
**native single-class profile**. It does not identify the native class
as the only possible five-block configuration.

## 1. A general finite lifting and packing lemma

The construction and its proof are those of
[the 3431 cylinder theorem](../CYLINDER_LIMIT.md), with changed parameters.
For completeness the general lemma used in both cases is as follows.

Let `a>b>0`, `a^2+ab+b^2=c^2`, and use integer axial coordinates for
one short-height class. A tile at `q`, rotation `j`, and hand `s` has
vertices `q`, `q-aU_j`, and `q+bU_(j+s)`. Let `x_(r,j,s)` be a
nonnegative rational torus endpoint solution, with integer total
population `n`, for residues modulo `cR`.

Fix an integer centre `(X_0,Y_0)`. Define `m(q)` by counting triples
`X,Y,K in {0,...,c-1}` giving

\[
 q=(X_0+X-K,\;Y_0-(c-1)+Y+K).
 \tag{1}
\]

Then `sum_(q congruent r) m(q)=c` for every residue. On each actual
supporting line, the remaining uniform parameter gives exactly one
representative of each longitudinal residue. Consequently

\[
 y_{q,j,s}=\frac{m(q)}c x_{(q\bmod c),j,s}
 \quad\Longrightarrow\quad
 A_{\rm cylinder}y=0,
 \tag{2}
\]

with all residue-column masses and hence all sign and gate data
preserved. The cylinder rows retain `y`, `x`, or `x+y` exactly and
periodize only the coordinate along the corresponding axis by `c`.

Suppose the entire support of (2), for all twelve orientations, admits
`M>n` distinct strictly contained translations by `cR`. Average those
translated lifts. If `T` is the finite translation set, put

\[
 \bar m(q)=\sum_{t\in T}m(q-ct),\qquad
 \bar y_{q,j,s}=\frac{\bar m(q)}{cM}x_{(q\bmod c),j,s}.
 \tag{3}
\]

For fixed `q`, the distinct preimages lie in one residue, so
`0<=mbar(q)<=c`. Every translation preserves gate residues and only
relabels actual supporting lines. Thus (3) preserves all the data of
(2) and has `ybar_q <= x_r/M`.

Distinct anchors in one fixed residue/orientation family differ by a
nonzero vector in `cR`, of Euclidean length at least `c`. The tile
diameter is `c`, so the corresponding tile interiors are disjoint.
At every point, at most one tile from each family can contribute.
Therefore the weighted coverage is at most `sum x_r/M=n/M<1`.

There is also an explicit fixed-cardinality convex decomposition. Let
`D=cM` and, in one residue/orientation family, let `w_q=n*mbar(q)`.
Then `0<w_q<D` and `sum w_q=nD`. Partition `[0,nD)` into consecutive
half-open integer intervals of lengths `w_q`. For each sampling offset
`t in {0,...,D-1}`, select the anchors whose intervals contain an
integer congruent to `t` modulo `D`. Exactly `n` intervals are selected,
and no interval is selected twice because its length is below `D`.
Each anchor occurs for exactly `w_q` offsets.

Choose the family with probability `x_r/n` and choose the offset
uniformly. The resulting marginal is

\[
 \frac{x_r}{n}\frac{n\bar m(q)}D=\bar y_q.
\]

Every component is an integral nonoverlapping contained partial packing
of exactly `n` tiles. The sign and gate requirements, and the endpoint
equations, remain statements about the average. This proves the lemma.

## 2. The exact source profile at 5063

The source is
[N5063_NATIVE_215_RATIONAL_CERTIFICATE.json.gz](../../five-block-two-heights/N5063_NATIVE_215_RATIONAL_CERTIFICATE.json.gz),
verified by
[verify_native_215_projection.py](../../five-block-two-heights/verify_native_215_projection.py).
The source defines an exact rational corrected point
`x_*=x_0+M^dagger(b-Mx_0)`. Its complete inverse-bound replay checks
all 1,849 Fourier blocks; the coefficient correction is bounded by

\[
 \|x_*-x_0\|_2^2\le\frac{78228810}{10^{24}}.
\]

The minimum approximate coordinate is `1538690768/10^12`, and

\[
 78228810<1538690768^2=2367569279528429824
\]

proves strict positivity. The source also exactly verifies all endpoint,
gate, population, and gate-capacity conditions. The present checker
reruns that source verification and records its hashes; it does not
rely on a floating feasible point or a saved optimizer status.

## 3. Exact contained geometry at 5063

Use the path frame divided by `z=(35+13 rho)/43`. The board vertices,
multiplied by `c`, are

\[
 (0,0),\quad(c^2(a+b),-c^2b),\quad(a^2(a+2b),ab(a+2b)).
\]

Apply (1) with centre `(1000,0)`, hence convolution shift `(1000,-42)`.
The support has 5,419 anchors. Every one of the twelve oriented tiles
at each anchor is strictly contained, giving **65,028** placed columns.
All 22,188 torus columns satisfy the exact operator identity
`A_cylinder L=E A_torus`. The verifier also checks 5,547 axis/residue
conditional marginals. The minimum board halfplane determinant across
the supported tile vertices is `739733128>0`.

The convex hull of all those tile vertices is the axial hexagon centred
at `(1000,0)` with radius `(c-1)+a=77`. A centre `(x,y)` gives a
contained radius-77 hexagon precisely when

\[
 13x+48y\ge3696,\qquad
 13x-35y\ge3696,\qquad
 48x+13y\le88109.
\]

For centres `(1000+43u,43v)`, the complete finite search box is

\[
 -23\le u\le24,\qquad -13\le v\le15.
\]

Exactly **410** such hexagons are contained, and all are strict. The
minimum accepted board halfplane determinant is `1468880>0`. The
replay records all 410 translations.

The averaged multiplicities from (3) have maximum 43 and support
855,572 anchors, or **10,266,864** oriented placed columns. All these
are actual strictly contained placements. Their density satisfies

\[
 \boxed{\text{coverage}(p)\le\frac{215}{410}=\frac{43}{82}<1
        \quad\text{for every point }p.}
\]

## 4. Exactly 215 tiles in each packing component

Here `D=cM=17630`, and every conditional interval has length at most
`215*43=9245<D`. Their total length in each residue family is
`215D=3790450`. The smallest family has 410 available anchors.

The interval difference checker verifies every one of the **32,597,870**
residue/sampling-offset cardinalities. Each selects exactly 215
distinct anchors. Including all twelve orientations and hands gives
391,174,440 convex components when repetitions are counted. Each has
weight `x_(r,j,s)/3790450`. The recipe specifies this finite family
exactly without materializing hundreds of millions of full packings.

Every component is a real integral nonoverlapping partial packing of
215 tiles. Each component has one orientation and one sign. Therefore
the target sign inventory `(129,86)`, signed gate profile `(42,1,0,...)`,
and cylinder equations are only guaranteed after averaging. No member
of the decomposition is asserted to satisfy that whole profile.

## 5. Consequence and limitation

Let `P_215` be the actual contained nonoverlapping native height-one
partial packings of exactly 215 tiles, and let `H` be the required
cylinder/sign/gate equations. The certificate constructs

\[
 \bar y\in\operatorname{conv}(P_{215})\cap H.
\]

This is not a point in `P_215 intersect H`. The intersection of a
convex hull with equations can be larger than the convex hull of
integral configurations satisfying those equations. Thus arbitrary
valid linear packing inequalities, even with exact cardinality 215,
cannot exclude this fractional candidate while only the stated linear
current equations are retained.

This does not limit an argument that couples packing geometry to
charge/current equations within one integer configuration, nor one
using full physical endpoint locations or the remaining even tiles.
It does not assert completeness of the cylinder model as a tiling
model, uniqueness of the native phase, or impossibility of 5063.

## 6. Reproduction

From the repository root:

```bash
python research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/native-215-5063/verify_5063_cylinder_packing.py
```

This standard-library verifier writes
`N5063_CYLINDER_PACKING_REPLAY.json`. Run without `-O` because the
imported source checker uses assertions. No LP/MIP solver is required.
