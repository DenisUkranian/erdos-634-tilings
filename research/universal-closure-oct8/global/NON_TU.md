# Complete positioned-current matrices are not totally unimodular

8 October 2026. A universal obstruction to one proposed shortcut, not a
counterexample to a tiling-existence equivalence for triangular targets.

**Theorem.** For every primitive integral 120-degree tile with positive
short sides a,b and long side c, the complete positioned-current matrix
on the exact three-height lattice has an atomic-edge submatrix with
absolute determinant two, provided the target contains the three placements
below. This applies in particular to sufficiently large equilateral targets.

Put rho=exp(i*pi/3), u=a, v=b*rho^2, and
T=conv(0,u,v), oriented counterclockwise. The exact band lattice for heights
[-1,1] is c^(-1) Z[rho], by the established coprime Eisenstein factorization.
The three allowed placements are

    T0=T,  T1=T+u/c,  T2=T+v/c.

All have short height zero. Since 0<1/c<1, the following pairs share a
positive-length collinear side interval:

* T0,T1 share part of their u-directed sides;
* T0,T2 share part of their v-directed sides;
* T1,T2 share part of their (v-u)-directed sides.

In each case the third triangle has its parallel side on a different line.
Choose one atomic segment in each common interval. Its two incident columns
have equal signs, since these are translations of one oriented triangle.
Reorienting rows if necessary gives the minor

    [ 1  1  0 ]
    [ 1  0  1 ]
    [ 0 -1 -1 ],       determinant = 2.

Every shared interval contains an atomic segment: all its endpoints lie in
the exact lattice and consecutive lattice points subdivide the edge. Thus
this is a minor of the actual positioned atomic-edge matrix, not a matrix
of merely directional totals or a minor created by endpoint differentiation.
A larger dictionary does not alter these three selected column entries.

For a concrete instance use denominator7 and tile(3,5,7). The three CCW
triangles, all contained in the equilateral target of side30, are

    T0: (70,70), (91,70), (35,105)
    T1: (73,70), (94,70), (38,105)
    T2: (65,75), (86,75), (30,110).

The rows, oriented by the listed endpoints, are

    (80,70)->(81,70),
    (60,80)->(61,79),
    (62,90)->(70,85).

Dividing every coordinate by7 gives physical Eisenstein coordinates.
`check_non_tu.py` verifies congruence, exact lattice membership, containment,
all nine signed incidences, and the determinant using integer arithmetic.
The same witness is contained in the side45 and side60 targets.

## Exact logical scope

This rules out total unimodularity as a universal reason that the complete
current relaxation should be integral. It does **not** prove that the special
polytope Bx=b_P for a triangular target has a fractional vertex, or that an
untileable target admits a positive fractional filling. A non-TU matrix may
still have an integral feasible polytope for a particular right-hand side.
Indeed the side30 instance used here is already known to have no nonnegative
current solution in its complete allowed bands.

The three-row relaxation with right-hand side (1,1,-1) has the unique solution
(1/2,1/2,1/2). The other geometric boundary rows cannot simply be discarded:
they prevent this observation from being advertised as a fractional tiling.
The remaining possible universal theorem would have to use the special
complete triangular boundary and geometry, beyond total unimodularity.
