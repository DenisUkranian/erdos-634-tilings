# A convex repair region with no acute tile-angle corner

Use the notation and geometry of [the pentagon construction](PENTAGONS.md).
Start with either the one-step or the two-equal-step board and extend the
vertical row all the way, $j=s$. Write $P=X-sf$ and $T=P+bF$.
The current pentagon ends in the complete side $TP$ shared with the
horizontal $b$-grid at this anchor.

For any $1\le l\le b-s$, take the $l$-band of this horizontal grid
along $PT$. Its far edge runs from $P+le$ to $T+lU$.
Also take the adjacent $s$ by $l$ upper grid rectangle with corners
$T,T-sV,T-sV+lU,T+lU$. This is a genuine rectangle of upper-grid
cells in the affine $U,V$ coordinates: on the first step the
availability condition is $b-s\ge l$, while on the second it is
$b+r-2s\ge l$ (where $r>s$). The signed-corner cancellation has
already turned the horizontal block into a full, positive $b$-grid.
Both annexed blocks are ordinary grid units. Their union with the
pentagon is the convex hexagon with cyclic vertices
$$ P,Y,W,D+lU,T+lU,P+le. $$
The consecutive edge directions are $f,e,U,V,-F,-e$ and all six
lengths are positive. In order they are
$$ sc+tb,\quad ta-kc,\quad (k+l)b,\quad sa,\quad
 (b-l)a,\quad lc. $$
The six angles are $60^\circ,120^\circ,180^\circ-\alpha,120^\circ,
120^\circ,180^\circ-\beta$. The former indivisible angle at $P$ is now
$\alpha+\beta$. The number of tiles required inside the hexagon is
$$ t^2-k^2+2s(a-s)+s^2+l(2b-l+2s). $$
The last term is the size of the new band and rectangle. A filling of
one hexagon suffices to tile the full unit board; in the two-step
layout the second required hexagon is its translate.

The construction and independent pairwise-separation verifier are
`notchshape.py` and `notch_check.py`. For example,
`verify(unit_board(33,7,37,2,2,1))` returns two identical remaining
regions of size 250 on the 3431 triangle. The same test with
`(35,13,43,2,4,1)` gives two remaining regions of size 414 on 5063.
The asymmetric loads $(r,s)=(26,1),(4,3)$ for 3431 also give a single
hexagon of size 248 by applying the annexation on the first step.
These are dissection certificates for the regions outside the hexagons.

A finite construction search on the seven controls tried to successively
remove tile-similar convex corner triangles of integer scale, ending in
a grid parallelogram or a triangle. For every oversized admissible load
and every viable $l$, the enumeration found no filling in this class
(1,042 tested shape-parameter tuples, allowing candidate step loads
before checking the rest of a staircase). Independent seam scans of the
two scale-2 control tilings and the scale-3 and scale-4 generated layouts
also found no congruent hole as a fully supported patch in a two-by-two
block of their point-reflected periodic repetitions, with $l=1$ or
$l=b-s$. Neither computation excludes an arbitrary tiling of any board.

In the residual sector the one- and two-step versions are the only
equal-load multiplicities. In fact
$\gcd(c-a,c-b)=\gcd(v(u+2v),u(u-v))/g=2$. Since $\gcd(u,v)=1$,
the $v$ factor is prime to $u(u-v)$ and $u$ is prime to $u-v$.
Consequently the numerator gcd factors as
$\gcd(u+2v,u)\gcd(u+2v,u-v)=2\gcd(3,u-v)$
when $u$ is even and $v$ odd. Unequal loads remain possible.
