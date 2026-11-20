# Counting compulsory T-junctions by Laurent coefficients

The whole 3431 board requires **at least 64** T-junctions, and the whole 5063 board requires **at least 56**. These statements encompass arbitrary tilings of the specified scale-one F2 triangles. A T-junction is a tile vertex in the relative interior of another tile side. Only interior endpoints on imbalanced straight contact blocks are counted in the proof.

Normalize $c$ to one in the formal edge lengths and write $t$ for the unit complex variable in place of the true $z=(a+b\rho)/c$, where $\rho=e^{i\pi/3}$. For a word with side counts $w=(x,y,z_c)$ define $P(w)$ to be its virtual length times $\rho-\bar\rho$. In increasing Laurent degrees $-1,0,1$ its coefficients, in the basis $1,\rho$, are
$$
 (-y,x),\quad (-z_c,2z_c),\quad (y-x,x).
$$
These formulas follow by solving $a(t)+b(t)\rho=t$ together with the conjugate relation. In particular every nonzero side-count relation $ax+by+cz_c=0$ has both outer Laurent coefficients nonzero: if $x=y=0$, also $z_c=0$.

Use the actual board at $O=0$, $B=bq$, $C=ap\rho$. Write $X,Y,S$ for its nonnegative side-count triples along $OB,OC,BC$. Each has a positive count of long sides: a boundary word with only short sides places an obtuse corner at one endpoint of every letter, but the only available sites are the interior joins, each able to accept at most one such corner. All three outer angles are below $120^\circ$.

The formal exterior sum is
$$
 F=P(X)-\rho P(Y)+\rho t^2 P(S).
$$
Every imbalanced block contributes $\rho^j t^hP(w)$, where $w$ is its bank difference, signed for agreement with the exterior. The sum is $F$ by adding the formal boundaries of the tiles. The local cost $\|w\|_1-2$ is a lower bound for the number of internal T-junctions of the block. These junctions are distinct across blocks. The [shortest relation calculation](BLOCK_SIZES.md) implies every block costs at least 8 for 3431 and 6 for 5063. Also each cost is even, since $a,b,c$ are odd and every side-count relation has even coordinate sum.

**The geometric sign test.** Fix a height $h$. The two short sides of a tile, when oriented counterclockwise around it, differ by $60^\circ$. Thus their signs $(-1)^j$ cancel, counting sides without weights. Grouping the two oriented banks of each internal contact shows that
$$
 \sum_{\text{blocks at }h}(-1)^j(x+y)=
 \begin{cases}
 X_a+X_b+Y_a+Y_b,&h=0,\\
 -(S_a+S_b),&h=2,\\
 0,&\text{otherwise}.
 \end{cases}
$$
The first quantity is strictly positive: $c$ does not divide $bq$ or $ap$. Signed short sides on a balanced block cancel in pairs by their matching multiplicities. This extra constraint uses the actual tiles, not an assumption about their positions.

**Why the searches are finite.** For $k$ blocks, each Laurent support is contained in $[h-1,h+1]$. Connect these intervals and the board's interval $[-1,3]$ whenever they intersect. A component separated from the board has zero Laurent sum on its own; its heights are disjoint from all others and avoid 0 and 2, so its signed short-side sums also vanish separately. Delete it. With at most $k$ remaining blocks every height therefore lies between $-2k$ and $2+2k$. This argument does not assume that actual tilings lack invisible cancelling clusters. Dropping them can only lower the tested cost. A smallest height below 0, or a largest height above 2, must occur at least twice to cancel the extreme coefficient beyond the board support.

The [exact integer checker](check_block_ledger.cpp) enumerates each remaining multiset of heights. At each height it enumerates nonzero integer relation vectors up to the remaining cost limit in one sign, since the opposite sign is the three-step change in $j$ among the six axes. To prune partial sums it uses their coefficients only at degrees that no future block can change. The coefficients at degrees $-1,0$ give
$$
 (Y_a-X_b, X_a-Y_a+Y_b),\quad (-X_c+2Y_c,2X_c-Y_c).
$$
It checks these against the actual possible outer words independently enumerated from the positive side lengths. They uniquely determine $X,Y$: after recovering $X_c,Y_c$, the two linear coefficient equations and the two physical side-length equations have a unique solution, with nonzero determinant coming from $c^2=a^2+ab+b^2$. At degrees $2,3$ the required coefficients are $(-2S_c,S_c),(-S_a,S_b)$ and uniquely determine $S$. Degree one need not be tested: both sides agree at the true unit $t=z$ by physical lengths, so any residual Laurent term supported only at degree one would be zero. Rejecting configurations on these necessary conditions is sufficient for the asserted lower bounds.

Run the following commands with a C++17 compiler.
```sh
c++ -std=c++17 -O3 check_block_ledger.cpp -o /tmp/check-blocks
/tmp/check-blocks 3431 63 signed
/tmp/check-blocks 5063 55 signed
```
Neither budget admits a ledger. The sign test is important. With only the Laurent identity the exact minima are 40 and 48, as verified by rerunning with the last argument omitted and budgets 39,40 and 47,48.

In fact a simple formal family explains these smaller numbers. Put $R=(v,-u,v)$ and take $3v/g$ copies at $(h,j)=(1,0)$ and $(u-v)/g$ copies at $(2,0)$. Choose exterior counts
$$
 X=(c-a,a,c-a),\quad Y=(a,2a-c,b),\quad S=(a,v(u-v)/g,b).
$$
They give the required physical side lengths; direct substitution into the three Laurent coefficients gives the identity. Its cost is $(u+2v)(u+2v-2)/g$. This family fails the signed test at height zero and hence cannot be the complete mismatch list of an ordinary tiling. The positive lower bounds on T-junction counts do not by themselves exclude either unit board.
