# Independent audit: realization of a complete disk certificate

Date: 2026-10-06.

Scope: Section 4 of [`exact-seam-certificates.md`](../exact-seam-certificates.md).
This is a proof audit and an expanded justification of an existing theorem.
It is not a new classification of tile counts, and it does not replace the
unresolved problem of describing all admissible disk gluings uniformly.

## Finding

The sufficiency theorem is correct. A **complete oriented disk gluing**, with
positive matching atom lengths and the stated exact angle sums, already
guarantees a triangular tiling without overlaps. There is no further global
embedding condition to guess after those checks pass.

The remaining geometric search is to find such a disk, or to prove that none
exists, from incomplete data such as side-contact trees and angle inventories.
Those incomplete data do not determine the required disk.

The proof of sufficiency does not use integrality, the contact-forest lemma,
or congruence of the faces. Those hypotheses provide a finite arithmetic
description and recover the lengths. Once positive lengths have been assigned,
the following more general realization statement applies.

## Realization statement

Let X be a finite oriented regular cell decomposition of a space homeomorphic
to a closed disk. Give every face a nondegenerate Euclidean triangle, with
finitely many marked points in the relative interiors of its sides. Assume:

1. Each marked side atom has positive length, and paired atoms are glued by
   the endpoint-matching isometry that reverses their face-boundary directions.
2. At each interior vertex, the sum of all incident face angles is exactly
   2 pi. A side-interior marked point contributes pi.
3. There are exactly three designated boundary corners. Their angle sums
   theta_1, theta_2, theta_3 lie in (0, pi); every other boundary vertex has
   angle sum pi.

Then X admits an orientation-preserving map to the plane whose restriction
to every face is a Euclidean isometry. This map is a homeomorphism onto a
closed convex triangle. In particular, the face images form a genuine tiling.
The boundary chain lengths determine the three side lengths of the target.
Consequently, checking prescribed target side lengths gives the prescribed
triangle up to a Euclidean isometry. The identity
theta_1 + theta_2 + theta_3 = pi follows from the conclusion; it may also be
included as a redundant finite check.

## Expanded proof

### 1. Local charts and consistent development

Glue the given Euclidean faces using the matching atom isometries. At an
interior point of an atom, the two incident half-neighborhoods unfold to an
ordinary planar neighborhood. At an interior vertex, the cyclic link supplied
by the disk topology orders the incident angular sectors. Their positive
angles sum to exactly 2 pi, so their union unfolds once around that vertex
and is locally isometric to a planar disk.

Thus the whole interior X^o is an oriented flat surface, including its
vertices. Its Euclidean chart transitions preserve orientation. Since X^o is
simply connected, continuation of one chart along paths has no monodromy:
homotopic paths give the same chart, and every closed path is contractible.
Equivalently, if the vertices are initially removed, the generators going
around them have identity Euclidean holonomy because each full fan has total
angle 2 pi. The resulting development

    F : X^o -> R^2

is an orientation-preserving local isometry. No injectivity is asserted at
this step.

The development on each open face is the restriction of a single Euclidean
isometry, which extends to its closed face. These extensions agree across
paired atoms, and at their endpoints, by continuity. They therefore give a
continuous map F on the finite closed disk X. At a boundary point its local
model is a Euclidean sector with angle equal to the prescribed boundary
angle sum.

### 2. The developed boundary is a simple triangle

Traverse the boundary in its positive orientation. At a boundary vertex of
angle pi the tangent direction continues straight; it does not reverse.
Each chain between successive designated corners therefore develops to one
straight segment of positive length, traversed once.

At a designated corner the exterior turn is pi - theta_i, strictly between
0 and pi. Continuity of F makes the three segments a closed chain. They are
not collinear, since their turns are strictly between 0 and pi. Any such
closed three-segment chain is a simple triangle, and the positive turns give
its positive orientation. Hence F restricts to a homeomorphism from the
boundary of X onto the boundary of a convex triangle T.

### 3. Degree rules out every fold and overlap

For y outside F(boundary X), every preimage of y lies in X^o. There are only
finitely many such preimages: otherwise compactness would supply an
accumulation point, which cannot lie on the boundary and would contradict
the local injectivity of F in X^o. Every preimage has local degree +1 because
F preserves orientation.

The degree of F at y is the winding number of the positively oriented
boundary triangle. It is 1 inside T and 0 outside T. Therefore each point
inside T has exactly one preimage, and no point outside T has a preimage.

No interior point of X can map to the boundary of T: its locally open image
would contain a point outside T, a contradiction. The boundary map is already
one-to-one, so F is a continuous bijection from X onto T. Compactness makes
it a homeomorphism. Each face is mapped by its Euclidean isometry; hence its
image is the required congruent tile when all original faces are congruent.

This argument also covers T-junctions. They are ordinary flat points of X
after all incident sectors, including the one straight angle, are included.

## A rational-development implementation can omit angle evaluation

The preceding proof audits the theorem already in the repository. A useful
implementation refinement is to check a global development directly. The
following statement supplies its justification and does **not** assume that
the interior angle sums have already been checked.

**Direct-development criterion.** Let X be an oriented finite regular cell
disk whose faces have specified nondegenerate Euclidean triangle metrics.
Suppose an orientation-preserving Euclidean isometry is assigned to each
closed face, the assignments agree on every glued atom and quotient vertex,
and the resulting boundary map traverses a simple triangle once positively.
Then these maps give a tiling of that triangle by the specified faces.

**Proof.** The agreement checks produce a continuous map F on X. Let S be
the finite union of all developed face edges. For any y outside S, every
preimage lies in a face interior and contributes +1 to the degree; there are
at most as many preimages as faces. The boundary winding gives degree 1
inside the triangle and 0 outside it. Hence exactly one face interior covers
each point inside the triangle outside S, and none covers a point outside it.

Two overlapping face interiors would have an open intersection containing
a point outside S, contradicting that count. A face interior extending
outside the closed target would likewise contain such a point outside the
target. The finite union of closed face images is closed, so its coverage of
the dense set of target points outside S gives coverage of the whole target.
This is exactly a tiling without overlaps. QED.

One can strengthen the conclusion to a homeomorphism. Across an interior
atom the consistent face orientations place the incident faces on opposite
sides. Around an interior vertex the cyclic fan has positive angles and
can wind only a positive integer number of times; winding more than once
would give multiple nearby face-interior preimages. The degree count forces
one winding. A boundary vertex has the corresponding single boundary fan.
In particular, all the angle conditions in the preceding theorem follow
from passing the direct-development criterion.

An interior fan of total angle 4 pi can have identity rotational holonomy
and locally consistent developed coordinates. It still cannot pass the
complete criterion: nearby regular values would have at least two positive
preimages, contradicting the degree forced by the simple boundary. This is
why the boundary check replaces, rather than merely approximates, the angle
checks in this implementation.

### Exact rational coordinates for a fixed integer-sided tile

Put

    H = (a+b+c)(-a+b+c)(a-b+c)(a+b-c) > 0,
    q(x,y) = x^2 + H y^2.

Represent the Euclidean point (x, y sqrt(H)) by the rational pair (x,y).
For a face whose positively oriented side sequence is (s0,s1,s2), local
corner coordinates are

    P0 = (0,0),
    P1 = (s0,0),
    P2 = ((s0^2+s2^2-s1^2)/(2s0), 1/(2s0)).

These satisfy the three prescribed squared distances under q. Every side
mark has rational coordinates when its cumulative distance along the side
is rational, in particular when the seam-tree reconstruction gives integers.

Suppose an oriented local edge vector e=(ex,ey) is to map to E=(Ex,Ey) of
the same nonzero q-length. The unique orientation-preserving linear
isometry that does this is

    R = [[u, -H v], [v, u]],
    u = (Ex ex + H Ey ey) / q(e),
    v = (Ey ex - Ex ey) / q(e).

Both u and v are rational, and u^2 + H v^2 = 1. Add the translation matching
one endpoint. For a paired atom, its endpoints must be matched in the
reversed face-boundary order. Starting with one face, propagate across a
spanning tree of face adjacency and then check **all** remaining pairings
and **all** quotient vertex occurrences for exact coordinate agreement.
It is not enough to check only the spanning-tree contacts.

All calculations use rational arithmetic. With the common fixed factor
sqrt(H), the sign of a Euclidean cross product is the sign of the ordinary
rational determinant of the represented coordinate pairs.

### What the developed boundary check must include

The three designated target corners must develop to three distinct,
noncollinear points in positive cyclic order. Along each of the three
boundary chains, every developed vertex must lie on the corresponding
segment, and its scalar position must increase strictly from 0 to 1.
Checking only the three corner coordinates and their distances would omit
possible backtracking or an extra traversal.

Prescribed side lengths are checked by q on the three displacement vectors.
For targets with rational squared side lengths, this is rational arithmetic
as well. These explicit boundary checks, together with the disk, metric,
orientation, and consistency checks above, are sufficient; no evaluation of
angles or inverse trigonometric functions is then needed.

## What an exact checker must verify

* **Topology, not just Euler characteristic.** For the dart quotient, check
  connectedness, the interval/circle condition on every vertex link, a single
  boundary component, compatible orientation, and Euler characteristic 1.
  These give a compact oriented surface of genus zero with one boundary
  component. An angle inventory without these link and gluing checks is not
  a disk certificate.
* **Regularity of the claimed cells.** If the implementation uses the regular
  cell formulation, check that every closed face is embedded in the quotient.
  In particular, this concerns all of its marked atomic vertices, not only
  its three original triangle corners. The statement in the source already
  requires embedded closed faces; the shorter phrase about uncollapsed
  corners should not be used as a replacement for that requirement.
* **True angle sums, if using the local-angle formulation.** A product of
  algebraic rotation factors equal to 1
  proves the sum is a multiple of 2 pi, not that it equals 2 pi. For example,
  a fan of 12 equilateral-triangle corners has angle 4 pi and passes the
  product-only test. Such a cone is not a flat neighborhood and has positive
  local mapping multiplicity under development. Winding counts are essential.
  The complete direct-development criterion above is an alternative that
  avoids this angle check altogether.
* **All side sums and strict positivity.** A zero or negative recovered atom
  is not a Euclidean edge and cannot be admitted as a harmless degeneration.

For integer sides a, b, c, put

    H = (a+b+c)(-a+b+c)(a-b+c)(a+b-c) > 0.

The rotation for the angle opposite a is exactly

    ((b^2+c^2-a^2) + i sqrt(H)) / (2bc).

Thus all local products can be checked in an algebraic number field. After
an exact product check, a certified angular approximation distinguishes the
possible full turns: if the product is 1, the total angle divided by 2 pi is
already known to be an integer, so an error below 1/4 determines that integer.
The same procedure handles equality with pi or with a prescribed corner
angle. This avoids an undecidable-looking comparison of arbitrary real
offsets; no such offsets remain in a complete certificate.

## Scope retained

For a fixed tile with positive integer sides, integer side compositions and
finite dart pairings give a finite search. A fixed-N search over all possible
tiles additionally needs the independently proved bound on candidate tile
shapes and side lengths; realization alone does not supply that bound.

The source explicitly supplies such a reduction under its stated published
classification inputs. This audit does not reprove or strengthen that
reduction. Nor does it provide a bound independent of N, a fixed finite seed
set, or a uniform arithmetic membership criterion.

**Audit outcome:** the existing sufficiency proof has no unresolved
non-overlap gap. Its topological and angle hypotheses are substantive and
must not be replaced by marginal counts or the separate seam trees.
