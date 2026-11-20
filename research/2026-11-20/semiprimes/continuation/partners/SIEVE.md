# Two prime factors save two logarithms in the residual upper bound

Let R(X) be the number of mixed-residue products of two distinct odd primes greater than three, at most X, whose primitive F2 arithmetic candidate lies outside the unit staircase. Then
$$
 R(X) \ll \frac{X^{3/8}}{(\log X)^2}\quad(X\ge 3).
$$
The number of primes up to Y incident to such a pair, with no size limit on the second endpoint, is consequently $O(Y^{3/4}/(\log Y)^2)$. Indeed the larger factor of an F2 product is less than twice the smaller, so every edge meeting this interval has product below $2Y^2$; each edge has two endpoints. This sharpens the earlier bound obtained by counting all parameter records in the exceptional region before requiring primality. It is an upper bound on a set of undecided candidates.

## Parameter region

Use the [ordered parameters and sharp staircase theorem](../../staircase/SHARP_STAIRCASE.md). For coprime positive u,v the two factors are
$$
 p=(u^2+4uv+v^2)/g,\qquad q=(2u^2+2uv-v^2)/g,\qquad
 g=\gcd(3,u-v).
$$
Here u>2v and q>p>u²/3; hence $u\ll X^{1/4}$. Failure of the staircase gives $u>4v^2$ or $u>4v(v-1)$, so $v\ll \sqrt u$. All such parameter pairs therefore lie in the single rectangle $1\le u\le U,\ 1\le v\le V$, where $U\asymp X^{1/4}$ and $V\asymp\sqrt U$, after rounding the sides up. We sieve the entire rectangle and retain the ordered cone only when bounding the possible small-prime exceptions.

## Sieve on the rectangle

Take $z=U^{1/25}$, treating bounded U by adjusting the implied constant. Use the primes $13\le\ell\le z$ in the two classes $1,11\bmod12$. For each such prime forbid all pairs modulo ℓ with v nonzero for which either numerator vanishes. In the variable u/v the two quadratics each have two simple roots: both discriminants are 12 and 3 is a quadratic residue. No roots coincide: the second polynomial minus twice the first is $-3(2u/v+1)$, and substituting $-1/2$ into the first gives $-3/4$. The number of forbidden classes is therefore $4(\ell-1)$. The discarded normalization g has prime factors only at 3.

Let D denote the product of the sieving primes. For squarefree d dividing D, the CRT gives $h(d)=\prod_{\ell\mid d}4(\ell-1)$ ordered pairs of residue classes forbidden at every prime of d. Put $w(d)=h(d)/d^2$. Each residue class occurs $UV/d^2+O((U+V)/d+1)$ times in the rectangle. Consequently the count forbidden at every prime of d is $UVw(d)+r(d)$, where
$$
 |r(d)|\ll 4^{\omega(d)}(U+V+d).
$$
Apply [Selberg's upper bound, equation (1)](https://people.math.harvard.edu/~elkies/M229.09/sieve.pdf) to the multiset assigning to each lattice point the product of exactly the sieving primes at which its residue class is forbidden. The number of surviving points is at most
$$
 UV/G(z)+\sum_{d\mid D,\,d\le z^2}3^{\omega(d)}|r(d)|,
 \qquad
 G(z)=\sum_{d\mid D,\,d\le z}\prod_{\ell\mid d}\frac{w(\ell)}{1-w(\ell)} .
$$
Here each sieving prime exceeds 12, so $12^{\omega(d)}\le d$ and the error is $O(U z^4+z^6)$.

To lower-bound G, restrict the Euler product to sieving primes at most $w_0=z^\eta$, for a fixed small positive η. Give each divisor d of this restricted product weight proportional to $\prod_{\ell\mid d}w(\ell)/(1-w(\ell))$. Each prime is then selected independently with probability $w(\ell)$. The expected log d is at most $4\sum_{\ell\le w_0}(\log\ell)/\ell\ll\log w_0$. Fix η small enough that this is less than half of log z for all sufficiently large z. Markov's inequality puts at least half of the total weight on $d\le z$. Thus
$$
 G(z)\ge\tfrac12\prod_{\substack{13\le\ell\le w_0\\\ell\equiv\pm1\ (12)}}(1-w(\ell))^{-1}
 \gg (\log z)^2 .
$$
Indeed $w(\ell)=4/\ell+O(\ell^{-2})$, and the reciprocal prime sum in the two indicated classes is $\tfrac12\log\log w_0+O(1)$ by Mertens' theorem in fixed progressions. The other estimate on prime logarithms follows from the ordinary Chebyshev bound by partial summation.

Finally a genuine prime pair removed by a sieve prime must have at least one factor equal to that prime. In the ordered cone this forces $p\le z$, hence $u<\sqrt{3z}$ and $v<u$. There are $O(z)$ such records. Collecting terms gives
$$
 R(X)\ll UV/(\log z)^2+Uz^4+z^6+z\ll U^{3/2}/(\log U)^2,
$$
as claimed. No distribution of simultaneous prime values of the two quadratics is assumed.
