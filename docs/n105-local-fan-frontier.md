# N = 105: every individual convex corner can pass

**Scope.** This is an exact partial configuration for the equilateral target of
side 105 with tile sides `(5,21,19)`. It is not a 105-tiling, and it does not
exclude or establish any of the remaining N = 105 cases.

The certificate places 45 congruent tiles without interior overlap and covers
the entire outer boundary. The residual is one region of area equal to 60 tiles,
with 36 boundary vertices and 18 strictly convex corners. At **each** of those
18 corners, a separate witness supplies a complete fan of one or two tiles
covering the corner angle. Each fan fits inside the target and avoids every
already placed tile.

The fans belonging to different corners are **not asserted to be mutually
compatible**. They are alternative local witnesses, not a single extension of
the collar. Consequently, testing full fans independently at every convex
corner still does not reject this particular partial configuration. A stronger
argument must impose compatibility between local choices or propagate further
into the remaining region.

This configuration is distinct from the two collars in
[the fixed-collar obstructions](n105-fixed-collar-obstructions.md). Their exact
nonextendability proofs remain valid. No extendability claim is made here for
this new configuration.

## Exact data and replay

- [45-tile collar](../data/n105-local-fan-collar-5-21-19.json).
- [18 individual full-fan witnesses](../data/n105-local-fan-witnesses-5-21-19.json).
- [Independent checker](../scripts/verify_n105_local_fans.py).
- [Deterministic verification report](../verification/n105-local-fans.json).

From the repository root:

```sh
python scripts/verify_n105_local_fans.py
```

The checker uses only the Python standard library, rejects `python -O`, imports
no search code, and writes its deterministic JSON report to standard output.
An optional positional argument supplies a different data directory. It makes
no implicit file writes.

Coordinates use the basis `(1,0), (1/2,sqrt(3)/2)`. Collar coordinates are integers
divided by the recorded scale; fan coordinates are exact rational strings.
Squared length is `x*x + x*y + y*y`. The checker verifies congruence, containment,
and disjoint interiors with rational convex clipping. Independent oriented-edge
atomization enumerates the complete residual boundary, including subdivisions
at T-junctions, and identifies all 18 convex corners.

For each fan, the checker requires a shared vertex at the specified corner,
consecutive incident rays, containment in that corner's convex angular sector,
and the correct first and last rays. Together with disjoint interiors, these
conditions certify coverage of a neighborhood of the corner. It checks each fan
against the entire collar and against the other tiles in that same fan.

The precise verified conclusion is therefore

> For every convex residual corner, there exists an admissible complete local
> fan at that corner.

The order of the quantifiers matters: this does not assert that there exists one
mutually compatible selection of fans for all corners. No exhaustive graph or
search counts are needed for this positive certificate.
