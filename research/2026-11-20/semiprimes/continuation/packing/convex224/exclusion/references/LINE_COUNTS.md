# An occupied orientation level needs at least two blocks of tiles

Use the tile, board and heights of [the full-board theorem](FULL_BOARD.md).
Throughout, $a>b$ are odd and the triple is primitive. For the unit F2
triangle, at every $h\ne2$,
$$
 n_h=0\quad\hbox{or}\quad n_h\ge2c.
$$
At some odd height $n_h\ge3c$. This applies to the entire board, for every
primitive parameter denominator $v$, independently of reflections, seam
placements or T-junctions.

In fact the exclusion of $n_h=c$ works for any tiled polygon at any
height where the signed exterior length on **each supporting line** of
that height is a multiple of $c$. Containment of the polygon and tiling
in the common direction normalization is understood. A total current
summed over all parallel lines would be too weak for this statement.

## A bound from intersecting lines

Let $G_h$ be the sum of the signs $\epsilon$ of the tiles counted at $h$.
The short-edge character on this height is $(a-b)G_h$, with opposite
signs on the $a$ and $b$ edges of each tile. All long edges have integral
length $c$. The exterior assumption therefore gives $c\mid G_h$, since
$\gcd(c,a-b)=1$. If $n_h=c$, parity forces $G_h=\pm c$, so all the
$c$ tiles have one common sign.

Take the $r$ distinct lines used by their short edges. On a line let
$M,L$ count the $a$- and $b$-edges. Add directed lengths along that
entire line, with the sign of the direction character. Whole long
edges and the exterior contribute multiples of $c$. Thus
$$
 (c-a)M+bL=0\pmod c,qquad \sum M=\sum L=c.
$$
Both $M$ and $L$ are at most $r-1$. Indeed, naming the line for the
$a$-edge and that for the $b$-edge fixes the obtuse vertex at their
intersection. The two choices of ray pairs for the $120^\circ$ sector
are opposite. Their tiles have opposite signs, so at most one is
available. Distinct tiles cannot occupy the same placement. This
line argument ignores no partial edge contacts.

Take $u/v=(a+c)/b$ in lowest terms and $g=\gcd(3,u-v)$. Then
$$
 ga=u^2-v^2,\quad gb=v(2u+v),\quad gc=u^2+uv+v^2 .
$$
Indeed the ratios follow by substitution in the norm equation and the
gcd of the three numerators is $g$: any common divisor is coprime to
$uv$, divides $2u+v$ and hence divides $3u^2$. Here $u$ is even, $v$
odd, $u>(1+\sqrt3)v$. Put $A=(u+2v)/g$, $D=(2u+v)/g$.
Then $\gcd(A,D)=1$, $D$ is odd, $c-a=vA$, $b=vD$, and
$2c=vA+uD$. Each used line determines integers $t,s$ with
$$
 AM+DL=tc,\quad t\ge1,\qquad
 2M=vt+Ds,\quad 2L=ut-As.
$$
For the first equality divide the congruence by $v$ modulo $c$.
For the second pair use $A(2M-vt)=D(ut-2L)$ and coprimality.
The parity is $s\equiv t\pmod2$. On summing the line equations,
$$
 \sum t=A+D=3(u+v)/g,\qquad \sum s=u-v .
$$

**Case $g=1$.** Here $t=1$ would give $s\ge1$ by $D>v$ and parity,
and then $2L\le u-A<0$. Hence every $t\ge2$ and
$r\le3(u+v)/2<D$. Since $M,L\le r-1$,
$$
 t < \frac{9(u+v)^2}{2(u^2+uv+v^2)} < 6 .
$$
We have $D>5v$ and $t\le5$, so $M\ge0$ forces $s\ge0$.
Also $M<D$ forces $s\le1$. Exactly $u-v$ lines therefore have $s=1$,
and each has odd $t\ge3$. In particular
$3(u+v)=\sum t\ge2r+u-v$, or $r\le u+2v=A$.
But every line with $s=1$ has $M\ge(3v+D)/2=A$, contrary to $M<r$.

**Case $g=3$.** Here $r\le u+v$ and
$$
 t < \frac{3(u+v)^2}{u^2+uv+v^2}<4 .
$$
If $s\ge3$ then $M\ge(v+3D)/2=u+v\ge r$. Negative $s$ is impossible
at $t=1$ by $D>v$, and at $t=2$ by parity and $D>v$. At $t=3$ it
would give $L>3u/2>u+v\ge r$. Thus $0\le s\le2$.
The possible pairs are $(1,1),(2,2),(2,0),(3,1)$. Exactly $v$ lines
have $t-s=2$, since the total difference is $2v$. Their $t$ is at
least 2, so $u+v=\sum t\ge r+v$ and $r\le u$. For either pair of
difference 2, $L\ge u$, since $A<u$. Again $L<r$ fails.

## Consequences on the original triangle

The exterior at height 0 is a single side of length $c^2$. At every other
height except 2 the exterior contribution is zero. The hypotheses
therefore apply at every $h\ne2$. Combine the exclusion just proved
with the [height divisibility theorem](../../i120-global-oct7/HEIGHT_LEVELS.md)
to obtain the stated bound. The two boundary characters on the full board
both equal $-3ab$, giving $\sum G_h=c+d$ and
$\sum(-1)^hG_h=-(c-d)$ with $d=a-b$. Therefore $\sum_{h\text{ odd}}G_h=c$.
Each $G_h$ with odd index is a multiple of $c$. At least one of their quotients by $c$ is odd.
At that height $n_h/c$ is also odd by parity, so it is at least 3.

Writing $j=N\bmod c$ with $1\le j<c$, the number of occupied heights is
at most $1+\lfloor(N-j-c)/(2c)\rfloor$. In particular, a search with
only two occupied heights must use 1 and 2: height 2 is compulsory,
and if height 1 is absent, four distinct heights are forced by the
full-board theorem. Such a search needs at least $3c$ height-1 tiles.
These restrictions do not decide whether the admissible inventories
have a geometric realization.
