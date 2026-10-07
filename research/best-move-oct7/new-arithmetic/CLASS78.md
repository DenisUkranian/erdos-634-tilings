# Complete classification of the square class 78

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

**Theorem.** For every positive integer m, some triangle can be tiled by
`78m²` congruent triangles if and only if m is even. Reflections and
arbitrary T-junctions are allowed.

This is a complete result for one square class, not a complete solution
of Erdős 634. The necessary angular spectra and F3 isolation theorem are
prior inputs. The new positive F3 construction supplies the 312-tile seed;
the negative argument below is an elementary rational-point obstruction
and requires no rank computation, Mordell-Weil basis, or conjecture.

## 1. Even multipliers are positive

The new [ordered-F3 construction for a<b](../hexagon/F3_SMALL_A.md), with
`(a,b,c)=(3,5,7)`, gives a triangle with sides `(49,91,120)` tiled by

```
3(3+5)(3+2*5)=312
```

congruent `(3,5,7)` triangles. Its expanded unit-coordinate certificate
has also been checked independently in that construction package.

If `m=2r`, integer dilation by r and ordinary triangular subdivision
replace each tile with r² congruent unit copies. This gives
`312r²=78m²` tiles.

## 2. An odd multiplier would force an odd F3 coefficient

Suppose m is odd. Then

```
78m²=14 (mod 16),
v_3(78m²)=1+2v_3(m) is odd.
```

By the established [F3 isolation theorem](../../../docs/f3-global-overlap.md),
every possible realization would belong to F3. The prime used to exclude
W is three: 2 is a quadratic nonresidue modulo three. All other branches
are excluded by the same residue-sector argument.

The primitive F3 count formula would give

```
3(a+b)(a+2b) r²=78m²,
c²=a²+ab+b², gcd(a,b)=1,
```

with positive integral r. Since 78 is squarefree, `r²|78m²` forces
`r|m`, by comparing each prime valuation. Thus `s=m/r` is an odd
positive integer. Put

```
S=a+b, T=a+2b.
```

We would have

```
ST=26s²,   c²=T²-3ST+3S².
```

Exactly one of S,T is even, with 2-adic valuation one. It cannot be S:
if `S=2 (mod 4)` and T is odd, the norm equation would give `c²=3
(mod 4)`. Therefore S is odd and `v_2(T)=1`. Consequently a is even,
b is odd, and c is odd.

## 3. The explicit rational-point map and its parity

Define rational coordinates

```
x = 26(2c+2T-3S)/S = 26(2c-a+b)/S,
y = 52s*x/S.
```

Then

```
y²=x³+156x²-2028x,        v_2(x)=1.                 (1)
```

Here x is positive and nonzero, because `c>a` and S>0. Its 2-adic
valuation is exactly one: S and `2c-a+b` are odd.

For an explicit verification of the curve equation, put

```
S0=S/s, T0=T/s, C0=c/s.
```

Then `S0*T0=26` and `C0²=T0²-78+3S0²`. The displayed map is
equivalently

```
x=T0(2T0-3S0+2C0),   y=2T0*x.
```

Its quadratic identity is

```
x²+(156-4T0²)x-2028=0,
```

which yields the curve equation after multiplication by x. This follows
by substituting the displayed expression for x and the norm equation.

This is the quartic-to-cubic map used in the
[odd-F3 note](../../../docs/f3-odd-multipliers.md), written explicitly.
It must not be replaced by the direct 2-isogeny image of the usual F3
point: that different map has a square x-coordinate and does not give
the needed parity. For the even seed `(a,b,c,s)=(3,5,7,2)`, the present
map gives `(x,y)=(52,676)`, whose x-valuation is two, as required.

## 4. No rational point on (1) has odd x-valuation at two

Suppose x is a positive rational number satisfying (1), with rational y
and odd `v_2(x)`. Write its positive squarefree square class as d:

```
x=d(u/v)²,  u,v positive coprime integers.
```

Every prime appearing to an odd exponent in x divides 2028. To see
this directly, for a prime l not dividing 2028 a negative valuation of
x makes x³ the unique least-valuation term in the cubic, so `3v_l(x)`
is even. A positive valuation makes `-2028x` the unique least-valuation
term, so `v_l(x)` is again even. Thus

```
d is one of 2,6,26,78.
```

The cubic equation implies an integer W satisfying

```
W²=d u⁴+156u²v²-(2028/d)v⁴.                       (2)
```

Indeed `W=yv³/(du)` is rational and its square is the displayed integer,
so W is an integer. We now exclude all four possibilities modulo 13.

### Case d=2 or 6

Modulo 13, equation (2) becomes `W²=d u⁴`. Both 2 and 6 are quadratic
nonresidues modulo 13. Hence `13|u` and `13|W`. Write `u=13u1`,
`W=13W1` and divide (2) by `13²` to get, modulo 13,

```
W1²=-(12/d)v⁴.
```

For d=2 and 6, the coefficient is respectively 7 and 11 modulo 13;
both are quadratic nonresidues. Hence `13|v`, contradicting
`gcd(u,v)=1`.

### Case d=13e with e=2 or 6

All terms on the right of (2) are divisible by 13, so `13|W`.
Dividing by 13 and reducing modulo 13 gives

```
e u⁴+12u²v²-(12/e)v⁴=0.                          (3)
```

Neither u nor v is zero modulo 13: if one were, (3) would force the
other to be zero too. Multiply (3) by `e/v⁴`, and put
`q=e(u/v)²` in the residue field. Then

```
q²-q+1=0 (mod 13).
```

Its roots are 4 and 10, both quadratic residues modulo 13. But q is a
quadratic nonresidue, since e is either 2 or 6 and u/v is nonzero. This
contradiction excludes the remaining two classes.

All possible d are excluded. Thus (1) has no rational point with
`v_2(x)=1`; in fact the argument excludes every odd x-valuation at two.
This contradicts the explicit point forced by an odd F3 multiplier.

## 5. Conclusion and scope

Odd m admits no classified branch, while every even m has the explicit
312-seed construction. Therefore

```
78m² is a triangle-tiling count  if and only if  2 divides m.
```

The obstruction permits positive-rank points with even x-valuation;
for example `(52,676)` lies on the curve. Thus the proof is not a
rank-zero argument and does not confuse the existence of some F3
coefficient in the square class with its odd-multiplier sector.

The attached exact checker verifies the rational map on all primitive
norm triples through a bounded range whose coefficient belongs to this
class, the seed, and every residue in the modulo-13 contradictions.
The general proof above, rather than finite enumeration, excludes all
odd multipliers.
