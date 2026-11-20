# A global dichotomy for the two phase trees

21 November 2026. This note classifies the entire class having no occupied
exterior-free short node in either prime tree. The result concerns full
tilings and arbitrary permitted tile heights and translations. It is not
an additional finite-catalogue assumption. Neither target is excluded by
the classification alone.

## 1. Frame and established inputs

Let

\[
 R=\mathbb Z[\rho],\quad \rho=e^{i\pi/3},\quad
 z=(a+b\rho)/c,\quad
 A=b(2a+b),\quad B=a(a+2b).
\]

The board is the triangle with vertices `0,A,B*rho`. Its two axial
outer sides have physical height zero; the other outer side has
physical height two and starts at `A`.

The triples are `(33,7,37)` and `(35,13,43)`. The exact control
`(5,3,7)` also satisfies the structural statement. In each case
`c` is prime and splits into two Eisenstein primes. Normalize their
valuations so

\[
 v_\pi(z)=1,\qquad v_{\bar\pi}(z)=-1,
 \qquad v_\pi(c)=v_{\bar\pi}(c)=1.
\]

We use the existing unrestricted vertex-lattice and phase-node
theorems: every tile vertex lies in `R[1/c]`, and a tile of short
height `h` has a short node in each tree. Equality of short nodes
at height `h` means, respectively,

\[
 v_\pi(q-q')\ge h,
 \qquad v_{\bar\pi}(q-q')\ge-h.                       \tag{1}
\]

In the first tree children increase physical height; in the second
they decrease it. A node is exterior-free if its descendant subtree
contains no outer edge node. An occupied node contains at least
one tile with that exact short node.

Within `R[1/c]`, the simultaneous conditions (1) describe one
Euclidean translate of `z^hR`: dividing a difference by `z^h`
makes it integral at both primes above `c`, and the vertex-lattice
theorem already supplies integrality at every other prime.

## 2. The exterior nodes form one chain in each tree

In the increasing-height tree, both axial outer sides have the
same node `e_0` at physical height zero, since their endpoints are
integral. The outer height-two side has node `e_2`, represented
by `A` at height two. Because `A` is integral, `e_2` is a descendant
of `e_0`. Therefore a node is not exterior-free precisely when it
is an ancestor of `e_2`, including `e_2` itself. Its physical height
satisfies `h<=2`, and its short-node membership condition is

\[
 v_\pi(q-A)\ge h.                                    \tag{2}
\]

In the decreasing-height tree, the same integrality says that the
outer height-two node is an ancestor of the height-zero core node.
Thus a node is not exterior-free precisely when it is an ancestor
of the core, including the core itself. Its physical height satisfies
`h>=0`, and its membership condition is

\[
 v_{\bar\pi}(q)\ge-h.                                \tag{3}
\]

These chain descriptions involve all ancestors, including arbitrarily
large negative or positive physical heights in the appropriate tree.
No truncation, no-gap theorem, or assumption of occupied intermediate
nodes has been used.

## 3. Exact simultaneous classification

**Two-tree exterior-spine theorem.** The following are equivalent
for a complete tiling:

1. Neither prime tree has an occupied exterior-free short node.
2. Every tile has one of the following three short-height/coset pairs:

| Short height | Obtuse vertex and all tile vertices |
|---:|---|
| 0 | `R` |
| 1 | `A+zR` |
| 2 | `A+z^2R` |

**Proof.** If (1) holds, each tile satisfies both (2) and (3).
Their height inequalities give `0<=h<=2`. At these heights `A`
satisfies `v_barpi(A)>=0>=-h`, so (3) is equivalent to
`v_barpi(q-A)>=-h`. The two valuation conditions therefore imply
`q-A in z^hR`. At height zero this is `q in R`, since `A in R`.
The two short edge vectors lie in `z^hR`, hence the other vertices
belong to the same translate.

Conversely, each listed coset satisfies (2) and (3), at a permitted
height. Both short nodes are consequently on their exterior chains,
so no occupied short node is exterior-free. This proves the equivalence.

In particular, every unrestricted tiling belongs to exactly one of
two exhaustive cases:

* At least one prime tree has an occupied exterior-free short node.
* All tiles belong to the three specified native cells.

The first case is where the previously proved bidirectional-cut and
charged-branch theorems apply. Those theorems must not be silently
used to assume that this first case occurs.

## 4. Consequences which retain the real geometry

The second case has exactly three permitted joint cells, rather than
arbitrary choices of one phase at each height. All its vertices lie
in `c^-2 R`; this follows directly from the denominators of `z` and
`z^2`. There are exactly 36 orientation templates: three short
heights, six rotations, and two hands. The long edges have heights
between -1 and 3, even though the short heights are only 0,1,2.

The phase `A+zR` is also `B*rho+zR`, because
`B*rho-A=c^2*rho*z^2` belongs to `zR`. Thus this classification
includes the middle cell of the earlier abstract axis-flow model;
it does not exclude that model by a different naming of its phase.

The classification leads to a finite **necessary and sufficient**
endpoint model for this complete class, developed in
`NATIVE_ENDPOINT_COMPLETENESS.md`. That model retains actual vertex
coordinates and supporting-line endpoint currents. A nonnegative
integer solution of all its equations is a genuine positive tiling;
an abstract axis-current inventory is not such a solution.

The known complete 143 tiling lies in this class: its 38 height-zero
tiles belong to `R`, and its 105 height-one tiles belong to `A+zR`.
Thus the class cannot be excluded by a shape-independent theorem
that also covers that control without an additional target-specific
geometric hypothesis.
