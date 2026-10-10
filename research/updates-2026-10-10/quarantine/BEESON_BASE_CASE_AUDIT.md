# Index-domain correction and an explicit first-column audit

9 October 2026. Review prepared for Denis Paliy with ChatGPT assistance.

## Status and scope

This note audits the latest objection to *The reverse-apex continuation: explicit induction for review* (four-page PDF dated 9 October 2026). It identifies an index-domain omission, gives a proposed explicit first-column argument without assuming a pure-c outer side, and checks how that restriction interacts with the later steps. It is not external peer review, a formal verification, or a new certification of the full beta nonexistence theorem. No original attachment or repository file has been modified.

The accompanying program checks algebra and finite index/inventory regressions only. It does not verify the universal geometric forcing.

## 1. What the objection correctly identifies

The preliminary argument proves that each equal side has **no b-edge**, not that it has only c-edges. These assertions must not be conflated.

Write a=uv, b=v^2-u^2, c=v^2, with coprime 0<u<v. Once b-edges have been excluded, the edge counts on a side of length vc satisfy

    A*a+C*c=v*c,
    u*A+v*C=v^2,
    A=v*h, C=v-u*h.

The condition C>=1 does not generally force h=0. For example, (u,v)=(2,5) gives

    (a,b,c)=(10,21,25),
    125 = 5*10+3*25,
    2*25 = 5*10.

These are possible length inventories, not a claimed tiling. They suffice to show that arithmetic alone does not prove a pure-c equal side.

The short-c lemma also concludes only 'no b', and applies to n*c when n<v. It cannot be applied to the whole equal side with n=v, and even in its valid range it permits a/c exchanges.

## 2. The missing index lower bound

Item 3 of the PDF's invariant says 'For every i<j' without explicitly saying 1<=i. This is particularly problematic because the grid templates D(i,t), U(i,t) use i=0, and V_0=B.

If i=0 is included among the components in item 3, the associated descending line is AB. Its assertion would require precisely the unjustified pure-c boundary property raised in the objection. The later statement that the other invariant clauses are empty at j=1 would then be inconsistent with that reading.

The intended corrected clause is:

> For every integer i with **1 <= i < j**, the fixed actual maximal internal component M_i descending from V_i in direction -q has the stated completed-bank and no-b properties. There is no M_0 in this invariant. The boundary AB is treated separately, using only the no-b boundary lemma.

This is an explicit correction to the index domain, not a claim that the original wording was unambiguous. To justify it, one must also check that the later argument never needs M_0. Section 5 below performs that dependency check.

With this correction, at j=1 the required region is T(0,v-1), an empty tile set, and there are no previous internal components. The remaining requirement is the one edge BV_1 supplied by the actual apex tile. It is not T(1,0), and does not assert a tiling along all of AB.

## 3. Preliminary boundary and apex facts

Let p be horizontal of length a and q have length c, with |q-p|=b. The target is

    A=0, B=v*q, C=u*(3v^2-u^2),

and Z(i,t)=i*p+t*q, V_j=Z(j,v-j). The tile angles satisfy 3alpha+2beta=pi. The irrationality argument and angular inventories are as in Section 2 of the PDF.

Here is the no-b proof, separated from any pure-c claim. Every target side contains a c-edge: each supported a/b edge would otherwise supply one obtuse gamma endpoint; none can be at a target corner, and two cannot share an internal straight junction. On an equal side of length vc, reduction modulo v makes its b-count a multiple of v. If at least v such edges occur, removing v of them leaves

    vc-vb=u*a.

The short-a statement applies because u<v and forces every remaining edge to be a, contradicting the required surviving c-edge. Thus no b occurs on either equal side.

At the 3alpha apex B, the angular inventory is exactly three alpha tiles. An alpha tile has incident sides b and c. Hence the two outer apex tiles have c, not a or b, along the equal sides: a is opposite alpha, and b has just been excluded. This concerns the FIRST boundary tile only.

Each outer apex tile has b on its inner ray. The central alpha tile has one b-side and one c-side. Choose the reflected labeling so that its c-side faces the inner b-side of the left outer tile D(0,v-1). This fixes the starting configuration without prescribing the rest of AB.

## 4. Explicit first-column argument, with no earlier columns

### 4.1 The first horizontal tile

Set

    P_0=(v-1)*q,
    V_1=p+(v-1)*q.

The actual outer tile is D(0,v-1), with vertices P_0,V_1,B. Its edge BV_1 has length b. The central apex c-edge starts at B on the same ray and passes through V_1, because c>b. Thus V_1 is strictly inside an actual edge on the opposite bank.

The horizontal edge P_0V_1 has length a. Its left extension leaves the convex target across AB, and its right extension enters the central tile. Therefore its opposite bank is a whole-edge decomposition of length a. The short-a statement at index 1 forces one a-edge. Equivalently, c>a rules out c, and a nontrivial all-b decomposition is impossible since gcd(a,b)=1 and b>1.

At V_1 the old tile contributes gamma and the central crossing tile contributes pi. The remaining angle is alpha+beta<gamma. The new a-edge tile therefore has beta, not gamma, at V_1, and is U(0,v-2).

At P_0, the old D-tile contributes beta and this U-tile contributes gamma, leaving one alpha sector. The next boundary tile must consequently have b or c on AB; the no-b boundary statement forces c. It is D(0,v-2).

Thus T(1,v-2) is actual and the first full c-edge of M_1 is present. No hypothesis about an earlier component has been used.

### 4.2 Conditional downward continuation

Suppose the already justified region is T(1,t), and the actual maximal internal component M_1 continues below

    X=p+t*q.

The known left tiles D(0,t),U(0,t) contribute gamma+alpha=pi-beta. Actual continuation along -q leaves exactly one beta sector on that bank. Its tile has either a or c on the descending ray.

If it has a there, it has c horizontally to the left. Its other endpoint would be

    X-(c/a)*p = (1-c/a)*p+t*q.

But c/a=v/u>1, so this point is on the exterior side of AB. In the (p,q) basis the target is in the half-plane whose p-coordinate is nonnegative, while this endpoint has negative p-coordinate. The tile would leave the target. This is a direct containment contradiction at j=1; it uses no purity or length estimate for the whole side AB.

Hence the descending edge is c and the tile is U(0,t-1). Its horizontal a-edge reaches t*q on AB. At that boundary point it contributes gamma beside the old D-tile's beta, leaving one alpha sector. Again only the absence of boundary b is used to force D(0,t-1).

This proves T(1,t-1) whenever actual continuation occurs. It does not assume continuation forever.

### 4.3 Termination and the permitted a/c exchanges

The first edge of M_1 is whole and every actual continuation adds another whole c-edge on its left bank. Since the tiling is finite and bounded, its maximal component terminates at some

    p+r*q,  r>=0 an integer.

If a proposed continuation left the target, that would instead already be a contradiction. Consequently its length, when the hypothetical tiling remains consistent, is

    |M_1|=(v-1-r)*c,
    1<=v-1-r<=v-1<v.

Only at this point is the short-c lemma applied to the complete opposite bank, giving no b there. It does NOT give no a.

The prefix of AB established by T(1,r) is from B down to r*q; its length is (v-r)c. The remaining segment from A to r*q has not been prescribed. In particular r=0 is NOT an initial assumption. This is the distinction between an actual truncated corner and the entire standard corner.

### 4.4 The first diagonal extension

At V_1, the central crossing tile, D(0,v-1), and U(0,v-2) contribute pi,gamma,beta, leaving one alpha sector on the right of the descending q-ray. The side of an alpha tile on that ray can be b or c, not a. The now established no-b property of M_1 forces c, hence D(1,v-2) and its actual b-edge V_1V_2.

The possibility of a/c exchanges at other points of M_1 is not excluded and is not used as a contradiction.

Thus the proposed first-column argument starts without a pure-c hypothesis for AB. Its logical inputs are the no-b boundary lemma, the actual apex tiles, whole-bank endpoint justification for the first horizontal edge, and ordinary angular/containment reasoning. For v=2 this is already the terminal diagonal step, rather than the initialization of another internal stage.

## 5. Does removing i=0 break the later steps?

The index correction is consistent with the uses of previous columns in the PDF:

- In Step A, the point on AB is treated separately using the no-b boundary lemma. The other horizontal grid points have indices 1<=i<j. Only these use M_i.
- Step B has the same separation: the endpoint t*q is on AB and is handled by the boundary lemma; all remaining alpha gaps use indices 1<=i<j.
- New c-edges at an internal point attach to the fixed earlier M_i because the known actual grid connects them to V_i. A continuation beyond a previously established maximal endpoint would itself contradict the hypothetical tiling; it is not permission to change the component.
- Step C uses the current M_j only after its whole-bank bound has been proved. Its existence is not part of the initial invariant at that same stage.

Therefore no identified use requires a pure-c M_0. This is a dependency audit of the proposed proof, not an external validation of all its geometric lemmas.

## 6. Overall conclusion and evidence boundary

The pure-c assertion about AB is not established by the preliminary arithmetic, and the email is right to reject that as an available premise. The missing lower limit in item 3 is a real defect in the presentation and makes that reading understandable.

It does not follow from this objection that the intended induction cannot start. Restricting previous internal columns to 1<=i<j and spelling out the first-column argument above avoids that premise. The first-column length is controlled on the internal component M_1, not on AB.

The appropriate communication is an explicit correction and a local proof for review, not 'the checks passed, therefore the objection is wrong.' The full candidate should retain its status pending scrutiny of the corrected geometric argument. The current review provides neither a counterexample to the final mathematical claim nor a formally verified proof of that claim.

## Sources and computations

Primary reviewed text: *The reverse-apex continuation: explicit induction for review*, Denis Paliy, 9 October 2026, four pages, especially Sections 2-6. The latest incoming objection was supplied verbatim by the user. No theorem in an external paper is used to prove the first-column argument above.

The accompanying `check_base_algebra.py` verifies nine symbolic coordinate/metric identities, 1,101 bounded primitive boundary-inventory cases, and 4,950 first-column index/template counts. These tests do not machine-check geometric forcing. The existing PDF was left unchanged so that the correction is distinguishable from the document that was actually sent.