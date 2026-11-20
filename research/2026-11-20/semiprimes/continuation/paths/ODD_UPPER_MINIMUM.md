# Closed-form odd upper-path minimum for the residual F2 family

This is a necessary bound on the original triangle with any tile
directions and T-junctions. It is exactly sharp on signed direction
inventories, before checking their order, area, containment, or completion.

Use the notation of `UPPER_RIGIDITY.md`. Take coprime $u$ even,
$v$ odd, and $g=\gcd(3,u-v)$. The proof needs
$u\ge6v$ and $u>v^2+3v$, both satisfied by every residual odd
unit-staircase parameter (even the exceptional staircase residual
bound $u>4v(v-1)$ suffices for $v\ge3$).
Set
$$ F=(u-v)/g,\quad D=(2u+v)/g,\quad A=(u+2v)/g,\quad K=a+b. $$
The minimum odd length among all net words with the correct
displacement and two polygon boundary characters is
$$
 K+vF+
 \begin{cases}
 2v(v+1)&g=1,\\
 2v\lceil v/3\rceil&g=3,\ v>1,\\
 2F&g=3,\ v=1 .
 \end{cases}
$$
The last line equals $K+3F$. Every upper median path in a completed
tiling obeys this bound if its length is odd. The even minimum is
$K$, with the unique geometrical equality case in the preceding note.

**Reduction to two small parameters.** The claimed minimum is at most
$K+2b<2d+c$, since $(a+c)/b=u/v\ge6$. This is clear from
$b=vD$ in each of the three lines; in the first two lines the excess
is at most $b$. It suffices to examine odd $L$ below $2d+c$. The
height-alternating character gives $J_1-J_2=-c$. Hence, in terms of
the signed middle and upper $\rho$ counts $B_1,B_2$ and displacement
parameter $t$ of `UPPER_RIGIDITY.md`,
$$ (2u+v)(t+F)=3(B_1-B_2). $$
Since $\gcd(2u+v,3)=g$, there is an integer $r$ with
$t=-F+3r/g$, $B_1-B_2=Dr$. Write
$R=L-K$ and $C=R+vt$ for the first-coordinate projection deficit.
Thus
$$
 R-vF\ge D|r|-3vr/g\ge 2F|r|.
$$
If $r\ne0$ this already gives an excess of at least $2F$ over
$K+vF$. For both nonexceptional lines $2F\ge 2v n_0$, where
$n_0=v+1$ for $g=1$ and $n_0=\lceil v/3\rceil$ for $g=3$.
This follows from $u>v^2+3v$.

If $r=0$, then $t=-F$, $B_1=B_2=B$ and $C=R-vF$.
Write $x=-uF+Dj$, $m=x+y=F(j+v)$ as in the displacement equations.
The full sum of the two characters is
$d-3vt-6vj/g-3(B_1+B_2)$. Its congruence gives
$2(vj+gB)\equiv v(u-v)\equiv-2v^2\pmod{v(u+v)}$.
The modulus is odd, so $B=vn$ for an integer $n$ and
$$ j\equiv-v-gn\pmod{u+v}. $$
We always have $C\ge2v|n|$. Also $X+Y=A(u-v-j)$ and
$y=-b+A(u-j)$ by the displacement equations.

**Lower bound in the first two lines.** Suppose $C<2v n_0$.
Then $|n|\le n_0-1$ and either $j\le-v-gn$ or $j\ge u-gn$.
In the first case $j\le0$, which gives $x\le-uF$ and $C\ge-x>2v n_0$.
In the second case the signed middle $E$-axis count is
$$ e_M=X+Y-vn\le (u+v)n-vA.$$
Each negative $E$ count costs two units of projection deficit, in
addition to the contribution $2v|n|$ from the two $\rho$ axes.
It follows that
$$ C/2\ge v|n|+vA-(u+v)n\ge vA-u(n_0-1)\ge v n_0. $$
For $g=1$ the penultimate expression is $2v^2$.
For $g=3$, put $s=v\bmod 3\in\{1,2\}$: it is
$(su+2v^2)/3\ge v(v+3-s)/3$. This contradicts the supposition.

**Lower bound at $g=3,v=1$.** Here $u=3F+1$, $A=F+1$, $b=2F+1$.
It remains to rule out $C<2F$ at $r=0$. Put $k_0=u-j$, so
$k_0\equiv3n\pmod{3F+2}$. Write $w=(F+1)k_0-n$.
The signed middle $E$ count is $w-(F+1)$ and the signed upper
$\rho^2$ count is $w-(2F+1)$: the latter equals $y-B$.
A positive $\rho^2$ count costs two units of projection deficit.
Thus
$$ C/2\ge |n|+\operatorname{dist}(w,[F+1,2F+1]). $$
If this were smaller than $F$, then $|n|<F$ and
$1+|n|<w<3F+1-|n|$. Since $w+n=(F+1)k_0$ this requires
$k_0=1$ or $2$. Neither is a multiple of 3 modulo $3F+2$ with
multiplier $|n|<F$: $|3n|\le3F-3$ whereas the nearest representatives
on the negative side are $-3F-1,-3F$. This proves $C\ge2F$.

**Sharpness on signed inventories.** At $r=0$ take $j=u-gn$.
In the three unoriented axes $1,\rho,\rho^2$, the signed counts of
the middle and upper alphabets respectively are
$$
 ((u+v)n-vA,\ vn,\ -b-un),\qquad
 (a-un,\ vn,\ -b+(u+v)n).
$$
Their displacements and boundary characters are exactly the ones
specified above by substitution. At $g=1,v\ge3$ choose $n=v+1$,
and at $g=3,v>1$ choose $n=\lceil v/3\rceil$. Then both $E$
counts are nonnegative and both $\rho^2$ counts are nonpositive,
so the actual first-coordinate deficit is $2vn$, as required.
For $g=3$ write $3n=v+s$, $s=1$ or 2: the two decisive sign tests
are $s(u+v)-v^2\ge0$ and $s(u+v)-uv\le0$, using $v\ge5$.
At $g=v=1$ instead take $n=1$: the middle $E$ count is $-1$ and
the total deficit is $4$.

Finally at $g=3,v=1$ take the signed counts
$(F,0,-F)$ and $(a,-b,-F)$. Here $a=3F^2+2F$,
$c=3F^2+3F+1$, $b=2F+1$. The upper net vector is
$(a+F,-b-F)$, giving $t=1-F$ and middle vector $(2F,-F)$
as required. The two characters are $J_1=0$, $J_2=c$, which satisfy
both polygon congruences. The word length is $K+3F$. Signed counts
are realized as abstract words by using each specified unoriented
axis in the sign indicated, in any order. This completes the net
minimum proof.

The first controls have odd upper-path minimum at least $49$
($a,b,c=33,7,37$) and $57$ ($35,13,43$). Exhaustive integer
checks for ten primitive controls are in `check_upper_odd.py`.
