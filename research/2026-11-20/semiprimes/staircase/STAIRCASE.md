# A variable staircase for primitive F2 tilings

Denote by F2 the triangle with sides a(a+2b), b(2a+b), c² where a>b>0 and c²=a²+ab+b². Its angles are twice the two acute tile angles and 60°. This note gives a constructive sufficient theorem for an actual tiling. Coordinates and all length and overlap checks in the certificates are exact. Reflections and partial side contacts are allowed.

## The step test

Suppose a,b,c are primitive. They are then pairwise coprime. Suppose there are finitely many integer steps (r_i,s_i) with

1. 0<r_i≤b, 0<s_i≤a.
2. t_i=(a r_i−b s_i)/c is a nonnegative integer.
3. Σr_i=c−b and Σs_i=c−a.

Then F2 is tiled by exactly (a+2b)(2a+b) congruent (a,b,c) triangles. Any positive integer dilation is tiled by subdivision. Each test instance is a finite bounded integer sum; the order of its steps may be chosen arbitrarily.

In developing this theorem we used Herdt's 143-tile geometry as pictured in Bonfioli's [143-tiling](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/tiling143.pdf). Bonfioli had already used a lift tool to solve equations for lattice piece sizes and reported nine F2 examples in the [v6 companion, Section 2](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_companion.tex). Our use of any number of steps and the stated arithmetic partition criterion are deductions here. No priority or outside review is claimed.

## Construction and proof

Write (x,y) for x+y exp(iπ/3). Orient the F2 board as O=(0,0), H=(b(2a+b),0), V=(0,a(a+2b)). Define four vectors

    u = (b(a+b), −ab)/c,       v = (ab, −a(a+b))/c,
    w = (a², ab)/c,           z = (ab, b²)/c.

Then u+w=(c,0), z−v=(0,c), b w=a z, and H−V=c(u+v). Their lengths, in order, are b,a,a,b. The vectors u+v, u+w and z−v all have length c.

A grid triangle with unit edge vectors E,F at its first vertex and integer scale n has corners (0,nE,nF). If E,F,E−F have the three desired lengths it tiles in the usual n²-grid. Its subregion with E-coordinate between 0 and k is a trapezoid for 0<k<n, or the whole triangle for k=n. This is tiled exactly by cutting out the grid triangle of scale n−k from its nE corner. We call this region the k-band of the n-grid in (E,F).

Start at P₀=H−b(c,0). For each step set

    d_i = r_i c−t_i a,      h_i = s_i c+t_i b,
    P_{i+1}=P_i+(-d_i,h_i).

The short-side congruences give b∣d_i and a∣h_i. In detail c d_i=b[r_i(a+b)+a s_i], c h_i=a[s_i(a+b)+b r_i]. All d_i,h_i are positive. The step sums give Σt_i=a−b, P_m=V−a(0,c), and every P_i has nonnegative coordinates. Set r_{−1}=b and s_m=a.

Place the following regions for each i=0,…,m:

- The **horizontal band** at P_i is the r_{i−1}-band of the b-grid with E=(c,0), F=w. It reaches T_i=P_i+bw.
- The **vertical band** at P_i is the s_i-band of the a-grid with E=(0,c), F=z. It shares the segment P_i T_i and reaches T_i−s_i v.

For each i<m also put an axis-parallel parallelogram from the horizontal coordinate axis x=0 up to x=P_i.x, between y=P_i.y and y=P_{i+1}.y. Its side lengths in those coordinate directions are respectively multiples of b and a, so it is an array of b-by-a cells, split along their sum diagonal. Fill the small triangle with vertices

    X_i=P_i+(0,s_i c),    Y_i=X_i+(0,t_i b),
    Z_i=X_i+t_i(a,b).

This is a tile-similar grid of scale t_i, omitted if t_i=0. It adjoins the right side of the preceding parallelogram and has upper side Y_i Z_i on the horizontal through P_{i+1}. The point Z_i=P_{i+1}+(r_i c,0) is the next horizontal band's right endpoint on that line.

For completeness the joints are as follows. The vector difference gives

    T_{i+1}=T_i−s_i v−r_i u.

The vertical band ends on the line from X_i to T_i−s_i v, in the direction of z. The small triangle uses X_i Z_i on that line. The next horizontal band uses the remainder Z_i to T_i−s_i v, of vector (b−r_i)w. Nonnegativity of t_i and b−r_i puts Z_i on that segment. Along the horizontal through P_{i+1}, the next parallelogram and the next horizontal band match the previous parallelogram followed by Y_i Z_i. At the first and last bands the outside horizontal and vertical intervals are exactly OH and OV.

It remains to describe the band along HV. In coordinates H−Uu−V'v it lies between the diagonal U=V' from (0,0) to (c,c) and the axis staircase that advances b in U, then s₀ in V', then r₀ in U, and so on, ending with a in V'. This is precisely the outer boundary of the bands described above. Each partial sum of the nonterminal vertical advances is at most c−a<b. Thus the staircase stays on the side U≥V' up to the last vertical leg, where U=c. The region is a union of whole lattice cells or their diagonal halves, with triangle sides u,v,u+v of the required lengths. One explicit dissection uses a grid triangle and a rectangle for each horizontal slice between successive attained V' coordinates.

These oriented pieces give a tiling even when some boundary vertices meet other edges partway. One way to see this exactly is by directed boundary cancellation. All the polygons above have their interiors on the indicated side of their oriented edges, with the bands positive because 0<r_{i−1}≤b and 0<s_i≤a. The shared segments listed above cancel, leaving the boundary of OHV. For a generic point the winding numbers add, so the count of positive polygon interiors equals the board indicator. The polygons are closed and finite in number, which gives coverage everywhere and disjoint interiors. Finally the area ratio relative to a tile is b(2a+b) a(a+2b)/(ab)=(2a+b)(a+2b).

## Reproduction

Run `python3 staircase.py` to write the three earlier close-prime exceptions as grid certificates, and `python3 check_staircase.py` to verify all included certificates. The independent checker uses exact Eisenstein norm comparisons for each cell, convex containment, an integer separating-axis test for every pair of macroregions, and exact areas. It imports no constructor. The three old exceptions passed with 27, 59, 59 regions for N=2,732,927, 70,696,487, 340,235,759 respectively. The three additional examples below one million all use 51 grid regions.

The step list at (a,b,c)=(5,3,7) consists of (2,1) twice and recovers the source 143 configuration. At (33,7,37), the only nonzero eligible step with s≤4 is (4,3), which cannot sum to (30,4). This establishes the limitation of the step test without excluding a tiling by a different layout.

## A whole thin family missed by the staircase

For k≥2 let a=k(3k+2), b=2k+1, c=3k(k+1)+1. This is the potentially difficult F2 shape on the same tile family as the isosceles obstruction. Every nonzero step has 0<s≤c−a=k+1. Because a=c−k−1, the load identity gives

    (k+1)r + (2k+1)s = c(r−t).

Its left side is positive and at most 2(k+1)(2k+1)<2c. It therefore equals c. Reducing modulo k+1 gives s=k, and then r=k+1. Copies of this step cannot sum to a vertical total k+1. This disproves the staircase condition on every such shape; a different proof or geometric construction would be needed to decide the corresponding F2 instances.

The obstruction cannot be removed just by varying the widths of the two uniform grid bands while keeping their common tip and the left fill. At any aligned pair of bands, the full horizontal and vertical scaffolds must have scale Lb and La for some integer L≥0, since they end on the same interior ray made of sides of lengths a and b. Initially L=1. At a transition from L to L' with right-bank step (r,s), put r'=r+b(L−L'). The triangle/rectangle identities become ar'−bs=ct≥0, d=rc−ta, h=sc+tb. If L' increases, r=r'+b(L'−L) and d≥bc, because r'c−ta≥0. But the initial rightmost available integral coordinate is b(2a+b−c)<bc since 2a+b<2c, and it cannot increase as long as L stays equal to one. Thus no first increase can fit. A transition from L=1 to L'=0 forces r=0 and c dividing b(a−s), whence s=a; this exceeds the available total c−a. These facts concern only this same axial geometry and upper scaffolds.
