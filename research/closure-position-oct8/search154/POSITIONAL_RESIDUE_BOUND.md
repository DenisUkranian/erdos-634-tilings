# A lower bound on the number of future tiles from affine-line residues

8 October 2026. A proved necessary completion bound. It is **not enabled**
in the recorded 600-second search, and does not exclude 154 by itself.

Consider a nonoverlapping partial placement of the `(8,7,13)` tile in
the canonical target `(0,0),(154,0),(49,56)`. Assign every complete
short-edge supporting line its height h and its unoriented direction
family. There are three such families for each h. Choose a consistent
orientation on each family and integrate oriented lengths over each
**complete affine line**, keeping separate parallel lines separate.

Let S(l) be the signed sum of the already placed short edges on line l.
Let b(l) be the corresponding oriented integral of the target boundary.
Modulo 13 its only nonzero value is 11 on the height-zero exterior base,
or -11 if that family is oriented oppositely. The base must be included
even when no currently placed edge lies on it. Both target equal sides
have length 91 and contribute zero modulo 13.

All complete long edges have length 13, so they contribute zero to
these line integrals modulo 13, whether already placed or still to be
placed. Splitting edges at T-junctions does not alter the whole-line
integral. Thus, on every line l, future short edges at the same height
must supply the residue

    r(l) = b(l)-S(l) modulo 13.

Their individual signed contributions belong to `{7,-7,8,-8}`. Let d(r)
be the shortest path length from 0 to r in the Cayley graph of Z/13Z
with these four increments. In residues 0 through 12 the values are

    d = (0,2,2,2,3,1,1,1,1,3,2,2,2).

This deliberately permits signs and lengths without testing their
geometric availability; it is a relaxation, so it can only underestimate
the number of future short edges required on a line.

For height h sum d(r(l)) over each of its three direction families,
giving D(h,0), D(h,1), D(h,2). Every future tile at height h has exactly
two short edges on two different direction families. Therefore the
number of future tiles at that height is at least

    R_h = max(ceil((D(h,0)+D(h,1)+D(h,2))/2),
              D(h,0), D(h,1), D(h,2)).

It suffices to include the exterior base and the lines of the currently
placed short edges. A future tile on an unlisted line cannot repair a
residue on a listed parallel line. Ignoring those additional lines
only weakens the bound.

If k_h tiles at height h are already placed, every completion satisfies
`n_h >= k_h+R_h`. This can be combined with the existing inventory and
population bounds by taking their **maximum**, then enforcing the known
residue and parity conditions. It must not be added to a separate lower
bound that may count the same future tiles.

The geometry and the max/sum counting step received a separate internal
review by the central-height audit agent. This is not external refereeing.
The implementation in `check_line_residue_bound.py` is a standalone
positive-control check, not a new pruning rule in the recorded search.

## General form

The same proof applies to a primitive integral 120-degree tile `(a,b,c)`
with `c*c=a*a+a*b+b*b`. Replace modulus 13 by c and the four Cayley-graph
increments by `{a,-a,b,-b}`; retain the actual target-boundary integral
on every relevant line. Primitivity gives `gcd(a,b,c)=1`, so the residue
graph is connected. Long-edge contributions still vanish modulo c, and
each tile still has two short edges in distinct direction families.
The identical maximum formula is therefore a general necessary
position-sensitive completion bound. It is not a sufficiency criterion
or a classification of admissible tile counts.
