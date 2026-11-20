# Exactly when a product of two primes and its triple are both tile counts

Write T(n) if at least one nondegenerate triangle admits a dissection into n congruent triangles, with reflections and T-junctions allowed. The triangles and tiles used in T(n) and T(3n) may be completely different.

**Theorem.** For any two primes p and q, including 2, 3 and repeated primes,
$$
 T(pq)\ \text{and}\ T(3pq)
 \quad\Longleftrightarrow\quad
 p=q\quad\text{or}\quad \{p,q\}=\{2,3\}.
$$
In particular, for every mixed-residue F2 arithmetic candidate, the triple is impossible even if the original unit board turns out to be untileable. This gives a negative answer at three times every unresolved semiprime in this branch. Its converse would not give an answer at the original count.

## The arithmetic obstruction

Let a>b be coprime positive integers such that c²=a²+ab+b². Suppose p=a+2b is a power of a prime l>3. Then **b and a+5b cannot both be squares**. There is no primality assumption on 2a+b.

Suppose otherwise. Write b=s² and a+5b=t². Consequently
$$
 t^2=p+3s^2,\qquad c^2=p^2-3ps^2+3s^4.
$$
Since a>b, we have p>3s². Put U=ct and V=s(p−3s²). Direct multiplication gives
$$
 (U-V)(U+V)=p^2(p-s^2).
$$
Both factors are positive because U²>V² and U,V>0. Also c<p, t<√(2p), and s<√(p/3). Hence
$$
 U+V<p^{3/2}(\sqrt2+1/\sqrt3)<2p^{3/2}<p^2.
$$
The common divisor of U−V and U+V divides 2V. Since gcd(p,s)=1 and l>3, we have l∤2V. Thus at most one factor contains l, and that factor must be divisible by the entire p². Neither factor reaches p². This proves the obstruction.

**An exact positive control outside the prime hypothesis.** Take (a,b,c)=(6319,1521,7201). Here b=39², a+5b=118², p=9361=11·23·37 and q=14159 is prime. The unit F2 staircase works at (u,v,g)=(80,9,1), since 80≤4·9². The Paliy construction works at (k,m)=(118,117), since 2k²−m²=q and 3k²−m²=3p. Hence both 132,542,399 and 397,627,197 really are tile counts. The smaller is squarefree with four prime factors. This also gives a direct check on the signs and the geometric meaning of the obstruction.

## Applying it to the original geometry

Assume 3<p<q.

* If p and q have the same residue modulo 4, then 3pq is squarefree, divisible by 3, and equal to 3 modulo 4. The [equal-residue theorem](counting/THREE_PRIME_EXCLUSION.md) excludes every such triple. Its only exceptional arithmetic equilateral candidate with three distinct primes is 231. The associated two position certificates were replayed with the [deposited verifier](https://github.com/DenisUkranian/erdos-634-tilings/tree/6c0a28e1902062ef661413427560960e210dc693/research/2026-11-19/nov19/equilateral231/cert); [replay output](REPLAY.md). The correctness of the preceding geometric reduction is a separate input.
* Suppose p and q have opposite residues modulo 4. For T(pq), [the primitive prime-pair reduction, §2](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md) leaves only F2. Indeed the odd BQ, QP and isosceles product coefficients are 1 modulo 4. The equilateral semiprime norm test has no candidate for p,q>3. The surviving F2 equations are p=a+2b and q=2a+b with a>b>0 coprime, c²=a²+ab+b², q<2p and pq=7 modulo 8. On precisely this sector our [direct multiplier-three reduction](counting/F2_TRIPLES.md) gives T(3pq) only if b and a+5b are both squares. The arithmetic obstruction excludes their coexistence. This implication makes no assumption on filling a prescribed quadrilateral or pentagon, and uses neither moving-bank manuscript exclusion in the longer general 3pq classification.

If p=3<q, the [established 3q exclusion](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md) applies. It also follows directly from the table. For q=1 modulo 4 use the equal-residue theorem for squarefree counts with at most three prime factors divisible by 3. For q=3 modulo 4, the odd count 3q is 1 modulo 4. The classical forms cannot give it. In the norm rows the only possibilities are E−, F1, F4 and the isosceles coefficient B(A+2B). E− reduces to F1 by taking A to be the difference of the two legs. F1 and F4 contain the composite factor A+B and another factor greater than one, as proved in the [three-prime reduction](counting/ALL_THREE_P_Q.md). In the isosceles row, 3 cannot divide A+2B by the primitive norm; hence B=3, which forces A=5 and q=11. Indeed (2c−2A−3)(2c+2A+3)=27 and the smaller factor is positive and less than 3. For BQ, 3∤Q and Q>k²−m²>1, so k²−m²=3, Q=q, giving 21. For QP one has 3∤Q and P>Q>3, impossible. The two remaining counts 21 and 33 are excluded in [Bonfioli's spectrum through 200](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_primes_and_N200.tex).

If p=2 and q>3 is 3 modulo 4, the count 2q is 6 modulo 8. Besides F3 (necessarily divisible by 3), only BQ and QP could supply it, and each is a product of two factors greater than one. BQ would require its smaller factor k²−m² to be 2, impossible for a difference of squares. The smaller QP factor exceeds k²≥4. The classical two-square test fails at q. This excludes T(2q). For q=1 modulo 4, the count 6q is 6 modulo 8. The squarefree table leaves only BQ, QP and F3, after the integral scale-one exclusions. In BQ write B=k²−m² and Q=2k²−m² for coprime k>m. If B is even, both k,m are odd and B is divisible by 8. Otherwise Q must be even, k is odd and m even, 3∤Q and Q>k²≥9. Thus Q=2q and B=3, whose only solution k=2,m=1 has the wrong parity. In QP, with P=3k²−m², one has Q>1, 3∤Q and Q<P. If Q is even, the same argument gives Q=2q and P=3. If Q is odd then Q=q and P=6; parity forces k,m odd, k≥3, so P>2k²≥18. In F3 the coefficient divided by 3 is (a+b)(a+2b). Its first factor is composite by the primitive norm parametrization and its second is greater than one, whereas 2q has just two prime factors. The classical counts cannot give squarefree 6q: its prime 3 occurs to the first power and it exceeds 6. This completes the negative cases. Sources for the preliminary small-prime rules and the coefficient table are [the prime-pair reduction](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md) and [the uniform reduction, §§3–5](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-reduction/PROOF.md).

For p=q the ordinary p-by-p triangular grid gives p² tiles. Subdivide each of the three congruent triangles joining an equilateral triangle's centroid to its vertices by the same grid to obtain 3p². For the pair 2,3, the three medians of an equilateral triangle give 6 congruent tiles. Subdividing the two halves of an isosceles triangle by a 3-by-3 grid gives 18. These constructions prove the converse.

The root identity and the finite prime-pair audit are reproducible with [check_simultaneous.py](check_simultaneous.py). The universal proof uses the stated branch classification and individual geometric inputs. It does not decide by itself which member of a general remaining pair is tileable, and it is not a Lean formalization or an external review.
