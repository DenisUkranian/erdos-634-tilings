# Audit of the prime-count consequence

29 September 2026. Scope: the prime-count subproblem of Erdős #634. This note audits the passage from the two new scale-one exclusion theorems to a classification of prime counts. It does not claim a classification for all integers N, external refereeing, formal verification, or research priority.

## Conclusion and its exact dependence

**Theorem, under the inputs below.** For a prime p, there exists a triangle dissectible into p congruent triangles if and only if

$$
p=2,\qquad p=3,\qquad\text{or}\qquad p\equiv1\pmod4.
$$

The only new geometric inputs are the two scale-one exclusions in `prime-case-candidate.md`, which includes the W proof as an appendix. The independent W manuscript is `prime-case-candidate.md (W appendix)`. The present audit takes those complete proofs as inputs; it checks their place in the exhaustive classification, rather than repeating their geometric review.

The global deduction passes this audit. All tilings here allow T-junctions; an edge-to-edge assumption is not added.

## Version-controlled outside inputs

| Input | Exact source and use |
|---|---|
| Shape classification | M. Laczkovich, *Tilings of triangles*, Discrete Mathematics 140 (1995), 79–94, [DOI](https://doi.org/10.1016/0012-365X(93)E0176-5), Theorems 4.1, 5.1, 5.3. Its isosceles specialization is written explicitly in Beeson [1206.1974v7](https://arxiv.org/html/1206.1974v7), Theorem 3.1 and Table 1. The non-isosceles specialization is restated in [2607.23453v1](https://arxiv.org/pdf/2607.23453v1), Theorems 6 and 9; independently compare Table 1 of [2604.01314v1](https://arxiv.org/pdf/2604.01314v1). |
| Reptilings | S. L. Snover, C. Waiveris, J. K. Williams, *Rep-tiling for triangles*, Discrete Mathematics 91 (1991), 193–200, [DOI](https://doi.org/10.1016/0012-365X(91)90110-N); also [1206.1974v7](https://arxiv.org/html/1206.1974v7), Theorem 2.1. |
| Isosceles right-tile and double-angle branches | Beeson, *Tilings of an Isosceles Triangle*, [1206.1974v7](https://arxiv.org/abs/1206.1974v7), revision 4 May 2026: Theorems 7.8 and 11.7. |
| Group 1 | Beeson, *Triangle Tiling: The case 3α+2β=π*, [1206.2229v4](https://arxiv.org/abs/1206.2229v4), revision 25 September 2026: Lemma 11, Theorem 9, Corollary 1, Theorems 16, 19, 22, 26. Local PDF has manuscript date 29 September 2026. **Version 4 is essential.** |
| Equilateral branches | Beeson, *Tiling an Equilateral Triangle*, [1812.07014v3](https://arxiv.org/html/1812.07014v3), revision 28 May 2024: five tile types in the introduction, Theorem 3(i), Theorem 6. Elementary arithmetic below replaces the printed prime calculation for the 60° case. |
| Rationality for irrational 120° tiles | Beeson–Zhang, *Rationality of certain triangle tilings*, [2604.01314v1](https://arxiv.org/pdf/2604.01314v1), Theorem **1.1**, a self-contained result for a nonsimilar 120° tile. This also replaces any appeal to the flawed older rationality argument. |
| Non-isosceles 120° arithmetic | Beeson, [2607.23453v1](https://arxiv.org/pdf/2607.23453v1), only the individual computations in Theorems 18–21, reproduced as formulas below. |
| Isosceles 120° obstruction | The signed-direction argument reproduced in `isosceles-120-invariant.md`, independently checked in this session; associated with V. Bonfioli's [repository commit 4bb61193bafa4471f7ba3a35324ae0f70bd2177c](https://github.com/ElVec1o/erdos_634_proof/tree/4bb61193bafa4471f7ba3a35324ae0f70bd2177c), [Zenodo v3.2](https://doi.org/10.5281/zenodo.22721069). The proof is summarized independently below. |

No broad prime-count conclusion from 2607.23453v1 is used: its original Group-1 and isosceles-120° dependencies are insufficient. In particular, this deduction does not cite its Theorem 3, Theorem 5(iii), Theorem 22 or Corollary 23 as an established global result. The withdrawn paper 2607.19572 is not used.

Two local wording errors in otherwise relevant sources must also be avoided. Corollary 7.9 of 1206.1974v7 forgets the valid N=2 exception; Theorem 7.8 supplies exactly what is needed for odd primes. The rational-angle equilateral discussion omits the valid 2k² family of 30–60–90 tiles; the elementary calculation below includes it. Neither correction affects the desired prime classification.

## Complete necessity argument

Suppose p>3 is prime and a target triangle is dissected into p congruent copies of a tile.

If the tile is similar to the target, the reptiling theorem gives a square, three times a square, or a sum of two integer squares as the tile count. Only the last option can equal p>3. Squares modulo 4 show p≡1 mod4.

It remains to exclude every nonsimilar possibility. Here is the exhaustive branch list.

| Target and tile branch | Exclusion for p>3 |
|---|---|
| Equilateral; rational tile angles | The three classical tile types are handled by the elementary area calculation below. |
| Equilateral; irrational angles and one 60° angle | Theorem 3(i) of 1812.07014v3 and the factorization below. |
| Equilateral; irrational angles and one 120° angle | Theorem 6 of 1812.07014v3; rationality may be supplied by Beeson–Zhang Theorem 1.1. |
| Non-equilateral isosceles; right tile | Theorem 7.8 gives N square or even. |
| Non-equilateral isosceles; tile γ=2α | Theorem 11.7 gives N non-squarefree. |
| Group 1; target (2α,α,2β) | 1206.2229v4, Theorem 16. |
| Group 1; isosceles base α+β | Same version, Theorem 22. |
| Group 1; isosceles base α | Same version, Theorem 26. |
| Group 1; target W=(2α,β,α+β) | Corrected necessary equation, followed by the new scale-one W theorem. |
| Group 1; isosceles base β | Corrected necessary equation, followed by the new scale-one β theorem. |
| Irrational 120° tile; non-equilateral isosceles target | The signed-direction obstruction below. |
| Irrational 120° tile; non-isosceles target | The four elementary factorizations below. |

Why this list is exhaustive: remove reptilings first. The equilateral classification gives exactly the five tile types used in the first three rows. For a non-equilateral isosceles target, Laczkovich's specialization gives right tiles, γ=2α, the three Group-1 isosceles shapes, and γ=120°. For a non-isosceles target with rational-multiple-of-π angles, Laczkovich's rational-angle theorem permits only a reptiling. In the remaining non-isosceles case, the tile must also have an irrational angle (target corner angles are sums of tile angles), and Laczkovich gives exactly the two scalene Group-1 shapes and the four scalene 120° shapes. Labels may be permuted as allowed by those classifications; the relation 3α+2β=π itself is never silently swapped.

### Direct integer-scale reduction

The sine law gives the W side proportions `(v³,uQ,vb)` and beta-isosceles proportions `(v³,v³,uP)`, with `Q=2v²−u²` and `P=3v²−u²`. Both triples are primitive: `gcd(v³,uQ)=gcd(v³,uP)=1`, since `gcd(u,v)=1`. Each actual external side is a sum of integer tile-edge lengths. Bezout therefore forces the similarity scale to be an integer. Comparing areas gives `N=j²Q` or `N=j²P`, and a prime count forces `j=1`.

This elementary route supplies the needed integer-scale conclusion independently of coloring-divisibility claims. The rationality and exhaustive shape-classification inputs remain necessary. See the [further internal review](audits/prime-case-review.md).

### The two newly closed rows

Group 1 means 3α+2β=π. By rationality and primitive normalization,

$$
(a,b,c)=(uv,v^2-u^2,v^2),\qquad 0<u<v,\quad\gcd(u,v)=1.
$$

For W, Corollary 1 of v4 gives

$$
N=j^2(2v^2-u^2),\qquad
(|AB|,|BC|,|CA|)=j(v^3,u(2v^2-u^2),v(v^2-u^2)).
$$

For isosceles base β, Theorem 19 gives

$$
N=j^2(3v^2-u^2),\qquad
\text{target sides}=j(v^3,v^3,u(3v^2-u^2)).
$$

Here j is a positive integer. Each parenthesized factor exceeds 1, so primality forces j=1. The two new theorems forbid exactly these two normalized targets for every coprime 0<u<v. No necessity of a construction-specific divisibility such as v|u² is asserted. No uniqueness of representation by either quadratic form is needed.

### Classical equilateral cases and the 60° calculation

For equilateral tiles the count is a square. For tile sides (1,1,√3), write the equilateral target side as L=A+B√3 with nonnegative integers A,B. Its area ratio is N=L². Rationality of N forces AB=0, giving a square or three times a square. For tile sides (1,√3,2), the area ratio is N=L²/2; again AB=0 and integrality gives N=2k² or 6k². None is prime greater than 3.

For the irrational 60° branch the cited discriminant condition is

$$
y^2=(9p-M^2)(p-M^2),\qquad 0<M^2<p,
$$

with M,y integers. Put X=5p−M². Then

$$
(X-y)(X+y)=16p^2.
$$

Both factors are positive. They cannot both be divisible by p, because their sum is 10p−2M² and p∤M. Therefore one factor contains p², and the sum is greater than p². But that sum is less than 10p, impossible for p≥11. For p=5 the two candidate discriminants are 176 and 41; for p=7 they are 372 and 177. None is a square. This checks all p>3 without the printed algebra in part (ii) of the source theorem.

### The 120° rows

After primitive normalization, rationality gives positive integers a,b,c satisfying

$$
c^2=a^2+ab+b^2.
$$

They are pairwise coprime and 3∤c. The four possible scalene targets have the following primitive side proportions and area ratios, obtained directly from the sine law. Since actual target sides are integers, the primitive proportions make λ a positive integer.

| Target angles | Primitive side proportions | N |
|---|---|---|
| (α,2α,3β) | (c²,c(a+2b),3b(a+b)) | 3λ²(a+2b)(a+b) |
| (α,2β,2α+β) | (ac,b(2a+b),(a+b)c) | λ²(2a+b)(a+b) |
| (α,α+β,α+2β) | (a,c,a+b) | λ²(a+b)/b |
| (2α,2β,α+β) | (a(a+2b),b(2a+b),c²) | λ²(a+2b)(2a+b) |

The first, second and fourth expressions are composite. In the third, b|λ², and a+b is composite: if a+b=q were prime, reducing the cosine equation modulo q would give q|(c−a)(c+a). Since a<c<a+b=q, the first factor cannot contain q; hence c+a=q, giving c=b, a contradiction. Thus this row is composite too. These are the individual computations of 2607.23453v1, Theorems 18–21, without its global conclusion.

For completeness, the isosceles 120° argument has a separate invariant. Take base angle α after interchanging a,b if necessary. Its primitive side proportions are (c,c,a+2b); indeed gcd(c,a+2b)=1 follows from the cosine equation and 3∤c. The actual sides are k(c,c,a+2b), k a positive integer, and the area ratio is

$$
N=k^2(a+2b)/b.
$$

Primality and gcd(b,a+2b)=1 force k²=b. The signed-direction character on directions jπ/3+ℓα is (−1)^j; irrationality of α/π makes it well defined. Assign length times this character to each directed edge. Reversal changes the sign, and subdividing at T-junctions cancels all interior contributions. Tile boundaries contribute ±(c+a−b), while the target contributes k(a+2b−2c). Hence

$$
\frac{k(a+2b-2c)}{c+a-b}
=\frac{c-a-b}{k}\in\mathbb Z.
$$

Thus k|(a+b−c). Since a<c<a+k², write c=a+kr with 1≤r≤k−1. Substitution gives

$$
a(2r-k)=k(k-r)(k+r).
$$

As gcd(a,k)=1, we have k|2r. Its only possible value in that range is 2r=k, making the left side zero and the right side positive. For k=1 there is no admissible r. This contradiction excludes the isosceles 120° row. The direction propagation and T-junction cancellation are detailed in `isosceles-120-invariant.md`.

Every nonsimilar row is now excluded. Consequently a prime p>3 allowing a tiling is a reptiling count and satisfies p≡1 mod4.

## Explicit existence, including the sum-of-two-squares construction

For p=2, cut an isosceles triangle along its altitude. For p=3, join the center of an equilateral triangle to its three vertices; the pieces are three congruent 120° isosceles triangles.

For p≡1 mod4, the two-squares theorem gives p=m²+n² with positive integers m,n. Use a right triangle T with legs m,n and hypotenuse √p. Take a larger right triangle OAB with

$$
OA=m\sqrt p,\qquad OB=n\sqrt p,\qquad AB=p.
$$

Let H be the foot of the altitude from O to AB. The right-triangle projection identities give

$$
AH=m^2,\qquad BH=n^2,\qquad OH=mn.
$$

Thus OAH is a copy of T enlarged by factor m, and OBH is a copy enlarged by factor n. Divide their sides into m and n equal parts, respectively, and use the usual parallel-line subdivisions. They contain m² and n² triangles, all congruent to T. Together these are exactly p congruent triangles and fill OAB. This is an explicit construction, not merely an appeal to a count in the reptiling classification.

## Audit status

The exhaustive passage from the stated published branch inputs and the two new scale-one theorems to the prime classification is valid. The source corrections noted above are incorporated. The new geometric theorems have internal adversarial reviews; that is not an external acceptance claim. General composite counts, larger scales j>1, and the full all-integer request of Erdős #634 remain outside this theorem.
