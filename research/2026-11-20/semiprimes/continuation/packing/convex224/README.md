# One convex quadrilateral sufficient for 5063

For the unit board with sides 1079, 1849 and 2135 and the tile with sides 13, 35 and 43, a tiling of the following single convex quadrilateral would give a complete 5063-tiling. Its area is 224 unit tiles. Whether the quadrilateral or the full board tiles is open in this record.

Use physical coordinates (x+yρ)/43 with ρ=exp(iπ/3). One copy of the quadrilateral has vertices (35217,0), (46397,0), (42081,8540), (35217,13545), in counterclockwise order. Its side lengths in that order are 260, 172, 143 and 315. The other copy is its exact translate by (−11180,13545) in these coordinates. A filling of either quadrilateral may thus be used verbatim in the other.

The certificate [placements.json.gz](placements.json.gz) contains every vertex of the 4615 intervening unit tiles, both holes and the original target. It was obtained by recombining placements from the two translated defects in the 5059 packing. This first leaves two identical, concave 345-tile quadrilaterals. In each one, a straight cut from the reflex vertex removes the standard 11-by-11 triangular grid and leaves the stated convex target. The final coordinates suffice to verify the implication independently of the construction history.

Run `python3 verify.py`. The checker verifies the squared edge lengths of every tile, the area and strict convexity of each hole, the translation vector and all signed boundary intervals. Subdividing an oriented segment does not change its endpoint differences on that line. Zero difference on every supporting line therefore gives equality of the polygonal boundary chains, allowing arbitrary T-junctions. By the winding number about any point off all edges, the multiplicity of the positive cells is one inside the board and zero outside. This proves containment, disjoint interiors and coverage simultaneously.

For computations with the 224-cell, rotate or reflect it so its counterclockwise edges (length, height, phase) read (143,0,0), (172,−1,1), (260,1,2), (315,1,4). A direction of height h and phase j means zʰρʲ with z=(35+13ρ)/43. The association with the coordinate certificate is up to rigid motion and cyclic change of starting edge.

Research record, 20 November 2026. Prepared with AI assistance for the Denis Paliy project. The metric certificate has an integer replay. Independent refereeing is outstanding.
