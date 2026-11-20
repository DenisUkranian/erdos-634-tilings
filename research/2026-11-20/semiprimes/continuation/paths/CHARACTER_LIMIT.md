# A limit of periodic endpoint invariants on the complete two-height lattice

Use the unit F2 board and the two-height lattice $L=z(R+zR)$ of
[VERTEX_LATTICE.md](VERTEX_LATTICE.md). Let $\chi:L\longrightarrow
\mathbb C^\times$ be any character. Give each unoriented axis
$(h,j\bmod3)$, $0\le h\le3$, an arbitrary complex coefficient $w_{h,j}$.
Assign a directed segment $P\to Q$ on that axis the value
$$ w_{h,j}(\chi(Q)-\chi(P)). $$
Suppose this value, summed over its boundary, vanishes on every tile
of short height 1 or 2, allowing both hands, all six rotations and
translations in $L$. Then the sum on the boundary of the unit F2 board
is zero. Primality and the staircase are irrelevant.

This also applies to differences $f_{h,j}(Q)-f_{h,j}(P)$ of arbitrary
axis-specific functions on any finite quotient of $L$: take finite
Fourier series in the simultaneous tile-translation variable. It
does not assert an actual tiling. It only excludes this class of
zero-valued tile obstructions. The one-sided population bounds in
[SUPERLINEAR.md](SUPERLINEAR.md) remain applicable.

**The local rule.** For a tile written $0,X,X+Y$ let $x=\chi(X)$,
$y=\chi(Y)$, and use weights $A,B,C$ on its two short and one long
axes. The tile and its half-turn give
$$
 A(x-1)+Bx(y-1)=C(xy-1),\qquad
 Ay(x-1)+B(y-1)=C(xy-1).
$$
Thus $(x-1)(y-1)(A-B)=0$. The weights of all edges with a
nontrivial character increment agree: this is immediate from the
first equation if either short increment is trivial, and otherwise
both short weights agree and force the long one too if $xy\ne1$.
Conjugating the tile or reversing its boundary leaves the rule intact.
Form a graph of the twelve axis labels, joining all such active
labels in every tile. Weights are constant on its components.

For $h=1,2$, consider the restriction of $\chi$ to $E_h=z^h R$. Write
$A_h$ for the axes with $\chi(az^h\rho^j)\ne1$ and $B_h$ similarly
for $b$. Each nonempty set has at least two members: the vanishing on
two Eisenstein unit axes forces it on the third. If both are nonempty,
their union is connected in the graph. In fact each distinct pair
$j\in A_h,k\in B_h$ occurs as the two short axes of a tile (choose
one of its hands). Two subsets of size at least two in a three-element
set give a connected union by these pairings. The union comprises
every axis where the unit character is nontrivial since $(a,b)=1$.
Call such a height connected. If a height is not connected, either
$\chi$ is trivial on $aE_h$ or on $bE_h$.

**The exterior.** The boundary sides $OB,OC,BC$ have axis labels
$(0,0),(2,0),(2,1)$ and lengths $c^2,ap,bq$. Call a side active
when its complete character increment is nontrivial. There cannot be
exactly one active side in a closed triangle. We show their labels
belong to one component, which telescopes around the boundary.

If $OB$ is inactive but the other two are active, both $A_2$ and
$B_2$ are nonempty by their lengths. Thus height 2 is connected and
the claim follows. Assume henceforth $OB$ is active. Its unit long
edge of length $c$ on height 0 is then active. The short-1 down tile
with base direction $(0,0)$ connects this label to at least one
active height-1 axis.

* Suppose height 1 is connected. Because $B=c^2$ lies in $cE_1$
  ($B/(cz)=a+b-b\rho$), $\chi$ must be nontrivial on $cE_1$. Some
  height-1 long edge of a short-2 down tile is therefore active and
  connects the height-1 component to an active height-2 axis. If
  height 2 is connected this reaches every active exterior side.
  If $\chi$ is trivial on $aE_2$, only $BC$ can be active besides
  $OB$. In a short-2 down tile with its $b$-edge along $BC$ the
  $a$-increment is trivial; the $b$ and long increments are
  nontrivial, joining this very axis to height 1. If $\chi$ is
  trivial on $bE_2$, interchange the roles of $a,b$ to attach $OC$.

* Suppose $\chi$ is trivial on $aE_1$. The base connects through its
  short-1 down tile to the active $b$-axis $(1,-1)$. The short-1 up
  tile with the same $b$-axis has active long axis $(2,1)$: its
  $a$-axis is $(1,-2)$ and $(1,-2)=(1,1)$ as an unoriented label.
  This joins the base to the axis of $BC$. If height 2 is connected
  this suffices. If $\chi$ is trivial on $aE_2$, then $OC$ is
  inactive and we already reached the only possible partner. The
  remaining possibility of triviality on $bE_2$ is impossible here:
  $cE_2\subset E_1$, so $\chi$ would be trivial on both $acE_2$
  and $bE_2$, hence on $E_2$ by $(ac,b)=1$. This would leave both
  side edges inactive while the base is active.

* If $\chi$ is trivial on $bE_1$, the same short-1 down tile attaches
  the base to its $a$-axis $(1,0)$, and the short-1 up tile with that
  $a$-axis attaches it to the active long axis $(2,0)$ of $OC$. If
  height 2 is connected this suffices, and triviality on $bE_2$
  leaves $BC$ inactive. Triviality on $aE_2$ would imply triviality
  on both $bcE_2$ and $aE_2$, again impossible by coprimality.

This covers every character. The result does not rule out inequalities,
location-dependent boundary tests confined to the board, higher-order
invariants, or currents that do not come from periodic endpoint
differences.
