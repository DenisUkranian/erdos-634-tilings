# A positive fan reduction for all ordered F3 ratios

This is a positive geometric partition and an obstruction to its simplest
filler. It does not prove that an F3 target can or cannot be tiled. In
particular, it does not decide 4830 or the unbounded-ratio F3 front.

Let `a>b>0`, `c²=a²+ab+b²`, `rho=exp(i*pi/3)`, and
`z=(a+b*rho)/c`. The canonical ordered F3 triangle is

    X=0, Y=c², K=c(a+2b)z³.

## 1. Three c-fold tile triangles always fit

Set

    R0=Y, R1=ac z, R2=c²z², R3=ac z³.

For j=0,1,2, the triangle `[X,Rj,R(j+1)]` is a c-fold copy of the
original tile. Their interiors are disjoint: they occupy the successive
angular sectors `[0,beta]`, `[beta,2beta]`, `[2beta,3beta]`, where
`beta=arg z` lies strictly between 0 and pi/6. The endpoint lengths at X
alternate c² and ac, and every opposite side has length bc.

Unlike the earlier three-grid gamma partition, this fan is contained for
**every** ratio a/b>1. Here is a short containment proof. Apply the
isometry `w -> z^-2 w - a²`, put `A=ab`, `B=b²`, and use Eisenstein
coordinates x+y*rho. The relevant points become

    X=(-a²,0),   Y=(2A,-2A-B),   K=(2A,A+2B),
    R1=(A,-A),  R2=(A+B,0),    R3=(0,A).

The supporting line YK is x=2A. All radial vertices are in its X-side
half-plane, since 0<B<A. They are also in the angular wedge XK, XY by
the successive-sector observation. Those three half-planes define the
convex target triangle, proving containment. For an entirely algebraic
check, write `S=c²`, `h=a+2b`, `ell=2a+b`. The three inward
cross-product tests for a point p are

    d1=det(Y-X,p-X), d2=det(K-Y,p-Y), d3=det(X-K,p-K).

For the successive radial vertices their values are

| p | d1 | d2 | d3 |
| --- | --- | --- | --- |
| R1 | abS | 3ab²(a+b) | ab*h*ell |
| R2 | b*ell*S | 3b²(a+b)(a-b) | b*h*S |
| R3 | 3a²b(a+b) | 6ab²(a+b) | 0 |

All are nonnegative for a>b>0. The determinant is in Eisenstein
coordinates; the common physical factor sqrt(3)/2 is positive.
Ordinary integer-scale
subdivision fills the three sectors with 3c² unit tiles.

Their complement is the nonconvex pentagon `[Y,R1,R2,R3,K]`. Its sides
have lengths bc,bc,bc,2bc,3b(a+b), and its normalized tile area is

    3(a+b)(a+2b)-3c² = 3b(2a+b).

## 2. Four more triangular grids leave an axis hexagon

In the isometric coordinates above define

    E0=(2A,-2A), E1=(A+B,-A), E2=(B,A), V=(2A,A).

Remove the four triangles

    [Y,R1,E0], [R1,R2,E1], [R2,R3,E2], [R3,K,V].

The first three have sides A,B,bc, hence are b-fold copies of the tile.
The fourth has sides 2A,2B,2bc and is a 2b-fold copy. Each has included
angle 120 degrees between its displayed short sides. All have the same
short-edge direction class in these isometric coordinates.

This is a positive partition. The first three lie respectively in the
closed y-strips [-2A-B,-A], [-A,0], [0,A]; the fourth lies in
[A,A+2B]. Their interiors are disjoint. The endpoint conditions B<A and
B<2A give the intended boundary order. Their exact union with the
hexagon below is the pentagon above; shared edges R3E2 and R3V are split
at E2, so the partition explicitly allows its T-junction.

The leftover hexagon is

    H(A,B)=[(2A,-2A), (A,-A), (A+B,-A),
            (A+B,0), (B,A), (2A,A)].

It is simple for 0<B<A. More explicitly, away from its horizontal
edges its horizontal cross-sections are precisely

    -2A<y<-A:  -y <= x <= 2A;
     -A<y<0:   A+B <= x <= 2A;
       0<y<A:  A+B-y <= x <= 2A.

Each interval has positive length. These sections also prove directly
that the four triangles and H fill the pentagon with no gaps or
interior overlap. The coordinate area of H is `3A²-2AB`, and its
normalized tile count is

    3b(2a+b)-3b²-(2b)² = 2b(3a-2b).

Consequently, **a filling of H(ab,b²) by the original tile in arbitrary
orientations is sufficient for the corresponding F3 target at multiplier
one**. Scaling everything gives the analogous multiplier-m reduction.
No converse is asserted: an arbitrary F3 tiling need not contain this fan.

## 3. The tempting parallelogram filler is impossible

The six directed boundary vectors of H are

    A rho², B, A rho, A rho², 2A-B, -3A rho.

Resolve length into the three unoriented short-axis classes, choosing
positive directions 1,rho,rho². The signed boundary-length vector is

    (2A,-2A,2A),

which is nonzero. Every parallelogram, including every a-by-b two-tile
parallelogram in these axis directions, has zero signed boundary-length
in each direction. Internal boundaries cancel, even with arbitrary
T-junctions. Therefore H cannot be tiled by any collection of those
parallelograms.

The simpler a-periodic Fourier integrals do vanish: this is why passing
those tests does not justify a parallelogram filling. The directionwise
boundary current is the missing obstruction. The separate
[short-height argument](../pentagon/SHORT_HEIGHT_OBSTRUCTION.md) excludes
even arbitrary original-tile fillings confined to this one short-edge
class. A successful filler must use additional short-edge orientation
classes, or one must abandon this particular sufficient decomposition.

There is a second limitation on a simple filler. In these coordinates
H has x-coordinate range `2A-B<2A`. Every equilateral triangle of side
2A whose sides belong to the three current short-axis directions has
x-coordinate range 2A in this same oblique coordinate system. Thus no
such triangle can be placed inside H.
In particular H cannot be partitioned into one axis-aligned equilateral
triangle of side 2ab and any collection of parallelograms. This statement
does not exclude differently oriented equilateral pieces or mixed-height
original-tile fillings.

This reduction improves the positivity domain of the three-c-grid
partition but leaves a geometric filling problem. It is not a complete
classification, and no new positive count is claimed here.
