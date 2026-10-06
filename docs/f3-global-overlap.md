# An infinite family for which every tiling belongs to F3

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

There are infinitely many actual triangle-tiling counts which admit no
realization in any branch other than the 120-degree F3 branch. Consequently,
a universal replacement of F3 by other branches cannot complete the
classification of counts in Erdős problem 634.

The positive construction used below is an existing F3 tail, credited to
the Harries–Zhang transfers in [square-class tails, Appendix A](square-class-tails.md#appendix-a-every-integer-tails-for-all-norm-rows).
The deduction combines that construction with the exhaustive necessary
spectra. It provides an obstruction to a proposed method; it does not
settle the remaining F3 scales or solve the whole problem. No external
priority or referee acceptance is claimed.

Let \(\mathcal S\) be the positive integers \(N\) for which some
nondegenerate triangle can be dissected into \(N\) congruent
nondegenerate triangles. Reflections and arbitrary T-junctions are allowed.

## 1. A sector in which only F3 can occur

**Theorem 1.1.** Suppose

\[
N\equiv14\pmod{16},
\]

and some odd prime \(p\equiv3\) or \(5\pmod8\) has odd valuation in
\(N\). Then every tiling with count \(N\), if one exists, belongs to
the 120-degree F3 branch of the exhaustive angular classification.

The classification and the integral square scales used in this theorem
are the existing inputs recorded in [uniform sectors, Section 2](../research/uniform-sectors/PROOF.md)
and the [uniform-reduction proof](../research/uniform-reduction/PROOF.md).
The latter identifies the published angular-classification, rationality
and classical-count sources. Neither the proposed all-primes theorem nor
a proposed scale-one W or beta exclusion is used.

**Proof.** Since \(v_2(N)=1\), every integral square scale in a necessary
count form \(N=Dt^2\) is odd. An odd square is 1 or 9 modulo 16, and
\(8D\equiv0\pmod{16}\). Thus

\[
D\equiv14\pmod{16},\qquad D\equiv6\pmod8.
\tag{1.1}
\]

The classical count forms are squares, sums of two squares, twice a
square, three times a square, and six times a square. Squares, twice a
square and sums of two squares cannot be 6 modulo 8. Three times a square
cannot have 2-adic valuation one. Six times an odd square is 6 modulo 16,
whereas six times an even square has greater 2-adic valuation. All
classical cases are therefore excluded.

For the five Group-1 rows, write

\[
b=v^2-u^2,\qquad Q=2v^2-u^2,\qquad P=3v^2-u^2,
\qquad 0<u<v,\quad \gcd(u,v)=1.
\]

The coefficients are respectively \(Q,P,b,bQ,QP\) for W, beta,
theta, alpha and the other scalene branch. The double-angle branch also
has coefficient \(v^2-u^2\), with its own range on \(u,v\).
If \(u,v\) have opposite parity, \(b\) is odd; if both are odd,
\(8\mid b\). Hence neither difference-of-squares row satisfies (1.1).
Substituting the square residues \(0,1,4,9\pmod{16}\), with \(u,v\)
not both even, gives

| Coefficient | Possible residues among \(6,14\pmod{16}\) |
|---|---|
| \(Q\) | \(14\) |
| \(P\) | None |
| \(bQ\) | \(6\) |
| \(QP\) | \(6\) |

Thus W is the only Group-1 possibility.

For completeness, the seven norm rows have primitive positive integers
\(a,b,c\), with \(\gcd(a,b)=1\) and
\(c^2=a^2\pm ab+b^2\). If exactly one of \(a,b\) is even, that side
is divisible by 8: subtract the odd side's square from \(c^2\) modulo 8;
the result is the even side times an odd number. If both sides are odd,
the plus norm gives \(ab\equiv7\pmod8\), hence \(a+b\equiv0\pmod8\),
and the minus norm gives \(ab\equiv1\pmod8\). Substitution yields:

| Branch | Coefficient | Possible residues modulo 8 |
|---|---|---|
| 60-degree equilateral | \(ab\), minus norm | \(0,1\) |
| 120-degree equilateral | \(ab\), plus norm | \(0,7\) |
| F1 | \(b(a+b)\) | \(0,1\) |
| 120-degree isosceles | \(b(a+2b)\) | \(0,1,2\) |
| F2 | \((a+2b)(2a+b)\) | \(2,7\) |
| F3 | \(3(a+2b)(a+b)\) | \(0,3,6\) |
| F4 | \((2a+b)(a+b)\) | \(0,1,2\) |

Only F3 can satisfy (1.1). This accounts for all thirteen nonclassical
rows, leaving only W and F3.

Finally, a W count would have

\[
N=(2v^2-u^2)t^2.
\]

Odd valuation at \(p\) forces \(p\mid2v^2-u^2\). Primitivity gives
\(p\nmid v\), so \((u/v)^2\equiv2\pmod p\). But 2 is a quadratic
nonresidue at primes congruent to 3 or 5 modulo 8. This excludes W and
proves the theorem. \(\square\)

The earlier W-only residue statement assumed \(3\nmid N\), which
excludes F3 through its coefficient's factor 3. Theorem 1.1 removes that
assumption and retains the one additional branch it permits.

## 2. An explicit infinite family of actual counts

**Theorem 2.1.** For every integer

\[
h\equiv3\pmod{600},\qquad h\ge3,
\]

the integer

\[
\boxed{N(h)=3h(h+2)^3(h^2+4h+1)}
\tag{2.1}
\]

belongs to \(\mathcal S\), and every tiling with that count belongs to
the 120-degree F3 branch. These counts are all distinct.

**Proof.** Set

\[
a=h^2-1,\qquad b=2h+1,\qquad c=h^2+h+1.
\tag{2.2}
\]

Direct expansion gives

\[
c^2=a^2+ab+b^2.
\]

We have \(a>b>0\) for \(h\ge3\). Any common divisor of \(a,b\) is
odd, and the identity

\[
4a=(2h-1)b-3
\]

shows that it divides 3. Since \(h\equiv0\pmod3\), we have
\(b\equiv1\pmod3\). Therefore \(\gcd(a,b)=1\): (2.2) is a
primitive plus-norm tile. Its F3 coefficient is

\[
D_h=3(a+2b)(a+b)
   =3h(h+2)(h^2+4h+1).
\tag{2.3}
\]

The congruence \(h\equiv3\pmod8\) gives
\(a\equiv8\) and \(b\equiv7\pmod{16}\). Consequently

\[
D_h\equiv3\cdot6\cdot15\equiv14\pmod{16}.
\tag{2.4}
\]

Also \(h\equiv3\pmod{25}\), so \(h+2\equiv5\pmod{25}\), while
\(h\) and \(h^2+4h+1\) are nonzero modulo 5. It follows that

\[
v_5(D_h)=1.
\tag{2.5}
\]

Every odd square multiple \(D_ht^2\) retains residue 14 modulo 16 and
odd valuation at 5. By Theorem 1.1, no such count can occur outside F3.
This statement alone is a necessary-branch exclusion; the following
existing construction supplies actual tilings.

The every-integer F3 tail in [square-class tails, Appendix A](square-class-tails.md#appendix-a-every-integer-tails-for-all-norm-rows)
constructs the primitive tile at every scale

\[
t\ge
\left\lceil\frac32
\left(\left\lfloor\frac{\max(a,b)}{\min(a,b)}\right\rfloor+2\right)
\right\rceil.
\tag{2.6}
\]

For (2.2), put \(r=(h-1)/2\). Then
\(a=rb+r\), with \(0<r<b\), and hence

\[
\left\lfloor\frac ab\right\rfloor=\frac{h-1}{2}.
\]

Thus (2.6) reduces to

\[
t\ge\left\lceil\frac{3(h+3)}4\right\rceil.
\]

The integer \(t=h+2\) is odd and satisfies this inequality, since
\(4(h+2)-3(h+3)=h-1\ge0\). Therefore the old tail constructs
\(D_h(h+2)^2=N(h)\), proving membership. The branch exclusion proves
that every tiling of this count is F3. Finally, each positive factor in
(2.1) is strictly increasing for \(h>0\), so the resulting counts are
distinct. \(\square\)

The first parameter \(h=3\) recovers the already known tile
\((8,7,13)\) and coefficient 990. The theorem concerns the infinite
family, using the existing construction at an explicit sufficient scale;
it claims no new F3 dissection. More generally, every odd scale satisfying
(2.6) supplies an actual count to which the same branch exclusion applies.

## 3. What this rules out

There is no universal transformation replacing every realizable F3 count
by a realization in a classical, QP, F4, or other non-F3 branch while
preserving the count. Theorem 2.1 rules this out even if the transformation
may change both the tile and the target, and may choose any permissible
integral square scale.

Overlap theorems on smaller domains remain possible. Multiplying a count
in Theorem 1.1 by another odd square preserves the obstruction. An even
square can leave the sector, so no obstruction to that changed-count
operation is asserted.

The arithmetic identity

\[
D_{F3}(a,b)=3D_{F4}(b,a)
\]

does not yield a replacement with the same count: its factor 3 is not an
integral square. The [oriented F4 construction](../research/group2-f4/PROOF.md)
and [balanced F2/F3 construction](../research/group2-trapezoids/BALANCED_F4.md)
remain useful positive inputs, but do not remove the family above.

Within this sector, an exact classification must therefore settle F3
itself. The [elliptic-rank theorem](elliptic-square-classes.md) decides
whether an F3 coefficient exists somewhere in a square class; the
[odd-multiplier theorem](f3-odd-multipliers.md) refines its parity. Neither
alone settles the remaining small-scale geometric membership questions.
