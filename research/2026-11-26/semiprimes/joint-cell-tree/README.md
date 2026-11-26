# Unsigned populations of joint cells and the 215-tile odd layer

Both original F2 boards remain **OPEN**. The base is main at `d3f1c5d10d3937cbb59a3d662051093a7c52929f`.

**Every ordinary Euclidean joint cell has unsigned population divisible by $c$.** Its positive and negative populations are separately divisible by $c$. Thus a nonempty ordinary cell has at least $2c$ tiles; a cell of charge $\pm c$ has at least $3c$ tiles. This holds for both target boards with arbitrary translations, reflections and T-junctions. The exceptional cell in the standard frame is the height-zero axial core. Its population is congruent to $N$ modulo $c$. The thresholds $2c$ are 74 and 86, and $3c$ are 111 and 129.

**At 5063, if there are exactly 215 odd-height tiles, all 215 belong to a single native height-one cell, even in the tree of lifted cells.** The former list contained 218,905 phase and sign schemes. Its 218,736 four-cell schemes fail the unsigned divisibility theorem. Its 168 two-cell schemes fail the localized gate equations and existing exact dual certificates. The one remaining scheme is a necessary population profile. Its geometry, including the possible remote even branches, remains open. Larger odd populations also remain open.

| Result | Proof and verification |
|---|---|
| One tree for the two prime phases, with an actual tile population on each side of every cut | [Cell tree and physical budgets](TREE.md) |
| Sparse monochromatic lifts force at least four other charged lifts each, without counting a shared branch twice | [Physical gate and branching budget](BRANCHING.md) |
| Independent area proof on the original plane, including a nonzero-residue test | [Two finite-field moments](MOMENTS.md) |
| Elimination of all split 215 cases, including distinct lifts of the same Euclidean cell | [Odd-layer localization](FIVE_BLOCKS.md) |
| Exact reconstruction on two complete 143 tilings and repeatable certificate checks | [Replay](replay.py), [recorded results](REPLAY.json), [status](STATUS.json) |

The tree refines the Euclidean cells. The old 45/58 ordinary-node bounds now hold for occupied ordinary vertices of this *one* tree, counting distinct lifts separately across the entire board. A terminal lift of charge magnitude $c$ off the exterior path costs at least 185 or 301 tiles, respectively. A half-turn pair belongs to one short lift, has opposite signs, and cancels on one tree edge. Thus the new cut bounds measure disjoint physical populations on distinct edges. The 555/731 native two-height bounds retain their previous hypotheses. Neither balanced-branch deletion nor a two-height assumption enters the cell theorem.

Run `python3 replay.py` in this directory. Add `--full` to regenerate the two finite exclusions used at 5063, including the exact certificate columns and both exhaustive enumerations. Public arithmetic uses integer or rational coordinates.

An additional local consequence at $M=149$ uses the [three-direction staircase](../boundary-word/RECTANGLES.md) of the height-two region. For a generic vertical slice, each connected component of the rectangular remainder has length in $35\mathbb N_0+13\mathbb N_0$. At inward distance $477+1/2$ from the slant, three of the 109 candidate paths have a component of length 121, which is outside that semigroup. Exactly 106 pass this transverse test. The three rejected words have original height-two populations 1849, 1935 and 2021; this excludes those words, not those entire populations. [Exact section checker](sections.py).
