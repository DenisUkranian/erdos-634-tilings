# Independent audit of the finite physical charge-budget criterion

21 November 2026. The theorem in
[PHYSICAL_CHARGE_BUDGET.md](../rigid-body/PHYSICAL_CHARGE_BUDGET.md)
was independently checked and is sound with its stated complete-row
and established-placement hypotheses. **It is a criterion, not a
computed exclusion of 3431 or 5063.**

## Complete rows and the charge lower bound

At one actual endpoint with one fixed unoriented side direction,
there are at most 24 congruent placed triangles: three side lengths,
two endpoint rays, two assignments of the other side lengths to the
ends, and two sides of the supporting line. Exact containment filters
may remove placements. For a finite row set `R`, complete enumeration
therefore gives a finite set `V(R)` containing every physical tile
which can affect a selected row.

If a full tiling exists, its induced selection `I` in `V(R)` is an
independent set in the actual interior-overlap graph. Omitted tiles
have zero coefficients on all rows of `R`, by completeness, so `I`
balances them exactly. Each omitted tile contributes one unit with a
sign to exactly one of the odd or even charge inventories. Hence

\[
 N\ge |I|+|G_{\rm odd}-g_{\rm odd}(I)|
             +|G_{\rm even}-g_{\rm even}(I)|.
\]

The minimum over all row-balanced independent subsets is therefore
a valid lower bound. The optional rounding to a proved containing
set of full odd populations is also valid. The omitted odd and even
tiles are disjoint, so no contact or population reserve is counted
twice.

An unfinished row using only a temporary finite candidate pool is
not complete in this sense. Infeasibility caused by such a row
cannot be substituted for the theorem's minimum.

## Finite-depth completeness

For a hypothetical full tiling, form the bipartite graph of its
selected tiles and all their nonzero physical endpoint/direction
rows. A component containing a tile must meet a nonzero board row.
Otherwise full row balance gives zero current for the component,
since every tile affecting one of its rows is in that same component.

Physical endpoint rows determine full boundary currents: on each
actual supporting line, the signed interval function has compact
support and its derivative is the endpoint counter. A zero counter
means a zero interval function. Green's area identity then makes a
zero-current component have total signed area zero. All its actual
counterclockwise triangles have positive area, a contradiction.

Every tile is consequently reached from a nonzero board row by a
simple incidence path with at most `N` tile vertices. Complete
row-to-incident-tile expansion through `N` tile steps contains the
entire tiling. The finite-degree argument requires no guessed height
or denominator bound. It retains the established exact placement and
orientation framework and a complete incident oracle.

Imposing full actual endpoint equations and Boolean choices on this
finite containing catalogue is equivalent to a tiling, by the
[physical-current theorem](FULL_CURRENT_AND_NONOVERLAP.md). The
catalogue can be extremely large. The completeness proof does not
provide an efficient enumeration or an infeasibility result.

## Monotonicity under adding complete rows

The unrounded lower bound `L(R)` is monotone when complete finite
row sets increase. If `R` is contained in `S`, take any feasible
selection `J` for `S` and retain `I=J intersect V(R)`. Completeness
makes `I` feasible for `R`. Every removed tile changes only one
signed charge by one, so the triangle inequality gives

\[
 |I|+\|G-g(I)\|_1\le |J|+\|G-g(J)\|_1.
\]

Taking minima proves `L(R)<=L(S)`. This helps interpret successive
necessary projections, but it supplies no target contradiction on
its own. No value exceeding 3431 or 5063 has been verified here.
