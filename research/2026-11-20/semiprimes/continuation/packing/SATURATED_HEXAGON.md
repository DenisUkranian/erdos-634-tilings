# A two-tile-area hexagon admits no complete tile in any orientation

Use axial coordinates in the Euclidean basis $1,\rho=e^{i\pi/3}$. Let H have cyclic vertices
$$
 (0,0),\ (-19,0),\ (-19,-13),\ (16,-13),\ (16,-26),
 \ (1248/43,-910/43).
$$
Then H contains no isometric copy of the triangle with vertices $0,35,35+13\rho$. The statement allows arbitrary real rotation, translation and reflection, including contact with the boundary. Its sides are 13, 35 and 43. This certifies the geometric obstruction on the individual hole; other arrangements of tiles in the original 5063 triangle require separate consideration.

**Geometry of the hole.** Label the vertices 0 through 5. H is the intersection of its convex hull with the complement of the open quadrant $x<16$, $y<-13$. The hull in positive order is $(0,1,2,4,5)$; the reflex corner is vertex 3. In the discarded quadrant the closing chord 2–4 and the two coordinate rays through vertex 3 enclose exactly the triangular notch. Beyond vertices 2 and 4 these rays leave the hull. These assertions follow directly from the vertex coordinates or from the hull half-planes. The doubled axial shoelace area is 910, exactly twice the doubled axial tile area 455.

**A finite cover of all rotations.** For either hand use 6 sectors of angle $\pi/3$. Within a sector use the rotations
$$
 Z(t)=\frac{1+t\rho}{1+t\bar\rho}
     =\frac{1-t^2+(2t+t^2)\rho}{1+t+t^2},
     \qquad 0\le t\le1 .
$$
The argument increases from zero to $\pi/3$ and has derivative $\sqrt3/(1+t+t^2)\le\sqrt3$. Use the midpoints of 64 equal subintervals in t. Replacing any rotation by its midpoint, about the translated copy of the vertex 0, moves every point of the tile by at most $43\sqrt3/128$ in Euclidean norm. Each axial coordinate changes by at most $2/\sqrt3$ times that norm, hence by at most $43/64<1$. The same estimate applies after reflection and multiplication by any power of $\rho$. These rotations are solely an angular covering argument; a putative tile may have any orientation.

Suppose the exact placement fits. Its midpoint placement then lies in every expanded hull half-plane
$$
 n\cdot x\ \ge\ n\cdot h-(|n_x|+|n_y|),
$$
where h is a hull edge vertex and n is its inward normal as a *coordinate* covector. Also the midpoint triangle avoids the open shrunken quadrant $x<15$, $y<-14$. Indeed every point of the midpoint triangle has a corresponding point of the original triangle with both coordinate errors less than 1. A point in that shrunken quadrant would come from a point in the discarded quadrant.

**Testing every translation.** A compact triangle disjoint from the open lower-left quadrant at $r'=(15,-14)$ is separated from it by a line through $r'$ with some nonzero normal $m=(s,1-s)$, $0\le s\le1$, pointing into the upper-right quadrant. This follows by convex separation, since a normal taking a negative coefficient is unbounded above on the open quadrant. At a fixed translation the minimum of $m\cdot(v-r')$ over the three vertices is a piecewise-linear function of s. Its maximum is attained at an endpoint of $[0,1]$ or where two vertex values coincide. Thus it suffices to try the two coordinate covectors and every nonnegative normal perpendicular to a tile edge. This reduction includes boundary contacts and cases where a tile vertex alone touches the separator.

For each such m, every expanded hull covector n and m supply inequalities for the continuous translation vector d. Each requires $n\cdot d$ to exceed or equal the corresponding edge offset minus the least projection of a tile vertex. The hull inequalities make the feasible translation polygon bounded, so when nonempty it has a vertex at two nonparallel boundary lines, including degenerate line-segment and point cases. The verifier checks every such intersection against all inequalities by integer cross multiplication. Axial coordinates are multiplied by 43 times the rotation denominator. No tolerance enters the replay.

Run direct with standard Python 3:

```sh
python3 verify_free_angle.py
```

The 768 enclosures (two hands times six sectors times 64 subintervals) yield 3,072 bounded half-plane systems. All are infeasible after the stated enlargement. Therefore no original placement fits.

A second implementation, `python3 replay_clipping.py`, uses rational polygon clipping and 48 intervals per sector. The axial displacement bound is then $43/48<1$. It checks 576 different midpoint orientations and 2,304 infeasible translation systems using exact fractions. The bounding box used to initialize clipping contains the expanded hull, as checked by its vertices.
