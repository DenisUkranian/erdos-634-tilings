# Boundary and corner foundations: an explicit proof audit

10 October 2026. Research for Denis Paliy, with ChatGPT assistance.
This is a reconstruction of specified existing project lemmas, not a claim of
first discovery, an independent human referee report, or formal verification.
The earlier sources are preserved in `inputs` and identified below. The local
lemmas here do not resolve the disputed reverse-apex induction.

## 1. Model and a distinction that cannot be suppressed

A tiling is a finite collection of congruent closed nondegenerate triangles
with disjoint interiors and union a closed triangular target. Reflection and
T-junctions are allowed. A supported edge is an ENTIRE tile side lying on an
outer side. A tile touching the outer side only at its vertex is not supported
by that side. A boundary atom can be shorter than any tile side.

These are different objects: an outer side, a maximal collinear component of
the full skeleton, an arbitrarily selected subsegment of such a component,
and a boundary atom of a partially filled target.

## 2. Whole edges on a convex exterior; finite boundary dictionary

Let L support the convex target. At every nonvertex boundary point, a tile
containing that point has a side on L: a tile interior would cross outside,
and a noncollinear tile side cannot contain an interval of the boundary.
Finitely many exceptional vertices do not leave a gap. A supported tile side
cannot extend outside the target, by containment. On the interior half-plane,
two such sides cannot overlap in a positive-length interval, since their tiles
would then overlap on an open set. Therefore whole tile sides partition the
outer side, including its endpoints.

If tile lengths are integral, every supported side begins at integral arclength
from an outer vertex. For an outer length H, the complete boundary dictionary
is consequently obtained by trying every integer start position 0,...,H-1,
every tile side length, and its two orientations. The cosine rule fixes the
third vertex on the interior side. Retain all contained triangles with allowed
corner-angle inventories. This is a FINITE DICTIONARY ON THE EXTERIOR ONLY;
it imposes no lattice or direction band on interior vertices.

## 3. Complete banks: where endpoint justification is indispensable

For a maximal connected collinear component S of the FULL skeleton on an
internal line, whole edges partition S on both sides. At a point other than
one of the finitely many tile vertices, an existing side has a tile opposite
it; that tile cannot cross it, and hence has a collinear side. Maximality
prevents any constituent side from overhanging an endpoint of S. Convexity of
the target ensures that this internal component does not switch to exterior
boundary partway along its supporting line. Thus both banks really are whole.

The same inference for a proper subsegment is invalid without new endpoint
information. For example, select a length-one interval strictly inside a
length-four side in a genuine (2,3,4)-tiling. The interval is covered by part
of that edge, not by a nonnegative combination of whole tile sides. Its length
being below the shortest tile side is not a contradiction.

Two standard sufficient endpoint justifications are an exterior supporting
line that forbids overrun, and an actual tile occupying the continuation past
the endpoint. A statement that a future row WOULD provide a cap cannot serve
as such a justification. Applying a short-chain arithmetic lemma first and
then using its conclusion to supply the endpoints would be circular.

## 4. Why the convex-corner branching has six possibilities

Take a valid partial placement. Suppose consecutive oriented residual boundary
rays at X enclose an unfilled sector of angle omega with 0<omega<pi. A completion
must place tile vertices at X: an interior point of a tile would occupy 2pi,
and an interior point of a tile side would occupy pi, neither fitting the
sector. Among the tiles at X choose the one adjacent to the outgoing residual
ray. It has a whole side on that ray, starting at X.

For a scalene tile there are six ordered choices (s,r) for that side and the
other incident side; the remaining length t is then determined. If e is a
unit vector on the ray, the third vertex is

    X + ((s^2+r^2-t^2)/(2s)) e + H e_perp,
    H^2 = r^2 - ((s^2+r^2-t^2)/(2s))^2,

on the sector side. Test the sector, target containment and interior-disjointness
from the partial placement. EVERY actual completion's chosen tile survives.
An empty list is a contradiction. A proof tree must include every surviving
choice, with all children refuted. Induction on a finite tree then refutes its
root. The choice of a convenient corner is not a completeness restriction.

The whole side is NOT required to end at the endpoint of the currently
visible boundary atom. Overrun is allowed unless it creates an actual overlap
or leaves the target. The new positive-control tests explicitly found 18
occurrences where a known completing side is longer than the atom. Deleting
such sides from the candidate list loses valid completions.

This argument justifies the local branching rule. A global statement that all
geometries have been excluded additionally requires the exhaustive
classification, normalization, root enumeration and a fully checked tree.

## 5. The blocked-c lemma, with the hypotheses used in this audit

Here c is the longest tile side, gamma its opposite angle, gamma>pi/2, and
alpha,beta are opposite a,b. Assume a,b>1, gcd(a,b)=1, c>a,b. We apply the
following argument ONLY to the documented W/beta targets, and to the primitive
120-degree equilateral case in the class-14 proof. In these cases:

* no target corner contains a gamma tile angle;
* a target corner is never a single alpha angle;
* a blocked beta endpoint not itself a single-beta corner leaves exactly one
  alpha tile immediately opposite the original a-side.

For W/beta these facts follow by writing beta=(pi-3alpha)/2,
gamma=(pi+alpha)/2 and equating coefficients of irrational alpha/pi.
A flat fan is (alpha,beta,gamma) or (3alpha,2beta,0 gamma). At the relevant
120-degree equilateral corner the fan is alpha+beta; at a marked flat beta
endpoint, beta+gamma leaves alpha. These facts do NOT hold for arbitrary
triangular targets; no automatic transfer to the other branches is made.

Mark a junction when a SUPPORTED a- or b-edge contributes gamma there. The
marks are distinct because 2gamma>pi. Target corners and these marks are
called blocked. Consider a supported c-edge PQ with alpha at P, beta at Q,
and third vertex R of angle gamma. Its sides PR=b and QR=a.

If Q is a single-beta target corner, QR is external and R is on the boundary.
Otherwise the inventory at blocked Q leaves an alpha tile across QR. Its side
starting at Q along QR has length b or c. If this overhangs R there is an edge
crossing R. If no edge crossed R, the complete opposite bank of QR would have
length a and begin with b; c or a could not fit after that positive contribution.
It would consist entirely of b, forcing b|a, impossible. This bank is complete
along an intact tile edge, with its first endpoint capped by convexity.
Thus R is external or is internal to a crossing edge. In both cases another
gamma angle at R is impossible (2gamma>pi or pi+2gamma>2pi).

The chord PR cannot itself be external: together with PQ that would produce
a target alpha corner, excluded above. Its opposite bank has length b and
both ends are capped, at P by the exterior and at R by the boundary or crossing
tile. No c fits; one b would occupy the entire chord and put gamma at P or R,
which is forbidden. The bank must be all a, forcing a|b, again impossible.
Hence a supported c-edge cannot have two blocked endpoints.

If an outer side has n supported edges, k of them c, then its n-k other edges
supply n-k distinct marked internal junctions. There are k-1 unmarked internal
junctions. Every c-edge needs an unmarked endpoint, so two of the k c-edges
must share one of those k-1 junctions. They are consecutive. This also proves
that k cannot be 0 or 1.

### A tempting but false strengthening, now backed by a full positive witness

Marking EVERY gamma vertex touching the boundary is wrong. The attached
`wrong_mark_counterexample.json` is a fully checked W28 tiling by (2,3,4).
One of its c-edges has one target-corner endpoint and one endpoint where a
third tile merely touches at gamma. Both would be blocked by the wrong rule,
although the c-edge occurs in a genuine tiling. Under the correct supported
rule only the first endpoint is blocked. Across the five controls we found
85 actual c-edges rejected by this false strengthening. This is not an error
found in the existing checker: the inspected checker uses the correct rule.

## 6. Boundary-path pruning and what it does not prove

For each exterior side, supported candidates are directed edges in an
arclength graph from 0 to H. Discard candidates overlapping already placed
tiles, except the identical tile itself. A completion induces a path satisfying
corner inventories, no two supported gamma endpoints at a junction, the
blocked-c prohibition and a consecutive pair c,c. Therefore no admissible path
on even ONE side rules out that partial placement.

Conversely, paths on the three sides need not be mutually compatible; their
future tiles can overlap, and the interior can remain impossible. Passing the
path test is only a necessary condition. Ignoring extra incompatibilities
weakens pruning but does not invalidate a negative leaf that already has no
path. A timeout is never such a leaf.

The new implementation tests rebuild 4,564 dictionary entries by a separate
cosine-rule and rational-clipping enumeration. For 24 banned-dictionary trials,
a brute-force complete-word oracle examined 68,824 words and agreed with the
existing finite-state path algorithm. This checks these implementations on
the stated finite data, not every possible dictionary by extrapolation.

## 7. Positive boundary currents versus aggregate signatures

Suppose all pieces are positively oriented simple polygons and the positioned
sum of their oriented edge currents is exactly the target current. Subtract
the target indicator from the sum of piece indicators. This compactly supported
piecewise constant function has zero jump across every open edge interval.
It is zero outside, so is zero in every face of the finite arrangement.
Positive coefficients imply multiplicity one inside and zero outside. Finite
closed pieces also cover the boundary. Thus there are no gaps or overlaps.

This requires cancellation ON THE SAME SUPPORTING LINE AND AT THE SAME
POSITIONS. Matching just directionwise totals, area or a few moments is weaker.
Allowing negative coefficients would also destroy the nonoverlap conclusion.
Our second macro checker bypasses this theorem entirely, using exact convex
clipping, containment and summed positive areas as an additional audit path.

## 8. Evidence limits and dependencies

The original blocked-c statement is
`research/w-global-oct7/ADJACENT_C_EDGES.md` at repository commit
`3a0ad269f645850ed9fd01bbd76a08c9b456032e` (blob
`6f51f92699e6c38114a646fb5cdcc8a276d4c7b6`). The equilateral extension and
corner certificate rules are in `inputs/Erdos634_class14_complete_PROOF_2026-10-09.md`.
This audit supplies an expanded reasoning record plus reproducible tests. It
is not a formal proof-assistant checking of the universal lemmas, nor a fresh
replay of the full 29,600-node negative forest (that was Phase 1).
