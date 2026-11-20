# Exact gate bounds in the native two-height model

20 November 2026. **Both unrestricted target questions remain open.**
These bounds have the additional hypotheses stated in Section 1. They
are not nonexistence certificates, even for the restricted model.

## 1. Native gates and their scope

Use the native path frame with outer vertices
`0,c^2,a(a+2b)z^2`, and suppose **both**:

1. The only short heights are 1 and 2.
2. Every short-height-one vertex lies in `zR`, and every short-height-two
   vertex lies in `z^2R`.

The second hypothesis is additional. The general two-height vertex
lattice is larger and does not establish it.

Rotate by `1/z`. The height-one mesh is now `R` and the height-two mesh
is `zR`. Write `z=lambda/eta` in lowest Eisenstein terms; their
intersection is `lambda R`, of index `c` in either mesh.

A height-one tile with long height two can meet a height-two short edge
only when both long endpoints lie in this intersection. In its own
coordinates the gate condition is

\[
 q-a\rho^j\in\lambda R.                              \tag{5}
\]

If (5) fails, a maximal supporting run contains only height-one long
edges of length `c`. Such an edge cannot occur on an outer height-two
side either: in the unrotated native frame all three outer vertices
`0,c^2,a(a+2b)z^2` lie in `z^2R`, since `c^2/z^2=(a+b*conjugate(rho))^2`
is integral. Integral boundary offsets put every boundary endpoint on
those sides in the same mesh. Hence the wrong-gate run is interior.
Its banks have the same endpoints, so it pairs
whole-to-whole with its half-turn mate. The paired mate remains in the
same native mesh. Independently, every interior height-zero long edge
is paired this way. The base has exactly `c` unpaired downward teeth,
with obtuse vertices

\[
 q_i=i(a+b,-b)+(a,0),\qquad 0\le i<c.
\]

No search for physical tile positions is used in the following finite
projection. In `R/cR`, assign three arbitrary endpoint tables, one for
each height-one axis. A directed edge has endpoint difference as its
weight. Tables are zero on points outside `R`. Every whole height-one
long edge has weight zero. All translations of a native tile are
covered by the `c^2` residues, and a gate is a single linear congruence
modulo `c`. Ungated upward tiles and interior downward tiles are tested
as their compulsory half-turn pairs.

The whole-board characters give `G_1=c` in this native frame. The fixed
base teeth have `G=-c`, so the remaining upward single columns have
signed count `2c`; pairs have count zero. This extra equality is included
in the finite dual.

## 2. Exact gate certificates

For integer endpoint weights `f` and integer sign multiplier `t`, define
the score of an upward single to be its endpoint weight plus `epsilon*t`.
A half-turn pair has opposite signs, so its score is just its combined
endpoint weight. Verify that every permitted single has score at most
`D` and each pair at most `2D`, where `D>0`. If `w_base` is the sum of the
fixed teeth's endpoint weights, then

\[
 n_1\ge c+\frac{-w_{\rm base}+2ct}{D}.                \tag{6}
\]

All inequalities in the following table were checked using integers.
The numerical LP is only a generator for the verified integer tables.

| Tile | Single/pair inequalities | Exact lower bound from (6) | After `c` divisibility and odd parity |
|---|---:|---:|---:|
| `(33,7,37)` | 222 + 8,214 | `518127703/1000001` | **555 = 15c** |
| `(35,13,43)` | 258 + 11,094 | `693711126/1000001` | **731 = 17c** |

The previous one-dimensional phase tables gave `9c` in each case.
The new values concern the more restricted native two-height model;
they must not replace the earlier bounds in its larger domain.

The exact 143 tiling satisfies these native hypotheses after the
isometry `x -> a(a+2b)z^2-rho*z^2*conjugate(x)` from the standard frame.
It has `n1=105,n2=38`, and the checker verifies all its height-one
columns exactly: 7 base teeth, 14 gate singles and 42 interior pairs.
Every torus equation has zero residual. This is a control of the
projection, not a new construction.

## 3. Charging the other mesh: outcome and limitation

A further finite projection adds the height-two endpoint equations and
signed line lengths, with each line classified modulo `c` in its native
mesh. The line equations retain the nonzero length of a whole long edge,
which endpoint differences alone erase. They charge both populations.

For a permitted gate, the short-anchor residue and opposite-mesh long
line residue are independent Chinese-remainder coordinates. A nonnegative
matrix of all such combinations can therefore be represented by its two
marginals, with one equality of totals for each orientation. This avoids
an enlarged geometric placement catalogue. The resulting projections
have 17,316 and 23,220 columns.

The complete 143 witness passes the coupled projection with exact integer
residual zero. A floating-point LP run on 3431 reported minimum total
population about **729.7996**, far below 3431; no exact dual is claimed
for this exploratory number. The 5063 run reached its 120-second limit
without a certified conclusion. In particular the solver's accompanying
`primal_status is Infeasible` text at timeout is **not** an infeasibility
certificate. Neither run provides an obstruction to its restricted
native model, let alone to an unrestricted tiling.

The [joint charge theorem](JOINT_CELLS.md) gives unconditional necessary
conditions; the exact 15c/17c bounds here are conditional necessary conditions. Neither
currently exceeds the available whole-board population. Additional
geometric information linking nonzero joint-charge transport to actual
supported boundaries is still needed for a nonexistence proof.

## 4. Reproduction

From this directory in the repository, using ordinary Python with
assertions enabled:

```sh
python3 verify_native_torus.py --known-base ../.. \
  torus3431/exact_dual.json torus5063/exact_dual.json
```

This exact check uses only the standard library and the project's exact
geometry module. Optional LP generation and the coupled positive control
also require NumPy and SciPy:

```sh
python3 check_coupled_143.py ../..
```

`native_torus.py` and `coupled_native_torus.py` reproduce the finite
relaxations. Numerical optimization alone is not a proof certificate;
`verify_native_torus.py` checks every integer dual inequality independently.
The exploratory coupled outcomes are recorded in `coupled3431/status.json`
and `coupled5063/status.json`; raw numerical primal and dual arrays are
not needed for the exact bounds.
