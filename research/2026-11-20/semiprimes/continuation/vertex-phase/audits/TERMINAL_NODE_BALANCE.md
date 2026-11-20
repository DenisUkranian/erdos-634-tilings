# Independent audit of terminal-node sign balance

The audit-time paths and hashes below identify the working snapshots. Publication relocates imports, renames the signed replay scripts, and adds the separately checked shared-height explanation and explicit conjugate-tree scope. The final code hashes and fresh executed controls are recorded in [the package replay](../REPLAY.json). These internal audits are not external refereeing.

20 November 2026. Snapshot: `theory/TERMINAL_NODE_BALANCE.md`, SHA-256 `d5773a89874daca3007e1917d97b240f2ca524c743887cbef5dfc717261c57e4`. Arithmetic replay: `theory/verify_terminal_balance.py`, SHA-256 `a4e160366bbc97f463aba2d90e46d285c423b9ed6b648ca0f48d05c5ee1f8916`.

**Assessment.** I found no error in the stated theorem: an exterior-free node, terminal in the full tiling, with population exactly `2c` has signed populations `(c,c)` for both target tiles. The geometric argument and the numerical contradictions are consistent. The theorem does not apply to an arbitrary ordinary node, nor to a node whose generated descendants happen to be absent from a finite catalogue.

## Whole-edge pairing

In the positive-valuation tree, a tile at short height `h` with hand `s=+1` has a long edge at a child node of height `h+1`. A tile on the opposite bank can have short height only `h`, `h+1` or `h+2`: these are the possible short heights of a tile having an edge of height `h+1`. The integral-offset lemma puts each such edge in the same child node. Terminality excludes short nodes at the latter two heights; for short height `h`, the child's parent is uniquely the original node. Exterior-freeness excludes an outer interval.

Thus every segment on either bank of the maximal finite supporting run is a whole edge of length `c` from a tile in the original node. The two banks have the same support, hence the same end points. Starting at either common end point, both partitions advance by successive lengths `c`; their edge divisions therefore coincide. This justifies whole-edge matching despite possible T-junctions elsewhere.

Across a matched edge, both tiles have the same short height and hand. Their opposite directed long sides force rotations differing by 3. They are half-turn mates and have opposite `epsilon=s*(-1)^j`. Consequently a terminal one-sign node has no `s=+1` tiles. The conjugate tree reverses the heights and excludes `s=-1` instead. A reflected mate would have short height two levels farther into the forbidden descendant subtree, so it is not a missing possibility.

## Line families and the arithmetic contradictions

With one hand and one sign fixed, only three rotations are available. For a pair of supporting lines, the hand determines which line carries the `a` edge; the sign selects one of the opposite 120-degree sectors. There is therefore at most one such tile at their crossing. This gives both `2c<=r0*r1+r1*r2+r2*r0` and the directed capacities `M_i<=r_(i-1)`, `L_i<=r_(i+1)`. Including both hands would invalidate this uniqueness argument.

For each line, the common tile sign makes the short-edge character sum a common factor times `a*M-b*L`; complementary long edges contribute multiples of `c`. Exterior-freeness removes the outer contribution. The congruence therefore survives multiple disconnected runs. The cyclic aggregate pair on family `i` is correctly `(n_i,n_(i+1))`, since tiles with their `a` line in family `i+1` have their `b` line in family `i`.

At 5063, the integer substitutions give `sum(t)=42`, `sum(s)=10`, and every used line satisfies `s<=t-2`; hence `r<=16`. The crossing count would require `86<=floor(16^2/3)=85`, a contradiction.

At 3431, the substitutions give `r<=20`. The per-line bounds imply `M>=1`, `L>=2`, so all three families have size at least 2. If all have size at most 9, every permitted pair has ratio `M/L=4/3`, contrary to equal total edge counts. A unique large family must therefore have size 10, with the other two at most 8. Its aggregate bound of at most 74 forces all ten pairs to be `(4,3)`, giving cyclic rotation counts `(40,30,4)`. Family 2 then has aggregate `(4,40)` and must consist of four `(1,10)` lines. Family 1 is restricted to `(4,3)` lines, whose aggregate `L` cannot be 4. The family indices and capacities are consistent throughout this step.

I ran `verify_terminal_balance.py`; its congruence substitutions and finite pair lists passed. The replay checks arithmetic only. Whole-edge matching and crossing uniqueness depend on the geometric reasoning above.

Any solver use must retain the full-tiling terminal hypothesis. In particular, a one-sign allocation of two auxiliary capacity blocks in a partial catalogue does not prove an actual population of exactly `2c`, and an empty generated descendant list does not prove terminality. The audited statement alone does not justify forbidding such partial assignments.
