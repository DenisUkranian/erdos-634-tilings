# Small-scale W/beta investigation: a limited completed audit

9 October 2026. Research for Denis Paliy with ChatGPT assistance.

**The entire small-scale problem has NOT been solved.** This package contains
six complete fixed-tile refutations, a short uniform deduction at u=1,m=1,
and explicitly unfinished searches. It neither establishes that m>=v is
necessary nor proves a complete classification of Erdős 634.

The six finite exclusions are verification results, not claims of new numbers
or priority. For example, 17 and 26 have other, classical realizations: the
fixed-shape exclusions below must not be confused with global exclusions.

## 1. Exact statements verified by the finite proof trees

| u,v,m | Family | Tile | Target sides | Tile count | Proof nodes |
|---|---|---|---|---:|---:|
| 1,2,1 | W | 2,3,4 | 8,7,6 | 7 | 15 |
| 1,2,1 | beta | 2,3,4 | 8,8,11 | 11 | 52 |
| 2,3,1 | W | 6,5,9 | 27,28,15 | 14 | 93 |
| 2,3,1 | beta | 6,5,9 | 27,27,46 | 23 | 490 |
| 1,3,1 | W | 3,8,9 | 27,17,24 | 17 | 91 |
| 1,3,1 | beta | 3,8,9 | 27,27,26 | 26 | 805 |

Each row means that the specified target cannot be tiled by congruent copies
of the specified tile. Reflections and arbitrary T-junctions are allowed.
The total proof forest has 1546 nodes and 552 terminal contradictions.
The independent replay accepted every node. It uses neither a direction band,
a chosen coordinate lattice, the disputed reverse-apex argument, the packing
lemma, nor the stronger chain/area pruning options of the exploratory search.
It does not machine-prove the geometric completeness argument below.

## 2. Why the corner proof is exhaustive

Fix a finite tiling extending a valid nonoverlapping partial placement. Its
unfilled region has polygonal boundary. Choose a boundary sector of angle
strictly between zero and pi. Any completion must have a tile vertex at that
corner: a tile interior or relative interior of its edge occupies respectively
2pi or pi locally and cannot fit the sector. The tile adjacent to the outgoing
boundary ray has a full side on that ray. That side need not end at the end of
the currently displayed boundary atom: overrun is allowed whenever geometrically
possible, so T-junctions are not forbidden.

For a scalene tile, the length of that outgoing side and the length of the other
side incident to the corner have exactly six ordered choices. The law of cosines
then determines the third vertex on the left of the outgoing ray. Retain exactly
those triangles lying in the corner sector, contained in the original target,
and having no interior overlap with already placed tiles. Every completion
contains one of them. Thus it is valid to branch on this finite list at any such
sector. An empty list is a contradiction. Induction over a finite proof tree
whose branch lists are all complete proves nonexistence.

For the chosen instances every generated coordinate is rational in the metric
x^2+D y^2. The verifier computes required square roots exactly and rejects a
nonrational or invalid operation rather than treating it as a contradiction.
It reconstructs the entire residual boundary from the original target and all
placed triangles at each node. It verifies that the recorded outgoing/incoming
rays delimit a convex unfilled sector, independently generates all six side-based
placements, and requires exact equality with the recorded branch list.

The generator and verifier are separate implementations. The verifier imports
no search code. Both use exact rational arithmetic. The second code verifies
geometry by a separating-axis criterion; this implementation independence is
not external mathematical refereeing or a formalization in a proof assistant.

## 3. A uniform short deduction: u=1 at scale one

Use the established project theorem that every outer side of a W or beta target
contains two consecutive whole c-edges [A]. Put

    a=v, b=v^2-1, c=v^2, v>=2.

The scale-one W side of length 2v^2-1 is shorter than 2c. It is therefore
impossible. This W deduction was already recorded in the earlier work.

For the scale-one beta target, the base has length 3v^2-1. Let A,B,C be its
nonnegative counts of a,b,c edges. The cited theorem gives C>=2. Hence

    Av+B(v^2-1)+Cv^2=3v^2-1,
    B(v^2-1)<=v^2-1, so B<=1.

Reduction modulo v gives B=1 mod v, hence B=1. Subtraction leaves

    A+Cv=2v.

Together with C>=2 this gives A=0,C=2. Each base corner of beta contains
exactly one beta tile, whose incident sides are a,c, never b. Consequently
the only possible base word is c,b,c. It contains no consecutive c-edges,
contradicting [A]. Therefore both fixed families are impossible at m=1 for
every pair u=1,v>=2. This is a deduction from [A], not an independent proof
of [A], nor an assertion that higher scales below v are impossible.

For (u,v)=(1,2), combine these m=1 exclusions with the prior unrestricted
positive theorem at all m>=v. This reproduces the complete W/beta spectrum
m>=2 for the tile (2,3,4). The first-tile classification was already part of the
project; it is not represented as a new discovery in this package.

## 4. Exact limits of the new runs

W56 with tile (6,5,9), target (54,56,30), remains undecided. The fresh 35-second
unrestricted-direction convex-corner search examined 3828 nodes and reached
36 placed tiles. It returned **INCOMPLETE**, not a refutation.

The beta92 run for the same tile, target (54,54,92), also remains INCOMPLETE.
Both partial records are retained, clearly labelled. Neither record is a proof
of impossibility, and no partial placement is asserted to extend to a tiling.

No general proof that m>=v is necessary was obtained. No new completion at
m<v was found. The positive theorem at m>=v remains a prior input; this audit
does not replace its verification. F3/14430 was not addressed by these runs.

## 5. Reproduction

Use standard Python 3, without optimization (-O):

    python generate_certificate.py
    python verify_certificate.py *refutation.json
    python check_controls.py

The replay verifies 1546 proof nodes. A separately checked 28-tile positive
control has all 378 pairs interior-disjoint and exact boundary coverage. Deliberately
deleted proof branches, moved tiles and cyclic proof references are rejected.
No solver or nonstandard Python package is needed for these checks.

## Sources and attribution

[A] Denis Paliy, project with ChatGPT assistance, *Adjacent longest edges in every
W and beta boundary*, 7 October 2026, repository snapshot 3a0ad269:
https://github.com/DenisUkranian/erdos-634-tilings/blob/3a0ad269f645850ed9fd01bbd76a08c9b456032e/research/w-global-oct7/ADJACENT_C_EDGES.md

The finite search develops the project's convex-corner method from
research/uniform-reduction/exact_search.py at the same snapshot. This method's
finite-search principle is not claimed as a new structural classification.

The positive range m>=v is the previous attachment
Erdos634_W_beta_unrestricted_PROOF_2026-10-09.md. The prime-case PDF remains a
candidate for scrutiny and is not used here. No assertion of current arXiv status,
external acceptance or research priority is made.
