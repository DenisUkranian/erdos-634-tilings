# The permissible directions in the seventh cap's complement

Use the notation and hypotheses of [the first-cut theorem](PROOF.md), with $v>1$. Its F4 complement has vertices $O,D,E,U$ in cyclic order, equal long sides $DE,OU$ of length $B=bq$, and two short sides $OD,EU$. The theorem shows that any proper cut of a tiled complement joins the two equal long sides.

**Theorem.** Every such cut is parallel to $OD$. Its endpoints along $DE,OU$, measured from $D,O$, are at distances $(jhc,jha)$ with $1\le j\le2v-1$, where $h=b/v$. These are necessary positions. The proof does not assert that the two resulting pieces are tileable. The direction result allows arbitrary internal tile orientations and T-junctions.

### The virtual apex and the denominator

The rays $DE$ and $OU$ meet behind $D,O$ at $P=-(aL/b)\rho$. Their angle is $\beta$. Write $t_0=L/b$ with $L=ad-be=ab-we$ as in the first-cut proof. The inner triangle has
$$
PD=ct_0,\quad PO=at_0,\quad DO=bt_0.
$$
For the outer triangle $PEU$, the ordered rays have respective lengths $(e/b)ap,(e/b)cw$ and its base is $ce$. For example, $PE=ct_0+B$, and the base angles are $\alpha+2\beta,2\alpha$. The primitive shape follows from the $2\alpha$ table.

The reduced denominator of $t_0$ is exactly $h$. Indeed $v\mid L$ and $L/v\equiv a(u-v)/g\pmod h$. The integers $(u-v)/g$ and $h=(2u+v)/g$ are coprime. Any common prime before division divides $3$ or $v$. Coprimality eliminates a prime of $v$. If $3\mid u-v$, the common power of 3 in $u-v$ and $2u+v=2(u-v)+3v$ is exactly 3. Consequently $\gcd(L/v,h)=1$. Also $\gcd(ac,h)=1$.

Given a proposed chord across the two long sides, extend its endpoints back along the rays to $P$, making a virtual triangle with ordered ray lengths $tx,ty$ and base $tk$. Here $(x,y,k)$ is its primitive integral side triple and $t$ its rational scale. Both radii differ from $ct_0,at_0$ by integers, and therefore have denominator exactly $h$. The chord itself has integer length. Hence $t=m/h$ in lowest terms: multiplying the three lengths by $h$ gives integers, and Bezout applied to $x,y,k$ shows $ht\in\mathbb Z$. The first radius forces $h$ to divide the denominator. Thus $h\mid k$.

### All virtual triangles and their boundary sums

The other two angles of the virtual triangle are sectors of the tiled inner piece at the two new endpoints. Their coefficient pairs sum to $(3,2)$, since the remaining angle at $P$ is $\beta$. This gives exactly five unordered pairs, including the two types whose chord fails $h\mid k$.

| Pair at the chord | Primitive chord $k$ opposite $\beta$ | Other sides |
|---|---:|---|
| $\beta,3\alpha+\beta$ | $c$ | $c,q$ |
| $2\beta,3\alpha$ | $c^2$ | $cq,3aw$ |
| $\alpha,2\alpha+2\beta$ | $b$ | $c,a$ |
| $\alpha+\beta,2\alpha+\beta$ | $b$ | $c,w$ |
| $\alpha+2\beta,2\alpha$ | $bc$ | $ap,cw$ |

The sine rule gives this table, and the gcd calculations of the first-cut proof ensure primitivity. Since $\gcd(h,c)=1$, the first two rows are impossible. For the remaining possibilities, we compute the two additive boundary sums, divided respectively by $a-b-c$ and $a-b+c$, using the positive ray $PD$ as reference axis. For instance if the first chord endpoint angle is $i\alpha+j\beta$, the directed edges of a counterclockwise triangle are its first radial segment, the chord after a turn $(3-i)\alpha+(3-j)\beta$, and the last radial segment directed back toward $P$. The normalized sums **per unit scale** are as follows.

| $x,y,k$ in the ordered rays | Ordinary | Alternating |
|---|---:|---:|
| $c,a,b$ | $-1$ | $1$ |
| $a,c,b$ | $1$ | $1$ |
| $c,w,b$ | $(c-b)/a$ | $(c+b)/a$ |
| $w,c,b$ | $(b-c)/a$ | $(c+b)/a$ |
| $ap,cw,bc$ | $b-c$ | $b+c$ |
| $cw,ap,bc$ | $c-b$ | $b+c$ |

The reference change is a legal direction rotation, so it changes the two signs for a unit tile at most. The region between the virtual triangle and the inner triangle is one actual tiled child. Subtract $(-t_0,t_0)$, the currents of the inner triangle, from $t$ times a row of the table. Both differences must be integers. Its area in tile units must also be an integer. These additivity statements need no tiling of the virtual triangle at $P$.

### Eliminating five orders

For row two the two differences are $t+t_0,t-t_0$. Their difference $2t_0$ is nonintegral. For rows three and six the sum of the two differences is $2ct/a$ and $2ct$ respectively. Neither can be integral since $t=m/h$ is reduced, $h$ is odd, $h>1$ and $\gcd(c,h)=1$.

In row five the second difference requires $(b+c)t-t_0\in\mathbb Z$. The outer boundary at scale $e/b$ obeys this same congruence by $(b+c)e-L=b(b+2e)$. Because $\gcd(h,b+c)=1$, it follows that $t-e/b$ is an integer. The allowed range of scale on either ray has width less than one, since $B<cw$. The outer boundary is its upper endpoint on that ray, so no strictly internal solution exists.

In row four the sum requires $2bt/a\in\mathbb Z$. Since $b=vh$, $a$ is odd and $\gcd(a,v)=1$, write $t=a k'/h$ for an integer $k'>0$. The second sum now gives $ck'\equiv L/v\pmod h$. It forces $k'\equiv e/v\pmod h$, because $c\equiv-a\pmod h$ and $(u-v)/g+(u+2v)/g=h$. The upper endpoint on the $PU$ ray gives $ct<cwe/b$. We have $e/b=(u+2v)/(2u+v)\le10/17<2/3$ and $w/a\le3/2$, thus $0<t<a$ and $0<k'<h$. Since $0<e/v<h$, we get $t=ae/b$. The virtual F1 has mass $t^2 w/a$ and the inner tile-similar triangle has mass $t_0^2$. Their difference can be integral only if
$$
b^2\mid awe^2-L^2\quad\Longrightarrow\quad
b\mid we(2a-e),
$$
using $L=ab-we$. Modulo $h$ the last expression equals $-8a^3$, since $e=c-a\equiv-2a$ and $w\equiv a$. This is a unit modulo odd $h>1$, a contradiction.

Only row one remains. Its currents force $n=t-t_0\in\mathbb Z$ and strict containment gives $n>0$. The mass difference is $2t_0n+n^2$. Its integrality and the odd denominator give $h\mid n$. Thus $n=jh$ and the cut is a translate parallel to $OD$, with the offsets stated above. Since $jhc<B$, we have
$$
j< vq/c = 2v-\frac{3v^3}{u^2+uv+v^2}.
$$
The subtracted fraction lies strictly between zero and one by $u>4v(v-1)$ and $v\ge3$. This proves $j\le2v-1$.

Following these cuts through a whole dissection forces a [terminal quadrilateral with an explicit area bound](TERMINAL.md).
