# Reversing the auxiliary staircase steps cannot reach a residual prime pair

Keep the primitive odd F2 tile and the ordered parameters $u,v,g$ of the [unit staircase](../../staircase/SHARP_STAIRCASE.md). Here $v$ is odd, $u$ is even and $a>b$. Consider the following relaxation of its arithmetic construction. Choose any finite set of nonzero pairs of integers $r,s\ge0$ with $r\le b$, with totals $\sum r=c-b$, $\sum s=c-a$. Require $c\mid ar-bs$, allowing $(ar-bs)/c$ to have **either sign**. No ordering, monotonicity of the auxiliary step, or geometric compatibility is required.

**Proposition.** This relaxation passes for exactly the same odd prime-product parameters as the original staircase. In particular it fails on every mixed pair in the residual table, with arbitrarily many steps allowed.

For each step introduce
$$
 n=\frac{vr+(u+v)s}{c},\qquad m=\frac{ur-vs}{c}.
$$
These are integers. Multiplication of either numerator by $a$ and substitution of $ar\equiv bs\pmod c$ gives zero modulo $c$, since $vb+(u+v)a=uc$ and $ub-va=vc$. We have $\gcd(a,c)=1$. In particular $n\ge1$ even for a reversed step, while $m$ may be negative. The same identities give
$$
 \sum n=2v,\qquad \sum m=u-2v,\qquad gr=vn+(u+v)m .
$$
The width bound gives $(u+v)m\le gb-v=2uv+v^2-v<2v(u+v)$. Hence $m\le2v-1\le(2v-1)n$, proving $u\le4v^2$ after summation.

If $g=3$ and $v\equiv2\pmod3$, then $v\ge5$ and $n\equiv m\pmod3$. For this congruence subtract the two numerators, using $u\equiv v\pmod3$ and $3\nmid c$. When $n=1$, the largest permitted $m\le2v-1$ is $2v-3$. When $n\ge2$, $2v-1\le n(2v-3)$. Now $\sum m\le2v(2v-3)$ gives the sharper bound $u\le4v(v-1)$.

Conversely the [original constructive theorem](../../staircase/SHARP_STAIRCASE.md) gives nonnegative auxiliary steps at every parameter inside these same bounds. This is an exact exclusion for the relaxed construction. A different geometric construction can change the width bound, the total loads, or the common divisibility equation.

## Exact minimum overrun when the width limit is lifted

For a parameter outside the staircase, relax $r\le b$ and keep all other conditions above. Define the cost of a load by $(r-b)_+^2$, where $x_+=\max(x,0)$. This counts the area in tiles of the reflected grid overrun in a horizontal band when that band is extended past its original apex. The cost is a statistic of this construction, not a minimum defect over all possible board tilings.

Put $M=u-2v$. Form the multiset of $2v$ integers $m_i\equiv1\pmod g$ of sum $M$ taking the two neighboring permitted values around $M/(2v)$ (just one when the average is permitted). Then the exact minimum sum of costs is
$$
\sum_{i=1}^{2v}\left(\frac{v+(u+v)m_i}{g}-b\right)_+^2 .
$$

To prove the lower bound, take any load with transformed coordinates $(n,m)$. We have $n\ge1$, and if $g=3$ then $m\equiv n\pmod3$. Split $m$ formally into $n$ nearly equal integers in the class $1\bmod g$. Their corresponding widths $r_i=[v+(u+v)m_i]/g$ add to $r$. When $m\ge n$ these widths are nonnegative, and the sum of their costs is at most the cost of $r$: moving a nonnegative width into a single load can only increase the sum of squared positive overruns. If $m<n$, all split entries can be chosen at most one. Each associated width is at most $(u+2v)/g\le b$ and has cost zero, even if a width is negative in this *formal lower bound*. After splitting all loads there are $2v$ entries. The squared positive part of an affine increasing function of $m_i$ is convex. Moving $g$ from a larger to a smaller entry whenever their difference is at least $2g$ cannot increase the sum. This gives the displayed balanced lower bound.

For attainment choose these balanced entries with $n_i=1$. Each $m_i\ge1$ since $u\ge4v$ throughout this residual odd family. Their sum and congruence are compatible since $g\mid (u-4v)$. Also $m_i<u/(2v)-1+g\le u/v$. The formulas $s_i=(u-vm_i)/g$, $t_i=(um_i-v)/g$, $r_i=[v+(u+v)m_i]/g$ now give integral loads with $r_i>0$, $s_i,t_i\ge0$ and both prescribed totals. This attains the lower bound. A zero $s_i$ is allowed by the stated relaxation.

| Board | Optimal repeated $(r,s,t)$ | Width $b$ | Minimum total overrun |
|---:|---|---:|---:|
| 3431 | $2\times(15,2,13)$ | 7 | 128 |
| 5063 | $2\times(15,4,11)$ | 13 | 8 |

These two particular placements and the resulting 105- and 117-tile notch regions were already present in the [pentagon construction](../patches/PENTAGONS.md) and the [notch exclusions](../notches/NOTCH_ENUMERATION.md). The new conclusion is optimality under arbitrary load counts, order and either sign of the auxiliary step. An overrun of eight on the 5063 board does not mean eight unplaced ordinary tiles can simply be added.

[Dynamic programming on the original loads](check_overruns.py) independently checks the exact minimum for the first 53 small residual parameter pairs and additional controls. For a partial sum $s$ the accumulated width is congruent to $bs/a\pmod c$ and is less than $c$, giving at most one state per partial sum. Run `python3 check_overruns.py`. Combining the bound with the [protected-side argument](OVERSHOOT.md) excludes separate repairs inside the oversized steps' auxiliary triangles throughout the odd residual $v=1$ family under its cited local geometric input.
