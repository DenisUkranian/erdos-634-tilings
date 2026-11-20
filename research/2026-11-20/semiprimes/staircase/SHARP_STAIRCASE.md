# Sharp parameter range of the primitive F2 staircase

Let a>b>0 be coprime and c²=a²+ab+b². Use the ordered parametrization
$$
a=\frac{u^2-v^2}{g},\qquad b=\frac{v(2u+v)}g,\qquad c=\frac{u^2+uv+v^2}{g},\qquad g=\gcd(3,u-v).
$$
with coprime u>v>0. The condition a>b gives u>(1+√3)v. This form permits both g=1 and g=3. It follows, for example, by reducing (a+c)/b=u/v. Substitution in c²=a²+ab+b² recovers the three numerators, whose common divisor is g (the possible common divisor divides 3 and occurs exactly when 3 divides u−v).

The primitive F2 dissection criterion used in the staircase proof takes a list of integer load vectors (r,s,t) satisfying
$$
0\le r\le b,\quad 0\le s\le a,\quad t\ge0,\quad ar-bs=ct,\qquad \sum(r,s,t)=(c-b,c-a,a-b).
$$
Zero loads may be dropped. If s=0, coprimality forces c to divide r, so r=0 because r≤b<c. All nonzero loads have r,s>0. A permutation of the loads is allowed. Every such list produces a dissection by the geometric staircase. It is based on the height regions of the independently existing 143-tiling of the (3,5,7) tile, which is credited separately. The equivalence below is for these loads. It implies sufficiency for unrestricted tilings, including all positive scale multiples by standard subdivision. No necessity for all tilings is assumed.

**Theorem.** The list exists exactly when
$$
u\le\begin{cases}4v^2-4v,&g=3,\ v\equiv2\pmod3,\\4v^2,&\text{otherwise.}\end{cases}
$$

**Lattice coordinates.** Put
$$
s=\frac{un-vm}{g},\qquad t=\frac{um-vn}{g},\qquad r=\frac{vn+(u+v)m}{g}.
$$
For g=1 take n,m integers. For g=3 also impose n≡m modulo 3. The resulting lattice of pairs (s,t) is precisely the set satisfying bs+ct≡0 modulo a. Indeed the formulas imply ar=bs+ct and are integral in the specified lattice. The determinant of the (n,m)→(s,t) map is (u²−v²)/g²=a/g. The congruence on n,m cuts out an index-g lattice, so its image has index a in the entire integer (s,t) plane. The congruence bs+ct≡0 also has index a because gcd(a,b)=1. Thus inclusion is equality. Summing the inverse transformation gives
$$
\sum n=2v,\qquad \sum m=u-2v=M.
$$
Every nonzero admissible load has n,m>0, by positivity of the entries in the inverse matrix acting on (s,t)≥0. The load bound r≤b implies
$$
m\le H=\left\lfloor\frac{2uv+v^2-v}{u+v}\right\rfloor.
$$
Take L=H for g=1, and for g=3 take L=1+3 floor((H−1)/3). Every load obeys m≤nL. For g=3 the case n=1 follows by the congruence. If H≥4 then 2L≥H. If H≤3 and n=2 then m≡2 modulo 3 gives m≤2, while n≥3 poses no restriction. Hence M≤2vL is necessary.

**Large aspect.** Assume u≥4v. If M≤2vL, build 2v loads with n=1 and with positive m≡1 modulo g, differing by at most g, whose sum is M. This is possible since M≥2v and M−2v=u−4v is divisible by g. Take m at the nearest allowed values on either side of M/(2v). Then m≤L, so r≤b. For g≤3 the largest m is strictly below M/(2v)+3=u/(2v)+2, hence at most u/v. Therefore s≥0. Also t≥0 as u>v and m≥1. The s values sum to c−a, strictly below a since c<a+b<2a, so s≤a. This proves sufficiency.

If u≥v² then H=2v−1, since H=2v−ceil((v²+v)/(u+v)). For g=1 this gives u≤4v². For g=3 the value L is 2v−1 if v≡1 modulo 3, or 2v−3 if v≡2 modulo 3. This gives the stated bounds. If u<v² then H≥v and L≥v−2. The bound M≤2vL is automatic since 2v(v−2)+2v≥v² when v≥2. The claimed threshold also always holds in this range.

**Smaller aspect.** For u≤3v we have c≤2b since u²−3uv−v²<0. The single vector (c−b,c−a,a−b) is admissible. For 3v≤u<4v, M lies between v and 2v. At g=1 take M loads with m=1 and n=1 or 2 adding to 2v. This is feasible since u≥3v, and u+3v≤2uv+v². At g=3 take (4v−u)/3 loads (n,m)=(5,2) and all the remaining m entries as unit (1,1) loads. Their number M−2(4v−u)/3 is nonnegative. The largest possible numerator of r is 2u+7v≤2uv+v² for v≥2 in this interval. There are no g=3,v=1 integer parameters in 3v≤u<4v. Also 2u−5v≥0 and 5u−2v>0, so both counts s,t are nonnegative. Again the total bounds s≤a. This covers every smaller parameter and proves the theorem.

**Checks.** arithmetic.py replays all 13,663 ordered coprime shapes with u≤350, 12,320 of which admit the construction. It separately uses exact dynamic programming on the original untransformed loads for u≤24. The three exceptional pairs from the prior narrow cone all have explicit certificates:

| tile (a,b,c) | (u,v,g) | load vector (r,s,t) with multiplicity |
|---|---|---|
| (649,455,961) | (46,13,3) | 16×(24,11,11) + 2×(61,68,9) |
| (3325,2291,4891) | (104,29,3) | 38×(54,25,25) + 4×(137,154,21) |
| (7289,5031,10729) | (154,43,3) | 56×(80,37,37) + 6×(203,228,31) |

**Counting the remaining candidate shapes.** The primitive F2 count N=(a+2b)(2a+b) is at least 2a². Since a=(u²−v²)/g and v<u/2, it follows that u=O(X^(1/4)) when N≤X. Failure of the sharp criterion forces v=O(√u), also in the exceptional residue class where 4v(v−1)≥2v² for v≥2. Thus at most O(X^(3/8)) integer parameter records still need geometry, before imposing primality. In particular, for every fixed ratio bound q/p≤2−ε for mixed primes, all sufficiently large F2 arithmetic candidates satisfy the staircase construction. The omitted parameter region concerns very thin tiles, including the first (a,b,c)=(33,7,37), (u,v,g)=(10,1,3), N=3431.


## A prime sector with only two missing pairs

Take odd primes 3<p<q with opposite residues modulo four. An F2 arithmetic candidate has p=a+2b and q=2a+b. Write x=u/v. The ratio q/p=(2x²+2x−1)/(x²+4x+1) strictly increases with x, since the numerator of its derivative is 6(x²+x+1). Its value at x=12 is 311/193. If 193q<311p, a candidate outside the sharp theorem must have x<12. Since b=(2uv+v²)/g is odd, v is odd. If v≥5 failure implies x>4v−4≥16. If v=3 primitivity forces g=1, and failure implies x>12. Consequently v=1. Since a is odd, u is even. Failure then restricts u to 6, 8 or 10. Their two factors are (61,83), (97,143) and (47,73), respectively. The middle pair drops out because 143 is composite. This identifies precisely the two candidate pairs for which the staircase provides no dissection. In the narrower range 61q<83p neither survivor is present, and the conic criterion is necessary and sufficient for every pair of mixed residues. The equality 193q=311p would introduce (193,311), from (u,v,g)=(12,1,1). The proof involves no unbounded prime scan. For the same-residue prime sector also apply the established classical and Paliy tests independently of this F2 argument.
