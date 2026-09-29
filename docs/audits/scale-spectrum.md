# Independent audit: complete scale spectrum for the other scalene target

29 September 2026. Separate internal check of the proposed
gluing construction. Verdict: PASS for
all primitive rational pairs 0<u<v, not just (u,v)=(2,3). No assertion of
publication priority or external refereeing is made.

## Theorem

Let the tile have primitive sides

    a=uv, b=v²-u², c=v², gcd(u,v)=1, 0<u<v,

with angles alpha,beta,gamma and 3alpha+2beta=pi. Put

    Q=b+c=2v²-u², P=b+2c=3v²-u².

A triangle of angles (2alpha,alpha,2beta) can be tiled by N congruent copies
of this tile if and only if

    N=k² Q P

for a positive integer k. Its sides, in the primitive tile units, are

    k cQ, k c², k bP.

This fully settles this one target-shape branch for every primitive rational
tile and every scale. It does not classify the other four target shapes or
all possible N globally.

## 1. The supplied W triangle is at exactly the required scale

Beeson, arXiv:1206.2229v4, Theorem 11 states that if

    M²+N_W=2K², M²<N_W, K|N_W,

then a tile (M,N_W/K-K,K) tiles the W triangle with sides

    BC=M N_W/K, AC=N_W-K², AB=K²,

and angles A=2alpha, B=beta, C=theta=alpha+beta.

Set

    M=a, K=c, N_W=cQ.

The identity a²=c(c-b) gives

    a²+cQ=c(c-b)+c(b+c)=2c².

Also N_W-a²=cQ-c(c-b)=2bc>0, and K|N_W is immediate.
The output tile is exactly (a,Q-c,c)=(a,b,c), and the output sides are

    BC=aQ, AC=bc, AB=c².

Thus this W triangle has an established tiling by exactly cQ copies of the
original tile. This invokes the sufficient construction in Theorem 11,
not any disputed necessary-divisibility assertion in earlier versions.

The printed construction proof's a-by-c brick angle labelled gamma is a
local angle-name typo; the preceding paragraph identifies its enclosing
parallelogram's angle beta, as required for a-by-c two-tile bricks. This
was separately checked in the earlier global-classification audit (see `docs/prime-case-dependencies.md`). The present
argument uses the actual beta-brick construction.

## 2. Gluing and angle audit

Take a triangle similar to the tile with integer scale factor Q. Its side
lengths are aQ,bQ,cQ, and the standard quadratic subdivision gives Q²
congruent copies of the original tile.

Glue its aQ side to BC, placing its interior on the opposite side of BC
from the W triangle. Match its beta endpoint to B and its gamma endpoint
to C. Call its remaining vertex D, so its angle at D is alpha.

At B the two angles add to beta+beta=2beta, strictly less than pi.
At C they add to theta+gamma=pi, since theta=alpha+beta and
alpha+beta+gamma=pi. Therefore A,C,D are collinear, with C between A,D.
The union is the single convex triangle ABD, with angles

    angle A=2alpha, angle B=2beta, angle D=alpha.

There is no overlap: the original triangles were placed in opposite open
half-planes of the shared side BC. Their interiors are disjoint and their
common side is exactly BC. Straightness at C removes that vertex from the
outer boundary, so there is also no unfilled gap.

The outside side lengths are

    AB=c²,
    BD=cQ,
    AD=AC+CD=bc+bQ=b(c+Q)=bP.

The number of tiles is

    N=cQ+Q²=Q(c+Q)=QP.

T-junctions on the glued seam are allowed; matching individual boundary
vertices of the two tilings is unnecessary. Only the complete side length
aQ and the opposite-half-plane placement are needed.

Replacing every tile by its quadratic k-by-k subdivision realizes k²QP
for every positive integer k.

## 3. Short necessity proof: the side triple is primitive

The construction shows that the target shape has side proportions

    (c²,cQ,bP).

This integer triple is primitive. Indeed gcd(c,Q)=1, so

    gcd(c²,cQ)=c.

Also gcd(c,b)=gcd(c,P)=1, hence gcd(c,bP)=1. Therefore

    gcd(c²,cQ,bP)=1.

Any triangle of this same shape has sides k(c²,cQ,bP) for a positive real
number k. If it is tiled by the primitive integer-sided tile, every target
side is a whole-edge chain and has integer length. Choose integer Bezout
coefficients x,y,z with x c²+y cQ+z bP=1. Multiplication by k gives

    k=x(k c²)+y(k cQ)+z(k bP),

an integer. Since the unit-scale target has QP tile areas, the area identity
now gives N=k²QP. This proves necessity without a coloring equation.

For an initially unspecified tile, the source rationality theorem remains
the reduction to primitive rational parameters; for a specified tile of
the displayed form, this necessity argument is entirely elementary.

## 4. Alternative necessity check by coloring valuations

Beeson's v4 Theorem 13 gives, for an arbitrary such tiling, the necessary
coloring equation

    N R² = M² QP,  R=(v-u)(2v+u),

with integer coloring number M. We check that R|M; this step must not be
replaced by the false general inference that an integer square ratio has
an integer square root before cancellation.

No odd prime divisor ell of R divides QP. Indeed gcd(ell,v)=1. If ell
 divides v-u, then modulo ell the pair (Q,P) is (v²,2v²), both nonzero.
If ell divides 2v+u, the pair is (-2v²,-v²), again nonzero. Consequently
at each such odd ell, nonnegativity of the valuation of N in the displayed
equation forces v_ell(M)>=v_ell(R).

At 2, the valuation of QP is at most 1:

* u,v both odd: Q is odd and P=2 modulo 8;
* u even,v odd: Q=2 modulo 4 and P is odd;
* u odd,v even: Q and P are odd.

Write r=v_2(R),m=v_2(M),e=v_2(QP)<=1. The equality gives

    2r=2m+e-v_2(N)<=2m+1,

and hence r<=m. Thus R|M at every prime. Write k=|M|/R>0. The equation
then gives exactly N=k²QP. This is the claimed necessary condition.

The source rationality theorem ensures primitive rational parameters for
this nonsimilar target shape. The angles cannot accidentally make the
target similar to the original tile: that would impose an additional
rational relation among alpha and pi, whereas alpha/pi is irrational.

## 5. Exact N=322 check

For (u,v)=(2,3), the tile is (a,b,c)=(6,5,9), Q=14,P=23.
Theorem 11 gives a W triangle with sides

    aQ=84, bc=45, c²=81,

and 126 tiles. It is the same parameter choice M=6,K=9,N_W=126
illustrated in Beeson's v4 Figure 14.

The Q-fold quadratic triangle has sides

    aQ=84, bQ=70, cQ=126,

and 196 tiles. Glue the 84 sides with the prescribed endpoint matching.
The outer triangle has sides

    81, 45+70=115, 126,

and 126+196=322 tiles.

The claim that the same source lists 322 as unresolved is genuine (v4,
Theorem 14 remark and Section 11.3). It does not invalidate the construction,
but it makes checking side labels and endpoint matching particularly
important. All four matches here have been independently checked against
Theorem 11's displayed side formulas and its specified target angles.

## 6. What this removes from the previous frontier

The necessary-versus-sufficient gap in the entire scalene
(2alpha,alpha,2beta) branch disappears. In particular it is no longer
correct to list the (6,5,9)-tile 322 instance as an unresolved small-scale
case. More generally every minimal QP is realized, even if u>1 or the
inequality c<2b used by the older Theorem 14 construction fails.

The general Erdős 634 question still includes the other target shapes and
60-degree/120-degree families. This theorem must not be promoted to a
complete global classification.
