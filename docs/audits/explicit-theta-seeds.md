# Internal audit of the explicit theta seed

29 September 2026. This is a second internal mathematical derivation by
ChatGPT during Denis Paliy's directed investigation. It is not an external
referee report, a formal proof-assistant verification, or a priority claim.

**Conclusion:** the negative-Delta construction in
[explicit-theta-seeds.md](../explicit-theta-seeds.md) passes this symbolic
audit. In particular, the proposed scale

$$
s=ucn(a^2+b^2),\qquad
n=\left\lceil\frac{(b-1)(c-1)-a^2\Delta}{b^3c^2}\right\rceil
$$

is a valid theta seed when

$$
a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad
0<u<v,\quad \gcd(u,v)=1,\quad
\Delta=b(a^2+b^2)-a^2c<0.
$$

This audit verifies the symbolic partition and the strip fillings. The
separate [exact checker](../../scripts/check_explicit_theta_seed.py) and
its [frozen report](../../verification/explicit-theta-seeds.json) supplement
that argument with finite macroregion checks; neither is a claim that every
individual tile of these potentially enormous constructions was enumerated.

## 1. Arithmetic and scale identities

Write $R=a^2+b^2$ and $\rho=ab^2cn$.
The identities used below follow from $a^2=c(c-b)$:

$$
a^4+c\Delta=b^3c,\qquad
a^2R-b^2c^2=-c\Delta.
$$

The target's similarity scale and theta scale are

$$
\mu=\frac{\rho R}{bc},\qquad
s=\frac{\rho R}{b^2v}=ucnR.
$$

All five initial triangular block scales are positive integers:

$$
\rho,\quad \frac{a\rho}{c}=a^2b^2n,\quad
\frac{a^2\rho}{bc}=a^3bn,\quad
\frac{b\rho}{c}=ab^3n,\quad
\frac{b\rho}{a}=b^3cn.
$$

No division requiring an unstated coprimality condition remains.

## 2. Position of the five triangular blocks

Use the points $A,B,C,K,L,H,I,J$ from the main construction.
Their stated side triples give original-tile triangles

$$
BKL,\quad KHL,\quad AKH,\quad HLJ,\quad HIJ
$$

at the scales just listed. In addition to the side calculations, the
placement of these triangles was checked separately.

The barycentric coordinates of $H$ in $ABC$ are

$$
\left(\frac{b^2}{R},
      \frac{a^2u^2}{cR},
      \frac{a^2b}{cR}\right).
$$

In $AKL$ they are

$$
\left(\frac{b^2}{c^2},
      \frac{u^2b}{c^2},
      \frac{u^2}{c}\right).
$$

Substitution into the displayed coordinate formulas reproduces $H$ in
both cases. Every coefficient is positive, and each triple sums to one,
using $b+u^2=c$. Thus $H$ is strictly inside both triangles.

The boundary orders are genuine:

$$
A,K,B;\qquad B,L,J,C;\qquad A,I,H.
$$

Indeed,

$$
AK+KB=\frac{\rho R}{b}=\mu c,
$$

$$
BL+LJ+JC
=c\rho+\frac{b^2\rho}{c}-\frac{\rho\Delta}{bc}
=\mu c.
$$

All three lengths on the latter line are positive. Also

$$
AI=-\frac{\rho\Delta}{ab}>0,\qquad
AH-AI=\frac{\rho b^2}{a}>0,
$$

where the last identity is exactly $a^4+c\Delta=b^3c$.

These facts first separate $BKL$, then use the interior point $H$ to
partition $AKL$. The triangle $HLJ$ attaches along the next part of the
same side, leaving the quadrilateral $AHJC$.

The directed edges of $AHJC$, traversed in that order, have angles

$$
\alpha,\quad -\beta,\quad -\theta,\quad -\pi,
\qquad \theta=\alpha+\beta.
$$

The clockwise turns are therefore

$$
\theta,\quad\alpha,\quad\pi-\theta,\quad\pi-\alpha,
$$

all strictly between zero and $\pi$. Consequently this quadrilateral is
convex. Since $I$ lies between $A$ and $H$, the segment $IJ$ divides it
into $HIJ$ and the red trapezoid $AIJC$.

This establishes a disjoint geometric partition, rather than merely a
matching list of areas or side lengths.

## 3. Red trapezoid dimensions

The trapezoid has top base and slant lengths

$$
IJ=\frac{\rho bc}{a}=b^3c^2n,\qquad
AI=-\frac{\rho\Delta}{ab},\qquad
JC=-\frac{\rho\Delta}{bc}.
$$

Its base difference is

$$
AC-IJ
=\rho\left(\frac{aR}{bc}-\frac{bc}{a}\right)
=-\frac{\rho\Delta}{ab}
=AI.
$$

This follows directly from $a^2R-b^2c^2=-c\Delta$.
Its lower corner angles are $\alpha$ and $\theta$; both slant sides
therefore meet the same horizontal top line with positive height.

Divide each slant into $n$ equal parts and join corresponding points.
Every horizontal strip then has left and right slants

$$
\ell=bc(-\Delta),\qquad r=ab(-\Delta).
$$

Both are positive, and $\ell$ is an integer multiple of both $b$ and $c$.

## 4. Each strip has an integral tiling

The two triangular corner blocks in a strip have scales

$$
r_1=-a\Delta,\qquad r_2=-c\Delta.
$$

Both are positive integers. Their side triples agree with the original
tile. The remaining region is an alpha-parallelogram with slant $\ell$
and horizontal length, for strips numbered downward from the top,

$$
W_j=b^3c^2n+a^2\Delta+jbc(-\Delta),
\qquad 0\le j<n.
$$

The minimum is $W_0$. By the definition of $n$,

$$
W_0\ge (b-1)(c-1).
$$

Thus every strip has enough top width for the indicated corner cuts;
the cuts lie inside that strip. The remaining parallelogram has positive
dimensions.

Since $\gcd(b,c)=1$, write $W_j=x_jb+y_jc$ with nonnegative integers.
The slant $\ell=bc(-\Delta)$ accommodates both orientations of the
$b$-by-$c$ grid cells. Each such cell at angle $\alpha$ splits into two
original tiles. Its tile count is $2(-\Delta)W_j$.

Consequently every region of the complete partition is tiled by
congruent copies of the fixed original tile. The target is the theta
triangle at scale $s$, so its total count is $bs^2$.

## 5. Consequence and limits

This construction supplies an explicit seed throughout $\Delta<0$.
The positive-Delta construction is treated in the earlier
[eventual-family note](../eventual-rational-families.md) and its
[separate audit](eventual-rational-families.md); this report does not
replace that review.

Together with the two internally checked
[universal annuli](../universal-rational-scales.md), an explicit seed
makes the eventual theta and alpha bounds numerical.
One can use $H_u$ alone when raising the seed, because $H_u\ge H_v$:
before taking ceilings,

$$
\frac{a^2+b^2+(b-1)(c-1)}{ub}
>
\frac{a^2+(b-1)(c-1)}{vb}.
$$

The seed is deliberately coarse. Neither its scale nor the resulting
eventual bound is asserted to be optimal. This result does not settle
the smaller exceptional scales or Erdős problem 634 as a whole.
