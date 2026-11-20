# An asymptotic for actual squarefree tile counts in the F2 residue sector

Let S(X) count squarefree integers N at most X with the following three properties.

1. N is 23 modulo 24.
2. Every prime divisor of N is 1 or 11 modulo 12.
3. Some triangle can be dissected into N congruent triangles, allowing reflections and T-junctions.

Let F(X) count the distinct integers in this sector given by the constructive unit F2 staircase. With the squarefree constant K of [the binary quartic count](F2_MASS.md),
$$
 S(X)\sim F(X)\sim (K/3)\sqrt X,\qquad
 0\le S(X)-F(X)\ll \frac{\sqrt X}{(\log X)^2}.
$$
The constant K/3 is approximately 0.02636. The integers in this definition may have any number of prime factors. The theorem applies to the original existential tiling problem, with the outer triangle and tile both free. It does not give a decision for each semiprime.

**Geometric reduction.** In the squarefree case the integral multiplier in the nonclassical rows is one. Four shapes (W, beta, theta and double-angle isosceles) exclude that multiplier. In the remaining nine rows only the plus-norm equilateral target and F2 have coefficient 7 modulo 8. The classical sum-of-two-squares family cannot give 7 modulo 8, and neither can the other classical families. The equilateral coefficient is E=ab and the F2 coefficient is D=(a+2b)(2a+b), with coprime positive sides and c²=a²+ab+b². The two reductions used here are [the tables in §§4–5](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-reduction/PROOF.md) and [the four scale-one exclusions in §1](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md).

Every odd primitive F2 coefficient falls in the residue and prime-support sector of (1)–(2). Both a and b are odd, hence ab=7 modulo 8 by the norm, and D=7 modulo 8. Modulo 3 the case a=b≠0 would force 3 to divide c and give c² congruent to 3b² modulo 9, an impossibility. Consequently D=−(a−b)²=2 modulo 3. For a prime l dividing D, the norm gives either c²=3b² or c²=3a² modulo l. Primitivity excludes zero on the right, and quadratic reciprocity then gives l=1 or 11 modulo 12. The F2 arithmetic and staircase counts differ by O(X^(3/8)) by [the sharp parameter bound](../staircase/SHARP_STAIRCASE.md). The squarefree leading term follows from [the quartic calculation](F2_MASS.md).

**Bounding the equilateral contribution.** Order the sides a>b by symmetry. With g=gcd(3,u−v) the primitive parametrization gives
$$
 E=\frac{v(u-v)(u+v)(2u+v)}{g^2},
 \qquad u>(1+\sqrt 3)v.
$$
In particular E is bounded below by a positive constant times u³v. Every parameter record contributing to S(X) avoids both classes 5 and 7 modulo 12 at each of the four factors in the numerator. Division by g² only affects the prime 3.

Here is a short proof that the number of these records is o(√X). We have v=O(X^(1/4)), and at each v there are O((X/v)^(1/3)) choices of u. The integers v avoiding all primes 5 or 7 modulo 12 have counting function o(Y) up to Y. This follows by excluding finitely many such primes, using the Chinese remainder theorem, and then taking more primes, whose reciprocal sum diverges. Partial summation gives a weighted count o(Y^(2/3)) with weight v^(−1/3). This proves the asserted main term for S(X) independently of the following rate.

**Quantitative remainder.** For a prime l in the two forbidden classes, the four factors vanish on four distinct lines in the plane modulo l. Their union has 4l−3 points. Write α(l)=(4l−3)/l² and extend it multiplicatively to squarefree products of these primes. In any translated square of side V consecutive integers, the number of pairs for which d divides the product is
$$
 V^2\alpha(d)+O\big(4^{\omega(d)}(V+d)\big).
$$
This follows by counting points of each residue pair modulo d separately. The Selberg upper-bound sieve with z=V^(1/16) and the product P of forbidden primes up to y=z^(1/20) bounds the sifted count by V²/G plus O(sum over d|P, d≤z² of 12^ω(d)(V+d)), where
$$
 G=\sum_{d\mid P,\ d\le z}\prod_{l\mid d}\alpha(l)/(1-\alpha(l)).
$$
The error is O(V^(11/8)): use 12^ω(d)≤d² for these primes. The unrestricted sum is the product of (1−α(l))^(−1), of order (log y)² by Mertens' theorem in progressions. In the corresponding product probability measure the expected log d is at most (4+o(1))log y by the prime number theorem. Markov's inequality preserves at least half of the mass at d≤z. It follows that each translated square contributes O(V²/(log V)²). Standard sieve references are [Elkies' notes on Selberg's sieve](https://people.math.harvard.edu/~elkies/M259.02/sieve.pdf) and [Williams on Mertens' theorem](https://doi.org/10.1016/0022-314X(74)90032-8).

For v≤X^(1/8) the unsieved bound sums to O(X^(5/12)). Otherwise split v dyadically, V≤v<2V, up to V=O(X^(1/4)). Since u=O((X/V)^(1/3)), each strip is covered by O(1+(X/V)^(1/3)/V) squares of side V. On nonempty strips of this range the second term is bounded below by an absolute positive constant, and log V is comparable to log X. Summing the geometric progression in V^(2/3) yields O(√X/(log X)²). This counts all admissible equilateral parameters even if none of their targets can be tiled. Adding the F2 error proves the theorem.

**Consequence for all squarefree integers.** The number of squarefree tile counts at most X outside the sums of two integer squares (allowing zero squares as summands) has order exactly √X. The lower bound is supplied by the displayed positive constant in the 23 modulo 24 sector. The upper bound is the sum of [the nine elementary parameter bounds in §§5.1–5.2](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-sectors/PROOF.md) after the four scale-one exclusions, together with the finitely many extra classical squarefree counts. In particular the leading-term assertion above counts genuine geometric examples even if every unresolved unit F2 board eventually turns out to be impossible.
