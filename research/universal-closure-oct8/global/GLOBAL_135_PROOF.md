# No 135-tiling; the complete square class 15

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
Computer-assisted proof with separate exact arithmetic, geometric reduction,
and propositional certificate checks. Internal independent checks are not
external mathematical refereeing.

**Theorem.** In Erdős problem 634, the count 135 is impossible. Consequently,
for every positive integer m,

> **15m² is realizable if and only if m >= 4.**

This closes one complete square class. It does not classify all tile counts.

## 1. Reduction of every shape and tile

The [all-branch arithmetic gate](../../final-closure-oct8/arithmetic-gates/README.md)
uses the published exhaustive angular classification and rationality inputs
with the thirteen necessary integer-scale spectra. At 135, the four
arithmetic candidates are:

| Branch | Primitive tile | Target sides |
|---|---|---|
| Equilateral 120-degree | (3,5,7) | (45,45,45) |
| Group-1 theta | (4,15,16) | (180,180,45) |
| Group-1 theta | (56,15,64) | (360,360,315) |
| Double angle | (49,15,56) | (315,315,360) |

The two latter rows violate the necessary whole-seam bounds 45 >= 56 and
45 >= 49, respectively. The (4,15,16) row requires at least two whole
16-edges on its base; the remaining 13 cannot be a sum of 4 and 15.
The classical cases are excluded by the squarefree part 15 and the odd
3-adic valuation. Thus only the equilateral side-45 instance remains.
The [written small-count reduction](../../final-closure-oct8/class15/REDUCTION.md)
gives these arguments and the exact independent parameter enumeration.
No proposed W/beta scale-one exclusion or prime-case candidate proof is used.

## 2. Every possible tiling is in one of five full direction bands

Put rho=exp(i*pi/3), eta=2+rho and z=eta/conjugate(eta)=(3+5rho)/7.
The short edges of a tile at height h have directions rho^j z^h.
Both chiralities and every rotation are permitted. The outer sides have
height zero.

The [global structural argument](../../final-closure-oct8/e135-structure/README.md)
proves that the occupied heights form a consecutive interval containing
zero. Its no-gap proof treats the possible 98-tile tail geometrically,
including full-edge interfaces, connected components, holes and the
independently checked exact cell-containment bounds. The separate
[signed-character argument](../../final-closure-oct8/e135-inventory/README.md)
proves that there are at most nine occupied heights. In particular, it
uses n_0 >= 9, n_h >= 14 at every occupied nonzero height, and the
odd-height population congruence modulo 14.

Therefore every tiling is contained in one of

    [-4,4], [-3,5], [-2,6], [-1,7], [0,8],

or its reflection. Empty heights at a band's ends are allowed, so these
five models include all shorter intervals too.

## 3. Exhaustive positioned geometry, including arbitrary T-junctions

The integral seam lemma gives the necessary vertex lattice

    Lambda[L,U] = g Z[rho],  g=eta^L/conjugate(eta)^U.

The target vertex at zero fixes its translate. This lattice follows from
the tiling; it is not a chosen coordinate mesh. At extreme long-edge
directions the full 7-edge partitions agree, so T-junctions do not add
unlisted translations.

For each height, the dictionary contains both orders of the short sides
and all six rotations, at every lattice anchor for which all three
vertices are in the target. Convexity makes the three containment tests
sufficient. The full dictionaries, compressed by integer intervals, are:

| Band | Initial placements | Independently checked range cuts | Survivors |
|---|---:|---:|---:|
| [-4,4] | 420445247592 | 49479639 | 246600 |
| [-3,5] | 420583549524 | 50644031 | 246600 |
| [-2,6] | 420309426351 | 50429425 | 246558 |
| [-1,7] | 420224867466 | 49218545 | 186798 |
| [0,8] | 420441801582 | 50973015 | 83163 |

A cut uses a positioned endpoint-current row with zero right side. If
all remaining coefficients have the same sign, every corresponding
nonnegative placement variable must be zero. Each recorded interval
checks this implication at every integer anchor in the interval.

A separately written verifier reconstructed the complete initial
dictionaries by exact scanline intersections, replayed every cut, and
compared every survivor. A further independent physical-coordinate
normalization verified that all five survivor dictionaries and their
reflections lie in one reflection-invariant pool of 246600 triangles.
Its canonical physical-coordinate hash is

    7a9182ff37328cc6e5b7c6fe822bbcf529687ecd12a0bc31927e6633d71f715a.

The detailed method, reports and reproduction command are in
[E135_REDUCTION_AUDIT.md](E135_REDUCTION_AUDIT.md). All
2,102,004,892,515 initial placements are represented; this is not a sample
or an assumption that a tiling has a particular combinatorial form.

## 4. The complete residual Boolean system is impossible

A true tiling chooses each distinct placement at most once and hence
defines 246600 Boolean variables. Summing counterclockwise tile
boundaries cancels every internal segment, including partial contacts.
The resulting positioned endpoint equations are necessary for every
true tiling.

The [independent geometric exporter check](../e135/check_unit_metric_model.py)
verifies every triangle's side lengths, area, containment and uniqueness,
and reconstructs exactly all 247770 equations and 1479600 nonzero
coefficients of the residual model. The [SAT encoding audit](../overlap-literature/SAT_AUDIT.md)
checks the sign conversion and independent auxiliary variables. The
resulting DIMACS formula has 5925966 variables and 12154716 clauses.

Native CaDiCaL 3.0.0 generated an LRAT contradiction. The separately
compiled upstream lrat-check verified the entire certificate, including
the final empty clause. The exact commands, fixed source revisions,
control tests and acceptance conditions are recorded in
[DIRECT_LRAT_SOURCE_AUDIT.md](DIRECT_LRAT_SOURCE_AUDIT.md). The final
[certificate report](direct_lrat_certificate.json) binds the CNF and
proof to their SHA-256 hashes; the retained checker log explicitly
reports VERIFIED.

Thus the entire residual Boolean system is inconsistent. Every
hypothetical tiling would yield a satisfying assignment to that system,
a contradiction. This proves the global exclusion of 135. Notice that
only necessity of the boundary equations is needed for this negative
argument; no claim about integrality of a fractional relaxation is used.

## 5. Completing the square class

The count 15 is excluded by the two-longest-edge boundary argument and
a separately replayed 102-node exact frontier certificate; see the
[small-count proof](../../final-closure-oct8/class15/REDUCTION.md).
The count 60 has a complete
[structural and positional exclusion](../../final-closure-oct8/e60-position/PROOF.md),
with independent replay of both exhaustive four-height models.
Together with the new exclusion of 135, these settle m=1,2,3 negatively.

For every m >= 4 there is a constructive
[equilateral tiling with 15m² tiles](../../final-closure-oct8/equilateral240/PROOF.md).
An independently checked 240-tile seed has side 60. The classical
trapezoid T(34,15), plus ordinary parallelogram strips, constructs
T(15m,15), since

    15m - 34 = 3(5m-13) + 5.

Attaching this band to the translated side-15m equilateral tiling
produces side 15(m+1) and adds 30m+15 tiles. Induction gives every m >= 4.
This proves the stated equivalence.

## Reproduction and scope

The geometric reduction can be regenerated and independently replayed by

```sh
python3 research/universal-closure-oct8/global/reproduce_e135_reduction.py /tmp/e135-reproduction
```

For the exported, geometrically checked endpoint model, regenerate its
CNF with the documented python-sat dependency and then independently
check a fresh LRAT proof:

```sh
python3 research/universal-closure-oct8/e135-residual/sat_certificate.py encode /path/e135-k7-center.model.txt /path/e135-k7.cnf
python3 research/universal-closure-oct8/global/reproduce_direct_lrat.py /path/e135-k7.cnf /path/e135-direct --cadical /path/cadical/build/cadical --checker /path/lrat-check --seconds 2400
```

A timeout is not an exclusion. Earlier limited searches, the unverified
DRAT attempt, the unfinished native pseudo-Boolean run and fractional LP
runs are not premises of this proof. The LRAT proof is supplied as a separate
compressed artifact. The geometric range traces are regenerated by the
commands above; their hashes and exact reproduction programs are retained
in the repository. Historical notes that describe
135 as unresolved record the state before this completed certificate.
