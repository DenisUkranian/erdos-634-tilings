# Independent audit of the new parallelogram bridge

29 September 2026. Symbolic proof checked independently of the generator.
No mathematical error found. Novelty relative to the full literature has
not been established.

Let 0<e<f be coprime integers and put a=ef, b=f²−e², c=f²,
N0=3f²−e², Y=eN0 and X=f³. Use oblique coordinates in the physical
unit-vector basis (1,exp(i beta)); its metric is

    |(x,y)|²=x²+y²+2xy cos(beta),
    2ac cos(beta)=a²+c²−b².

For positive integers p,q with e|q and q≤2p, the parallelogram

    P(p,q)=[0,pY] × [0,qX]

is tiled by 2pqN0 congruent copies of the primitive tile (a,b,c).

Write H=qf, J=2pf and s=peb. Then pY=Ja+s and qX=Hc. The two lines

    x/a+y/c=H and x/a+y/c=H+s/a

partition the box into exactly three regions:

1. A left triangle with vertices (0,0),(Ha,0),(0,Hc). The standard
   a-by-c triangular grid gives H² tiles.
2. A middle parallelogram with vertices (Ha,0),(Ha+s,0),(s,Hc),(0,Hc).
3. A right trapezoid with vertices (Ha+s,0),(Ja+s,0),(Ja+s,Hc),(s,Hc).
   Since J≥H, it is the J-by-H grid box shifted by s with its lower-left
   H-grid triangle removed. Its exact count is 2JH−H².

For the middle piece set U=(b,0), V=(-a²/b,ac/b). In the displayed
metric, |U|=b, |V|=a, |U+V|=c. Thus each grid cell on U,V splits along
its U+V diagonal into two genuine copies of the tile. Its macrovectors are

    (pe)U=(s,0), (qb/e)V=(-Ha,Hc).

Both repetition counts are positive integers. It uses 2pqb tiles. The
three regions have disjoint interiors and exhaust the entire box, so the
total is H²+(2JH−H²)+2pqb=2pqN0.

Stacking q/e copies of P(p,e) proves the stronger sufficient condition

    e|q and p≥ceil(e/2).

## Exact additive gluing

Write T_r={(x,y):x≥0,y≥0,x/Y+y/X≤r}. Its physical sides are rX,rX,rY.
If T_p and T_q already have tilings, append the bridge P(p,q) in the
lower left, T_p translated by (0,qX), and T_q translated by (pY,0).
These three regions exhaust T_{p+q} with disjoint interiors. Their
tile counts sum to (p²+2pq+q²)N0.

No extra reflection or rotation assumption is needed: the two triangle
pieces are simple translates of the known triangles. T-junctions along
the glued boundaries are allowed.

## Limits of the conclusion

This is a constructive sufficient condition, not a necessary divisibility
condition on triangle scales. It does not revive the false lemma f|t.
It supplies a closure rule on already realized scales. In particular it
cannot create a new residue class from seeds all sharing the same common
factor; a new seed outside that factor needs a separate construction.

The six recorded exact computational cases in
`verification/replay.json` agree with the theorem. The proof above
does not depend on finite testing.
