# Sharp positive-chain thresholds and the length budget in the scale-one induction

**Erdős 634 research project — Denis Paliy, with ChatGPT assistance**  
**29 September 2026**

## Status and scope

This is a focused mathematical audit of the positive whole-edge relations used in the scale-one candidate. It supplies a complete elementary proof of the arithmetic parameterization and its sharp thresholds. These thresholds clarify an argument already present in the candidate; no claim of novelty is made.

The geometric dependency ledger below records where the candidate establishes the hypotheses needed to use those thresholds. The finite computation checks arithmetic only. It does not enumerate tilings, certify the geometric induction, establish independent human review, or settle the full classification requested in Erdős problem 634.

No private correspondence is reproduced in this note.

## 1. Complete parameterization of positive c-relations

Let

\[
0<u<v,\qquad \gcd(u,v)=1,\qquad
 a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad d=v-u.
\]

**Proposition.** For a nonnegative integer \(n\), all nonnegative integer solutions of

\[
nc=Aa+Bb+Cc
\tag{1}
\]

are exactly

\[
\boxed{A=vh-d\ell,\qquad B=v\ell,\qquad C=n-uh-d\ell,}
\tag{2}
\]

where \(\ell,h\) are nonnegative integers satisfying

\[
vh\ge d\ell,\qquad uh+d\ell\le n.
\tag{3}
\]

**Proof.** Reduction of (1) modulo \(v\) gives \(B\equiv0\pmod v\), so write \(B=v\ell\). Dividing (1) by \(v\), then reducing modulo \(v\), gives \(A\equiv u\ell\pmod v\). Thus \(A=u\ell+vk\) for some integer \(k\). Substituting and writing \(h=k+\ell\) gives (2). Since \(A\ge0\) and \(d\ell\ge0\), necessarily \(h\ge0\). The remaining nonnegativity conditions are exactly (3). Conversely, substitution of (2) into (1) verifies the equality, so the parameterization is both necessary and sufficient. ∎

### Sharp consequences

If \(B>0\), then \(\ell\ge1\), and \(A\ge0\) forces \(h\ge1\). Consequently

\[
n=C+uh+d\ell\ge u+d=v.
\]

Hence, for \(0\le n<v\), all solutions have the more specific form

\[
\boxed{(A,B,C)=(vh,0,n-uh),\quad
0\le h\le\lfloor n/u\rfloor.}
\tag{4}
\]

In particular:

* For \(n<u\), the only solution is \((0,0,n)\): the opposite chain is purely c.
* For \(n<v\), no b-edge can occur, but a-edges may occur.
* At \(n=u\), the two solutions are \((0,0,u)\) and \((v,0,0)\), because \(uc=va\). The first threshold is sharp.
* At \(n=v\), the unique solution with \(B>0\) is \((u,v,0)\), because \(vc=ua+vb\). The second threshold is sharp. Uniqueness follows because equality in \(n\ge u+d\) requires \(\ell=h=1\) and \(C=0\).

The distinction between a purely-c chain and a chain without b is essential. They are not interchangeable conclusions.

**Example.** For \((u,v)=(2,5)\), the tile has sides \((10,21,25)\). Already \(2\cdot25=5\cdot10\), so a two-c chain need not have only c opposite it. However, no b can occur opposite an n-c chain with \(n<5\). The first positive relation involving b is \(5\cdot25=2\cdot10+5\cdot21\).

## 2. The other two short-chain lemmas and their exact endpoints

For \(0<i<v\),

\[
ib=Aa+Bb+Cc\quad\Longrightarrow\quad(A,B,C)=(0,i,0).
\tag{5}
\]

Indeed, reduction modulo \(v\) gives \(B\equiv i\pmod v\), while positivity gives \(0\le B\le i<v\). Thus \(B=i\), and the remaining terms vanish. This range cannot be enlarged to include \(i=v\), since

\[
vb=(v-u)(a+c).
\tag{6}
\]

Similarly, for \(0<i<v\),

\[
ia=Aa+Bb+Cc\quad\Longrightarrow\quad(A,B,C)=(i,0,0).
\tag{7}
\]

To prove this, write \(B=v\ell\) after reduction modulo \(v\), and put \(r=i-A\ge0\). The equation becomes

\[
ru=\ell(v^2-u^2)+Cv.
\]

Reduction modulo \(u\) gives \(\ell v+C=uT\) for an integer \(T\ge0\), and substitution gives

\[
r=vT-u\ell.
\]

If either \(\ell>0\) or \(C>0\), then \(uT=\ell v+C>\ell u\), so \(T\ge\ell+1\) and \(r\ge v+(v-u)\ell\ge v\), contradicting \(r\le i<v\). Therefore \(B=C=0\) and \(A=i\). Again the range is sharp, because \(va=uc\).

## 3. Geometric applicability: the hypothesis is a whole component

The arithmetic applies to a segment only after both sides of that segment have been shown to be complete chains of **whole** tile edges. A finite initial run on one side is not sufficient: an opposite edge might cross its endpoint and continue beyond it.

For a maximal connected collinear component of actual tile boundaries in a finite tiling, an endpoint cannot lie in the relative interior of one of its constituent edges; otherwise that edge extends the component. In the candidate, shorter non-maximal segments instead require explicit endpoint barriers: an external supporting line, a tile crossing the continuation, or a known start of an actual edge. The presence of T-junctions alone does not justify truncating the opposite chain.

## 4. Length-budget ledger for the W induction

The candidate's appendix treats the scale-one W target. Its external side OC has exactly u b-edges and u c-edges and no a-edge. Its column statement is established in this order:

1. Using the separate first-strip argument for column 1, and the previously completed smaller columns for later columns, force the whole left side of the **actual maximal** column to consist of normal c-edges.
2. If the completed column has height n, its rectangular completion supplies n consecutive c-edges on OC.
3. At the boundary point nq, the known tile angles force one additional c-edge on OC. Therefore n+1 <= u, i.e. n < u.
4. Only now apply (4), concluding that the opposite chain is purely c and, in particular, has no right a-edge.

The point to scrutinize geometrically is the implication from actual continuation to rectangular completion, including its use of strictly smaller columns. One must not use the no-right-a property of the column currently being proved in order to establish its own height bound.

As written, the candidate uses the already proved property for smaller indices and obtains the current column's no-right-a property at the end. The arithmetic range n<u is explicit rather than assumed.

## 5. Length-budget ledger for the reverse-apex beta induction

The beta-isosceles target is placed above its horizontal base. Column m, for 1 <= m <= v-1, starts at the blocked upper endpoint V_m=Z(m,v-m). The candidate uses the following order:

1. The actual opposite tile crossing V_m blocks upward continuation.
2. Force each actual downward continuation to add one complete normal c-edge. Horizontal chains have length ma with m<v; the smaller columns, not the present column, supply the required no-opposite-b statements for interior gaps.
3. Boundedness and maximality make the lower endpoint Z(m,r) with integer r>=0. The last inequality follows from containment above the base.
4. The complete component therefore has length nc, where

\[
0<n=(v-m)-r\le v-m<v.
\]

5. Apply (4) to the complete component: the opposite chain contains **no b-edge**. It need not be purely c.
6. Use that newly obtained no-b property to force the next diagonal tile.

At the final diagonal step, the candidate reaches index v without invoking short-b purity at index v. This matters because (6) shows precisely why the endpoint v is outside the valid range.

The distinction between n<u and n<v is not an incidental weakening: it is what permits the beta induction to allow valid a/c compensation without allowing b.

## 6. What the audit establishes

The arithmetic parameterization and all sharp cutoffs above have complete proofs. The candidate has an explicit proposed geometric mechanism for maintaining those cutoffs; this focused reading did not identify an application outside the stated numerical ranges.

That is narrower than a complete correctness certificate for the geometry. A full review still has to check every forced placement, the completeness of both edge chains, and the earlier-column implications, and then check all external classification dependencies in the prime deduction. This note does not replace those tasks and does not determine the remaining composite counts in problem 634.

## 7. Reproducible finite regression

Run:

```bash
python check_relations.py --max-v 40 --output check_results.json
```

The saved run exhaustively checked every primitive pair 0<u<v<=40 (489 pairs). It compared two enumerations of every nonnegative c-relation for 0<=n<=2v: a direct modular enumeration of A,B,C, and the parameterization (2). It also checked all short-a and short-b lengths and the three sharpness identities. The numerical results are in `check_results.json`.

The direct enumerator does not assume B is a multiple of v or assume either cutoff. It solves the congruence modulo c separately for each nonnegative A. All computations use exact integers. Passing this regression is a check of implementation and arithmetic consistency, not a proof of a geometric nonexistence statement.

## Sources and attribution

* Project candidate: `docs/prime-case-candidate.md`, including "Downward column completion" and Appendix sections 2–6, in https://github.com/DenisUkranian/erdos-634-tilings .
* Existing internal audit: `docs/audits/reverse-apex.md` in that repository. Its audit status is not treated as external refereeing.
* Michael Beeson, *Triangle Tiling: The case 3α+2β=π*, arXiv:1206.2229v4, revised 25 September 2026. Its abstract and revision comments explicitly retain the prime question for the W and beta-isosceles shapes. https://arxiv.org/abs/1206.2229v4 .

The short-chain lemmas themselves are already present in the project candidate. The present document isolates their full parameterization, their exact failure thresholds, and the separation between arithmetic and geometric verification.
