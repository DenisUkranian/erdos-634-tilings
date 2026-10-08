# Supporting-line obstructions reduce 154 to three through five heights

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
The count 154 and the full problem remain unresolved.

The new [supporting-line proof](NO_THIRTEEN_HEIGHT.md) shows that any nonzero
height in an actual I120 tiling by `(8,7,13)` cannot contain
exactly 13 tiles. Its population is therefore at least 26. This is a
geometric restriction: it uses the affine line of each edge, and then
the nonoverlap of tiles with the same orientation and gamma vertex.

Apply it to the [complete signed-direction dynamic program](../dual/DIRECTIONAL_SUPPORT.md).
For a prospective exact support `[L,U]`, use minimum populations

    b_h = 11                         if h=0,
          26                         otherwise.

For a signed state `A_h,B_h`, minimize the unsigned population subject to
the same L1, parity, and residue conditions as before, adding `n_h>=b_h`.
The residue of 26 remains zero modulo 13, so taking the previous minimum,
raising it to `b_h`, and correcting parity by another 13 computes the
new minimum exactly. Replace the suffix lower bounds by `sum b_h`.
All other recurrence and terminal conditions remain unchanged.

`all_height_direction_dp.py` implements these changes. For K occupied
heights their total minimum cost is `11+26(K-1)`, so every one of the
enumerated signed B-vectors has L1 norm at most
`154-[11+26(K-1)]+26 = 195-26K`. This is a safe upper bound, two units
looser than necessary at height zero. Suffix pruning uses the same new
minimum costs. The equations and both endpoint conditions are unchanged.

Seven heights already require at least `11+6*26=167>154` tiles. The exact
integer dynamic program exhausts all six supports of length 6 containing
zero and finds none. It supplies formal inventories for all five supports
of length 5. The latter are independently replayed by
expanding the twelve unsigned tile orientations and summing the three
directed edges of each tile type. Each has precisely 154 tiles, the
required target currents, and the new population bounds at every
nonzero height.

Combined with the no-gap theorem and the complete two-height obstruction,
the conclusion is:

> Any actual 154-tiling has a consecutive interval of three through five
> occupied short heights, and therefore height span at most four.

There are 12 such intervals containing zero and seven reflection orbits.
The five-height formal controls show why the new supporting-line obstruction
does not complete a nonexistence proof: these are inventories without
placements, and no geometric realization is claimed.

Reproduce the finite checks with:

```sh
python research/closure-position-oct7/oct8-structural/check_no_thirteen_height.py
python research/closure-position-oct7/oct8-structural/check_all_height_direction.py
python research/closure-position-oct7/global/check_all_height_backward.py
```

The second command writes `all_height_direction_probe.json`. A time or
state limit yields `INCOMPLETE`, which the replay rejects. The independent
backward checker has no resource cutoff, enumerates the other chirality,
and tries the admissible unsigned populations directly. It reproduces all
six negatives and replays the five formal controls; see
[`all_height_backward_verified.json`](../global/all_height_backward_verified.json).
Every recorded negative result exhausts its finite state set.

The earlier endpoint-only proof and its eight-height exclusion remain in
`EXTREME_13.md`, `extreme_direction_dp.py`, and
`extreme_direction_verified.json`. They are superseded by the stronger
all-height conclusion above, not used to claim an additional result.
