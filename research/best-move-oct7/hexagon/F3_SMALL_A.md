# Every multiplier in the ordered F3 family with a<b

Let positive integers `a<b` satisfy `c²=a²+ab+b²`. Then the ordered F3
triangle with sides

    c², c(a+2b), 3b(a+b)

has a positive tiling by `3(a+b)(a+2b)` congruent `(a,b,c)` triangles.
Consequently every positive integer multiplier works for this orientation.
Primitivity is unnecessary for the geometric theorem. This does not
decide the other orientation with `a>b`, including `(24,11,31)` and 4830.

The construction joins the already proved all-multiplier F4 theorem for
`a<b` to the already proved ideal-trapezoid construction. The new step is
the positive five-region partition below. No negative or overlapping
region is used, and no filling of the earlier fan hexagon is assumed.

## A five-region partition, valid for every a,b>0

Use the basis `(1,rho)` with `rho=exp(i*pi/3)` and squared norm
`x²+xy+y²`. Put `A=ab`, `B=b²`, `Z=a+b*rho`, `z=Z/c`. Apply the
isometry `w -> z^-2*w-a²` to the canonical F3 triangle. Its vertices are

    X=(-a²,0), Y=(2A,-2A-B), K=(2A,A+2B).

Define

    P=(A,-A), E=(2A,-2A), L=(A,A+B), R=(2A,A+B).

The five pieces are

| Piece | Geometry | Count |
| --- | --- | --- |
| `[X,Y,P]` | c-fold original tile | `c²` |
| `[Y,P,E]` | b-fold original tile | `b²` |
| `[L,R,K]` | b-fold original tile | `b²` |
| `[X,P,L]` | F4(a,b) triangle | `(2a+b)(a+b)` |
| `[E,P,L,R]` | ideal trapezoid T(2ab+b²,ab) | `5ab+2b²` |

Here `T(x,H)` denotes the trapezoid with vertices
`(0,0),(x+H,0),(x,H),(0,H)`.

For positivity, `L` lies strictly on `XK`:

    L-X = ((a+b)/(a+2b))*(K-X).

Also `P` lies strictly inside `XYL`: its horizontal coordinate is A, its
vertical coordinate lies between the lower edge XY and L. Indeed the
intersection of XY with x=A is

    y=-b(2a+b)(a+b)/(a+2b) < -ab,

because the difference of its magnitude and ab is `b*c²/(a+2b)>0`.
Joining P to X,Y,L partitions triangle XYL into XYP, YPL and XPL.
The line from L to R cuts triangle YLK into YRL and LRK, and E is
strictly between Y and R. The triangles YPL and YRL together form the
convex quadrilateral YPLR. The segment EP cuts off YPE from it,
leaving the trapezoid EPLR. Equivalently, all four points P,E,R,L are
the vertices of the displayed positive ideal trapezoid. These cuts give
the five regions with disjoint interiors and union XYK.

The lengths of XYP are `(ac,bc,c²)`. For YPE and LRK the three lengths
are `(ab,b²,bc)`. The lengths of XPL are

    |XP|=ac, |PL|=b(2a+b), |XL|=c(a+b).

Thus XPL is exactly the F4(a,b) target. The isometry

    w -> L-z*w

maps the F4 source triangle ODC in
[`group2-f4/PROOF.md`](../../group2-f4/PROOF.md) to LXP:
`O->L`, `D->X`, `C->P`. The last identity follows from
`(a+b*rho)(b+a*rho)=c²*rho`.

The isometry `w -> E+rho*w` maps T(2A+B,A) to ERLP, which has the same
closed region as EPLR.

## The trapezoid always fills when a<b

Put `d=a+b-c>0`. The existing
[ideal-trapezoid theorem](../../group2-trapezoids/PROOF.md), with its two
short-side labels interchanged, fills T(s,ab), where

    s=a²+b²-a*d.

The needed increase of the short base is

    (2ab+b²)-s = a(3b-c).

Since `c<a+b<2b`, the integer `3b-c` is positive. Attach the
parallelogram of width `a(3b-c)` and height `ab`, tiled by
`(3b-c)` columns and `a` rows of a-by-b two-tile cells. This fills the
whole ideal trapezoid T(2ab+b²,ab).

The fourth piece XPL is filled by the existing F4 theorem for a<b.
The other three pieces use ordinary integer triangular grids. Their
counts sum to

    c²+2b²+(2a+b)(a+b)+(5ab+2b²)
      =3(a+b)(a+2b).

Integer dilation and ordinary subdivision give every positive multiplier.
For a nonprimitive triple, apply the same construction to its primitive
normalization at the common-divisor multiplier; rescaling the physical
unit size gives the stated theorem.

## Scope

Combining this result with the earlier gamma construction for
`b<a<2b` gives every multiplier of the ordered F3 target whenever
`0<a<2b`. The equality a=b or a=2b cannot occur for positive integer norm
triples. For a>2b no conclusion follows from this argument: F4(a,b) is
then the unresolved orientation even in cases where the trapezoid fills.

The proof uses established positive constructions from this repository;
it is not a claim of independent priority over the literature.

## Concrete verification

`construct_small_a.py` expands the five-region construction into exact
unit coordinates. `check_small_a.py` independently verifies unit side
lengths, containment, area and nonoverlap; it imports no constructor or
geometric helper. Its exact interval filter accounts for all pairs before
using separating-axis tests on the candidates. The retained certificates
are `f3-312.json` for `(3,5,7)` and `f3-2331.json` for `(5,16,19)`.

For the larger primitive example `(136,209,301)`, the five counts are

    90601, 43681, 43681, 165945, 229482,

totaling **573390**. The needed trapezoid has short base 100529 and leg
28424. Its stored six-region seed certificate
`trapezoid-136-209-301.json` has short base 56193 and 140810 tiles; the
added strip has width 44336=136*326 and 88672 tiles. Its existing
independent macrorecipe verifier passes without expanding 140810 tiles.
The new macrochecker verifies this example and every primitive norm
triple `0<a<b<=500` (87 triples). The symbolic argument above supplies
the proof for all parameters; these checks are supporting verification.

From the repository root:

```bash
python research/best-move-oct7/hexagon/check_small_a.py research/best-move-oct7/hexagon/f3-312.json research/best-move-oct7/hexagon/f3-2331.json
python research/group2-trapezoids/verify.py research/best-move-oct7/hexagon/trapezoid-136-209-301.json
```
