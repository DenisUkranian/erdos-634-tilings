# Rotational symmetry of equilateral fillings

Let the tile have primitive positive integer sides $a,b,c$, with angle
$120^\circ$ opposite $c$. Consider an equilateral target of side
$S=mab$, where $m$ is a positive integer. The standard necessary
scale theorem gives this form for every possible target. Reflected
copies, arbitrary orientations and T-junctions are allowed.

**Theorem.** A tiling invariant under a nonidentity symmetry of the
equilateral triangle must be invariant under a rotation by
$120^\circ$, and $3\mid m$. Conversely, if $a>b$, every
$m=3t$ with $t\ge \lfloor a/b\rfloor+2$ admits a tiling with
this rotational symmetry. Thus the symmetric spectrum eventually
consists exactly of the multiples of three.

**Proof of necessity.** Write $d=a-b$, $X=c+d$, $Y=c-d$.
The norm equation gives $XY=3ab$. The
[two signed direction characters](../../../../general-spectra/PROOF.md)
sum lengths of oriented edges with weights $(-1)^j$ and
$(-1)^{j+h}$, where the edge direction is
$h\alpha+j\pi/3$. Adding a half-turn reverses both signs, so
subdivision and cancellation work at every T-junction. With a
horizontal exterior side the two counterclockwise boundary values
are both $3S$. A tile contributes $\pm X$ and $\pm Y$ in
the reference convention of the cited proof. Hence the sums of
the respective unit signs over the tiles are $3S/X=mY$ and
$3S/Y=mX$.

A rotation by $120^\circ$ adds two to $j$, preserving both
signs. All tile orbits under this rotation have size three because
the tile is scalene. Thus $3\mid mX,mY$.
At least one of $X,Y$ is a unit modulo three. Indeed, if both
were multiples of three, then $3\mid c$. The norm equation
would first give $a\equiv b\pmod3$; setting $a=b+3r$ then
gives $c^2\equiv3b^2\pmod9$, contradicting primitivity.
This proves $3\mid m$.

A reflection fixing the tiling would force its axis to be contained
in the union of tile boundaries. Otherwise a fixed point interior
to a tile would be interior to its reflected image, forcing the tile
itself to have a reflection symmetry. The axis cuts a target corner
into two 30-degree angles. Each would be a sum of tile corner angles.
Writing the other two tile angles as $\alpha,\beta$, one has
$\alpha+\beta=60^\circ$. They are rationally independent:
$2\cos\beta=(2a+b)/c$ is rational and strictly between one and two;
a rational multiple of $\pi$ would make it a rational algebraic
integer. Since the obtuse angle is $2\alpha+2\beta$, no sum of
tile angles equals $(\alpha+\beta)/2$. This excludes reflections.

**Construction.** Set $L=ab$ and $q=\lfloor a/b\rfloor$. The
[trapezoid construction, Sections 4 and 5](../../../../general-spectra/PROOF.md)
tiles an ideal trapezoid with short base $kL$ and legs $nL$ for
every $k\ge q+2$ and $n\ge1$. In axial coordinates let $H=tL$.
Take the trapezoid with vertices
$(H,0),(3H,0),(2H,H),(H,H)$.
Its shorter base and both legs have length $H$. Its images under
the two nonidentity powers of $R(x,y)=(3H-x-y,x)$ complete the
equilateral triangle of side $3H$. Tile the first trapezoid once
and carry that tiling to the other two by $R$. This gives the
asserted symmetry.

| Fixed tile | Equilateral side | Tile count | Two sign sums |
|---|---:|---:|---:|
| (33, 7, 37) | 231 | 231 | 11, 63 |
| (33, 7, 37) | 462 | 924 | 22, 126 |
| (35, 13, 43) | 455 | 455 | 21, 65 |
| (35, 13, 43) | 910 | 1820 | 42, 130 |

For both scale-one F2 controls a filling of the indicated side
$2ab$ would suffice to tile the complete board by attaching three
ordinary grids, as in the [cut theorem](README.md). The table shows
that every possible such filling has trivial symmetry. The same is
true at side $ab$ for every primitive 120-degree tile. For the
(33,7,37) tile, both displayed counts are divisible by three, so
the cardinality of tile orbits alone would miss the obstruction.
The unrestricted existence decisions at 3431 and 5063 do not follow.
