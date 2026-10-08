# Complete direction inventories reduce 154 to at most eight heights

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
This is a necessary restriction, not a solution of 154 or Erdős 634.

**Result.** For the `(91,91,154)` target and `(8,7,13)` tile, no formal
orientation inventory with exactly 154 tiles can satisfy all directional
length currents and height-population congruences if its occupied short
heights form an interval of length 9, 10, 11, or 12. Every interval of
length 8 containing zero has an exact formal inventory satisfying these
conditions. The latter are not geometric tilings.

Combining the negative part with the [no-gap theorem](../heights/HEIGHT_GAPS.md),
the existing population bound, and the supplied two-height exclusion,
every hypothetical tiling of this 154 candidate has a consecutive interval
of **three through eight occupied heights**, hence height span at most 7.
There are 33 such intervals containing zero. Reflection pairs leave 18
representatives. No positioned feasibility decision for these intervals
is claimed here.

## 1. All six directions, both chiralities

In Eisenstein coordinates let `rho=exp(i*pi/3)` and `z=(8+7rho)/13`.
A direction of short height h and rotation j is `rho^j z^h`. After
reversing negative directions, a signed length current at a fixed height
is a vector with three coordinates for j=0,1,2; j+3 has negative sign.

There are two gamma-anchored reference triangles, with vertices

    T_A = (0, 8, 7rho²),     T_B = (0, 7, 8rho²).

Both are counterclockwise. At height h and rotation j their oriented
edge data `(height,rotation,length)` are

| Type | First short edge | Long edge | Last short edge |
| --- | --- | --- | --- |
| A | `(h,j,8)` | `(h-1,j+3,13)` | `(h,j+5,7)` |
| B | `(h,j,7)` | `(h+1,j+2,13)` | `(h,j+5,8)` |

Let A_h and B_h be signed three-vectors: for each type and each j=0,1,2,
subtract the count at rotation j+3 from the count at j. If R denotes
rotation by 60 degrees on these vectors, then

    R²(v0,v1,v2)=(-v1,-v2,v0),     R³=-I.

The total short current at height h is therefore

    S_h=(8I-7R²)A_h+(7I-8R²)B_h.                    (1)

The long edges arriving at that height contribute `-13A_(h+1)` and
`13R² B_(h-1)`. Counterclockwise target currents are

    F_0=(154,0,0), F_1=(0,0,91), F_-1=(0,-91,0),
    F_h=0 otherwise.

Thus an actual tiling, including one with T-junctions, necessarily satisfies

    S_h-13A_(h+1)+13R² B_(h-1)=F_h.                 (2)

Splitting contacts into atoms justifies cancellation; only positions have
been discarded here. This system is stronger than retaining just the
alternating character studied in [the first inventory check](INVENTORY_SUPPORT.md).

## 2. Exact population cost and finite search

For prescribed signed vectors A_h,B_h, the least unsigned population is
at least `s=||A_h||_1+||B_h||_1`. Every n>=s with n=s modulo 2 can realize
these signed vectors as a formal inventory: insert cancelling pairs of
opposite rotations to absorb the even excess.

For an occupied height impose the established congruences

    n_0=11 (mod 13),   n_h=0 (mod 13) for h!=0,
    n_h>0.

Let c_h(A,B) be the smallest n satisfying these conditions, the L1 bound,
and parity. This is calculated with integers, by rounding to the proper
residue modulo 13 and adding 13 if the parity is wrong.

Fix an occupied interval [L,U] containing zero, of length K. At the start,
`B_(L-1)=0` and the equation one height below the interval fixes

    A_L=-F_(L-1)/13.                               (3)

The dynamic-programming state is `(A_h,B_(h-1))`, together with the least
total cost through height h-1. Try every integer B_h with bounded L1 norm.
Equation (2) then fixes the next vector:

    A_(h+1)=(S_h-F_h)/13+R²B_(h-1).                 (4)

All three coordinates of S_h-F_h must be divisible by 13. Add the cost
c_h and retain only the cheapest path to the same successor state.
Every future condition depends only on that state, so this minimization
is exact. Discarding a cost that, even after the minimum positive costs
for remaining heights, exceeds 154 is also valid.

Every height other than zero has population at least 13, and height zero
at least 11. Hence any one B_h in a valid solution satisfies

    ||B_h||_1 <= 154-[11+13(K-1)]+13 = 169-13K.      (5)

The bound is two units looser than necessary for h=0 and is safe for all
heights. The code enumerates every integer three-vector within (5), groups
them by the residue of `(7I-8R²)B` modulo 13, and uses the appropriate
residue bucket for each state. This grouping loses no candidate.

At the upper end require both

    A_(U+1)=0,     13R²B_U=F_(U+1),                 (6)

which enforce the last in-band equation and the equation just above it.
All more distant equations are zero. Equations (3) and (6) also cover the
one-sided intervals ending or beginning at height zero.

The implementation has time and state limits. A breached limit returns
`INCOMPLETE`. None of the excluded intervals reaches either limit: each
ends by exhausting all integer states.

## 3. Checked conclusions and controls

The exact dynamic program exhausts all 42 intervals of lengths 9 through
12 containing zero and returns no inventory for any of them. For each of
the eight intervals of length 8, it produces an inventory. Its possible
deficit from 154 is a multiple of 26: the alternating boundary equation
fixes even total population and the height congruences fix residue 11
modulo 13. Cancelling pairs at height zero fill that deficit.

The positive inventories are replayed without using (1) or (4): expand the
signed vectors to all twelve nonnegative rotation counts, list the three
edge directions from the table above, and sum their signed lengths.
Every replay gives exactly 154 tiles and target currents F. This checks
the recurrence against a separate direct-edge representation.

The eight-height witnesses show that this full directional inventory
cannot itself yield a two-height normal form or an impossibility proof.
Positions remain essential.

Reproduce all exclusions and the positive controls with:

```sh
python research/closure-position-oct7/dual/check_directional_supports.py
```

The output is `directional_supports_verified.json`. The weaker Laurent
checker and exploratory SciPy runs are retained as additional diagnostics.
Their solver statuses are not used in the exhaustive proof above.

A separate [backward checker](../global/check_full_inventory_backward.py)
derives the edge matrices from exact coordinates and reproduces all 42
negative supports without resource cutoffs; it also independently expands
the eight witnesses. See the [saved audit](../global/FULL_INVENTORY_AUDIT.md).
