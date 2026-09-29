# Scale spectra for the W and beta-isosceles families

29 September 2026. Internal mathematical report. This supplies a uniform
structural theorem and checks two complete fixed-tile spectra. It does not
classify all instances of Erdős problem 634. No priority or external-review
claim is made.

**Later refinement in this snapshot.** The [eventual rational-family
construction](eventual-rational-families.md) proves that both divisors
are $d=1$ whenever $b(a^2+b^2)-a^2c>0$, with an explicit threshold.
The structural theorem below applies also in the complementary range.

## 1. Statements and attribution

Fix coprime integers `0<u<v` and the primitive tile

    a=uv, b=v²-u², c=v²,
    Q=b+c=2v²-u², P=b+2c=3v²-u².

The tile angles opposite a,b,c are alpha,beta,gamma, with
`3alpha+2beta=pi`; set `theta=alpha+beta`. Define

    W_t: sides t(v³,uQ,vb), angles (2alpha,beta,theta), count Q t²;
    B_t: sides t(v³,v³,uP), angles (beta,beta,3alpha), count P t².

Let `S_W` and `S_B` be the positive integer scales t admitting an actual
tiling by the fixed tile. The base side triples are primitive, so integer
boundary lengths make t an integer: for W the first and third sides have
gcd v, coprime to uQ; for B, gcd(v³,uP)=1.

**Uniform structural theorem.** Each of `S_W,S_B` is nonempty and eventually
consists of exactly the multiples of a positive divisor d of v. The two
families can have different d. In each family d equals the gcd of all its
realizable scales. More precisely, each scale set is a union of finitely
many arithmetic rays of common step v, and its eventual residue set is
the subgroup of Z/vZ consisting of the multiples of d.

**Effective sufficient version.** Suppose r is any verified additional
scale in the chosen family, and let `d0=gcd(v,r)`. Then every positive
multiple of d0 at least

    B = u r (v/d0 - 1) + d0

is realizable. This is a sufficient bound, not necessarily the least
conductor. If d0=1, it proves that every scale at least B is realizable.

**Two complete fixed-tile spectra.** For tile (2,3,4), that is (u,v)=(1,2),

    S_W = S_B = {2,3,4,...}.

Thus the exact counts in these two shapes are respectively `7t²` and
`11t²`, with `t>=2`. The 63-tile W seed and 99-tile beta seed are due to
Vico Bonfioli, not this project. His companion source already states both
complete-member results. The proofs below supply independently checked
geometry and arithmetic and must not be presented as newly discovered
spectra. The beta bridge/general eventual-gcd theorem appeared earlier in
this project's [beta-scale-bridges.md](beta-scale-bridges.md); the W version and explicit bound
are derived here.

## 2. One bridge construction treats both shapes

Use coordinates `(x,y)` for the physical point
`x(1,0)+y(cos beta,sin beta)`. Set h=1 for W and h=2 for B, and put

    F=b+h c, X=v³, Y=uF.

The corresponding scale-t triangle is

    T_t = {(x,y): x>=0, y>=0, x/Y+y/X<=t}.

Its sides are precisely those above. Consider the parallelogram

    R(p,q) = [0,pY] x [0,qX].

**Bridge lemma.** R(p,q) is tileable with `2pqF` copies whenever

    u divides q,  h p >= u.

It is also tileable by a pure a-by-c grid whenever `v divides p`, with
no lower bound on q.

For the first assertion initially assume `q<=hp`, and set

    H=qv, J=hpv, s=pub.

The identities `pY=Ja+s` and `qX=Hc` partition the box into three actual
polygons using the two parallel lines

    x/a+y/c=H,       x/a+y/c=H+s/a.

The left polygon is the triangle `(0,0),(Ha,0),(0,Hc)`, a standard
quadratic block of H² tiles. The right polygon is the translate by (s,0)
of the part of `[0,Ja] x [0,Hc]` with `x/a+y/c>=H`. Since J>=H, ordinary
a-by-c cells, cut on their b-diagonal when on the sloping boundary, tile
it with `2JH-H²` tiles.

The middle parallelogram has sides `(s,0)` and `(-Ha,Hc)`. Define

    U=(b,0), V=(-a²/b,ac/b).

In the physical metric

    |(x,y)|²=x²+y²+2xy cos beta,
    2ac cos beta=a²+c²-b²,

direct substitution gives `|U|=b`, `|V|=a`, `|U+V|=c`. Thus the cell on U,V
splits along its U+V diagonal into two congruent copies of the tile.
The middle macrovectors satisfy

    (pu)U=(s,0),     (qb/u)V=(-Ha,Hc).

These are positive integer multiples because u divides q. The middle
uses `2pqb` tiles. The pieces have full straight interfaces, disjoint
interiors, and exhaust the box. Their total is

    H² + (2JH-H²) + 2pqb = 2pq(hv²+b) = 2pqF.

To remove the condition q<=hp, apply this construction with q=u and
stack q/u translated copies. The hypothesis hp>=u is exactly what is
needed for the elementary piece. No alignment of internal subdivisions
on different sides of an interface is required: T-junctions are allowed.

For the pure-grid assertion, the box side ratios are

    pY/a=pF/v,       qX/c=qv.

They are integers if v divides p. Each a-by-c cell is two tiles.

## 3. Exact additive gluing, with all needed seed hypotheses

If p,q are both realizable in the chosen family, the triangle T_(p+q)
is the disjoint-interior union of

* R(p,q), with lower-left corner (0,0);
* T_p translated by (0,qX);
* T_q translated by (pY,0).

Indeed their two sloping outer sides are both on
`x/Y+y/X=p+q`; their remaining shared sides are precisely the two exposed
sides of R(p,q). Therefore

    p,q in S, u|q, p>=u  ==> p+q in S

for both families. For beta the weaker bound `p>=ceil(u/2)` also works.
The pure grid, with p,q interchanged if necessary, gives

    p,q in S, v|q  ==> p+q in S.

The second triangle must actually be tiled; an arbitrary difference
q between two target scales cannot be used without that seed hypothesis.

Beeson's Theorem 11 gives W_v with cQ tiles, and hence v belongs to S_W.
Every W_t gives B_t by adding a tv-fold quadratic copy of the original
tile. Its sides are `(tva,tvb,tvc)`; the common side is tvb, and the
collinear base segments have lengths tuQ and tva, summing to tuP.
The count changes from `t²Q` to `t²Q+(tv)²=t²P`. Thus

    v in S_W subset S_B.

In particular both scale sets are nonempty, and every multiple of v is
realizable by quadratic subdivision. The earlier phrase 'either empty
or eventually ...' can be strengthened to nonempty for these families.

## 4. Eventual-gcd theorem and explicit conductor bound

Fix either family and write S for its scale set. Quadratic subdivision
gives kr in S for every r in S and every positive integer k.

Since v is itself realizable, the pure-grid rule shows

    r in S ==> r+v in S.

For each residue j modulo v that appears, let m_j be its least
realizable member. Then the entire ray `m_j+v Z_{≥0}` lies in S, and
these rays exhaust S. There are at most v such rays. This proves
eventual periodicity modulo v, but alone does not identify its residues.

Let R be the set of residues that appear. Start at the known scale v,
which exceeds u. For any r in S, the scale ur is realizable; it may be
added repeatedly by the new bridge rule. Consequently every residue
`n u r mod v` belongs to R. Because u is invertible modulo v, these are
exactly the cyclic subgroup generated by r. For any finite collection
of scales, adding their ur increments in arbitrary nonnegative
combinations realizes the subgroup generated by all their residues:
in a finite group, nonnegative multiples supply inverses as well.

Choose finitely many scales whose gcd together with v is
`d=gcd S`. Such a finite choice exists because the gcd is an integer
divisor of v and decreases only finitely many times. The argument shows
that every multiple-of-d residue occurs. No other residue can occur
by the definition of d. Hence the finite collection of rays eventually
exhausts exactly the multiples of d, and d divides v.

For the effective bound from one seed r, put d0=gcd(v,r). Starting at v,
we can add ur and v repeatedly, so

    v + {A v+B ur: A,B nonnegative integers} is contained in S.

For every multiple n of d0, choose the unique
`j in {0,...,v/d0-1}` with `j ur congruent n modulo v`.
If `n>=ur(v/d0-1)+d0`, then

    n-jur >= d0.

The left side is a positive multiple of v, so it is at least v. Therefore
`n=v+j ur+A v` with A nonnegative, proving the displayed bound.

This theorem has an exact computational limitation. Verified seeds give
an explicit sufficient conductor for multiples of their gcd; they do
not show that an unobserved future seed cannot lower that gcd. When a
seed r coprime to v is known, d=1 is certified and every scale beyond
the displayed bound is settled. Otherwise the actual d and the least
members m_j remain unknown. Merely enumerating more scales does not
give a terminating algorithm to certify d or all omitted residue
classes. No effective uniform bound for all exceptional scales has
been proved here.

## 5. Complete spectra for tile (2,3,4)

At u=1,v=2, both bridge constructions work for every p,q>=1. Thus both
S_W and S_B are additively closed.

* The scale-two W seed is Beeson's explicit 28-tiling, Theorem 11 with
  M=2,K=4. Adding a standard scale-four tile gives the 44-tile beta seed.
* The scale-three W seed is Bonfioli's `CevianTiling63.lean`, with target
  `(18,21,24)` and tile `(2,3,4)`. Adding a standard scale-six tile would
  also give a 99-tile beta seed.
* Bonfioli separately supplies the beta 99-coordinate certificate with
  target `(24,24,33)` in `tiling_99_isobeta_24_24_33.txt`.

Every integer t>=2 is a nonnegative sum of 2 and 3. The actual bridge
gluing therefore constructs both targets at all such scales. The
scale-one exclusions are the corresponding cases of the W/beta proof
in this project (and these two small counts were previously excluded
in the literature). It follows that both spectra are exactly t>=2.

This directly disproves necessity of `v|t` in BOTH branches, already at
the verified scale-three examples. It leaves the general scale-one
proofs intact. Any attempted extension of their local short-seam
forcing to imply `v|t` must fail.

## 6. Independent exact checks and source handling

The original Python program `scripts/check_scale_bridges.py` generates
the bridge pieces with rational oblique coordinates and checks their
side lengths, containment, exact area, and every pair for disjoint
interiors. Its seven cases include both W and beta, u>1, and stacked
bridges. The uniform proof is the symbolic construction above; the
finite checks test its implementation.

A separate internal reviewer independently checked the metric identities,
three-region partition, stacking, additive gluing and conductor argument
symbolically and found no gap. This is an internal mathematical check,
not external review or formal verification.

The same script optionally reads Bonfioli's W63 and beta99 coordinates
as data. It imports and executes none of his code, uses Fraction
arithmetic throughout, and independently checks all 1,953 and 4,851
tile pairs. The W63 data are scaled by 8; the script divides the
coordinates by 8 and checks primitive tile sides 2,3,4. The results,
including the source-file hashes, are in
the optional JSON output of the checker.

Source snapshot: Vico Bonfioli, `ElVec1o/erdos_634_proof`, commit prefix
`2f9af59`. Relevant primary files are `paper/erdos-634-companion.tex`,
sections 'Realizability: the collar induction and the first complete
member' and 'W-addition, and the second complete pair';
`lean/Erdos634/CevianTiling63.lean`; and
`code/engine/tilings/tiling_99_isobeta_24_24_33.txt`.
Upstream coordinate files and code are not copied into this report or
our verifier. Reproduction takes a separately obtained upstream tree:

    python scripts/check_scale_bridges.py --bonfioli-root /path/to/erdos_634_proof

Without that option, the program checks only the original bridge
constructions. Attribution of the two complete-member spectra and
their nonclassical seeds belongs to Bonfioli; the generalized bridges
and eventual-gcd analysis must be distinguished from those inputs.

## 7. Remaining gap

The full problem is not solved. Even in these two fixed-angle families,
the general divisor d and the finite exceptional scales have not been
determined. The proof reduces arbitrary-scale behavior to a finite
residue structure for each fixed tile, but provides no uniform finite
bound covering all primitive tiles and all exceptions. Other target
families, including the independent N=105 instances, remain outside
this result.
