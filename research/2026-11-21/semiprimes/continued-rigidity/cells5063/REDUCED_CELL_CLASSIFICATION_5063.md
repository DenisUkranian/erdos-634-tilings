# Fewer cell populations in the remaining 215-tile mode

21 November 2026. This is a necessary structural reduction for 5063,
not an exclusion of its 215 odd-tile mode or of any larger odd population.

The [one-height classification](../../global-closure-next/global-strengthening/ONE_HEIGHT_CELL_CLASSIFICATION_5063.md)
puts all 215 odd tiles at short height one, with total odd sign charge 43.
They occupy one, two, or four positioned Euclidean cells. In the four-cell
case their positive/negative populations are

\[
\begin{pmatrix}
(x,x)&(43-x,43-x)\\
(43-x,43-x)&(43+x,x)
\end{pmatrix},\qquad 1\le x\le42.
\]

Two new independent necessary results reduce this parameter list:

* The [support-line minority theorem](../global/UNIT_CHARGE_CELL_MINORITY.md)
  requires at least five minority tiles in an ordinary Euclidean cell
  of charge 43. Applied to the lower-right cell, it gives `x>=5`.
* The [positive integer endpoint-kernel exclusions](../integer3431/SMALL_BALANCED_CELLS.md)
  forbid nonempty balanced Euclidean cells of populations
  `2,4,8,10,14`. Applied to the other three cells, they exclude any
  `x` with `2x` or `2(43-x)` in that list.

Every cell here is ordinary: there is no exterior side at short height one.
The endpoint-kernel condition comes from the complete cell current identity;
it does not assume that a cell fills an entire exact phase node. Thus these
two results apply despite the sharing of exact nodes in the four-cell case.

Consequently

\[
\boxed{x\in\{6\}\cup\{8,9,\ldots,35\}\cup\{37,40\}.}
\]

There are 31 remaining parameters. Their charged-cell population lies between
55 and 123. The native class may be any of the four cells; this reduction
does not identify an individual cell's gate currents with its entire
shared node's currents.

## Finite containing list

The original classification has 43 possible exact nodes at each prime,
with native label zero. Each split partition chooses its one nonnative
label in 42 ways and chooses whether the native node is the balanced 86-node
or the charged 129-node. The revised containing count is therefore:

| Form | Number of phase and sign skeletons |
|---|---:|
| One occupied node at both primes | `1` |
| One split partition, either prime | `2*2*42=168` |
| Both partitions split | `4*42^2*31=218736` |
| Total | **218905** |

This removes 77616 skeletons from the previous 296521 list. The count keeps
all physical symmetries and is an exhaustive containing list, not a count
of realizable configurations. The one- and two-cell forms are unchanged.
No placements or completed even layers are supplied by this reduction.

`python3 verify_reduced_skeletons.py` checks all 42 prior parameter values,
the sign matrices, and the new count. Its
[`REDUCED_SKELETONS_REPLAY.json`](REDUCED_SKELETONS_REPLAY.json) records the
hashes of the prerequisite replays. The support-line and kernel theorems
have their own exact independent verifiers; this arithmetic consequence
does not replace those verifiers.

## Limits of stronger population guesses

There are exact balanced six-tile and sixteen-tile ordinary-cylinder
partial packings, with integer nonoverlapping tiles. In particular, a
claim that every small balanced cell population must be a multiple of six
is false even after imposing those physical conditions. See the
[sixteen-tile cylinder countercontrol](../global/BALANCED_CYLINDER_COUNTERCONTROL.md).
Neither partial packing is claimed to extend to a complete 5063 tiling.

Closing the remaining mode requires additional information about how these
cells share complete-node gates or how all short and long physical edge
currents fit together. The finite dual exploration in this folder retains
that shared-node distinction explicitly.
