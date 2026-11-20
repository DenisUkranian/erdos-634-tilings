# How the quadrilateral fits in the unit F2 triangle

Let $n=a-b$, $p=a+2b$, $q=2a+b$, $\rho=e^{i\pi/3}$ and
$z=(a+b\rho)/c$. Here use the reflected frame with the smallest-angle
vertex at $0$ and its bisector along the real axis. The other vertices
are $A=c^2\bar z$ and $C=apz$. Put $W=ac$, $J=c^2z$.
The triangles $0AW$ and $0WJ$ are mirrors across the real axis and
each is the tile at side scale $c$. Their interiors are disjoint and
$J$ lies on $0C$ since $ap-c^2=bn>0$. Their complement has successive
vertices $W,A,C,J$ and side lengths $bc,bq,bn,bc$. Only a tiling using
both these corner pieces needs to fill this particular quadrilateral.

In the coordinates of the [orientation obstruction](PROOF.md), the
quadrilateral is the region between $cT_o$ and $nT_i$ in the
angle-$\beta$ wedge. Its vertices in cyclic order are
$(c^2,0),(0,ac),(0,nc),(na,0)$ in the $(1,z)$ basis. Its four sides
have lengths $bc$, $bc$, $bn$, and $c^2-na=bq$. The parallel positions
can also be checked by matching the two shared $bc$ sides: the corner
between them is $120^\circ$ and the two adjacent angles are
$\alpha$ and $180^\circ-\alpha$. Thus the two quadrilaterals are
congruent. The number of unit tiles needed is $c^2-n^2=3ab$.
