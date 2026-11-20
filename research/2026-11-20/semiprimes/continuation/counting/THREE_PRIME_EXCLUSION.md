# A complete exclusion for half the odd squarefree products of three primes containing 3

Write T(N) if some nondegenerate triangle admits a tiling by N congruent triangles, allowing reflections and T-junctions. Let Ω count prime factors with multiplicity.

**Theorem.** If N is squarefree, divisible by 3, congruent to 3 modulo 4, and Ω(N) ≤ 3, then T(N) holds exactly when N = 3. In particular, if p and q are distinct primes greater than 3 and p ≡ q modulo 4, no triangle admits a tiling with 3pq congruent triangles.

**Scope.** The arithmetic proof below uses the deposited geometric branch reduction cited below and project certificates for two explicitly identified counts. The conclusion is unconditional with respect to orientations and edge alignments, on those stated mathematical inputs. It does not decide all 3pq or the mixed-semiprime branch F2. The four ordered pairs of odd prime classes modulo 4 have equal asymptotic frequency for unordered products when they are counted by their size and ordered consistently by the size of their prime factors. Equivalently, products with equal prime classes comprise half the 3pq population in the limit. The elementary theorem itself requires no density result.

## Geometric inputs

Every nonclassical tiling gives an entry in the primitive count table at an integer multiplier t, in the form N = d t². Since N is squarefree, t = 1. The W, beta, theta and double-angle branches are impossible at this multiplier. For the remaining branches the following are the full coefficient residues modulo 8. The names F1 to F4 refer to the displayed formulas. For the rows containing a,b, they are coprime positive integers with c² = a²+ab+b², except for the indicated minus sign.

| Coefficient | Residues modulo 8 |
|---|---|
| Group-1 alpha and Paliy products | 0,1,2,5,6 and 1,2,5,6, respectively |
| Equilateral ab (minus norm) | 0,1 |
| Equilateral ab (plus norm) | 0,7 |
| F1 b(a+b) | 0,1 |
| Isosceles b(a+2b) | 0,1,2 |
| F4 (2a+b)(a+b) | 0,1,2 |
| F2 (a+2b)(2a+b) | 2,7 |
| F3 3(a+b)(a+2b) | 0,3,6 |

For instance an even leg in a primitive plus-norm solution is divisible by 8, by reduction modulo 4 and 8. If both legs are odd their product is 7 modulo 8. The minus norm gives 1 instead. Substitution gives the listed conic residues. The Group-1 residues follow by substituting coprime integers w,z in (z²−w²)(2z²−w²) and (2z²−w²)(3z²−w²). The classical families are sums of two squares and 3r², 6r². The first excludes 3 modulo 4, the last is even, and the middle gives only N = 3 here. Joining the barycenter of an equilateral triangle to its three vertices realizes 3.

Sources for the branch reduction, multiplier restrictions and residues: [Paliy, Uniform reduction, §§3–5](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-reduction/PROOF.md), [Beeson and Roșu, unit W and beta exclusions](https://arxiv.org/abs/2607.23453v4), [combined count table with updated unit exclusions](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md).

## One elementary factorization

For a primitive plus-norm triple reorder the two legs so a>b. They cannot be equal. In lowest terms put u/v = (a+c)/b. Substituting c=ub/v−a into the norm equation gives a:b:c proportional to

    u²−v² : v(2u+v) : u²+uv+v².

Here u,v are coprime and u>(1+√3)v by a>b. The gcd of the first two numerators divides 3: a common prime cannot divide v or u, and it divides both 2u+v and u²−v². Substitution v ≡ −2u modulo any common prime power forces that prime power to divide 3u². All three numerators are divisible by 3 exactly if u≡v modulo 3. Consequently the primitive triple is obtained by dividing the three numerators by g = gcd(3,u−v). In particular g divides u−v, 2u+v and u+2v.

The symmetric sum of the legs is u[(u+2v)/g]. Both factors exceed one since u>2v and u+2v>3. Thus a+b is always composite. An independent proof for an odd prime r=a+b uses (2c−|a−b|)(2c+|a−b|)=3r². For r>3 the smaller factor lies strictly between r and √3 r, an interval containing no divisor of 3r². This latter observation was already used in the project's even triple-product reduction.

## The two residues

If N ≡ 3 modulo 8, F3 is the sole nonclassical candidate. The count 3(a+b)(a+2b) has at least four prime factors with multiplicity because a+b is composite and a+2b>1. This part uses no individual tiling exclusion.

If N ≡ 7 modulo 8, only the plus equilateral row and F2 survive the table. F2 is impossible because either of its factors is divisible by 3 exactly when a≡b modulo 3, in which event both are divisible by 3, contradicting squarefreeness. The equilateral candidate therefore has odd count

    N = ab = v F U D,     F=(u−v)/g,  U=u+v,  D=(2u+v)/g.

Here v is odd (since b is odd and g is odd) and u is even (since a and v are odd). If v≥3 then u−v>√3v>3, and every displayed factor exceeds one. This would require Ω(N)≥4.

If v=1, the factors U,D exceed one. If F=1, then u−1=g gives u=4 (the alternative u=2 violates u>1+√3). This yields (a,b,c)=(5,3,7), N=15. If F>1, all three factors F,U,D must be primes. One equals 3 since 3 divides N. U=3 again forces u=2. D=3 gives 2u+1=3g, hence u=1 or 4, neither in this subcase. F=3 gives u−1=3g, which forces g=3 and u=10. This yields (a,b,c)=(33,7,37), N=231. There are no other arithmetic candidates.

For 15 use Bonfioli's reported exact spectrum through 200. For 231 use the project's geometric reduction to two orientation bands and its exact position certificates, which cover T-junctions. These two finite inputs are separate from the universal factor argument. [Bonfioli, exact spectrum through 200](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_primes_and_N200.tex) · [231 reduction](https://github.com/DenisUkranian/erdos-634-tilings/blob/6c0a28e1902062ef661413427560960e210dc693/research/2026-11-19/nov19/equilateral231/INDEPENDENT_REDUCTION.md) · [231 certificates, replay procedure and verification status](https://github.com/DenisUkranian/erdos-634-tilings/blob/6c0a28e1902062ef661413427560960e210dc693/research/2026-11-19/nov19/equilateral231/RESULT_UK.md).

The odd multiples of 3 congruent to 3 modulo 4 occupy exactly 3 and 15 modulo 24. For N=3p with p>3, the theorem covers exactly the primes p≡1 modulo 4. The previously established full semiprime row excludes 3p also for p>3 with p≡3 modulo 4. The edge products 3·2 and 3·3 are classical. [Earlier prime-pair reduction](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md).
