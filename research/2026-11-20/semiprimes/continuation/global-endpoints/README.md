# Unrestricted endpoint searches for the residual semiprimes

20 November 2026. Denis Paliy's Erdős 634 project, with ChatGPT assistance.

**3431 and 5063 remain open.** This continuation supplies a finite global
certificate criterion, exact independent checkers, an unrestricted integer
search, and a separate arithmetic audit. It contains neither a complete tiling
nor a global nonexistence certificate for either original board. It does not
complete the semiprime classification.

## The precise remaining geometry

Write T(N) for existence of some triangle tiled by N congruent triangles,
allowing reflections and T-junctions. For distinct primes 3<p<q of opposite
residues modulo four, the recorded arithmetic reduction leaves only

```
q < 2p,  3 divides p+q,  c²=(p²-pq+q²)/3,
a=(2q-p)/3,  b=(2p-q)/3.
```

The unique possible tile has sides (a,b,c), and the exterior sides are
ap, bq, c². An arithmetic candidate is not a construction. The existing
[sharp staircase](../../staircase/SHARP_STAIRCASE.md) is a sufficient
construction; its necessity was proved for staircase loads only.

| N | Prime factors | Tile (a,b,c) | Exterior sides, sorted | Reduced (a+c)/b |
|---:|---|---|---|---|
| 3431 | 47 × 73 | (33,7,37) | (511,1369,1551) | 10/1 |
| 5063 | 61 × 83 | (35,13,43) | (1079,1849,2135) | 6/1 |

The separate [arithmetic audit](AUDIT.md) enumerates all 210,035 semiprimes
through one million, with repeated primes included. Its seven residual mixed
F2 products are 3431, 5063, 19367, 60023, 64367, 271151, and 641591.
The census separately retains eighteen distant BQ/I120 candidates whose
exclusion depends on the recorded geometric manuscripts; it does not silently
promote those manuscripts to independently verified inputs. With those inputs
admitted, the census has 55,359 positive, 154,669 negative, and seven open
entries. See [the machine-readable census](census_million.json) for the
dependency-sensitive categories.

## A finite test that is genuinely global

Associate to an oriented side its signed start and end on its supporting line.
The endpoint-current vectors of tiles add to that of their board. Subdividing
either bank leaves these vectors unchanged, so this identity includes partial
contacts and T-junctions.

For any specified endpoint and unoriented side direction there are at most
24 congruent placements: three side lengths, two directions on the line, two
choices of the other incident side, and two hands. Thus a finite table of
endpoint weights has only finitely many potentially nonzero tile scores.
The enumeration is complete over all real rigid placements. It does not assume
a fixed orientation range, a preselected translation lattice, or a frozen
corner packing.

Let B be the weighted board current. Optionally choose exact points with
nonnegative penalties λ_r, and subtract λ_r from a tile's score when the point
lies strictly inside it. Let U_N be the sum of the N largest positive adjusted
scores among distinct contained candidates, padding with zero if necessary.
Then

```
B - sum(λ_r) > U_N
```

is an exact global nonexistence certificate. Every actual tiling has N distinct
placements and at most one tile interior at any penalty point. Unenumerated
placements have nonpositive adjusted scores. The full argument, boundary
arithmetic justification and certificate format are in
[ENDPOINT_DUAL.md](ENDPOINT_DUAL.md).

The independent checker uses rational arithmetic and the cosine law. It does
not import the search engine's orientation templates. **No passing certificate
for 3431 or 5063 has been found.**

## Integer and fractional searches

The [integer search](integer/README.md) completes selected endpoint equations
by enumerating all 24 incident placements. All exterior boundary placements
are also enumerated. A true tiling projects to a satisfying assignment of this
finite necessary model: omitted tiles have zero contribution to every completed
row and to the external boundary. It follows that a verified UNSAT result for
the completed model would be global even though not every interior placement
has been generated.

Uncompleted equations are used only as temporary assumptions to guide
expansion. An UNSAT core containing any such assumption is **inconclusive**.
Every recorded target core in this continuation still has temporary
assumptions. Resource interruptions are also inconclusive.

The [LP search](lp/README.md) starts from the earlier exact signed polygon
identities: 3506 positive minus 75 negative copies for 3431, and 5071 minus
8 for 5063. It adds previously omitted placements, missing endpoint equations
and exact point-coverage inequalities. No initial tile is frozen. Its primary
objective also includes artificial endpoint errors and must not be described
as the minimum possible number of negative tiles. A partial zero objective,
or even a complete fractional cover, is not an ordinary tiling.

The global pricing oracle found many omitted placements violating earlier
restricted duals. In particular, the prior restricted optimum of eight
negative tiles cannot be quoted as an unrestricted lower bound. It remains
a result about its specified finite placement pool.

## Independent positive control

Both search approaches recover the known 143-tiling for sides (5,3,7).
The [exact tile list](tiling_143.json) is checked by
[verify_endpoint_tiling.py](verify_endpoint_tiling.py), which reconstructs
the physical geometry independently. It checks 143 distinct congruent tiles,
containment, area and exact cancellation of the full oriented endpoint current.
Positivity and that current identity imply multiplicity-one coverage and
disjoint tile interiors. This is a verification of the known construction,
not a new 143 result.

## The separate two-height experiment

The [catalogue experiment](two_height/README.md) includes every real placement
using at most two short heights, after a proved lattice normalization. Its
corner and line filters preserve all 143 tiles of the control. At 3431 they
reduce 311,334,312 placements to a nonempty fixed point of 128,146,772.
The result is OPEN. The 5063 run was interrupted before a fixed point.
Neither result decides a two-height tiling, much less the unrestricted problem.
See the [scope audit](AUDIT_TWO_HEIGHT.md).

## Reproduce the finite checks

Run from this directory with Python 3 and assertions enabled:

```sh
python replay.py
```

This checks the global dual verifier's controls, the exact positive 143
certificate, rejection of corrupted positive data, and the independent
semiprime census. It does not rerun the large, inconclusive searches or certify
the geometric manuscript inputs to the arithmetic reduction.

The search-specific instructions and dependencies are in the two solver
directories. [Search status](SEARCH_STATUS.json) separates complete controls,
restricted pruning, finite-pool optimization and unresolved target searches.

## What would close the gap

A positive answer needs an exact integral tile list passing the independent
geometric checker. A negative answer needs a passing global dual, a completed
integer-model refutation with its encoding and proof independently checked,
or a universal geometric theorem. Failure of a staircase, a selected cavity,
two chosen heights, or a finite placement pool cannot supply that conclusion.

In particular, the missing implication is not another arithmetic identity:
it is a necessity theorem or a new construction for the residual F2 unit
boards. The [v=1 gap note](V1_CLOSURE_GAP.md) gives the exact missing
normal-form implication and an explicit unplaced inventory showing why
aggregate direction totals do not supply it. The present work supplies stronger tools for that question and leaves
its answer explicitly open. No external refereeing or formal proof-assistant
verification is claimed.
