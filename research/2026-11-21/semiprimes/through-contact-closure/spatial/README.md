# Exact interior-point exclusions

This optional acceleration of the owned-through model adds necessary
nonoverlap constraints. It places no grid restriction on the tiles.

Choose finitely many physical points. For each point `p`, let `V_p` be
any finite set of candidate whole triangles whose **strict interiors**
contain `p`. A packing satisfies

\[
\sum_{T\in V_p}x_T\le1.
\]

Completeness of `V_p` is unnecessary: restricting the sum to any subset
preserves this necessary inequality. Enlarging a group as new placements
are generated is therefore sound. Points on an edge or vertex do not
belong to its strict-interior group. All determinants are integral after
clearing the actual powers of `c`; no denominator or height cutoff is used.

`spatial_search.py` chooses axial integer grid points inside generated
triangles and adds the corresponding at-most-one clauses. The step controls
which cuts are requested, never which placements are allowed. Selected
triangles are still checked for *all* pairwise overlaps by the inherited
exact routine. Passing the sampled point cuts alone is not a packing
certificate.

The optional `--prefer-tiles` flag changes only Z3's initial Boolean phase
heuristic. It adds no mathematical assumption or minimum population.

## Checks

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/spatial/verify_spatial.py
```

The replay compares the integer implementation with a separately evaluated
rational containment predicate. It checks three grids on all 143 triangles
of the genuine positive control, and sixty placements at positive and
negative heights. The actual control covers 850 distinct interior integer
points with no point used twice. These checks validate only the additional
cuts; the complete owned model has its own integrated positive controls.
