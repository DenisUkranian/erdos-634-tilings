# A fifteen-region ordinary-grid proof of the 240-tile seed

8 October 2026. Denis Paliy, research with ChatGPT assistance.

The new side-60 equilateral tiling has a compact description: **15 convex
polygons**, each a union of ordinary triangular grid cells. No search
solver is needed to construct the pattern from this table.

Use Eisenstein coordinates. All physical vectors in the columns `o,u,v`
are divided by 7. The last column is an integer polygon in grid
coordinates: each vertex `(i,j)` denotes `(o+i u+j v)/7`.

| Region | Tiles | o | u | v | Integer grid polygon |
|---|---:|---|---|---|---|
| 1 | 12 | (252,105) | (21,0) | (-35,35) | (0,2), (0,0), (3,0), (3,2) |
| 2 | 35 | (385,0) | (-21,21) | (35,0) | (5,-5), (0,0), (0,1), (5,1) |
| 3 | 24 | (21,0) | (-21,0) | (0,35) | (1,0), (-1,0), (-1,7), (1,5) |
| 4 | 14 | (63,0) | (-21,0) | (0,35) | (1,0), (-6,0), (-7,1), (0,1) |
| 5 | 1 | (182,175) | (-21,21) | (35,0) | (0,-1), (-1,0), (0,0) |
| 6 | 16 | (238,0) | (9,15) | (-40,15) | (-1,1), (3,-3), (3,1) |
| 7 | 9 | (112,35) | (9,15) | (-40,15) | (-1,1), (2,-2), (2,1) |
| 8 | 9 | (154,105) | (9,15) | (-40,15) | (-1,1), (2,-2), (2,1) |
| 9 | 8 | (147,175) | (9,15) | (-40,15) | (0,1), (0,0), (2,-2), (2,1) |
| 10 | 35 | (57,25) | (-15,24) | (-15,-25) | (0,1), (0,-5), (5,-5), (5,-4) |
| 11 | 25 | (15,200) | (-15,24) | (-15,-25) | (0,1), (0,-4), (5,-4) |
| 12 | 9 | (203,154) | (-24,9) | (25,-40) | (4,0), (4,1), (-1,1), (0,0) |
| 13 | 25 | (196,224) | (-24,9) | (25,-40) | (4,-4), (4,1), (-1,1) |
| 14 | 10 | (210,35) | (-24,9) | (15,25) | (5,0), (0,0), (0,1), (5,1) |
| 15 | 8 | (116,205) | (-9,-15) | (-25,40) | (1,2), (1,0), (-1,0), (-1,2) |

![The fifteen convex grid polygons](figures/macro_240.svg)

In every row `Q(u)=441`, `Q(v)=1225`, `Q(u-v)=2401`, where
`Q(x,y)=x²+xy+y²`. Thus the elementary triangles in the grid have side
lengths 3,5,7. All polygon vertices are integer grid points, and all
polygon edges have constant i, constant j, or constant i+j. Hence the
ordinary triangular lattice subdivision fills the polygon exactly.
The stated number of tiles follows from its determinant area.

The 15 placed polygons are convex and contained in
`[(0,0),(420,0),(0,420)]/7`. Their interiors are pairwise disjoint, and
their total determinant area equals that of this equilateral target.
These finite exact facts prove that they form a partition. The counts
sum to

```
12+35+24+14+1+16+9+9+8+35+25+9+25+10+8 = 240.
```

The standard-library program `macro_240.py` reads only the 15-region
file `macro_grid_regions.json`, verifies all the above statements
(including all 105 macroregion pairs), and reconstructs the 240 unit
triangles. Its reconstructed triangle set is exactly the previously
independently verified seed. In particular the finite proof input can be
the small table above rather than the search result or 240 unrelated
coordinate triples.

Run `python macro_240.py` to produce the full unit certificate and
`macro_240_verified.json`. Run `python draw_macro_240.py` for the figure;
floating point is used for visual rendering only.
