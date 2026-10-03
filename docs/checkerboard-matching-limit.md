# The limit of a parallelogram matching reduction

3 October 2026. Internal mathematical argument; not a solution of Erdős
634 or a nonexistence theorem for the triangular tilings considered here.

## A contact matching survives T-junctions

Suppose a polygon is dissected into congruent polygonal tiles of common
perimeter p. Suppose their faces have a black/white coloring such that
every positive-length contact joins opposite colors and every tile with
a positive-length exterior contact is black. Write B,W for the numbers
of tiles of each color.

There is an adjacency matching covering every white tile. Weight each
contact by its length divided by p. The weights sum to one at each
white tile and to at most one at each black tile. Thus every set S of
white tiles satisfies `|S|<=|neighbors(S)|`, and Hall's theorem applies.
Partial-edge contacts cause no difficulty.

Cancellation of the internal lengths also gives

```
perimeter(target) = (B-W)p.
```

Such a matching consequently leaves M=B-W black tiles unmatched. This
does not specify the geometry of any matched pair.

## Half-turn matching forces similarity

**Theorem.** Suppose the target and tiles are triangles and the preceding
coloring hypotheses hold. If every white tile can be paired injectively
with a black tile that is a translate of its half-turn, then the target
is similar to the tile. Adjacency of these pairs is not required.

Orient a polygon boundary counterclockwise. In each unoriented line
direction, choose one orientation and sum edge lengths with the
corresponding sign. Regard these as independent formal coordinates of a
signed-direction signature. Splitting edges at T-junctions shows that
this signature is additive under dissection. Its l1 norm is bounded by
the perimeter, with equality for every nondegenerate triangle, whose
three edge directions are distinct.

A half-turn negates this signature, so the paired signatures cancel.
The remaining M black triangles have total signature equal to that of
the target. But

```
||signature(target)||_1 = perimeter(target) = Mp
```

is also the sum of their individual signature norms. Equality in the
triangle inequality forbids any cancellation. A direction absent from
the target cannot occur in a remaining tile. Thus each remaining tile
has its three sides parallel to the target's three sides; the triangles
are similar. This proves the theorem.

In particular, for a non-similar target it is impossible to cover all
white tiles by black/white pairs whose union is a parallelogram. This
continues to hold after another tiling of the same target if the
coloring hypotheses continue to hold. Kites, partial-edge pairs and
decompositions leaving tiles of both colors are not ruled out.

## Application to the Group-1 beta and alpha targets

For the irrational-angle tile satisfying `3alpha+2beta=pi`, write
`gamma=2alpha+beta`. A genuine interior vertex has an even number of
incident tile corners: solving the angle equation gives counts
`(6-2r,4-r,r)` for alpha,beta,gamma. A T-junction has either the
three-corner fan `(1,1,1)` or the five-corner fan `(3,2,0)` opposite
its straight-through tile, so its graph degree is four or six. A
straight outer-boundary junction also has degree four or six.

The beta target has corner inventories beta, beta, three alpha, giving
boundary graph degrees two,two,four. The alpha-isosceles target has
inventories alpha, alpha, one alpha plus two beta, with the same
degrees. The planar boundary graph is therefore Eulerian in both
cases. Its faces admit a checkerboard coloring; choosing the exterior
white makes all boundary tiles black. Neither target is similar to
the tile, so the half-turn matching reduction is impossible.

For example, the beta target's perimeter ratio is `M=t(u+v)`, since

```
2v³+u(3v²-u²)=(u+v)(uv+2v²-u²).
```

The contact matching exists, but it cannot turn all the other triangles
into parallelogram pairs. A successful global reduction would have to
retain additional geometry beyond this pairing rule.
