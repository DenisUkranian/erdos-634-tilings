# The sharp initial uniform cone for the new F3 mixed-corner construction

8 October 2026. Arithmetic theorem using the existing exact Apéry formula
and the new positive mixed-corner construction. This is an infinite-sector
result, not a classification of all F3 tilings or all Erdős634 counts.

**Theorem.** Let primitive positive integers a,b,c satisfy

    c²=a²+ab+b²,       2<a/b<2725/1139.

Then

    D=b²+2ab−a² belongs to c+<a,b,c>.

Consequently the [mixed-corner theorem](../f3-general/MIXED_CORNER_THEOREM.md)
constructs the ordered F3 target at scale one; subdivision supplies every
positive integer multiplier. Combined with the previous0<a<2b theorem,
this gives the full sufficient sector

    0<a/b<2725/1139  (approximately2.3924495).

The endpoint is **sharp for the initial uniform cone of this particular
semigroup construction**. At(2725,1139,3439), D does not belong to c+<a,b,c>.
This is not a nonexistence theorem for arbitrary F3 tilings at that endpoint.

## 1. Uniform large-size estimate

Put R=2725/1139, r=a/b, s=c/b. On2<r<=R, one has

    r<12/5,   s<31/10,
    1+2r−r² >=79246/1297321 >3/50.

The last expression is decreasing for r>1 and has the displayed value at R.
Thus, with d=D−c,

    d >(3/50)b²−(31/10)b.                              (1)

By the coprime normalization and exact Apéry theorem proved in
`../../global-criterion-oct7/SHARP_NESTED_CONE.md`, the unordered pair(a,b)
has a representation

    a0=p²−q², b0=q(2p+q), c=p²+pq+q²,

where p>q>0, gcd(p,q)=1, and p−q is not divisible by3. This includes the
factor-three parameter families after exchanging a0,b0. The Frobenius
number of<a,b,c>, the largest missing integer, is exactly

    F=(p−q−1)b0+(p−1)c−a0 <p(b0+c).                   (2)

We claim p<(8/5)sqrt(b). If a0=a,b0=b, put t=p/q=r+s<11/2. Then

    p²/b =t²/(2t+1)<121/48<64/25.

If a0=b,b0=a, then t=(1+s)/r>1+1/r>17/12, giving

    p²/b =t²/(t²−1)<289/145<64/25.

The relevant functions are respectively increasing and decreasing for t>1.
Since b0+c<=a+c<(11/2)b, (2) gives

    F <(44/5)b^(3/2).                                (3)

For b>=22500, the increasing function(3/50)sqrt(b)−(31/10)/sqrt(b)
is at least

    9−31/1500 =13469/1500 >13200/1500 =44/5.

Equations(1)–(3) show d>F, so d belongs to the semigroup. This argument
even includes the closed endpoint ratio whenever b>=22500.

## 2. Complete finite remainder

If b<22500, the proved parameter bound gives p<240. Enumerate all
2<=p<=239 and1<=q<p, requiring gcd(p,q)=1 and p−q not divisible by3.
Form the normalized unordered tile and retain precisely

    2b<a, 1139a<=2725b, b<22500.

There are exactly711 cases in this complete finite range. Exactly710 lie
in the strict ratio interval, and each has a directly checked nonnegative
integer decomposition

    d=i*a+j*b+k*c.

All coefficients are preserved in `f3_uniform_cone_verified.json`.
`check_f3_uniform_cone.py` regenerates the entire bounded parameter set
and checks each equality using integer arithmetic. No parameter sampling,
floating-point tolerance, or unverified optimization answer supplies the
finite assertion.

To find witnesses efficiently the checker uses the existing Apéry set

    {j*b0+k*c: 0<=j,k<p, not both j,k>=p−q}.

It reduces any representative using the exact positive relations

    p*b0=q*a0+q*c,
    p*c=(p+q)*a0+q*b0,
    (p−q)(b0+c)=(p+2q)*a0.

The cited lemma proves completeness and uniqueness of these residues.
For all positive cases the final certificate is also checked simply by
substitution, independent of how the witness was found.

## 3. Exact endpoint obstruction and sharpness scope

The sole closed-endpoint case is p=42,q=25, giving

    a0=1139, b0=2725, c=3439,
    D=79246, d=D−c=75807.

The unique Apéry representative of75807 modulo1139 is

    34*2725+11*3439=130479=75807+48*1139.

The pair(34,11) belongs to the L-shaped Apéry domain because p−q=17.
Since its least semigroup representative exceeds75807, the latter is
not in<2725,1139,3439>. The checker independently enumerates the whole
endpoint Apéry domain to confirm this unique residue representative.
Thus D is not in c+<a,b,c> at the endpoint.

Every larger initial open cone would contain this primitive tile, so the
endpoint2725/1139 is maximal for a uniform cone based on the stated
criterion. No such maximality is claimed for all possible F3 constructions.
The earlier sector0<a<2b and the newly proved sector2b<a<Rb meet without
an integral exceptional tile: a=2b would require c²=7b², which is impossible
for positive integers. The theorem therefore gives the stated combined
sufficient sector at every positive integer multiplier.
