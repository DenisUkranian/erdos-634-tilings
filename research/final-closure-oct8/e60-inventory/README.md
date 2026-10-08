# E30: finite direction inventories still leave formal survivors

8 October 2026. The equilateral target has vertices `(0,0),(30,0),(0,30)`
in Eisenstein coordinates, and area equal to 60 tiles `(3,5,7)`.
**This directory does not prove or disprove its tileability.**

## A central population bound

Each outer side is a concatenation of whole tile sides. If x, y, z count
its length-3, length-5, and length-7 edges, then

```
3x+5y+7z=30.
```

The least possible x+y is 3. For example, the residue condition
`3x+5y=2 (mod7)` has no solution with x+y<=2. All these short boundary
edges belong to height zero, so the three sides need at least nine such
edges. A tile has at most two short edges; hence n_0>=5. Together with
the established congruence `n_0=60=4 (mod7)`, this proves

```
n_0 >= 11.
```

In fact a tile inside an equilateral triangle cannot have both short
edges on its boundary: their common angle is 120 degrees, while two
outer sides meet at 60 degrees. This gives n_0>=9 directly and the same
congruence strengthens it to 11.

The companion [structure proof](../e60-structure/STRUCTURE.md) supplies
`n_h>=14` for every occupied nonzero height and excludes height gaps.
Thus there are at most four consecutive occupied heights containing zero.
At four heights the only population possibilities are central 18 with
three populations 14, or central 11 with one population 21 and two 14.

## Complete signed direction recurrence

Put `rho=exp(i*pi/3)`, `z=(3+5rho)/7`. At height h use the twelve
counterclockwise orientation types A_j,B_j, j=0,...,5, whose two directed
short edges are respectively

```
A_j: 3 rho^j z^h, 5 rho^(j-1) z^h;
B_j: 5 rho^j z^h, 3 rho^(j-1) z^h.
```

Their long edges have heights h-1 and h+1. Let A_h,B_h be the three
signed counts, subtracting the opposite orientations j+3 from j.
Set `R²(v0,v1,v2)=(-v1,-v2,v0)`. Exact direction-current matching is

```
J_h = 3A_h - 5R²A_h + 5B_h - 3R²B_h
      - 7A_(h+1) + 7R²B_(h-1),
J_0 = (30,-30,30), J_h=0 for h!=0.
```

`direction_dp.py` exhaustively propagates the pair `(A_h,B_(h-1))`.
For every candidate B_h it reconstructs A_(h+1) by this identity and
keeps only integral vectors. A population n is compatible with signed
counts only if `n>=|A|_1+|B|_1` and their difference is even. The required
population congruences and the lower bounds above are imposed.

Only the lowest feasible accumulated population is retained at a fixed
state. Increasing a layer population by 14 permits seven cancelling
antipodal pairs and preserves its signed data. The code checks every
possible next admissible local population rather than rejecting a state
merely because its smallest population fails the geometric filters.

## Necessary local geometry

`line_filter.py` expands all unsigned inventories realizing each signed
layer/population. On any affine line at nonzero height, the residues of
its short edges, `(3,-3,5,-5)`, sum to zero modulo7. Every such multiset
splits into minimal zero-sum multisets of size at most7. Exact dynamic
programming over these atoms bounds how many lines can carry a given
edge kind. Same-sign edges on each line have disjoint interiors, so their
length sum is at most the target's exact maximum parallel chord.

For unit direction `(x,y)=rho^j z^h`, that chord length is

```
900 / (max(0,-30y,30x)-min(0,-30y,30x)).
```

If an orientation occurs n times, its gamma vertices are intersections
of two such line families. Therefore n cannot exceed the product of
those two line-count upper bounds.

At height zero, one outer line in each axis family is permitted and its
short-edge inventory must solve the side equation above. The remaining
lines obey the zero-residue condition. Boundary gamma vertices cannot
lie at intersections of two outer lines, so the available vertices for
a boundary edge are bounded by the *interior* lines in its other family.
The filter keeps all outer-line inventory choices passing these necessary
constraints. It does not require that separate line partitions admit a
common placement.

## Outcome

All five reflection-representative bands of widths two, three and four
still have formal survivors. Their JSON files include the full signed
layers, chosen populations, and explicit unsigned orientation inventories
passing the implemented necessary filters. These are **not coordinates
of placed triangles**, and do not establish any positive tiling.

In particular, for support `[0,1,2,3]` there is a survivor with populations
`(18,14,14,14)`. Thus these direction and individual-line invariants do not
eliminate the four-height case. A geometry argument retaining incidence
between line families, or a full positioned search, is still needed.

Reproduce a run from the repository root:

```
python3 research/final-closure-oct8/e60-inventory/direction_dp.py --support 0,1,2,3 --seconds 120
```

A resource cutoff reports `INCOMPLETE`; no timeout is an impossibility
result. Only written necessary inequalities and explicit formal controls
are claimed here, not a solver certificate for unrestricted tilings.
