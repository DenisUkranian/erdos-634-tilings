# A shortest upper median path is the canonical two-segment path

This result concerns the original unit F2 triangle and arbitrary
congruent-tile dissections. In particular it imposes no corner grids
or assumptions on which short heights occur. It applies to every
odd unresolved mixed semiprime parameter, and more generally when the
coprime ordered integers $u,v$ have $u$ even, $v$ odd and $u>3v$.
Write $g=\gcd(3,u-v)$ and
$$
 ga=u^2-v^2,\quad gb=v(2u+v),\quad gc=u^2+uv+v^2,\quad d=a-b.
$$

**Theorem.** Every vertex-simple upper median path from $O$ to $B$ has
at least $a+b$ whole long edges. If it has exactly $a+b$, in the
$cz$ frame it is $E^a S^b$ with $E=(1,0), S=(1,-1)$, **including
the indicated order**. It cuts off the standard triangle of $c^2$
tile areas, which can in particular be replaced by a standard grid.
Every other path has at least $a+b+2$ edges provided $(u,v)\ne(4,1)$; this exception is already outside the residual semiprime domain.

**Two characters on the enclosed tile union.** We use the directed
upper median path and its simple-region theorem from
`midlevel20/TWO_PATHS.md`. Its endpoints in the $cz$ frame are
$O=0$, $B=(a+b,-b)$, with steps $\rho^i$ (long height 1) or
$\rho^i z$ (long height 2). Each step has physical length $c$.
Let $J_1,J_2$ be the sums of $(-1)^i$ over the two respective
alphabets. The lower polygon's positive boundary comprises the
physical base $O\to B$, of length $c^2$ at height 0, minus the
directed upper path. The ordinary and height-alternating characters
of a tile are, up to signs, $c-d,c+d$. Consequently
$$
 J_1+J_2\equiv d\pmod{c-d},\qquad
 J_1-J_2\equiv d\pmod{c+d}.
$$
We used $\gcd(c,d)=1$, also for division by $c$. For example the
alternating boundary weight is $c^2+c(J_1-J_2)$. These congruences
test the actual closed region, beyond fitting an open path of tiles.

**Projection deficit.** Write $(X,Y)$ for the net height-1 displacement
and $(x,y)$ for the net height-2 displacement before rotation.
Set $m=x+y$. For an integer $t$ the established displacement equations
are
$$
 X=a+b-x-vt,\qquad Y=-b+(u+v)t+m .
$$
For completeness, $t=-[(u+2v)x+(2u+v)y]/(gc)$ is integral because
the first component of $z(x+y\rho)$ must be integral; subtract $x$
and use $\gcd(v,c)=1$. Substitution in the second component gives
the expression for $Y$.

Let $L$ be total path length in steps, and $B_1,B_2$ be the signed
counts of the unoriented $\rho$ axis, i.e., the count of $\rho$ minus
that of $-\rho$ in each alphabet's own frame. A unit step has first
coordinate at most 1. A step on this axis has projection zero. Thus
$C=L-(X+x)\ge |B_1|+|B_2|$. The six unit directions have character
$x_i+2y_i$ except on this axis, where the net correction is
$-3B_i$. It follows that
$$
 J_1-J_2=d+(2u+v)t-3(B_1-B_2).
$$

If $L\le a+b$, then $C\le vt$, so $t\ge0$, and
$J_1-J_2\ge d+2(u-v)t$. This quantity cannot reach the next congruent
value $d+(c+d)$ since $a+b<2d+c$: equivalently
$g(c+a-3b)=(2u+v)(u-3v)>0$. Hence $t=0$, $C=0$, and each step has
first projection 1, i.e. is $E$ or $S$ in its own frame.

Now $F=(u-v)/g$, $D=(2u+v)/g$ are coprime, and the equation for $t$
is $Fx-Dm=0$. Hence $x=Dj,m=Fj$ for an integer $j$. Nonnegative
$E,S$ counts on both heights give $0\le j\le b/F$.
As $B_1=B_2=0$, one has
$J_1+J_2=d-2x+4m=d-6vj/g$. Since $c-d=3v(u+v)/g$, its congruence
says $u+v\mid 2j$. The integer $u+v$ is odd, and $b/F<u+v$,
as $u^2-2uv-2v^2>0$ for $u>3v$. Thus $j=0$.
There are no height-2 steps, and the inventory is $a$ copies of $E$
and $b$ copies of $S$.

The lower polygon is now contained on the $czR$ lattice in the sense
that every vertex is in it (the base is its chord). Its positive area
in tile units is a multiple of $c^2$ since $\gcd(ab,c^2)=1$.
Among words with that inventory the area is uniquely maximized
by $E^a S^b$: exchanging adjacent $SE$ for $ES$ increases it by one
whole unit parallelogram in the scaled lattice. The maximum lower
area is exactly $c^2$ tiles. Thus the path has the asserted order and
the lower triangle is the standard tile-similar one of area $c^2$
in tile units.

**The gap at one extra step.** If $L=a+b+1$, then $C\le vt+1$.
For $t\ge0$, the previous calculation gives
$J_1-J_2\ge d-3+2(u-v)t>-c$. The upper bound $L<2d+c$ still holds
since $(2u+v)(u-3v)/g>1$. Its congruence forces $J_1-J_2=d$.
But all $L$ summands are odd and $L$ is odd while $d$ is even.
The only possibility with $t<0$ is $v=1,t=-1,C=0$.
It gives $J_1-J_2=d-(2u+1)$, strictly between $-c$ and $d$ as
$c+d=(u-1)(2u+1)/g$ and $u-1>g$. The last strict inequality excludes
the boundary instance $u=4,v=1$; for it $u-1=g=3$ and the congruence
at $a+b+1$ is consistent, so the claimed one-step gap is asserted
only for $u\ge6$ below. All original odd residual parameters satisfy
$u/v\ge6$.

**Scope of the gap.** The minimum and rigidity hold already for $u>3v$.
The one-step gap uses $u-1>g$ when $v=1$ and thus holds for
$u>3v$ except $(u,v)=(4,1)$. No claim is made here for that parameter's
one-step case.

At $(a,b,c)=(33,7,37)$ this requires 40 steps canonically or at least
42; at $(35,13,43)$ it requires 48 steps canonically or at least 50.
The mixed 40-step and 47-step configurations satisfying the earlier
open-path containment and area tests cannot occur as upper median
paths in completed tilings.

## Companion theorem for the lower median path

On the same original boards, every **even** lower path has at least
$a+b$ edges. At equality the only possible path is the identical
canonical $E^aS^b$ in the $cz$ frame. Equivalently, a lower path's
odd excess beyond its straight-base minimum $c$ is at least $a+b-c$.
Other even lengths start at $a+b+2$. Odd path lengths, including the
straight base $c$, are outside this parity restriction. Again the
result holds for all $u>3v$ under the odd primitive assumptions.

Indeed the low exterior is the base. The arc may follow it for some
distance, but closing the arc by the base gives an integral tile
winding chain, hence both characters still apply. In the $cz$ frame
the alphabets for the lower cut are the middle steps $\rho^i$ and the
low steps $\bar z\rho^i$. Call their characters $J_M,J_L$ and their
net vectors in their respective alphabet frames $(X,Y)$ and $(x,y)$.
The congruences are
$$
 J_M+J_L\equiv d\pmod{c-d},\qquad
 J_M-J_L\equiv d\pmod{c+d}.
$$
The second follows from the height-alternating lower-polygon boundary
weight $c^2+c(J_M-J_L)$. For the net-displacement calculation put
$A=(u+2v)/g$, $D=(2u+v)/g$, $F=(u-v)/g$. The first-coordinate
equation gives an integer $t=(Fx+Dy)/c$ and $X=a+b-x-vt$, since
$a+b-c=vF$, $b=vD$, and $v$ is a unit modulo $c$. The second coordinate
is $Y=-b+(b x-a y)/c$. With the respective signed $\rho$-axis counts
$B_M,B_L$ as before, direct subtraction gives
$$
 J_M-J_L=d-(2u+v)t-3(B_M-B_L)
$$
using $c+a-b=(2u+v)F$ and $2a+b+2c=(2u+v)D$.
For $L\le a+b$, $|B_M|+|B_L|\le vt$ forces $t\ge0$. Hence
$J_M-J_L\le d-2(u-v)t$. If $L$ is even, that difference is even.
The next smaller *even* member of its congruence class is
$d-2(c+d)<-(a+b)$. Therefore $t=0$, and the first-coordinate
projection deficit is zero. All steps are $E$ or $S$ in their
respective frames. Now $x=Dj$, $y=-Fj$, $Y=-b+Aj$, where
$bD+aF=cA$. Thus $0\le j\le b/A<2v$. Also
$J_M+J_L=d+2(A-F)j=d+6vj/g$. The first character enforces
$(u+v)\mid 2j$, and $4v<u+v$. Hence $j=0$. The inventory is purely
middle with $a$ copies of $E$ and $b$ copies of $S$.
In this case no interior point of the base belongs to the middle
step lattice: its endpoint in $R$ is the primitive vector $(a+b,-b)$.
Thus the lower bounded polygon has positive tile area, divisible by
$c^2$, and the same maximum-area argument forces the canonical order.
If both cuts use this equality case, the bodies of their long-edge
paths coincide, and their distinct forced tiles lie on opposite banks.

## Odd upper paths incur an excess of order b

Put $K=a+b$. In the residual range $u/v\ge6$, every odd-length
upper median path satisfies
$$ L\ \ge\ 2K-c+2.$$
The bound follows directly if $L\ge 2d+c$, since $c>3b$.
Below that threshold parity and the alternating character force
$J_1-J_2=-c$. To see that the next smaller odd representative is also
excluded, note that $3c+2d>2d+c$. The identity above and
$c+d=(2u+v)F$ yield
$$
 B_1-B_2={(2u+v)(t+F)\over3},\qquad
 L-K\ge -vt+{2u+v\over3}|t+F|\ge vF=K-c .
$$
The last estimate uses $(2u+v)/3>v$, so equality implies $t=-F$
and $C=0$. Then all steps are $E$ or $S$, and displacement imposes
$x=ut+Dj$, $m=Fj-vt$ as in the upper-path net theorem; this
parameterization follows by solving $Fx-Dm=ct$ with $uF+vD=c$.
The ordinary character is
$$ J_1+J_2=d-3vt-6vj/g .$$
Its congruence gives $2j\equiv u-v\pmod{u+v}$, i.e.
$j\equiv-v\pmod{u+v}$. If $j\le-v$ one finds
$x=-uF+Dj<0$. If $j\ge u$ the number $X+Y$ of middle $E$ steps is
negative: its value at $j=u$ is $-vA$ (where $A=(u+2v)/g$), and
its slope is $F-D=-A<0$. This rules out equality. Since both $L$
and $2K-c$ are odd, the next possible length is $2K-c+2$.
This gives lower bounds 45 and 55 at the two controls. Exact evaluation
of the linear direction inventories raises them to 49 and 57 there;
whether such longer paths can be completed is separate.
