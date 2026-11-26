# Both native banks constrain the corrected even charge

For any complete tiling of either target F2 board use the positioned joint-cell tree and reflected path-frame signs. At an even lift put \(e_v=(G_v-d\mathbf1_{v=C})/c\), where \(d=a-b\), \(G_v\) is the signed short population, and C carries the axial exterior walls. The corrected charges are integers of sum zero. Then
\[
 W=\sum_{v\ {\rm even}}|e_v|\le38\quad(N=3431),\qquad W\le58\quad(N=5063).
\]
The previous bounds were [56 and 80](OFF_HULL.md). Further, on **every exterior-free side of a physical lifted cut**, let ce and co be its signed even and odd short populations. Then \(|e-o|\le18\) or \(25\), respectively. Both original counts remain open.

## 1. Local costs, including the exceptional core

Mark C, the slant marker T, and every even lift with nonzero corrected charge. Let H span the marks. At a marked vertex with corrected charge e the actual charge and the total signed odd bank arriving there are
\[
 G=ce+d\mathbf1_C,\qquad R_0=de+2c\mathbf1_C-c\mathbf1_T .
\]
These are the [positioned cut identities](OFF_HULL.md#a-zero-bank-test-for-both-parities). Set σ to the sign of G, taking + when G is zero. Write \(R=\sigma R_0\), n for the short population and m for the minority population, so \(n=|G|+2m\).

An individual aligned signed gate current is at most \(p=m+\lfloor(A|G|+F)/D\rfloor\), and the opposite current magnitude is at most m. Here (A,D)=(43,222) or (8,43). Normally F=0. At C use F=424 or 88. In fact the [unsigned gate certificate](../../../2026-11-20/semiprimes/continuation/global-closure/median/NATIVE_GATE_CAPACITY.md) telescopes with the actual outer endpoint source. In standard axial coordinates this source has exactly two directed wall differences. Each has absolute value at most the largest range of one axis table. Twice that maximum gives the stated allowances, valid after any residue shift, orientation change, sign reversal or hand exchange. At T the single wall difference vanishes by its period. Endpoint differences localize to each physical lift, including at split contacts. Standard core sign residues (19,8) and (5,27) become (8,19) and (27,5) in path signs. The checker also enforces the [minimum core sizes](../axial-reserve/README.md).

For a direction outside H, with signs aligned by σ, the outgoing and incoming banks have currents dj,cj. The whole far component has signed odd population σcj and each even lift there has zero charge. A nonzero j costs at least \(c|j|+2fc\) tiles there, with f=2,3 respectively. To verify the parity exchange in the [branch argument](EXTERIOR_RESERVE.md), its odd root alone pays at least \(2c|j|\) by the ordinary one-gate capacity. If there is another occupied odd lift, an occupied even lift lies between them by the no-empty-ancestor theorem. Both cost at least 2c, and the total branch block count has parity j. If the root is the only occupied odd lift, it carries the whole charge and its outgoing gates beyond the entering gate have signed current zero. If other tiles occur, add at least 2c to the single-signed-gate bound. Otherwise apply the stronger physical terminal bound. These are exactly the three alternatives in that argument and do not require a branch of zero net charge to be empty.

For degree ℓ in H, define \(J=\max(0,\lceil(|G|-\ell p)/d\rceil)\). If J>0 then the net outward index t is at least J and at least \(g=\lceil J/\lfloor p/d\rfloor\rceil\) gates have nonzero current. A zero denominator excludes the case. For J=0 start with g=0. At an ordinary leaf that fails the [single-signed-gate population bound](../axial-reserve/README.md), require at least one such gate. The population paid at this marked vertex is at least
\[
 L=n+2fcg+\max(|R|,2cJ-R).
\]
Indeed outside components pay at least \(c\sum|j|+2fcg\); hull banks pay at least \(|R-ct|\). The components for different marks are disjoint, as are the marked short populations and the odd owners with different long markers. Thus \(N\ge\sum L\). All occupied ordinary vertices and both signs use the previous block divisibilities. An empty T is allowed.

The checker subtracts \((c+d)|e|\) from L, adding shifts d+2c at C and c at T. Each resulting cost is nonnegative by \(L\ge |G|+|R_0|\). The available total is \(K=N-(c+d)W+d+3c\). For each regular marked vertex enumerate the minority size and degree. At fixed surplus 2−ℓ keep the cheapest cost. Combine lists by adding costs and surpluses, dropping an option only when a cheaper or equal one gives at least its surplus. Positive and negative corrected charge each total W/2. Enumerate the signed charges at C and T separately.

The sum of surpluses of the marks is at least two. Every unmarked H vertex has degree at least two by minimality. At 3431 the maximum surpluses for even W from 56 down to 40 are −7,−5,−4,−3,−2,−1,0,1,2. At 5063 the W=80 budget has no profile and the maxima for 78 down to 60 are −6,−5,−4,−4,−3,−2,−1,0,1,2. These are exact results for the stated relaxation.

## 2. The middle vertex when the surplus is two

Equality forces every unmarked vertex of H to have degree two. In particular the odd middle vertex B has precisely its C and T directions in H. Cutting at B separates all marks into these two sides. Each side separately needs marked surplus at least one. Its full sum of 2−degree, with degrees taken in H, equals one by the tree degree identity with one outgoing edge.

For one side rooted at v=C or T, let E be its total corrected even charge in blocks, and o its odd charge in blocks. The even owner current toward B and the opposite B current are
\[
 P=cE+d\mathbf1_C-do,\qquad Q=dE-co+2c\mathbf1_C-c\mathbf1_T .
\]
These follow directly from the two characters on the whole side. The sign normalization σ is applied only after computing these currents. Require \(-m\le\sigma P\le p\). The other ℓ−1 hull gates at v can supply at most (ℓ−1)p aligned owners. Thus replace J by \(\max(0,\lceil(|G|-\sigma P-(\ell-1)p)/d\rceil)\), pay |Q| on the native bank, and use \(R-\sigma Q\) in place of R for the residual banks.

Split the remaining positive and negative corrected even charges in all ways between the two sides. The sums E on the two sides are opposite. Their odd charges o,t obey \(|o|+|t|+|1-o-t|\le V\) with the earlier [odd limits 39 and 59](EXTERIOR_RESERVE.md). Each side can now be tested by the same degree recursion with its prescribed bank.

There is a further disjoint payment. Let q,r be the resulting signed B currents. Both banks have so far been charged at exactly |q| and |r| in the two side bounds. Enumerate positive and negative B populations cP',cM'. They must cover the sums of positive and negative parts of q,r, and each gate must satisfy its own unsigned capacity. Add \(c(P'+M')-|q|-|r|\) for the whole middle lift. None of its tiles are in the other populations charged above: its only possible H neighbors are C,T. All its other gates enter components disjoint from both sides.

The total absolute *net* odd charge in blocks required outside those sides and B, taking the absolute value after summing, is
\[
 h=\left|P'-M'-(q+r)/c\right|.
\]
Indeed every additional gate from B has signed current equal to minus the far odd charge, since all far corrected even charges vanish. If h>0 these components contain at least ch odd tiles, raised to 3c if h=1 by the ordinary block bounds. Their even roots are individually balanced. Their entering bank currents sum in absolute magnitude to at least dh by the cut equations. Each root has both sign populations divisible by c, so these roots cost at least \(2c\lceil dh/c\rceil\) more tiles. This counts physical owners on both banks without requiring connected Euclidean regions or discarding balanced descendants.

At W=40 the 3431 budget K is 1048. The cheapest side combination after the preliminary budget tests and the middle payment costs **1052**. At W=60 the 5063 budget is 1314 and the minimum is **1386**. Preliminarily discarded cases already exceed the budget. The [replay](EVEN_VARIATION.json) records each generic boundary charge pair, using a cap above the budget for failed combinations. This excludes both equality rows.

## 3. Check by four disjoint sector populations

For an exterior-free component with charges (e,o) split all tiles by parity and side of its entering edge. The signed totals are ce, co inside and d−ce, c−co outside. Put \(p=ce-do,\ q=de-co\). For an even inside root the prescribed signed banks are p on the inside even sector and q on the outside odd sector. For an odd inside root they are −q on the inside odd sector and −p on the outside even sector.

Independently of the subtree recursion, consider a sector of signed total s with a bank of signed current u≠0. Set \(s'=\operatorname{sign}(u)s\). If its unsigned population is n, its aligned population must cover |u|. The endpoint capacity remains valid on enlarging the root's sign populations to the whole sector because both coefficients are positive. Thus
\[
 n\ge\max\bigl(|s|,2|u|-s',\lceil[2D|u|+(D-2A)s'-2F]/D\rceil\bigr).
\]
Use the core allowance whenever the sector contains C, including when its bank might actually be ordinary. Round up using n=s+2M and the appropriate negative sign residue for M. The four lower bounds must sum to at most N. Enumerating \(-W/2\le e\le W/2\) and \(-(V-1)/2\le o\le(V+1)/2\) gives the stated bounds on |e−o| for both root parities. A surviving pair satisfies only necessary conditions.

Run `python3 even_variation.py | diff - EVEN_VARIATION.json` from this directory. The verifier rechecks the original capacity tables on every placement residue and reconstructs the marked owners, all occupied signed gate counts, and the two native bank equations on both complete 143 controls. On these controls B supplies currents 14 and −7, and C and T receive those respective currents. Neither control exercises a charged off-spine branch at B. The numerical target bounds use their own moduli.
