# Complete five-height inventory support for N=154

8 October 2026. Research directed by Denis Paliy with ChatGPT assistance.
This is an exact necessary-condition computation, not a tiling construction
or an exclusion of N=154.

## Result

For each five-height band `[0,4]`, `[-1,3]`, `[-2,2]`, the full direction-current
and affine-line-capacity model permits **all twelve tile orientation groups at
every height**. No orientation group can be deleted merely because it is absent
from one previously chosen formal witness.

The full set of surviving population profiles has a short description. Define

    b_h =24 if h=0, and26 otherwise.

Then a feasible five-height profile has

    n_h = b_h +13*epsilon_h,
    epsilon_h in {0,1},
    exactly two epsilon_h equal1, at heights of opposite parity.

There are precisely six such profiles in each band. All six pass the stated
necessary model; this is not a claim that any is geometrically realizable.
In particular,

    n_0 in {24,37};  n_h in {26,39} for h!=0.

Populations50 at height0 and52 elsewhere, though allowed by the crude total
budget, are excluded by the full necessary model. Reflections give the
corresponding statement for the other five-height bands.

These constraints can be added to a position model. They do not remove a whole
orientation class from placement enumeration, so they do not by themselves
resolve the size of the unrestricted five-height position matrix.

## Complete state retention

The previous `filtered_dp.py` retained only a minimum used population at a
state and returned one witness. That was sufficient for its existential
purpose, but one cannot read universal orientation exclusions from that
witness.

Here `all_support.py` retains every state `(A,Bprev,used)`, where A and Bprev
are signed triples of opposite orientation-count differences and `used` is the
exact population already allocated. Let

    R(x,y,z)=(-y,-z,x),
    S0(A)=8A-7R(A),
    S1(B)=7B-8R(B).

The boundary vector is F0=(154,0,0), F1=(0,0,91), F-1=(0,-91,0), zero otherwise.
The recurrence is

    A_next = (S0(A)+S1(B)-Fh)/13 +R(Bprev).

It is checked with exact integer arithmetic. The bottom and top long-edge rows
are also enforced. Every admissible population n is enumerated, with the known
congruence n0=11(mod13), nh=0(mod13) otherwise, the minimum24/26, and the parity
of the signed orientation norm. Thus the admissible n values advance by26
for each fixed signed pair(A,B).

The signed L1 vector enumeration is bounded by52: with five occupied levels,
all other levels already consume at least their24/26 minima. This covers the
central maximum50 and noncentral maximum52 before further exclusions.

The local checks are exactly the earlier necessary affine-line/chord screens:
`closure-position-oct8/layers/probe.py` for noncentral levels and
`closure-position-oct8/central/probe_central_24.py` for the central level.
For each signed triple pair, all unsigned inventories are obtained by adding
opposite-orientation pairs. No selected unsigned witness replaces that
existence check.

After the forward enumeration, only terminal states with `used=154` are kept.
Backward projection identifies every local signed record occurring on at least
one complete terminal path. Population profiles are propagated separately,
retaining their correlations. Orientation supports then enumerate the unsigned
inventories attached to those records. A support enumeration stops early only
if all twelve groups have already been witnessed positive; that shortcut
cannot manufacture a universal zero.

## Internal verification

A separate agent reviewed the state sufficiency, the bound52, congruence and
parity stepping, suffix and next-state pruning, terminal rows, and backward
projection. This was an internal code-and-mathematics review, **not** an
independently written DP or an external review.

The three committed JSON files report exact completion. Their `witnesses`
fields give local inventories witnessing each positive orientation. The claim
that each local record belongs to a complete formal path follows from the
reproducible forward/backward DP; a local inventory alone is not being called
a complete global certificate.

## Reproduction

From the repository root, using only the Python standard library:

```sh
python3 research/final-closure-oct8/154-inventory/all_support.py --lo 0 --hi 4 --seconds 180 --output /tmp/support_0_4.json
python3 research/final-closure-oct8/154-inventory/all_support.py --lo -1 --hi 3 --seconds 180 --output /tmp/support_m1_3.json
python3 research/final-closure-oct8/154-inventory/all_support.py --lo -2 --hi 2 --seconds 180 --output /tmp/support_m2_2.json
```

The runs completed in approximately24,21,33seconds in this environment. A time
limit produces `INCOMPLETE_TIMEOUT`, which supports no negative conclusion.
