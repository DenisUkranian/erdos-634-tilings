# Final F3 geometry audit and a small macro-recipe obstruction

7 October 2026. This investigation does **not** settle 4830, the remaining
ordered F3 sector, or Erdős 634.

## The smaller sufficient target

For `a>b>0`, `c²=a²+ab+b²`, put `n=a-b` and work in Eisenstein
coordinates `(x,y) -> x+y exp(i*pi/3)`. The convex quadrilateral

```
Q = [(an,0), (c²,0), (a²,ab), (an,bn)]
```
needs exactly `3ab` original tiles. It is the c-fold original triangle
with the reflected n-fold corner removed. Its successive side lengths are

```
b(2a+b), bc, bc, b(a-b).
```
The existing reflected-corner attachments in
[`BALANCED_F4.md`](../../group2-trapezoids/BALANCED_F4.md) show that any
filling of Q supplies reversed F4, F2, and both ordered F3 targets.
This is a sufficient route only; no necessity is asserted.

For `(a,b,c)=(24,11,31)` this reduces a positive attack on 4830 to

```
Q=[(312,0),(961,0),(576,264),(312,143)],
count=792, boundary lengths=(649,341,341,143).
```
The resulting counts would be F4=2065, F2=2714 and F3=4830. These
attachments were already established; the present work does not claim
this reduction as new.

## A rigorous obstruction to at most four ordinary grid pieces

The [stronger theorem](FOUR_PIECE_OBSTRUCTION.md) extends this obstruction
to every integer multiplier and to at most four similar pieces of arbitrary
positive real sizes, by a rationalization argument.

**Proposition.** Suppose the norm triple is primitive, `a>b`, and a is
even. Then Q cannot be partitioned into at most four integer-scaled
copies of the original triangle, each to be filled by its ordinary
triangular grid. Reflections and T-junctions between macrotriangles are
allowed.

Primitivity makes b and c odd. Reduction of the norm identity modulo 8
gives `a(a+b)=0 (mod 8)`. As a+b is odd, `8|a`. Consequently Q has tile
area `3ab=0 (mod 8)`, and all four of its boundary lengths above are odd.

If the proposed grid scales are `k_1,...,k_r`, `r<=4`, area gives
`sum k_i²=3ab`. A sum of at most four squares divisible by 8 must have
all its summands' bases even: squares have residues 0,1,4, and if any
base is odd then the number of odd bases is 1,2,3 or 4; none gives total
0 modulo 8 after adding the remaining even-square residues. Hence all
macrotriangle sides have even integer lengths. Each convex exterior
side of Q is a concatenation of whole macrotriangle sides, and therefore
has even length, contradicting its odd length. This proves the
proposition.

This is a restricted recipe obstruction, not an obstruction to a unit
tiling. In particular it rules out the tempting identities expressing
792 as three or four squares as sources of a direct grid dissection.

## Exact exploratory search

`probe_beta_quad.py` applies the previously available exact
advancing-corner search to Q. It additionally rejects any exposed segment
on an original convex exterior side whose length is outside
`<11,24,31>`. This is a necessary condition because such a segment must
be covered by whole original tile sides. The search permits reflections
and T-junctions and restricts each piece to an integer-scaled original
tile.

The retained five-macro search exhausted its search tree: 3961 nodes,
maximum four placed macrotriangles, in approximately 25 seconds. This is
an **exploratory search-engine report**, without a separately audited
exhaustion certificate. It is not promoted to an independently certified
nonexistence theorem for five macros, and certainly not for arbitrary
4830-tilings. The elementary four-macro proposition above has its own
written proof and does not rely on this computation.

The eight-macro probe stopped after 120 seconds, 10161 nodes and a maximum
of seven placed macrotriangles, with status `INCOMPLETE`. Neither run
found a positive tiling certificate.

Replay from the repository root (reports are printed unless an explicit
`--output` path is supplied):

```bash
python research/final-synthesis-oct7/f3/probe_beta_quad.py
python research/final-synthesis-oct7/f3/probe_beta_quad.py --max-macros 8 --seconds 120
```

The other positive reductions were checked for false shortcuts:

* The five-region F3 partition is geometrically positive for all a,b,
  but for a>2b its F4(a,b) region is the unresolved orientation. In the
  case (24,11,31), its ideal trapezoid already has a valid filling;
  the unresolved region is specifically the F4 triangle.
* The good F4(b,a) corner leaves a convex quadrilateral needing 3220
  tiles. Its short side 70 has the permitted inventory 24,24,11,11,
  and these four boundary tiles fit geometrically. Thus that short
  side does not provide a new obstruction.
* The fan hexagon needs 1100 tiles. Its four 60-degree corners bound
  an incident triangular grid scale by 13,18,13,8, respectively.
  Thus the numerical identity 1100=31²+11²+3²+3² does not furnish a
  four-grid filling: the 31-grid cannot serve any corner, leaving
  insufficient pieces to supply the two acute tile angles at each
  of four 60-degree corners. This observation is supplementary, not
  a classification of all hexagon fillers.

The remaining obligation is a positive fill of one of these sufficient
regions, a different full F3 construction, or an obstruction covering
arbitrary tilings. None has been established here.
