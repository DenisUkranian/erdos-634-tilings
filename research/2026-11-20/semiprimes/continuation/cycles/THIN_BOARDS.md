# The number of reflex corners grows on thin F2 boards

For the board and supported cycles of [CYCLES.md](CYCLES.md), assume
$a\ge8b$. Every such cycle has at least
$$
 r\ \ge\ \left\lceil\frac{2c^2}{9ab}-1\right\rceil
$$
reflex vertices after straight runs are merged. This conclusion allows
any placement of the grid and any interior tile orientations. It follows
from continuous geometry once opposite directions balance. In particular
it applies to any separated far tail across an empty height. It does not
assert that a tiling or a tail occurs at a given parameter.

Let $B=c^2$, $D=C-B$, so $|D|=bq$. Apply the real affine map taking
$xB+yD$ to $(x,y)$. The board becomes $0\le y\le x\le1$. A finite
slope $s$ in these coordinates corresponds to the physical line directed
by $B+sD$. For $-1\le s\le2$ these vectors lie in a disk centered at
$B$ of radius $2|D|<|B|/2$: indeed $bq/c^2<2b/a\le1/4$.
This disk subtends an angle strictly smaller than $60^\circ$ at the
origin. Hence at most one of the three grid axes has slope in $[-1,2]$.
Over the nonvertical axes let $s_0=\min|s|$ and $s_1=\min|1-s|$.
Then $s_0+s_1\ge1$. If both are below 1, their minimizers must be the
same slope and the claim follows from the triangle inequality.

Let the horizontal projection of the polygon have length $w$. Outside
this interval the uncovered area is at least $(1-w)^2/2$, attained
for the rightmost interval of that length. For almost every $x$ in
the interval choose the lowest and highest boundary points of its
vertical section. With counterclockwise traversal the supporting edges
there point right and left, respectively. This holds even if the vertical
section is disconnected. If a lower edge of slope $s$ is selected on a
set of horizontal measure $l$, its contribution to the uncovered area
below the polygon is at least $|s|l^2/2$. Its nonnegative height is affine
on that edge. Among subsets of measure $l$ the smallest integral is
attained adjacent to the end of smaller height. For the upper edges
apply the same argument to the gap to $y=x$ using $|1-s|$.

Each of the two selections uses at most $3+3r$ distinct edges. To see
this, measure turns in units of $60^\circ$. Positive turns are at least
1 and each reflex turn has magnitude at most 2, so the total number
of merged edges is at most $6+3r$. If all three axes occur, balance
ensures at least three edges are unavailable for the lower selection:
each nonvertical axis has an edge directed left and any vertical axis
has both directions. For the upper selection reverse left and right.
If only two axes occur, an affine map sends them to perpendicular axes;
the resulting rectilinear polygon has $4+2r$ edges. At least two are
unavailable on either side, and $2+2r\le3+3r$. A positive-area polygon
uses at least two axes.

Cauchy's inequality applied separately to the chosen edge lengths gives
uncovered area in the projection interval of at least
$(s_0+s_1)w^2/[2(3+3r)]$. Dividing by the board area $1/2$, the missing
fraction is at least
$$
 (1-w)^2+\frac{w^2}{3+3r}\ \ge\ \frac1{4+3r}.
$$
For a supported cycle the missing fraction is $3ab/(2c^2+3ab)$.
Rearranging yields the claimed bound.

For example it gives at least two reflex vertices for $(161,15,169)$
and $(323,37,343)$, and at least four for $(533,27,547)$, whose board
has $N=587\cdot1093=641591$. The inequality is uniform in the ratio
$a/b$. Its use does not require an assertion about how often both F2
factors are prime.
