# Independent audit of the finite integer charge-profile filter

21 November 2026. The objects here are necessary projections of a
hypothetical `n_odd=3c` tiling. A surviving profile is not a tiling.
An interrupted or early-stopped filter is not an exhaustive exclusion.
This note reviews the complete profile universe, the exact dual cuts,
and their symmetries separately from numerical LP discovery.

## 1. Complete charge profiles

In the path frame, the actual height-one population has signs `2c,c`.
Its upward and downward gate currents satisfy

`Q_up(r)=d*g_up(r)+2c*[r=0]`,

`Q_down(r)=d*g_down(r)-c*[r=0]`,

where all `g` are integers and `d=a-b`. Summing all bins counts each
height-one tile once, so `sum(g_up)+sum(g_down)=0`.

Every positive gate current is at most the positive single-gate capacity
44 or 51; every negative current has magnitude at most the entire
negative population `c`. Remote positive charge units sum to at most
`floor(2c/d)`, and negative units to at most `floor(c/d)=1`.
Thus the canonical remote charge description is:

* a multiset of positive gate indices, with at most two entries at one
  gate for 5063 and at most one for 3431;
* either no negative gate or one gate of charge -1 outside the positive
  multiset.

There is no loss in forbidding a gate from appearing on both lists:
these lists represent the positive and negative parts of its **net
integer charge**, not separately hidden physical populations. Balanced
occupied gates remain possible at charge zero.

For each such profile, one native charge determines the other by the
total-charge equation. The code tests both native current bounds and
the two necessary sign-reserve bounds

`max(Q_up(0),0)+max(Q_down(0),0)+d*positive_units <= 2c`,

`max(-Q_up(0),0)+max(-Q_down(0),0)+d*negative_units <= c`.

These count disjoint long-side bins. They do not add populations from
different prime trees. The C++ native-charge search interval contains
the exact interval for both target parameter sets. Its specialized
one-negative-unit enumeration is justified by `floor(c/d)=1` here;
it is not a general-purpose enumerator for arbitrary tiles.

## 2. Independent count of the finite universe

Let `n=2(c-1)` be the number of remote gates. For `p` positive charge
units on `k` occupied gates, exactly `p-k` gates have multiplicity two.
At 3431 multiplicity two is prohibited. The number of remote profiles
with `m` negative units, `m in {0,1}`, is therefore the sum over allowed
`k` of

`choose(n,k)*choose(k,p-k)*(n-k)^m`.

Multiplying by the directly enumerated native choices and applying the
sign reserves gives these exact totals, independently of every dual:

| Target | Profiles before sign reserves | Profiles after sign reserves |
|---:|---:|---:|
| 3431 | 554,942 | 376,022 |
| 5063 | 34,672,599 | 17,800,359 |

Any claimed full execution of the filter must account for these totals.
An execution stopping at the first survivor need not do so and cannot
be reported as a complete exclusion. The checker can verify complete
filter accounting with `--filter-output`.

## 3. Exact dual inequality and independent translations

Each checked certificate has three periodic endpoint tables and two
gate-weight arrays. For every one of the `12c^2` actual single-tile
residue columns it satisfies

`W(T)+epsilon(T)*lambda_hand(gate(T)) <= D`.

The old zero-remote certificate has an additional charge multiplier
`t`; it is absorbed by adding `t` to both gate-weight arrays. This
retains the contribution `t*c` when summed. The independent checker
reconstructs CCW triangle polygons, their two short edges, their exact
axis directions, and their beta-endpoint gate labels. It imports no LP
model or certificate generator.

Summing the inequality over an actual height-one population cancels
the endpoint weights and gives `sum(lambda*Q)<=D*3c`. Translate the
endpoint tables and gate arrays together by an integral vector `w`.
The gate shifts are

`phi(w)=a*w_y-b*w_x`, `psi(w)=a*w_x-b*w_y` modulo `c`.

Their determinant `b^2-a^2` is nonzero modulo `c`: 19 at 5063 and
33 at 3431. Therefore one physical integral translation realizes every
pair of gate shifts independently. The full family of translated
inequalities is exactly equivalent to

`max_s sum_r Q_up(r)*lambda_up(r+s)`

`+ max_t sum_r Q_down(r)*lambda_down(r+t) <= D*3c`.

This does not require the triangular board to be translation invariant.
It translates the functional on the unrestricted residue columns; the
outer height-one endpoint contribution remains zero.

## 4. Rotations and reflection

Rotation by 60 degrees sends an axial point `(x,y)` to `(-y,x+y)`,
flips the sign `epsilon`, and multiplies the upward/downward residues
by `-a/b` and `-b/a`, respectively. Reflection `w -> -conjugate(w)`
sends `(x,y)` to `(-x-y,y)`, swaps the hands, preserves `epsilon`,
and multiplies the old upward/downward residues by `a/b` and `b/a`
in their new hands. These operations generate the twelve supplied
dihedral variants. Endpoint rows are permuted, with the boundary
orientation reversed for a reflection; a zero total remains zero.

`verify_profile_duals.py` derives the transformed arrays from images
of explicit residue representatives instead of importing the generator's
formulas. When `--cut-file` is supplied, it compares every serialized
array exactly. It also checks that the signed 64-bit arithmetic bound
is adequate for the supplied integer weights.

## 5. Controls and remaining distinction

The initial two certificates passed 44,376 independent integer column
checks. Their 24 serialized dihedral variants matched exactly. The
43-by-43 residue calculation verified all 1,849 translation-shift pairs
and 7,396 rotation/reflection identities. A later replay of 24 saved
certificates passed 532,512 column checks; the saved replay identifies
each included file by SHA-256 rather than claiming to include future
files from an ongoing search.

For the enumerator itself, the independent checker uses a Cartesian
product over all small remote integer-charge vectors, rather than the
C++ multiset recursion. It checks cut translations by directly testing
every pair of shifts, rather than summing separate maxima. Three small
controls agreed exactly in profile sets, absence of duplicates, visited
counts, sign reserves, and final survivors (201, 2,530, and 143).
These controls support the implementation; completeness for the target
universe is the enumeration argument in Sections 1 and 2.

Every exact dual remains valid even if its discovery LP was numerical.
Conversely, a numerical optimum, a timeout, or a floating projected
feasible point is not itself a mathematical certificate. Full exclusion
of these finite profiles excludes the complete `3c` mode. It still
leaves larger odd-height populations and does not by itself close either
semiprime count.

## 6. Final complete exclusion at 5063

The final, fresh full enumeration with all 65 base certificates reports

* `exhaustive = true`;
* `visited = 34,672,599`;
* `reserve_passed = 17,800,359`;
* `cut_passed = 0`.

Its file is `../gate-model/FINAL_PROFILE_ENUMERATION_5063.jsonl`.
This execution starts again from the complete charge universe. Its
conclusion therefore does not depend on the intermediate survivor-pool
transitions or candidate-selection heuristic.

The independent final replay `FINAL_DUAL_REPLAY_5063.json` checks all
65 base certificates, **1,442,220** CCW polygon column inequalities,
all **780** serialized dihedral cuts, the exact translation and symmetry
identities, signed 64-bit arithmetic bounds, and the final complete
enumeration accounting against the independently derived universe size.
The current C++ source was separately compiled for the small Cartesian
controls; they again passed. Each certificate is identified by its
SHA-256 in the replay. This is an exact computational certificate with
an explicit finite exhaustiveness argument, not an inference from a
numerical solver status.

The theorem follows by contradiction. Any complete 5063 tiling with
`n_odd=129` has the proved minimal-mode normal form, so its actual
integer neighboring-node charges occur in the enumerated universe.
Every accepted geometric population must satisfy every checked and
transformed endpoint inequality. The exhaustive filter leaves no such
profile. Therefore **no complete 5063 tiling has `n_odd=129`**.

Finally, the existing signed-population theorem makes `n_odd/c` a
positive odd integer. The single-block case is excluded by the ordinary
node population theorem. Removing the three-block case proves the
unconditional necessary bound for every complete tiling of this board:

`n_odd >= 5c = 215`.

The number 5063 itself remains open: five or more odd population blocks
are not excluded. No corresponding all-profile exclusion at 3431 is
claimed here.

For completeness, `POOL_TRACE_REPLAY_5063.json` also verifies all 33
intermediate pool hashes, canonical profile sets, subset transitions,
and accounting from 12,066 profiles to zero. Separate small controls
verify the new complete-scan pool output and the incremental filter
against independent Cartesian enumeration. Artificially inflated stored
lower bounds do not prune any profile, confirming that those fields
affect candidate choice only. These checks are supplementary to the
final fresh exhaustive scan.
