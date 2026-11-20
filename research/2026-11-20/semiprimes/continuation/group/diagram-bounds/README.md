# Upper bounds on the number of negative faces

For the plane-wide unit-direction presentation, let $A(W)$ be the minimum number of faces in a van Kampen disc for the F2 boundary word. The two-step staircase gives the following bounds.

| Board area in unit tiles | Positive faces | Negative faces | Upper bound on $A(W)$ |
|---:|---:|---:|---:|
| 3431 | 3559 | 128 | 3687 |
| 5063 | 5071 | 8 | 5079 |

The [project staircase constructor](notchshape.py) partitions each board into seventeen convex blocks. Fifteen are triangles or parallelograms with the specified ordinary triangular grids. The other two blocks are congruent quadrilaterals. Write $X,Y,W,D$ for the successive vertices of either quadrilateral in the orientation returned by the constructor. A point $Z$ on the extensions of $YW$ and $XD$ makes $XYZ$ a tile-shaped triangle of scale $t$ and $ZWD$ a tile-shaped triangle of scale $k$. The vertices occur in the orders $Y,W,Z$ and $X,D,Z$. The two boards have $(t,k)=(13,8)$ and $(11,2)$ respectively.

Take a positively oriented abstract copy of the grid in $XYZ$ and a negatively oriented abstract copy of the grid in $ZWD$. There are $t^2$ positive and $k^2$ negative faces. Glue their boundary copies of the arc $WZD$ to each other using matching physical points. These are two discs glued on a single proper boundary arc, so the result is a disc with boundary $XYWD$. Its boundary maps homeomorphically onto the quadrilateral boundary. Its interior can fold. Subdivision into unit steps makes the edge words agree along the whole glued arc because both side lengths and the offsets of $W,D$ on the larger sides are integral.

Use a copy of this disc for each of the two quadrilaterals in the seventeen-block subdivision. Fill each remaining block by its ordinary grid. Subdivide the block edges at all unit offsets and glue along the interfaces of the planar block subdivision. The abstract result is a disc with the original board boundary. This supplies the displayed diagram bounds, including its topology in addition to signed area cancellation. A geometric tiling of the full board would give zero negative faces.

Run `python3 verify.py` with Python 3.8 or later. The standard-library [checker](verify.py) verifies the exact macro coordinates, interior disjointness and area of the convex partition, the two boundary arcs, every grid shape and scale, interface integrality at block vertices, and the final face counts. The constructor is the project copy used for the 3427 and 5059 reference packings.
