# Two congruent convex pentagons in the unit F2 board

Let the primitive tile have odd integer side lengths $a>b>0,c$, with
$c^2=a^2+ab+b^2$. Set $p=a+2b$, $q=2a+b$, $N=pq$, and suppose
$c>3b$. There is an exact dissection of the unit F2 triangle into
ordinary grids of the tile and **two translates of a single convex
pentagon**. Each pentagon has area equal to
$$M=t^2-k^2+2(a-s)+1,qquad
s=(c-a)/2,\quad r=(c-b)/2,\quad t=(a-b)/2,\quad k=r-b.$$
Any tiling of one pentagon by the original tiles gives a tiling of the
complete triangle by translation and addition of the certified grids.
This is a sufficient reduction. An arbitrary original tiling need not use
the indicated partition. Primality is unnecessary for the construction.

In Eisenstein coordinates $(x,y)\equiv x+y\exp(i\pi/3)$ the five
corners, cyclically around the first corner taken as the origin, are
$$
 \begin{split}
 &(0,0),\quad(0,c+tb),\quad(ta-kc,c+tb),\\
 &(ta-ka^2/c,c+tb-kab/c),\\
 &(ta-ka^2/c+ab/c,c+tb-kab/c+b^2/c-c).
 \end{split}
$$
All quantities are explicit in the original (unit-scale) tile metric.

## Proof of the dissection for arbitrary parameters

The board has vertices $O=(0,0)$, $H=(bq,0)$, $J=(0,ap)$. Put
$$
 e=(c,0),\quad f=(0,c),\quad
 U=(b(a+b),-ab)/c,\quad V=(ab,-a(a+b))/c,
 \quad F=(a^2,ab)/c,\quad G=(ab,b^2)/c .
$$
Then $U+F=e$, $G-V=f$, $bF=aG$ and $H-J=c(U+V)$.
Write $\Delta(A;E,B;n)$ for the oriented chain of the triangle with
corners $A,A+nE,A+nB$, given positive planar orientation even when
$n<0$. Its boundary is zero when $n=0$. The signed $j$-band of
the $n$-grid (integer $n>0$, $j\ge0$) is by definition
$$
 \Delta(A;E,B;n)-\Delta(A+jE;E,B;n-j).
$$
For $0\le j\le n$ this is an ordinary grid band (empty at $j=0$).
For $j>n$ the corner subtracted is a positive triangle of scale $j-n$
outside the original grid, on its far side. Oriented side cancellations
in this identity hold for either sign.

Use anchors $P_i=(b(q-c)-id,ih)$, $0\le i\le2$, where
$$d=rc-ta=b(q-c)/2,\qquad h=sc+tb=a(p-c)/2.$$
Indeed $ar-bs=ct$ and $c^2=a^2+ab+b^2$. Both increments are positive,
$d$ is a multiple of $b$ and $h$ a multiple of $a$ because $p,q,c$ are odd.
The horizontal terminal coordinate is zero and
$P_2=J-af$. The first upper corner starts at $P_0+be=H$.
Write $T_i=P_i+bF=P_i+aG$. At each anchor install these **signed**
pieces before pairing and extending them:
 
- a horizontal band of the $b$-grid with $(E,B)=(e,F)$, width $b$ at
  $i=0$ and $r$ at $i=1,2$;
- a vertical band of the $a$-grid with $(E,B)=(f,G)$, width $s_i=s$
  at $i=0,1$ and $s_2=a$ at $i=2$.

The vertical widths satisfy $1\le s<a$ since $c<a+b<2a$.
For $i=0,1$, put $X=P_i+sf$, $Y=X+(0,tb)$, $Z=X+t(a,b)$.
Install the positive triangle $XYZ$, a grid of scale $t$ because its
sides have lengths $tb,ta,tc$. On its left add the rectangle in axial
coordinates $[0,P_i.x]\times[P_i.y,P_i.y+h]$, a parallelogram grid
of $b$ by $a$ cells split along the sum diagonal. Here
$Z=P_{i+1}+re$.

The last required region adjoins the outer side $HJ$. In coordinates
$H-IU-LV$ it lies between the diagonal $I=L$ from $(0,0)$ to $(c,c)$
and the staircase advancing $b$ in $I$, then $s$ in $L$, $r$ in $I$,
$s$ in $L$, $r$ in $I$, and $a$ in $L$. These advances reach $(c,c)$.
Every nonterminal vertical level is at most $2s=c-a<b$, while the first
horizontal advance is $b$. Thus the staircase stays in $I\ge L$, and
this region is a union of unit $(U,V)$ grid parallelograms and their
diagonal halves. These split into the prescribed triangles since
$|U|=b, |V|=a, |U+V|=c$.

For detail on the signs, the horizontal band's top right edge runs
from $T_i$ in direction $U$, and the vertical band's top edge runs
from $T_i$ to $T_i-s_iV$. The identities
$$
 T_{i+1}=T_i-sV-rU,\qquad
 D:=T_i-sV=X+(a-s)G=Z-kF,\qquad W:=P_{i+1}+be=Z-ke
$$
match these edges to the staircase and to the bridging triangle.
Equivalently the vertical band and the bridge meet on the line through
$X,D,Z$; the bridge and the next horizontal band meet on the horizontal
through $Y,W,Z$. For $r>b$, the excess on the two lines is exactly
the two edges $DZ$ and $WZ$ of the subtracted corner $ZWD$. Its
third edge $WD$ continues the right boundary $T_{i+1}W$ of the
positive horizontal grid beyond $W$ in direction $U$.
The horizontal anchor slice matches the lower rectangle and the upper
one at $P_{i+1}$. The initial and final outside segments lie on $OH$
and $OJ$. These identities give oriented boundary cancellation down
to $OHJO$; another way to check the signs is that the signed band's
vertices follow $A,A+jE,A+jE+(n-j)B,A+nB$ as a boundary chain,
also for $j>n$. In this formula use the same orientation sign as
the initial grid's ordered edge pair. The closed oriented sum has the
winding number of the board at every point off the finitely many edges.

The subtracted corner is entirely contained in the positive bridge:
on its two rays from $Z$ the lengths left after removing it are
$$ ta-kc=bc-d=b(3c-q)/2>0,\qquad tc-ka=b(a-s)>0.$$
The latter identity uses $D-X=(a-s)G$. For the first inequality
$q^2=4c^2-3b^2$, so $q<2c$.
Pair the two positive bridges with their respective negative corners.
This replaces each pair by the positive convex quadrilateral $XYWD$
of tile area $t^2-k^2$. All regions are now positive, so their winding
number sum proves both containment and disjoint interiors. Closedness
and finiteness give the whole closed board. This argument allows
non-edge-to-edge contacts and does not rely on a finite list of shapes.

Finally remove the last single row of the preceding vertical band
(the row between widths $s-1$ and $s$) and annex it to $XYWD$. Its far
side meets $XD$ exactly. Its other long side runs from $X'=X-f$ to
$D'=D+V$ with $D'-X'=(a-s+1)G$. The row contains
$(a-s+1)^2-(a-s)^2=2(a-s)+1$ tiles. The union has cyclic vertices
$X',Y,W,D,D'$, giving the displayed coordinate formula. The successive
edge directions are $f,e,U,V,-G$ with strictly positive coefficients:
in particular $D-W=kU$, $D'-D=V$, and $X'-D'=-(a-s+1)G$.
Each consecutive determinant is negative (including $(-G,f)$), so
the five corners are strictly convex. The two pentagons are translates
since both steps use exactly the same $s,r,t$ and the same depth.

## Entire odd residual sector and sharp guaranteed area coverage

Use the ordered primitive parameters
$$
 (ga,gb,gc)=(u^2-v^2,v(2u+v),u^2+uv+v^2),\qquad
 g=\gcd(3,u-v).
$$
In the unresolved odd mixed-prime sector $u$ is even, $v$ odd, and
the sharp staircase reduction requires $u>4v^2$, except possibly
$u>4v(v-1)$ for $g=3$, $v=2\bmod3$. See
[the arithmetic reduction](https://github.com/DenisUkranian/erdos-634-tilings/blob/dab363d0600d62a2c483b9ec1ac5265f1f595a9b/research/2026-11-20/semiprimes/staircase/SHARP_STAIRCASE.md).
Thus $x=u/v\ge6$: for $v=1$, $u\ge6$; for $v\ge3$ the ordinary
bound gives $x>4v\ge12$ and the exceptional bound requires $v\ge5$,
giving $x>4(v-1)\ge16$. Since $g(c-3b)=u^2-5uv-2v^2>0$
for $x\ge6$, the dissection applies uniformly.

In fact the area occupied by the ordinary completed tile grids is always
at least $3095/3431=90.2069\ldots\%$ of the whole triangle. The
smaller of the two control boards attains equality. To check this
sharp fraction, write $\eta=g/v^2\le3$ and
$H=(x^2+4x+1)(2x^2+2x-1)$. The two pentagons jointly have fraction
$$
 R(x,\eta)=\frac{2M}{N}=
 \frac{3x(x-4)(2x+1)/2+2\eta(2x^2-x-4)+2\eta^2}{H}.
$$
Indeed $t^2-k^2=3uv(u-4v)(2u+v)/(4g^2)$ and
$2(a-s)=(2u^2-uv-4v^2)/g$. The expression increases in $\eta$
for $x\ge6$. At $x=10+w$, the difference
$2H(336-3431 R(x,3))$ equals
$$3w(448w^3+13298w^2+128725w+404100).$$
Only $u=6,8$, $v=g=1$ occur below $x=10$; the formula gives
$R(6,1)=360/5063$ and $R(8,1)=1050/13871$, both strictly below
$336/3431$. For $u=10,v=1,g=3$, equality holds. More generally
$R=O(1/x)=O(v/u)$ as $x\to\infty$, so along any unbounded sequence of
these residual parameters, the proportion still to fill tends to zero.
(The residual bound gives $v=O(\sqrt u+1)$.) The fraction measures area
in each board, not the proportion of open numbers decided.

## A single larger pentagon and fewer remaining tiles

A different dissection needs only one copy of a convex pentagon. Take a
single step $r=c-b,s=c-a,t=a-b,k=c-2b$, and annex one row as above.
All formulas for the five corners and for $M$ continue to hold with
these new parameters. The same proof now uses the two anchors $P_0,P_1$
and the two positive increments $d=b(q-c)$, $h=a(p-c)$, which end at
$P_1=J-af$. The upper path is $b,s,r,a$, with $s=c-a<b$.
The removed corner fits strictly since
$ta-kc=bc-d=b(2c-q)>0$ and $tc-ka=b(a-s)>0$.
All other lengths and widths are positive by $c>3b$ and $c<a+b$.
Thus a positive tiling of this single pentagon also suffices for the
original unit problem.

The exact missing fraction is now
$$
 R_1(x,\eta)=
 \frac{(x-3)(x-1)(2x+1)+2\eta(x^2-x-3)+\eta^2}{H}.
$$
Here $t^2-k^2=v(u-3v)(u-v)(2u+v)/g^2$.
As before $R_1$ increases with $\eta$.
At $x=10+w$, $H(206-3431R_1(x,3))$ equals
$$w(412w^3+11678w^2+108425w+326412).$$
The two small parameter cases have fractions $250/5063$ and $702/13871$,
both below $206/3431$. Thus this single-pentagon dissection certifies
that at least $3225/3431=93.9959\ldots\%$ of the board area consists of
completed grids. Equality is attained at 3431. The single holes need
206 and 250 tiles on the first two controls; the two-copy version has the
smaller individual holes of 168 and 180, respectively.

One may also annex $j$ rows at once, $1\le j\le s$, with $X'=X-jf$,
$D'=D+jV$. The area to fill per pentagon becomes
$t^2-k^2+2j(a-s)+j^2$, and the same convexity and grid checks apply.
For $j=s$ the side $D'X'$ has length $ab$.
