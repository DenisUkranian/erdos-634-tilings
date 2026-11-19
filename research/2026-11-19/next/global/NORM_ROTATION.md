# Two fixed square multipliers for all real-quadratic norm counts

19 November 2026. Write \(G(n)\) when some triangle has a dissection into \(n\) congruent triangles, with arbitrary T-junctions. The following deductions use Bonfioli's six-piece construction, the large-scale W and beta constructions, and Paliy's exhaustive row reduction. They are research deductions, with no claim of priority or external refereeing.

## A constructive implication for every integer represented by the norm

For all positive integers \(n\), the following implications hold.

| An integral representation of \(n\) | A resulting tiling count | Target family |
| --- | --- | --- |
| \(n=2y^2-x^2\) | \(77^2 n\) | W |
| \(n=3y^2-x^2\) | \(65^2 n\) | beta-isosceles |
| Either representation | \(91^2 n\) | The corresponding family |

The representing pair may be nonprimitive, and the constants are sufficient. Every integer-square multiple of the resulting count is also tiled. The construction may change the tile as it chooses a representation of the norm.

**Geometric input.** Set \(D=2\) for W and \(D=3\) for beta. A primitive pair \(0<e<f\) realizes \(M^2(Df^2-e^2)\) in its indicated family when
\[
 Me\ge f,\qquad (M-1)(f-e)\ge f.
\]
For \(e\ge2\) and \(f-e\ge2\), this is Bonfioli's Theorem W (both targets). When \(e=1\) the first inequality implies \(M\ge f\). When \(f-e=1\) the second implies \(M>f\). Both endpoint cases follow from the all-parameter construction at \(M\ge f\). Dividing an integral pair by its common divisor \(g\) raises the multiplier from \(M\) to \(gM\), preserving both inequalities. [Bonfioli, release v3.0, Theorem W](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/README.md) and [Paliy, unrestricted positive construction](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/updates-2026-10-10/w-beta/UNRESTRICTED_CONSTRUCTION.md).

**Normalization.** Choose a representation with \(y>0\), so \(z=x+y\sqrt D>0\) and its conjugate is negative. Put \(L_D=\log\epsilon_D\) with \(\epsilon_2=3+2\sqrt2\), \(\epsilon_3=2+\sqrt3\). Multiplication by integral norm-one units shifts \(\log(z/\sqrt n)\) by any multiple of \(L_D\), and changing the sign of \(x\) reflects it about zero. Thus one can arrange that \(0\le\log(z/\sqrt n)\le L_D/2\). Since \(\log(z/\sqrt n)=\operatorname{arctanh}(x/(\sqrt D y))\) and \(\exp(2\operatorname{arctanh}(1/\sqrt D))=\epsilon_D\), this gives \(r=x/y\in[0,1]\).

**Integral norm rotations.** For either family put \(K\) equal to the multiplier in the table and use the following integers.

| \(D\) | \(A\) | \(B\) | \(l\) | Choices of \(K\) | Corresponding \(M=K/l\) |
| --- | ---: | ---: | ---: | --- | --- |
| 2 | 9 | 4 | 7 | 77, 91 | 11, 13 |
| 3 | 14 | 3 | 13 | 65, 91 | 5, 7 |

If \(1/K\le r\le1-1/(K-1)\), use the original pair at scale \(K\). Otherwise put
\[
 e'=|Ax-DBy|,\qquad f'=Ay-Bx,\qquad h(r)=e'/f'=\frac{|Ar-DB|}{A-Br}.
\]
Now \(Df'^2-e'^2=l^2n\), since \(A^2-DB^2=l^2\). On each outside interval \(0\le r\le1/K\) or \(1-1/(K-1)\le r\le1\), the signed fraction inside the absolute value is increasing, with derivative \(l^2/(A-Br)^2>0\). Its zero \(DB/A\) lies between the two intervals. Thus its absolute value takes its extrema at the four listed endpoints. For the smaller respective \(K\), these values are

| \(D,K\) | \(h(0)\) | \(h(1/K)\) | \(h(1-1/(K-1))\) | \(h(1)\) | Required interval |
| --- | --- | --- | --- | --- | --- |
| \(2,77\) | \(8/9\) | \(607/689\) | \(67/384\) | \(1/5\) | \([1/11,9/10]\) |
| \(3,65\) | \(9/14\) | \(571/907\) | \(306/707\) | \(5/11\) | \([1/5,3/4]\) |

These lie in the required interval. Increasing \(K\) to 91 shrinks each outside interval and increases \(M\), which enlarges the permitted interval. The rotated pair therefore realizes \(M^2l^2 n=K^2 n\) after primitive normalization. This proves the three constructive implications, including \(r=0,1\). [Reproducible exact computations](check.py).

## A complete arithmetic criterion in part of the W-only residue class

Suppose \(N\equiv14\bmod16\), \(3\nmid N\), and \(77^2\mid N\) (or \(91^2\mid N\)). Then
\[
 G(N)\quad\Longleftrightarrow\quad
 v_p(N)\text{ is even for every prime }p\equiv3,5\bmod8 .
\]
Paliy's mod-16 collapse leaves only W: both difference-of-squares families fail at 2-adic valuation one, the other Group-1 residues fail, F3 requires a factor of 3, and the remaining Eisenstein and classical families fail modulo 8. Thus any tiling makes \(N\) a negative norm from \(\mathbb Z[\sqrt2]\) up to a square, preserving even valuations at inert primes. Conversely, the inert-prime condition is unchanged on dividing by \(K^2\). The ring \(\mathbb Z[\sqrt2]\) is norm-Euclidean (round both coordinates, giving absolute remainder norm at most \(1/2\)). Split prime ideals are principal, the ramified prime 2 has generator \(\sqrt2\), and inert primes of even exponent are squares. These facts represent \(N/K^2\) up to a norm sign. The unit \(1+\sqrt2\) has norm \(-1\) and supplies the required sign. Apply the constructive implication. [Paliy, uniform sectors, Lemma 3.1](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-sectors/PROOF.md).

For \(D=3\) the corresponding criterion for the *norm hypothesis* is also arithmetic. Write \(n=3^a n'\) with \(3\nmid n'\). Each odd prime \(p\ne3\) with \((3/p)=-1\) must have even valuation and \((-1)^{a+1}n'\equiv1\bmod3\). These conditions suffice: \(\mathbb Z[\sqrt3]\) is norm-Euclidean by coordinate rounding (absolute remainder norm at most \(3/4\)), and 2 and 3 are ramified with generators \(1+\sqrt3,\sqrt3\). Build a generator of absolute norm \(n'\) using split primes, squares and the ramified factor 2. Its norm must be \(1\bmod3\), since its first coordinate is nonzero modulo 3. This fixes its sign uniquely. Multiplication by \((\sqrt3)^a\) yields norm \(-n\). The beta implication gives a sufficient tiling condition; other angular families occupy the same mod-16 residues.

## An exact criterion with two prescribed primes in the kernel

Suppose \(N\equiv14\bmod16,\ 3\nmid N\). Write \(N=dm^2\) with \(d\) squarefree. If \(217=7\cdot31\) divides \(d\), then \(G(N)\) holds **exactly when** \(m>1\) and every prime \(3,5\bmod8\) has even valuation in \(N\). This puts no fixed divisibility condition on \(m\).

The same W-only reduction gives necessity, including \(m>1\) because primitive W multiplier 1 is excluded. Conversely \(m>1\) implies \(m\ge5\) here. The norm criterion gives a representation of \(-d/217\), which can be normalized to starting ratio \(r\in[0,1]\). For any \((A,B)\) in the following four rows, \(A^2-2B^2=217\). Multiplication by \(A+B\sqrt2\), followed if needed by a sign change of the first coordinate, replaces \(r\) with \(|(Ar+2B)/(A+Br)|\). On each displayed interval this belongs to \([1/4,2/3]\).

| \(A,B\) | Certified interval of \(r\) |
| --- | --- |
| \(15,2\) | \([0,18/41]\) |
| \(17,-6\) | \([2/39,1/2]\) |
| \(15,-2\) | \([1/2,6/7]\) |
| \(27,-16\) | \([6/7,1]\) |

These intervals cover \([0,1]\). Direct substitution at the endpoints suffices since the signed fraction is strictly increasing and has the same sign at both ends of each interval. The resulting representation of \(-d\) satisfies the central cone condition at \(M=4\), hence at every \(M\ge4\), including \(m\). This proves unrestricted existence.

The same finite-interval calculation gives the following unconditional constructions already at \(M=3\). If \(n>0\) has a representation of norm \(-n\) from the indicated field, the respective geometric family realizes \(h\,n\,M^2\) at every \(M\ge3\):

| \(D\) | A squarefree choice of \(h\) | Other verified \(h\) |
| --- | --- | --- |
| 2 | \(7\cdot17\cdot23\cdot31=84\,847\) | \(25\,823\) |
| 3 | \(11\cdot13\cdot23\cdot37=121\,693\) | \(20\,449\) |

The certificate gives eight rational intervals for each of these four counts. For each interval one verifies \(A^2-DB^2=h\), endpoint signs, and the same endpoint inequalities now with \([1/3,1/2]\). All their unions cover the complete unit interval. Primitive normalization is valid as above. [Exact rational certificates](small_scale_results.json), [generator](small_scales.py), [independent verification](verify_covers.py).
