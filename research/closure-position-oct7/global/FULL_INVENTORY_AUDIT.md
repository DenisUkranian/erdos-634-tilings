# Independent audit of the complete directional inventory reduction

7 October 2026; saved independent replay rerun 8 October 2026. Separate
internal derivation and exact computational review. This is not outside refereeing and does not decide 154.

Reviewed:

* `../dual/DIRECTIONAL_SUPPORT.md`;
* function `run_variable` in `../dual/directional_dp_probe.py`;
* `../dual/check_directional_supports.py`;
* the full-direction reports for 8, 9, 10 and 11 occupied heights.

**Outcome: PASS.** The exact inventory exclusions safely imply that a
hypothetical 154 tiling has at most eight occupied short heights, once
combined with the independently reviewed interval-support theorem.
The supplied two-height obstruction gives a lower bound of three.
Every eight-height interval has a formal inventory, so this restriction
is sharp for the stated direction/count constraints and is not a tiling
existence or nonexistence theorem.

## 1. Independent geometric derivation of the six signed variables

The counterclockwise reference triangles are

    A: (0,8,7rho^2),     B: (0,7,8rho^2).

For A the boundary vectors are `8`, `-13*z^(-1)`, `-7rho^2`.
For B they are `7`, `13rho^2*z`, `-8rho^2`. These identities follow
by substituting `z=(8+7rho)/13` and `rho^2=rho-1`; no angular
approximation is involved.

At each height identify direction j+3 with the negative of direction j,
for j=0,1,2. The signed rotation populations of the two triangles are
three-vectors A_h and B_h. Rotation by 120 degrees is

    R2(v0,v1,v2)=(-v1,-v2,v0).

The short-edge current is

    S_h=(8I-7R2)A_h+(7I-8R2)B_h,

and the long-edge contributions at height h are `-13A_(h+1)` and
`13R2 B_(h-1)`. Thus the necessary equation is exactly

    S_h-13A_(h+1)+13R2 B_(h-1)=F_h,

where `F_0=(154,0,0)`, `F_1=(0,0,91)`, `F_-1=(0,-91,0)`.
T-junctions do not change it because splitting and cancelling collinear
segments preserves signed lengths in each actual direction.

## 2. Finite enumeration is complete

For fixed signed vectors the minimum unsigned population is their combined
L1 norm s. Any population at least s and congruent to s modulo 2 is achieved
by adding pairs of opposite rotations. Applying the established positive
population residues modulo 13 therefore gives the exact local cost used
in the program.

An interval with K occupied heights has baseline population
`11+13(K-1)`. After reserving that baseline at all other heights, every
single nonzero-height population is at most

    154-[11+13(K-1)]+13 = 169-13K.

The height-zero maximum is two smaller. Consequently the uniform bound
`||B_h||_1<=169-13K` is safe. The three nested integer loops enumerate
precisely every three-vector satisfying that bound. Grouping by the three
residues of `(7I-8R2)B` modulo 13 preserves all those candidates.

At the lower outside height the equation forces
`A_L=-F_(L-1)/13` and `B_(L-1)=0`. All entries of that F are divisible
by 13 in the cases used here. Given the state `(A_h,B_(h-1))` and a
candidate B_h, division of the three coordinates of S_h-F_h by 13 is
valid exactly when the residue test passes, and then uniquely determines
A_(h+1). The terminal conditions `A_(U+1)=0` and
`13R2 B_U=F_(U+1)` close both remaining boundary equations.

Every permitted signed inventory therefore induces a path through these
states, and every complete path satisfies all directional equations.

## 3. Population and resource pruning are safe

Keeping the least population cost for a state is valid because subsequent
choices and costs depend only on that state. All future populations are
positive and have the specified residues; subtracting their baseline
costs is consequently a valid necessary budget test. The additional
bound on `||A_(h+1)||_1` reserves the minima for every later height except
h+1, so it also cannot remove a feasible inventory.

For a complete path the sum of local costs has residue 11 modulo 13 and
is even, by the alternating character of the directional equations.
Its deficit from 154 is therefore a multiple of 26. Padding at height
zero by opposite-rotation pairs preserves the equations and congruences.
Thus the minimum-cost representation is sufficient for the **formal
inventory constraints**, even though positions have been discarded.

The time and state cutoffs return `INCOMPLETE`, never `EXACT_UNSAT`.
An `EXACT_UNSAT` output is reached only after an entire finite transition
layer has been enumerated and no states remain. None of the retained
negative reports used a resource-limit answer as an exclusion.

## 4. Independent backward dynamic-programming replay

The saved [independent checker](check_full_inventory_backward.py) derives
the three edge vectors of both counterclockwise reference triangles using
exact rational Eisenstein coordinates, and identifies each vector with its
unique length, height offset and rotation. It also derives the target
boundary from its actual vertices `(0,0),(154,0),(49,56)`. From these data
it builds the short-edge matrices and the signed-permutation long-edge
matrices; it does not import the producer's recurrence or rotation tables.

This implementation traverses the heights in reverse. Its state
was `(A_(h+1),B_h)`, with top conditions

    A_(U+1)=0,
    B_U=R2^(-1)(F_(U+1)/13),

and it enumerated A_h, rather than B_h. The recurrence was independently
solved in the other direction:

    B_(h-1)=R2^(-1)((F_h-S_h)/13+A_(h+1)),
    R2^(-1)(v0,v1,v2)=(v2,-v0,-v1).

This version enumerated possible populations directly in steps of 13 and
checked parity, rather than copying the producer's ceiling expression.
It reproduces the negative answer for **all 42 intervals of lengths
9 through 12**, without any time or state cutoff. Its state keeps the
minimum population already used above the current height; all later
conditions depend only on that state. Local admissible population costs
are found by testing the progression in steps of 13 with the correct parity,
then cached. This gives separate exact verification for every asserted
negative support. The retained report is
[full_inventory_backward_verified.json](full_inventory_backward_verified.json).

Run the forward checker first, then:

```sh
python research/closure-position-oct7/global/check_full_inventory_backward.py
```

The report records the source hash and the hash of the forward report used
for the eight positive controls. The latter is expected to change on a
new forward run because its reports include runtime observations.

## 5. Independent positive controls and remaining scope

All eight length-8 formal witnesses were independently expanded into the
twelve nonnegative rigid-rotation counts at every height. The unused even
population at each height was assigned to an opposite pair. Direct addition
of the three oriented edges, independently derived as described above,
then gave exactly

    (height0,axis0):154,
    (height1,axis2):91,
    (height-1,axis1):-91,

with every other coefficient zero. Each witness has exactly 154 tiles,
positive populations at every claimed height, and the required residues.
This check uses explicit edge contributions rather than the recurrence.

Combining this result with the no-gap theorem and two-height obstruction,
the only possible exact supports are intervals containing zero of lengths
3 through 8. Their number is `3+4+5+6+7+8=33`. Exactly three are fixed by
reflection, so there are `(33+3)/2=18` reflection orbits. A complete
geometric search may safely use span<=7. It must still allow all compatible
completion intervals for a partial placement.

The formal positive controls do not determine positions or certify a
nonoverlapping dissection. In particular, this audit does not assert that
any of the eight-height inventories is geometrically realizable.
