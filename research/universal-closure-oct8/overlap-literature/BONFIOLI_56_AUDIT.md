# Audit of the earlier exclusions of 14 and 56

8 October 2026. This note is an audit record, not a new priority claim.

## Immutable primary source

Vico Bonfioli, `ElVec1o/erdos_634_proof`, commit
`4bb61193bafa4471f7ba3a35324ae0f70bd2177c`:

* [paper, equilateral 56](https://github.com/ElVec1o/erdos_634_proof/blob/4bb61193bafa4471f7ba3a35324ae0f70bd2177c/paper/erdos-634.tex#L2048):
  reports exhaustion in 156,646 nodes.
* [paper, corrected W56 branch](https://github.com/ElVec1o/erdos_634_proof/blob/4bb61193bafa4471f7ba3a35324ae0f70bd2177c/paper/erdos-634.tex#L2112):
  reports exhaustion in 4,890,763 nodes, after removing the erroneous
  scale-divisibility filter. The same passage reports W14 in678 nodes.
* [original Python engine](https://github.com/ElVec1o/erdos_634_proof/blob/4bb61193bafa4471f7ba3a35324ae0f70bd2177c/code/engine/engine.py),
  [simple GMP engine](https://github.com/ElVec1o/erdos_634_proof/blob/4bb61193bafa4471f7ba3a35324ae0f70bd2177c/code/engine/cengine.cpp),
  [optimized exact engine](https://github.com/ElVec1o/erdos_634_proof/blob/4bb61193bafa4471f7ba3a35324ae0f70bd2177c/code/engine/cengine_c2.cpp), and
  [W instance generator](https://github.com/ElVec1o/erdos_634_proof/blob/4bb61193bafa4471f7ba3a35324ae0f70bd2177c/code/engine/gen_cevian.py).

The engine code is MIT licensed, copyright2026 Vico Bonfioli. The prose
is CC-BY4.0. These are separate from the unfinished universal packing claims
elsewhere in the same repository.

## Independent arithmetic gate

Our divisor sieve and independently implemented parameter sweep agree:

| Count | Complete remaining instances |
|---|---|
|14|W, tile(6,5,9), target(27,28,15)|
|56|E120, tile(7,8,13), equilateral side56; W, tile(6,5,9), target(54,56,30)|

See `attribution_candidate_gate.json`. The gate uses the published exhaustive
angular classification, rationality, and the character/scale arguments in
`../../uniform-reduction/PROOF.md`. In particular it does not use the revoked
condition `K | M²`, a packing lemma, or a general W scale-one exclusion.

## Source review

The engine's basic mathematical reduction is sound. Every positive residual
component has a convex corner. Any tile covering that corner must have a tile
vertex there; the tile first in angular order has an entire incident side
on the outgoing boundary ray. The three corner types and their two possible
incident sides exhaust all six possibilities. Exact containment and subtraction
retain arbitrary T-junctions. Every subtraction error aborts the run; it is not
converted into a negative branch.

The basic prunes are necessary: each residual component has an integer number
of tile areas; a maximal straight boundary interval with two convex endpoint
corners consists of whole tile edges; a convex residual corner cannot be
smaller than the smallest tile angle. The MRV option chooses a different
convex corner, without reducing its six candidate placements. Optional walk
filters are not used in the replays recorded below.

All relevant coordinates have rational x and rational multiples of sqrt(D)
for y. Exact rotation by a tile angle and intersection preserve that form.
Directions are unit vectors of this form, so lengths along a known edge are
rational. The engine's rational-length representation therefore imposes no
unjustified grid restriction on these instances.

## Executed checks and remaining scope

The original optimized engine was compiled from the immutable source with
GMP6.3.0. The complete equilateral56 run returned

    EXHAUSTED_NO_TILING nodes=156646 maxdepth=25
    pruneA=12563 pruneR=39474 pruneP4=35716 pruneP5=0

This reproduces the external published node count exactly. W14 was also
exhausted with the source's MRV option in51 nodes; a build which recalculates
every optimized arithmetic operation in GMP reports1,180,215 agreements and
zero discrepancies.

At this checkpoint, the W56 replay is still incomplete. Neither a capped
search nor the external manuscript's reported node count is labelled an
independently replayed negative certificate here. The current source tree
does not expose a per-node W56 refutation trace. Consequently this audit
alone does not yet supply a new self-contained global proof of56.

Replays were run in `/workspace/scratch/12ca7a077497/bonfioli56audit`.
The completed E56 result and W14 arithmetic cross-check are preserved alongside
this note as `eq56_c2.log` and `W14_crosscheck.log`, with command and source
hashes in `bonfioli_replay_checkpoint.json`. Subsequent W56 experiments import the project's
proved integer-seam filter and exact residual-state memoization; unfinished
experiments retain their INCOMPLETE scope.
