# Every unit F2 tiling has imbalanced internal contacts in two nonparallel directions

Let $a>b>0$ be relatively prime integers with $c^2=a^2+ab+b^2$. The tile has sides $a,b,c$. Put $p=a+2b$, $q=2a+b$, $\rho=e^{i\pi/3}$ and $z=(a+b\rho)/c$. Put the outer vertices at $0,bq,ap\rho$; the third directed side is $ap\rho-bq=\rho(a+b\rho)^2$. Its Euclidean length is $c^2$. No primality of $p,q$ is required.

On an internal supporting line take a maximal connected interval of tile sides. Each bank partitions it into whole tile sides. Cut at the points that are endpoints on both banks. Each resulting block now has two words of whole sides on the same interval. Call the block **imbalanced** if the words have different numbers of $a$-, $b$-, or $c$-sides. Merely permuting the same letters gives zero imbalance. Finiteness and convexity of the outer region justify the bank partitions: a generic point of an internal interval has a tile on each side, and a collinear tile edge cannot extend past an endpoint of the maximal interval.

**Theorem.** In every tiling of this board, imbalanced blocks occur on at least two nonparallel lines. This holds for every orientation, including reflected tiles and arbitrary T-junctions. In fact the *aggregate* signed imbalances are nonzero in at least two distinct directions, after summing over every block parallel to a given direction.

### A formal rotation of all the edges

Directions that occur in the tiling are $\rho^jz^h$. They propagate from a boundary side along positive-length contacts, since the tile angles are $120^\circ$, $\arg z$, and $60^\circ-\arg z$. The graph of such contacts is connected by following a path avoiding tile vertices. Height $h$ is unique: $2\cos(\arg z)=q/c$ is rational strictly between 1 and 2, excluding a root of unity. Opposite directions differ by the sign of the unit $\rho^j$.

Use a formal variable $t$ for $z$. Normalize the long side to one and replace the short lengths by
$$
 A(t)=\frac{\rho t^{-1}-\bar\rho t}{\rho-\bar\rho},\qquad
 B(t)=\frac{t-t^{-1}}{\rho-\bar\rho}.
$$
On the unit circle both are real, $A+\rho B=t$, and $A+\bar\rho B=t^{-1}$. At $t=z$ they equal $a/c,b/c$. Assign to a directed side its new length times $\rho^jt^h$. The boundary sum of each tile remains zero identically: the two displayed identities are exactly the two tile hands, up to multiplication by a direction and reversal. This only deforms edge *vectors*. The locations of tile vertices need not have a simultaneous geometric deformation.

Write $L_i=x_i A+y_i B+n_i$ for the boundary words on the horizontal, axial, and sloping sides, indexed by $i=X,Y,S$ respectively. All $x_i,y_i,n_i$ are nonnegative integers. Adding the edge-vector identities gives
$$
 F(t)=L_X-\rho L_Y+\rho t^2L_S
       =\sum_{(h,j)}\rho^jt^h\big(u_{hj} A+v_{hj} B+w_{hj}\big).
$$
Here $j$ is taken modulo 3 for unoriented directions, with sign incorporated in the integer multiplicities. Each triple on the right is the signed sum of whole-bank multiplicity differences in that direction, with an overall sign chosen from the cancellation identity. In particular $a u_{hj}+b v_{hj}+c w_{hj}=0$. Splitting the original sides into partial lengths and trying to deform those lengths independently would not establish this identity. Summing whole words between common endpoints does.

### Two exterior coefficients prevent a single active direction

Every exterior side contains at least one $c$ edge. Otherwise each of its $k$ boundary tiles puts its $120^\circ$ angle at one endpoint of its short boundary edge. The three outer angles are all strictly less than $120^\circ$, and two obtuse angles cannot share a straight boundary vertex. There would be $k$ different interior endpoints among only $k-1$. Consequently $n_X,n_Y,n_S>0$.

The coefficients of $t^0$ and $t^2$ in $F$ are $n_X-\rho n_Y$ and $\rho n_S$, both nonzero. If the right side had only one active direction $(h,j)$, its Laurent degrees would lie between $h-1$ and $h+1$. Hence $h=1$. Its coefficients at degrees zero and two are conjugates up to the common phase: $F_0=\rho^{2j}\overline{F_2}$, because $uA+vB+w$ is real on the unit circle. Also $F_3=0$. On the left, this last equality gives $y_S-\bar\rho x_S=0$, hence $x_S=y_S=0$. The whole sloping side therefore consists of $c$ edges of length $c$, giving $n_S=c$.

It follows that $n_X-\rho n_Y=c\rho^{2j-1}$. The possibilities for the unit on the right are $1-\rho$, $\rho$, and $-1$. Since both $n_X$ and $n_Y$ are positive, the only choice is $1-\rho$, with $n_X=n_Y=c$. The horizontal side would then have length at least $c^2$, whereas its length is $bq=c^2-a(a-b)<c^2$. This contradiction proves the theorem.

### Consequences on the two open boards

The bounds on each individual imbalanced block follow from the [integer relations between the three tile lengths](BLOCK_SIZES.md).

| $N$ | Tile | Required nonparallel blocks | Length of each, at least | Interior T-junctions on each, at least | Distinct T-junctions, at least |
|---:|---|---:|---:|---:|---:|
| 3431 | $(33,7,37)$ | 2 | 70 | 8 | 16 |
| 5063 | $(35,13,43)$ | 2 | 78 | 6 | 12 |

The interior T-junctions on nonparallel blocks are distinct. At such a point one bank has an edge passing straight through; on its side a second transverse block cannot continue past the point. The theorem excludes every construction whose multiplicity mismatches are confined to one direction, regardless of how many parallel supporting lines or additional balanced T-junctions it uses.
