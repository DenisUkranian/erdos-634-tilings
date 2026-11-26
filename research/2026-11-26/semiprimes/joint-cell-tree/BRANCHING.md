# Sparse monochromatic lifts require other charges in distinct branches

In the standard frame call a lift ordinary if it is not the exceptional axial lift $C$. Count short tiles at each lift. For each parity separately let $m_2$ be the number of ordinary lifts with $2c$ tiles all of one sign. At 3431 also let $m_3$ count ordinary lifts of that parity with $3c$ tiles all of one sign. Set $m_3=0$ in the bounds at 5063.

**Theorem.** At least $4(m_2+m_3)$ *other distinct charged ordinary lifts of the same parity* are needed. Each of these costs at least $3c$ tiles. Thus the odd population satisfies
$$
n_{\rm odd}\ge c(14m_2+15m_3)
$$
with the right side rounded up to an odd number of $c$-blocks. The corresponding even population is at least $j+c(14m_2+15m_3)$ with the counts taken at even lifts, where $j=N\bmod c$ is the separate exceptional-core reserve. In particular a monochromatic $2c$ odd lift requires at least **555 odd tiles at 3431 and 645 at 5063**. These are conditional on a monochromatic $2c$ odd lift; they are not the earlier bounds for native two-height configurations.

**Proof.** At a fixed short lift its $c$ gates of each hand are the incident edges of the covering tree. For a monochromatic population $n_v$, the [single-gate endpoint inequality](../../../2026-11-20/semiprimes/continuation/global-closure/median/NATIVE_GATE_CAPACITY.md) bounds the number of tiles at any one gate by $\lfloor43 n_v/222\rfloor$ at 3431 and $\lfloor8 n_v/43\rfloor$ at 5063. For negative tiles use the sign-reversed inequality. The endpoint potentials isolate the lift, as in [the five-block proof](FIVE_BLOCKS.md). The only possible exterior side at an ordinary lift is the slant of length $c^2$, whose endpoints have equal residues modulo $c$ after normalization. Thus its contribution to every such periodic endpoint difference is zero. For $n_v=2c$ the caps are 14 and 16. For $n_v=3c$ at 3431 the cap is 21. All three caps are strictly smaller than $d=a-b$, and in each case the population needs at least six nonempty physical gates.

In the far component beyond an incident edge with no exterior marker, the character formulas of [the tree theorem](TREE.md) give the following signed count of tiles of $v$ using that gate:
$$
Q=\begin{cases}
dE/c-O,&v\text{ odd},\\
dO/c-E,&v\text{ even}.
\end{cases}
$$
Both $E,O$ are multiples of $c$. If no lift of the same parity as $v$ in this component is charged, $Q$ is a multiple of $d$. Monochromaticity makes $|Q|$ the actual gate population, so the strict cap forces it to vanish. This use of the cap would be invalid at a gate of a mixed-sign lift.

In the common lifted tree take the finite minimal subtree spanning the two exterior markers and all charged lifts of the chosen parity. Every nonempty gate at a counted monochromatic lift leads toward another spanning vertex. Its degree in this finite subtree is consequently at least six. A finite tree with at least two vertices has $2+\sum_{\deg w>2}(\deg w-2)$ leaves, so there are at least $2+4(m_2+m_3)$ leaves. Each leaf must be a spanning vertex. At most two leaves are exterior markers, and no counted monochromatic lift is a leaf. The other leaves are distinct charged ordinary lifts of the same parity, all outside the counted set. A charged ordinary lift with just $2c$ tiles would itself be monochromatic and counted. The proved block divisibility therefore charges at least $3c$ for each of these other leaves. The stated population bounds follow by disjointness of the lifted short populations.

For both parities together the number of ordinary monochromatic $2c$ lifts is at most 6 for 3431 or 8 for 5063. For 3431 the stronger combined bound is $14m_2+15m_3\le92$ when the counts run over both parities. For a small odd layer of at most $13c$ tiles all its two-block lifts on either board must be balanced. This proof uses signed imbalances on genuine connected sides of cuts in the auxiliary tree. It neither assumes geometric connectedness of the unions of tiles nor counts one required leaf several times.
