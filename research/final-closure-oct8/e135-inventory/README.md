# E45: at most nine occupied heights, with formal high-width survivors

8 October 2026. The target is the equilateral triangle of side45, to be
tiled by 135 congruent `(3,5,7)` triangles. This note gives necessary
conditions only. It does not decide whether that tiling exists.

## An elementary exclusion of ten occupied heights

Set `rho=exp(i*pi/3)`, `z=(3+5rho)/7`, with height zero on the exterior
sides. Let `n_h` be the number of tiles whose short sides have height h.
Population divisibility gives `7 | n_h` for nonzero h and
`n_0=135=2 (mod7)`. The geometric exclusion of population seven at a
nonzero height, proved in [the E30 structure note](../e60-structure/STRUCTURE.md),
does not depend on the target size and therefore gives `n_h>=14` here too.

Every outer side has length45, which is not divisible by7, so each of
the three sides contains a short tile edge. A tile cannot put both of
its short edges on two exterior sides: its angle120 exceeds the exterior
corner angle60. Thus these edges belong to at least three height-zero
tiles. The congruence strengthens `n_0>=3` to `n_0>=9`.

Use the signed orientation vectors `A_h,B_h` and the exact current
recurrence from [the E30 inventory proof](../e60-inventory/README.md):

```
J_h = 3A_h-5R²A_h+5B_h-3R²B_h-7A_(h+1)+7R²B_(h-1),
R²(v0,v1,v2)=(-v1,-v2,v0),
J_0=(45,-45,45), J_h=0 for h!=0.
```

The linear character `chi(v)=v0-v1+v2` satisfies `chi(R²v)=chi(v)`.
Write `a_h=chi(A_h)`, `b_h=chi(B_h)`, `D_h=b_h-a_h`. The scalar recurrence is

```
135 * 1_(h=0) = 2D_h-7a_(h+1)+7b_(h-1).
```

Summing over all heights gives `9 sum D_h=135`, while summing after
multiplication by `(-1)^h` gives `-5 sum (-1)^h D_h=135`. All sums are
finite because the tiling is finite. Hence

```
sum D_h=15,   sum (-1)^h D_h=-27,
sum_(h odd) D_h=21.                              (1)
```

At every nonzero height the scalar recurrence modulo7 gives `7|D_h`.
Every tile contributes +1 or -1 to D_h, so `D_h=n_h (mod2)`.
Consequently `D_h=n_h (mod14)` for nonzero h. Equation (1) therefore yields

```
sum_(h odd) n_h = 7 (mod14).                     (2)
```

At least one odd height has an odd multiple of7 tiles, hence at least21.
If ten heights were occupied, the population budget already forces
`n_0=9` and all nine nonzero populations equal14. This contradicts (2).
Eleven or more occupied heights exceed the budget immediately. Therefore

**Every such 135-tiling has at most nine occupied short-height classes.**

This bound does not require consecutive support or any computer check.
More generally, for an equilateral target of side `15m` the same two
sums give `sum_(h odd)D_h=7m`, and therefore

```
sum_(h odd) n_h = 7m (mod14).
```

## Exact finite-direction DP

`direction_dp.py` and `line_filter.py` adapt the previous fully documented
E30 recurrence to N135 and side45. The central floor is9; other occupied
heights have floor14. The maximum chord in unit direction `(x,y)` is

```
2025 / (max(0,-45y,45x)-min(0,-45y,45x)).
```

The local filters use all unsigned orientation expansions, signed
supporting-line residues, exact chord capacities, gamma-vertex intersection
bounds, and exact short-edge inventories on the outer sides. They still
lose incidence between distinct lines and between different heights.

The retained batch tests consecutive bands containing zero, up to
reflection. Its outcome is:

| Occupied-band width | Reflection types | Outcome |
|---|---:|---|
| 10 | 5 | All exact formal inventories excluded |
| 9 | 5 | All retain explicit formal survivors |
| 8 | 4 | One formal survivor; three runs stopped at their 12-second budgets |

The ten-height exclusion has the independent elementary proof above, so
it need not rely on the larger geometric filter. The width-nine JSON files
contain signed and unsigned inventories passing every implemented filter.
They are **not placed triangles**. Thus these current and individual-line
constraints do not close the remaining geometry.

The three width-eight timeouts are recorded as `INCOMPLETE`; no negative
conclusion follows. The batch took approximately47.5 seconds. No further
searches are left running.

Reproduce the budgeted batch from the repository root:

```
python3 research/final-closure-oct8/e135-inventory/run_batch.py
```

The JSON `batch_report.json` records all cases and scopes. This directory
makes no claim that all tilings have consecutive support; that requires
the separate no-gap analysis. The elementary nine-class bound itself does
not require that analysis.
