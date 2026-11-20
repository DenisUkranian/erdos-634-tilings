# Counting distinct tile counts on unit F2 boards

For primitive positive $a>b$ with $c^2=a^2+ab+b^2$, put
$D=(a+2b)(2a+b)$. The unit F2 triangle has sides $a(a+2b),b(2a+b),c^2$
and requires $D$ congruent copies of the tile $(a,b,c)$. The arithmetic
test at scale $h$ is $N=h^2D$.

**Theorem for the entire unit F2 spectrum.** Let $U(X)$ count the distinct
integers up to $X$ occurring on a unit F2 board, and let $U_{\rm ar}(X)$
count the corresponding arithmetic candidates. Put
$$
I=\int_0^1\frac{ds}{\sqrt{(1+4s+s^2)(2+2s-s^2)}},\qquad
K_0=\frac{3I}{8\zeta(2)} .
$$
For every $\epsilon>0$,
$$
 U(X)=K_0\sqrt X+O_\epsilon(X^{3/8+\epsilon}),
 \qquad 0\le U_{\rm ar}(X)-U(X)\ll X^{3/8}.
$$
The same main term and error hold when counting only the distinct
numbers constructed by the staircase. The odd-only main term is one
third of this. The density-one coverage is a statement about distinct
unit counts passing the F2 arithmetic condition.

**Squarefree refinement.** Among distinct squarefree $D\le X$ the number of arithmetic
candidates is $(K+o(1))\sqrt X$. Both the actual unit F2 tilings, counted
by distinct numbers, and the counts realized by the constructive unit
staircase have this same asymptotic. Relative to the arithmetic candidates,
the proportion outside the staircase is $O(X^{-1/8})$. The conclusions
also hold for the odd squarefree subfamily with constant $K/3$. Here
$$
K=\frac14\int_0^1\frac{ds}{\sqrt{(1+4s+s^2)(2+2s-s^2)}}
\prod_{\ell\ge5\ {\rm prime}}\left(1-\frac{\ell^2+
[2+2(3/\ell)](\ell^2-\ell)}{\ell^4}\right).
$$
The truncated numerical estimates are $K\approx0.07908177$ and
$K/3\approx0.02636059$. The numerical estimates carry no role in the proof.

## Single polynomial for both normalizations

The primitive ordered parametrization is
$(ga,gb,gc)=(u^2-v^2,v(2u+v),u^2+uv+v^2)$, with $u/v=(a+c)/b$,
$g=\gcd(3,u-v)$ and $u>(1+\sqrt3)v$. The order can be dropped. Use a
single cone with $x>y>0$, $\gcd(x,y)=1$, $x\ne y\pmod3$ and
$$
H(x,y)=(x^2+4xy+y^2)(2x^2+2xy-y^2).
$$
For $g=1$ use $(x,y)=(u,v)$. For $g=3$ use $x=(u+2v)/3$, $y=(u-v)/3$.
Then $x^2-y^2=b$, $y(2x+y)=a$, and $x-y=v$ is prime to 3. Their gcd
is 1 since the inverse is $(u,v)=(x+2y,x-y)$. The second sector has
$1<x/y<1+\sqrt3$; the first has $x/y>1+\sqrt3$. Conversely the same
formulas recover the original ordered triple in each sector. Each $H$
equals the original $D$. Odd coefficients correspond to $x$ even, $y$ odd.
The raw quartic already excludes imprimitive pairs from squarefree values.

## Unit parameter count with a power-saving error

Let $B=X^{1/4}$. The dilated region $0<y<x$, $H(x,y)\le X$ has area
$B^2 I/2$ and perimeter $O(B)$. Its boundary consists of two rays and a
smooth compact arc after scaling. The restriction $x\ne y\pmod3$ has
density $2/3$ and excludes any common factor 3. For all other primes
remove common divisors by Möbius inversion, which gives the density
$(2/3)\prod_{\ell\ne3}(1-\ell^{-2})=3/(4\zeta(2))$. Counting residue
classes modulo 3 in the domain divided by each $d\le CB$ incurs
$O(B/d+1)$ error, and extending the density series past $CB$ costs $O(B)$.
Thus the pair count is $K_0\sqrt X+O(X^{1/4}\log(2X))$. For the odd
count restrict to the single odd-producing parity class of the three
primitive ones. Apply the orbit estimate below to count distinct values,
and subtract the upper bound on staircase failures to prove the first
theorem.

## Squarefree lattice-point count

In the scaled region $H(x,y)\le X$, $0<y<x$, both coordinates are
$O(B)$ for $B=X^{1/4}$, since $H\ge2x^4$ there. Area is $B^2$ times
one half of the displayed integral, by setting $s=y/x$. At 2, all three
primitive parity classes have $4\nmid H$; the odd-only count uses one
class. At 3, $x=y\pmod3$ gives $9\mid H$, and all other pairs have
$H=2\pmod3$. The two local densities are $3/4$ and $2/3$ respectively,
with $1/4$ at 2 for the odd-only count.

For $\ell\ge5$, there are $\ell^2$ pairs modulo $\ell^2$ with both
coordinates divisible by $\ell$. Every other solution of $\ell^2\mid H$
has $x,y$ units modulo $\ell$. In a projective chart both quadratics have
discriminant 12 up to square and no common root at these primes (their
resultant is $-27$). Thus there are $2+2(3/\ell)$ distinct roots modulo
$\ell$, lifting uniquely by simplicity modulo $\ell^2$, and
$\ell^2-\ell$ unit scalings per root. This gives the local factors.
Finite sets of sieving primes give the corresponding density by lattice
counting in residue classes in this bounded region and the Chinese
remainder theorem.

For completeness, nonprimitive pairs with a common prime $\ell>Y$
contribute $O(B^2/Y)$ by summing $\lfloor CB/\ell\rfloor^2$.
For primitive pairs a large square divisor must occur in one of the
quadratic factors, so $\ell=O(B)$. For each fixed root modulo $\ell^2$
the reduced rational slopes $y/x\in(0,1)$ of distinct primitive pairs
are separated by at least $\ell^2/(C B)^2$, by taking determinants.
There are at most four roots. The contribution of all primes $\ell>Y$ is
$O(B+B^2/Y)=o_Y(B^2)+O(B^2/Y)$. This proves the infinite product
asymptotic by taking $B$ then $Y$ to infinity. Each factor is positive
and their defects have finite sum.

## Counting distinct integers

The four projective roots in the order
$-2-\sqrt3,-2+\sqrt3,(-1-\sqrt3)/2,(-1+\sqrt3)/2$ have cross ratio
$-1/3$. Its six cross-ratio transforms are distinct, so precisely the
four permutations of the Klein four group come from transformations of
the root set. Representatives in coordinates $(x,y)$ are the identity,
$(-x-2y,2x+y)$, $(-x,x+y)$, and $(-x-2y,-x+y)$. Substitution in $H$
gives multipliers $1,9,1,9$ respectively. No nonzero rational scalar
has fourth power $1/9$. The exact rational automorphisms are therefore
$\pm I$ and $\pm(x,y)\mapsto(-x,x+y)$. Only the identity can send
a point in the positive cone to another point of that cone.

We count repeated representations within our positive cone. The two
pairs $x,y$ and $z,w$ both have coordinates $O(X^{1/4})$ and give
a rational point on the smooth projective quartic surface
$H(x,y)=H(z,w)$. Smoothness follows because the gradient of a binary
form with distinct roots has no nonzero simultaneous zero. The number
of rational projective points of height at most $B$ off the lines
is $O_\epsilon(B^{3/2+\epsilon})$ by Stewart and Xiao, equation
(2.5), using $d=4$. Their surface theorem applies in the bounded-height
box before the large-coordinate tail of their general representation
estimate. The quadruple here is primitive since its first pair is.
The positive cone fixes its sign.

A rational line on the surface with nonzero $H$ at the point in
question must project with rank two to each of the two coordinate
pairs. If the two ranks were one, the form on one constant direction
would give a multiple of one fourth power and on the other a multiple
of an independent fourth power; equality forces both zero. If just
one rank were two, its separable quartic would have to equal a fourth
power, also impossible. Rank zero forces $H=0$. A rank-two projection
on both sides expresses the line as the graph of an invertible rational
matrix, necessarily preserving $H$ exactly. Thus no rational line
produces a distinct cone pair. The surface has only finitely many
geometric lines (also noted for curves of degree at most $d-2$ in the
same source). Each nonrational line contains at most one rational
projective point, since two rational points span a rational line.
The total loss from multiplicities is therefore
$O_\epsilon(X^{3/8+\epsilon})$ parameter pairs. This argument concerns
only repetitions between two *in-cone* representations. The
normalization by a single integral quartic is needed before applying it.
[Stewart and Xiao, Math. Ann. 375 (2019)](https://doi.org/10.1007/s00208-019-01855-y)
· [Preprint, §2, equation (2.5), pp. 9–10](https://arxiv.org/pdf/1605.03427).

## Geometry at unit scale

Use the project's unit staircase. In ordered parameters the unit staircase fails only
for $u>4v^2$, or $u>4v(v-1)$ in the exceptional residue class.
Since $D>u^4/8$ in the ordered cone, the residual records satisfy
$u=O(X^{1/4})$ and $v=O(\sqrt u+1)$. Their number is $O(X^{3/8})$.
This is also an upper bound on the number of distinct integers missed,
including after squarefreeness or oddness restrictions. Combined with the
positive leading constant it proves the asserted fraction for unit boards.
All odd unit values here are $7\pmod8$ and cannot be sums of two squares.

The geometric input is the [sharp unit staircase](../staircase/SHARP_STAIRCASE.md). The [numerical replay](check_squarefree_mass.py) independently checks the arithmetic in finite ranges. The squarefree theorem makes no lower-bound claim after requiring both F2 factors to be primes.
