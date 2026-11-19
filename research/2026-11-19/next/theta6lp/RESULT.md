# An exact endpoint obstruction for the 180-tile theta triangle

Take the tile with sides \((6,5,9)\). In coordinates \(x+i\sqrt2y\), the outer vertices are \((0,0),(60,0),(30,60)\). This is the specific triangle with sides \(90,90,60\) and an area equal to 180 tiles. The unrestricted orientation-height reduction and subsequent exact placement enumeration supply a pool of 146,434 possible placements. Its integer coordinates have denominator 729. The calculation below excludes every choice of 180 different placements from this pool.

For each point \(p\) and primitive unoriented line direction \(d\), choose an integer \(w(p,d)\). The sign convention takes the lexicographically positive of the two primitive vectors. Travelling counterclockwise around a triangle, score each directed side from \(p\) to \(q\) by \(w(p,d)-w(q,d)\). Write \(s(T)\) for the three-side sum. Splitting a straight side at any intermediate point preserves its score by telescoping. In a tiling the two traversals of every interior subsegment cancel. Thus the score of the board equals the sum of the scores of the selected tiles, including tilings with T-junctions.

For an integer \(m\) and any choice of 180 placements from the pool \(P\), its total score is at most

\[
180m+\sum_{T\in P}\max(0,s(T)-m).
\]

For the supplied [integer weights](d729-weights.tsv.gz), use \(m=1,000,000\). The outer score is 180,902,886. Exactly 19,810 of the 146,434 candidates exceed \(m\), with total excess 892,648. Therefore every candidate subset has a score at most 180,892,648, strictly below the board score by **10,238**. The standard-library verifier checks all tile lengths, orientation, containment, unique tagged placements, and the score calculation with exact Python integers.

Run from this directory:

```sh
python verify.py candidates.dat.gz d729-weights.tsv.gz
```

The uncompressed candidate file has SHA-256 `7e26641ac3db164d9cba1c1a38e7c7d075713d18132852e06e842e2dff0800a1`. Its shape file has SHA-256 `e4783058042b3ba66065c9361d57a9ae0404e062c52928755ee68fbd45b32483`. The candidate file and the independent [score verifier](verify.py) are included. The separate geometric reduction is required to infer full impossibility for this target. The conclusion for the 280-tile alpha triangle is the exclusion of every tiling with a complete straight vertex seam by the [seam equivalence](../alpha/VERTEX_SEAMS.md).

A simpler comparison uses only the maximum individual score, 1,001,552. Its product with 180 is 180,279,360, below the target 180,902,886. The 180 largest scores together give the still smaller bound 180,130,676. [Complete geometric reduction](../theta6/PROOF.md) · [Independent top-score check](../audit/theta6_top_scores.py).
