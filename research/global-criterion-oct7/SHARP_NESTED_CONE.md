# A sharp uniform cone for the nested-corner construction

7 October 2026. This note derives an exact numerical-semigroup formula
and extends an existing sufficient geometric theorem. It does **not**
classify arbitrary tilings or solve Erdős problem 634. No claim of
external priority for the semigroup formula is made.

## The result

Let primitive positive integers A>B satisfy C²=A²+AB+B². If

    1 < A/B < 45/32,

then every positive integer multiplier is realizable in the reversed
F4 row, F2, and both ordered F3 rows for this fixed tile. The target
formulas and positive partitions are those of the existing
[nested-corner theorem](../group2-nested-corners/PROOF.md).

The new assertion is the arithmetic identity

    BC−A² belongs to <A,B,C>

throughout that open cone. The already proved nested-corner theorem
turns it into actual tilings at multiplier one; ordinary quadratic
subdivision supplies every positive multiplier.

The endpoint is sharp **for a uniform cone using that particular
construction criterion**. The primitive endpoint tile (45,32,67) has
BC−A²=119 outside <45,32,67>. No nonexistence of arbitrary F2, F3 or F4
tilings at this endpoint is asserted.

## 1. A normalization with no factor of three

The existing primitive plus-norm parameterization is

    a=(p²−q²)/g,
    b=q(2p+q)/g,
    c=(p²+pq+q²)/g,

where p>q>0 are coprime and g is 1 or 3. In fact g=3 precisely when
p−q is divisible by 3. If g=3, put

    p'=(p+2q)/3, q'=(p−q)/3.

These are coprime positive integers with p'>q' and p'−q'=q not divisible
by 3. Their unnormalized triple is (b,a,c), as direct expansion shows.
Thus every primitive unordered plus-norm tile can be written

    a0=p²−q², b0=q(2p+q), C=p²+pq+q²,                  (1)

with p>q>0 coprime and p−q not divisible by 3. The pair (a0,b0) is
(A,B) or (B,A). All semigroup assertions are invariant under that swap.
The parameterization used here is derived in the existing
[ternary-semigroup note](../f3-descent-attempt/TERNARY_SEMIGROUP_TAIL.md).

To check coprimality in the g=3 conversion: a common divisor of p',q'
also divides p'+2q'=p and p'−q'=q; hence it is one. Also p,q are not
multiples of 3, since they are coprime and congruent modulo 3.

## 2. The exact Apéry set and Frobenius number

For (1), define the set of pairs

    L = {(j,k): 0<=j,k<p, and not both j,k>=p−q}.

Then the Apéry set of <a0,b0,C> relative to a0 is exactly

    {j b0+k C : (j,k) in L}.                            (2)

In particular its Frobenius number, the largest missing integer, is

    F=(p−q−1)b0+(p−1)C−a0.                             (3)

**Proof.** The following exact positive relations hold:

    p b0=q a0+q C,
    p C=(p+q)a0+q b0,
    (p−q)(b0+C)=(p+2q)a0.                              (4)

Starting with any nonnegative pair (j,k), use the first relation when
j>=p, the second when k>=p, and the third when j,k>=p−q. Each replacement
preserves the residue of j b0+k C modulo a0, keeps j,k nonnegative, and
strictly decreases that nonnegative integer weight. The process therefore
terminates at a pair in L.

Every residue modulo a0 has a nonnegative representative j b0: indeed
(a0,b0) are coprime. The reduction proves that L represents every residue.
But |L|=p²−q²=a0, so it represents every residue exactly once.
For any semigroup representation x=i a0+j b0+k C with i,j,k>=0, the
same reductions increase i by positive integers. Consequently the
unique L weight in the residue of x is at most x. This proves (2),
including minimality, not merely a residue-completeness assertion.

Since C>b0, the largest L weight is

    (p−q−1)b0+(p−1)C.

Subtracting a0 gives (3). For completeness, each integer larger than
that difference is at least its least residue representative: otherwise
the positive difference would be a multiple of a0 and at least a0.
The displayed difference itself is not representable. This proves the
claimed Frobenius formula without invoking an external formula. ∎

## 3. A uniform size bound through 45/32

Suppose 1<A/B<=45/32, and put r=A/B, s=C/B. The function

    f(r)=sqrt(r²+r+1)−r²

is strictly decreasing for r>=1. At r=45/32 one has s=67/32, hence

    BC−A² >= (119/1024) B².                            (5)

Choose the normalized parameters in (1). If a0=A,b0=B, then

    t=p/q=(A+C)/B=r+s<=7/2,
    p²/B=t²/(2t+1)<=49/32<25/16.

If a0=B,b0=A, then

    t=p/q=(B+C)/A=(1+s)/r>=11/5,
    p²/B=t²/(t²−1)<=121/96<25/16.

The monotonicities are immediate by differentiation; alternatively
(1+s)/r equals x+sqrt(x²+x+1) with x=1/r.
In either ordering, p<(5/4)sqrt(B), and b0+C<=A+C<=(7/2)B.
Formula (3) therefore gives

    F<p(b0+C)<(35/8) B^(3/2).                          (6)

For B>=1444=38², (5) is larger than (6), since

    (119/1024)*38=2261/512 > 2240/512=35/8.

Thus BC−A²>F and belongs to <A,B,C>. This part includes the closed
ratio bound A/B<=45/32, but only at the stated large size.

## 4. The narrow extension has no small primitive tiles

The earlier result proves the desired membership for every primitive
tile with 1<A/B<=7/5, with no size restriction. It is proved in the
[ternary-semigroup note](../f3-descent-attempt/TERNARY_SEMIGROUP_TAIL.md),
using its general conductor bound and complete finite certificate.
It remains to consider

    7/5 < A/B < 45/32.                                 (7)

We show directly that (7) forces B>1444, so Section 3 applies. This step
requires no new finite enumeration.

If a0=A,b0=B, the parameters satisfy

    (7+sqrt(109))/5 < p/q < 7/2.

The left endpoint is larger than 87/25. Therefore

    0 < 7/2−p/q < 1/50.

The numerator 7q−2p is a positive integer, so the difference is at
least 1/(2q). Hence q>25 and

    B=q²(2p/q+1) > (199/25)q² > 1444.

If a0=B,b0=A, then

    11/5 < p/q < (5+sqrt(109))/7 < 53/24.

It follows that

    0 < p/q−11/5 < 1/120.

The numerator 5p−11q is a positive integer, so q>24. Consequently

    B=q²((p/q)²−1) > (96/25)q² >=2400>1444.

Combining the old closed cone through 7/5, this Farey-denominator gap,
and Section 3 proves the stated open cone through 45/32. ∎

## 5. Exact limitation and scope

The endpoint tile is primitive and satisfies

    67²=45²+45*32+32²,
    32*67−45²=119.

If 119=45i+32j+67k with nonnegative integers, k is 0 or 1. For k=0,
i can only be 0,1,2, leaving 119,74,29, none divisible by 32. For k=1,
i is 0 or 1, leaving 52 or 7, again impossible. Thus the unit nested
criterion fails. Its other width parameters cannot help: the existing
unit-criterion equivalence proves that k=1 is the only possible width
when A>B; concretely 32*67−2*45²<0 here.

Accordingly the maximal initial open ratio interval for which this
specific unit criterion holds for **every primitive norm tile** is
exactly (1,45/32). This is not an exact classification outside that
interval, nor a necessary condition for other tiling constructions.
In particular the gamma theorem already constructs the ordered F3
target of (45,32,67), despite failure of the nested-corner recipe.
Neither 154 nor 4830 is decided by this result.

Run `python research/global-criterion-oct7/check_sharp_cone.py` to compare
the Apéry formula against an independent shortest-path computation,
verify factor-three normalization and label swaps, check a finite exact
sample of the cone, and replay the endpoint obstruction. Finite checks
corroborate the proofs above; no sample is used to infer the uniform
statement. The checker writes no files unless `--report` is supplied.
