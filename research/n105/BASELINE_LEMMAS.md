# Baseline lemmas (preserved source, superseded status)

> **Historical baseline.** This note records the three-fixed-target stage and its original partial fourth target. Its geometric lemmas are inputs to [PROOF_N105.md](PROOF_N105.md), which now excludes all four targets. Counts such as 64/120 below are historical, not the current coverage.

This is the earlier fixed-instance proof note. Its final partial status for (5,16,19) is superseded by PROOF_N105.md and the new complete certificate. Sections 1–6 provide the geometric dependencies and baseline root coverage.

# Three fixed 105-tile instances: geometric lemmas and exact refutations

**Denis Paliy — 30 September 2026. Research conducted with ChatGPT assistance.**

This note excludes the three fixed tile/target pairs listed below. It does not classify all triangle-tiling counts, does not claim that 105 is globally impossible, and does not settle Erdős problem 634. The arguments and computational replays are internal to this project, not external refereeing or proof-assistant verification. No priority claim is made.

| Tile sides (sorted) | Target sides | Status in this package |
|---|---|---|
| (7,8,13) | (56,91,105) | Complete fixed-target computer-assisted exclusion |
| (5,19,21) | (105,105,105) | Complete fixed-target hand proof; separate finite refutation also supplied |
| (7,13,15) | (105,105,105) | Complete fixed-target computer-assisted exclusion |
| (5,16,19) | (80,95,105) | Partial: only explicitly certified boundary roots are excluded |

Throughout, tilings are finite, interiors are disjoint, reflections are allowed, and arbitrary T-junctions are allowed. An external side of a tile on a straight target side is a whole tile edge. A tile merely touching the target boundary at one vertex is not thereby a boundary-supported tile.

## 1. The boundary lemma, with its essential support hypothesis

First consider a primitive integer 120-degree tile with sides a>b>1 and c²=a²+ab+b². Let the opposite angles be ε,δ,Γ. Thus Γ=2π/3, ε+δ=π/3 and δ<ε. The F1 target has angles ε, ε+δ, ε+2δ. Every one is less than Γ.

Fix an external target side. Mark an internal junction only if a tile having a **whole edge on this very target side** has its Γ angle there. Do not mark a point merely because an interior tile touches it with a Γ vertex. A c-edge endpoint is called blocked if it is marked or is a target corner.

**Local lemma.** A boundary c-edge cannot have both endpoints blocked.

To prove this, write its tile as PQR with PQ=c, PR=a, QR=b and angles δ,ε,Γ at P,Q,R respectively. At a marked Q, the sector directly across QR between this tile and the boundary-supported marking tile is δ. At a target corner Q the sector is 0, δ or 2δ. Irrationality of δ/π implies that kδ, k=1,2, can only be filled by k δ angles. The first opposite tile therefore has an a- or c-edge along QR, both longer than b. That edge overruns R and supplies a straight sector π there. If the remaining sector at Q is zero, R is instead on the external boundary. Either way a further Γ angle at R is impossible.

A Γ angle directly across PR at P is also impossible: at a marked P the intervening sector is ε, and at a target corner the whole available angle is smaller than Γ. The edge PR is internal, since a target corner cannot equal δ.

The opposite side of PR is a complete chain of whole tile edges. At P an overrun leaves the target. At R it leaves the target or enters the already placed crossing tile. At internal T-junctions the straight edge PR forces collinear continuation. Thus no partial edge has been silently truncated. This chain has total length a. A c-edge is too long; an a-edge would occupy the entire chain and put Γ at P or R; so only b-edges remain. This gives a=jb, contradicting coprimality and b>1.

A side with m whole edges, k of them c-edges, has exactly m-k marked junctions from its non-c boundary tiles: their Γ endpoints are distinct and not at target corners. There are m-1 internal junctions, hence k-1 unmarked ones. Every c-edge needs an unmarked internal endpoint by the local lemma. Pigeonhole therefore gives two adjacent c-edges.

**Boundary-adjacency conclusion:** every target side contains a consecutive pair of longest edges. When k=2, their shared point is the only unmarked junction. All non-c boundary edges on either side of the pair have their Γ endpoint pointing toward the pair.

The same proof applies to an equilateral target tiled by a triangle with angles

    δ, ε=π/3, Γ=2π/3−δ,   0<δ<π/6,

and integer opposite sides s<m<ℓ, where gcd(s,m)=1 and s>1. Replace (a,b,c) above by (m,s,ℓ). At an ε endpoint of a longest boundary edge the residual sector is δ at a marked junction, or zero at a target corner. Also Γ>π/2, so the same angular barriers apply.

In this general equilateral setting, 2cosδ=(m²+ℓ²−s²)/(mℓ) is rational and strictly between √3 and 2, so δ/π is irrational by the rational-algebraic-integer argument. For our two equilateral tiles, 2cosδ equals 37/19 and 23/13, respectively. Each is a noninteger rational number; rationality of δ/π would make it a rational algebraic integer, an impossibility. For the two F1 tiles the corresponding rational cosine argument applies as well. The geometric results below do not assume edge-to-edge tilings.

## 2. A shortest-edge lemma: pure-long boundary rows cannot be omitted

For the preceding equilateral setting, a nonnegative inventory xδ+yε+zΓ equals ε exactly when

    x=z,  y+2z=1.

Consequently each target corner contains exactly one ε tile. For an inventory equal to π=3ε, the equations are

    x=z,  y+2z=3.

The only possibilities are three ε angles, or one each of δ,ε,Γ. In particular, a straight boundary junction can contain **at most one δ**. No target corner contains δ.

Each boundary edge of length m or ℓ contributes a δ endpoint. If an external side had no s-edge, its n boundary edges would need n distinct internal δ junctions, but only n−1 exist. Therefore every target side has at least one shortest edge.

This excludes the otherwise arithmetically possible pure-long rows 105=5·21 and 105=7·15. They are not discarded by an unstated enumeration cutoff.

## 3. Cyclic corner pairs

**Lemma.** Suppose every side of an equilateral target of side S has exactly two longest edges, and S>2ℓ. Then the longest-edge pair on each side is incident to a target corner, and the three corner assignments are cyclic, in one of two mirror orientations. The orientations of the two tiles supporting each pair are forced.

Each target corner contains one ε tile, whose incident sides have lengths s and ℓ. Thus exactly one of the two external edges at that corner is long. This gives three corner-long incidences. A target side with only two adjacent ℓ-edges cannot have long edges at both ends when S>2ℓ. Hence each side receives at most one incidence, so each receives exactly one. The assignments are the two orientations of a three-cycle. A global reflection makes all three agree with counterclockwise traversal of the target.

At the corner the first long-edge tile has angle ε, and at the other end it has angle δ. If the second long-edge tile also presented δ at their junction, the remaining half-plane would need an inventory satisfying

    (2+x−z)δ + (y+2z)ε = 3ε.

Irrationality gives z=x+2≥2 and y+2z=3, impossible. The second tile therefore presents ε at that junction and has the same orientation as the first.

If a target side has counts A of s, B of m, and two of ℓ, the non-long orientations are also forced by Section 1. The final boundary edge at the next ε corner must be s, not m. Up to the global normalization, the side therefore has the word

    ℓ, ℓ, [A copies of s and B copies of m, with final entry s].

There are binomial(A+B−1,B) such words. The two long pairs on the other sides are fixed, and the full side word fixes the remaining boundary-supported tiles on the selected side.

## 4. A four-tile hand obstruction

The cyclic lemma yields a short geometric obstruction without an exhaustive search.

**Theorem.** In the equilateral setting of Sections 1–3, suppose:

1. each target side has exactly two longest edges;
2. S>2ℓ+s;
3. the only nonnegative whole-edge decomposition of 2m is 2m itself: if 2m=As+Bm+Cℓ, then A=C=0 and B=2.

Then no tiling exists.

**Proof.** Use oblique vectors p,q of lengths ℓ,s with angle π/3. Normalize a cyclic corner to O=0, its adjacent long pair to the segment 0,p,2p, and its other side to the positive q-ray. Its first two boundary tiles are

    D00 = conv(0,p,q),       D10 = conv(p,2p,p+q).

At p these contribute δ+ε, leaving Γ. A sector Γ admits only one Γ tile: the angle-inventory equations x−z=−1 and y+2z=2 imply (x,y,z)=(0,0,1). Its two incident lengths are s,m, so it has just two possible placements.

One placement is the standard tile U00=conv(p,q,p+q). Suppose the other placement were used. Its m-edge would run from p toward p+q, beyond p+q because m>s. At R=p+q this crossing tile supplies π, while D10 supplies Γ, so another Γ cannot occur there. At Q=2p the end of the long pair is marked by the next non-long boundary tile (Section 1). The sector directly across RQ, between D10 and that marking tile, is ε, so no Γ can occur there either. The opposite chain along RQ is complete: Q is external and an extension beyond R enters the crossing tile. Its length m cannot contain ℓ>m, or one m-edge, since the latter would place Γ at R or Q. It must consist of s-edges, contrary to gcd(s,m)=1 and s>1. Thus U00 is forced.

At q the existing angles of D00 and U00 are Γ+δ=2π/3, leaving the unique ε tile. Its external edge is s or ℓ. The two external ℓ-edges on this other side already occupy the opposite-corner interval [S−2ℓ,S]. Because s<S−2ℓ, an ℓ-edge starting at distance s from O is impossible. Hence the ε tile is

    D01 = conv(q,p+q,2q).

These four actual whole tiles fill K2=conv(0,2p,2q). Its front from 2p to 2q is an internal chord, consisting of two whole m-edges. Both endpoints are strictly inside the external sides, since 2ℓ<S and 2s<S. The opposite side of this chord is a complete chain of whole edges; exterior supporting lines prevent overruns, and T-junctions do not truncate it.

By hypothesis 3 the opposite chain is exactly two m-edges. In particular its first tile has an m-edge starting at Q=2p. But D10 contributes δ at Q and the next external boundary tile contributes Γ, leaving only ε directly across the chord. This sector admits exactly one ε tile, and an ε tile has incident sides s and ℓ, not m. Contradiction. ∎

This proof does not apply a short-chain relation beyond its valid length. The only two complete chains invoked have lengths m and 2m, with explicitly justified endpoint barriers.

### Application to (5,19,21), S=105

The equation 5A+19B+21C=105 with C≥2 has exactly two rows:

    (A,B,C)=(5,2,2), (0,0,5).

Section 2 excludes the second row. Thus every side has exactly two 21-edges. Also 105>2·21+5. Finally, 38=5A+19B+21C has only (A,B,C)=(0,2,0). For C=1, reduction modulo 5 would require B≥3, already too long; for C=0 it forces B=2. The theorem therefore excludes the entire equilateral target by a hand argument.

### Application to the two-long-edge subcase of (7,13,15)

Here 105>2·15+7, and 26=7A+13B+15C has only (0,2,0). Thus the same hand proof excludes the subcase in which all three sides have two 15-edges. A side with three 15-edges is a different subcase and is not excluded by this theorem.

## 5. Exhaustive finite reductions for the supplied certificates

### F1 (7,8,13) on (56,91,105)

The side 56 has exactly two edges of each length once longest-edge adjacency is imposed. All 90 orders of the multiset (7,7,8,8,13,13), and both inward orientations for each edge, are generated. Exact containment and pairwise nonoverlap leave 840 raw side states. The corrected boundary lemma leaves 120. Their whole edge-word coverage is independently regenerated by the checker, not inferred from a supplied root count.

The earlier 119-root package was replayed successfully in this continuation. The former last root 834, with side word 13,13,7,7,8,8, is now refuted in a standalone 105-state certificate, with at most 17 placed tiles. At its largest target corner, the existing δ tile leaves ε+δ=60°. This inventory is exactly one ε and one δ; the two orders and two orientations for each tile give eight possible initial fans. The supplied small certificate covers all eight.

A further fresh search, without importing the old checkpoint, produced the complete 120-root certificate supplied here: 9,949 reachable proof states, maximum 27 placed tiles. The standalone last-root proof is an additional small review aid, not a substitute for the complete 120-root proof.

### Equilateral (5,19,21)

The hand proof above is sufficient. As a separate check, the cyclic normalization gives 15 roots: 21,21 followed by five 5-edges and two 19-edges, ending in 5. All 15 roots are independently refuted in 1,585 proof states, maximum 53 placed tiles. This finite proof is redundant with the hand argument.

### Equilateral (7,13,15)

The complete arithmetic list for C≥2 is

    (A,B,C)=(7,2,2), (3,3,3), (0,0,7).

The pure-long row is excluded by Section 2. If all three sides have the first row, Section 3 gives 28 normalized roots, also excluded by the hand theorem. Otherwise rotate a side with the second row to the base. Generate every order of three 7-edges, three 13-edges and three 15-edges, both inward orientations, and retain exact containment, nonoverlap, the unique ε tile at each target corner, and the boundary lemma. This gives 1,760 roots. There is no assertion that the other sides must have the same row.

The complete disjunction therefore consists of 28+1,760=1,788 roots. Every root is refuted in the supplied 8,051-state certificate, maximum 60 placed tiles. The independent checker regenerates both subcases and their root identities.

### F1 (5,16,19) on (80,95,105)

The side 80 again has exactly two of each edge length. Its full 840-to-120 root reduction is independently reconstructed. The present certificate proves only 64 of the 120 roots impossible; 56 remain INCOMPLETE. Nothing in this note excludes the entire fixed target or produces a tiling of it.

## 6. What the exact replay checks

Coordinates use the basis (1,0),(1/2,√3/2). The norm is x²+xy+y². Every coordinate is rational, every comparison is exact, and there is no fixed-denominator grid restriction on newly generated vertices. Time limits affect search only; they never produce a mathematical rejection.

The checkers validate congruence, target containment, and disjoint positive-area interiors for every visited state. Residual edges are subdivided at all known vertices, including T-junctions, before internal atomic edges cancel. At an unfilled convex corner of angle less than π, any completion is a fan of whole tile angles, so the checker generates every such fan. A tile cannot pass straight through that convex corner because its π sector would not fit.

Arc consistency deletes a fan only if it lacks a compatible partner at another corner. Binary implication tests exclude a choice only when it implies its opposite, and reject a binary subproblem only when both choices lead to such contradictions. These are necessary conditions, not assertions of global sufficiency. Singleton fan domains force their actual tiles. A branch must cover every surviving fan at the chosen corner; its child must contain precisely the parent tiles plus that fan. Each nonterminal step increases the number of placed tiles.

A simple residual component bounded entirely by actual tile edges must have an integral multiple of the tile area. This test is applied only when the residual boundary consists of ordinary disjoint simple positively oriented cycles, with no negatively oriented hole. No artificial cut is treated as a tile boundary.

The search uses integer separating-axis predicates and angle-quota recursion. The independent replay does not import the search engine: it uses exact homogeneous polygon clipping and a separately written geometric fan enumeration. Both implementations belong to this project. The geometric lemmas and their root-normalization hypotheses remain human-written proof dependencies.

An old exploratory 240-state 'full' certificate based on incorrectly marking interior touching vertices is not used. The regression suite checks that a tile touching a side only at its Γ vertex does not mark it, using the explicit nonoverlapping patch described in the earlier corrected note.

## 7. Verification boundary and wider problem

These fixed-instance proofs do not rely on an external shape-classification theorem: the tile and target are specified. Passing from them to a statement about **all** 105-tilings would additionally require a complete audited reduction of every possible tile and target shape, and the remaining F1 instance is not excluded here. Passing to all positive integers N requires still more. The separate prime-case manuscript sent to Michael Beeson is not certified by these finite computations and remains a separate proof candidate.

The definition of the full problem is given at https://www.erdosproblems.com/634. Source context includes Michael Beeson, *Tiling an Equilateral Triangle*, arXiv:1812.07014v3, and Yan X Zhang, *Tiling Triangles with 2π/3 Angles*, arXiv:2512.22696v4. Their broader conjectures or withdrawn claims are not used as premises of these fixed-target proofs.

To reproduce the packaged finite claims, run `python verify_all.py`. This checks the actual files, their declared scopes and the independently rebuilt root coverage. An `INCOMPLETE` root remains unresolved regardless of how many of its internal exploratory branches were checked.
