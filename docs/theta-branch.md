# Round 4: isosceles constructions, a stronger bound, and a counterexample to a printed divisibility lemma

29 September 2026. Internal research report. This note does **not** classify either
isosceles branch for all primitive tiles, nor solve Erdős 634 in full. The 48- and108-tile seed tilings reproduce constructions of Beeson. The odd-scale
147- and243-tile constructions are new to this investigation; priority is not claimed.

## 1. Setup and the exact current boundary

Let `a=uv`, `b=v²-u²`, `c=v²`, `0<u<v`, `gcd(u,v)=1`, with opposite angles
`alpha,beta,gamma` and `3alpha+2beta=pi`. Write `theta=alpha+beta` and
`Q=b+c`. Put `b=q h²`, where q is squarefree.

For a theta-isosceles target (apex alpha, base angles theta), every tiling has

    N=q t²,  X=v q h t,  Y=u q h t,

where X is either equal side, Y is the base, and t is a positive integer. The
area proof in `theta-squarefree-obstruction.md` establishes these formulas.

The improved necessary bound proved below is

    q h(t-h) >= 2v.

Thus `N>=q(h+ceil(2v/(qh)))²`. There is also the independent base condition

    u q h t >= 2v²,

and the exact nonnegative edge decomposition of Y must contain at least two c
edges. These conditions are not sufficient.

For the particular tile `(2,3,4)`, the reliable status is:

* Necessarily `N=3t²`.
* `t=1,2,3` are impossible.
* Every `t>=4`, except possibly `t=5`, is realized.
* The sole remaining fixed-tile theta case is `N=75`, equal sides30 andbase15.

The 147-tile construction disproves the divisibility statement of Beeson v4
Lemma 55; Section 5 identifies the retracted intermediate claim in its proof.

## 2. Self-contained two-c-edge lemma for this theta shape

**Lemma.** Every outer side of a theta-isosceles target contains at least two
whole c edges.

The proof uses only that the target's corner angle inventories are one acute tile
angle or one alpha plus one beta, that gamma is obtuse, and that neither of the
shorter tile lengths is an integer multiple of the other. All these properties
hold here. Irrationality of alpha/pi follows from `2cos(alpha)=2-u²/v²`, a
nonintegral rational algebraic-integer contradiction if alpha/pi were rational.
It then gives precisely these corner inventories. Also `gcd(a,b)=1`, while
`a>=2,b>=3`, so neither is an integer multiple of the other.

Temporarily rename the acute tile angles delta and epsilon so that their
opposite sides satisfy `a'<b'<c`. Suppose an outer side has only one c edge PQ.
Its tile has delta at P, epsilon at Q, and gamma at its third vertex R; thus
`PR=b'`, `QR=a'`. If there are boundary edges before P or after Q, all are
of types a' or b'. The obtuse endpoint pigeonhole argument forces the boundary
tile immediately before P to contribute gamma at P, and the one immediately
after Q to contribute gamma at Q. (All obtuse endpoints point toward PQ.)
In particular no additional tile can contribute gamma at either P or Q.

At Q there are two possibilities. If Q is a target corner filled just by the
epsilon angle, QR lies on the target boundary and R lies on the boundary.
Otherwise, whether Q is a target corner of angle delta+epsilon or an interior
boundary point, there is exactly one delta tile immediately across QR at Q.
Its edge there has length b' or c', both longer than `QR=a'`; consequently R
lies in the relative interior of this tile's edge. In that case this tile
contributes a straight angle at R, separately from the original gamma angle.
Thus, in either case, **no further tile can have gamma at R**: the boundary case
would exceed pi, and the crossing case would give `pi+2gamma>2pi`.

We must also consider whether PR is an external side. This can happen only if
P is a target corner filled by the single delta angle. If QR is also external, R is a target corner containing gamma, impossible.
Otherwise QR is an internal chord with both endpoints on the outer boundary. Since a' is the shortest tile
side, its whole opposite edge chain is a single a' edge. The opposite tile has
gamma at Q or R, both of which were ruled out above. So PR has a tiled region
on its other side.

The opposite whole-edge chain along PR starts at P and ends at R: the outer
boundary prevents extension past P, while at R either the outer boundary or
the interior of the crossing tile prevents extension along PR. Its total length
is b'. It cannot contain a c edge. If it contains a b' edge, that edge occupies
the whole segment and its tile has gamma at P or R, again impossible. Hence
all its edges have length a'. This says b' is an integer multiple of a', a
contradiction. The lemma follows.

This proof allows T-junctions. In particular it never excludes two obtuse
angles at an arbitrary interior vertex merely because `2gamma>pi`; it first
establishes either a boundary half-plane or an additional straight sector.

## 3. Stronger count bound and the three smallest (2,3,4) cases

At the target apex there is exactly one alpha tile, so one equal side contains a
b edge. If that side has A, B, C whole edges of lengths a, b, c, reducing
`X=Auv+B(v²-u²)+Cv²` modulo v gives `v|B`. Thus B>=v. Section 2 gives C>=2,
so

    v q h t = X >= v b+2c = v q h²+2v².

Divide by v to obtain the claimed `qh(t-h)>=2v`.

For `(u,v)=(1,2)`, we have `b=q=3,h=1,X=6t,Y=3t`.

* t=1 has base Y=3<2c=8.
* t=2 would give X=12, but the apex-side argument requires X>=2b+2c=14.
* t=3 has base Y=9. Two c edges occupy length 8, and the remainder 1 cannot
  be decomposed into tile edges of lengths 2,3,4.

These exclude the **fixed tile and target shape** at N=3,12,27. They do not
exclude those integers globally in Erdős 634.

## 4. Exact additive construction and infinite sufficient subfamilies

Here is a general geometric gluing lemma. Let a fixed target be
`T=conv(0,p,q)`. If scale m and scale n of T have tilings, then scale m+n
partitions into those two smaller targets and the parallelogram

    R=conv(0,np,np+mq,mq).

The two triangular parts are

    np + mT = conv(np,(m+n)p,np+mq),
    mq + nT = conv(mq,np+mq,(m+n)q).

Their interiors are disjoint and together with R they exhaust `(m+n)T`.
If the angle between p and q is alpha, any R whose p-direction side is an
integer multiple of b and q-direction side is an integer multiple of c is a
rectangular array of b-by-c parallelograms, each split into two original tiles.
Reflections and T-junctions along the interfaces cause no difficulty.

### Theta target

Take `|p|=|q|=bc` and included angle alpha. The target's third side is ab and
its area is bc times the tile area. For integers m,n, the bridge has `nc`
steps of length b and `mb` steps of length c. It therefore uses `2mn bc` tiles.
Thus the tileable integer scales of this target are additively closed.

For `(a,b,c)=(2,3,4)`, Beeson v4 Figure 21 (printed p79) exhibits the two seed
counts 48 and 108, namely scales 2 and 3 relative to `(12,12,6)`. Every integer
k>=2 is `2r+3s` with r,s nonnegative. Repeated gluing therefore constructs

    N=12k², k>=2.

The seeds can also be reproduced by the integer parameters of Theorem 24:

| N | mu | p | q | t | r | u | v | h |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 48 | 6 | 2 | 3 | 1 | 2 | 4 | 2 | 5 |
| 108 | 9 | 4 | 6 | 2 | 1 | 4 | 2 | 14 |

Here letters p,q,t,r,u,v,h are **local construction parameters in Theorem 24**,
not the primitive tile's u,v or the squarefree parameters in Section 1.
For the last parallelogram choose `h=2+3` for 48 and `h=7*2` for 108.
`../scripts/generate_theta.py` independently instantiates the macrogeometry and
writes all individual tiles as rational coordinates with metric `dx²+15dy²`.

### Alpha-base target

Take `|p|=bQ`, `|q|=bc`, with included alpha. The remaining side also has
length bc, and the area is bQ tile areas. The bridge has nQ b-steps and mb
c-steps, so it uses `2mn bQ` tiles. The tileable integer scales are again
additively closed.

At `(2,3,4)`, Figures 28 and 29 of Beeson v4 give scale-two and scale-three
seeds N=84 and189. The latter is credited there to Jan Philip Harries (July 2026).
Consequently every `N=21k²`, k>=2, is realized by this fixed tile and shape.
The necessary tiling equation allows k=1 as well. Beeson reports a computational
exclusion at21; this note does not independently prove that exclusion and does
not claim a complete alpha spectrum.

## 5. An explicit counterexample to the printed Lemma 55

Source: Michael Beeson, *Triangle Tiling: The Case 3alpha+2beta=pi*,
[arXiv:1206.2229v4](https://arxiv.org/abs/1206.2229v4), revised 25 September 2026.

Lemma 55 (printed pp92–93) claims a divisibility consequence for the theta shape
when b is squarefree and coprime to c-a. Its proof extends a theta tiling to a
beta-isosceles tiling, and on p92 says:

> By Theorem 18, k divides the coloring number of the new tiling.

But Theorem 18 footnote3 (printed p71) explicitly retracts the former claim
`gcd(a,c)|M`. The present Theorem 18 does not assert it. This leaves the printed proof of Lemma 55 unsupported at that step. The new
147-tile construction below goes further and supplies a counterexample to its
statement.

At tile(2,3,4), Lemma 55 would force the theta coloring number t to be even.
But Section 6 constructs N=147, t=7, equal sides42 andbase21, so its coloring
number M=7 is odd and mu=X/c=21/2 is nonintegral. Its hypotheses hold:
b=3 is squarefree and gcd(b,c-a)=gcd(3,2)=1. This is therefore a concrete
counterexample to Lemma 55 as printed.

The known beta scale-three tiling N=99 also has odd coloring number9, so the
intermediate blanket beta divisibility is false. That beta construction is due
to Bonfioli and is audited separately in `scale-spectra.md`.

## 6. Odd theta seeds:147 and243

Use the macrogeometry of Theorem 24 but allow both orientations of the a-by-b
cells in its parallelograms. Keep `(a,b,c)=(2,3,4)`. For target count `3T²`, put
`mu=3T/2` and choose the local green scale `p=4`. Its other local parameters are

    q=6, red_scale=2, yellow_scale=2(T-4), pink_scale=T-4,
    r=3T/2-8, final_width=26-2T.

The five triangular blocks have integer scales even when T is odd. The first
parallelogram has horizontal length `L=3T-16` and slanted length6, with included
angle gamma. Write `L=2x+3y` with x,y nonnegative integers. Since6 is divisible
by both2 and3, each horizontal2 strip can use 2-by-3 cells and each horizontal3
strip can use3-by-2 cells. Thus r itself need not be an integer.

The final parallelogram has horizontal length `3(T-4)` and slanted length
`26-2T`, an even integer, so it is a grid with horizontal3 and slanted2 steps.
For T7, take `L=5=2+3`; for T9, take `L=11=4*2+3`. Both layouts fit with
positive dimensions. Their tile counts are respectively147 and243.

For the 147-tile example, coordinates `(x,y)` mean physical `(x,y*sqrt(15))`.
An explicit macrodissection is:

| Point | Coordinates |
|---|---|
| A | `(0,0)` |
| B | `(21/2,21/2)` |
| C | `(21,0)` |
| P | `(16,0)` |
| G | `(21/2,3/2)` |
| K | `(6,6)` |
| L | `(33/2,9/2)` |
| Q | `(29/2,3/2)` |
| R | `(39/2,3/2)` |
| V | `(15/2,9/2)` |

The target is ABC. Its five similar triangular pieces are APG, AGK, BKL, PGQ,
and KLV, at scales 4,6,6,2,3. Parallelogram PCRQ has sides 5 and6 at gamma;
split its horizontal 5 into2+3 and tile the two strips as explained above.
Parallelogram GRLV has sides 9 and12 at gamma; use a 3-by-6 array of cells
with side lengths 3 and2. The seven piece counts are

    16+36+36+4+9+10+36 = 147.

The coordinates directly show that the pieces have disjoint interiors and
exhaust ABC; alternatively this follows from the exact checks below. Thus the
smallest stated counterexample can be inspected without reconstructing a
published diagram.

The explicit coordinate generator `../scripts/generate_theta.py` uses the rational
metric `dx²+15dy²` and outputs every tile. The certificates
`../data/theta-147.json` and`../data/theta-243.json` pass exact
side congruence, containment, summed area, and every pair's nonoverlap check.
These numerical certificates supplement the macrogeometry and do not replace
its general proof. A separate exact-arithmetic replay checked all pairs by convex polygon clipping
and checked edge cancellation at T-junctions; see [the audit](audits/theta.md).

For propagation, use target unit vectors p,q with equal length6 and included
angle alpha. In the scale-addition parallelogram, one side has length6m and the
other6n. If either m or n is even, one side can be divided into c4 steps and the
other into b=3 steps. Thus any two existing scales can be added when one is even.
The existing even scales 4 and6 give all even scales at least4. Starting with7
and9 and repeatedly adding4 gives every odd scale at least=7. Therefore

    theta(2,3,4): all N=3T² with T>=4 except possibly T=5 exist.

Together with Section 3, N=75 is the only undecided case in this fixed branch.

## 7. An effective eventual construction for a broad uniform family

Put `Delta=b(a²+b²)-a²c` and suppose Delta>0, the same geometric range as
Beeson's Theorem 24. Let `F=(a-1)(b-1)`. Then every integer

    T >= ceil((a²c+F)(a²+b²)/(u Delta))

admits a theta-isosceles tiling with exactly `N=bT²` tiles. In particular, if
b is squarefree, the area equation shows these are all possible count forms,
and the theorem settles every sufficiently large scale with an explicit bound.

Here u is the primitive parameter `a=uv,c=v²`. Choose an integer J in

    uT/(a²+b²) <= J <= (ubT-F)/(a²c).

The displayed bound makes the interval length at least1, so such J exists and
is positive. Set the target scale `mu=bT/v`, so equal sides `X=bvT` andbase
`Y=ubT`. In the local notation of Theorem 24 choose its green scale `p=a²J`.
The triangular blocks have scales

    p=a²J,
    q=abJ,
    red_scale=a u²J,
    yellow_scale=vT-acJ,
    pink_scale=uT-a²J.

All are integers. The interval's upper bound gives positive base-parallelogram
length and also positivity of the yellow and pink scales: since c>b,
`T >= a²cJ/(ub) > avJ`, and `vT>acJ`.

The first parallelogram has horizontal length

    L=ubT-a²cJ >= F,

and slanted length `H=ab u²J`, an integer multiple of both a and b. Since a,b
are coprime, every integer at least F is `xa+yb`, with x,y nonnegative. Split L
into such strips. An a-strip uses b-steps along H; a b-strip uses a-steps.
Each resulting cell has side lengths a,b and included gamma, and its difference
diagonal has length c, so it splits into two original tiles.

The final parallelogram has horizontal length

    b(uT-a²J),

an integer multiple of b, and slanted length

    a[(a²+b²)J-uT],

an integer nonnegative multiple of a by the lower bound on J. Thus this is
another ordinary a-by-b grid. All the same interface and angle identities of
Theorem 24 apply, regardless of whether its auxiliary r is integral; only actual
side lengths and the indicated triangular scales must fit. The resulting target
has area `X²/(bc)=bT²` tile areas, proving the construction.

At `(2,3,4)`, Delta23, F2, and the bound is T>=11; Section 6 improves the result
using explicit smaller seeds. When b is not squarefree, this theorem covers the
subfamily N=bT²; it does not dispose of other possible square multiples of the
squarefree kernel of b. When Delta<0, this particular macrogeometry fails; no
claim is made here about that complementary range.

## 8. What prevents a full classification

The area and coloring equations select discrete target sizes, and the corner
arguments remove small cases. However, at larger scales actual seams can admit
mixed a-, b-, c-edge decompositions. The short-chain forcing used for W and beta
scale one no longer holds. Inverting an additive construction or cutting a known
tiled larger triangle does not guarantee that the new cut follows tile edges.
Thus the successful other-scalene construction cannot simply be cut backward
into a theta tiling. No theorem here licenses either of these inversions.
