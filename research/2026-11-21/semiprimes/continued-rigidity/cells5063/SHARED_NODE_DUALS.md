# Exact new endpoint cuts for shared-node cell currents

21 November 2026. The certificates in this folder give exact population
bounds for individual recorded cell current lists. They do not exhaust
the two-cell or four-cell current universe and do not exclude 5063.

## A cell inequality that remains valid when exact nodes are shared

Let `L` be an ordinary Euclidean cell at short height one, with upward and
downward integer gate lists `Q_up,Q_down`, each of length 43. A certificate
contains three integer endpoint potential tables, two integer gate weight
lists `lambda_up,lambda_down`, and a positive integer `D`. For every tile
column, compute its counterclockwise endpoint weight on its two short
sides, and add its signed gate weight. If every resulting score is at
most `D`, then

\[
\sum_r \lambda_{\rm up}(r)Q^L_{\rm up}(r)
+\sum_r \lambda_{\rm down}(r)Q^L_{\rm down}(r)
\le D n_L. \tag{1}
\]

Indeed, the endpoint terms cancel in the complete cell boundary identity.
Period 43 makes every whole long edge of this height have zero endpoint
weight, and the exterior has no side of this short height. Summing the
per-tile inequalities gives (1), including arbitrary T-junctions. It does
not require the cell to fill an exact node of either prime tree.

For a shared exact node `V`, the complete gate list is the sum over its
incident cells:

\[
Q^{V}_{\rm up}(r)=\sum_{L\ni V}Q^L_{\rm up}(r),\qquad
Q^{V}_{\rm down}(r)=\sum_{L\ni V}Q^L_{\rm down}(r). \tag{2}
\]

Only these complete lists satisfy the even-branch congruences

\[
Q^V_{\rm up}(r)=86\,1_{V\text{ native},r=0}+22E^V_r,
\qquad
Q^V_{\rm down}(r)=-43\,1_{V\text{ native},r=0}+22E^V_r,
\quad E^V_r\in\mathbb Z. \tag{3}
\]

The exploratory master keeps an independent integer `Q^L` for each cell
and imposes (3) on the sums (2). It does not impose the complete-node
congruence on a proper subcell.

The two prime residue maps are independent modulo 43. A cell's coordinate
origin can therefore align its two hand lists with the chosen full-node
gate labels. Every independent cyclic shift of the two certificate lists
is consequently included, together with the twelve geometric symmetries.
The finite shifted family has the equivalent maximum form

\[
\max_u\langle Q^L_{\rm up},\lambda_{\rm up}(\cdot+u)\rangle
+\max_v\langle Q^L_{\rm down},\lambda_{\rm down}(\cdot+v)\rangle
\le Dn_L.
\]

In discovery this can be represented by two unrestricted continuous
maximum variables, 43 lower-bound constraints for each, and one constraint
on their sum. The extended formulation changes no member of the cut family.

## The first old-pool survivor is now excluded

The [finite old-pool witness](FINITE_CUT_POOL_LIMIT.md) had one balanced
86-cell and one charged 129-cell. In the latter cell,

\[
Q_{\rm up}(0)=34,\quad
Q_{\rm up}(9)=Q_{\rm up}(11)=Q_{\rm up}(23)=3,\quad
Q_{\rm down}\equiv0.
\]

This list passed every translated and transformed inequality from the
earlier 65-certificate pool. The new
[`shared_profile_cut_001.json`](shared_profile_cut_001.json) gives instead

\[
n_L\ge\frac{143166999}{1000001}>129.
\]

An actual cell with charge 43 has odd population, so this particular list
would require at least 145 tiles. This excludes the recorded 129-cell list;
it does not exclude every possible shared-node 129-cell.

The first nine certificates were generated adaptively against other
two-cell current candidates with native whole-node currents 42 and 1.
Each certificate is universal as an inequality of the form (1); the fixed
profile was used only to select a useful certificate. Their individual
recorded bounds are included in
[`SHARED_PROFILE_DUALS_REPLAY.json`](SHARED_PROFILE_DUALS_REPLAY.json).
Later hash-named certificates, if present in that replay, use the same
independent validation.

## Independent exact replay

Run:

```sh
python3 verify_shared_profile_duals.py
```

The checker imports the existing independent polygon audit, not the
numerical discovery model. For each certificate it reconstructs all
`12*43^2=22188` oriented residue triangles, orders each triangle boundary
counterclockwise, identifies its 35-, 13-, and 43-edges by exact squared
lengths, and verifies every score by integer arithmetic. It separately
recomputes the bound for the stored integer current list and its parity
consequence. The replay records certificate hashes.

The discovery files use SciPy only to suggest coefficients. Rounding a
floating dual is harmless here because `D` is recomputed as the exact
maximum of all tile-column scores and the independent checker verifies
that maximum bound. Numerical infeasibility, time limits, or a master
with no returned incumbent do not become mathematical exclusions.

`discover_cell_cut.py` first offers an additive marginal relaxation. Its
`--full` option uses the full 22,188-column endpoint relaxation. For an
infeasible prescribed current list a residual-penalty LP can still
suggest a separating dual; only the exported all-column inequality is
used as an exact result. Floating positive column solutions, if returned,
remain relaxation diagnostics until an exact witness is reconstructed,
and even an exact periodic witness would not be a physical tiling.
