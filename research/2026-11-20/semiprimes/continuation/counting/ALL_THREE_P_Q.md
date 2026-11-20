# All squarefree products 3pq: a constructive test and at most one unresolved partner per prime

Let 3<p<q be primes. Use the branch classification, the four unit-scale exclusions, and the finite exclusions for 15 and 231 identified in [the equal-residue theorem](THREE_PRIME_EXCLUSION.md). This theorem also uses the project proof excluding the entire adjacent BQ family, its general unit isosceles 120° exclusion for longest-edge defect one, the recorded exclusion of 105, and the positive dissection of 345. Reflections and T-junctions are allowed.

**The classification outside explicit curves.** When q<2p, a triangle admits a tiling by 3pq congruent triangles if and only if

    3p/2 < q < 2p,    3p−q and 3(2p−q) are integer squares.

When q>2p, the product 345 admits a tiling. Every other product is impossible except possibly 777 and the following two prime-partner conditions. The formulas give candidate boards. They do not establish a dissection.

| Possible remaining board | Condition on p | Equation for q |
|---|---|---|
| Unit BQ, gap three | p≡1 mod 4 | 4q=p²+18p+9 |
| Unit 120° isosceles | p≡3 mod 4, p>9 | 4q=p²+18p−27 |

Consequently there is at most one unresolved larger prime partner for every smaller p. The isolated case 777 has p=7, while the isosceles curve requires p>9. There are O(X^(1/3)) exceptional products 3pq≤X, allowing the parameters to run over all integers before testing primality. The count follows directly from q of order p². For example p=5 has candidate q=31; its former candidate q=191 is eliminated by the general unit isosceles geometric theorem. The old candidate (5,79) has gap one and is removed by the adjacent BQ result. The exceptional value 777=3·7·37 uses the reversed F4 board with tile (16,5,19).

## Proof

The accompanying equal-residue theorem handles p≡q modulo 4. In the other cases N≡1 modulo 4, and its squarefree factor 3 rules out a sum of two squares. The only classical alternatives are 3r² or 6r², neither applicable. The unit-scale residue table removes E+ (odd output 7 modulo 8), F2 (odd output 7 modulo 8), and F3 (odd output 3 modulo 8). The remaining rows are exhausted below. The argument provides the same positive square test in all prime residue classes: satisfying it constructs the tiling, so by the companion theorem no equal-residue pair passes it.

**The Paliy row.** Q=2k²−m² and P=3k²−m² are coprime and exceed one, for coprime 0<m<k. Modulo 3, Q cannot vanish, since k²+m²≡0 would force both parameters divisible by 3. Now 3/2<P/Q<2. The factorization QP=3pq can therefore only be Q=q, P=3p. Indeed Q=p gives P=3q>2Q, Q=pq gives P=3<Q, and Q=1 is impossible. Inverting gives k²=3p−q, m²=3(2p−q). Conversely the two positive roots in the stated interval satisfy 0<m<k and are coprime because a common prime square would divide Q=q. Paliy's construction gives a tiling. [Construction](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/docs/two-piece-construction.md) · [Beeson, Sections 11.3 and 11.6](https://arxiv.org/html/1206.2229v6#S11).

**The BQ row.** Here N=(k−m)(k+m)(2k²−m²) with coprime 0<m<k. Odd N forces k even and m odd. The case k−m=1 is excluded by the project's geometric adjacent BQ theorem, including its separate small counts 21 and 70. Otherwise every factor exceeds one and must be a prime. Modulo 3 the last cannot equal 3. The middle exceeds 3 except at (k,m)=(2,1), hence k−m=3. The remaining primes in increasing order are p=2k−3 and q=k²+6k−9. Substitution of k=(p+3)/2 gives 4q=p²+18p+9. In particular q>2p and p≡1 modulo 4. The adjacent step is a project manuscript input and is essential for this cubic exceptional-set bound in the stated explicit form. See [the adjacent boundary proof](inputs/bq/MIXED_BRANCH_INPUTS.md), [the interior-bank proof](inputs/bq/OFFSET.md), and the closing section of [the geometric input](inputs/I120_THEOREM.md).

**Equilateral minus, F1 and F4.** For a minus-norm triple with longer leg S and shorter leg B, put A=S−B. Its equation becomes C²=A²+AB+B², and SB=(A+B)B. This reduces E− and F1 to the same count expression, even though their boards differ. F4 gives (A+B)(2A+B). In the ordered primitive plus-norm parameters of the companion proof, A+B=u[(u+2v)/g], both factors exceeding one. The third factor B or 2A+B exceeds one as well. A unit leg cannot occur for a primitive positive plus-norm triangle because x²+x+1 lies strictly between consecutive squares for x≥1. Each of the three factors must therefore be prime and one must equal 3.

If u=3, ordering forces v=1 and the tile is (8,7,13). If (u+2v)/g=3, then g=3, u+2v=9, and the ordering u>(1+√3)v forces v=1, giving (16,5,19). Taking the odd coefficient in each order yields 105 from F1 or E−, and 345 or 777 from F4. In the remaining option B=3, the equation (2C−2A−3)(2C+2A+3)=27 forces the smaller factor to be 1 since it is strictly less than 3. Hence A=5 and B(A+B)=24 is even. The alternative 2A+B=3 would require A=B=1, which fails the norm equation. The 105 case is excluded independently; 345 has a dissection. [105 exclusion](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/n105/PROOF_N105.md) · [345 construction credited to Paliy, with Bonfioli's Lean instance](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/lean/Erdos634/Draft/N345N506.lean).

**The isosceles row with a 120° tile.** Write N=B(A+2B). In a primitive plus-norm triple 3 cannot divide A+2B. Otherwise A≡B≠0 modulo 3, and A²+AB+B²=3(B²+3Bt+3t²) for A=B+3t. Its 3-adic valuation would be one. Hence 3 divides B. The factor A+2B is larger than 2B. For B=3 the computation above gives A=5 and N=33. Otherwise B=3p and q=A+2B>6p, since B=3q or B=3pq is too large.

Set D=2A+B=2q−9p and d=2C−D. Then d(2C+D)=3B²=27p². Since D>B the larger factor exceeds 3B and 0<d<B=3p. Its only possible divisors are 1,3,9,27 or p (p²>3p). The difference of the two factors gives

    4q = 18p + 27p²/d − d.

For d=p this yields q=11p. For d=3 or 9 it forces 3|q. For d=27 this gives 4q=p²+18p−27, so reduction modulo 8 forces p≡3 modulo 4, and 27<3p gives p>9.

For d=1, the formal curve 4q=27p²+18p−1 is entirely excluded by the previously proved unit isosceles geometric theorem in [Sections 1–4 of the geometric input](inputs/I120_THEOREM.md). Write h=(B−1)/2=(3p−1)/2≥7. The displayed equation gives A=(3B²−2B−1)/4=h(3h+2), B=2h+1, and the norm gives C=3h(h+1)+1. These are exactly the tile and the target (BC,BC,B(A+2B)) in that theorem. The theorem is stated for every h≥3, with no primality hypothesis on B. Its moving-bank proof is an internal manuscript input, distinct from its corollary about semiprimes.

Both candidate curves lie beyond q=2p. The only isolated positive there is 345 outside the curves, and the F4 case 777 has p=7, outside the domain of the isosceles construction. This completes the asserted classification outside the explicit exceptions.

## One potential partner, explicitly invertible

Write χ(p)=1 for p≡1 modulo 4 and χ(p)=−1 for p≡3 modulo 4. The exceptional 777 has p=7 and q=37, which numerically satisfies the second polynomial at p=7. Its geometry is F4. Thus every potentially unresolved pair, including this one, satisfies

    q=F(p)=(p²+18p−9+18χ(p))/4.

This single function is strictly increasing on the odd integers p≥5. On stepping from p to p+2 the numerator increases by at least 4p+4, after allowing a drop of 36 in the residue-dependent constant. Consequently each prime also has at most one *smaller* possible unresolved partner. There are at most O(√Y) primes q≤Y that could have such a smaller partner, since F(p) grows quadratically.

## Prime rows fully determined by a congruence test

If p≡1 modulo 4 and p is 1 or 2 modulo 7, then 7 divides the numerator p²+18p+9. If p≡3 modulo 4 and p is 5 or 10 modulo 11, then 11 divides p²+18p−27. The possible q is larger than the dividing prime in both cases. The exceptional p=7 satisfies neither filter. Thus every larger prime partner is decided for each p in either class: apply the square test and include the isolated positive 345 when applicable. The two families of smaller primes are disjoint and have total natural density 1/6+1/10=4/15 relative to the primes, by the prime number theorem for arithmetic progressions.

In fact the set of smaller primes with *all* larger partners decided has relative natural density one. For each prime ℓ≡1 modulo 24, the discriminants of the two numerators are 288=12²·2 and 432=12²·3. Quadratic reciprocity shows that both 2 and 3 are quadratic residues modulo ℓ. Each polynomial therefore vanishes in exactly two distinct invertible residue classes modulo ℓ. For a finite set L of these primes, consider each parity class of p modulo 4 separately. Primes p with F(p) prime avoid two classes modulo every ℓ in L, apart from finitely many cases F(p)=ℓ or p=ℓ. By the Chinese remainder theorem and the prime number theorem for the fixed modulus 4 times the product of L, the upper density of such p among all primes is at most

    product over ℓ in L of (1−2/(ℓ−1)).

The reciprocal sum of primes ℓ≡1 modulo 24 diverges, so these finite products tend to zero. Here the limit in the prime-counting variable is taken before enlarging the fixed modulus. This proves the claim without assuming a prime-values conjecture for either quadratic. Combining it with the O(√Y) bound just proved shows that a density-one set of primes has every 3pq partner decided, in either order. [Prime distribution for fixed moduli and reciprocal sums, MIT Lecture 18](https://ocw.mit.edu/courses/18-785-number-theory-i-fall-2021/mit18_785f21_lec18.pdf).

The finite arithmetic inversion in replay_3pq.py verifies the claimed branch support at all 139,667 inputs 3pq≤3,000,000 with 3<p<q. The stored output in replay_3pq.txt gives the exact counts. This replay does not kernel-check the two geometric moving-bank exclusions or the antecedent case-231 argument.

## The exceptional F4 board admits no vertex-to-opposite-side seam

For 777 the only possible target and tile have sides (185,304,399) and (16,5,19). Suppose a segment made entirely of tile boundaries joins a vertex of the target to the interior of the opposite side. Each resulting triangle must be tiled. For this fixed tile the smaller possible counts are Dm², with D in {1,80,105,130,336,546,592}, by specialization of the triangle classification above. Exhausting these seven possibilities at m≤√776 gives just one pair summing to 777. Its triangles have sides (105,336,399), count 441, and (80,304,336), count 336. The latter is the exchanged F1 board with sides ab, ac, a(a+b), where a=16, b=5 and c=19. This enumeration is the antecedent vertex-seam calculation in [the earlier F4 analysis](https://github.com/DenisUkranian/erdos-634-tilings/blob/a837eb58e837132734342a53b889aade5cad723b/research/2026-11-19/next/f4/RESULT.md) and its accompanying enumeration.

The ordered plus-norm parameters are u=7,v=1,g=3. The exchanged-F1 stopped-run obstruction in [the unit F1 proof](inputs/F2_V1_PURITY.md), “Both F1 orders and all straight caps on the unit F2 board”, therefore excludes the 336 board completely. In this instance K=⌊16/7⌋=2. The geometric input forces at least three c-edges on the side ab=80. The only inventories (number of 16-, 5-, and 19-edges) summing to 80 are (0,16,0), (1,9,1), (2,2,2), (5,0,0). Thus the seam in the 777 target is impossible. A tiling with no such seam remains geometrically open. The stopped-run argument is a previous internal manuscript result and has not been verified in Lean or independently refereed.
