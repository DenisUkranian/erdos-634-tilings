# Global necessary conditions for the remaining count 135

8 October 2026. **The existence of a 135-tiling remains unresolved.**

The exhaustive [all-branch arithmetic reduction](../arithmetic-gates/README.md)
and its geometric exclusions show that any 135-tiling must use the primitive
tile `(3,5,7)` and an equilateral target of side 45. Thus the following
conditions apply to every possible realization of the count, rather than
only to one chosen tile or target.

Put `rho=exp(i*pi/3)` and `z=(3+5rho)/7`, with exterior directions at height
zero. In every possible tiling:

* the occupied short-edge heights form a consecutive interval containing zero;
* at most **nine** heights are occupied;
* `n_0 >= 9` and `n_0 = 2 (mod 7)`;
* every occupied nonzero height has at least 14 tiles and population divisible
  by 7;
* `sum_(h odd) n_h = 7 (mod 14)`, so at least one odd height has at least
  21 tiles.

The [no-gap proof](NO_GAPS.md) rules out the only possible gap tail, of size
98. Such a tail would be a lattice polygon with 15 elementary up triangles
and 15 down triangles. An exact containment calculation excludes it at each
of the three possible gap heights. The separate
[signed-character argument](../e135-inventory/README.md) gives the nine-height
bound without a computer calculation or a no-gap assumption.

The containment calculation was independently implemented in physical
coordinates, using exact polygon clipping and direct vertex containment:

* producer: [cell_bound.py](cell_bound.py),
  [recorded output](cell_bound_checked.json);
* independent checker:
  [check_e135_cells_independent.py](../154-audit/check_e135_cells_independent.py),
  [PASS report](../154-audit/e135_cells_independent.json).

Both implementations obtain orientation maxima `(12,14)`, `(12,14)`, and
`(16,13)` for the three possible gap heights. The independent mathematical
review also checks the whole-edge interface, isolated-gap, component, and
hole arguments needed to apply those computations to arbitrary tilings with
T-junctions. This is an internal independent review, not external refereeing.

The [local population investigation](LOCAL_FLOOR_BARRIER.md) records why the
supporting-line argument alone cannot simply replace the off-zero population
floor 14 by a larger one. Its final paragraph describes the state before the
no-gap proof above; the local counterexample and inventory checks remain valid.

The [finite-direction inventories](../e135-inventory/README.md) and
[positional searches](../e135-bitmap/README.md) retain their stated limited
scope. None of these notes proves either existence or nonexistence at 135.
Consequently the complete classification of square class 15 still has exactly
one unsettled count: 135. Counts 15 and 60 are excluded, and every `15m^2`
with `m >= 4` is constructed.

Reproduce the two exact containment checks from the repository root:

```sh
python3 research/final-closure-oct8/e135-structure/cell_bound.py
python3 research/final-closure-oct8/154-audit/check_e135_cells_independent.py
```
