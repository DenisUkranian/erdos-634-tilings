# No further tile fits in the 3423-unit packing

For the specified packing of 3423 copies of the (33,7,37) tile in the 3431 board, neither remaining vacancy contains a congruent tile. Translations are continuous, the orientation can be any real angle, and both handednesses are included. A larger packing would have to move or remove at least one of the retained tiles.

Each vacancy is contained in a convex pentagon of area 16 in tile units. Twelve retained unit tiles lie in the pentagon. Its hull and all twelve tiles are listed in [the local coordinates](remaining_region.txt) with common denominator 37 in the axial basis $1,\rho=e^{i\pi/3}$. Translate the entire local picture by $(-4662,6105)/37$ to reach the second vacancy. The [position verifier](check_boards.py) checks the hulls and obstacles, exact tile metrics and equality of oriented boundary chains for the entire packing plus the two residual regions and the target. The fixed layout also admits a direct explanation for why it cannot be completed within the same two pentagons even if all 12 units in each are relocated: each pentagon has a side of length one, shorter than every tile side.

### Continuous rotations

Parametrize a unit vector by $u(t)=(1-t^2,2t+t^2)/(1+t+t^2)$ in axial coordinates. For $0\le t\le1$ this runs continuously from direction zero to 60 degrees, with quadratic norm $x^2+xy+y^2=1$. Its six successive 60-degree rotations therefore cover the circle. In a direction $u$, the triangle's two handednesses are represented by $0,33u,(33+7\rho)u$ and $0,33u,(40-7\rho)u$.

Take any interval of width $1/d$ and its midpoint. Physical Euclidean speed along the unit circle is $|u'(t)|=\sqrt3/(1+t+t^2)$, using axial norm, so the physical angle changes by at most $\sqrt3/(2d)$ radians from the midpoint. The triangle's centroid has distance at least $r=ab\sqrt3/(6c)$ from every side: one third of the smallest altitude. All of its vertices are within distance $c$ of the centroid. Here $a=33,b=7,c=37$.

Shrink the midpoint triangle by the factor $1-18/d$ about its centroid. If a full tile at an angle in this interval fits, the shrunken midpoint triangle fits with strictly positive clearance after matching centroids. Indeed shrink the full tile around its centroid first, moving every side inwards by at least $18r/d$. Rotating this smaller triangle to the midpoint changes no point by more than $c\sqrt3/(2d)$. Since $18>3c^2/(ab)$, the inward margin strictly exceeds the motion. A small open set of translations of the smaller triangle thus fits as well.

### Continuous translations

For the shrunken triangle $T$ compute the entire convex polygon of translations $w$ with $w+T$ in the pentagon. For each outer halfplane apply its tightest translated inequality over the three vertices of $T$. A fixed obstacle $A$ meets $w+T$ exactly when $w\in A-T$, the convex hull of the nine pairwise vertex differences. Subtract all twelve such convex polygons from the allowed translation polygon by rational halfplane clipping. Boundary-only fragments are irrelevant since a full tile fitting at any actual angle implies an open set of translations for its smaller midpoint representative.

At denominator $d=64$, every one of the 64 angular intervals has zero remaining translation area for each of the six rotations and both handednesses. The [standalone checker](check_saturation.py) uses only standard Python rational arithmetic and [the local coordinate table](remaining_region.txt).

Run `python check_saturation.py` to check the continuous exclusion. Run `python check_boards.py` to match both local pictures to the complete packing. The saturation result describes this layout; existence of an unrestricted 3431 tiling remains open.
