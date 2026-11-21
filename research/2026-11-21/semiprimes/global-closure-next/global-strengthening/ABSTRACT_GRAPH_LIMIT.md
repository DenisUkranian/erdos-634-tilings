# Exact limits of the joint contact-graph and global-moment bounds

21 November 2026. **Neither 3431 nor 5063 is decided here.** The new
joint contact-graph theorem is valid, but the previously published
abstract axis inventories satisfy all of its charge-energy, connectedness,
area-energy, mean-centering, and global covariance constraints. The
following exact calculation identifies the additional geometry that
still has to be imposed.

The input is the existing
[two-tree axis inventory](../../../../2026-11-20/semiprimes/continuation/charge-transport/joint/ABSTRACT_AXIS_FLOW.md).
It already has the required orientation, hand, sign, cell, axis and
boundary-port counts, but no common geometric realization. This note
does not supply that realization or a nonoverlapping odd-only packing.

## 1. Two connected bands suffice for the abstract inventory

Let `d=a-b`, and choose an odd integer `K>=3` with `N-Kc-d>=0`.
The old inventory has `Kc` tiles in the height-one middle cell and
`N-Kc` in the height-zero core. Its signed populations are `-c` and
`-d`. Designated half-turn pairs leave

\[
 M_1=2c+d,\qquad M_2=c,\qquad M=3c+d
\]

unmatched tiles in bands one and two. Each band graph has two
vertices joined by that many parallel edges. Both are connected,
and their opposite-level subtree populations partition all `N`
tiles as required by the new band lemma.

The complete cut data are:

| Tree / physical band | `n_e` | `w_e` | `U_e` | `V_e` | `P_e` | `Q_e` |
|---|---:|---:|---:|---:|---:|---:|
| Increasing / 1 | `Kc` | 1 | `2c` | `d` | `-2c` | `-d` |
| Decreasing / 1 | `N-Kc` | 2 | `d` | `2c` | `-d` | `-2c` |
| Increasing / 2 | 0 | 1 | 0 | `c` | 0 | `c` |
| Decreasing / 2 | `N` | 2 | `c` | 0 | `c` | 0 |

On the increasing vertices the area demands are

\[
 F_1=3Kc-N-2c+d,\qquad F_2=c-N.
\]

On the corresponding decreasing vertices they are their negatives.
Thus all component balances hold. The graph energy is exactly

\[
 \mathcal E_F=\frac{F_1^2}{2c+d}+\frac{(N-c)^2}{c}.
                                                               \tag{1}
\]

The physical vector sums, as prescribed by the axis inventory, are
`W=(A,-B)` on both increasing vertices and `-W` on the other two;
`|W|^2=c^4`. Consequently the rank-two mean correction reduces to
the following exact two-by-two matrix on independent band potentials:

\[
 D_0=\begin{pmatrix}2c+d&0\\0&c\end{pmatrix}
      -\frac{c^2}{N}\begin{pmatrix}1&1\\1&1\end{pmatrix}.
\]

It is positive definite in all the checked cases. The centered energy
is `(F_1,F_2) D_0^{-1}(F_1,F_2)^T`.

## 2. Every joint charge-energy bound passes exactly

On the increasing vertices the two charge divergence vectors are

\[
 \alpha=(d-2c,-c),\qquad \beta=(-(2c+d),c).
\]

Both are negated on the decreasing vertices. Direct evaluation gives

\[
 \alpha^TL_H^\dagger\alpha
 =\frac{(2c-d)^2}{2c+d}+c
 =M-\frac{8cd}{2c+d}<M,
\]

\[
 \beta^TL_H^\dagger\beta=M,\qquad
 \alpha^TL_H^\dagger\beta=c-d.
\]

The actual unit-flow correlation in this inventory is also `T=c-d`.
Therefore for every `u,v` the difference between the right and left
sides of the joint charge-energy inequality is

\[
 \frac{8cd}{2c+d}\,u^2\ge0.
\]

All charge cut bounds and parities hold as well: they are supplied
by the explicit `+1/-1` flows on the parallel physical edge copies.
This is an exact feasibility statement for the specified graph
projection, not a numerical solver result.

## 3. The two previously relevant populations have substantial moment slack

The replay checks the old choices `K=15` at 3431 and `K=17` at 5063.
Those are the original abstract inventories selected to meet the
earlier conditional population bounds.

| Target | Odd tiles | Unmatched tiles | Exact centered area energy | Exact available `K_M` | Budget used, approximately |
|---:|---:|---:|---|---|---:|
| 3431 | 555 | 137 | `485173732268/1389683` | `789364406106/5929` | 0.262232% |
| 5063 | 731 | 151 | `15645750366800/23233373` | `2193255502904/15925` | 0.488961% |

The displayed decimals only describe size; all comparisons use
fractions. In particular replacing the separate tree estimates by
the full joint graph and its centering correction does not exclude
either of these inventories.

## 4. Exact orientation covariance does not exclude them either

This check retains the actual short height, rotation and hand of
every abstract tile copy. For a triangle with edge vectors `v_i`,
its uniform covariance in axial coordinates is

\[
 C_T=\frac1{36}\sum_{i=1}^3 v_i v_i^T.
\]

Let `C_B` be the board covariance. Subtracting the orientation-dependent
tile covariances and the known paired-centroid offsets gives the
required reduced centroid covariance

\[
 S_M=N C_B-\sum_t C_{T_t}
              -\sum_{\text{pairs}}2\delta_t\delta_t^T.          \tag{2}
\]

This matrix is fixed by the abstract orientation inventory. Its
Euclidean trace is precisely the scalar reserve used in the theorem.

The checker constructs rational reduced centroid vectors `x_t^0`
which satisfy the zero total mean and both exact area-flow rows,
minimizing the Euclidean squared norm. On every paired tile the
vector is the same common value `x_pair`. The resulting covariance
`C_0=sum_t x_t^0(x_t^0)^T` is reconstructed exactly. In both cases

\[
 R=S_M-C_0\succeq0.                                \tag{3}
\]

The replay lists all entries and verifies the diagonal and determinant
conditions for the two-by-two matrix (3) using rational arithmetic.

Equation (3) is enough for a full abstract covariance completion.
Choose real vectors `u,v` with `R=4uu^T+4vv^T`, possible because
`R` is positive semidefinite. There are at least four designated
half-turn pairs. Replace the reduced common midpoints of four such
pairs by

\[
 x_{\rm pair}+u,\quad x_{\rm pair}-u,\quad
 x_{\rm pair}+v,\quad x_{\rm pair}-v.
\]

Each midpoint occurs twice, once for each tile of its pair. These
changes preserve the global mean, add exactly `R` to the covariance,
and do not alter any area-flow row because paired tiles have zero row
coefficients. Restoring each pair's opposite centroid offsets preserves
its correct rigid half-turn geometry. Thus the abstract data satisfy
all the tensor inequalities with every positive-definite test matrix,
not merely the isotropic trace inequality.

**This completion supplies global moments only.** The centroids are
not claimed to be contained in the board, to have the assigned phase
coordinates, or to realize common contacts. Several abstract copies
may coincide or overlap. The argument does not manufacture a physical
tiling from the moment equations. Its purpose is to show precisely
that these moment equations alone cannot rule out the inventories.

## 5. A complete finite range for this particular projection

The exact verifier also checks every nonnegative integer inventory of
the displayed one-parameter form:

* 3431: all 45 odd values `K=3,5,...,91`;
* 5063: all 58 odd values `K=3,5,...,117`.

Every one satisfies the new joint charge, connectivity, centered area,
and covariance-completion conditions. The largest centered area-budget
fractions in the respective finite checks are

\[
 \frac{3090211141735102}{548483147985302199},\qquad
 \frac{69647072391373750}{6369590397908901899}.
\]

Some of these inventories violate other, already proved restrictions.
For example this standalone projection does not contain the endpoint
certificates which exclude the 5063 population 129. The range check
does not reopen that excluded case or assert feasibility of the full
combined relaxation. The two selected inventories in Section 3 are
the relevant established larger-population controls.

## 6. What remains missing

The new theorem controls the energy and connectivity of a genuine
contact graph. These abstract witnesses show that it has not yet
forced an impossible energy or tile count. Exclusion must retain
additional information such as the actual supporting lines of the
contacts, phase-compatible common endpoints, local sector order,
individual placement containment coupled to those interfaces, or
the exact integer covering multiplicity.

The separate [physical-current audit](FULL_CURRENT_AND_NONOVERLAP.md)
explains the last point: once all actual endpoint currents close
with nonnegative integer placement multiplicities, nonoverlap and
coverage already follow. The missing step is obtaining a verified
infeasibility certificate for that physical system, not asserting
that its formulation alone establishes infeasibility.

## Reproduce

```sh
python3 verify_abstract_joint_graph.py
```

The verifier uses only Python's standard library. It reconstructs the
inventory arithmetic, both graph bands, charge energies and correlation,
centering matrix, all required covariances, and their exact positive
semidefinite completion. The output is
[`ABSTRACT_JOINT_GRAPH_REPLAY.json`](ABSTRACT_JOINT_GRAPH_REPLAY.json).
