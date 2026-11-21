# A half-fan must select its actual whole through tile

21 November 2026. **3431 and 5063 remain OPEN.** This package strengthens
the unrestricted physical necessary model and supplies exact positive and
negative controls. It does not contain a target impossibility certificate.

The implementation reuses the historical unrestricted `Geometry`, vertex
fan construction, and corner-search infrastructure without modifying those
files. It imposes no short-height, denominator, phase, radius, or
odd-population cutoff. A root file, when supplied, explicitly conditions
the search on its six specified corner tiles.

## 1. The physical condition missing from the old local fan

At an interior vertex `p` of a selected tile, the other tiles either form
a complete vertex fan or form a half-fan opposite a tile whose side
contains `p` in its relative interior. The existing
[corner-fan theorem](../../../../2026-11-20/semiprimes/continuation/vertex-phase/CORNER_FANS.md)
enumerates all such vertex fans. Its through-tile test checks only whether
one of six shapes has a feasible real translation interval in the board.
It does not require selection of that whole triangle.

Specifically, `CornerOracle.alternatives()` calls `through_possible()` and
then appends the two vertex-fan graphs. Its `constraint()` inserts their
vertex-at-`p` tiles. `CornerSearch.install_corner_tile()` follows the same
pattern. An actual through tile is absent from those local graph variables,
because `p` is not one of its vertices. It may already occur elsewhere in
the global catalogue, but the old local fan does not require its selection.

The strengthened implication is

\[
x_T\Longrightarrow F_{\rm full}(T,p)\ \lor\!
\bigvee_{\ell}\left[
F_{\rm prefix}\land F_{\rm suffix}
\land\bigvee_{Q\in C(p,\ell)}x_Q\right].                 \tag{1}
\]

Every `x_Q` is the same global Boolean used for that actual whole triangle
everywhere else. It incurs one tile, contributes its physical endpoint
currents, and participates in nonoverlap constraints. Several junctions
cannot choose different placements while pretending to use one tile.

The half-fan itself lies on the opposite half-plane from its through tile.
The additional restriction concerns common ownership, tile counts, the
owner's other endpoint obligations, and consistency with other neighborhoods.
It does not forbid any legitimate T-junction.

## 2. A complete finite catalogue of owners

Let `u` be the unit ray from which a counterclockwise half-fan starts.
The half-fan occupies the left half-plane; the through tile occupies the
right half-plane. For each possible side length `L in {a,b,c}` there are
two congruent triangles with that side starting at `p` along `u` and
interior on the right. These are six reference shapes.

Move such a shape by `-t*u`. The point `p` lies strictly inside its side
exactly when `0<t<L`. In a complete tiling, an extreme tile of the
half-fan has a side ending at `p` on the same maximal straight run. The
[integer-offset lemma](../../../../2026-11-20/semiprimes/continuation/first-cuts/CORNER_RAYS.md)
therefore puts `p` and the through-side endpoints at integer distances
along that run. Hence

\[
\boxed{t\in\{1,2,\ldots,L-1\}.}                         \tag{2}
\]

This argument uses a genuine endpoint on the run. It imposes no integer
condition on an arbitrarily chosen point inside an isolated edge.

`OwnedCornerOracle.through_candidates(p,ray)` enumerates all six shapes
and all shifts in (2), retaining the contained placements that pass the
inherited necessary outer-boundary arithmetic. Before containment there
are at most

\[
2(a+b+c-3)=148\quad(3431),\qquad176\quad(5063)
\]

candidates. The old unrestricted 24-placement endpoint oracle supplies
the six reference shapes, including both hands and every adjacent short
height. No finite global placement catalogue is assumed complete.

All candidates for the same `(p,ray)` contain `p` strictly inside a side
on the same bank. Any two overlap near `p`, so an additional at-most-one
constraint on that catalogue is valid. Different catalogues share global
tile identities through the normalized `(q,h,j,s)` key.

## 3. Permanent physical equations and exact overlap

Every inserted placement registers all six signed endpoint contributions.
A physical row is imposed only after the unrestricted oracle enumerates
every incident contained placement; there are 24 possibilities before
containment and boundary filtering. This produces a permanent necessary
equation. Uncompleted rows have **no** finite-pool equality attached.

The driver repeatedly solves the current necessary model. For a partial
selection it adds exact overlapping-pair exclusions, completes selected
owners' endpoint rows, and completes additional residual rows. It also
installs more owned fan implications. Selected owners' rows are all
completed by default; `--owner-rows-per-round` can limit that refinement
batch, leaving omitted rows unconstrained. The limit weakens the current
necessary model and never turns a resource stop into a proof.

`exact_geometry.py` uses exact rational-coordinate separation at arbitrary
powers of `c`. A spatial hash accelerates the pair enumeration without
discarding possible overlaps. Contacts along sides or vertices are allowed;
only positive-area interior intersection is excluded. A global model may
still contain an overlap before its exclusion is generated. Such a model
is a partial candidate, not an accepted tiling.

The refinement priority favors selected owners, then interior vertices,
then vertices incident to residual rows. This prevents exterior fan
completion from indefinitely postponing through-tile ownership. It changes
search order, not the necessary conditions.

## 4. Global charge reserve without an odd-population assumption

Put `d=a-b` and `epsilon=s*(-1)^j` in the historical standard board frame.
The directed characters `(-1)^j L` and `(-1)^(j+h) L` have tile sums
`(d-c)*epsilon` and `(d+c)*(-1)^h*epsilon`. The board has only even
direction heights and both boundary sums equal

\[
A+B-c^2=3ab=(c-d)(c+d).
\]

Consequently its complete even and odd signed populations satisfy

\[
G_{\rm even}=-d,\qquad G_{\rm odd}=-c.                   \tag{3}
\]

For any selected subset `S`, the missing tiles must supply the two charge
deficits. Each missing tile contributes one unit in exactly one parity.
Therefore

\[
|S|+|-c-G_{\rm odd}(S)|+|-d-G_{\rm even}(S)|\le N.        \tag{4}
\]

Expanding the absolute values gives four Boolean cardinality bounds. For
each `sigma,tau in {-1,+1}`, let `M` count selected odd tiles with sign
`-sigma` and selected even tiles with sign `-tau`. Then

\[
2M\le N+\sigma c+\tau d.                                \tag{5}
\]

The driver asserts (5) and the total count bound for the entire currently
generated pool at each query. They are valid for projections of any full
tiling and do not assume a particular odd population or occupied height.

## 5. Why a finite contradiction would be globally sound

Fix the completed physical rows, owned corner roots, and overlap clauses
in an exported model. Every actual tiling induces a satisfying assignment
by retaining its generated placements. No omitted tile contributes to a
completed row, because that row's incidence catalogue is complete. An
actual through tile needed by an imposed half-fan belongs to its complete
catalogue in Section 2 and is therefore generated. The inherited vertex
fans and all nonoverlap/upper-count constraints are likewise necessary.

Thus a checked UNSAT certificate for this finite model would exclude all
tilings in its stated scope. Without a root assumption that scope is the
whole board, including every odd population. With `--root-file` and
`--root-id`, it is only that explicit corner branch. The separately checked
corner catalogue has at most 128 roots; excluding all surviving roots
would give full exclusion. A single branch refutation would not.

`necessary_model.json` exports the canonical placements, complete rows,
owned fan roots, shared Boolean fan definitions, owner catalogues,
angular/owner cliques, overlap pairs, and explicit root literals. Its
`permanent_assertions` field contains the permanent Boolean assertions.
`query_count_bound` is the conjunction of the total tile bound and all
four charge reserves; their metadata is also supplied separately.
There are no integer population variables or temporary guarded equations.

A solver-reported UNSAT is saved as a candidate requiring independent
encoding and proof verification. The driver always leaves
`full_target_excluded=false`. SAT may be a partial selection; it becomes
a positive candidate only when every actual physical row balances and
there are no interior overlaps, after which independent geometric
verification remains required. Time, memory, column, round, and solver
limits are explicitly inconclusive.

## 6. Exact controls

`verify_owned_controls.py` uses the known complete 143 certificate with
SHA256 `f9c864244612d930efeeea405f22a44881399d6f6974bdeda2fb6f70b2047aa9`.
It verifies metric, containment, area and full physical line current,
then checks:

| Control | Result |
|---|---:|
| All actual owned vertex fans | 429 preserved |
| Through incidences / distinct owners | 38 / 29 |
| Integer shifts and inclusion of every actual owner | All pass |
| Old local fan with its actual owner deleted | 114 still accepted |
| New local fan with that owner deleted | 114 rejected |
| Exact overlap controls at heights -4 through 4 | 18 pass |
| Charge-reserve subset/sign checks | 264 pass |

The explicit local SMT comparison gives SAT with the owner present, SAT
for the **old local** predicate after deletion, and UNSAT for the **new
local** predicate after deletion. This does not claim that deleting a
tile preserves the old full global endpoint model.

The integrated control includes all physical rows of the selected 143
tiles, all their vertex fans, complete exterior constraints, the known
corner root, and the tile/charge reserves. Fixing the actual tiling is
SAT before and after an equivalent solver rebuild. The replay has 36,434
candidate variables, 335 complete physical rows, 447 owned fan roots,
19,109 permanent assertions and 29 actual selected owners. Additional
roots beyond the 429 actual corners come from exterior candidates.

Run from the repository root, without `-O`:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/owned/verify_owned_controls.py
```

Use `--geometry-only` for the standard-library mathematical controls
without SMT. The integrated encoding check uses the already available
system `libz3`. The saved result is [OWNED_CONTROL_REPLAY.json](OWNED_CONTROL_REPLAY.json).

An example branch search is:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/owned/owned_search.py \
  35 13 43 --out /tmp/owned-5063-O0-X0-Y0 \
  --root-file research/2026-11-21/semiprimes/through-contact-closure/corners/ROOTS_5063.json \
  --root-id O0-X0-Y0 --rounds 50 --time-limit 600 --proof
```

Omit both root options for an unrestricted whole-board necessary model.
`--seed-json` only introduces unfrozen candidate placements. `--rows`
regenerates old completed rows using the unrestricted oracle, and
`--corner-checkpoint` regenerates old corner roots with the new ownership
condition. Neither fixes an old partial packing.

The package is a sound implementation and internally checked research
tool. The controls do not prove that the two target searches will finish
or that either board is impossible.
