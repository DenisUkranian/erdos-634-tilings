# Fresh audit of the global five-height upper bound for 154

8 October 2026. Direct mathematical audit and fresh independent replay.
No global nonexistence decision for 154 is asserted by this note.

**Conclusion: PASS.** Every tiling of (91,91,154) by (8,7,13) has a
consecutive interval of occupied short heights containing zero, with
at most five members. In particular its height span is at most four.
The six-height case is excluded by an exhaustive signed-current
calculation; it must not be discarded by population arithmetic alone.

The argument does **not** require the newer central bound n_0>=24.
It already works with n_0>=11. Thus the observation
24+5*26=154 is consistent with this proof and exposes no missing case:
that potential six-height population is one of those covered by the
signed-current exclusion.

## Written geometric inputs, checked directly

1. In `../../i120-global-oct7/HEIGHT_LEVELS.md`, whole-edge median cuts
   give 13|n_h for h!=0 and n_0=154=11 mod13. The exterior heights are
   -1,0,1; the two side lengths91 supply the required lattice closure
   at the two exceptional cuts. This proof allows T-junctions and does
   not replace actual whole-edge cut chains by an arbitrary mesh.

2. In `../../closure-position-oct7/heights/HEIGHT_GAPS.md`, an empty
   positive height k removes one of the two possible selected long-edge
   types. Every remaining cut step lies in13*z^k*Z[rho]. Its closed
   walks have area in169*sqrt(3)/4 times integers. Coprimality
   gcd(8*7,169)=1 makes a nonempty tail contain at least169 tiles.
   Since154<169, no such gap is possible. Reflection treats negative
   heights. Levelzero is occupied because n_0=11 mod13.

3. In `../../closure-position-oct7/oct8-structural/NO_THIRTEEN_HEIGHT.md`,
   each separate nonzero-height short-edge supporting line has signed
   short length divisible by13. Other edges on it have whole length13;
   an exterior side, if present, has length91. For a population13,
   the alternating character forces all tiles to have the same sign.
   The finite line-pair and orientation inventory enumeration then
   forces two identical tiles to share one gamma vertex. Thus an
   occupied nonzero height has at least26 tiles, not necessarily a
   multiple of26.

All three steps retain actual affine lines or actual whole-edge chains
where required. They introduce no edge-to-edge assumption, connectivity
assumption for a single level, or pure-island hypothesis.

Seven occupied levels already require 11+6*26=167>154. For six levels,
however, the baseline is141. The following exhaustive calculation is
therefore necessary.

## Exact six-height state space

The forward implementation is
`../../closure-position-oct7/oct8-structural/all_height_direction_dp.py`.
The separately written reverse implementation is
`../../closure-position-oct7/global/check_all_height_backward.py`, using
`check_full_inventory_backward.py` for its independently derived exact
coordinate edge data.

For chirality A or B, a signed three-vector subtracts each half-turn
orientation count from its opposite. For given vectors A_h,B_h, the
least compatible unsigned population is obtained by testing

    n>=||A_h||_1+||B_h||_1,
    n=||A_h||_1+||B_h||_1 mod2,
    n=11 mod13 and n>=11, if h=0;
    n=0 mod13 and n>=26, otherwise.

These are necessary conditions and also exactly describe the possible
unsigned populations of that signed inventory: adding opposite pairs
adds any even excess. Negative conclusions need only necessity.

For six occupied heights, reserving the minimum populations at all other
heights bounds any nonzero height by39 tiles and the central height by24.
Therefore enumerating every signed A-vector with L1 norm at most39 is
exhaustive. It includes 82,239 vectors; using39 also at zero merely
includes extra impossible vectors and cannot lose an actual tiling.

The reverse state is (A_(h+1),B_h) and the minimum already used population
at larger heights. It enumerates each A_h and solves the exact current
equation for B_(h-1); the long-edge matrix is13 times a signed permutation,
so this solution is unique or fails integer divisibility. Residue grouping
is only an index into the complete A-vector list and loses no vector.

The local minimum population is computed by directly testing the
progression in steps of13, independently of the forward rounding formula.
The recurrence reserves the lower-level minima before rejecting an
over-budget state. If multiple paths reach the same state, retaining
only the cheapest is safe: every future equation and local population
constraint depends only on the state and the remaining budget. A more
expensive prefix cannot enable a continuation unavailable to the cheaper
prefix. Exact equality to154 is not used for pruning in the negative
check; accepting any path of cost at most154 is an overapproximation.

At the top, A_(U+1)=0 and the equation at U+1 fixes B_U. At the bottom,
B_(L-1)=0 and the equation at L-1 constrains A_L. All in-band equations
are processed. More distant target currents are zero because L<=0<=U
and target heights are only -1,0,1. Thus no outside equation is omitted.

There are exactly six consecutive intervals of lengthsix containing
zero, and every one is checked. There is no time or state cutoff in the
reverse implementation.

## Fresh replay results

The prior files were read and their callable routines were rerun, with
new outputs saved here rather than overwriting the frozen reports.

* The independent no-thirteen checker again examined8,568 compositions,
  found54 one-sign inventories and108 including half-turns, verified all
  pigeonhole contradictions, and recovered nine orbits of size12.
* The independent reverse-height program again returned EXACT_UNSAT
  for all six six-height intervals.
* The five old five-height formal witnesses were expanded into twelve
  unsigned orientations per level and checked against the exact edge
  signatures. All have154 tiles and the required boundary currents.

| Six-height support | State counts after successive reverse steps |
| --- | --- |
| [-5,0] | 18,19,26,38,38,0 |
| [-4,1] | 411,54,19,26,38,0 |
| [-3,2] | 411,925,54,19,26,0 |
| [-2,3] | 411,925,925,54,19,0 |
| [-1,4] | 411,925,925,925,54,0 |
| [0,5] | 411,925,925,925,925,0 |

The fresh records and source hashes are `154_structural_replay.json`
and `no_thirteen_independent.json` in this directory. The five positive
controls are formal inventories only; their existence is not claimed
to produce placed tiles.

## Scope of the audited conclusion

The zero-level congruence, no-gap theorem, population26 floor,
seven-height budget, and six-height exact exclusion together prove the
global upper bound of five consecutive heights. The earlier positioned
one/two/three-height exclusions are separate lower-bound inputs and
were not needed for this upper-bound audit.

To exclude154 globally by a positioned enumeration, one still must
cover every band of five consecutive heights containing zero (or a
larger lattice that provably contains each), and justify its exact
placement completeness and terminal negative certificate separately.
The signed-current program alone does not supply that conclusion.
