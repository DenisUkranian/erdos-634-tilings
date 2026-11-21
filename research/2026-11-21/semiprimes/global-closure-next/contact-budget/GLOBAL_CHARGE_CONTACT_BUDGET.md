# The one-tree form of the global charge and contact budget

21 November 2026. Research in the Denis Paliy project, with ChatGPT assistance.

The [joint contact-graph theorem](../common/JOINT_CONTACT_GRAPH.md) is the
main result of this continuation. It couples both prime trees using one
edge for each physical unmatched tile. This companion gives its one-tree
corollary, a detailed derivation of the centroid budget, and the elimination
of the unsigned crossing counts in favor of signed charge and area demands.

**Result.** The phase transport identities admit a global quadratic geometric
budget, valid at every odd population. It couples the odd charge, the area
behind each actual contact, and the total number of available tiles.
Whole-long-side half-turn pairs consume a geometric reserve even after
their boundary currents cancel.

**Scope.** This is a necessary theorem for complete positive tilings in the
established phase framework. It assumes neither the minimal three-block
mode, a unique odd phase, terminality, nor a prescribed height interval.
Reflections and partial contacts are retained. The inequalities do **not**
yet exclude the complete 3431 or 5063 tilings. Both counts remain **OPEN**.

## 1. Setting and geometric inputs

Use the standard unit F2 frame
\[
 \rho=e^{i\pi/3},\quad z=(a+b\rho)/c,\quad
 c^2=a^2+ab+b^2,\quad d=a-b>0,
\]
\[
 A=b(2a+b),\quad B=a(a+2b),\quad
 T=\operatorname{conv}\{0,A,B\rho\},\quad N=(a+2b)(2a+b).
\]
The tile area is \(\Delta=\sqrt3 ab/4\). The board has side lengths
\(A,B,c^2\) and area \(N\Delta\). A placement has short height \(h\),
hand \(s=\pm1\), and sign \(\epsilon=s(-1)^j\). Its long-edge node is
adjacent to its short node in either prime phase tree. In this frame
\[
 G_{\rm odd}=-c,\qquad G_{\rm even}=-d.                 \tag{1}
\]

Fix **one** of the two trees. The theorem can be applied separately in
the other tree; their unweighted tile budgets must not be added.

For a parent/child edge \(e\), let \(S_e\) be the child subtree, let
\(n_e\) count the actual tiles whose short nodes lie in \(S_e\), and let
\(k_e\) be the child's physical height. Put
\[
 G_e=\sum_{\operatorname{short}(t)\in S_e}\epsilon_t,\qquad
 G_{*,e}=\sum_{\operatorname{short}(t)\in S_e}(-1)^{h_t}\epsilon_t.
\]
The subtree's odd charge is \((G_e-G_{*,e})/2\).
Let \(\delta_0(e)\) and \(\delta_2(e)\) indicate that the subtree
contains the exterior core edge node and the exterior height-two edge
node, respectively. The core contains both axial outer sides. Set
\[
 w_e=2\delta_0(e)+\delta_2(e),\qquad
 b_e=(A+B)\delta_0(e)-c^2\delta_2(e).                  \tag{2}
\]

Let \(P_e\) be the signed population of root tiles whose long-edge node
is the parent, and \(Q_e\) that of parent tiles whose long-edge node
is the root. The established exact transport equations are
\[
 c(P_e-Q_e)=(c-d)G_e+b_e,\qquad
 c(-1)^{k_e}(P_e+Q_e)=(c+d)G_{*,e}-b_e.              \tag{3}
\]
The physical boundary-chain identity is
\[
 \partial U_{S_e}-\Gamma_e=\mathcal A_e-\mathcal B_e. \tag{4}
\]
Here \(U_{S_e}\) is the union of the actual subtree tiles;
\(\Gamma_e\) is the sum of the complete outer sides whose edge nodes
lie in the subtree; and \(\mathcal A_e,\mathcal B_e\) are the two
whole-long-side chains defining \(P_e,Q_e\).
In particular \(\Gamma_e\) is not a guessed exposed portion of
\(\partial U_{S_e}\). The chains permit partial cancellations.

These are inputs from
[signed cut transport](../../../../2026-11-20/semiprimes/continuation/charge-transport/flux/SIGNED_CUT_TRANSPORT.md)
and [signed phase populations](../../../../2026-11-20/semiprimes/continuation/vertex-phase/SIGNED_PHASE_POPULATIONS.md).
The physical chain identity, rather than an abstract contact-port
matching, is essential.

## 2. The global theorem

Cancel every **actual** whole-long-side half-turn pair as a boundary
current. This does not delete tiles from the tiling, change \(n_e\),
or provide a retiling operation. Such a pair has opposite signs and
the same short and long nodes; it cancels within one crossing class.

Let \(u_e,v_e\) count the remaining tiles in the \(P_e,Q_e\) classes.
Put \(m_e=u_e+v_e\) and \(M=\sum_e m_e\). Use the complete collection
of edges carrying remaining tiles. Each remaining tile belongs to
exactly one edge, so \(M\le N\) is the total unmatched population and
\(N-M\) is even. Edges with \(m_e=0\) can be included using the zero
convention below.

Define
\[
 S=A^2+B^2+c^4-a^2-b^2-c^2,\qquad D=a^2+b^2-ab.       \tag{5}
\]

**Global charge/contact budget theorem.** Every complete positive
tiling satisfies (3), the integer reserves
\[
 \begin{aligned}
 u_e&\ge |P_e|,&u_e&\equiv P_e\pmod2,\\
 v_e&\ge |Q_e|,&v_e&\equiv Q_e\pmod2,\\
 \sum_e(u_e+v_e)&=M\le N,
 \end{aligned}                                      \tag{6}
\]
and the joint geometric inequality
\[
 \boxed{
 \sum_{e:m_e>0}
 \frac{(3n_e-Nw_e-u_e+v_e)^2}{m_e}
 \ \le\
 \mathcal K(M):=
 \frac{c^2}{3a^2b^2}\left[NS-(N-M)D\right].
 }                                                   \tag{7}
\]
If \(m_e=0\), then \(3n_e-Nw_e-u_e+v_e=0\).
A nonzero numerator with zero denominator is impossible.

Although \(n_e\) counts a tile at each ancestor subtree, the
denominators in (7) use **disjoint physical tiles**. The theorem does
not add population costs from the two trees or from repeated bank
incidences. Ignoring the paired-tile reserve gives the weaker bound
\(\mathcal K(N)=c^2NS/(3a^2b^2)\).

### A charge-only description of the required load

Set
\[
 p_e=|P_e|,\quad q_e=|Q_e|,\qquad
 L_e=p_e+q_e+\left|3n_e-Nw_e-p_e+q_e\right|.           \tag{8}
\]
The same tiling satisfies
\[
 \sum_e\frac{(L_e-m_e)_+^2}{m_e}\le\mathcal K(M),
 \qquad m_e\ge p_e+q_e,\qquad \sum_e m_e=M\le N,       \tag{9}
\]
with the same zero convention. Consequently
\[
 \boxed{\sum_e L_e\le M+\sqrt{M\mathcal K(M)}
                     \le N+\sqrt{N\mathcal K(N)}.}    \tag{10}
\]
For an exterior-free subtree, \(w_e=0\) and \(n_e\ge p_e\), giving
\[
 \boxed{L_e=3n_e+2|Q_e|.}                             \tag{11}
\]

Thus the subtree odd and even charges determine \(Q_e\) through
(3), its actual enclosed area determines \(n_e\), and their combined
load must fit one global tile and geometric budget. Moving imbalance
to a remote branch does not erase its area or parent-bank cost.
For a terminal exterior-free node of charge \(cg\), the transport
equations give \(P_e=cg,Q_e=dg\), so its load is
\(3n_e+2d|g|\). The theorem does not assert that the whole odd charge
must occur in a terminal node.

## 3. Proof

### 3.1 A long side records its centroid and one third of the tile area

Let \(o\) be the board centroid and \(x_t\) a tile centroid. If
\(u\to v\) is that tile's counterclockwise long side and
\(\ell_t=v-u\), then
\[
 \det(u-o,v-o)=\det(x_t-o,\ell_t)+\frac{2\Delta}{3}.    \tag{12}
\]
Joining a triangle's centroid to its three sides gives three equal
areas, proving the formula for both hands and all rotations.
Every long vector has length \(c\).

Apply the centered determinant to (4). Each outer side has centered
determinant \(2N\Delta/3\), and \(\Gamma_e\) has \(w_e\) such sides.
After the half-turn pair cancellations, (12) yields
\[
 \frac{2\Delta}{3}(3n_e-Nw_e-u_e+v_e)
 =\sum_{t\in\mathcal C_e}\tau_t\det(x_t-o,\ell_t),     \tag{13}
\]
where \(\mathcal C_e\) is the unmatched crossing class, and
\(\tau_t=+1\) on the root bank and \(-1\) on the parent bank.
The identity retains the actual contact positions and telescopes
through all partial contacts and T-junctions.

The unmatched crossing classes may include sides whose contributions
cancel partly or completely as intervals. The argument does not
assume that every counted side survives fully on the physical
boundary. Counting them only weakens the upper capacity.

### 3.2 The complete tiling has a fixed centroid moment

For a triangle with side lengths \(l_1,l_2,l_3\), the mean squared
distance from its centroid is
\((l_1^2+l_2^2+l_3^2)/36\).
Decompose the board's second moment into those of its disjoint
congruent tiles:
\[
 \sum_{t=1}^N|x_t-o|^2=\frac{NS}{36}.                 \tag{14}
\]
The banks cannot each use the entire board's second moment.

### 3.3 Cancelled pairs still consume a reserve

A half-turn pair has centroids \(m+\delta,m-\delta\), with \(m\)
the common long-side midpoint. The median formula gives
\[
 |\delta|^2=\frac{2a^2+2b^2-c^2}{36}=\frac D{36}.
\]
Its contribution to (14) is
\[
 |m+\delta-o|^2+|m-\delta-o|^2
 =2|m-o|^2+\frac D{18}\ge\frac D{18}.                 \tag{15}
\]
There are \((N-M)/2\) cancelled pairs, hence
\[
 \sum_{t\text{ unmatched}}|x_t-o|^2
 \le\frac{NS-(N-M)D}{36}.                            \tag{16}
\]
This is a reserve within the same \(N\) tiles.

### 3.4 Sum over the disjoint banks

Cauchy--Schwarz in (13) gives
\[
 \frac{(3n_e-Nw_e-u_e+v_e)^2}{m_e}
 \le\frac{9c^2}{4\Delta^2}
       \sum_{t\in\mathcal C_e}|x_t-o|^2.
\]
The classes \(\mathcal C_e\) partition the unmatched tiles. Sum and
apply (16), then use \(4\Delta^2=3a^2b^2/4\), to obtain (7).
The zero-denominator case follows from (13).
The cancelled pairs have opposite signs in the same crossing class,
which proves the reserves (6) and preserves (3).

For (9), write \(u_e=p_e+x,v_e=q_e+y\), where
\(x+y=m_e-p_e-q_e\) and \(x,y\ge0\). Thus \(u_e-v_e\) lies in the
interval centered at \(p_e-q_e\) with radius \(m_e-p_e-q_e\).
The distance from \(3n_e-Nw_e\) to that interval is
\((L_e-m_e)_+\). Finally
\[
 \sum_e L_e\le M+\sum_e(L_e-m_e)_+
 \le M+\sqrt{M\sum_e(L_e-m_e)_+^2/m_e},
\]
giving (10). Integer parity in (6) can further strengthen the interval
distance; omitting that rounding is safe.

## 4. Quantitative scope

The previous estimate was
\(\sum_e(|P_e|+|Q_e|)\le N\).
The new condition also measures enclosed populations, their actual
area flux, the fixed second moment of the board, and the reserve of
cancelled pairs. It applies to every possible odd population.

The isotropic capacity is nevertheless large at the target boards:

| Target | Tile | Odd charge | \(S\) | \(D\) | \(\mathcal K(N)\) |
|---:|---|---:|---:|---:|---|
| 3431 | (33,7,37) | -37 | 4,538,376 | 907 | 789515891432/5929 |
| 5063 | (35,13,43) | -43 | 9,138,024 | 939 | 4073594899128/29575 |

No violation of (7) for every admissible target profile has been
proved. In particular it does not reduce the original existence
questions to the excluded 5063 population 129.

An orientation-sensitive tensor form and the correction using
the known displacements of the exterior chains are recorded in the
[independent review](../common/CONTACT_INERTIA_AUDIT.md).
They are additional forms of this geometric theorem, not target
nonexistence certificates.

## 5. Exact controls

From the repository root, run:

    python3 research/2026-11-21/semiprimes/global-closure-next/contact-budget/verify_contact_budget.py

The standard-library checker independently checks congruence,
containment, and complete boundary-current coverage of two different
143 tilings. It reconstructs every cut in both prime trees, finds the
actual half-turn pairs, and checks signed transport, area flux,
centroid inertia, the pair reserve, (7), and (10) using rationals.

| Complete control | Half-turn pairs | Unmatched tiles | Left side of (7), either tree |
|---|---:|---:|---|
| Original 143 tiling | 60 | 23 | 29696/7 |
| Different 143 macro tiling | 60 | 23 | 98351/28 |

Different costs at the same total count, odd charge, and unmatched
population illustrate the retained geometric information.
The universal proof is above. The finite checks test its implementation
and conventions; they are not Lean formalization or external peer review.
