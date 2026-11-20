# In the unit F2 board, the aligned exchange cells have no cycles

Use $H=bq$, $V=ap$ and $W=c^2$, the three side lengths of the board with vertices $0,H,V\rho$. Write $\alpha$ for the angle opposite tile side $a$. The [exchange](RHOMBUS.md) uses an elementary rhombus with sides $bc$ and included angle $\alpha$. The following bound allows any real rotation, reflection or translation, irrespective of how the rest of the board is filled.

**Theorem.** A rhombus of side $2bc$ and included angle $\alpha$ cannot fit in the F2 board. For a fixed tiling of the plane by elementary $bc$ exchange rhombi, the graph of the cells contained in the board, with adjacency along a full side, is a forest. At every parameter $a\ge2b$ at least one elementary cell fits at the explicit orientation and location of the exchange theorem.

For an axial vector $w=(x,y)$ set
$$
 g(w)=\tfrac12\bigl(|x|/H+|y|/V+|x/H+y/V|\bigr)
     =\max(|x|/H,|y|/V,|x/H+y/V|).
$$
Let $u,v$ be any Euclidean unit side vectors of a rhombus. A translated rhombus of side $L$ fits exactly when $L(g(u)+g(v))\le1$. Indeed a centered rhombus has minimum axial x coordinate $-L(|u_x|+|v_x|)/2$ and similarly for y. Translating by their negations is the smallest translation in each coordinate making both nonnegative. The maximum of $x/H+y/V$ after this translation is precisely the left-hand side.

As the rhombus rotates, each argument of an absolute value in the formula for $g$ is a sinusoid of the physical rotation angle. On an interval of fixed signs the sum $f=g(u)+g(v)>0$ satisfies $f''=-f<0$. Its minimum is attained at a sign change, when one side is parallel to a board side. We can exchange $u,v$, reverse the individual vectors without changing $g$, and reflect the angle. Thus it suffices to take $u=1,\rho,(-H+V\rho)/c^2$ and $v=us$ or $u\bar s$ for $s=(b+a\rho)/c$.

* For $u=1$, $bc\,g(u)=c/q>1/2$ because $4c^2-q^2=3b^2$.
* For $u=\rho$, both possible $v$ have $|v_x|=a/c$. Thus $bc(g(u)+g(v))\ge bc/(ap)+a/q>1/2$: here $1/2-a/q=b/(2q)$ and $2cq>ap$.
* For $u=(-H+V\rho)/c^2$, $g(u)=1/c^2$. With $v=us$, its x coordinate is $-(a+b)/c$, giving $bc\,g(v)\ge (a+b)/q>1/2$. With $v=u\bar s$, $v_x/H+v_y/V=c/(bpq)$, so $bc(g(u)+g(v))\ge b/c+c^2/(pq)>1/2$. The last inequality is $2pq>3ac$, since $pq=2c^2+3ab$ and $c>a$.

The minimum is strictly above $1/(2bc)$, proving the size bound. As $a/b\to\infty$, the reciprocal of $bc(g(u)+g(v))$ for $u=1,v=s$ tends to 2. Thus 2 is a uniform limiting constant over elongated F2 shapes, though equality is always excluded.

For the forest assertion, the set of centers of translates of a fixed elementary rhombus contained in the board is convex: each vertex gives three linear conditions on the center. In affine grid coordinates, the centers of one rhombus grid form a translate of the integer square lattice. If their side-adjacency graph contains a simple cycle, its polygonal interior contains a whole open elementary lattice square. The four vertices of that square belong to the convex hull of the cycle, hence all four centers are feasible. The four cells together form a rhombus of side $2bc$, contrary to the bound. This argument also rules out a cycle formed by only a subset of the feasible cells.

## Exact largest rhombus throughout the residual range

For $a\ge 2b$ the maximum attainable side length is
$$
 L_{\max}=\frac{bc}{b/c+c^2/(pq)}.
$$
In the sloping-side test take $u=\rho z^2$ and $v=u\bar s=z^3$. Both axial coordinates of $v$ are nonnegative: the numerators of $c^3v$ are $a^3-3ab^2-b^3$ and $3ab(a+b)$. Thus $g(v)=v_x/H+v_y/V=c/(bpq)$, and the cost $bc(g(u)+g(v))$ is exactly $f_*=b/c+c^2/(pq)$. Translating the rhombus as in the proof achieves this side length.

To see that no other candidate has smaller cost, in the horizontal case $|v_y|=a/c$ for either choice, so the cost is at least $c/q+b/p$. Subtracting $f_*$ gives $(p-c)(c^2-bq)/(pqc)>0$, since $c^2-bq=a(a-b)>0$. In the vertical case the lower bound $bc/(ap)+a/q$ exceeds $f_*$ by $b(a-b)(1/(pq)-b/(apc))>0$. Here $ac>bq$: indeed $c>a+b/2$ and $a^2+ab/2\ge 2ab+b^2$ for $a\ge2b$. For the other sloping-side orientation $b/c+(a+b)/q>f_*$ since $p(a+b)>c^2$. This finishes the comparison.
