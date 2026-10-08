# Independent audit of the general corner filling criterion

This proof concerns the corner quadrilateral used in the companion F3
construction. It is independent of the placement enumeration and of the
480-tile numerical certificate.

Let `a,b,c` be positive integers with `c²=a²+ab+b²`. Put

\[
k=a-2b>0,\qquad D=b^2-ak.
\]

Suppose there are nonnegative integers `s,t,q` such that

\[
D=sa+tb+qc. \tag{1}
\]

Then the ordinary `2b`-fold tile triangle with its reflected `k`-fold
corner triangle removed has a tiling by

\[
4b^2-k^2
\]

congruent `(a,b,c)` triangles. This includes q=0 as a geometric
degeneration. For a primitive triple in this range, q=0 is impossible
arithmetically, as proved below.

## Coordinates and containment

Use axes along the two short sides of an ordinary tile, at angle 120
degrees. Their coordinates `(X,Y)` are related to standard Eisenstein
coordinates by `(x,y)=(X-Y,Y)`. The metric is

\[
\|(X,Y)\|^2=X^2-XY+Y^2.
\]

The corner quadrilateral is

\[
Q=[(bk,0),(2ab,0),(0,2b^2),(0,ak)].
\]

Write `r=sa+tb=D-qc`. In particular `ak+r+qc=b²`, so `ak≤b²`.
The following pieces partition Q with disjoint interiors:

1. The right triangle
   `R=[(ab,0),(2ab,0),(ab,b²)]`.
2. The rectangle `[0,ab]×[0,ak]` with
   `[(0,0),(bk,0),(0,ak)]` removed.
3. The strip `[0,ab]×[ak,ak+r]`.
4. The upper triangle
   `T=[(0,ak+r),(ab,ak+r),(0,ak+r+b²)]`.
5. The parallelogram
   `P=[(0,2b²),(0,2b²-qc),(ab,b²-qc),(ab,b²)]`.

For an explicit coverage check, when `0≤X≤ab` the lower boundary of Q
is `max(0,ak-aX/b)` and its upper boundary is `2b²-bX/a`.
The four pieces on this interval have successive top levels

\[
ak,\quad ak+r,\quad 2b^2-qc-bX/a,\quad 2b^2-bX/a.
\]

Their successive lower levels coincide with the preceding top levels;
the first piece has the stated lower boundary of Q. When
`ab≤X≤2ab`, the remaining section of Q is precisely R. This proves
coverage and disjointness, including degenerate empty strips or P.

## Tiling each piece

Both R and T are b-fold ordinary tile triangles, with `b²` tiles each.

The lower rectangle has `a` columns of width b and `k` rows of height
a. Split each elementary parallelogram into two reflected ordinary
tiles. Its corner k-fold triangle is exactly a union of `k²` of those
tiles. Since `k=a-2b<a`, this triangle is contained in the rectangle.
The remaining region therefore has `2ak-k²` tiles.

Split the strip of height `r=sa+tb` into s strips of height a and t
strips of height b. The width ab is a multiple of both a and b, so
ordinary two-tile parallelogram grids fill these strips. Their total
tile count is `2r`.

For P, work in the same 120-degree coordinates and define

\[
v_1=\left(\frac{ab}{c},-\frac{b^2}{c}\right),
\qquad
v_2=\left(\frac{ab}{c},\frac{a(a+b)}{c}\right),
\qquad w=v_2-v_1=(0,c).
\]

The identity `c²=a²+ab+b²` gives

\[
\|v_1\|=b,\qquad \|v_2\|=a,\qquad \|w\|=c.
\]

Each parallelogram spanned by `v1` and w splits along its diagonal
`v1+w=v2` into two congruent `(a,b,c)` triangles. Starting at
`(0,2b²-qc)`, P is spanned by `c*v1=(ab,-b²)` and `q*w=(0,qc)`.
It is therefore a c-by-q grid of these parallelograms and contains
`2cq` tiles. No assertion about tiling an arbitrary parallelogram is
needed.

The total count is

\[
b^2+(2ak-k^2)+2r+b^2+2cq
=4b^2-k^2,
\]

using `ak+r+cq=b²`. Every piece was filled by an explicitly described
finite grid. Thus this is a constructive sufficiency theorem, not an
inventory relaxation.

## Primitive form of the arithmetic criterion

For `gcd(a,b)=1`, condition (1) is exactly

\[
D\in\langle a,b,c\rangle.
\]

Any such representation automatically has q≥1. Indeed, if
`D=sa+tb`, reduction modulo b gives `s≡-a≡b-k (mod b)`.
Here `0<k<b`, since D≥0 implies `a/b≤1+sqrt(2)<3`.
Consequently `sa≥a(b-k)>b²-ak=D`, a contradiction; the strict
difference is `b(a-b)>0`.

## Specialization to 4830

For `(a,b,c)=(24,11,31)`,

\[
k=2,\quad D=73=11+2\cdot31,\quad r=11,\quad q=2.
\]

The five tile counts are

\[
121+92+22+121+124=480.
\]

Converting Q to standard Eisenstein coordinates gives exactly
`[(22,0),(528,0),(-242,242),(-48,48)]`, the independently verified
480-tile certificate. The companion general F3 construction supplies
the remaining 4350 tiles in the 4830 example.

## Scope

This is a sufficient construction criterion. Non-membership in the
semigroup does not prove nonexistence of an F3 tiling. The full F3
insertion and its other pieces are proved separately in
`../f3-general/`; the audit here establishes the corner theorem
without relying on that insertion.

## Audit of the companion implementation and canonical isometry

The implementation `../f3-general/construct_mixed_corner.py` uses
the other corner of each elementary parallelogram. In its notation,

\[
u=c\rho^{-1},\qquad v=b\overline z,\qquad
z=(a+b\rho)/c.
\]

Direct multiplication gives

\[
u-v=\frac{(a^2,-a(a+b))}{c}
     =a\overline z\rho^{-1}.
\]

Hence its code triangles `[o,o+u,o+v]` and
`[o+u,o+u+v,o+v]` have precisely the required lengths. The c-by-q
loop bounds, strip widths, two b-grid triangles, and cut-rectangle
inequalities `i+j>=k` / `i+j>=k-1` agree with the proof above.
The second inequality retains the upper half-cell immediately above
the k-fold corner boundary, as required.

For the insertion implemented in `reduce_corner.py`, write
`Z=a+b*rho`, `h=a+2b`, and `z=Z/c`. Its vectors simplify exactly to

\[
u_{\rm out}=-a z^2,\qquad v_{\rm out}=b\rho z^2,
\qquad O=T+a v_{\rm out}.
\]

The reported embedding of a canonical Eisenstein point `w=x+y*rho`
is therefore

\[
\begin{aligned}
E(w)&=O+(x+y)u_{\rm out}/a+yv_{\rm out}/b\\
    &=O-z^2\overline w.
\end{aligned}
\]

Since `|z|=1`, this is exactly a reflection followed by a rotation and
translation. It preserves every tile metric; the implementation's
orientation correction is appropriate because the map reverses
orientation.

The transport's common cell has ordinary-grid dimensions b by a and
reflected-grid dimensions a by b. In ordinary indices it lies inside
the h-grid because `h=a+2b>a+b`. The reflected hole has t=a-b levels;
above height ab its translated equation becomes
`X/b+Y/a=t-b=k`, exactly the smaller k-fold corner. Thus the code's
retained ordinary cells, switched common cell, and smaller canonical
Q have the stated shared boundaries. This independently verifies
the insertion used by the general theorem, not just its numeric 4830
specialization.
