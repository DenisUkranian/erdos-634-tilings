# First straight cuts on every residual mixed prime-product board

Let the primitive tile have odd sides $a>b>0,c$, opposite angles $\alpha,\beta,120^\circ$ respectively. Put $p=a+2b$, $q=2a+b$, $c^2=a^2+ab+b^2$, $s=ab$, $w=a+b$. The F2 board has sides $A=ap$, $B=bq$, $C=c^2$ opposite $2\alpha,2\beta,60^\circ$. Use the [mixed-ratio reduction](../counting/MIXED_RATIO.md). The remaining mixed pairs have coprime parameters $u>v>0$, with $u$ even and $v$ odd. With $g=\gcd(3,u-v)$,
$$
(a,b,c)=(u^2-v^2,\ v(2u+v),\ u^2+uv+v^2)/g.
$$
They satisfy $a\ge2b$. For $v>1$ the staircase bound gives $u>4v(v-1)$ and hence $u\ge8v$. These are hypotheses on the residual family.

**Theorem.** In any unit tiling, every proper straight cut along tile edges joining two points of the board boundary has one of the following geometries. T-junctions are allowed.

| Corner cut off | Offsets from that corner along the sides in the stated order |
|---|---|
| $60^\circ$, sides $A,B$ | $(s,s),(2s,2s),(s,bw),(bw,s),(2bw,2s),(aw,s)$ |
| $2\beta$, sides $A,C$ | $(cw,ac)$, only for $v>1$ |

All entries listed at the specified parameters are geometric chords. The chord, both offsets and both remaining intervals have lengths in $S=\langle a,b,c\rangle$. They meet the angle, integer-area and additive divisibility conditions below. Tiling both resulting pieces requires additional evidence. The earlier [stopped-run work](../counting/inputs/F2_V1_PURITY.md) gives stronger geometric conclusions for $v=1$ subject to its stated inputs.

### Vertex cuts at arbitrary positive integer scale

The angles $\alpha,\beta$ are rationally independent. Indeed $\alpha+\beta=\pi/3$, and $2\cos\beta=q/c$ is rational strictly between 1 and 2. A rational multiple of $\pi$ could only give a rational algebraic integer here. Every tiled sector has nonnegative integer coefficients in $\alpha,\beta$. A vertex cut at $2\alpha$ or $2\beta$ therefore bisects the angle. Each boundary interval of either child lies in $S$, being covered by whole tile edges even with T-junctions on the other bank.

We have $\gcd(c,3abwpq)=1$. For instance, a common prime of $c,q$ would divide $4c^2-q^2=3b^2$. A common divisor of $c,w$ divides $ab$ by the norm. If $3\mid c$, then $a\equiv b\pmod3$ and the norm is $3b^2\pmod9$, contradicting primitivity. Also $\gcd(p,q)=1$, since a common prime divides 3 and $3\mid p$ would force $a\equiv b\pmod3$.

At integer scale $t$ the adjacent sides at $2\alpha$ have reduced ratio $B:C$. The offsets on the opposite side are integers exactly when $B+C=wp$ divides $tA=tap$, equivalently $w\mid t$. At $2\beta$, use $A+C=wq$. At $60^\circ$ the two sectors are $\alpha,\beta$ in either order. The sine rule gives reduced offset ratios $p:q$ and $a^2p:b^2q$. For the former $p+q=3w$, giving $3w\mid t$. For the latter $a^2p+b^2q=wc^2$, giving $w\mid t$. None is possible at $t=1$. The criteria at general scale are equivalences for offset integrality alone.

### Chords across two side interiors

A chord across two side interiors separates a triangle at the common corner. Its three angle coefficient pairs sum to $(3,3)$. At $2\alpha$ the other two angles jointly have coefficients $(1,3)$, giving just three pairs.

| Other two angles | Primitive integral sides, unordered | Area in tile units at this scale |
|---|---|---:|
| $2\beta,\alpha+\beta$ | $A,B,C$ | $pq$ |
| $\alpha,3\beta$ | $c^2,cp,3bw$ | $3wp$ |
| $\beta,\alpha+2\beta$ | $bc,cw,ap$ | $wp$ |

Use the sine rule, $2\cos\alpha=p/c$, $2\cos\beta=q/c$, and $\sin(3\beta)/\sin\beta=q^2/c^2-1$. The gcd identities above make each triple primitive. Integer sides thus force a positive integer scale, multiplying its mass by the square of that scale. Exchanging $a,b$ gives the table at $2\beta$. The first two rows are too large in both orders. In the third row $4w>\max(p,q)$, so only scale one fits. At $2\alpha$ the incident side $cw$ exceeds both $C$ and $B$, since $w>c$ and $C-B=a(a-b)>0$. At $2\beta$ this side must lie along $A$, with $ac$ along $C$ and chord length $bq$. Its remaining intervals are treated below.

At $60^\circ$ the other two angle pairs sum to $(2,2)$. This gives the original F2 shape, an equilateral triangle, or the two orders of F1 with incident sides $kb,kw$ or $ka,kw$ and opposite side $kc$. Both F1 triples before multiplication by $k$ are primitive.

The necessary scales follow from the [two boundary sums](../cuts/README.md). In headings $z^h\rho^j$, where $\rho=e^{i\pi/3}$ and $z=(a+b\rho)/c$, the sums assign $L(-1)^j$ and $L(-1)^{j+h}$ to an oriented length $L$. Both cancel on internal contacts. The absolute contributions of one tile are $D_-=|a-b-c|$ and $D_+=|a-b+c|$, respectively. These odd integers are coprime since $\gcd(c,a-b)=1$, and their product is $3ab$. For an equilateral triangle of side $L$ both sums have absolute value $3L$, so $ab\mid L$. For the F1 triangle with vertices $0,kb,kw\rho$, the directed headings are $1,z\rho,\rho^4$. The sums are $k(a+2b-c)$ and $k(a+2b+c)$. Divisibility by $D_-,D_+$ respectively gives $D_-\mid3bk$ and $D_+\mid3bk$, hence $a\mid k$. Swapping the two tile labels and its reference frame gives $b\mid k$ for the other F1. The primitive F2 already consumes the full area.

Fitting the remaining scales gives exactly the six entries at $60^\circ$. In detail, $B=2s+b^2<3s$, $bw=s+b^2$, $2bw>B$, $aw>B$ and $2aw>A$ by $a\ge2b$. The six sets of complementary intervals also belong to $S$. Those smaller than $ab$ are $b^2$, while every integer at least $ab$ lies in the semigroup of the coprime pair $a,b$. The chord lengths are whole-side multiples. The listed equilateral and F1 scales give integral areas and satisfy both boundary divisibilities by the expressions just derived.

### The seventh chord

Write $d=w-c$, $e=c-a$. The two residual intervals of the $2\beta$ cap are $C-ac=ce$ and $L=A-cw=ad-be$. For $v=1$, we have $b\mid a+c$ and $0<d<b/2$, since $c>a+b/2$. If $L=xa+yb+zc$ in nonnegative integers, then $|x-z|\le x+z<d$. Reduction modulo $b$ gives $x-z\equiv d$, impossible. This recovers the previously known obstruction.

For $v>1$ put $h=(2u+v)/g$. Then $b=vh$, $\gcd(h,v)=1$, $c\equiv-a\pmod h$, $c\equiv a\pmod v$. Indeed $g$ is coprime to $v$. The integer
$$
H=d-(v-1)h/2=(h-3v^2/g)/2
$$
is positive by $u>4v(v-1)$ and $v\ge3$. Choose $0\le z<v$ with $H+2z\equiv0\pmod v$, and put $x=H+z$. Then $xa+zc\equiv L\pmod h$ since $x-z\equiv d\pmod h$, while both vanish modulo $v$. Thus $b\mid L-xa-zc$. Since $xa+zc\le(H+2(v-1))a+(v-1)e$, nonnegativity of the quotient follows from
$$
(v-1)(1/2-2/h)\ge \big(v+(v-1)/h\big)e/a .
$$
Here $h\ge17$ and $e/a=(u/v+2)/((u/v)^2-1)\le10/63<1/6$. The left side is at least $3(v-1)/8$, and the right side is less than $3v/16$. In particular $L>0$. This gives explicit counts in $S$ on the final interval. The triangle has mass $wq$ and passes both boundary divisibilities. Indeed it is the geometric union of the swapped F1 at scale $a$ and a tile-similar triangle at scale $w$, whether or not its F1 part admits a tiling. See the [F1 to F4 transfer](../../../../../docs/square-class-tails.md).

The first $v>1$ board of the [ratio-1.9 list](../counting/mixed_ratio_19_10.csv) has $(u,v)=(44,3)$, $(p,q)=(2473,4127)$ and $(a,b,c)=(1927,273,2077)$. The witness is
$$
196071=34\cdot1927+463\cdot273+2\cdot2077 .
$$
It certifies the leftover length. Feasibility of tiling both pieces remains open here.

The [independent enumeration](verify.py) replays the classification on the seven residuals below one million and on higher-denominator controls. It enumerates angle triples, computes primitive sides by the exact sine rule, and solves for candidate scales by both boundary divisibilities before testing membership in $S$.

### A constraint on the F4 complement

For $v>1$, a tiling realizing the seventh chord would leave a quadrilateral of **$bq$** tiles. Every proper straight cut of that quadrilateral would join the **interiors of opposite sides**, leaving two quadrilaterals. No triangle can be cut off, even with a cut through an existing vertex.

In the complex plane take $O=0$, $V=A$, $U=B\rho$. The chord joins $D=L$ to $E=V+(a/c)(U-V)$. Its vector is
$$
E-D=(B/c)(b+a\rho).
$$
Thus the successive sides of $O,D,E,U$ have lengths $L,B,ce,B$. The four angles in that order are $\alpha+\beta$, $2\alpha+3\beta$, $\alpha+2\beta$, $2\alpha$. The area follows by subtracting the F4 mass $wq$ from $pq$. Both short lengths are strictly smaller than $ab$. Indeed $L=ad-be<ab/2$, and $ce=bw-ae<ab$ since $a\ge2b$ and $e>b/2$.

Any triangular child inherits a full angle at one quadrilateral corner, with two sides along its incident edges. The two sides may reach either old endpoint. At $O$ every tiled triangular corner cap from the $60^\circ$ list, including the full F2, needs at least $ab$ along both sides. At $D$ the remaining two angle pairs would sum to $(1,0)$, which is indivisible. At $U$ use the $2\alpha$ table above: the F2 and triple-angle rows exceed the entire quadrilateral in area; the F4 option needs $cw>B,ce$. At $E$ the remaining pair sum $(2,1)$ gives only two unordered choices. For angles $\alpha,\alpha+\beta$ the shape is F1 and the incident sides at $E$ are multiples of $ab,bc$ by the earlier scale proof. For angles $\beta,2\alpha$ it is F4 and those incident sides are multiples of $bc,ap$ by primitivity. Both orderings in both cases exceed the available short side $ce$. This excludes each possible triangular child. It permits tilings with no cuts and cuts across opposite sides.

In fact **every such cut joins the two equal sides of length $B$**. The short sides $OD$ and $EU$ lie on the original board sides $A,C$. A chord between their interiors would make a larger triangle at $V$ by adjoining the geometric F4 cap to the part of the quadrilateral between the two chords. Its two new endpoint angles are sectors of the tiled quadrilateral child. Its side lengths are integers, since the offsets from $V$ are sums of the old integer offsets and integer boundary segments. Its area is strictly smaller than the full board. The primitive-side table at $2\beta$ already forces the unique F4 corner triangle at scale one under just these conditions. Strict containment of the previous cap contradicts this. The argument only assumes that the quadrilateral under consideration is tiled.

The [virtual apex argument](VIRTUAL_APEX.md) further restricts these cuts to one direction and at most $2v-1$ positions. Its [integer and rational replay](verify_virtual.py) tests the first examples with higher denominators.
