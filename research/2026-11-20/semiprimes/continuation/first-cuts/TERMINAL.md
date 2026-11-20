# A compulsory terminal quadrilateral behind the F4 cap

Assume a residual mixed pair of primes with $v>1$ and use the notation of [the first-cut theorem](PROOF.md) and the [transversal theorem](VIRTUAL_APEX.md). For $0\le j\le2v-1$, let $D_j,O_j$ be at distances $jhc,jha$ from $D,O$ along $DE,OU$. Let $Q_j$ be the quadrilateral $O_jD_jEU$. Thus $Q_0$ is the whole F4 complement.

**Theorem.** In every maximal straight-cut dissection of a tiled $Q_0$, some terminal piece is a $Q_j$. Its area in tile units is
$$
M_j=bq-2jL/v-j^2h^2.
$$
In particular such a leaf contains at least $M_{2v-1}$ tiles. On the first higher-denominator example $N=10{,}206{,}071$, it contains at least $266{,}076$ tiles. This theorem applies to the seventh-chord construction. It does not assert that an arbitrary F2 tiling contains the cap.

### Vertex and corner cuts

The two short sides of $Q_j$ have lengths $L_j=L+jhb$ and $ce$. Both are strictly below $ab$. For the first, $ab-L=we$, $jhb<2b^2$, $e>b/2$, and $w>4b$. Indeed $a>4b$: for $v\ge5$, $u/v>4(v-1)\ge16$, and for $v=3$, $u\ge26$ since it is even. Both imply $u/v>4+\sqrt{21}$, which is equivalent to $a>4b$ in the parametrization. The bound on $ce$ was proved for $Q_0$. All angles of $Q_j$ equal those of $Q_0$. The corner argument applies verbatim: a $60^\circ$ corner triangle needs sides at least $ab$, the angle $\pi-\alpha$ cannot be a tiled triangle corner, the $2\alpha$ candidate needs a longer side than available, and the candidates at $\alpha+2\beta$ all exceed $ce$. Thus a cut of a tiled $Q_j$ must join two opposite side interiors. A cut between its long sides is also a cut of $Q_0$ as geometry. The [transversal theorem](VIRTUAL_APEX.md) applies when $Q_0$ is tiled and the cut is part of that tiling. Its terminal-side child is then $Q_k$ with $k>j$. It remains to exclude cuts joining the two short sides for $j>0$.

### The other virtual vertex

Let $V_j$ be the intersection of the lines $O_jD_j$ and $UE$. It is a virtual apex of angle $2\beta$. Ordered from the $V_jE$ ray to the $V_jD_j$ ray, the inner triangle $V_jED_j$ is F4 with radii $(ac,cw)r$ and the outer triangle $V_jUO_j$ is F2 with radii $(C,A)r'$, where
$$
r=1-\frac{jc}{vq},\qquad r'=1-\frac{ja}{vq}.
$$
For the outer triangle, $OO_j/OU=jha/B=ja/(vq)$ and $V_jO_j$ is parallel to $VO$. For the inner one, $DD_j/DE=jhc/B=jc/(vq)$ and $V_jD_j$ is parallel to $VD$. Its geometry is a homothety about $E$. Both scales are positive by the bound on $j$. Any cut between the short sides yields a strictly intermediate virtual triangle. Its two new angles are tiled sectors. Its two radii differ from those of either reference triangle by integers: these differences are full boundary intervals of tiled children. Its chord is an integer.

Both $r,r'$ have odd reduced denominator $D=vq/\gcd(j,v)$. Here $q$ is a prime greater than $2v-1$, and $a,c,w,p$ are all coprime to $vq$. Both radii therefore have exactly denominator $D$. Applying Bezout to each primitive side triple shows that the scale $t$ of the intermediate triangle likewise has reduced denominator $D$. The three possible primitive shapes about $2\beta$ are F4, F2 and the triple-angle F3 from the [primitive side table](PROOF.md).

### The triple-angle alternative is too wide

The largest available radius divided by the smallest is at most $Ar'/(acr)=(p/c)(r'/r)$. We have $r'/r<2$. Indeed
$$
\frac{r'}r=1+\frac{j e}{vq-jc},\qquad vq-jc\ge c-3v^3/g .
$$
The sufficient inequality $2ve+3v^3/g<c$ is equivalent to $2v^2u+7v^3<u^2+uv+v^2$. For $v\ge5$ one has $u(u-2v^2)>8v^2(v-1)(v-2)>7v^3$ by $u>4v(v-1)$. For $v=3$ the difference $u^2-15u-180$ is positive at $u=26$ and strictly increases thereafter. Since $a>4b$ implies $2p<3a$ and $c<w$, it follows that $2p/c<3aw/c^2$. The F3 radii are $3aw,c^2$ up to common scale, so neither order fits.

### The two remaining shapes

Use the two normalized boundary sums in a reference frame along the first ray. For the F4 order $(ac,cw)$ the contributions per unit scale are $(a+c,c-a)$, and reversing the two radii negates both. For the F2 order $(C,A)$ they are $(a-b+c,a-b-c)$ and reversal again negates both. These follow by the directed-side formula of the transversal proof, with final radial signs $-1,-1$ because the apex has coefficients $(0,2)$. The two entries of the F4 vector have gcd two, and those of F2 are coprime. Thus their gcds are coprime to the odd denominator $D$.

Subtract the inner currents for F4, or the outer currents for F2. The differences are integral since the region between the intermediate cut and the respective reference base is one tiled child. Hence the F4 scale satisfies $t\equiv r$ or $-r\pmod1$, according to its order. The analogous F2 congruences use $r'$. In the matching order the allowed interval of scales is narrower than one since both short edge lengths are below $ab$, while the primitive radii exceed $ab$. One endpoint already realizes $r$ or $r'$, so strict interiority makes this impossible.

In the reversed order, $0<t<1$. For reversed F4 the first radius is $cw\,t<Cr'<cw$; for reversed F2 it is $A t<Cr'<A$. Since $0<r,r'<1$, this leaves $t=1-r$ or $t=1-r'$. Subtracting the squared-scale areas of the F4s gives $wq(1-2r)$, which must be an integer. Hence $v\mid 2wjc$, forcing $v\mid j$. For F2 use $pq(1-2r')$, obtaining $v\mid 2pja$ and the same conclusion. Since $1\le j<2v$, it suffices to check $j=v$. Now $r=(q-c)/q$ and $r'=w/q$. For reversed F4, $t=c/q$, so the first radius $c^2w/q$ reaches the upper endpoint $Cr'$ exactly. For reversed F2, $t=a/q$ and its second radius $c^2a/q$ falls below the lower endpoint $cw(q-c)/q$ by $c(w-c)=cd$. This rules out both.

The short-to-short case for $j=0$ is in the first-cut theorem. Follow the child containing $EU$ whenever a cut of the distinguished piece occurs. Each such cut increases $j$, so a terminal piece must be among the stated quadrilaterals in every order of cuts. The removed region has mass $(L/b+jh)^2-(L/b)^2$ by the virtual tile-similar triangles, yielding $M_j$. The displayed lower bound uses monotonicity. For the first $v=3$ example $B=1{,}126{,}671$, $h=91$, $L/v=65{,}357$ and $j=5$.
