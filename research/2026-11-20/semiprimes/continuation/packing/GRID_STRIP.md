# Every scale-one F2 board can be filled up to one strip along a side

Let $a,b,c$ be positive integers with $c^2=a^2+ab+b^2$, $p=a+2b$, $q=2a+b$ and $g=\gcd(p,q)$. In the triangular board with vertices $0,bq,ap\rho$ in the Euclidean axial basis $1,\rho=e^{i\pi/3}$ there is an explicit packing of
$$
pq-p-q+g
$$
congruent triangles of sides $a,b,c$. The remaining area is $p+q-g$ tile units and lies in a single layer along the sloping side. This packing is optimal among all translations of the grid with axes and diagonal described below, even if one selects the grid triangles individually. The conclusion applies to every F2 parameter, including every residual prime pair.

**Construction.** Use coordinates $x,y$ for the physical point $bx+ay\rho$. Integer grid cells are parallelograms, and the diagonal from their lower left to their upper right has length $|b+a\rho|=c$. It splits each cell into two copies of the tile. The board in these coordinates is
$$
x\ge 0,\qquad y\ge0,\qquad px+qy\le pq .
$$
Both halves of a cell contain its lower-left and upper-right vertices. The lower-left vertex gives both coordinate minima; the upper-right vertex gives the largest value of $px+qy$. Either half lies in the board precisely when the whole cell does.

An anchored grid cell with upper-right corner $(i,j)$ belongs to the packing precisely when $i,j\ge1$ and $pi+qj\le pq$. The strictly interior lattice points of the large right triangle number $(pq-p-q-g+2)/2$ by Pick's theorem. There are $g-1$ additional lattice points in the relative interior of the sloping side. The sum gives $(pq-p-q+g)/2$ cells. Equivalently, summing the row lengths $\lfloor q(p-j)/p\rfloor$ for $j=1,\ldots,p$ gives the same formula.

For an arbitrary translated grid reduce its two coordinate offsets modulo one to $s,t\in[0,1)$. A cell contained in the board has lower-left coordinates $i+s,j+t$ with $i,j$ nonnegative integers. Shifting it back by $(-s,-t)$ keeps it inside the board. This injects the available cells into the anchored grid and gives optimality over the stated translations. In the anchored grid every uncovered interior point lies in the closure of a cell cut by the sloping side. Such cells meet that side successively, since the side intersects a convex cell in one interval.

For distinct prime factors $g=1$. Since $1<q/p<2$ when $a>b$, we have
$$
p+q<\frac{3}{\sqrt2}\sqrt{pq}.
$$
Thus every candidate has an ordinary unit-scale packing whose uncovered area is less than $3\sqrt{pq/2}-1$ tiles, with no staircase threshold. The counts at 3431 and 5063 are 3312 and 4920. The [individual exchanges](README.md) give stronger bounds there. Whether the boundary layer can be filled, or a different packing completed, is a separate existence question.
