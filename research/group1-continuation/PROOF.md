# A two-long-edge obstruction for every primitive W and beta tile

6 October 2026. Internal continuation of the Group-1 investigation.
This note proves a universal boundary obstruction. It does not classify
all Group-1 scales or solve Erdős 634. No priority claim is made.

The argument adapts the complete-chain proof in
[`docs/theta-branch.md`](../../docs/theta-branch.md), Section 2, to two
other target shapes. It uses no candidate W/beta packing theorem, no
retracted scale-divisibility statement, and no edge-to-edge assumption.

## 1. Statement

Let coprime positive integers u<v specify the primitive tile

    a=uv, b=v²-u², c=v²,
    3alpha+2beta=pi, gamma=pi-alpha-beta,

where a,b,c are opposite alpha,beta,gamma. No order between a and b is
assumed.

Let a convex target be either the W triangle with angles
(2alpha,beta,alpha+beta), or the beta-isosceles triangle with angles
(3alpha,beta,beta).

**Theorem.** For every primitive parameter pair u<v, if such a target is
tiled by congruent copies of this tile,
every outer side contains at least two whole edges of length c.

Consequently, at any realizable scale t, each of the target side lengths
must belong to the numerical semigroup translate

    2c + <a,b,c>.

In particular, for every integer v>=2, the primitive tile

    (a,b,c)=(v,v²-1,v²)

does not tile its W target at scale one. Its side Q=2v²-1 is shorter
than 2c=2v².

There is a second uniform excluded family: u=v-1, for every v>=2.
Here the W side vb=v(2v-1)=2v²-v is again shorter than 2c.
Thus any possible primitive W tiling at scale one must satisfy

    u>=2 and v-u>=2.

This is an exclusion of a fixed tile and target shape. It does not
exclude the integer Q globally: another tile or another classified
branch might realize that count.

## 2. Corner inventories and the first c edge

The relation 3alpha+2beta=pi gives gamma=(pi+alpha)/2, so gamma
is obtuse. Also a<c and b<c. The argument does not require alpha<beta
or require every target angle to be smaller than gamma.

Also alpha/pi is irrational. Indeed

    2cos(alpha)=2-u²/v²

is a nonintegral rational number. If alpha/pi were rational,
2cos(alpha) would be an algebraic integer, hence an integer.

Writing beta=pi/2-3alpha/2 and gamma=pi/2+alpha/2, and comparing
the rational-pi and irrational-alpha coefficients, gives the exact
corner inventories:

* a corner k alpha, for k=2 or 3, contains k alpha angles only;
* a corner beta contains exactly one beta angle;
* a corner alpha+beta contains one alpha and one beta angle.

At a straight outer-boundary vertex the possibilities are
alpha+beta+gamma or 3alpha+2beta. In particular, once a beta and
a gamma angle are present there, the remaining angle is precisely one
alpha angle.

An outer side is partitioned into complete tile sides by convexity.
Every a- or b-edge presents one gamma endpoint, while a c-edge does
not. Two gamma angles cannot meet at a straight boundary vertex;
no gamma angle occurs at a target corner. If an outer side had k
edges and no c-edge, their k gamma endpoints would have to occupy
only k-1 internal boundary junctions. This is impossible. Hence every
outer side contains at least one c-edge.

## 3. A unique c edge is impossible

Suppose one outer side has exactly one c-edge PQ. Name its endpoints
so that its tile PQR has alpha at P, beta at Q, and gamma at R.
Then PR=b and QR=a, with a<c and b<c.

Any chain of a- and b-boundary edges preceding P forces one gamma
angle at P. To see this, if the chain has k edges, their k gamma
endpoints cannot occur at the outer target corner and cannot share
an internal boundary junction, so every remaining junction, including
P, is occupied. The analogous argument after Q forces one gamma at
Q whenever Q is not the target corner. Therefore no additional gamma
angle is possible at either P or Q. If one of these points is a target
corner instead, its corner inventory already excludes gamma.

At Q, the c-edge tile presents beta. Q cannot be a target corner
2alpha or 3alpha, by the inventories in Section 2. There are two cases.

1. If Q is a target corner beta, QR lies on the other outer side.
   Thus R is on the outer boundary and cannot support a second gamma
   angle.
2. Otherwise Q is either an alpha+beta corner or an internal point
   of the chosen outer side. In the latter case the preceding chain
   argument has already supplied a gamma angle there. In both cases
   exactly one alpha tile lies immediately across QR at Q. Its edge
   on the ray QR has length b or c. We claim that some tile edge on
   this opposite bank passes through R.

   The segment QR is an intact full side of the original tile.
   Consequently its opposite bank is covered consecutively by whole
   collinear tile sides, starting at Q, until reaching or crossing R.
   No such edge extends backward through Q: Q is on the boundary of
   the convex target, and in this case the ray QR points inward.
   At an intermediate endpoint before R, the original tile's side
   continues straight, so the opposite partition also continues.
   This is the complete-side partition of a maximal seam; arbitrary
   T-junctions on that seam do not interrupt it.

   If the first edge has length c, it crosses R because c>a. If its
   length is b>a, it likewise crosses R. In the remaining case it
   has length b<a. If no edge crossed R, the complete chain would
   end exactly at R and express a as a sum of full side lengths,
   starting with b. No c-edge could occur because c>a. No a-edge
   could occur after the first positive b-edge either. Thus every
   edge in the chain would have length b, requiring b to divide a.
   This is impossible: gcd(a,b)=1 and b=v²-u²>=3. Equality a=b
   is also excluded by these facts. Hence some opposite edge must
   cross R in all cases.

   Its tile supplies a flat angle pi at R, separately from the
   original gamma. This prevents any further gamma angle at R,
   since pi+2gamma>2pi.

Now consider PR. It cannot itself be an outer side: together with PQ
that would make P an outer corner alpha, and neither target has such
a corner. Hence PR has tiles on its opposite bank. The maximal seam
on this line cannot extend beyond P, since P is on the target boundary.
It cannot extend beyond R either. In case 1, that would leave the
convex target. In case 2, the forward continuation of PR past R enters
the interior of the flat tile crossing QR, and thus cannot be a seam.

The opposite bank of PR is consequently a partition of the complete
segment PR into whole tile edges, of total length b. A c-edge cannot
fit. If a b-edge occurred, it would occupy the entire segment; its
tile would present gamma at P or R, both already excluded. Therefore
the entire opposite chain consists of a-edges. This requires a to
divide b. But gcd(a,b)=1 and a=uv>=2. Contradiction.

The argument explicitly allows a long edge to pass through another
tile's corner: this is precisely case 2 above. It therefore does not
discard T-junctions. The theorem follows.

## 4. Scope of the continuation

The boundary theorem covers every primitive pair, including a>b.
The decisive extension is the complete QR-chain argument: the first
alpha tile need not itself cross R, but some tile on its bank must.
The W scale-one exclusions for u=1 and u=v-1 are uniform in v.

The theorem does not exclude all W scale-one targets: primitive
parameters with u>=2 and v-u>=2 remain possible under this test.
It does not prove a general beta scale-one exclusion or existence at
any scale surviving the boundary test. The known positive set
v+<u,v> remains a sufficient construction set, not a proved exact
spectrum.

## 5. Audit of the removal of the side-order hypothesis

The first version of this note assumed a<b so that the alpha tile
immediately across QR had an edge longer than QR. A separate
project-internal reviewer checked the replacement argument above:

* the unbroken original side QR ensures a whole-edge partition on
  the opposite bank until R;
* convexity caps that partition at Q, so its first edge really starts
  there and has length b or c;
* if no opposite edge crossed R, the first b-edge would force the
  entire length a to be a multiple of b, which primitivity excludes;
* an edge crossing R supplies the required flat sector and blocks
  continuation of PR past R in its actual interior half-plane;
* at a target corner 3alpha, the exclusion of gamma follows from
  the exact angle inventory, even when 3alpha exceeds gamma.

The terminal PR argument requires only that c>b and that a does not
divide b, both valid for every primitive pair. Thus removing a<b
introduces no edge-to-edge assumption or restriction on T-junctions.
This is an independent internal mathematical audit, not external
refereeing or formal verification.
