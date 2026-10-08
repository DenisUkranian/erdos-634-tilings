# The high-ratio F3 hexagon: a positive dissection and a precise row barrier

This note does not fill the hexagon and does not classify F3. It records
an exact positive rearrangement and rules out one overly simple way to
turn the new small formal inventory into a geometric patch.

## 1. Two equilateral defects joined by a tiled corridor

Write A=ab, B=b², with a>b>0. The previously established sufficient
F3 remainder is

```
H=[(2A,−2A),(A,−A),(A+B,−A),(A+B,0),(B,A),(2A,A)]
```

in Eisenstein coordinates. It is the interior-disjoint union of

```
E1=[(2A,−2A),(A,−A),(2A,−A)],
E2=[(A+B,0),(B,A),(A+B,A)],
P=[A+B,2A]×[−A,A].
```

Both E1 and E2 are equilateral triangles of side A. The three horizontal
cross-section formulas in the earlier fan proof verify this partition
directly: E1 fills the bottom section, E2 fills the left part of the top
section, and P fills the right parts of the middle and top sections.

The 60-degree parallelogram P has sides A−B=b(a−b) and 2A=2ab. Split its
first side into a−b intervals of length b and its second into 2b intervals
of length a. Each cell splits into two original 120-degree tiles. Thus P
uses exactly 4b(a−b) tiles.

Consequently, **a tiling of an equilateral triangle of side ab by the
original tile is sufficient for this F3 construction**: use two copies
and the displayed pure corridor. The equilateral count would be ab,
so the total is

```
2ab+4b(a−b)=2b(3a−2b).
```

No such minimum-scale equilateral tiling is asserted to exist. Known
larger equilateral seeds cannot simply be placed inside these two
triangles. Nor is the implication reversed: an arbitrary filling of H
may cross all three displayed regions.

## 2. The proposed small formal inventory

Use rho=exp(i*pi/3), Z=a+b*rho, and z=Z/c. The direct tile P has CCW
vertices `[0,a,Z]`; the reflected tile Q has vertices `[0,conjugate(Z),a]`.
Let P_j be P rotated by rho^j, and let Q_j be Q first rotated by z and
then rho^j. A formal boundary identity supplies these positive counts:

```
b copies P_3,
a−b copies P_4,
a copies P_2,
c copies Q_1,
c copies Q_5.
```

Its total is 2(a+c). This is an orientation inventory, not a placement.
At the directions of height one the cancellations require:

```
P_3 long c-edges against Q_1 short b-edges, along z;
P_2 long c-edges against Q_5 short a-edges, along rho^5*z;
P_4 long c-edges and Q_5 short b-edges against Q_1 short a-edges,
along rho*z.
```

These identities retain lengths and orientations but do not specify
which parallel supporting line contains an edge.

## 3. Why one straight bc seam cannot realize this inventory

Suppose all b long edges of P_3 are concatenated into one straight seam
of length bc, and all c short b-edges of Q_1 cover its opposite side.
After translation, their intervals must be exactly

```
[j*b*z,(j+1)*b*z],   j=0,...,c−1.
```

The corresponding Q_1 short a-edge goes from `j*b*z` to
`j*b*z−a*rho*z`. These c edges lie on c distinct lines parallel to
rho*z, because the displacement between any two initial points is a
nonzero multiple of z, not rho*z. There is therefore at most one
oppositely oriented Q_1 edge, of length a, on each such line.

But every P_4 long edge has length c and direction rho*z. In this exact
inventory the only opposite-direction contribution on its supporting
line can come from those Q_1 a-edges; Q_5 b-edges have the same sign as
P_4. Since c>a and there is at least one P_4 tile (`a−b>0`), its length-c
edge cannot cancel against the available length at most a.

This is a positioned-current contradiction. Thus the formal inventory
cannot be realized by this single-straight-seam arrangement. It does not
exclude branching staircases, several separate bc-direction seams,
additional opposite-orientation pairs, or any arbitrary filling of H.
