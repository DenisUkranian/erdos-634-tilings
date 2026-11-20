# Every 3431 tiling needs at least 88 T-junctions; every 5063 tiling needs at least 106

These bounds apply to the complete primitive F2 board, including arbitrary orientations, reflections and T-junctions. They allow any number of active edge heights of any size. The exact dual certificate is particularly short: its integer table has 15 entries per board.

Use the [formal edge-word and short-side character identities](CONTROL_LEDGERS.md). For a word $w=(x,y,z_c)$ its three coefficient pairs are $p_{-1}=(-y,x)$, $p_0=(-z_c,2z_c)$, $p_1=(y-x,x)$. An imbalanced contact block has $w\ne0$, $ax+by+cz_c=0$ and cost $\|w\|_1-2$. Its internal T-junctions number at least this cost, with no duplication across blocks. Every cost is even.

A height-periodic score for a signed block or exterior word is
$$
 W(h,j,w)=\sum_{s=-1}^1 \lambda_{(h+s)\bmod4}\mathbin{\cdot}(\rho^j p_s(w))
        +\mu_{h\bmod4}(-1)^j(x+y).
$$
The dot is the ordinary pairing of integer coordinate pairs, and multiplying $(l,m)$ by $\rho$ gives $(-m,l+m)$. Comparing Laurent coefficients, summing them in classes modulo four, and adding the height-wise short-side identities gives
$$
 \sum_{\text{imbalanced blocks}} W(h,j,w)
 = W(0,0,X)+W(0,4,Y)+W(2,1,S).
$$
Here $X,Y,S$ are the three outer side-count triples, of lengths $bq,ap,c^2$. Each has at least one $c$-side by the boundary obtuse-corner count. Axis 4 means the reverse of axis 1 on the side directed back to the origin.

In each JSON certificate the first eight integers in `Y` give the four $\lambda$ pairs in order. The next four give $\mu$ and the last three give $K_X,K_Y,K_S$. Write $d$ for the certificate's positive common denominator. The [verifier](check_periodic_weights.py) checks, solely over integers, all of the following.

* Every nonzero relation $w$ of cost at most 120, in every one of the four height classes and six directed axes, satisfies $W(h,j,w)\le d(\|w\|_1-2)$. One of $w,-w$ suffices since $j\mapsto j+3$ negates the score.
* Every possible nonnegative exterior word of its physical length with positive $c$-count has score at least $K_X$, $K_Y$ or $K_S$, as appropriate.

If some block has cost greater than 120, the bounds already follow. Otherwise these inequalities and the score identity give a lower bound on total local cost of $(K_X+K_Y+K_S)/d$. At 3431 this is $43573855/500001>87$; at 5063 it is $20920960/200001>104$. Rounding up to an even integer gives 88 and 106. Neither lower bound asserts that the required junctions can be arranged in an actual tiling.

Run `python3 check_periodic_weights.py` with assertions enabled. It verifies 5088 and 4368 local score inequalities, respectively, and independently enumerates all exterior words. Linear programming was used only to discover the two integer certificates.
