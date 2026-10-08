# W/beta: what is already proved in the candidate and what remains

8 October 2026. Independent reading during the final-closure attempt.
This note records a mathematical dependency check, not a new theorem of
research priority and not external refereeing. It does not solve all of
Erdos 634.

## The both-c-on-equal-sides case is already addressed

Write

\[
a=uv,\quad b=v^2-u^2,\quad c=v^2,\qquad
0<u<v,\quad \gcd(u,v)=1.
\]

The file `docs/prime-case-candidate.md` contains a complete proposed
reverse-apex extraction. Its stated conclusion is that every scale-one
beta tiling contains a standard corner of \(v^2\) tiles. A separate
fresh audit, `docs/audits/beta-c-on-side-2026-10-08.md`, already explains
the consequence for the case in Beeson's letter. Thus that consequence
must not be presented as a discovery of this later attempt.

Here is its short dependency-minimal form. After the corner is removed,
the residual W triangle has a side of length \(u(b+c)\) on the original
base. It contains a whole c-edge: each a- or b-edge contributes a gamma
endpoint, no target corner admits gamma, and two gamma angles cannot
share a straight boundary junction.

Let \((A,B,C)\) be its whole-edge counts, with \(C\ge1\). Reduction modulo
\(v\) gives \(B=u+v\ell\), \(\ell\ge0\), hence

\[
uc=Aa+v\ell b+Cc.
\]

For a positive chain \(nc=Aa+Bb+Cc\) with \(n<v\), the exact arithmetic
lemma gives \(B=0\), \(A=vh\), \(C=n-uh\). Applied at \(n=u\), it gives
\(\ell=0\), \(A=vh\), \(C=u(1-h)\). Positivity of C forces h=0:

\[
\boxed{(A,B,C)=(0,u,u).}
\]

The unextracted base corner cannot therefore have c on its equal side:
its unique beta tile would then have a on the base. This contradicts
A=0. The argument depends on the reverse-apex extraction but **does not
depend on the separate W nonexistence induction**.

## The long c/a relations are permitted

For completeness, put \(d=v-u\). If a chain has length \(nc\), reduction
modulo v writes its counts in the form

\[
B=v\ell,\qquad A=vh-d\ell,\qquad n=C+uh+d\ell.
\]

If \(n<v\), then \(\ell>0\) would force \(h\ge1\), and hence
\(n\ge u+d=v\). Therefore \(\ell=0\). This forbids opposite b-edges
but allows \(uc=va\). Only the stricter hypothesis \(n<u\) forbids
opposite a-edges too.

The reverse-apex extraction uses no-b for its columns; the next forced
tile occupies an alpha sector, whose incident sides are b and c.
Consequently a c/a relation elsewhere on the column is not itself an
obstruction to this step. The W proof uses c-only after separately
establishing the stricter column bound n<u.

The actual proof was reread with the following possible failure points
in mind:

* A cap has both endpoints blocked before a short-chain lemma is used.
* The tiling is fixed throughout; previously completed columns are not
  redefined when a new edge reaches them.
* A newly supplied edge joins the old component through the actual
  truncated corner, so an extension past its old maximal endpoint is
  a contradiction, not a new component.
* Each column is completed before its no-b conclusion is derived;
  forcing inside its completion uses only smaller column indices.
* The last initialization reaches height zero. No length lemma with
  the impermissible index v is invoked.

No missing implication was found in these points. This is a check of
the written argument; it is not a formal proof assistant certificate
or a claim that external review has occurred.

## Why this does not finish the composite problem

The scale-one W and beta exclusions yield the intended prime-case
consequence only together with the separately audited exhaustive branch
classification. At general integer scale j, the counts are
\(j^2(2v^2-u^2)\) and \(j^2(3v^2-u^2)\). The scale-one column bound does
not automatically hold when j>1.

In particular, W at (u,v,j)=(2,3,2), with tile (6,5,9), target sides
(54,56,30) and count 56, remains unresolved in this repository's fixed-
tile branch. The existing boundary theorem leaves two exact roots;
the stored continuation searches are INCOMPLETE. Neither their timeouts
nor the scale-one theorem exclude these roots.

Prime closure also would not classify squarefree composite counts.
For example the valid primitive 120-degree norm triple

\[
(a,b,c)=(39,16,49),\qquad 49^2=39^2+39\cdot16+16^2,
\]

has the F3 coefficient

\[
3(a+b)(a+2b)=11715=3\cdot5\cdot11\cdot71.
\]

It is squarefree while a/b>2. The arithmetic fact alone does not decide
its scale-one F3 geometry. This example is given to distinguish the
scopes, not as a claim that the global count 11715 is impossible or
unresolved across every other branch.

The useful next target in this direction is therefore a new argument
for small scales j>1, rather than another relabeling of the existing
scale-one proof or another internal-audit PASS.
