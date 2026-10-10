# An unrestricted all-scale positive theorem for W and beta

**Denis Paliy — research with ChatGPT assistance**  
**9 October 2026**

## Status and precise scope

This note supplies a positive dissection for **every** primitive rational
Group-1 tile in both the W and beta-isosceles shapes, at every integer scale
at least v. There is no hypothesis on v/u apart from 0<u<v. In particular,
the golden-ratio hypothesis and the Omega coin test in the immediately
preceding note are unnecessary for this new construction.

This is NOT a complete classification of Erdős problem 634, NOT a claim
that scale v is minimal, and NOT a validation of the disputed scale-one
reverse-apex argument. Arbitrary tilings at scales M<v remain a different
question. The F3 scale-one candidate 14430 is not decided.

The new step is a **three-macro partition** with an earlier transition to
the upper grid triangle. Its clipped rectangle widths have explicitly
nonnegative representations for all parameters. The old scale-v
triquadratic seed, attributed to Michael Beeson, and the prior +u external
cap are stated inputs. The positive proof and the explicit computations
below do not use any proposed W/beta nonexistence or prime-case theorem.
No first-priority or external-referee acceptance is claimed. A separately
implemented certificate verifier is not a proof-assistant formalization.

## 1. The theorem

Let coprime integers 0<u<v be given, and put

    a=uv, b=v²-u², c=v²,
    d=v-u, Q=2v²-u², P=3v²-u².

The tile has sides (a,b,c), with angles satisfying 3 alpha+2 beta=pi.
For every integer M>=v, that one fixed tile tiles both targets:

| Target | Sides | Number of congruent original tiles |
|---|---|---|
| W | M(v³,uQ,vb) | QM² |
| beta-isosceles | M(v³,v³,uP) | PM² |

Reflections and T-junctions are permitted. No fixed ratio cone, coin-test
hypothesis, or adjacency hypothesis on u,v is imposed.

### Prior inputs and how they are used

The earlier cap theorem [C] establishes:

* the scale-v W tiling (the credited triquadratic seed);
* a disjoint external collar taking an **arbitrary** W tiling from scale
  T to T+u, whenever T>=v-u.

It follows that it is enough to construct each of the u-1 new residue
seeds

    m=v+t,  1<=t<=u-1.                               (1)

For arbitrary M>=v, let t=(M-v) mod u. Start at v if t=0, and otherwise
at v+t, then attach (M-v-t)/u collars. Every collar starts at T>=v>v-u.
For u=1, the credited seed and +1 collar already suffice; the new residue
range is empty. We therefore prove (1) with u>=2.

The proof is constructive for every residue, not a finite extrapolation.

## 2. Metric and elementary grids

Use rational oblique coordinates with Euclidean squared norm

    G(x,y)=v²(x²+y²)+(uP/v)xy.                       (2)

The Gram determinant is b²(4v²-u²)/(4v²)>0. In these coordinates the two
triangles

    A0=[(0,0),(u,0),(0,v)],
    B0=[(0,0),(v,0),(0,u)]

are congruent to the tile. An ordinary coordinate area uv/2 corresponds
to the area of one original tile. Half-turns of the same triangles fill
axis-parallel u-by-v and v-by-u rectangular cells.

A rectangle of height uv and width xu+yv, for x,y>=0 integers, is filled
by x columns of width u and y columns of width v. In a width-u column
use u rows of A0 cells; in a width-v column use v rows of B0 cells. Each
cell splits into two tiles. The total is 2(xu+yv) tiles. The partitions
need not agree at a seam, since T-junctions are allowed.

Define

    s=(b/v,0),       e=(v³/b,-uv²/b),
    s2=(-u,v),       e2=(u/v)e.

Their physical lengths satisfy

    |s|=b, |e|=c, |e-s|=a,
    |s2|=b, |e2|=a, |e2-s2|=c.

Thus the triangles [0,s,e] and [0,s2,e2] have ordinary tile grids too.
Both coordinate determinants det(s,e),det(s2,e2) equal -uv.

For any tile basis f,g, the L-fold grid on [X,X+Lf,X+Lg], with the
k-fold corner at X+Lf removed, consists of L²-k² whole original tiles,
provided 0<=k<L are integers. Its polygon is

    [X, X+(L-k)f, X+(L-k)f+kg, X+Lg].              (3)

This is a positive trapezoid (a full triangle when k=0), not a signed
subtraction of overlapping pieces. The removed smaller triangle consists
of actual whole triangles of the L-grid.

## 3. The three outside regions

Fix a residue t in (1), and set

    m=v+t,  w=u+t,  K=vm-uw=b+dt=d(u+v+t)>0.

Use the following points:

    X=(0,0),                       O=um e,
    A=(-uvm,u²m),                   C=(-uvm,v²m),
    Q0=(ub,0),                      S=Q0+ut s2,
    P0=Q0+ut e,                     R0=S+dt e2,
    V=(-u²w,uvw).

The large triangle is OAC. Its sides, computed using (2), are

    |OA|=uQm, |OC|=v³m, |AC|=vbm.

Use these three grid regions:

| Region | Actual grid | Number of tiles |
|---|---|---:|
| [O,X,Q0,P0] | Grid at X with basis (s,e), outer scale um, removed corner ut | u²(m²-t²) |
| [P0,Q0,S,R0] | Grid at Q0 with basis (s2,e2), outer scale vt, removed corner dt | t²(v²-d²) |
| [R0,V,C] | Complete grid at V with basis (s2,e2), scale K | K² |

The two annular scale differences are uv and ut, both positive. The
new point V and scale K replace the preceding note's fourth macro and
intermediate annulus. In particular the upper filling starts at y=uvw,
not y=uvm. The following exact identities locate all joins:

    C=V+K s2,             R0=V+K e2,
    S=V+b e2,             R0-S=dt e2,
    O-P0=uv(e-s),          P0-R0=ut(e2-s2),
    R0-C=K(e2-s2).

The vectors e-s and e2-s2 are positively parallel; consequently
O,P0,R0,C occur in that order on OC. Also

    O-A=(uQm/v²)e,   O-X=um e,

so X is strictly between O and A. S is strictly between V and R0.

The remaining boundary is the hexagon

    H=[X,A,C,V,S,Q0].                               (4)

The three clockwise macro boundaries and the clockwise boundary in (4)
sum to the clockwise boundary of OAC: all shared intervals cancel at
the actual displayed coordinates. Section 4 proves that H is a positive
region and gives its filling. Together these facts establish a true
partition without having to assume that the macros do not overlap.

For completeness, the boundary argument is as follows. Orient all regions
consistently. Subtract the target indicator from the sum of the region
indicators. Its jumps across every open edge interval vanish, by the
positioned boundary identity. It is zero outside a bounded set. Therefore
it is zero in every complementary face. Since all piece coefficients are
positive, the multiplicity inside the target is one and outside is zero.
This proves both containment and absence of interior overlaps. A finite
union of closed polygons then covers the boundary as well.

## 4. Fill the hexagon at every parameter

The left boundary of H is

    ell(y)=-(v/u)y,       0<=y<=u²m,
           -uvm,         u²m<=y<=v²m.

Its right boundary is

    r(y)=ub-(u/v)y,       0<=y<=uvt,
         bw-(v/u)y,       uvt<=y<=uvw,
         -(u/v)y,         uvw<=y<=v²m.              (5)

The two right-boundary transitions are continuous. We have

    uvt<u²m<uvw<v²m.

The second inequality follows from v(u+t)-u(v+t)=dt>0, and the last
from vm-uw=K>0. We now fill the horizontal strips. The construction
itself proves ell(y)<=r(y), rather than presupposing a positive H.

### 4.1. Lower expanding strips

For j=0,...,t-1, put y=uvj and use bottom endpoints

    Lj=(-v²j,uvj),  Qj=(ub-u²j,uvj).

The sloping left portion is the v-fold B0 triangle with vertices

    Lj+(-v²,uv), Lj+(0,uv), Lj.

The sloping right portion is the u-fold A0 triangle with vertices

    Qj+(-u²,0), Qj, Qj+(-u²,uv).

Between them is a height-uv rectangle of width

    Wlow_j=ub+bj-u²
          =u(v+qj)+v qj,
    qj=(d-1)u+dj>=0.                              (6)

The elementary columns of Section 2 fill it. These three portions have
disjoint interiors and exactly the cross-sections in (5).

### 4.2. Full middle cells

For j=t,...,w-1, the full slant cell has bottom-left (-v²j,uvj),
width bw, height uv, and displacement (-v²,uv) from bottom to top.
It consists of two v-fold B0 triangles and a rectangle. The rectangle
has width

    bw-v²=u(v+q*)+v q*,
    q*=(d-1)u+d(t-1)>=0.                          (7)

If its bottom-left x is x0 and its bottom height is y0, its left
triangle is

    F=(x0-v²,y0+uv), F+(v²,0), F+(v²,-uv),

its right triangle is

    (x0+bw-v²,y0), (x0+bw,y0), (x0+bw-v²,y0+uv),

and the rectangle lies between them. These are ordinary disjoint grid
pieces. The actual middle has u=w-t strips.

### 4.3. The one strip cut by the vertical target side

Let

    J=floor(um/v),   r=v(J+1)-um,   1<=r<=v.        (8)

Since um/v=u+ut/v and 1<=t<u<v, we have t<=J<w. Thus the kink of
the left boundary occurs inside one of the middle strips.

For j<J retain the full cell. At j=J remove from its left v-grid the
r-grid corner at

    F=(-v²(J+1),uv(J+1)).

The removed triangle has vertices

    F, F+(vr,0), F+(vr,-ur).

The last two vertices are exactly

    (-uvm,uv(J+1)), (-uvm,u²m)=A.

Hence only the part outside the vertical line x=-uvm is removed.
The r-grid corner is a union of r² whole tiles. Because r<=v, it is
contained in the left v-grid. If r=v, the whole left triangle is omitted;
this occurs in some nonprimitive controls. No tile fragment is retained.

### 4.4. The decisive width identity: no ratio hypothesis remains

For j>J the entire old left triangle lies outside the vertical side.
Retain the right v-grid triangle and put the rectangle's left edge at
x=-uvm. Its width is

    Wclip_j=bw+uvm-v²(j+1)
           =uK+v²(w-1-j)
           =K*u+[v(w-1-j)]*v.                    (9)

Every coefficient in (9) is nonnegative, for every v>u. In fact K>0,
so the width is strictly positive. There is no Omega, Delta, or
Frobenius restriction in this formula. This is the step eliminating the
golden-ratio boundary of the previous layout.

All retained right triangles lie to the right of the vertical side,
because the rectangle's width is positive. The rectangles in (9) are
filled by the actual columns of Section 2. No geometry of an arbitrary
hypothetical tiling is assumed; these are explicitly chosen pieces.

### 4.5. Finish with the upper grid triangle

Above y=uvw the remaining triangle is

    [(-uvm,uvw), (-uvm,v²m), (-u²w,uvw)].           (10)

Its vertical and horizontal legs are vK and uK. It is therefore a
K-fold A0 grid. The construction now fills every part of H.

The description covers all placements of the kink, including a strip
endpoint, and every t in (1). The full argument is symbolic; finite
examples are not used to infer the universal result.

## 5. Count and beta lift

The hexagon's coordinate area is uv/2 times

    NH=b[t²+2t(u+v)+u²+v²].                        (11)

This follows either by its shoelace formula or by summing the positive
strip areas. Adding the three outside counts gives the polynomial identity

    u²(m²-t²)+t²(v²-d²)+K²+NH=Qm².               (12)

Here (12) is a count check, not a substitute for the geometric filling.

For beta put

    Bstar=O+(P/Q)(A-O).

A is between O and Bstar. Triangle A Bstar C is across AC from OAC,
and has side lengths vm(a,b,c). Add its ordinary (vm)-grid. The union
is triangle O Bstar C with sides m(uP,v³,v³), and the count is

    Qm²+(vm)²=Pm².

This is the established positive W-to-beta attachment, applied to the
new actual W seed. Alternatively it can be performed after the collars.
Section 1 now gives every M>=v, proving the theorem.

## 6. Nonprimitive parameters and a quantitative corollary

If u=g u0 and v=g v0, division of all lengths by g² changes the target
scale from M to gM with the primitive tile (u0 v0,v0²-u0²,v0²). The count
is unchanged:

    (2v²-u²)M²=(2v0²-u0²)(gM)²,

and likewise for beta. The primitive theorem therefore already supplies
the original targets whenever gM>=v0, i.e. M>=ceil(v/g²). In particular
M>=v always works. The direct seed formulas and exported controls also
allow nonprimitive integers, but introduce no new triangle shapes.

### W-compatible square classes now have a square-root sufficient bound

Call a squarefree integer d0>2 W-compatible if each odd prime dividing
it is congruent to 1 or 7 modulo 8. The prior norm lemma [S, Lemma 5.1]
gives a primitive representation

    d0=2v²-u²,   0<u<v.

This is a prior arithmetic theorem, not a new norm-solvability claim.
It also follows by the norm-Euclidean ring Z[sqrt(2)] and its unit
3+2sqrt(2), reducing a norm -d0 element to 0<u<v.

For any such representation v²<d0. Thus the new geometry proves

    d0*m² is realizable for every m>=floor(sqrt(d0)).   (13)

The sharper bound is m>=v for any chosen representative. The prior
unrestricted common bound was linear in d0; (13) is a square-root bound.
Neither is claimed necessary.

### A global exact sector

Write N=d0*m² with d0 squarefree. Suppose

    N=14 (mod 16),   3 does not divide N,
    m>=floor(sqrt(d0)).                              (14)

Then

    N is realizable  <=>  every odd p|d0 is 1 or 7 (mod 8). (15)

For necessity the prior exhaustive branch isolation [S, Section 7]
leaves only W at the first two conditions of (14). An inert odd prime
cannot divide a primitive 2v²-u², since it would divide both u,v.
An inert prime occurring to odd exponent in N therefore excludes every
possible tiling. Sufficiency is (13). These global negative statements
use the published classification inputs and exact branch normalization
specified in [S]; they do not follow from the construction alone.

The condition m²>=d0, equivalently N>=d0², is a convenient slightly
stronger sufficient version of the last condition in (14). No conclusion
is drawn when the small multiplier lies below the threshold and the
necessary arithmetic passes.

## 7. Exact certificates and checks

The constructor exports full unit coordinates using rational arithmetic.
Its new seed routine implements Sections 3-4; the credited previous seed
and collar routines implement the stated prior inputs. Its output is a
positive certificate only. A size limit on exporting a large certificate
never means nonexistence.

`verify.py` is copied unchanged from the preceding package and imports
no construction code. It derives the metric and target lengths from
(u,v,M), checks every unit triangle's metric, orientation and containment,
checks the exact total area, and checks every positioned boundary event.
Its optional separate pair loop checks all unordered pairs using integer
separating-axis tests. It guards against integer determinant overflow.

`check_symbolic.py` verifies 46 exact rational identities (metric, joins,
counts, clipping and rectangle formulas) and 14 nonnegative-coefficient
sign checks on the full parameter cone

    u=x+y+2, t=y+1, v=x+y+z+3,  x,y,z>=0.

Its independent bounded regression covers 3247 integer parameter pairs,
66640 residue seeds and 1427531 rectangle identities. These sample counts
are implementation controls, not the proof of the theorem.

A fresh 22-case complete unit regression checks 290482 triangles and
4256291188 unordered triangle pairs. It includes every seed residue for
(5,8) and (3,10), old seed controls, one and several collars, beta lifts,
and the nonprimitive kink-at-layer-end case (4,6,9). Deliberate duplicate,
deformed, and orientation-reversed certificates are all rejected.
See the machine-readable reports for the exact scope of each check.

Examples retained in the package include:

| u,v,M | Tile | Family | Count |
|---|---|---|---:|
| 2,5,6 | (10,21,25) | W | 1656 |
| 2,5,6 | (10,21,25) | beta | 2556 |
| 3,10,12 | (30,91,100) | W | 27504 |
| 2,11,12 | (22,117,121) | W | 34272 |

Each has explicit coordinates. Their existence for this specified tile
and target is what is certified; no claim of a previously unknown global
count or of priority is inferred merely from finding these witnesses.

## 8. Remaining gaps — not silently converted into a full solution

The new theorem closes the **entire positive region M>=v in W and beta**,
not the exact spectrum of either family. There are infinitely many
primitive parameter pairs, so the finitely many M<v for each pair do
not constitute a single finite global exception list.

For a surviving W candidate N=Q M² with M<v, necessarily M<N^(1/4),
since Q>v²>M². Similarly a surviving beta candidate with M<v satisfies
M<(N/2)^(1/4), since P>2v². These bound the remaining residual multiplier;
they do not decide its geometric feasibility.

The universal F3 small-scale question is untouched. In particular the
published project gate for N=14430 leaves the ordered primitive tile
(56,9,61) at residual scale one. That gate excludes W as an alternative
branch at the same count. An unrestricted positive W theorem cannot
therefore solve this particular F3 instance by substitution.

The reverse-apex PDF sent to Michael Beeson explicitly remains a candidate
for independent scrutiny; this note does not use its claimed forcing,
its W complement contradiction, or an all-primes conclusion.

## 9. Reproduction and attribution

From this directory:

    python check_symbolic.py
    python construct.py --u 2 --v 5 --m 6 --output W_1656.json
    python verify.py W_1656.json --all-pairs
    python regression.py

The exact finite geometric checks do not machine-prove the prior
classification results or the written universal geometric argument.

[C] Prior seed and +u external collar, repository snapshot
`3a0ad269f645850ed9fd01bbd76a08c9b456032e`:
`research/w-beta-caps/PROOF.md`, Sections 3-6. The scale-v seed is credited
there to Michael Beeson. This is a positive-construction dependency only.

[S] `research/square-class-saturation/PROOF.md`, Sections 5 and 7, at the
same snapshot: the reduced norm representative and W-only global sector.
These are used only in Section 6, not in the positive geometry.

[G] Previous 9 October file
`Erdos634_W_beta_golden_cone_PROOF_2026-10-09.md`: the preceding four-macro
construction and clipped strip. Its ratio/Omega restrictions are not
premises here. The new three-macro layout removes their geometric cause.

[Gap] `research/universal-closure-oct8/global/ALL_N_GAP_AUDIT.md`, same
repository snapshot: the separate unique F3 candidate at 14430.

The upstream angular/rationality input for the global corollary is
M. Beeson and Y. X. Zhang, *Rationality of certain triangle tilings*,
arXiv:2604.01314v1, with the precise further normalization dependencies
listed in [S]. No exhaustive audit of priority in the literature was
performed for the present new construction.
