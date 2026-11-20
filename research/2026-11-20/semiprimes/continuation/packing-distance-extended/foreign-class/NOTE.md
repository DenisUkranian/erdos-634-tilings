# A 90-placement lower bound on the 5063 board

The reference file contains the specified 5059 triangles of the F2 board with tile lengths 35, 13, 43. Every full tiling omits at least 86 reference placements and contains at least 90 new placements. A placement includes all three physical vertices.

The previously certified two-class calculation in `unit_boards_packing_replay.zip` already gives at least 90 new placements when every tile belongs to either distinguished class. Write R for the Eisenstein lattice, z=(35+13ρ)/43, H=1079. These classes have short height 0 and vertices in R, or short height 1 and vertices in H+zR. All reference tiles belong to the distinguished classes. The same package proves an unrestricted lower bound of 86 new placements. The argument below strengthens its remaining cases.

Assume 86 through 89 new placements. There are 82 through 85 omissions. The whole-board population theorem says every occupied short height outside {0,1} has at least 86 tiles. Choose such a height h and call all tiles at h the selected group. If all heights belong to {0,1} but a foreign translate occurs, the extreme-translate theorem gives a foreign translate of some native height h with at least 86 tiles. Call those tiles the selected group. In either case, every member of the group is new and at most three new placements lie outside the group. The population and translate statements are applied as in the independent upstream two-class package, which contains their proofs.

Use an endpoint row identified by an exact point, a line height k and one undirected axis j modulo 3. Count a counterclockwise edge by +1 at its start and −1 at its end. Orient the board counterclockwise. Summing rows of tiles exactly reproduces the board rows even with partial edge contacts. The selected group cannot touch rows of heights outside {h−1,h,h+1}. If h is 0 or 1 it also cannot touch rows at points in the native translate for h. The 8499 rows of the board and the reference tiles have k in {−1,0,1,2}. Four relaxations suffice. For h≤−1 keep rows of heights 1 and 2, and for h≥2 keep heights −1 and 0. At h=0 and h=1 keep the rows guaranteed untouched by the height or the point test.

On retained rows, write E_i for the signed endpoint column of the i-th reference triangle, D_j for the endpoint column of a nonreference triangle, and b for all reference columns summed, less the board column. Set y_i=1 for an omitted reference and x_j=1 for a new placement outside the selected group. Then
```
sum(E_i y_i) − sum(D_j x_j) = b
82 ≤ sum(y_i) ≤ 85.
```
A candidate whose endpoints touch no weighted row can be left out, giving a lower bound on the number of new placements outside the group.

The JSON contains signed integer row weights w, two nonpositive integer count weights u,v, and scale S=1000000. The exact lower bound numerator on S times the number of additional placements outside the group is
```
w·b + 85u − 82v
 + sum_i min(0, −w·E_i −u +v)
 + sum_j min(0, S+w·D_j).
```
This follows by expanding the equality and count inequalities and minimizing each remaining term over its own interval [0,1]. Thus a certificate works equally well for the continuous relaxation.

The checker verifies directly which rows the selected group cannot touch. It reconstructs every candidate placement contributing to the last sum from a weighted vertex, either orientation of the specified line, the six ordered side assignments, and the two choices of half-plane. It verifies the third side length precisely, discards vertices outside the convex board, and removes reference placements and duplicates. Each construction uses integer axial coordinates with denominator 43^6. These coordinates serve only to represent the triangles determined by a weighted point and direction, and impose no restriction on the coordinates of an arbitrary completed tiling.

Run `python check_three_exceptions.py` from any directory. Each of the four lower bound numerators exceeds 3000000. Therefore a fourth new placement outside the selected group is necessary, contradicting the assumed maximum of three. Together with the two-class calculation this proves the stated unrestricted distance. Existence of a full 5063 tiling is still undecided by this bound.
