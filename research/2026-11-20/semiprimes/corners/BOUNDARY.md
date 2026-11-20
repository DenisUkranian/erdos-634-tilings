# Exact lengths of straight boundary segments for every primitive F2 tile

Assume gcd(u,v)=1 and a>b>0, where g=gcd(3,u−v), a=(u²−v²)/g, b=v(2u+v)/g and c=(u²+uv+v²)/g. These sides are pairwise coprime. Set A=(u+2v)/g, D=(2u+v)/g, F=(u−v)/g, and C=u if g=1, C=A if g=3. Let S consist of all nonnegative sums xa+yb+zc. A supporting segment between two endpoints of whole side-words, including those abutting a transversal crosscut, has a length in S.

**Normal form.** For each of the b residue classes modulo b, its least member of S is uniquely xa+zc for a pair

                  0≤x<A,  0≤z<C,  min(x,z)<v.                     (1)

Thus these values form the Apéry set of S relative to b. The largest nonrepresentable nonnegative integer is

           max((A−1)a+(v−1)c, (v−1)a+(C−1)c) − b.

Proof. The following relations follow by substitution. In both normalizations Aa=F(b+c) and ub=v(a+c). If g=1, Cc=(u+v)a+vb. If g=3, Cc=Fa+Db. In a least representative in its class no b summand can occur. If x≥A, z≥C, or both x,z≥v, the matching relation exchanges some summands for a strictly positive multiple of b and other summands. Removing the b's would make the representative smaller. Every residue is represented since a is a unit modulo b. There are AC−(A−v)(C−v)=v(A+C−v)=vD=b pairs in (1), all needed to cover the b distinct residue classes. This proves minimality and uniqueness together. Maximizing on the two arms of (1) gives the displayed formula.

For a fast membership test set r=(a⁻¹L mod D). All possible differences t=x−z lie in [1−C,A−1] and satisfy t≡r mod D because a+c=uD. This interval contains at most two representatives of a fixed residue, since A+C−v=D and v<D. For each t choose the unique z∈[max(0,−t),max(0,−t)+v−1] satisfying uz≡(L−at)/D mod v (use the whole trivial residue when v=1). Put x=t+z. Exactly one pair satisfies (1). Call its value m(L); then L∈S iff L≥m(L), with witness (x,(L−m(L))/b,z). Thus at most two candidates need checking after a modular inverse or extended gcd. No search through boundary words is required.

**Geometric application.** For a scale-one F4 triangular cap cut off about the smallest F2 angle, the requisite segments on the two adjacent board sides have lengths ac and c(a+b). The remainder on the longer side must therefore have length

         R=a(a+2b)−c(a+b)=wa−d b,   w=b−(c−a)=vF,   d=c−a=vA.

For this F4 shape the sides incident to the corner are ac and c(a+b). Since a+b>c the latter exceeds the adjacent board side of length c² and must lie on the side of length ap. The argument just uses the necessity of a nonnegative side sum. When v=1, w=F<A; wa is the least element of its residue class by (1). Subtracting the positive db makes R unrepresentable. For (33,7,37) and (35,13,43), R=71 in both cases. The least representable lengths in the same classes are 99 and 175 respectively.

For *every* mixed semiprime candidate beyond the staircase with v>1 this particular test succeeds. Indeed b is odd, so v≥3 is odd. Outside the ordinary threshold u>4v². Outside the exceptional one (g=3, v≡2 mod 3) we have v≥5 and u>4v(v−1). In both cases u≥3v²+v. An explicit side sum is

    R = (w−A−v²)a + (F−d+vu)b + (F−v²)c.

It follows by applying Aa=F(b+c) once and v(a+c)=ub exactly v times. F≥v² by the bound on u. Also g(w−A−v²)=(v−1)u−(1+g)v²−2v≥3v(v²−2v−1)>0. Finally g(F−d+vu)=((g−1)v+1)u−(2v²+v)>0. All coefficients are nonnegative. This establishes the precise v=1 versus v>1 dichotomy for the specified scalar test on the residual semiprime domain. Realizing the rest of the boundary or tiling the cap is a separate geometric condition. Standard background on Apéry sets is provided by J. C. Rosales et al., “Modular Diophantine inequalities and rotations of numerical semigroups”, https://doi.org/10.1017/S1446788708000141 . The special formulas and the side-segment application here have direct elementary proofs; no literature priority claim is made.

For a check beyond the first seven, u=44,v=3 gives (a,b,c)=(1927,273,2077) and prime factors 2473,4127. The remainder 196071=64·1927+23·273+32·2077 passes the scalar test, while inequality (1) of PROOF.md fails (6076400>4734639). This illustrates two different geometric tests on the same primitive triangle. Neither gives a verdict on whether 10206071 is a tile count.
