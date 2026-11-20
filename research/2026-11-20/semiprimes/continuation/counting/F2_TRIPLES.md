# The triple of a mixed F2 prime candidate

Take distinct primes p=a+2b and q=2a+b, where positive coprime odd integers a>b satisfy c²=a²+ab+b². Then

$$
 T(3pq) \quad\Longleftrightarrow\quad
 a>4b,\qquad b\text{ is a square},\qquad a+5b\text{ is a square}.
$$

Here T(n) means that some triangle splits into n congruent triangles. The criterion holds whether or not the F2 board for pq tiles. In fact q<2p automatically. The [close-pair criterion](ALL_THREE_P_Q.md) therefore applies, and its three tests become 2q−3p=a−4b>0, 3(2p−q)=9b square, and 3p−q=a+5b square. This proves both directions. The [prime-power factorization](../SIMULTANEOUS.md) subsequently rules out the two squares simultaneously whenever p is prime. In particular every such F2 input has an untileable triple. For sufficiency the construction is the Paliy two-piece construction in a different angular branch.

For the seven unit pq controls below a million the triple always has a negative answer. These do not settle the original seven counts.

| pq | a | b | 3pq | Failed test |
|---:|---:|---:|---:|---|
| 3,431 | 33 | 7 | 10,293 | b is between 4 and 9 |
| 5,063 | 35 | 13 | 15,189 | a is smaller than 4b |
| 19,367 | 85 | 11 | 58,101 | b is between 9 and 16 |
| 60,023 | 143 | 25 | 180,069 | a+5b = 268 lies between 256 and 289 |
| 64,367 | 161 | 15 | 193,101 | b is between 9 and 16 |
| 271,151 | 323 | 37 | 813,453 | b is between 36 and 49 |
| 641,591 | 533 | 27 | 1,924,773 | b is between 25 and 36 |

**A shorter dependence chain.** In fact the argument below applies to every pair of primes 3<p<q<2p with pq equal to 7 modulo 8, including all the F2 candidates. Then 3pq is 5 modulo 8. In the squarefree count table the only remaining rows that can give 5 modulo 8 are BQ and QP, after excluding W, beta, theta and double-angle at unit scale. The BQ row would require 3pq=(k−m)(k+m)Q, Q=2k²−m² and coprime 0<m<k. Here 3 does not divide Q, because squares modulo 3 are 0 and 1. Also Q>k²−m²≥3. If k−m=1, then k²−m²=2k−1 is divisible by 3, must equal 3 or 3p (the other divisor choices exceed Q), and 3 only gives k=2 and total 21. In the other case k=(3p+1)/2 and Q=k²+2k−1>2p, contradicting q<2p. More explicitly, writing k²−m²=3q would require Q=p<3q. If k−m>1, all three factors must be primes. Since k+m>3 and 3 does not divide Q, one has k−m=3. Then p=2k−3 and q=k²+6k−9>2p for k≥4, again impossible. This leaves only QP. Its arithmetic and both geometric directions are the Paliy theorem. Thus the close F2 corollary uses neither of the two moving-bank manuscript exclusions, nor an individual exclusion for 105 or 231. The [count table](THREE_PRIME_EXCLUSION.md) gives the sources of the shape and multiplier inputs.
