# Upper bounds on the number of negative faces

For the plane-wide unit-direction presentation, let $A(W)$ be the minimum number of faces in a van Kampen disc for the F2 boundary word. Two staircase constructions give the following bounds.

| Board area in unit tiles | Positive faces | Negative faces | Upper bound on $A(W)$ |
|---:|---:|---:|---:|
| 3431 | 3506 | 75 | 3581 |
| 5063 | 5071 | 8 | 5079 |

The [staircase constructor](notchshape.py) produces triangles, parallelograms and two convex quadrilaterals. Each triangular or parallelogram block has the indicated ordinary grid. The quadrilaterals use the following folded discs.

Write $X,Y,W,D$ for the successive vertices of a quadrilateral in the orientation returned by the constructor. A point $Z$ on the extensions of $YW$ and $XD$ makes $XYZ$ a tile-shaped triangle of scale $t$ and $ZWD$ a tile-shaped triangle of scale $k$. The vertices occur in the orders $Y,W,Z$ and $X,D,Z$.

Take a positively oriented abstract copy of the grid in $XYZ$ and a negatively oriented abstract copy of the grid in $ZWD$. There are $t^2$ positive and $k^2$ negative faces. Glue their boundary copies of the arc $WZD$ using matching physical points. These are two discs glued on one proper boundary arc. The resulting disc has boundary $XYWD$, mapping homeomorphically onto the quadrilateral boundary. Its interior can fold. Subdivision into unit steps makes the edge words agree along the glued arc because the side lengths and the offsets of $W,D$ on the larger sides are integral.

At 5063 take initial depth one and the loads $(15,4,1),(15,4,1)$. The seventeen blocks partition the whole board. Its two quadrilaterals both have $(t,k)=(11,2)$, giving $2^2+2^2=8$ negative faces.

At 3431 take initial depth two and the loads $(8,2,1),(15,2,1)$. In the axial frame with board vertices $(0,0),(511,0),(0,1551)$, this staircase extends outside the left side by the rectangle $P=[-7,0]\times[0,165]$. The sixteen convex blocks partition the board together with $P$. This is verified by exact boundary-chain equality and disjoint interiors. Their two quadrilaterals have $(t,k)=(13,1)$ and $(13,8)$, giving $1+64$ negative faces. The padding rectangle consists of five axial $7$-by-$33$ parallelograms. Each splits along its length-$37$ diagonal into two tiles. Glue a negatively oriented copy of this ten-tile rectangle to the filled union along the three-side exterior arc from $(0,0)$ through $(-7,0)$ and $(-7,165)$ to $(0,165)$. This is another gluing of two discs on one proper boundary arc. The exposed side restores the original board boundary and gives $1+64+10=75$ negative faces.

In each construction the block discs glue along the interfaces of the planar block subdivision. All block vertices on another side have integral physical offsets, so the unit subdivisions agree. The construction supplies the displayed upper bounds on diagram area, including the topology. A tiling of the full board would give zero negative faces.

Run `python3 verify.py` with Python 3.8 or later. The standard-library [checker](verify.py) verifies the exact block coordinates, pairwise interior disjointness, coverage of the stated region, the two notch arcs, every grid shape and scale, interface integrality at block vertices, and the final face counts. The generator is the constructor used for the reference packings, with an option to permit the 3431 padding.
