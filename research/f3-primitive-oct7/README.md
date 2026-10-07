# Primitive F3 investigation, 7 October 2026

**No new tiling or unrestricted obstruction was obtained here.** In
particular the primitive count 4830 is still unresolved. The files in
this directory are exploratory and are not classification certificates.

The proposed necessity `a<2b` for ordered primitive F3 targets with
`a>b` was compared with the current positive constructions. No
counterexample was found among those constructions, but this is not a
proof of necessity. The known multiplier-one gamma construction covers
`b<a<2b`; its failure above that range is only a restriction on that
construction. The full directed-edge signature has a positive formal
orientation inventory on both sides of the proposed threshold, so it
cannot prove the proposed necessity.

## Another positive route tested

The script `macro_search.py` searches for a decomposition of the whole
F3 target into triangles congruent to **integer-scaled** copies of the
original tile. A macrotriangle at scale k would be expanded into k²
ordinary unit triangles. This search is over exact rational coordinates
in Q(sqrt(3)); it permits reflections and non-edge-to-edge contacts.

It uses the existing advancing-corner implementation's exact placement,
containment, and separating-axis overlap checks. The following runs for
`(a,b,c)=(24,11,31)` produced no completed positive certificate:

| Macro restriction | Nodes visited | Stop |
| --- | ---: | --- |
| At most 8 macrotriangles, every scale at least 5 | 6139 | 55-second limit |
| At most 6 macrotriangles, every scale at least 1 | 3621 | 50-second limit |

Both outputs are explicitly `INCOMPLETE`. Neither is an exhaustive
negative result, even inside its restricted macro family. No inference
about nonexistence of a 4830-tiling follows.

## Geometry that still needs proof

The F3 target angles are `3 beta, 2 alpha, alpha`, where
`alpha+beta=pi/3` and a>b. Irrationality fixes the corner fan inventories,
but does not force the three c-scaled triangular patches of the gamma
construction. At the `2 alpha` corner, the two incident alpha-corner
tiles can meet with equal or unequal edge lengths; the latter produces
a permissible T-junction. A proof cannot replace this freedom by a
full c-scaled patch without an additional argument.

Likewise, the earlier all-directions gamma boundary obstruction does
not exclude a full F3 tiling: necessity of the gamma partition already
has a concrete counterexample in the main research notes. This remains
an essential distinction for the infinite squarefree primitive front.
