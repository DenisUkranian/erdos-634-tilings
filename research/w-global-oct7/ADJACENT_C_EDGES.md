# Adjacent longest edges in every W and beta boundary

7 October 2026. This is a necessary geometric condition, not a complete
classification of W scales or of Erdős 634. Reflections and arbitrary
T-junctions are allowed. The proof strengthens the complete-chain argument
in `../group1-continuation/PROOF.md`; no order between a and b is assumed.

## The theorem

Let 0<u<v be coprime and put a=uv, b=v²-u², c=v². Write alpha,beta,gamma
for the opposite tile angles, so 3alpha+2beta=pi and gamma=2alpha+beta>pi/2.
If the target is W, with corners (2alpha,beta,alpha+beta), or beta-isosceles,
with corners (3alpha,beta,beta), **every target side contains two consecutive
whole c-edges**.

## Blocked endpoints

The irrationality of alpha/pi follows from the nonintegral rational number
2cos(alpha)=2-u²/v². The exact target-corner inventories are therefore:
k alpha has k alpha angles (k=2,3), beta has one beta, and alpha+beta has
one alpha and one beta. In particular no target corner contains gamma.
A straight boundary fan is either alpha+beta+gamma or 3alpha+2beta.

Fix a target side. Mark an internal junction precisely when one of the
tiles supported on this side has gamma there; a tile merely touching the
side at its gamma vertex does not mark the junction. Each a- or b-edge
provides one such mark. All marks are distinct because 2gamma>pi, and all
are internal because target corners contain no gamma. Call the endpoints
of the side and all its marked junctions blocked.

We claim that a supported c-edge PQ cannot have both endpoints blocked.
Name its tile PQR with alpha at P, beta at Q, gamma at R. Thus PR=b and
QR=a. At either blocked endpoint an additional gamma angle is impossible:
at a mark it would join the marking gamma in the boundary half-plane;
at a corner it is excluded by the exact inventory.

If Q is a beta corner, QR is on the other target side and R is a boundary
point. Otherwise Q is either a marked straight point or an alpha+beta
corner. It cannot be a 2alpha or 3alpha corner since its tile has beta.
Exactly one alpha tile lies immediately across QR at Q. Its edge there
has length b or c. If this length exceeds a, it crosses R. If instead
b<a and no opposite edge crossed R, the opposite bank of the intact
side QR would be a whole-edge chain from Q to R starting with b. No
c-edge or a-edge could fit after that first positive b contribution.
Thus all its edges would be b and a would be a positive integer multiple
of b, impossible since gcd(a,b)=1 and b>=3. Therefore in this case too
some opposite edge crosses R. (At every intermediate endpoint the
unbroken edge QR supplies a straight sector and forces continuation;
convexity prevents an edge extending backwards through Q.)

Hence R is either a boundary point, or lies in the relative interior of
a crossing tile edge. In the second case that tile supplies a separate
straight sector at R. No further gamma angle is possible at R, since
respectively 2gamma>pi or pi+2gamma>2pi.

PR cannot be an external side, since the corner at P would then be alpha,
which neither W nor beta has. Its opposite bank is a whole-edge chain
of length b: its extension past P leaves the convex target, while its
extension past R either leaves the target or enters the interior of the
crossing tile just found. The chain contains no c-edge because c>b.
A b-edge would occupy the entire segment and contribute gamma at P or R,
both forbidden. The chain therefore consists entirely of a-edges, giving
a|b, again impossible since gcd(a,b)=1 and a>=2. This proves the claim.

## Counting unmarked junctions

Suppose the chosen side has n whole edges, of which k are c-edges. Its
n-k other edges give exactly n-k marked internal junctions. Thus k>=1
and exactly k-1 internal junctions are unmarked. By the claim, every one
of the k c-edges needs an unmarked internal endpoint. Since there are
only k-1 such junctions, two c-edges share one. They are consecutive.
This proves the theorem.

## A whole infinite scale-two boundary word

For u=v-1 and scale m=2 the W side opposite beta has length
2v(2v-1). Let (A,B,C) count its edges (a,b,c). The theorem gives C>=2.
Reduction modulo v gives v|B. If B>=v, then after its contribution
there is less than 2c remaining, impossible. Therefore B=0. The length
equation becomes A(v-1)+Cv=4v-2. Hence A=2+kv and C=2-k(v-1).
For v>=3 nonnegativity and C>=2 force k=0. Thus for v>=3 the
unique counts are A=C=2. At the 2alpha corner its first edge must be c,
since the corner contains alpha tiles and an a-edge is not incident to
alpha. Adjacency now forces the complete word c,c,a,a toward theta.

For v=2 a=2,b=3,c=4, side12 also permits three c-edges; the unique-word
claim is intentionally restricted to v>=3.

In particular W56, (u,v,m)=(2,3,2), has side30 word **9,9,6,6** from its
2alpha corner to its alpha+beta corner. In coordinates (x,sqrt(2)y),
the target is O=(0,0), A=(56,0), C=(46,20). Here C is 2alpha and A
is theta, so the side runs from C to A. Its endpoints are

    (46,20), (49,14), (52,8), (54,4), (56,0).

This is a necessary boundary word, not a completion of W56. The two
remaining sides and the interior remain to be checked.

## Theta extension

The same conclusion holds for the theta-isosceles target with corners
(alpha,alpha+beta,alpha+beta). Its alpha corner contains exactly one
alpha tile; again no corner contains gamma. In the blocked-edge argument
Q, which has beta, can only be a theta corner or a marked flat point.
Thus the opposite-QR chain necessarily contains an edge crossing R.

The only new issue is that PR could be external, in which case P would
be the alpha apex and R would lie on the other target side. But QR is
then a genuine chord, starting at Q on the chosen target side and ending
at R on a different target side. Extending the crossing edge past R
would leave the convex target. This contradicts the already established
crossing. Hence PR is internal here too, and the same whole-b-chain
contradiction and unmarked-junction count apply. All three theta sides
therefore contain two consecutive c-edges.

The theorem and this additional external-PR case received an independent
project-internal proof audit during this continuation. This is not an
external review or proof-assistant verification.

## The two exact W56 boundary roots

The first c-edge has alpha at C. The last a-edge has beta at A, because
no target corner contains gamma. At their common boundary junction the
two a-edges cannot both present gamma. Thus both a-edges, in the C-to-A
ordering, present gamma at their first endpoint and beta at their second.
Only the orientation of the second c-edge remains free. The third vertices
of the four boundary triangles, in that order, are exactly:

| Second c-edge starts with | First | Second | Third | Fourth |
| --- | --- | --- | --- | --- |
| alpha | (133/3,50/3) | (142/3,32/3) | (47,8) | (49,4) |
| beta | (133/3,50/3) | (1289/27,266/27) | (47,8) | (49,4) |

Each triangle uses the corresponding successive pair of listed boundary
vertices and its third vertex in this table. Both four-tile roots are
contained and have pairwise disjoint interiors, as checked exactly in
`W56-boundary-roots.json`. Thus neither is discarded merely from the
short boundary. `w56_boundary_search.py` starts the finite exact search
from these two roots. A resource-limited run is INCOMPLETE; the boundary
lemma is not a claim of nonexistence or existence of W56.

## Bounded search outcome

A fresh search rooted at this necessary boundary was run for a total of
300 seconds. The alpha-first second-c root used 240 seconds, 13,305 nodes,
and reached 47 of 56 placed tiles. The beta-first root used 60 seconds,
3,009 nodes, and reached 48 of 56 placed tiles. Both runs stopped with
**INCOMPLETE**. No tiling, exhaustive exclusion, or full refutation
certificate was obtained. These runs do not change the status of W56.

The reports are `W56-boundary-search.json` and
`W56-boundary-root1-search.json`. The independent audit caught a temporary
coordinate-label reversal before these final runs: C=(46,20), not
A=(56,0), is the 2alpha corner. The committed roots and final search
reports all use the corrected C-to-A boundary. The incorrect roots are
not used in any inference.
