# Exactly two effective mismatch directions force the outer boundary words

Let $a>b>0$ be primitive with $a^2+ab+b^2=c^2$ an integer square. Use $p=a+2b$, $q=2a+b$, $\rho=e^{i\pi/3}$, and $z=(a+b\rho)/c$. The scale-one F2 board in this frame has vertices $0,bq,ap\rho$ in counterclockwise order. Write $X,Y,S$ for the unsigned multiplicities of sides $a,b,c$ along $[0,bq]$, $[0,ap\rho]$ and the opposite sloping side. Their lengths are $bq,ap,c^2$. The three counterclockwise headings are $1,-\rho,\rho z^2$, in the order $X,Y,S$.

On an internal straight contact, take consecutive endpoints common to the two banks. The two words between them have equal physical length. For each unoriented axis choose one of its two signs as reference. The signed counts of the tile edges on its two banks are subtracted, giving a vector in the integer lattice orthogonal to $(a,b,c)$. The sign convention here makes the sum of all formal tile boundaries equal the oriented exterior **minus** the resulting net interior vectors. Aggregate independently on each axis, including all translates. Call an axis effective when its resulting vector is nonzero. Any effective axis has an actual mismatch. There may also be mismatches which cancel in the aggregate.

**Alternative for every complete tiling.** Either at least three distinct axes are effective or the two effective axes are exactly $1,z$. In the latter case the signed differences and unsigned boundary multiplicities satisfy
$$
 D_{1,0}=(c,-c,b-a),\qquad
 D_{0,0}=(X_a+a-b,\ X_b,\ X_c-c),\qquad
 S=(0,0,c),\quad Y=(0,a-b,c).
$$
Subscripts $h,j$ denote the unoriented axis $\rho^j z^h$, represented with $0\le j<3$. In particular the slope side must be made entirely of long edges. No position of a seam, paucity of T-junctions, or uniform grid is assumed. The equations are necessary conditions for genuine tilings.

## A side-count identity before identifying different axes

Write $e_0,e_1,e_2$ for the formal coordinate vectors of a free integer group of rank three. No linear relation from the Euclidean plane is imposed between them. Represent the oriented direction $\rho^{j+3}$ by $-e_j$, the direction $\rho^j$ by $e_j$. Rotation by $60^\circ$ is the linear map $R(v_0,v_1,v_2)=(-v_2,v_0,v_1)$.

For each height $h$, let $A_h,B_h,C_h$ be the three signed tile-edge counts at this height in these three axes, separated by lengths $a,b,c$. For example $A_h$ is the signed vector of length-$a$ edges. They are the signed outer counts minus the aggregate mismatch vectors, coordinate by coordinate. This claim concerns counts of whole edges, not counts of subdivided atoms: a bank contributes its entire word once between common endpoints.

Orient every tile counterclockwise. If its directed $a$ edge has vector $a\rho^jz^h$, the directed $b$ edge is either $b\rho^{j+1}z^h$ or $b\rho^{j-1}z^h$. This follows since the two sides meet at $120^\circ$ and occur with one pointing in, the other pointing out. In the first case the directed $c$ edge is $-c\rho^j z^{h+1}$ and in the second it is $-c\rho^j z^{h-1}$, by closure of the triangle. Let $U_h,V_h$ be the signed vectors of $a$ edges, split according to these two alternatives. Then
$$
 A_h=U_h+V_h,\qquad B_h=R U_h+R^{-1}V_h,\qquad C_h=-U_{h-1}-V_{h+1}.
$$
In particular $U_h=U_{h-2}+C_{h-1}+A_h$. Everything has finite support since the tiling is finite. The alternating functional $\chi(e_j)=(-1)^j$ satisfies $\chi(B_h)=-\chi(A_h)$. Consequently there is always a nonzero mismatch at height zero: the exterior contributes $X_a+X_b+Y_a+Y_b$ to $\chi(A_0+B_0)$, which is strictly positive. Indeed $\gcd(c,bq)=1$ (use primitivity, $4c^2-q^2=3b^2$ and $3\nmid c$); thus the side of length $bq$ cannot consist exclusively of $c$ edges. To see $3\nmid c$, divisibility by 3 would give $a\equiv b\pmod3$ and the norm would be $3b^2\pmod9$, contradicting squarehood and primitivity.

## Excluding all other axis pairs

Normalize physical lengths by $c$. With an indeterminate $t$ let $a(t)=(\rho/t-\bar\rho t)/(\rho-\bar\rho)$ and $b(t)=(t-1/t)/(\rho-\bar\rho)$. Put $L_W=W_a a(t)+W_b b(t)+W_c$ for any word vector $W$. The individual oriented tile closes formally at all $t$, since $a(t)+\rho^{\pm1}b(t)=t^{\pm1}$. Summing yields the Laurent identity
$$
 L_X-\rho L_Y+\rho t^2 L_S=\sum_{h,j}\rho^j t^h L_{D_{h,j}} .
$$
All three $c$ counts in the outer words are positive. Otherwise each edge on such a side would have a $120^\circ$ endpoint. An outer corner angle is smaller than $120^\circ$, and no interior point along the side can receive two such endpoints. There are fewer interior endpoints than edges. Consequently the coefficients at powers 0 and 2 of the left hand side are $X_c-\rho Y_c\ne0$ and $\rho S_c\ne0$.

An effective summand has both extremal powers $h-1,h+1$: its two real short-side multiplicity differences cannot turn either complex coefficient to zero unless both vanish, which would make the long-side difference zero by equality of the actual lengths. If all effective terms were of height zero they could not supply power 2. Since one height is zero, at least two directions are required. With exactly two, their heights are distinct. The extremal powers cannot cancel across different heights. Thus both heights must be in $\{0,1,2\}$ and the second is 1 or 2.

If it were 2, power 2 gives $\rho^j D_{2,j,c}=\rho S_c$, requiring the axis to be $j=1$ and the multiplicities equal. Power 3 is likewise supplied exclusively by this direction. Its complex coefficient gives $D_{2,1,b}-\bar\rho D_{2,1,a}=S_b-\bar\rho S_a$. Taking the two real coefficients in this quadratic field proves $D_{2,1}=S$. This contradicts nonzero physical side length for $S$ and zero for any difference. So the heights must be 0,1 and the missing power 3 forces $S_a=S_b=0$. Hence $S_c=c$.

At heights above 2 all three signed data are zero; finite support and the recurrence force $U_h=0$ for $h\ge2$ (use $A_h=C_h=0$ above 2). Similarly $U_h=0$ for $h<0$. At height 2 we have $A_2=B_2=0$, $C_2=c e_1$, so $U_1=-c e_1$. At height 1, write $A_1=A e_j$, $B_1=B e_j$. The middle identity becomes
$$
 B e_j=-c e_2+A R^{-1} e_j+c e_0.
$$
For $j=1$ or $2$, the $e_2$ or $e_0$ component is impossible. For $j=0$ it gives $A=-c$, $B=c$. Thus $V_1=-c e_0+c e_1$ and $C_0=c e_0-c e_1$. Equality of actual word lengths gives $D_{1,0,c}=b-a$.

The remaining mismatch axis $i$ at height zero must satisfy
$$
 D_{0,i,c}e_i=(X_c-c)e_0+(c-Y_c)e_1 .
$$
Since $bq<c^2$, we have $X_c<c$. Thus $i=0$ and $Y_c=c$. At the low end $C_{-1}=0=-V_0$, so $B_0=R A_0$. There is no exterior or mismatch $b$ edge along $e_2$, hence $Y_a=0$. The length of $Y$ gives $Y_b=a-b$. Comparing the other components of $B_0=R A_0$ gives the asserted $D_{0,0}$.

## A metric consequence

In the two-axis case the total physical length of the imbalanced intervals on the $z$ axis is at least $ac$: their net excess includes $c$ edges of length $a$ in one bank orientation. The longest chord of the board in this direction has length $c/(a/(bq)+b/(ap))$. Indeed the positive axial unit direction $(a,b)/c$ increases $x/(bq)+y/(ap)$ at rate $(a/(bq)+b/(ap))/c$, between 0 and 1 on the board. The bound is attained by the ray from the origin. Thus there must be at least $\lceil a^2/(bq)+b/p\rceil$ imbalanced intervals on this axis. Similarly the horizontal total is at least $c(c-X_c)$, and an individual interval there has length at most $bq$. These are lower bounds on intervals and on combined lengths, not on the size of an individual interval. The slanted lower bound is 3 intervals and 1221 length units at 3431, and 2 intervals and 1505 units at 5063.

An independent enumeration of all outer word counts and all two-direction Laurent spans gives 84 arithmetic candidates at 3431 and 149 at 5063. Testing the signed integer incidence recurrence leaves respectively 15 and 30 choices, all exactly as above (one per possible $X$). Neither the identities nor this census constructs a tiling. The diagnostic requires Python 3, NumPy and SymPy; run `python3 check_two_axes.py`.

In addition, let $m$ be the least $\ell^1$ norm of a nonzero integer word difference. For a block of $n$ letters, the $n-2$ interior T-junctions are at least $(1-2/m)n$. Distinct blocks have disjoint sets of interior T-junctions. On any axis, the sum of $n$ over the imbalanced blocks is at least the norm of its aggregate difference. In the two-effective-axis case this gives
$$
 \#T\ \ge\ \left\lceil(1-2/m)(2c+a-b)\right\rceil+
 \left\lceil(1-2/m)(X_a+X_b+a-b+c-X_c)\right\rceil.
$$
At 3431 the two norms are $100$ and at least $62$, and $m=10$. At 5063 they are $108$ and at least $56$, and $m=8$. Thus the two-effective-axis alternative needs at least **130 and 123 distinct interior T-junctions**, respectively. For three or more effective axes the last numerical estimates need a separate argument.
