# Exact capacity with one reflex corner

The problem here is geometric packing. Inside the scale-one F2 board,
place a simple polygon on any triangular grid of mesh $c$, allowing
arbitrary rotations and translations. Opposite directions must have
equal total lengths, as they do on a supported cycle. Maximize the
number $K$ of upward grid cells subject to at most one reflex corner.
The polygon then consists of $2K$ cells. The exact maxima are **193**
for $(33,7,37)$ and **432** for $(35,13,43)$. Supporting an actual
tiled region requires $K=231$ and $455$, respectively.

## Exhaustive parameterization

Work in grid units with axial basis $1,\rho$. Merge collinear runs and
traverse the boundary counterclockwise. A single reflex turn is either
$-60^\circ$ or $-120^\circ$. Start at that corner with the outgoing
direction numbered 0. Every remaining turn is $+60^\circ$ or $+120^\circ$.
If the reflex turn is $-60t$ degrees, $t=1,2$, the successive directions
are a subsequence of $0,1,\ldots,6+t$ modulo 6, starting and ending at
the two displayed extremes. A skipped direction has length zero.
Opposite-direction balance gives the following complete run lists.

| $t$ | Runs in order | $K$ from shoelace |
|---:|---|---|
| 1 | $x,y,C,A,B,C,A-x,B-y$ | $AB+AC+BC-x(B-y)$ |
| 2 | $x,y,z,A,B,C,A-x,B-y,C-z$ | $AB+AC+BC-x(B-y)-(x+y)(C-z)$ |

Here $A,B,C$ denote run totals only. The unsplit opposite runs give
$1\le A\le L$, $0\le B,C\le L$ with $L=\lfloor ap/c\rfloor$,
since $ap$ is the board diameter. Use $1\le x\le A$, $0\le y\le B$
and, in the second row, $0\le z<C$. In the first row $y<B$ since the
last run is positive. Keeping further zero runs can admit invalid shapes;
the enumeration is an upper bound even with these extra candidates. It
includes both mirror images by counterclockwise traversal starting at
the unique reflex corner. The program also checks closure and the full
shoelace identity separately on every tuple it processes.

## Fitting a polygon at every real translation and rotation

The board in grid-length units has vertices $(0,0),(c,0),(X,Y)/c^3$
where $X=ap(a^2-b^2)$ and $Y=ap\,bq$. Write $F=c^4$, $D=cY$.
For an axial point $w$, the two nonconstant barycentric coordinates
relative to the board edge vectors are $I/D$ and $J/D$ where
$$
 I=Yw_x-Xw_y,\qquad J=Fw_y.
$$
Let a grid rotation be the nonzero complex numerator $g$ divided by
$|g|$, and first apply the numerator alone to each vertex. Then some
translation of the rotated polygon is contained in the board if and
only if
$$
 \max(I+J)-\min I-\min J\ \le\ D|g|.
$$
Indeed translation adds two independent constants to $I,J$. Setting
them to minus their respective minima is feasible precisely when the
third side inequality holds. Containment of the vertices suffices by
convexity. The two sides of this comparison are nonnegative.

It suffices to test rotations aligning a convex hull edge with a board
side. In fact, for a normalized rotation through angle $\theta$, the
left-hand side is a sum of three support functions, call it $W(\theta)$.
Between changes of their supporting vertices it is of the form
$A\cos\theta+B\sin\theta$. The hull has positive area, so $W>0$ and
$W''=-W<0$ on each such interval. A minimum over the circle occurs at a
change, when a board side is parallel to a hull edge. For each hull edge
$e$ and each board side direction $s$ use both numerators $\pm s\bar e$.
Representatives for $s$ are $1$, $(a^2-b^2)+bq\rho$, and $\rho$ times
the latter. Comparing the squares of both sides gives an integer test
over all rigid placements, including a placement tangent to the board.

## Enumeration and independent witnesses

For the required $K=ab$, the following counts are tuples, not
congruence classes. The diameter check uses every vertex pair.

| $N$ | Reflex turn | Area-correct tuples | Within the diameter | Fit under a rigid placement |
|---:|---:|---:|---:|---:|
| 143 (positive control) | $-60^\circ$ | 63 | 31 | 0 |
| 143 (positive control) | $-120^\circ$ | 304 | 176 | 3 |
| 3431 | $-60^\circ$ | 4,955 | 3,936 | 0 |
| 3431 | $-120^\circ$ | 60,180 | 52,359 | 0 |
| 5063 | $-60^\circ$ | 11,783 | 8,507 | 0 |
| 5063 | $-120^\circ$ | 199,323 | 157,586 | 0 |

For the *sharp capacity*, the area of the board gives
$K\le\lfloor Nab/(2c^2)\rfloor$. The verifier enumerates every tuple
at every integer $K$ from 193 to 289 for $3431$, and from 432 to 622 for
$5063$. The largest fitting values are the lower endpoints. A convex
balanced polygon has $K\le\lfloor Nab/(3c^2)\rfloor$ by the central
symmetry bound, giving at most 192 and 415, respectively. Thus including
convex shapes does not increase the maxima.

Here are examples at the exact capacities. The first row is a separate
small-board control. Each listed rotation is applied by Eisenstein
multiplication; every coordinate is rational in the axial basis.

| $N$ | $K$ | Run lengths in the second parameterization | Rotation |
|---:|---:|---|---|
| 143 | 15 | $1,1,2,2,2,4,1,1,2$ | $(39-55\rho)/49$ |
| 3431 | 193 | $3,1,14,6,3,25,3,2,11$ | $(511-1551\rho)/1369$ |
| 5063 | 432 | $5,4,16,11,6,29,6,2,13$ | $(1079-2135\rho)/1849$ |

The [Python verification](check_witnesses.py) constructs the polygons
from their runs, checks simplicity, turning, direction balance and area,
then finds a rational translation by intersecting pairs of contact lines
and testing every vertex against the three original board half-planes.
It does not call the C++ hull or support-function code. This establishes
attainability for the geometric maximization. These are witnesses to the
packing problem only.

The [exhaustive verifier](check_cycles.cpp) is specialized to the three
displayed triples. After the diameter filter the modulus of any vertex
or hull difference in grid units is below 50. A side direction has
modulus at most $c^2\le1849$, hence any rotation numerator has modulus
below 92,450. Each axial coordinate of a complex number has magnitude
at most $2/\sqrt3$ times its modulus. The linear forms and their sum
therefore fit in signed 64-bit integers; the final squared comparisons
fit in signed 128-bit integers. Prior to the diameter filter there are
at most nine runs of at most 49 units. The area and diameter checks on
those coordinates also fit in 64 bits. The code uses no floating point.

From this directory, with GCC and Python 3, run

```sh
g++ -std=c++20 -O3 check_cycles.cpp -o check_cycles
./check_cycles --capacity
python3 check_witnesses.py
python3 check_staircases.py
python3 check_pairs.py
python3 check_long_pairs.py
```

The default C++ invocation checks only $K=ab$ on the three boards.
[Recorded output](replay.txt) includes the full capacity scans and the
independent rational translations.
