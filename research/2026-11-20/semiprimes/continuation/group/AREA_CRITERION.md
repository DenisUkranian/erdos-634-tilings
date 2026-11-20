# Full tiling as an exact minimum-area problem in the edge presentation

Let the primitive tile have sides a,b,c and area T, with a,b,c positive integers, gcd(a,b)=1 and c²=a²+ab+b². Use the edge presentation and the group G from the [universal boundary identity](DIRECTION_GROUP.md). Its unit-step generators carry their actual plane displacements. Its relators are the subdivided boundaries of the two hands of the triangle at the admitted headings. A single use of a tile relator or its inverse counts as one face. In the convention with opposite headings as inverse generators there is no separate face for reversal.

Let W be the counterclockwise boundary word of a simple F2 board of area NT. Write A(W) for the least number of tile faces in any van Kampen disc diagram with boundary word W. In this family it is finite by the universal identity. Then

$$A(W)=N+2\min_D q(D),$$

where q(D) counts the faces whose oriented geometric image is clockwise. In particular the board tiles by N congruent copies, with arbitrary rotations, reflections and T-junctions, **if and only if** A(W)=N. Proving A(W)≥N+2 for either board would give a whole-board obstruction. This last inequality has not been proved for either numerical case.

## Proof

The displacement sum of each relator is zero. Fix the position of one vertex of a diagram. Assign to every other vertex the sum of the displacements along a path from this basepoint. Relator closure and simple connectedness give path independence. Extend each edge by its unit line segment. The boundary of every face now traverses a translated unit tile once, in one of its admitted orientations and with one of its two signs. This uses neither planarity of the geometric image nor containment of the images in the board. The combinatorial diagram itself is planar.

Sum the geometric boundaries with the orientations induced from the diagram. Every internal edge cancels, including any edge subdivision. A spur has two cancelling traversals. Only the board boundary remains. The signed area formula therefore gives (p−q)T=NT, where p and q count positive and negative faces. Thus the number of faces p+q is N+2q in each diagram, proving the displayed formula.

If a diagram has exactly N faces, all the face images are positive triangles. For any point off their edges and the board boundary, add the winding numbers of their boundaries about that point. The result is one for a point in the board's interior and zero for a point in its exterior. This winding number is precisely the number of tile interiors containing the point. It follows that no two tile interiors overlap and no tile extends outside the closed board. Since a finite union of closed tiles is closed, the interiors' generic coverage also covers all the remaining boundary and edge points. These rigid placements give a complete geometric tiling.

Conversely take any tiling by the specified congruent triangle. Its directions propagate across parallel contacts and are among the headings of the presentation. Along a maximal straight chain of edges the two banks consist of whole tile sides measured from a common endpoint; both banks therefore have vertices at integral offsets there. The exterior has the same integral subdivision. Insert all unit subdivisions, so each unit edge of the interior cell decomposition is shared with the opposite orientation. Every two-cell is a subdivided unit tile. The disk gives a diagram for W with exactly N tile faces. This proves the criterion.

## The two words

Write x(h,j) for a unit step of heading z^h rho^j, with a,b respectively 33,7 or 35,13. The two words in their respective presentations are

* 3431: `x(0,0)^511 x(2,1)^1369 x(0,1)^(-1551)`.
* 5063: `x(0,0)^1079 x(2,1)^1849 x(0,1)^(-2135)`.

The word problem alone gives the identity for both. The remaining problem concerns the minimum number of tile relators in a filling. A candidate equality still needs an explicit diagram or independent argument; the geometric reconstruction above gives exact coordinates from a diagram, including any partial-edge contacts. This criterion concerns the scale-one board. Using it for a negative answer to the original existential question additionally requires the project's classification reduction.

## Explicit finite intervals

The existing two-notch constructions give actual abstract disc diagrams, including when their faces overlap after being mapped to the plane. For a notch XYWD the staircase supplies a standard gridded triangle XYZ and a smaller triangle ZWD with reversed sign. W lies strictly between Y and Z, and D strictly between X and Z. Glue the two grid disks along the single proper arc W–Z–D, with agreeing unit subdivisions. The glued complex is a disk with boundary XYWD. Substitute these disks for the two notches in the existing dissection of the board. All other cells use positive standard grids. This explains why the signed count gives a diagram upper bound; an arbitrary formal cancellation of polygon boundaries alone would not establish disk topology.

| Board | Positive faces | Negative faces | Range for A(W), in steps of two |
|---:|---:|---:|---:|
| 3431 | 3506 | 75 | 3431 to 3581 |
| 5063 | 5071 | 8 | 5063 to 5079 |

The newer 3431 construction extends by five parallel grid parallelograms outside the board and glues their reversed disc along a three-side arc. The two notches contribute 1 and 64 negative faces. Removing the padding contributes ten more. The [disc checker and construction](diagram-bounds/README.md) verify both rows. Run `python3 diagram-bounds/verify.py` from this directory. The older `verify_area_bound.py` still reproduces the unpadded 128-negative-face bound at 3431 and the same eight-negative-face bound at 5063. Neither construction determines optimality.
