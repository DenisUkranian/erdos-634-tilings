# No 56-tiling, and the complete square class 14

**Erdős problem 634 — Denis Paliy, research with ChatGPT assistance**  
**9 October 2026**

## Status and scope

This package supplies a computer-assisted exclusion of the global count 56 and, using the prior constructions, a complete classification of the square class 14:

\[
\boxed{14m^2\in\mathcal S\quad\Longleftrightarrow\quad m\ge3,\qquad m\in\mathbb Z_{>0}.}
\]

Here \(\mathcal S\) is the set of counts for finite dissections of some nondegenerate triangle into congruent nondegenerate triangles. Reflections and arbitrary T-junctions are permitted.

The exact finite certificates and the new necessary boundary-path test are distinct from the prior positive constructions and angular/rationality classification. The global exclusion uses the complete thirteen-row arithmetic reduction of [U], with its explicitly identified published classification and rationality inputs. We do not reprove those outside theorems here. The finite arithmetic overlist is independently recomputed by `check_gate.py`, and its geometric cases are closed below.

All three finite negative certificates were replayed by a Python rational-arithmetic verifier which imports neither the C++ search nor its boundary-update code. This is internal independent implementation and mathematical review, not external peer review or proof-assistant formalization. No claim of priority over other work is made. The general small-scale W/beta problem, the beta-92 case, and the full Erdős problem remain unsettled by this package.

The disputed reverse-apex candidate, packing lemma, assumed scale divisibility, and any assertion that an arbitrary tiling has a predetermined grid or a bounded direction band are NOT premises.

## 1. The complete arithmetic gate for 14 and 56

Separate the classical count families

\[
r^2,\quad r^2+s^2,\quad 2r^2,\quad3r^2,\quad6r^2.
\]

Neither 14 nor 56 belongs to them. The remaining primitive branches and scale formulae are those of [U]. For Group 1 they use

\[
a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad Q=2v^2-u^2,\quad P=3v^2-u^2,
\]

with coprime \(0<u<v\), and coefficients \(Q,P,b,bQ,QP\). The separate double-angle coefficient is also \(b\), but its tile is \((u^2,b,uv)\). The seven norm rows have coefficients

\[
ab\text{ (both norm signs)},\quad b(a+b),\quad b(a+2b),
\quad(a+2b)(2a+b),\quad3(a+b)(a+2b),\quad(a+b)(2a+b).
\]

Every count is its coefficient times an integral square. The normalization and source hypotheses are not to be inferred merely from these displayed expressions; [U] supplies the exhaustive reduction.

`check_gate.py` deliberately uses a different finite enumeration from the repository's factor-based generator. For Group 1 and the double-angle row, it checks all coprime \(1\le u<v\le N\). This bound is safe: the b-rows have \(b\ge2v-1\) and every other Group-1 coefficient exceeds \(v^2\). For norm rows it checks all \(1\le a,b\le N\), since each coefficient is at least \(\max(a,b)\). The code verifies the integer-square multiplier and Heron's exact area identity for every retained row. It retains both orders of a,b, deduplicating identical target/tile pairs within a row.

At 14, the only nonclassical candidate is

| Branch | Tile | Target | Scale |
|---|---|---|---:|
| W | (6,5,9) | (27,28,15) | 1 |

At 56, before geometric removals, the complete list is

| Branch | Tile | Target | Scale |
|---|---|---|---:|
| W | (6,5,9) | (54,56,30) | 2 |
| 120-degree equilateral | (8,7,13) | (56,56,56) | 1 |
| theta | (45,56,81) | (504,504,280) | 1 |
| theta | (195,56,225) | (840,840,728) | 1 |
| double-angle | (25,56,45) | (280,280,504) | 1 |
| double-angle | (169,56,195) | (728,728,840) | 1 |

The four last rows are excluded by the established scale-one isosceles lemmas in [U, Sections 3–4]. Their short geometric arguments are recalled here to make clear that they do not depend on the disputed prime-case argument.

For theta, the apex has one alpha tile, so one equal side contains a b-edge. That side has length bv at scale one. Reducing its whole-edge decomposition modulo v makes the b-count a positive multiple of v. The side would therefore consist of v b-edges. Each such edge has an obtuse gamma endpoint, no outer corner admits gamma, and a straight boundary point admits at most one gamma. There are fewer internal junctions than b-edges: contradiction.

For the double-angle tile \((u^2,v^2-u^2,uv)\), the angles satisfy \(3\alpha+\beta=\pi\), with gamma=2alpha. The equal side incident to the alpha tile at the apex must contain b: otherwise its a/c edges each contribute a beta endpoint, neither outer endpoint can receive beta there, and the straight-vertex inventory admits only one beta. Modulo u, its b-count is a positive multiple of u. At scale one the side has length bu, so it is all b. Each b-edge contributes a 2alpha endpoint, no target corner can receive one, and the straight-vertex equation admits at most one such endpoint. The same junction count is contradictory.

Thus the only remaining cases at 56 are the first two rows. Excluding only the W row would not have proved a global exclusion.

## 2. The necessary blocked-c boundary lemma

The Group-1 statement and its proof are prior project results [B]. We also use the same local argument for the primitive 120-degree tile (8,7,13) and an equilateral target. The applicable hypotheses and the extension are written out rather than silently transferred between angular branches.

Write alpha,beta,gamma for the angles opposite a,b,c. In the two cases used here:

* W with (6,5,9) has \(3\alpha+2\beta=\pi\), \(\gamma=2\alpha+\beta>\pi/2\), and target corners 2alpha, beta, alpha+beta.
* The equilateral target with (8,7,13) has gamma=2pi/3 and alpha+beta=pi/3.

The smaller angle is not required to be alpha. In both cases alpha/pi is irrational: respectively \(2\cos\alpha=14/9\) and \(22/13\), which cannot be rational algebraic integers. The exact corner inventories follow by comparing the rational-pi and irrational-alpha parts. A W corner contains respectively two alpha tiles, one beta tile, or one alpha and one beta; an equilateral corner contains one alpha and one beta. No target corner contains gamma. At a straight point, once beta and gamma are present, the remaining angle is precisely one alpha tile. Also \(\gcd(a,b)=1\) and a,b>1 in the two cases.

### Definition of marked and blocked points

Fix one outer side. A supported edge is a whole tile edge lying on that side. Mark an internal junction exactly when one of these supported a/b-edges presents gamma there. A tile merely touching the side at a gamma vertex is not a mark. No marks coincide, because 2gamma>pi. Call every target corner and every marked point blocked.

### Lemma

A supported c-edge cannot have both endpoints blocked. Consequently every outer side contains two consecutive supported c-edges.

### Proof of the local prohibition

Let the c-edge be PQ, with its tile PQR having alpha at P, beta at Q, gamma at R. Then PR=b, QR=a. At blocked P or Q another gamma is impossible.

If Q is the W beta corner, QR is the other outer side, so R is on the target boundary. Otherwise Q is a marked straight point or an alpha+beta corner. The angular inventory leaves exactly an alpha tile across QR at Q. Its first edge along QR is b or c.

Some opposite edge crosses R in its relative interior. Indeed, c>a immediately crosses, as does b>a. If b<a and no edge crosses R, the complete opposite bank of the intact segment QR would be a whole-edge chain of length a starting with b. Neither c nor a can occur after that positive initial b contribution, so b would divide a, contrary to coprimality and b>1. Whole-edge completeness follows along the unbroken original edge; convexity caps its endpoint at Q. T-junctions do not change this argument.

In this second case R is in the relative interior of a crossing tile edge, which supplies a straight angle pi there. Another gamma at R is impossible, since pi+2gamma>2pi. In the first case another gamma at R is impossible on the outer boundary.

PR cannot be another outer side: then P would be a target corner alpha, absent in both target types. Its opposite bank is a complete whole-edge decomposition of length b. Past P the line leaves the convex target; past R it either leaves the target or enters the crossing tile. No c-edge fits. A b-edge would fill the entire segment and present gamma at P or R, both forbidden. Only a-edges remain, forcing a to divide b, again impossible.

This proves the local prohibition. It includes the equilateral case: Q there is an alpha+beta corner, never a beta corner, and PR cannot be external because no target corner equals alpha.

### Proof of adjacency

Suppose the chosen side has n supported edges, including k c-edges. The n-k other edges provide n-k distinct marked internal junctions. Thus k>=1, and exactly k-1 internal junctions are unmarked. Every c-edge needs an unblocked endpoint, necessarily one of these unmarked internal junctions. Since there are k c-edges and only k-1 such junctions, two c-edges share a junction. They are consecutive. QED.

The lemma is a written geometric input to the boundary-path verifier, not a theorem formally proved by running that program.

## 3. Complete boundary roots for the W56 candidate

The W target has sides (54,56,30) and tile (6,5,9). On its length-30 side, the lemma gives at least two c-edges. The integer equation

\[
6A+5B+9C=30,\qquad A,B\ge0,\ C\ge2
\]

has the unique solution (A,B,C)=(2,0,2). From the 2alpha corner, the first edge must be c: that corner has only alpha tiles, and a is not incident to alpha. The two c-edges must therefore be the first two edges, giving the whole word c,c,a,a.

The first c-edge has alpha at the 2alpha corner. The last a-edge has beta, not gamma, at the other target corner. The preceding a-edge cannot have gamma at that same internal junction, so both a-edges run from their gamma endpoint toward their beta endpoint. Only the second c-edge has two choices. Hence exactly TWO boundary-root configurations exhaust every possible W56 tiling.

For comparison with [B], in coordinates of metric x^2+2y^2 the target is (0,0),(56,0),(46,20). The boundary endpoints from the 2alpha corner are

\[
(46,20),\ (49,14),\ (52,8),\ (54,4),\ (56,0).
\]

The four third vertices are

* root 0: (133/3,50/3), (142/3,32/3), (47,8), (49,4);
* root 1: (133/3,50/3), (1289/27,266/27), (47,8), (49,4).

The certificate generator uses an isometric reflected coordinate frame. The verifier does not assume the stored picture or the generator's transformation: it identifies the corners from target side lengths and constructs the four triangles by the cosine rule from the word and endpoint angles. It checks their congruence, containment and pairwise disjoint interiors.

## 4. A necessary boundary-path test for a partial placement

The new pruning test retains positions of external tiles rather than only counts of edge lengths.

On an outer side of integral length L, all supported whole edges start at integral arclength positions 0,...,L, since every prior supported edge has integral length a,b or c. Enumerate every possible oriented supported tile starting at every such position. Retain it only if it is contained in the target and has an allowed angle at a target endpoint. The two possible orientations for each edge length are constructed directly by the cosine rule.

For a fixed valid partial placement, discard a boundary candidate if its interior overlaps an already placed distinct tile. An identical tile is retained: it may already be the supported tile of the final dissection. This gives a finite directed graph from side position 0 to L. An edge of that graph is a candidate supported tile.

Every full completion induces a graph path on each target side satisfying the following necessary rules:

1. Two consecutive supported tiles cannot both present gamma at their shared junction.
2. A c-edge with its starting endpoint blocked cannot be followed by a tile whose starting endpoint is gamma. If that c-edge ends at the target corner, it is forbidden as well. This is precisely the blocked-c lemma.
3. The path contains two consecutive c-edges.

A dynamic program records the current position, the previous tile's gamma endpoint flag, whether the previous edge is c and its start is blocked, and whether c,c has already occurred. The start and end conditions mark outer corners as blocked. The verifier independently reconstructs the complete candidate dictionary and tests these paths.

If any side has NO path, no completion is possible. Passing all three sides is not sufficient: nonconsecutive future boundary tiles or tiles on different sides may overlap, and the interior may still be impossible. Omitting those extra restrictions is safe on the negative side because this is a relaxation. No surviving boundary path is called a tiling.

The W dictionary has 650 oriented candidates over its three sides. The equilateral dictionary has 768. These are individual candidate tile positions, not complete tilings.

## 5. Why the remaining finite search is exhaustive

Take a valid partial placement and its actual unfilled polygonal region. At any residual sector with angle strictly between 0 and pi, a completion must place a tile VERTEX at that corner. A tile interior or the relative interior of its edge occupies respectively 2pi or pi and cannot fit there.

The tile adjacent to the outgoing residual boundary ray has a full side on that ray. There are exactly six ordered choices for its two incident side lengths. The law of cosines determines the third vertex in the left half-plane. Retain every choice which fits the sector, lies in the original target and has no interior overlap with any placed tile. Its outgoing side may overrun the displayed boundary atom when geometry permits: this expressly allows T-junctions.

At a branch node the certificate lists ALL retained choices. The independent verifier recomputes them and requires exact set equality. An empty set is a contradiction. At a boundary-path leaf it requires an actually empty side-path set as in Section 4. No other pruning is used in the FINAL three proof trees. In particular there are no chain-length-pruning leaves, component-area-pruning leaves, solver-status leaves, or timeout leaves.

The verifier obtains a residual sector without trusting the generator's boundary. At the announced corner it recomputes the local oriented boundary current of the target minus every placed triangle. It checks that the selected outgoing and incoming rays are consecutive, have the correct signs, and enclose a strictly convex unfilled sector. Since the known tiles are contained and interior-disjoint, this residual indicator is 0 or 1. The local signed rays therefore determine the correct unfilled sector. The generator instead maintains a global supporting-line sweep, a separate implementation.

The final certificates are TREES, not shared-state DAGs: every record is reached exactly once. The verifier rejects repeated records, cycles, missing branches, extra branches and unreachable rows. All accepted arithmetic is rational in x^2+D y^2, with D=2 for W and D=3 for equilateral. A nonrational required operation raises an error; it is never converted into a nonexistence conclusion. No direction cutoff or preselected interior vertex lattice is imposed.

Induction over each finite tree proves that its root partial placement has no completion. Both W roots have complete refutations; the equilateral tree starts from the empty placement and refutes every possibility.

## 6. Fresh complete replays

| Certificate | Root | Nodes | Empty-corner leaves | Boundary-path leaves |
|---|---|---:|---:|---:|
| W56proof0.json | first W root | 7680 | 3119 | 652 |
| W56proof1.json | second W root | 3372 | 825 | 312 |
| E56.json | empty equilateral target | 18548 | 6872 | 2776 |
| **Total** | all remaining cases | **29600** | **10816** | **3740** |

All 29,600 records were accepted by the separate verifier. The full negative forest has 14,556 terminal contradictions. C++ GMP was used for discovery, Python `fractions.Fraction` for replay. The replay checks mathematical rules, not a solver's confidence or an elapsed-time flag.

As controls, the prior constructor supplied actual W126, beta207, W224 and beta368 tilings. Their coordinates were converted to the diagonal rational metric by an explicitly derived isometry. The independent checker validated each tile, pairwise disjointness and exact positioned-boundary cancellation. Every prefix in both orders and additional random subsets passed the necessary boundary-path test: 1974 positive partial placements altogether. These are prior positive constructions, not new counts of this package. Deleting a proof branch, creating a cycle, inserting a moved triangle or replacing the root by an unjustified boundary leaf was rejected.

These tests are implementation controls. The geometric completeness and blocked-c lemmas remain written proofs, not machine-checked universal theorems.

## 7. Deductions: 56, the class 14, and the first exact W spectrum

Section 1 removes all 56 candidates except W and equilateral. Sections 2–6 refute both. Therefore

\[
\boxed{56\notin\mathcal S.}
\]

At 14 the sole W candidate has a length-15 side, shorter than two length-9 c-edges. The boundary lemma excludes it. Thus 14 is also impossible; this is an earlier elementary deduction, not the new computation.

The prior positive result [P] tiles (27m,28m,15m) by (6,5,9) at every m>=3. It has independent seeds at m=3 and m=4, and the prior +2 external collar supplies all subsequent odd and even scales. Combining this with the two exclusions gives

\[
\boxed{14m^2\in\mathcal S\iff m\ge3.}
\]

In particular the least realizable number in this square class is 126. The same argument also gives an exact fixed-tile spectrum:

\[
\boxed{(27m,28m,15m)\text{ tiles by }(6,5,9)\iff m\ge3.}
\]

The positive statements here are prior constructions; the new contribution completing these equivalences is the small negative count 56 with its two distinct geometric branches.

## 8. Limits of the completed work

This does NOT prove that every primitive W or beta tile has exact spectrum m>=v. The beta target (54,54,92) by (6,5,9), at m=2, remains unresolved by this package. The separate fixed W target for (u,v,m)=(1,3,2), with count 68, remains unresolved here too. Incomplete explorations are listed in `incomplete_searches.json`; none is a negative certificate. One plain equilateral-56 search timed out, but that case IS closed by the distinct completed boundary-assisted proof included here.

The F3 candidate 14430 is not decided. The reverse-apex manuscript is neither used nor validated. The theorem m>=v for general W/beta and the old square classes 15,22,78 are separate prior results. A finite remaining interval for EACH fixed tile is not a finite global exception set over all parameters.

## 9. Reproduction

Run, with Python 3 and its standard library only:

```
python reproduce.py
python check_controls.py
```

The first command recomputes the arithmetic gate and replays all three negative proof trees. The second rechecks the positive controls and corruption tests. No SAT/MILP solver, online access or C++ compiler is needed to check the supplied proofs.

For OPTIONAL regeneration with a C++17 compiler and GMP development library:

```
g++ -O3 -std=c++17 generate.cpp -lgmpxx -lgmp -o generate
BOUNDARY=1 W56ROOT=0 ./generate 2 3 2 W 120 0 W56proof0.json
BOUNDARY=1 W56ROOT=1 ./generate 2 3 2 W 120 0 W56proof1.json
BOUNDARY=1 ./generate 8 7 1 E120 120 0 E56.json
```

The last zero disables exploratory chain/area pruning. A shorter time allowance may produce INCOMPLETE on another machine; only an EXHAUSTED file that is subsequently accepted by the verifier is a refutation. The original complete certificates remain sufficient for replay regardless of discovery runtime.

## 10. Sources and dependency boundaries

Repository references are to the examined snapshot `3a0ad269f645850ed9fd01bbd76a08c9b456032e` of `DenisUkranian/erdos-634-tilings`.

**[U]** `research/uniform-reduction/PROOF.md`, especially Sections 1,3,4, and its companion `candidates.py`. The global exhaustion input is Laczkovich's angular classification reproduced in M. Beeson and Y. X. Zhang, *Rationality of certain triangle tilings*, arXiv:2604.01314, Table 1 and Theorem 1.2, with the separate classical/right/commensurable-angle restrictions identified in [U]. The double-angle and theta scale-one exclusions used here are the elementary lemmas recalled in Section 1 above. The program `check_gate.py` independently enumerates the resulting finite numerical lists; it does not formally verify the external classification.

https://github.com/DenisUkranian/erdos-634-tilings/blob/3a0ad269f645850ed9fd01bbd76a08c9b456032e/research/uniform-reduction/PROOF.md

**[B]** `research/w-global-oct7/ADJACENT_C_EDGES.md`: blocked-c lemma, consecutive longest edges and the two W56 boundary roots. This is a prior geometric input. The equilateral extension needed by this package is proved with its explicit angular hypotheses in Section 2 above.

https://github.com/DenisUkranian/erdos-634-tilings/blob/3a0ad269f645850ed9fd01bbd76a08c9b456032e/research/w-global-oct7/ADJACENT_C_EDGES.md

**[P]** `research/universal-closure-oct8/group1/PROOF.md` and `research/w-beta-caps/PROOF.md`: the known W126/W224 seeds and the +2 collar for (u,v)=(2,3). The scale-v triquadratic seed is credited there to Michael Beeson. A copy of the previous unrestricted constructor is supplied only to regenerate positive regression controls; its general theorem is not newly claimed here.

https://github.com/DenisUkranian/erdos-634-tilings/blob/3a0ad269f645850ed9fd01bbd76a08c9b456032e/research/universal-closure-oct8/group1/PROOF.md

No current arXiv acceptance, external referee approval, or first-priority claim is inferred from any file or checker report.
