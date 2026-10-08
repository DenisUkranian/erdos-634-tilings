# Every closed subcone below 1+sqrt(2) has only a finite arithmetic remainder

8 October 2026. A further consequence of the new mixed-corner construction.

**Theorem.** Fix a real number R with2<R<1+sqrt(2), and put

    delta=1+2R−R²>0.

Every primitive integral120-degree tile with

    2<a/b<=R,          b>=169/delta²

has a scale-one ordered F3 tiling. Hence it has such a tiling at every
positive integer multiplier. Below this explicit bound there are only
finitely many primitive tiles in the cone; the construction's arithmetic
criterion can be evaluated exactly for each.

**Proof.** Write d=b²+2ab−a²−c. Since r=a/b<1+sqrt(2)<5/2, one has c/b<4
and consequently

    d>delta*b²−4b.                                     (1)

In the normalized parameters of the exact Apéry theorem, p<2sqrt(b).
Indeed, if a0=a, then t=p/q=r+c/b<6 and
p²/b=t²/(2t+1)<36/13<4. Here c/b<13/4 follows from r<5/2, so r+c/b<23/4<6.
If a0=b, then t=(1+c/b)/r>1+1/r>7/5 and
p²/b=t²/(t²−1)<49/24<4. The exact Frobenius formula therefore yields

    F<p(b0+c)<12*b^(3/2).                              (2)

Because0<delta<1, the assumed size bound gives

    delta*sqrt(b)−4/sqrt(b)>=13−4delta/13>12.

Thus(1) exceeds(2), so d lies in<a,b,c>. The mixed-corner theorem applies
to D=c+d. QED.

This result concerns primitive tile size while keeping multiplier one.
It is different from the existing eventual-scale statement for one fixed
tile. It does not cover a/b>=1+sqrt(2), and does not classify the finite
exceptions to this construction in an arbitrary chosen cone. The sharper
[F3 uniform-cone theorem](F3_UNIFORM_CONE.md) removes the finite remainder
entirely through the exact endpoint2725/1139.
