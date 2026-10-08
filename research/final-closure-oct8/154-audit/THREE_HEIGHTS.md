# Historical scope

The three-height checks below were subsequently subsumed by the complete
five-height checks and the global reduction in [GLOBAL_154_PROOF.md](GLOBAL_154_PROOF.md).
Any references below to heights still remaining describe this intermediate stage.

# The 154 candidate needs at least four short-edge direction classes

8 October 2026. Internal independent mathematical and computational audit.
This result excludes three classes as well as the formerly excluded one-
and two-class cases. It does not exclude tilings with four or five classes.

## Statement

Suppose the triangle with sides `(91,91,154)` has a tiling by congruent
`(8,7,13)` triangles. Normalize the target to

```
P = conv(0,154,49+56 rho),   rho=exp(i pi/3),
z=(8+7 rho)/13.
```

The two short edges of each tile have directions `rho^j z^h` for a
common integer h, called its short height. Then the set of occupied
short heights has cardinality at least four.

The prior population and empty-height theorems show that this set is a
contiguous interval containing zero: see
[the empty-height proof](../../closure-position-oct7/heights/HEIGHT_GAPS.md).
The existing complete directed-inventory calculation bounds its cardinality
by five. Thus any remaining 154-tiling must have **four or five consecutive
short-height classes**, including zero. The present proof supplies the
new lower bound only; the old upper bound retains its previous source.

## Complete lattice and orientation enumeration

The existing integer-atom and extreme-edge lattice argument applies to
arbitrary T-junctions and yields

```
Lambda_[L,U] = sum_(h=L)^U z^h Z[rho]
```

for all vertices, after fixing the target vertex at zero. For three
consecutive heights centered at zero this lattice is exactly
`(1/13) Z[rho]`. Inclusion in that lattice is immediate, and the reverse
inclusion follows from the explicit identity

```
4(z+z^(-1)) - 7 = 1/13.
```

For the band `[0,2]` the lattice is `z/13 Z[rho]`; rotate the target by
`z^(-1)` to reduce it to the same denominator-13 lattice and height band
`[-1,1]`. In coordinate numerators with denominator 13 the two targets
are exactly

```
center 0: (0,0), (2002,0), (637,728);
center 1: (0,0), (2310,-1078), (1127,105).
```

For each height h=-1,0,1 and each j=0,...,5, there are two templates
whose 120-degree vertex is zero:

```
(0,8 rho^j z^h,7 rho^(j+2) z^h),
(0,7 rho^j z^h,8 rho^(j+2) z^h).
```

Their 36 possibilities include both mirror types. Every tile has a
unique 120-degree vertex, so translating these templates by every
lattice point inside the target and retaining those with all vertices
inside lists every possible tile in that band. Convexity makes the
vertex containment test sufficient. No unexplained coordinate mesh or
corner construction is imposed.

The independent enumerator obtains:

| Band in the original target | All contained placements |
|---|---:|
| `[-1,0,1]` | 17,013,246 |
| `[0,1,2]` | 16,972,710 |

Reflection `w -> 154-conjugate(w)` preserves the target and reverses h,
so exclusion of `[0,2]` also excludes `[-2,0]`. These are all three-height
intervals containing zero. Subsets of these intervals are also included
in each search, so the resulting exclusions do not assume that every
listed height is used.

## Necessary positioned endpoint equations

Orient each tile boundary counterclockwise. For an oriented edge A->B,
place +1 at A and -1 at B in the row associated to its unoriented
supporting direction. A row is identified by an exact point and a line
direction; together they specify the supporting affine line.

This is the one-dimensional distributional derivative of the signed
edge current on that line. Although the direction is stored without an
orientation, the start/end signs are correct for both edge directions:
reversing the edge reverses the signed current and exchanges its endpoints.
Summing over a tiling cancels internal edges, including subdivided edges
at T-junctions. Therefore, for each row, the sum of its tile endpoint
contributions must equal the target boundary's contribution.

Let x_j indicate whether candidate placement j is selected. A genuine
tiling has x_j in {0,1}: selecting a coincident placement twice would
produce overlap. The endpoint equations are necessary for these variables.
The refutation uses only their binary interval bounds; it need not assume
or test additional nonoverlap constraints.

For any row, let lo and hi be the minimum and maximum achievable sums
under currently assigned variables. If its right side b is outside
[lo,hi], there is a contradiction. If b equals an endpoint, every
unassigned variable with nonzero coefficient has a uniquely forced value
in that row. These deductions remain valid even over the relaxation
0<=x_j<=1.

## Independent replay

The producer `../154-cpsat/full_three_level.cpp` records individual forced
assignments. The verifier `replay_three_level.cpp` is separately written:

* it derives templates using complex multiplication by six explicit roots
  of unity and verifies every squared side and oriented area;
* it independently enumerates contained placements;
* it **scatters** all six geometric endpoint incidences of each placement
  into stored row bounds, rather than importing the producer's inverse
  template row generator or propagation queue;
* for each recorded assignment it requires a currently tight incident
  equation justifying that exact value, then updates the six bounds;
* it stops at the first independently detected contradiction.

All arithmetic is integral. Exact results are:

| Band | Justified assignments before contradiction | Terminal lower/upper | Required value |
|---|---:|---:|---:|
| `[-1,0,1]` | 17,012,488 | `[-1,-1]` | `0` |
| `[0,1,2]` | 16,972,231 | `[-1,-1]` | `0` |

The producer processes its queue in a different order and notices the
same infeasibility slightly later. Stopping at the earlier independently
verified contradiction is sufficient. No timeout or incomplete search
is interpreted as a negative proof.

This eliminates every three-height band, proving the new lower bound.
The remaining four- and five-height cases require separate arguments.

## Reproduction

From the repository root, with a C++17 compiler:

```
python research/final-closure-oct8/154-audit/reproduce.py
```

The script compiles the two distinct programs, regenerates the producer's
traces in a temporary directory, and independently replays both. Large
intermediate traces need not be committed. The retained reports are
`symmetric_replayed.json`, `asymmetric_replayed.json`, and `audit_hashes.json`.
