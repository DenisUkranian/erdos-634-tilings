# The scale spectrum of integral signed triangle tilings

Fix a nondegenerate triangle $T$ and one tile $K$. The set of allowed placements of $K$ is closed under translations and half-turns. A signed tiling means equality almost everywhere of indicators with a finite integral linear combination of permitted tile indicators. Placements may extend beyond the target.

**Theorem.** The positive integer scales at which $T$ has a signed tiling form either the empty set or $d\mathbb N$ for some $d\ge1$. More specifically, given signed tilings at any finitely many scales, there is a signed tiling at their greatest common divisor. This holds also when $K$ is an arbitrary bounded measurable tile. The conclusion concerns signed tilings with unrestricted translations.

### Reduction to a Laurent module

Replace $T$ by the triangle at the greatest common divisor of the given scales. Write $I$ for the rescaled list, so $\gcd I=1$, and take vertices $0,u,v$ for this new triangle. Let $U$ be its indicator and $D$ the indicator of the triangle $u,v,u+v$. The standard triangular grid gives disjoint interiors to all the lattice translates of the two unit cells. Thus their indicators form a free rank-two module over $R=\mathbb Z[X^{\pm1},Y^{\pm1}]$, with $X,Y$ the translations by $u,v$. We work in the coefficient module $R^2$ for this grid. The tiles $K$ themselves may have arbitrary positions and need not lie on its grid.

Let $v_n$ be the coefficient column of the triangle $nT$ in these two generators. Let $w_n$ be the coefficient column of its half-turn image under $z\mapsto n(u+v)-z$. This image is the other half of the parallelogram with vertices $0,nu,nv,n(u+v)$. For every $n\in I$, both columns represent regions having signed tilings. We show that these columns generate $R^2$.

### The three boundary rows

For a unit cell sum, take its oriented boundary as a sum of lattice translates of three directed edges. Use $0\to u,\ 0\to v,\ u\to v$ as their origins and orientations. Orient $U$ around $0,u,v$ and $D$ around $u,u+v,v$. The boundary map on grid columns is

$$
J=\begin{pmatrix}1&-Y\\-1&X\\1&-1\end{pmatrix}.
$$

Writing
$$
A_n=\sum_{i=0}^{n-1} X^i,\qquad B_n=\sum_{i=0}^{n-1} Y^i,\qquad
C_n=\sum_{i=0}^{n-1} X^{n-1-i}Y^i,
$$
summing unit edges on the three sides gives
$$
Jv_n=(A_n,-B_n,C_n)^t,\qquad
Jw_n=(-Y^nA_n,X^nB_n,-C_n)^t .
$$

### Excluding every simultaneous rank drop

Let $M$ be the two-row matrix of the columns $v_n,w_n$ for $n\in I$. If its $2\times2$ minors generated a proper ideal in $R$, they would all lie in a maximal ideal. Reduce modulo that ideal. The resulting coefficient field has nonzero elements $x,y$ as images of $X,Y$, and all columns of $M$, hence all columns of $JM$, span at most one dimension.

If $x=y=1$, the integer cell counts in $v_n$ are $n(n+1)/2,n(n-1)/2$, and $w_n$ has the opposite order. Before reduction their determinant is $n^3$. It is nonzero in the field for some $n\in I$ because $\gcd I=1$. This argument also works in characteristic two, without dividing in the residue field.

Suppose at least one of $x,y$ differs from one. The three minors of the two boundary columns at scale $n$, in row pairs $(1,2),(1,3),(2,3)$, are
$$
 A_nB_nC_n(x-y),\quad A_nB_nC_n(y-1),\quad A_nB_nC_n(1-x).
$$
They all vanish, forcing $A_nB_nC_n=0$ for every $n\in I$.

None of the three particular row coordinates can vanish for all $n\in I$. For the first row, if $x\ne1$ then $A_n=0$ implies $x^n=1$, incompatible with gcd one for all $n$. If $x=1$, then $A_n=n$ in the field, again nonzero for some $n$. The second row is the same with $y$. For the third use $C_n=y^{n-1}\sum_{i=0}^{n-1}(x/y)^i$ and $y\ne0$.

In particular some ordinary column $Jv_n$ is nonzero. It has at least one zero coordinate by the vanishing product. Every $Jv_m$ must be a scalar multiple of that nonzero column. The same coordinate would then vanish for all $m\in I$, a contradiction.

The minors therefore generate the unit ideal in $R$. For each $2\times2$ submatrix with determinant $\delta$, the adjugate identity shows that $\delta (1,0)^t$ and $\delta(0,1)^t$ belong to the column module. An $R$-linear combination of the determinants equals one, so both unit columns belong to the module. Its Laurent coefficients are finite integral sums of translations. This constructs an integral signed representation of $U$ from translated copies of the two source orientations, which have signed tilings by $K$.

### Consequences

This proves gcd closure. Conversely any positive integer multiple of a signed-tileable scale is signed-tileable: subdivide into the ordinary grid of up and down copies at the given scale, and substitute the signed tiling or its half-turn. If a signed scale exists, let $d$ be the least one. Its gcd with every other one is also a signed scale, so by minimality it equals $d$. This proves the claimed description of the spectrum.

For the residual semiprime F2 boards the ordinary large-scale constructions imply $d=1$. The [three-consecutive-scale identity and exact checks for the two controls](SIGNED_TILINGS.md) also give direct certificates without ideal computation. The proof allows signed cancellations across the boundary. Neither that cancellation nor the gcd conclusion transfers automatically to ordinary tileability.
