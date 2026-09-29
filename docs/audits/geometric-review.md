# Fresh geometric audit of the scale-one proof

29 September 2026. Audited file: `prime-case-candidate.md`.

## Verdict

I independently read the entire proof and reconstructed its local geometry, rather than relying on the earlier reviewers' conclusions. **I found no mathematical gap.** In particular, the actual-component and T-junction arguments, use of earlier completed columns, and the W appendix's row forcing withstand the checks below. This is an internal mathematical audit, not formal verification or an external referee report. The result concerns the two displayed rational families at scale one and is not a solution of all of Erdős 634.

A separate fresh local-fan check, delegated after my own reconstruction began, also found no error. That check is corroboration, not a premise of the verdict.

## A precise chain principle behind the prose

The relevant tiling is fixed throughout. A finite collinear component is the connected union of actual collinear tile edges. At every point of its relative interior there is an edge chain on each side. A chain cannot stop at a point interior to an edge on the other side: that other tile contributes a straight sector, and the remaining half-plane requires continuation along the line. Nor can the line be swallowed at a vertex of the already supplied row, because the next supplied whole edge remains an actual tile boundary. A maximal component cannot end inside any of its constituent whole edges.

To invoke a length lemma for a *subsegment*, both chains need endpoints there; the audited proof supplies them in all instances:

- W fronts meet two external supporting lines, which block both overruns.
- Horizontal caps start on an external supporting line and end where their positive horizontal extension enters an actual crossing tile's interior.
- In reverse downward completion, the candidate lower beta tile has its horizontal edge starting at the right endpoint X; the external side blocks overrun at the left endpoint. Thus the lower chain of length ma is complete even without asserting that the full horizontal component stops at X.
- A completed maximal column has complete chains on both sides by maximality. Its initial endpoint is on the external base in W, and is blocked by the crossing apex-diagonal tile in the reverse argument.

Thus the proof does not apply its integer edge-count lemmas to a merely truncated collection of partial edges.

## Reverse-apex argument

Write the directions of p, q, and q-p as 0, beta, and theta=alpha+beta. Both beta and theta lie strictly between 0 and pi/2, with beta<theta. Also gamma=pi-theta.

### Starting configuration and caps

The angle-inventory argument excludes a gamma sector at the three-alpha apex even when 3alpha>gamma. Each outer apex tile has its c-edge on the corresponding equal side. Of the two inner radial seams, exactly one is b/c and one is b/b, counting incident lengths on the two tile sides. Reflection can put the b/c seam next to the first outer tile. Its c side overruns the outer b side because c>b.

At a cap endpoint V_m, the old D occupies the gamma sector from theta to pi, while the crossing tile contributes a straight sector on the other side of the diagonal. The remaining sector from pi to pi+theta has angle theta<gamma. Hence the opposite horizontal a-tile has beta at V_m and is the asserted normal U. Equal a lengths fix all row junctions. At any reversal, adjacent lower U tiles would contribute two gamma sectors in one half-plane, which is impossible.

At the outer-side endpoint, old D(beta) and new U(gamma) leave alpha, and the equal-side exclusion of b forces the normal D. At an inner point Z(i,t), the upper row contributes pi and the new U tiles contribute beta+gamma, leaving exactly alpha. Its downward q-side is opposite the c-edge of the new left U. The already established no-opposite-b property of column i forces c and the stated D.

### Downward continuation

At X=Z(m,t), the old left tiles occupy the sector from beta to pi, of angle alpha+gamma=pi-beta. The actual downward q-ray therefore leaves exactly the beta sector from pi to pi+beta on the left. If its tile uses a on that ray, it necessarily uses c on the horizontal ray -p. This gives a complete lower chain of length ma containing c, contradicting short-a purity. If it uses c, it is the normal U, and the same complete-chain and two-gamma arguments supply the lower U row.

Every continuation consequently adds a full c-edge. Boundedness and maximality put the lower endpoint at a grid height r>=0. The total length is (v-m-r)c, with 0<v-m-r<v, so fact (3) correctly excludes all b-edges on the opposite side. It does not incorrectly assert c-only purity in the larger range n>=u.

### Why earlier columns cause no circularity

When the current row supplies U(i-1,t-1), its c-edge joins Z(i,t-1) to Z(i,t). The old actual truncated patch contains the full chain of U(i-1,s) c-edges from Z(i,t) upward to V_i. Hence the newly exhibited edge belongs to the same previously established *maximal actual* component M_i. This is collinear connectivity, not merely connectivity somewhere in the old patch.

The earlier component is fixed by the assumed tiling; its completed side property is unconditional on all of that component. If the new edge were below an allegedly completed endpoint, that would contradict the earlier maximality conclusion. There is no assumption that earlier columns reach the base, and no induction on a future column is used.

The successive initialization states are also correct: initializing M_m supplies T(m,v-m-1), exactly what the next cap needs. Finally M_(v-1) supplies T(v-1,0), and the final alpha tile is D(v-1,0). No short-b lemma is applied at the disallowed index v. The resulting K_v consists of whole tiles, so removing it really leaves the stated W triangle.

## W appendix

### First strip

Since a,b<c, a tile attached with an a- or b-edge on the left of L_1 has strictly larger altitude than the strip width, and would cross the supporting line of OC. Thus every full left edge is c. The normal and reflected third-vertex distances on OC are (i+1)c and ic+u^2(3v^2-u^2)/v^2. The latter is nonintegral: its fractional term has numerator congruent to -u^4 modulo v^2, coprime to v. Every boundary-junction distance is an integer sum of integer side lengths. Thus all left tiles are normal U.

The intervening D-shaped regions are bounded by actual whole edges and the external side, and each has exactly one tile's area. They must each be one tile. At the top external vertex, alpha+gamma already exceeds the target angle at C, so it is an internal point of OC. Its remaining beta fan forces an additional boundary c-edge. Therefore the column height n satisfies n<u. Applying c-only purity in precisely this range is valid.

### Diagonal obstruction

The initial a/c edge and the supplied b-chain lie on opposite sides of the same line. After each crossing, the crossing tile occupies the lower/right side, so +p from the crossing point enters its interior. This verifies the horizontal-cap hypothesis. The cap forces the next normal D, whose c-edge belongs to a smaller actual base-connected column. Its established completion property supplies exactly the next rectangle needed. At the terminal OC point, the opposite chain cannot overrun the supporting line, so short-b purity applies to the complete length-jb chain. The proof works whether a<b or a>b and does not rely on the initial a/c edge itself reaching OC.

### Exact fan order in the strong column induction

Read the two residual sectors counterclockwise from +p toward the theta ray. At an inner top-row junction the residual angle is theta and its inventory is exactly one alpha plus one beta.

- Order alpha,beta: the tile incident with the theta ray has beta there, hence an a- or c-edge on that ray, on its lower/right side. This is exactly the forbidden diagonal in the lemma, with the rectangle and preceding D already supplied by the row sweep.
- Order beta,alpha: their common ray has direction beta, so it is the actual upward q-ray. The beta tile lies on its right; no-right-a forces its q-side to be c and makes it normal D. The alpha tile lies on its left; the earlier column's c-only left side forces its q-side to be c and makes it normal U.

At the outer column endpoint, the actual upward q-ray and the preceding D leave the alpha sector from beta to theta on the left. Choosing b on q puts c on theta on its lower/right side, again exactly the diagonal-lemma configuration. The other choice gives normal U. This proves the full new rectangular row.

The row sweep supplies the smaller rectangle required at each invocation: after completing point i-1, the tiles through that point include R(i-1,n+1), followed by the preceding D(i-1,n). No future-column result is needed.

The completed column height again satisfies n<u, making its opposite chain c-only. In forcing the next front, every switched beta notch introduces a right a-edge on one of these actual base-connected columns. Those columns have index at most the already present front index. Thus the no-switch argument is valid.

## Numerical checks of the delicate regimes

These are sanity checks on the symbolic geometry and integer-chain identities, not substitutes for the proof. For all three examples I exhaustively enumerated nonnegative edge-count solutions for every short-a and short-b length with index <v and every nc length with n<v. They agree with (1), (2), and (3).

| (u,v) | (a,b,c) | (P,Q) | (alpha,beta,gamma) in degrees | 3alpha in degrees |
|---|---|---|---|---|
| (1,2) | (2,3,4) | (11,7) | (28.9550,46.5675,104.4775) | 86.8651 |
| (2,3) | (6,5,9) | (23,14) | (38.9424,31.5863,109.4712) | 116.8273 |
| (5,6) | (30,11,36) | (83,47) | (49.2486,16.1270,114.6243) | 147.7459 |

The coordinates are

    q = (uP/(2v), b sqrt(4v^2-u^2)/(2v)).

They give respectively q=(2.75,2.9047375), (7.6666667,4.7140452), and (34.5833333,9.9996528), with |q-p|=b in each case. Thus both a<b and a>b, and both apex-angle orderings relative to gamma, are covered.

The nonintegral reflected-strip vertex distances lambda*c are 11/4, 92/9, and 2075/36. The first possible non-c decomposition of nc in the short n<v range occurs at n=u and is respectively c=2a, 2c=3a, and 5c=6a. These examples underscore why the reverse argument needs the proved no-b statement instead of an incorrect c-only statement through n<v.

## Expository improvements, not identified gaps

For a polished manuscript, explicitly state the chain principle above, define the maximal component as a connected union of actual collinear whole edges, specify that fan order is read counterclockwise from +p, and replace generic references to connectivity through a patch by the explicit collinear U-edge chain. Those changes make the delicate points easier to referee; none changes the mathematics checked here.
