# Almost every prime has only classical partners

Call a count classical if it is a sum of two integer squares (zero allowed), three times a square or six times a square. All such counts occur. Let T(n) mean unrestricted tileability of some triangle. Then
$$
 \#\{P\le Y : P\text{ prime},\ \exists Q\text{ prime},\ T(PQ)
                  \text{ and }PQ\text{ nonclassical}\}
 \ll Y/(\log Y)^2 \qquad(Y\ge3).
$$
The other prime Q is unrestricted in size. For every P outside this exceptional set, its entire row of products with prime Q follows the classical rule. The exceptional set has relative density zero among primes. Furthermore the number of distinct nonclassical tileable semiprimes at most X is $O(\sqrt X/(\log X)^2)$.

We use only the [semiprime geometric overlist, Sections 1–3](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md). A more recent exclusion of some rows would leave the argument valid.

A repeated prime gives a square. Fixing the smaller factor at 2 or 3 produces only finitely many nonclassical candidates by the large-prime-factor theorem in Section 3 of the overlist. For distinct primes $3<p<q<2p$ all nonclassical possibilities come from F2 or Paliy. If one endpoint is at most Y, then $p\le Y$.

* For F2, the proof in [SIEVE.md](SIEVE.md) without the failed-staircase condition puts the parameters in a square box of side $U\asymp\sqrt Y$, since $p>u^2/3$ and $v<u$. Its local classes, Selberg lower bound and small-factor estimate are unchanged. For sufficiently small fixed κ, the error $O(Uz^4+z^6)$ with $z=U^\kappa$ is negligible against $U^2/(\log U)^2$.
* For Paliy, write $p=2v^2-u^2$, $q=3v^2-u^2$, $0<u<v$. Since $p>v^2$, the parameters also fit in such a square. At a prime ℓ≥13 consider the forbidden classes with v nonzero at which at least one factor vanishes. Dividing by v² gives the equations $r^2=2,3$. They have disjoint solutions; in total there are $k_\ell=2+(2/\ell)+(3/\ell)$ roots, where parentheses denote Legendre symbols. Take the primes with $k_\ell>0$. There are $k_\ell(\ell-1)$ forbidden pairs, at most $4(\ell-1)$. The rectangle error is bounded exactly as in the F2 sieve. Each of the two nonprincipal real characters modulo 8 and 12 has mean zero over reduced classes modulo 24. Mertens' theorem in these fixed classes therefore gives $\sum_{\ell\le w}k_\ell/\ell=2\log\log w+O(1)$. The Euler truncation proof gives the same two logarithms. Exceptions in which a true prime factor is at most z satisfy $v<\sqrt z$ and number $O(z)$.

Both shape lists therefore contribute $O(Y/(\log Y)^2)$ pairs meeting the endpoint bound. A pair contains at most two endpoints.

For $q>2p$ the older necessary overlist leaves only three polynomials:
$$
 4q=f(p),\qquad f(t)\in\{t^2+6t+1,\ 3t^2+6t-1,\ t^2+6t-3\}.
$$
All larger endpoints at most Y on these curves arise from $p\ll\sqrt Y$, giving $O(\sqrt Y)$ possible endpoints. To bound smaller endpoints $p\le Y$ on one curve, sieve $1\le t\le Y$ simultaneously for primality of t and f(t)/4. At every prime ℓ≥13 forbid the class t=0 and the roots of f modulo ℓ. These are disjoint. The discriminants of the three quadratics are respectively 32,48,48. Thus the total count of forbidden classes is $2+(2/\ell)$ for the first polynomial and $2+(3/\ell)$ for either of the last two. This is at most 3 and has mean 2 in the same reciprocal-prime sense. For squarefree d the CRT gives at most $3^{\omega(d)}$ forbidden residues simultaneously and a counting error of that size. The Selberg remainder is bounded by $\sum_{d\le z^2}9^{\omega(d)}\ll z^4$ since all sieving primes exceed 9. The lower bound for G and the two factors of log follow as before, using $z=Y^{1/25}$. A genuine prime solution removed by sieving has p or q at most z, hence p at most z. This gives $O(Y/(\log Y)^2)$ possible smaller endpoints for each polynomial.

Finally if $pq\le X$ and $p<q<2p$, the smaller endpoint is at most $\sqrt X$; the square-box proof already bounds **pairs** meeting that cutoff. For $q>2p$ the polynomials force $p\ll X^{1/3}$, with at most three partners per smaller prime on this list. The resulting two contributions give the asserted bound for distinct nonclassical semiprimes. The analytic input is only a standard upper-bound sieve and prime distribution in fixed arithmetic progressions. The estimates make no lower-bound assertion for simultaneous prime values.
