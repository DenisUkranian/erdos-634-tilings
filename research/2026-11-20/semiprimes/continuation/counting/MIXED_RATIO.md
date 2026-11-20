# Exact prime-product tests on ratio intervals, with no bound on the product

Write T(n) when some triangle can be partitioned into n congruent triangles. Reflections and T-junctions are allowed. Fix primes 3<p<q≤199p/100. Except for the finite set specified below, the following rules are necessary and sufficient for T(pq). In particular the rules hold for every such pair with p>7,952,292,373.

* If both primes are 1 modulo 4, the answer is yes.
* If both primes are 3 modulo 4, the answer is yes exactly when 3p<2q and both q−p and 2q−3p are positive integer squares.
* If their residues modulo 4 differ, the answer is yes exactly when 3 divides p+q and (p²−pq+q²)/3 is an integer square.

At each listed product the mixed-residue arithmetic test passes, but its unit F2 staircase fails. A tiling using different orientations or a different subdivision is a separate question. All exceptions lie in the mixed case. The [complete list through the ratio 19/10](mixed_ratio_19_10.csv) fits in 56 rows. For q≤7p/4 the complete exception list is **3431, 5063, 19367, 60023, 271151, 10206071**. Thus these explicit tests settle all semiprimes with p≥5 and q≤7p/4 above 10,206,071, including arbitrarily large counts. Squares of primes always tile by the ordinary triangular grid.

| Ratio interval | Number of exceptions | Largest exceptional product | Largest exceptional smaller prime |
|---|---:|---:|---:|
| q/p≤7/4 | 6 | 10,206,071 | 2,473 |
| q/p≤9/5 | 9 | 59,686,343 | 5,783 |
| q/p≤19/10 | 56 | 606,162,116,423 | 564,997 |
| q/p≤199/100 | 18,789 | 125,845,513,570,493,443,703 | 7,952,292,373 |

**Geometric inputs.** The [prime-pair reduction, Section 2](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md) proves the same-residue rules in q<2p and the necessity of the mixed test. The square tests for two primes equal to 3 modulo 4 use the Paliy construction. The mixed test recovers the single possible primitive tile with a=(2q−p)/3, b=(2p−q)/3, and c²=a²+ab+b². In particular a>b>0. The [unit staircase](../../staircase/SHARP_STAIRCASE.md) constructs it except when u exceeds the threshold below. Earlier work already showed that only finitely many mixed boards remain in each fixed interval q/p≤R<2. The complete exception lists and their exact maxima on these four intervals are the contribution here. They do not require the moving-bank results for q>2p.

**Finite exhaustion.** Set g=gcd(3,u−v), with coprime u>v, and use (ga,gb,gc)=(u²−v²,v(2u+v),u²+uv+v²). For distinct odd primes a,b are odd, hence v is odd and u is even. Writing x=u/v,
$$
\frac qp=f(x)=\frac{2x^2+2x-1}{x^2+4x+1},\qquad
f'(x)=\frac{6(x^2+x+1)}{(x^2+4x+1)^2}>0 .
$$
For every staircase exception we have u>4v², except that when g=3 and v≡2 modulo 3 the weaker u>4v(v−1) suffices. In particular x>4(v−1) always. Choose any integer L with f(L)>R. Every exceptional parameter satisfies
$$
 v<1+L/4,\qquad u<Lv .
$$
Thus one enumerates a finite set fixed by the ratio, with no size assumption on p, q, or N. For R=19/10 one may take L=57 and v≤15, u<855. For R=7/4 one may take L=21 and v≤5, u<105. The threshold is applied separately in its two residue cases. The factor tests then use trial division by all primes through a proven square-root bound. All comparisons at endpoints are integral.

The [replay](mixed_ratio.py) builds the entire list for any of these intervals. For the widest interval use `python3 mixed_ratio.py --wide` or `--write-wide output.csv` to export all 18,789 rows. The largest row has (p,q,u,v)=(7952292373,15825061211,88878,149). An [independent implementation](verify_mixed_ratio.py) uses the single positive cone from the [quartic parametrization](../F2_MASS.md) and SymPy for primality. Run `python3 verify_mixed_ratio.py 199/100`. The completely sorted rows, written as N,p,q,u,v in ASCII with line feed after every row and no header, have SHA-256 `c54e2541756eb1506861973d6720bef120b68c27d3a0c139bc2af14487c81b50` in both computations. The result is a criterion for every product in the displayed ranges except those listed by the method. The largest exceptional values are sharp for the staircase test itself.
