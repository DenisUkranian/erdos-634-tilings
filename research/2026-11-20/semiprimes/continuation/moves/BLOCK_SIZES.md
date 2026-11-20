# The least possible size of a multiplicity mismatch

For an internal contact block, its two banks are words in the tile side lengths $a,b,c$. A block is maximal between successive shared bank endpoints inside a straight run, so that no point in its relative interior is an endpoint on both banks. Write $w=(x,y,z)$ for the signed difference of the three multiplicities. Then $ax+by+cz=0$. Call the block imbalanced when $w$ is nonzero. The short lengths have the primitive parametrization
$$
(a,b,c)=(u^2-v^2,\ v(2u+v),\ u^2+uv+v^2)/g,\qquad
g=\gcd(3,u-v),
$$
where $u>v>0$ are coprime. Write $D=u^2+uv+v^2$.

**Count theorem.** Every imbalanced block contains at least $m-2$ distinct T-junctions in its relative interior, where
$$
m=\begin{cases}u+2v &g=1,\\u &g=3.\end{cases}
$$
This value of $m$ is the exact minimum of the $\ell^1$ norm of a nonzero integer relation. The proof makes no claim that a shortest pair of bank words occurs in a full tiling.

Indeed put $R=(v,-u,v)$ and $S=(u+v,v,-u)$. Their cross product is $g(a,b,c)$, so their integer span has index $g$ in the primitive normal's relation lattice (equivalently, extend a Bezout vector for $a,b,c$ to a covolume computation). At $g=3$, $(R+S)/3$ is integral, so $R,(R+S)/3$ generate the relation lattice. For $w=iR+jS$ one has
$$
Di=v x-(u+v)y,\qquad Dj=u x+v y .
$$
If $g=1$ and $\|w\|_1<u+2v$, these identities force $|i|,|j|<2$, since $(u+v)(u+2v)<2D$. The only nonzero possibilities up to sign are $R,S,R+S,R-S$; their norms are $u+2v,2(u+v),3u,3u+2v$. If $g=3$ and $\|w\|_1<u$, both coefficients are strictly between $-1$ and $1$, with $3i,3j$ integral and $i-j$ integral. Up to sign the nonzero possibilities are $(R+S)/3,(R-2S)/3,(S-2R)/3,2(R+S)/3$. The first has norm $u$, the others have norms $(5u+4v)/3,(4u+2v)/3,2u$. Hence the stated minima are attained as integer relations. The two words have at least $\|w\|_1$ letters in total, so together they have at least $m-2$ interior endpoints. Each is counted only once by the definition of the block and is a T-junction.

**Metric theorem.** If $u\ge6v$, each imbalanced block has physical length $M\ge ub=v(a+c)$. Every imbalanced block shorter than $ac/u$ has $w=kR$ for a nonzero integer $k$. At the shortest possible length $ub$, one bank uses $u$ sides of length $b$ and the other bank uses $v$ sides of length $a$ and $v$ of length $c$.

To see this, the weighted positive and negative parts of the signed relation are both at most $M$. Because $u/a\ge v/b$ and the coefficients $u,v$ are positive, $|u x+v y|\le (u/a)M$. If $j\ne0$, $|j|\ge1/g$ gives $M\ge Da/(gu)=ac/u$. This exceeds $ub$ at $u\ge6v$, since
$$
g(aD-3u^2b)=u^4-5u^3v-3u^2v^2-uv^3-v^4>0
$$
(the first two powers leave at least $u^3v$). If $j=0$ then $i$ is integral and $M\ge |i|ub$. Equality $M=ub$ requires $|i|=1$ and no matching letters on the banks.

| Unit count | $(a,b,c)$ | $(u,v,g)$ | $m$ | T-junctions in each imbalanced block | Least possible length | Least integer length if $w$ is independent of $R$ |
|---:|---|---|---:|---:|---:|---:|
| 3431 | 33,7,37 | 10,1,3 | 10 | 8 | 70 | 123 |
| 5063 | 35,13,43 | 6,1,1 | 8 | 6 | 78 | 251 |

The count and metric minima need not be reached by the same block. The unit-count rows at 3431 and 5063 come from the original whole board. If at least two imbalanced blocks are proved necessary there, their internal T-junctions count separately: a T-junction in the interior of an atomic block is traversed straight through by a bank side, and no transverse contact can continue through that junction on both sides of it.
