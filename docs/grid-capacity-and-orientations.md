# A capacity obstruction for every bounded-sided single-grid grammar

4 October 2026. Denis Paliy, research with ChatGPT assistance.
This is a fixed-pair obstruction, not a
solution of Erdős 634 or a refutation of arbitrary recursive construction
recipes. Its capacity mechanism already appears for T/P blocks in the
1 October `Erdos634_unbounded_blocks_PROOF` archive, whose scope is
recorded in the [archive reconciliation](audits/research-2026-10-03.md). The extension here is to
arbitrary convex single-grid blocks, and more generally to blocks with a
uniformly bounded number of straight boundary segments.

## Statement

For each positive multiple r of 3, let R_r have side lengths

    a=r²−1, b=2r+1, c=r²+r+1.

Then c²=a²+ab+b², so its angle opposite c is 120 degrees. There are
equilateral triangles E_r tiled by congruent copies of R_r. Nevertheless,
**every tiling of the same E_r by the same R_r, described as a positive
partition into convex single-grid regions, requires at least r+1 regions.**

A single-grid region here is any finite polygonal union of unit triangles
from one ordinary triangular grid of R_r: all its unit triangles are
translations of one orientation or its half-turn. Convexity restricts its
shape, but does not require it to be a triangle or parallelogram. In
particular the result includes triangular grids, parallelogram grids, and
convex corner-deleted triangular or parallelogram grids.

If convexity is replaced by the requirement that each region has at most s
straight boundary segments, the required number K satisfies

    K >= c/[s(r+1)] = (r + 1/(r+1))/s.

Thus no fixed finite catalogue of bounded-sided single-grid polygon types
admits a universal block bound. The lower bound concerns every alternative
tiling of the fixed target by the fixed tile, and is independent of its
size or the number of unit tiles.

## 1. A character with small tile value

Put rho=exp(i*pi/3), and use the reference triangle with vertices
0,a,a+b*rho, traversed counterclockwise. Let theta=arg(a+b*rho), so
its consecutive directed edges have directions 0,pi/3,pi+theta and
lengths a,b,c.

The number theta/pi is irrational. Indeed

    2 cos(theta)=(2a+b)/c

is rational and strictly between 1 and 2. If theta/pi were rational,
this would be a rational algebraic integer, hence an integer.

Fix one side of the equilateral target horizontally. Connectivity through
positive-length tile contacts implies that every directed tile edge lies
in G=Z theta + Z(pi/3), modulo 2pi. To start propagation, use a tile with
an edge on the horizontal target side; changing which reference edge is
aligned only shifts its orientation by an element of G. Reflections have
the same property. A generic path between interior tile points avoids all
vertices, proving the necessary contact connectivity without an edge-to-edge
assumption.

Irrationality makes

    chi(n theta + j*pi/3)=(-1)^j

well-defined. It is multiplicative under angle addition and odd under
direction reversal. For any directed polygon boundary define Phi as the
sum of edge length times chi(direction). Internal edges cancel after
atomizing their overlaps, so Phi is additive under all permitted
dissections, including T-junctions.

The reference tile has

    Phi(R_r)=a-b-c=-(c-a+b)=-q,
    q=3(r+1)>0.

Rotation multiplies this by a sign. Reflection negates edge directions
and reverses the counterclockwise traversal; because chi(-angle)=chi(angle),
it also changes the value only by a sign. Hence every congruent unit tile
has Phi-value either q or -q.

An equilateral target of side length L has counterclockwise directions
0,2pi/3,4pi/3. Therefore

    Phi(E_r)=3L.

## 2. Capacity of a convex single-grid region

Let B be any contained single-grid block. Choose the positive orientation
of its grid, and let S be the number of its positive unit triangles minus
the number of half-turn unit triangles. Then

    |Phi(B)|=q |S|.

Use now the full signed-direction signature, whose coordinates separately
record net directed length in each unoriented edge direction. Choose the
coordinate of the c-edge of the positive unit tile. The three directions
within one grid are distinct, so the a- and b-edges contribute nothing to
this coordinate. Additivity gives exactly ±cS in that coordinate.

Since B is convex, in that direction its boundary has at most one segment
of each orientation (merge collinear consecutive segments). Each segment
has length at most diam(E_r)=L. The absolute difference of their two
lengths is consequently at most L. Thus

    c |S| <= L,        |Phi(B)| <= qL/c.

For a positive partition into K such blocks, their boundaries cancel,
even when their grids differ and their interfaces contain T-junctions.
Consequently

    3L = |Phi(E_r)| <= sum_B |Phi(B)| <= K q L/c,

and

    K >= 3c/q = c/(r+1) = r+1/(r+1).

As K is an integer, K>=r+1. This bound applies to all such descriptions,
not merely to the supplied construction.

For a nonconvex block with at most s straight boundary segments, the
absolute c-coordinate is at most sL. The same proof gives

    K >= 3c/(s q)=c/[s(r+1)].

The convex estimate is sharper because opposite parallel lengths are
subtracted, and only one of each occurs.

## 3. Actual positive targets, uniformly in r

It remains essential to establish existence. Here it can be made fully
explicit without using the angular classification or any negative theorem.
The following is the standard ideal-trapezoid construction already proved
in the [general-spectra proof](../research/general-spectra/PROOF.md),
sections 4–5.

For r=3h, gcd(a,b)=1: every common divisor divides 3, since
4a=(2r+1)(2r-1)-3, while a=-1 modulo 3. This leaves an infinite
family of primitive triples. Also a>b for every r under consideration.

Write a=Qb+R with 0<R<b; put H=ab and k=Q+2. The ideal trapezoid with
shorter base a²+b² and legs H has a positive dissection into three
R_r-shaped triangular grids of scales a,c,b. In 60-degree coordinates its
vertices and interior dividing point are

    A=(0,0), B=(a²+b²+H,0), C=(a²+b²,H), D=(0,H),
    F=(a²,H),

and the three triangles are AFD, ABF, FBC. Their side lengths are,
respectively, a(a,b,c), c(a,b,c), b(a,b,c), in suitable order.

For every integer t>=k,

    tH-a²-b² = a(b-R)+b[a(t-Q-1)-b],

with both coefficients nonnegative. Attach the parallelogram of that
width and slanted side H. Splitting its width into the indicated a- and
b-strips tiles it by a-by-b parallelograms, each cut on its length-c
diagonal. This gives an ideal trapezoid of shorter base tH and legs H.

Stack k bands with shorter bases kH,(k+1)H,...,(2k-1)H. The result is an
ideal trapezoid with shorter base and legs both kH. Three congruent cyclic
copies partition an equilateral triangle of side

    L=3kH=3k ab.

For explicit coordinates of the outer triangle use

    (0,0), (3kH,0), (0,3kH).

The three trapezoids are obtained from the cyclic dissection in the cited
project proof with all three parameters equal to k; equivalently the
interior point is (kH,kH), and the extra boundary points are
(kH,0),(2kH,kH),(0,2kH). This is a positive dissection and every band has
the positive construction above. Its count is

    N=L²/(ab)=9 k² ab.

Therefore each r=3,6,9,... supplies an actual tileable fixed pair with
the proved lower bound K>=r+1. No finite search is needed for either
the positive construction or the lower bound.

## 4. Exact limitation

This does not establish an orientation lower bound. The positive
trapezoid construction uses at most **18 rigid orientations**, uniformly in
the tile parameters and number of bands. In complex coordinates z=x+y*rho,
write R={0,a,a+b*rho}, theta=arg(a+b*rho), and Rbar for its reflection.
For the basic trapezoid, the exact vertex-set identities are

    AFD=F-aR,       FBC=B+b*rho²R,       ABF=c exp(i theta) Rbar.

In the attached extension, an a-horizontal, b-slanted cell uses Rbar
and its half-turn; a b-horizontal, a-slanted cell uses rho²R and its
half-turn. Band stacking introduces only translations. The three outer
trapezoids use cyclic 120-degree rotations. Thus every unit tile lies
in one of the three sixfold orbits

    rho^j R, rho^j Rbar, rho^j exp(i theta) Rbar,  0<=j<6.

This is thus also
an explicit demonstration that bounded orientations do not bound the
number of convex single-grid regions.

After naming the longer short side a, the same bound of 18 holds for
every primitive 120-degree norm tile on the entire equilateral tail
supplied by the standard band construction, not
just the displayed r-family. It supplies no alternative for an unknown
tileable scale below that sufficient tail.

Nor does it refute a grammar that allows one block to stand for a
parameterized repetition of different grids, or permits a single-grid
region with an unbounded number of boundary segments. For a nonconvex
comb-shaped grid region, the net c-direction boundary length can exceed
the diameter; the convex capacity estimate cannot be applied. A finite
recipe that names the whole repeated trapezoid is an example of the
former escape. Treating that whole recipe as one block changes the
grammar and must be made explicit.

The archive already expressly leaves finite recursive recipes open.
Thus this proof closes the bounded-sided single-grid extension of
the old T/P conjecture, but does not justify claiming that every finite
recursive or parameterized construction grammar is impossible.

## Independent internal audit

An independent agent checked the exact proof, including direction
propagation, reflection signs, convex signed-direction capacity, the
three triangles and strip arithmetic, and returned no proof errors.
The final cyclic partition is verified directly as follows. Put d=kH,
take outer vertices O=(0,0), U=(3d,0), V=(0,3d), and P=(d,d),
Q=(d,0), R=(2d,d), S=(0,2d). The quadrilaterals OQPS, QURP, SPRV have
disjoint interiors and union OUV. Each is an ideal trapezoid with bases
d,2d and legs d. This audit is internal and is not external peer review
or formal proof-assistant verification.
