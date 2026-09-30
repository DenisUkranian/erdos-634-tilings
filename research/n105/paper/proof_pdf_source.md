---
title: "No triangle can be dissected into 105 congruent triangles"
author: "Denis Paliy"
date: "30 September 2026 · Research with ChatGPT assistance"
lang: en
---

**Status.** This is a computer-assisted proof with explicit published classification/rationality dependencies, written geometric lemmas, and reproducible exact finite certificates. It has internal mathematical and computational checks, but no external referee acceptance, no proof-assistant formalization, and no claim of priority. It concerns the integer **105**, not a classification of all integers in Erdős problem 634. The separate all-primes manuscript is not an input.

A tiling is a finite dissection into congruent nondegenerate triangles with disjoint interiors. Reflections and arbitrary T-junctions are permitted.

## 1. The theorem and the dependency boundary

**Theorem.** There is no triangle tiled by exactly 105 congruent triangles.

The proof has two distinct parts. Sections 2–6 reduce an arbitrary hypothetical 105-tiling to exactly four fixed tile/target pairs. Section 7 excludes each pair. The reduction does not assume a bound on tile side lengths without proving it, and does not use the withdrawn packing argument or the global prime conclusion of [B4].

The external inputs are:

* Laczkovich's shape classification, reproduced with its source references in [BZ], Table 1; [B1], Theorem 3.1 for the non-equilateral isosceles specialization; and [B4], Theorems 4, 6, 7 and 9 for equilateral, commensurable-angle and reptiling cases. Only the classification and individual count restrictions are used, not their claims about all primes.
* Rationality of a nonsimilar non-right irrational-angle tile: [BZ], Theorems 1.1–1.2.
* The right-tile isosceles count restriction in [B1], Theorem 7.10.

For transparency, the squarefree exclusion in [B1], Theorem 11.7, is rederived in Section 4. The needed 120-degree count equations in [B4], Theorems 18–21, are rederived from primitive side ratios in Section 5. This separates those elementary inputs from unrelated withdrawn results.

Throughout the proof an external target side is a union of **whole** tile edges. A tile is contained in the convex target, so an edge supported by an exterior line lies entirely on the corresponding target side. Consequently all exterior lengths are integers after primitive integer normalization of the tile.

## 2. Exhaustive shape split

A similar-tile dissection is a reptiling. Its count is a square, a sum of two integer squares, or three times a square [B4, Theorem 7]. None can be 105. In particular, if 105=x²+y², reduction modulo 3 forces 3|x and 3|y, incorrectly giving 9|105.

In the remaining cases, classify the target and tile as follows.

1. A commensurable-angle scalene target can only be reptiled. Non-reptiling commensurable-angle cases are isosceles/right-tile or equilateral. The equilateral counts in this case are a square, twice a square, three times a square, or six times a square. The right-tile isosceles restriction gives, for odd N, only a square. Thus 105 is excluded in these cases.
2. For irrational tile angles, a right tile has an isosceles target (unless the tiling is similar); again the preceding restriction excludes 105.
3. Every remaining tile is rational by [BZ]. The exhaustive nonsimilar irrational-angle cases are:
   * an equilateral target, with a 60-degree or a 120-degree tile;
   * an isosceles target with base angle α and a tile (α,β,2α);
   * the five targets for 3α+2β=π: W=(2α,β,α+β), the other scalene target (2α,α,2β), and the isosceles targets with base angle α, β or α+β;
   * a 120-degree tile (α,β,120°), with an isosceles target of base angle α or one of the four scalene targets
     (α,2α,3β), (α,2β,2α+β), (α,α+β,α+2β), (2α,2β,α+β).

Angles and corresponding side labels may be interchanged as allowed by the classification. In the calculations below positive primitive parameters are enumerated in **both** orders where relevant.

This is the point at which the published exhaustive shape theorem is used. The following arithmetic is not asserted to prove that classification independently.

## 3. Equilateral targets: a finite factor-pair test without a tile-size cutoff

Let the rational tile have sides a,b,c opposite α,β,γ, with α/π irrational and γ=π/3 or 2π/3. Normalize a,b,c to primitive positive integers. Let S be the equilateral side. The area equation is

    S² = N a b.

Every tile edge direction lies in the group nα+jπ/3. Indeed, tiles sharing a segment of positive length form a connected adjacency graph: a generic path through the target avoids the finitely many tile vertices. Starting from an exterior edge and crossing shared segments transports directions by integer combinations of tile angles. This argument does not require edge-to-edge tilings. Irrationality makes n and j unique, with j taken modulo 6.

Define direction characters

    f(nα+jπ/3)=(-1)^j,       g(nα+jπ/3)=(-1)^(j+n).

For a counterclockwise polygon boundary take the sum of edge lengths times f, and analogously for g. Both change sign under edge reversal and are additive in edge subdivision. Hence all internal atomic subsegments cancel, including at T-junctions. Each congruent orientation contributes plus or minus the reference tile's value. In particular, the target value divided by the nonzero reference value is an integer of the parity of N.

For a 120-degree tile, c²=a²+ab+b². The two absolute tile values are

    X=c+a-b,        Y=c+b-a,        XY=3ab.

Both target values equal 3S. Thus positive integers s=3S/X and t=3S/Y satisfy

    st=3N,      (t-s)²+16N = [2S(a+b)/(ab)]².

The bracket is rational. A rational number with integral square is an integer. Therefore the left side is an integer square.

For N=105, after interchanging a,b, the complete factor pairs of 315 are

\Needspace{10\baselineskip}

| s | t | (t-s)²+1680 |
|---:|---:|---:|
| 1 | 315 | 100276 |
| 3 | 105 | 12084 |
| 5 | 63 | 5044 |
| 7 | 45 | 3124 |
| 9 | 35 | 2356 |
| 15 | 21 | 1716 |

None is a square. This excludes the entire irrational 120-degree equilateral branch, irrespective of how large the primitive tile might initially have been.

For a 60-degree tile, c²=a²-ab+b². The two absolute tile values are a+b-c and a+b+c. Set

    s=3S/(a+b+c),       t=3S/(a+b-c).

Then

    st=3N,      (t-s)²-4N = [2S(a-b)/(ab)]².

Also s²<N for a nonequilateral tile. To see this, a+b>2√(ab) and c>√(ab), so a+b+c>3√(ab). For N=105, s can only be 1,3,5,7,9. The corresponding radicands are

    98176, 9984, 2944, 1024, 256.

Only the last two are squares. If q²=(t-s)²-4N, then

    a:b = (s+t+q):(s+t-q).

Primitive normalization gives exactly

    (a,b,c;S) = (21,5,19;105), (15,7,13;105),

up to interchanging a and b. These are the two fixed equilateral cases in Section 7.

## 4. Two squarefree isosceles exclusions

### 4.1 The family γ=2α (a short reproduction of [B1], Theorem 11.7)

The target has angles α,α,α+β and the tile has α,β,2α, where 3α+β=π and α/π is irrational. Rationality and the sine law give primitive sides

    a=k²,       b=m²-k²,       c=km,
    gcd(k,m)=1,       k<m<2k.

The equal target sides and its base have primitive proportions k,k,m, so they are λk,λk,λm with λ a positive integer. Comparing areas gives N=λ²/b.

If N is squarefree, write b=N h² and λ=N h, with h a positive integer. A whole-edge decomposition of either equal side X=Nkh satisfies

    X=A k²+B b+C km.

Reduction modulo k shows k|B. If B>0, then

    B b ≥ k N h² ≥ Nkh = X.

Equality is the only possibility, and forces h=1 and the entire side to consist of b-edges. Such a pure-b side is impossible: each b-edge contributes a γ=2α endpoint; the target corners have no γ sectors; and a straight boundary angle π=3α+β admits at most one γ. There would be more γ endpoints than internal junctions.

Therefore neither equal side has a b-edge. The target apex α+β contains exactly one α and one β tile. Choose the equal side incident to its α tile. At the other end of this side is a target α corner. Every boundary a- or c-edge has a β endpoint, but neither endpoint of this side can contain β and a straight junction admits exactly one β. The same counting contradiction follows. Thus N is not squarefree, excluding 105.

### 4.2 The Group-1 theta-isosceles family

For 3α+2β=π, write the primitive rational tile as

    a=uv,       b=v²-u²,       c=v²,
    0<u<v,       gcd(u,v)=1.

Indeed a²=c(c-b), and reducing a/c=u/v gives these primitive proportions. Let Q=b+c and P=b+2c.

For the isosceles target with base angles θ=α+β and apex α, the primitive target proportions are v,v,u. Thus equal sides are λv and the base λu, with λ integral. Area comparison gives N=λ²/b.

If N is squarefree, again b=N h² and λ=N h. On an equal side X=Nvh, reduction modulo v makes its b-edge count B a multiple of v. If B>0, its b-edges alone have length at least vNh²≥X. Equality would make that side pure b.

Here γ=2α+β>π/2 and all three target angles are smaller than γ. Every target side must therefore contain a c-edge: otherwise each of its edges contributes a distinct internal γ junction, too many for the available junctions. A pure-b side is impossible, so both equal sides have no b-edge.

The apex α can contain only a single α tile. Its two incident sides are b and c; both lie on the two equal sides of the target. This contradicts absence of b. Hence this entire theta family has no squarefree count.

Neither squarefree argument invokes a short internal relation or a packing assumption.

## 5. The remaining rational arithmetic

### 5.1 Group 1

Keep the parameters u,v,b,c,Q,P from Section 4.2. The following primitive target side ratios and necessary count formulas follow from the sine law and area comparison:

| Target | Primitive side ratios | Necessary count |
|---|---|---|
| W | (v³,uQ,vb) | N=Q t², t∈Z>0 |
| beta-isosceles | (v³,v³,uP) | N=P t², t∈Z>0 |
| other scalene | (c²,cQ,bP) | N=QP t², t∈Z>0 |
| alpha-isosceles | (c,c,Q) | N=λ² Q/b, λ∈Z>0 |

The triples are primitive. For example, gcd(v³,vb)=v and gcd(v,uQ)=1 in W; gcd(v³,uP)=1 in beta; gcd(c,Q)=1 and gcd(c,bP)=1 in the other scalene case. In alpha, gcd(c,Q)=1. Integer target lengths therefore force integer scale, by Bezout's identity.

For alpha-isosceles we use **only** N=λ²Q/b and gcd(b,Q)=1. In particular Q|N and λ²=Nb/Q. We do not silently impose λ multiple of b when b is nonsquarefree.

For N=105, squarefreeness forces t=1 in the first three rows. In every row Q>v² and Q≤105 whenever a solution exists, so v≤10. Enumerating coprime 0<u<v≤10 yields no W, beta, or other-scalene candidate. For alpha, Q|105 leaves only (u,v,b,Q)=(1,2,3,7); then λ²=45, impossible. The finite bound has been derived, not selected experimentally.

The theta row was already excluded in Section 4.2. Thus the entire Group-1 family contributes no 105-tiling, without using the separate candidate scale-one obstructions.

### 5.2 The 120-degree families

Normalize the tile to pairwise coprime positive integers a,b,c with c²=a²+ab+b². Pairwise coprimality follows because a prime dividing two sides divides the third. Also 3 does not divide c: otherwise a≡b (mod 3), and substitution a=b+3r gives c²=3b²+9br+9r², which has 3-adic valuation 1 since 3∤b, contrary to being a square.

Useful consequences are gcd(c,a+2b)=gcd(c,2a+b)=1. For if a prime p divides c and a+2b, substitution gives p|3b²; p∤b, and p=3 is impossible. The other identity is symmetric.

The sine law gives the following primitive target triples. Their primitiveness follows from pairwise coprimality and the preceding 3-adic argument. Hence λ below is a positive integer.

| Target angles | Primitive target sides | Area equation |
|---|---|---|
| isosceles, base α | (c,c,a+2b) | N=λ²(a+2b)/b |
| (α,2α,3β) | (c²,c(a+2b),3b(a+b)) | N=3λ²(a+2b)(a+b) |
| (α,2β,2α+β) | (ac,b(2a+b),c(a+b)) | N=λ²(2a+b)(a+b) |
| F1=(α,α+β,α+2β) | (a,c,a+b) | N=λ²(a+b)/b |
| (2α,2β,α+β) | (a(a+2b),b(2a+b),c²) | N=λ²(a+2b)(2a+b) |

These are also the individual equations in [B4, Theorems 18–21] and [B1, Section 12], but their derivation here uses no prime classification.

For isosceles targets, d=a+2b divides 105 and λ²=105b/d. Loop over the eight divisors d of 105 and 1≤b<d/2, setting a=d-2b; the norm equation and square condition leave no candidate.

For the three product rows, squarefreeness forces λ=1. Put x=a+b,y=a+2b in the first product row (xy=35); x=a+b,y=2a+b in the second (xy=105); and x=a+2b,y=2a+b in the last (xy=105). The first two require x<y<2x; the last requires x/2<y<2x with the associated integral positive a,b. Factor pairs give no norm solution. The only positive coprime parameter trial for the first row is (a,b)=(3,2), with c²=19; the other two rows have no positive parameter trial satisfying their factor inequalities.

For F1, d=a+b divides 105 and

    λ² = 105 b/d.

For each divisor d, take 1≤b<d and a=d-b. Test coprimality, the norm square, and this scale square. There are exactly two ordered solutions:

    (a,b,c,λ)=(8,7,13,7), (16,5,19,5).

They give exactly the targets

    tile (7,8,13), target (56,91,105);
    tile (5,16,19), target (80,95,105).

No assumption that b is squarefree or that the scale must equal b was used. Other orderings were included in the divisor test.

The exact lists in this section are reproduced by `check_arithmetic.py`.

## 6. A convex-capped whole-chain lemma used in the new certificate

Let a residual region be the target minus a specified set of actual, nonoverlapping whole tiles. Consider a straight residual boundary segment AB such that:

1. all its interior boundary vertices have straight angle and a single incoming and outgoing boundary edge;
2. at both endpoints the residual region has angle strictly less than π and a single incoming and outgoing boundary edge.

The segment is followed along the residual boundary; it is not an invented cut or an artificially extended tile edge.

**Lemma.** In every completion, AB is tiled on its residual side by a complete chain of whole tile edges. In particular, for integer tile side lengths a,b,c,

    |AB| ∈ {ia+jb+kc: i,j,k are nonnegative integers}.

If the first actual edge at A has length ell, then |AB|-ell belongs to the same semigroup; analogously at B.

**Proof.** At a relative interior point of AB the exterior side is occupied or outside the target. Any completing tile meeting a positive-length interval must therefore support AB with an edge, not cross the line. If one opposite edge ends strictly inside an existing supporting edge, the remaining straight sector forces the chain to continue; T-junctions are allowed.

At A or B a completing edge cannot extend through the endpoint: a point in the relative interior of a triangle edge has a straight local sector of angle π, which cannot fit the residual angle less than π. Thus no edge at either end is partially truncated. Finiteness of the tiling gives the complete whole-edge chain. Removing its first edge gives the second assertion. $\square$

The implementation does not apply this lemma at a reflex endpoint, at an endpoint with straight angle π, or at a branch point of the residual boundary. It traverses all intervening collinear atomic edges. In the fixed convex target every segment is at most its diameter 105, so its whole-edge semigroup only needs to be tabulated up to 105.

Additional safe propagation: if every admissible fan at a convex corner contains a particular actual tile, that tile is forced even if several fans remain. Two fan choices cannot coexist if their tiles overlap or jointly violate the correctly supported exterior-boundary lemma. Arc and binary-implication deductions remain necessary conditions only; satisfiability of these relaxations is never asserted to construct a tiling.

## 7. Exact refutation of the four fixed targets

The earlier three fixed-instance proofs are retained, with their written geometric premises in `BASELINE_LEMMAS.md`:

* (7,8,13) on (56,91,105): every one of the 120 boundary roots is refuted.
* (5,19,21) on the equilateral side-105 target: a four-tile hand obstruction in Sections 3–4 of the baseline note; also a separate 15-root exact certificate.
* (7,13,15) on that equilateral target: the full disjunction of 28 two-long-edge roots and 1760 three-long-edge roots is refuted. Pure-long rows are excluded by the shortest-edge lemma, not discarded without proof.

The new result closes the fourth target, (5,16,19) on (80,95,105).

The external short side satisfies

    5A+16B+19C=80,     C≥2.

Its only nonnegative solution is A=B=C=2. Generate all 90 orders of the multiset (5,5,16,16,19,19), with both inward placements for each edge. Exact containment and disjointness give 840 raw side configurations. The supported-boundary adjacency lemma leaves exactly 120, independently regenerated by the checker.

Each of these 120 configurations is refuted by a complete certificate. A fresh search was performed from the initial configurations, without importing any old checkpoint, and supplied the final certificate `data/f1_5_16_19.json`. It uses 22,552 stored proof states, 826 rational points, 855 distinct tile placements and at most 59 placed tiles in any state. The replay may legitimately stop earlier than some stored subtrees when its independent necessary tests already yield a contradiction; the exact number actually entered is recorded in its report.

The separate checker does not import the search engine. It uses homogeneous exact polygon clipping rather than the search engine's separating-axis predicate; it enumerates whole fans geometrically rather than using the search engine's angle-quota recursion. It checks congruence, containment, disjointness, root coverage, supported boundary marks, atomic residual edges, the convex-capped chain restriction, forced tiles, complete branching, and terminal contradictions. All coordinate and geometric comparisons are exact. Newly constructed points are not restricted to a fixed-denominator grid.

No INCOMPLETE root is counted as refuted. Search time limits only cause INCOMPLETE, never a rejection. The old false rule marking an interior tile merely touching the exterior at its obtuse vertex is not used.

Positive regression witnesses for the new chain rule consist of 32 congruent tiles in two half-shifted parallelograms. They have eight vertices in strict interiors of other edges. Testing 258 subsets of this known tiling checks 3418 capped endpoint rays and the true incident completing edges. Both chain implementations preserve every known completion. These tests exercise the T-junction and reflex-endpoint issue; they do not replace the written proof.

All four cases from the exhaustive reduction are now excluded. This proves the theorem, subject to the stated published inputs and written/computer-assisted proof boundary. $\square$

## 8. Scope, reproducibility and priority

Run `python verify_all.py --jobs 2`. This replays all four certificates, checks exact arithmetic and the regression suite, and writes a combined verification report. The report explicitly keeps `full_Erdos634_solved` false. The global-105 result uses both the written reduction and the fixed certificates; no program here formally proves the classification theorems or the human geometric lemmas.

The older reports 64/120 and 94/120 for the last tile were different retained subsets, not a classification. A replay in this continuation restored the older 94, after which the new argument supplied all missing roots. The final fresh 120-root certificate avoids relying on that bookkeeping history.

This work makes no research-priority claim. Similar conclusions may have been reported elsewhere; checking this proof does not adjudicate priority. The full problem still asks for a necessary and sufficient criterion for every positive integer N. The theorem above settles the single global count 105 and adds reusable geometric restrictions; it does not answer that infinite classification problem.

## References (only the specified inputs are used)

[BZ] M. Beeson and Y. X Zhang, *Rationality of certain triangle tilings*, arXiv:2604.01314v1 (1 April 2026), Table 1 and Theorems 1.1–1.2. https://arxiv.org/abs/2604.01314v1

[B1] M. Beeson, *Tilings of an Isosceles Triangle*, arXiv:1206.1974v7 (4 May 2026), Theorem 3.1, Theorem 7.10, Theorem 11.7 and Section 12. https://arxiv.org/abs/1206.1974v7

[B4] M. Beeson, *Tiling a triangle into a prime number of congruent triangles*, arXiv:2607.23453v1 (26 July 2026). The shape/reptiling statements and individual elementary equations are used; the main all-primes conclusion and its Group-1 nonexistence dependencies are **not** used. https://arxiv.org/abs/2607.23453v1

[B2] M. Beeson, *Tiling an Equilateral Triangle*, arXiv:1812.07014v3 (28 May 2024), for the equilateral setting and coloring/area context. Section 3 above gives its own subdivision-compatible two-character reduction. https://arxiv.org/abs/1812.07014v3

The Laczkovich and Snover–Waiveris–Williams classification/reptiling sources are identified in the cited theorem statements. Problem definition: https://www.erdosproblems.com/634
