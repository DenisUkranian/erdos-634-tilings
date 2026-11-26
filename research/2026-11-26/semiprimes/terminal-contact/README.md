# Terminal contact cost on the two F2 boards

Both original counts are **OPEN**. This checkpoint builds on main at `0c7c8e90167b4d35d82008fd02f80415f968b3fe`. A tile is counted in $M$ if it has no actual half-turn mate across its entire long side. A reflection across a long side does not qualify as such a mate.

| Necessary condition | 3431 | 5063 |
|---|---:|---:|
| Unmatched owners on the entering cut of any occupied exterior-free terminal short node, both banks together | ≥16 | ≥16 |
| Total unmatched tiles if either prime tree has any occupied exterior-free short node | ≥123 | ≥165 |
| Total unmatched tiles without that hypothesis | ≥109 | ≥149 |
| Angular inventory combinations at the previous lower endpoints ($M=107,149$), before and after the joint tests | 2 → 0 | 8 → 7 |

These bounds use actual whole edges, including across split contacts. The terminal result is sharp for a local polygon with specified contact owners for both tile shapes. The 5063 polygon has just two owners in the parent bank. The sharpness claim concerns this local information alone.

- [Physical contact identity and terminal theorem](TERMINAL.md). Includes the reduction from arbitrary positions to one finite boundary word and the independent integer enumeration. Below the nonnative thresholds it gives one exact signed-bank profile at 3431 and two at 5063.
- [Equality geometry at the two distinguished cuts](JUNCTIONS.md). Directed cycles are excluded in every saturated inventory. The same three-direction combination fails on both boards. The torus currents of the axial core exclude the other combination at 3431.
- [5063 local coordinates](patch5063.json) and [exact reconstruction](patch5063.py). The last two entries are parent tiles.
- [Nested-cut theorem](../boundary-word/README.md), [joint-cell reserves, gate theorem and terminal divisibility](../../../2026-11-20/semiprimes/continuation/common-obstruction/README.md), and [ordinary-node budgets](../../../2026-11-20/semiprimes/continuation/vertex-phase/README.md).

The 45/58 bounds count ordinary phase nodes. The present bounds count physical owners, so adding the two budgets would count some tiles twice. Neither the native two-height floors 555/731 nor removal of an arbitrary balanced branch is used. All orientation and sign assignments refer to the standard vertex-phase board. Local changes of coordinates are specified in the proofs. The F2 restrictions here are necessary for the indicated boards. The outstanding cases prevent an impossibility conclusion even at the F2 stage.

## Reproduce

In this directory run `python3 -u replay.py --independent` with a C++17 compiler named `c++` on PATH. Python assertions must be enabled. The shorter default replay omits only the independent integer-tuple terminal enumeration. [Recorded output](REPLAY.txt) and [machine-readable status](STATUS.json) accompany the checks. Both complete 143 controls verify the physical contact identity before either target-specific word search starts.
