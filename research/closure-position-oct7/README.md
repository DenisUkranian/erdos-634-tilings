# Erdős 634: finite direction bands and the remaining 154 search

Research directed by Denis Paliy, with ChatGPT assistance. Results developed
7–8 October 2026; separate exact checking implementations preserved.

**Erdős 634 remains unresolved. Neither 154 nor 4830 is decided by this
package.** The principal new necessary conclusion is:

> Any tiling of the `(91,91,154)` triangle by `(8,7,13)` triangles must
> have **three through five consecutive occupied short-edge heights**,
> including height zero.

Here `rho=exp(i*pi/3)`, `z=(8+7rho)/13`, and a short edge of height h has
unoriented direction `rho^j z^h`. Rotations by 60 degrees belong to the same
height. The result leaves exactly 12 intervals, or seven up to reflection.
It excludes neither the remaining intervals nor all their placements.
Arbitrary T-junctions are allowed throughout.

## Proof dependencies and exact checks

| Step | Result | Proof / reproducible evidence |
| --- | --- | --- |
| Supplied positional obstruction | At least three heights are necessary | [Original proof and certificate](../position-currents-oct7/PROOF.md); [fresh independent replay](input-audit/AUDIT.md) |
| Empty-height cut | For an I120 target, an empty positive height forces the higher tail count to be divisible by `c²`; reflection gives the lower-tail statement | [Whole-edge proof](heights/HEIGHT_GAPS.md); [separate audit](global/HEIGHT_GAPS_AUDIT.md) |
| Consecutive support | When `N<c²` and `c` does not divide N, the occupied heights form an interval containing zero | Same proof, combined with the established [population congruences](../i120-global-oct7/HEIGHT_LEVELS.md) |
| Initial count bound | For 154, at most twelve heights occur | `n_0=11 mod 13`, and each other occupied population is a positive multiple of 13 |
| Supporting-line geometry | Every occupied nonzero height has at least 26 tiles, including internal heights; a 13-tile height would force two coincident tiles | [Proof with nine-case table](oct8-structural/NO_THIRTEEN_HEIGHT.md), [exact checker](oct8-structural/check_no_thirteen_height.py) |
| Current sharp bound in this package | All six supports of length 6 are excluded; lengths 7 and above require at least 167 tiles | [Updated direction proof](oct8-structural/DIRECTION_BAND_UPDATE.md), [forward checker](oct8-structural/check_all_height_direction.py), [independent backward check](global/all_height_backward_verified.json) |
| Remaining formal controls | All five length-5 intervals pass the strengthened inventory test | These are exact unsigned inventories satisfying the necessary currents and new population bounds, **not tilings** |
| Complete signed-direction inventory | All 42 intervals of lengths 9–12 are impossible even before positions are required | [Proof](dual/DIRECTIONAL_SUPPORT.md), [forward checker](dual/check_directional_supports.py), [independent backward checker](global/check_full_inventory_backward.py) |
| Limit of the earlier inventory test | Every one of the eight length-8 intervals passed before supporting-line geometry was imposed | Those earlier formal inventories are excluded by the new positional theorem |

The [full inventory audit](global/FULL_INVENTORY_AUDIT.md) explains why the
finite enumeration and pruning are complete. The independent checker
constructs the edge signatures from rational Eisenstein coordinates,
traverses heights in reverse, enumerates the opposite chirality's signed
vectors, and tries admissible populations directly. Its negative search
has no time or state cutoff. This is internal implementation diversity,
not external mathematical refereeing or formal proof-assistant verification.

The new [supporting-line audit](global/NONZERO_HEIGHT_AUDIT.md) separately
derives the short-edge signatures from exact coordinates and checks all
108 thirteen-tile inventories. It then reruns the strengthened direction
test backward, excluding all six six-height supports without a resource
cutoff. This is the independent audit of the current three-to-five bound.

The earlier [alternating-character inventory](dual/INVENTORY_SUPPORT.md)
is weaker: it rules out 15 of the original 75 intervals and admits formal
inventories in the other 60. It is retained as a separate consistency check.
Its remaining inventories do not override the stronger full-direction test.

## General exact lattice statement

For any primitive integral 120-degree tile, write

    c²=a²+ab+b²,  O=Z[rho],  z=(a+b*rho)/c.

There is an Eisenstein integer omega and a unit epsilon with
`a+b*rho=epsilon*omega²`, `Norm(omega)=c`, and coprime conjugate factors.
For a short-height interval `[L,U]`, the finite-band vertex lattice is exactly

    Lambda_[L,U] = sum_(h=L)^U z^h O
                 = z^L * conjugate(omega)^(-(U-L)) O.

Its covolume is `sqrt(3)/(2*c^(U-L))`. The proof and its scope are in
[EXACT_BAND_LATTICE.md](global/EXACT_BAND_LATTICE.md). Positive-length contact
connectivity also gives the universal count-dependent bound
`U-L<=2(N-1)`. Thus a fixed tile, target and count do admit a finite complete
placement formulation. This does **not** supply a structural classification
of all N; fixed-N decidability was already available in the repository.

The actual positioned-current criterion requires a nonnegative **integer**
solution. A formal direction inventory or a nonnegative fractional solution
is not promoted to a geometric tiling. The lattice test is a regression for
the algebraic identity, not a proof by checking finitely many tiles.

## Reproduce the mathematical checks

From the repository root, using ordinary Python 3 without `-O`:

```sh
python research/closure-position-oct7/oct8-structural/check_no_thirteen_height.py
python research/closure-position-oct7/global/check_no_thirteen_independent.py
python research/closure-position-oct7/oct8-structural/check_all_height_direction.py
python research/closure-position-oct7/global/check_all_height_backward.py
python research/closure-position-oct7/dual/check_directional_supports.py
python research/closure-position-oct7/global/check_full_inventory_backward.py
python research/closure-position-oct7/dual/check_inventory_supports.py
python research/closure-position-oct7/global/check_exact_band_lattice.py
```

These commands use only the Python standard library. The supporting-line
checker prints its exact certificate; the direction and lattice checkers
write fresh JSON reports beside their scripts. Run each backward checker
**after** its corresponding forward checker: it replays those witnesses
and records the exact input report's SHA-256. Expected totals:

- Supporting-line geometry: 108 inventories excluded, represented by nine symmetry orbits.
- Strengthened inventory: six excluded supports and five positive formal controls.
- Complete inventory: 42 excluded supports and eight positive formal controls.
- Alternating inventory: 75 supports checked, 15 excluded and 60 formally feasible.
- Lattice regression: 68 primitive ordered triples and 544 band checks.

To replay the original supplied two-height positional certificate, first
copy [its directory](../position-currents-oct7/README.md) to a working area
and run `python reproduce.py` there. That separate pipeline needs NumPy,
SciPy and GNU g++ with C++17, and generates a few hundred MB of working data.
The imported source and its frozen manifest are preserved unchanged.
Our [fresh audit](input-audit/AUDIT.md) records all 873,496 placements,
19,222,288 matrix entries and 678,493 checked forced assignments, plus the
known 88-tile positive control. No stopped search is used for that theorem.

## Remaining geometric attempts

The [compiled 154 search](search154/fixed_search.cpp) attacks actual
placements, including all compatible completion bands rather than treating
a partial placement's current support as final. Its primitive checker
compares exact geometry and corner fans with the older rational engine and
checks a known four-tile positive control. A resource-limited search status
`INCOMPLETE` is not an exclusion. Any future exhaustive result would need
its own complete-search and certificate audit.

The [4830 construction probes](f3/README.md) combine known positive F4
macros with ordinary triangular grids, and also test a 792-tile residual
quadrilateral. They have produced no positive 4830 certificate and no
unrestricted impossibility proof. The established constructions of
`4830m²` for all `m>=2` do not resolve `m=1`.

The required missing step remains geometric existence for the surviving
small scales, or a new sufficient construction theorem. None of the results
in this package relies on the candidate W/beta scale-one exclusions or on
the proposed all-primes proof.
