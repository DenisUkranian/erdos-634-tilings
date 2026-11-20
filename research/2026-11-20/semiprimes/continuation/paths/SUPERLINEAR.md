# A superlinear population at a bottom height of one

Use the odd primitive unit F2 normalization and parameterization of
[TWO_PATHS.md](TWO_PATHS.md). Suppose every short height is at least 1.
Higher heights and T-junctions are unrestricted. Put $M=2\pi(u+v)/c$.
Then, whenever $u\ge6$,
$$
 n_1\ \ge\ c+
 \frac{2c(u-v)\sin(M/2)}{(u+v)M^2}
 \ \ge\ c+\frac{(u-v)c^2}{\pi^2(u+v)^2}
 \ >\ c+\frac{2}{9\sqrt3\pi^2}c^{3/2}.
$$
In particular this bound applies uniformly to the occupied minimum
height in any two-height tiling among the residual semiprimes.
The fraction of $N$ implied by the bound need not stay positive.

Work after rotation by $1/z$ so the height-1 axes are the three
Eisenstein axes. Write $w_j=\rho^j$, $\phi(x+y\rho)=b x+(a+b)y$.
Use the real linear phase $\theta(P)=2\pi k\phi(P)/c+\theta_0$,
where the integer $k$ satisfies $kab=u+v\pmod c$. The additive
constant will be chosen below. To an oriented segment on the
$j$-th height-1 axis assign
$$
 V_j[\sin\theta(\mathrm{end})-\sin\theta(\mathrm{start})],
 \qquad
 (V_0,V_1,V_2)=(-v,u+v,-u)/(u+v),\quad V_{j+3}=V_j.
$$
Ignore other axes. These values telescope on subdivisions and reverse
under orientation reversal, so summing over tiles gives zero: there is
no exterior on height 1. Every height-1 long edge has zero value,
since $\phi(cw_j)$ is divisible by $c$ for all $j$. This assertion
also holds at nonintegral tile positions.

Let $X_0=2\pi(u+v)/c$, $X_1=2\pi u/c$, $X_2=-2\pi v/c$ and extend
by $X_{j+3}=-X_j$. The phase shifts on $a w_j$, $b w_{j+1}$ and
$b w_{j-1}$ are respectively $X_j$, $X_{j-1}$ and $-X_j$ modulo
$2\pi$. To see this put $t=-b/a\pmod c$. The phase coefficients
on an $a$-edge, in units $2\pi/c$, are $(u+v)t^j$ since
$t^2=t-1$ and $\phi(a\rho)/(ab)=(a+b)/b=t\pmod c$.
Here $tv=u+v$ follows from $a(u+v)+vb=uc$, hence
$t(u+v)=u$. For the $b$ coefficients use $b/a=-t$.

For a tile with long height 2, let $P$ be its obtuse vertex.
In CCW order its short edges end at $P$ after a step $aw_j$ and
start there with a step $bw_{j+1}$. Their summed value has first-order
Taylor term
$$ (V_j X_j+V_{j+1}X_{j-1})\cos\theta(P)=0 $$
for all six $j$, directly from the three weights. The remainder has
absolute value at most $M^2$ since both shifts have absolute value
at most $M$ and $|\sin''|\le1$.

The height-1 tiles with long height 0 consist of the $c$ base teeth
and interior half-turn pairs, by matching equal whole edges at
height 0. On one such tile the two short-edge contributions sum to
$(V_{j-1}-V_j)[\sin\theta(P)-\sin(\theta(P)-X_j)]$ because
the signed order reverses. The paired apex is displaced by
$-aw_j+bw_{j-1}$, with phase increment $-2X_j$. Its rotation changes
$j$ to $j+3$. The pair therefore contributes $(V_{j-1}-V_j)$ times
the second difference of sine at $\theta(P),\theta(P)-X_j,
\theta(P)-2X_j$. Its absolute value is bounded by $2M^2$ for the
pair: the second difference has magnitude at most $X_j^2$ by two
integrations of the second derivative.

The obtuse apices of the base teeth are $p_i+(a,0)$ with
$p_i=i(a+b,-b)$ in the rotated frame. These apices have identical
$\phi=ab$ and $j=0$. Choose $\theta_0$ so their phase is $X_0/2$
modulo $2\pi$. Their contributions have the same sign and common
absolute value $2(u-v)\sin(M/2)/(u+v)$. All other height-1 tiles
contribute at most $(n_1-c)M^2$ in total by the bounds for individual
up tiles and interior down pairs. Comparing with the $c$ base teeth
proves the first bound. For $u\ge6$, $g\le3$ gives $c\ge2(u+v)$,
so $0<M\le\pi$ and $\sin(M/2)\ge M/\pi$. Finally
$u>2v$ and $u\le\sqrt{3c}$ give the last inequality.

## Exact stronger bounds for the two controls

One can replace the three weighted sine functions by arbitrary functions
of the phase. Work in the same rotated axial frame. Choose three tables
of integer weights $f_j(r)$ indexed by $j\bmod3,r\bmod c$. Assign
weight $f_j(\phi(P))$ at an endpoint $P$ when $\phi(P)$ is integral,
and zero otherwise. An oriented segment of the corresponding height-1
axis receives the difference of the endpoint weights, and all other
axes receive zero. This assignment telescopes on all subdivisions,
including those at nonintegral positions. A whole height-1 long edge
still has zero weight. The changes of $\phi$ along short edges and
between half-turn matched apices are integral, so every contributing
short-height-1 tile in this calculation has either all integral phases
or none.

Let $d>0$ be any integer. If each single short-1 long-2 tile has
weight at most $d$ and each interior pair of short-1 long-0 tiles has
weight at most $2d$, write $w$ for the weight of one base tooth. Since
the outside boundary has zero weight, $-cw\le d(n_1-c)$. Translation
is accounted for by the $c$ possible integral residues and the zero
nonintegral case. The [certificate verifier](verify_phase.py)
checks the individual and paired inequalities for all residues and six
orientations with integer arithmetic on [these tables](phase_duals.json).
It uses only the Python standard library. The witnesses can optionally
be regenerated by [linear-programming search](make_phase_duals.py) using
NumPy and SciPy. The following counts include the fixed base teeth.

| $N$ | Exact lower bound before divisibility | $n_1$ if all short heights are at least 1 | $n_1$ if only 1 and 2 occur |
|---:|---:|---:|---:|
| 3431 | 27681846/100001 | 296 | 333 |
| 5063 | 32029539/100001 | 344 | 387 |
| 19367 | 100221576/100001 | 1092 | 1183 |
| 60023 | 211583719/100001 | 2198 | 2355 |
| 64367 | 242708167/100001 | 2535 | 2535 |
| 271151 | 668335500/100001 | 6860 | 7203 |

The last two columns are lower bounds. The single-height divisibility
comes from the full-board cut identity, and the parity in the last
column follows from the two scalar currents. These bounds concern
populations inside hypothetical tilings and leave existence open.
