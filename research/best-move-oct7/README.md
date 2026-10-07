# Complete square class 78 and an all-multiplier F3 sector

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

This continuation proves two general results and supplies exact positive
certificates. It does **not** solve Erdős problem 634 in full.

## 1. A complete square-class classification

For every positive integer m,

```
78m² is a congruent-triangle tiling count if and only if m is even.
```

The new 312-tile construction proves the positive direction by ordinary
subdivision. For odd m, the exhaustive necessary spectra isolate F3.
An explicit rational-point map then forces a point on
`y²=x³+156x²-2028x` with positive x and odd 2-adic valuation.
An elementary descent excludes all four possible square classes of x
modulo 13. No elliptic-curve rank, basis computation or conjecture is used.

- [Complete proof](new-arithmetic/CLASS78.md).
- [Independent internal proof audit](geometry/CLASS78_AUDIT.md).
- [Exact arithmetic checks](new-arithmetic/check_class78.py).

## 2. A whole ordered F3 sector at every multiplier

Let positive integers a,b,c satisfy `c²=a²+ab+b²`. For every positive
integer m, the triangle with side lengths

```
m*c², m*c*(a+2b), 3m*b*(a+b)
```

has a tiling by `3(a+b)(a+2b)m²` congruent `(a,b,c)` triangles whenever
`0<a<2b`. The part `a<b` is established here by a positive five-region
partition into three ordinary grids, one F4 triangle and one ideal
trapezoid. The part `b<a<2b` follows from the earlier
[gamma-corner theorem](../group2-gamma-corners/PROOF.md).
Neither equality a=b nor a=2b is an integral norm triple.

The new partition crosses the boundary of the previous fan remainder;
it does not assert a filling of that isolated hexagon.

- [Universal positive proof for a<b](hexagon/F3_SMALL_A.md).
- [Independent internal proof audit](geometry/F3_A_LT_B_AUDIT.md).
- [Unit-coordinate constructor](hexagon/construct_small_a.py).
- [Independent unit checker](hexagon/check_small_a.py) and
  [retained fresh report](hexagon/verification.json).

| Count | Tile | Target sides | Retained geometric evidence |
|---|---|---|---|
| 312 | (3,5,7) | (49,91,120) | [All 312 unit coordinates](hexagon/f3-312.json); exact congruence, containment, area and complete pair-overlap filtering |
| 2331 | (5,16,19) | (361,703,1008) | [All 2331 unit coordinates](hexagon/f3-2331.json); the same independent checks |
| 573390 | (136,209,301) | (90601,166754,216315) | Symbolic five-region construction and independently checked [hierarchical trapezoid seed](hexagon/trapezoid-136-209-301.json); full unit expansion is not claimed |

All geometric checks use exact rational arithmetic. The unit checker
imports no constructor or geometric helper. Supporting macro checks cover
the 87 primitive triples `0<a<b<=500` and the larger displayed example;
the parameter-uniform proof is the written argument, not this sample.

## 3. An additional F3-only membership decision and infinite family

The [arithmetic audit](new-arithmetic/COUNT_573390.md) proves that 573390
has exactly one possible ordered primitive tile, `(136,209,301)`, at
multiplier one. No other branch can realize it. The earlier sufficient
criteria recorded in this project did not cover this count; the new
construction does.

More generally, for `p=15+1650k`, k>=0,

```
a=8(p+2), b=p²-16, c=p²+4p+16,
N=6p(p+8)(p²+4p-8)
```

gives infinitely many actual F3-only counts. None is divisible by 11,
so none is a square subdivision of the earlier 990 seed. Uniqueness of
the primitive tile is asserted for 573390 only, and no external priority
claim is made.

## 4. Reproduce the supporting checks

From the repository root:

```bash
python research/best-move-oct7/hexagon/check_small_a.py
python research/best-move-oct7/geometry/check_f3_a_lt_b_audit.py
python research/best-move-oct7/new-arithmetic/check_class78.py
python research/best-move-oct7/new-arithmetic/check_573390.py
python research/group2-trapezoids/verify.py research/best-move-oct7/hexagon/trapezoid-136-209-301.json
```

The first command defaults to both retained unit certificates. This
continuation freshly reran these targeted checks and the repository
integrity/link audit. It does not claim a fresh run of every historical
suite or formal proof-assistant certification.

## 5. Remaining scope

F3 with `a>2b` is not completely classified. In particular, the count
4830, whose sole primitive F3 tile is `(24,11,31)`, remains unresolved;
its square multiples at multiplier at least two were already constructed.
The separate 154 case also remains unresolved. The
[global gap map](../../docs/global-gap-2026-10-07.md) records the other
branches. The new square-class theorem and positive sector must not be
read as a full all-N classification.
