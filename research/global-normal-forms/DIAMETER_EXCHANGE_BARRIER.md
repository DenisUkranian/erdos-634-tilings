# Why scalar exchange-length bounds do not decide the norm rows

7 October 2026. This is a limitation of one proposed necessary-condition
route, not a tiling theorem or a solution of the remaining classification.

## The exact arithmetic barrier

Let `a,b,c` be positive integer sides of a nondegenerate triangle, with
`gcd(a,b)=1`. Define the three shortest positive exchange lengths by

```
La = min {na : na = Bb+Cc, n>0, B,C>=0},
Lb = min {nb : nb = Aa+Cc, n>0, A,C>=0},
Lc = min {nc : nc = Aa+Bb, n>0, A,B>=0}.
```

The right-hand sides are positive automatically. When a mixed whole-edge
seam initially has additional a-edges on both banks, canceling their
counts gives an a-relation of this form, of length no greater than the
original seam. The definitions assert arithmetic equalities, not that
the corresponding seams can be placed in a prescribed region.

**Proposition.** If `a,b>1`, then

```
La <= ab,       Lb <= ab,       Lc < ab.                 (1)
```

**Proof.** The identity `b*a=a*b` proves the first two bounds. By the
two-generator Frobenius theorem, every integer greater than
`F=ab-a-b` belongs to the nonnegative semigroup `<a,b>`. Let

```
n=floor(F/c)+1.
```

Then `F<nc<=F+c`. The strict triangle inequality `c<a+b` gives
`nc<ab`, proving the third bound. In particular all three minima exist.
This proof uses no geometric tiling assumption. QED.

Primitive integral 60-degree and 120-degree norm triples have
`gcd(a,b)=1`. The nonclassical triples have `a,b>1`. Consequently (1)
applies to all the norm candidates in the current reduction.

## Every target already has enough diameter

The following table exhibits one side of every canonical norm target
which is at least `ab` at residual scale one.

| Target row | Such a side |
| --- | --- |
| Equilateral, either norm | `ab` |
| F1, plus norm | `ab` |
| 120-degree isosceles | `bc > ab` |
| F2 | `a(a+2b) > ab` |
| F3 | `c^2 > ab` |
| F4 | `ac > ab` |

In the last four rows the plus norm gives `c>max(a,b)`. A triangle's
diameter is its longest side. Multiplying the target scale by an integer
`m>=1` cannot decrease its diameter. Thus, for **every** arithmetically
admissible norm candidate at **every** positive residual scale,

```
max(La,Lb,Lc) <= target diameter.                        (2)
```

For example, the unresolved primitive F3 candidate `(24,11,31)` has
`La=168`, `Lb=55`, and `Lc=155`, whereas its diameter is `1426`.
The isosceles candidate `(8,7,13)` for 154 has exchange lengths
`La=40`, `Lb=21`, and `Lc=39`, and target diameter `154`.
These short arithmetic relations are not tiled strips or fillings.

## Consequence for a proposed geometric proof

Suppose a source-to-relation argument were strengthened to show that
each of the three side types has a positive mixed whole-edge exchange
somewhere in any tiling, with its length bounded by the target diameter.
Discarding its position and direction would yield only (2). The
proposition proves that this resulting arithmetic test removes **no**
candidate from any norm row of the current classification.

This does not invalidate actual-seam existence statements. It identifies
the information that a successful extension must retain: the direction
and location of a seam, simultaneous placement of several exchanges, or
a stronger constraint on its permitted bank inventories. Merely proving
the existence of a sufficiently short arithmetic exchange cannot bridge
the remaining gap.

The accompanying checker independently computes the three minima for a
finite set of primitive plus/minus norm triples and checks every
applicable row. These finite checks supplement the universal elementary
proof; they are not its basis. No claim about full problem 634 is made.
