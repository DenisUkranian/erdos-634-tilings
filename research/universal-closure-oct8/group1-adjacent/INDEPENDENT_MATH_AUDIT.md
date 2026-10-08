# Independent mathematical audit of the adjacent W construction

8 October 2026. This audit checks the symbolic argument for every integer
`u>=2`, not an inference from the first numerical examples. The checked
sources are [PROOF.md](PROOF.md),
[`adjacent_formula.py`](../group1/adjacent_formula.py), and
[`check_adjacent_symbolic.py`](../group1/check_adjacent_symbolic.py).

**Conclusion: PASS.** The macro construction, the one-tile exchange,
and the positive-boundary argument give a genuine tiling for every
stated parameter. This is an independent internal audit, not external
peer review or an assertion of literature priority.

## 1. The central strip is a positive uniform construction

Put `v=u+1`, `b=2u+1`, and define

```
d=(uv,−u²),  e=(0,ub),  P_j=P_0−j d,  P_0=(−v,u).
```

The j-th square, its upper B-grid triangle, and its lower B-grid triangle
have union exactly the parallelogram

```
[P_j,P_j+d,P_j+d+e,P_j+e].
```

Successive parallelograms share an entire vertical edge and have
interiors in consecutive disjoint x-intervals of positive width uv.
Their union, for `j=0,...,u`, is therefore one larger parallelogram.
The prescribed central strip omits the lower triangle at j=0 and
removes one B-unit from the upper corner at j=u. Both deletions are
whole triangular corners, giving the six-vertex convex polygon used
in the symbolic checker.

The upper-left apex is `F=P_u+e`. For
`V=(−u²(u+2),uv(u+2))` and `k=u²−u−1`, direct expansion gives

```
F−V=(k,−u²)=H.
```

The other removed vertices become `H+(0,−u)` and `H+(v,−u)`, precisely
the extra unit K,R in the left cap. Thus the claimed exchange is an
identity of positioned triangles for every u; equality of shapes or
areas alone is not being substituted for equality of positions.

## 2. Exact boundary cancellation really proves a dissection

The symbolic checker proves positive areas and convexity for every
macro polygon, using nonnegative polynomial coefficients after
`u=t+2`, `t>=0`. The central polygon is the explicitly truncated
parallelogram just described; the remaining polygons are triangles or
quadrilaterals with positive grid dimensions. No polygon winds around
its own boundary more than once.

For each supporting line, the checker stores signed endpoint events.
Their exact cancellation means the oriented boundary multiplicity is
constant along that line. It is zero beyond the finite collection of
segments, so it is zero everywhere on the line. Keeping the direction,
the supporting-line offset, and the exact endpoint prevents cancellation
of edges at different positions.

After adding the four outside macros, the full boundary identity is
that of one positively oriented target triangle. If the positive macro
polygons are `P_i` and that triangle is T, the compactly supported
integer-valued function

```
f = sum_i 1_(P_i) − 1_T
```

has zero distributional boundary. It is constant on the plane and is
zero outside a sufficiently large disk; hence `f=0` almost everywhere.
Therefore macro interiors are disjoint and cover T. Containment and
nonoverlap are conclusions of this argument, not assumed inputs.
Refining each macro by its stated grid then gives an actual tiling.

The direction polynomials used by the checker are nonzero for `u>=2`.
Any accidental coincidence of two symbolic supporting-line families at
a particular u could only merge two separately zero currents, so it
would not invalidate the implication.

## 3. The oblique metric and the A/B unit tiles

The physical squared norm in the displayed oblique coordinates is

```
Q(x,y)=v²(x²+y²)+[u(3v²−u²)/v]xy.
```

The determinant of its Gram matrix is

```
(v²−u²)²(4v²−u²)/(4v²)>0.
```

Thus it is a genuine Euclidean metric throughout the claimed range.
Furthermore

```
Q(u,0)=(uv)²,
Q(0,v)=v⁴,
Q(u,−v)=(v²−u²)²=b².
```

Interchanging x,y gives the same three side lengths for the B tile.
Every A or B grid cell consequently uses the original `(uv,b,v²)`
triangle, including the swapped rectangular grids and exchanged unit.

For the three outside annular grids, the checked homothety ratios r:s
and side lengths prove that each is an ordinary r-fold tile triangle
with an s-fold corner removed. Their parameters satisfy `r>s>0` for
`u>=2`; the fourth outside region is the ordinary `(u+2)`-fold grid.
The symbolic metric checks therefore certify the entire construction,
not only the residual A/B grids.

## 4. Target shape, count, and non-similarity

Writing `m=u+2` and `Q0=2v²−u²`, the target sides obtained from its
vertices are

```
m v³,  m u Q0,  m v b.
```

The exact area identity gives

```
N=Q0 m²=(u+2)²((u+2)²−2).
```

The target is not similar to the tile. The tile's ordered sides are
`b<uv<v²`. The target's ordered sides are
`m v b < m v³ < m u Q0`, since

```
uQ0−v³=u²−u−1>0.
```

Its smallest-to-middle ratio is `b/v²`, whereas the tile's is `b/(uv)`;
they differ because `u!=v`. Consequently the construction supplies the
required non-similar triangular tilings, and not merely subdivisions of
a triangle similar to the tile.

The resulting infinite family is therefore

```
N=t²(t²−2),  tile=((t−2)(t−1),2t−3,(t−1)²),  t>=4.
```
