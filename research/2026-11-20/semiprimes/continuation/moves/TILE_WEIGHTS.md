# Ordinary tilings of the two unit F2 boards require at least 138 and 146 T-junctions

Every tiling of the 3431 board by $(33,7,37)$ has at least **138 distinct T-junctions**. Every tiling of the 5063 board by $(35,13,43)$ has at least **146**. The lower bounds concern all tilings, including any outside the known constructions. They do not assert nonexistence of a tiling with more T-junctions.

Place the board at $O=0$, $B=bq$, $C=ap\rho$ with $p=a+2b$, $q=2a+b$, $\rho=e^{i\pi/3}$, $z=(a+b\rho)/c$. Its oriented CCW sides $OB,BC,CO$ have directions $1,\rho z^2,-\rho$ and lengths $bq,c^2,ap$. Indeed $\rho(a+b\rho)^2=ap\rho-bq$. All tile side directions are of the form $\rho^jz^h$ by propagation across positive-length contacts. The rational number $2\cos(\arg z)=(2a+b)/c$ lies strictly between 1 and 2, so $\arg z$ is an irrational multiple of $\pi$ and the integer height $h$ is unique.

Assign a signed integer weight $W(h,j,k)$ to a whole oriented tile side of label $k=a,b,c$. The weight changes sign when $j$ increases by 3. It is periodic in $h$ with period 4. Extend it linearly to side-count words $w=(x,y,s)$. The certificate satisfies for every $h,j$ and both choices of sign
$$
 W(h,j,a)+W(h,j\mathbin\pm1,b)-W(h\mathbin\pm1,j,c)=0 .
$$
In the reference tile the oriented sides have vectors $a,b\rho,-cz$; reflecting gives $a,b\bar\rho,-c\bar z$. Rotation translates $h,j$ and reversing the boundary negates all weights. Thus each individual triangle in every ordinary tiling has zero total weight.

On each interior line, cut its maximal runs at all points where both banks end a tile side. Between successive such common endpoints, the two banks are words of whole tile sides. The outer boundary of a convex board has only one bank, which we treat separately. The multiplicity difference $w$ across an interior block satisfies $ax+by+cs=0$. Orient the difference so that the sum of block scores equals the exterior score; this follows by summing the zero tile boundaries. A balanced block has zero score regardless of the order of its two words. An imbalanced block has at least $\|w\|_1-2$ internal T-junctions, since all its interior bank endpoints belong to just one bank. T-junctions counted by different blocks are distinct. In particular, at such a point one tile side passes through the point, so no transverse interior straight block can also pass through it. Each cost $\|w\|_1-2$ is even because $a,b,c$ are odd.

Every outer side word contains at least one $c$-side. Otherwise each letter ($a$ or $b$) would put a tile's $120^\circ$ corner at one of its two endpoints. The board corners have angles strictly below $120^\circ$, and each interior join can host at most one such corner. There are more letters than interior joins.

The files [3431 weights](tile_weights_3431.json) and [5063 weights](tile_weights_5063.json) give the 36 integers for $h=0,1,2,3$, $j=0,1,2$ and $k=a,b,c$, in that order. They also specify a common denominator $d$, a cutoff 160 and three exterior lower bounds $K_X,K_Y,K_S$. The [standalone checker](check_tile_weights.py) verifies that each tile and its mirror have zero weight. It also verifies two families of integer inequalities:

* For each nonzero integral side relation of cost at most 160, $W(h,j,w)\le d(\|w\|_1-2)$ in all four height classes and all six directed axes. It suffices to enumerate one of $w,-w$ since adding 3 to $j$ negates the weight.
* Every legal exterior word along $OB$, $CO$ or $BC$, respectively, has weight at least $K_X,K_Y,K_S$. These use $(h,j)=(0,0),(0,4),(2,1)$ respectively. All nonnegative count triples of the required actual lengths with at least one $c$ are tested.

If a single interior block exceeds the cutoff, the assertion already follows. Otherwise add the block inequalities and the exterior inequalities to obtain
$$
 \sum_{\rm blocks}(\|w\|_1-2)\ge (K_X+K_Y+K_S)/d ,
$$
where the sum counts only imbalanced blocks. At 3431 the rational bound is $276000320/2000007>137$ and at 5063 it is $29199854/200001>145$. The total cost is even. This proves the two claims.

Run `python3 check_tile_weights.py` with assertions enabled. It checks 8928 local inequalities at 3431 and 7752 at 5063 in addition to all tile identities and exterior words. The integer certificates were found by linear programming; their proof and replay require no optimization solver, floating-point calculation or bound on the heights in a tiling.
