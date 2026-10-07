# Independent audit of the complete square class 78

The theorem in [CLASS78.md](../new-arithmetic/CLASS78.md) passes this
independent audit:

```
78*m^2 is a triangle-tiling count if and only if m is even.
```

The arithmetic proof uses the established exhaustive necessary spectra
and their [F3 isolation theorem](../../../docs/f3-global-overlap.md).
It does not use a prime-classification candidate, a rank computation,
a conjectural list of rational points, or a negative tiling search.

## 1. Exhaustive reduction and parity

For odd m, `78m^2=14 mod16`. The existing residue reduction leaves only
W and F3. In W, the primitive coefficient `Q=2v^2-u^2` cannot be
divisible by 3: otherwise `u^2+v^2=0 mod3` forces both u,v divisible
by 3. Thus W has even 3-adic valuation after multiplication by an
integer square, whereas `78m^2` has odd 3-adic valuation. This also
explains explicitly why the argument still works when 3 divides m.

In F3, write

```
3(a+b)(a+2b)t^2=78m^2.
```

Squarefreeness of 78 gives t|m by prime valuations. Hence q=m/t is
an odd integer, and with `S=a+b`, `T=a+2b`,

```
ST=26q^2, c^2=T^2-3ST+3S^2.
```

The product has 2-adic valuation one. If S were even, then S=2 mod4
and T would be odd; the norm would be 3 mod4, impossible. Therefore
S is odd and T=2 mod4. It follows that a is even, b is odd, and c is
odd. No assumption about a<b is used in this negative direction.

## 2. Re-derivation of the rational map

Put `r=T/S=26z^2`, `z=q/S`, `w=c/S`. Then

```
w^2=r^2-3r+3,
(2w)^2-(2r-3)^2=3.
```

Let `U=2w+2r-3`. Since w>0, the second identity gives U>0 and

```
U-3/U=4r-6.
```

Setting `x=26U`, `y=52xz` yields, by multiplication and substitution,

```
2704*x*z^2=x^2+156*x-2028,
y^2=x^3+156*x^2-2028*x.
```

Furthermore

```
x=26(2c-a+b)/S,
```

whose numerator after removing the factor 26 and whose denominator
are both odd. Thus x>0 and `v_2(x)=1`. This is the actual displayed
map, not the different isogeny map whose x-coordinate is a square.

## 3. Complete elementary descent obstruction

Write `x=d(u/v)^2`, with d positive squarefree and u,v positive
coprime integers. At a prime not dividing 2028, a negative x-valuation
makes the cubic term uniquely minimal, and a positive x-valuation
makes the linear term uniquely minimal. Either valuation is even.
As `2028=2^2*3*13^2` and `v_2(x)` is odd, the exhaustive list is

```
d in {2,6,26,78}.
```

The number `W=y*v^3/(d*u)` is rational with integer square, so is
an integer. Its equation is

```
W^2=d*u^4+156*u^2*v^2-(2028/d)*v^4.
```

For d=2 or 6, reduction modulo 13 first forces 13|u,W, since 2 and 6
are nonsquares. Dividing by 13^2 and reducing again gives

```
(W/13)^2=-(12/d)*v^4 mod13.
```

The coefficients are 7 and 11, both nonsquares, forcing 13|v and
contradicting coprimality.

For d=13e, e=2 or 6, the right side is divisible by 13. Hence 13|W,
and division by 13 followed by reduction gives

```
e*u^4+12*u^2*v^2-(12/e)*v^4=0 mod13.
```

Neither u nor v can vanish modulo 13. With `q0=e*(u/v)^2`, the
equation becomes `q0^2-q0+1=0`. Its only roots are 4 and 10, both
squares. But q0 is a nonsquare because e is 2 or 6. This excludes
both remaining classes.

This is a contradiction for every potential odd-multiplier F3
realization. Positivity of x is sufficient for the geometric
application. In fact the same proof also excludes the four negative
square classes, since -1 is a square modulo 13.

## 4. Positive direction and status

The [independently audited positive F3 construction](F3_A_LT_B_AUDIT.md)
at `(a,b,c)=(3,5,7)` supplies 312 tiles, with target sides 49,91,120.
For m=2r, ordinary r-fold subdivision gives
`312r^2=78m^2`. This covers every even multiplier.

The argument therefore proves necessity and sufficiency for every
positive m in square class 78. No part of the proof asserts that all
other square classes have been classified.

As an additional arithmetic sanity check, all eight signed quartics
were checked modulo `13^3=2197` in the two normalized projective
charts `v=1` and `u=1, 13|v`. None of their 18,928 normalized cases
had a square right side. This finite check is supplementary; the two
short modular arguments above supply the proof.
