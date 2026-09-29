# Changelog

## 0.1.0 — initial research snapshot, 29 September 2026

- Present the candidate classification of all prime tile counts in a complete manuscript, with the two new scale-one obstruction arguments, an exhaustive case table, the remaining branch calculations and explicit existence constructions.
- Present the two-piece construction for the rational target shape $(2\alpha,\alpha,2\beta)$ and the exact fixed-tile spectrum $k^2(2v^2-u^2)(3v^2-u^2)$.
- Include an explicit 322-tile construction of $(81,115,126)$ by copies of $(6,5,9)$, with complete coordinates and figures.
- Provide a separately implemented exact verifier for all 51,681 tile-pair intersections and subdivided edge cancellation, including T-junctions.
- Include additional exact construction certificates for 77 and 897 tiles.
- Establish eventual divisibility structure for the two remaining scale spectra, while leaving their general divisors and small exceptions undetermined.
- Record the known first-tile $W$ and $\beta$ spectra with attribution to Bonfioli and add a separate necessary-bound argument for the $\theta$-isosceles branch.
- Construct and separately verify theta examples with 147 and 243 tiles. Together with scale addition, these settle all fixed-tile $(2,3,4)$ counts $N=3t^2$, $t\ge4$, except possibly $N=75$.
- Include five exact theta certificates at counts 48, 108, 147, 243 and 300, and a separate exact replay of both odd-scale examples.
- Identify the 147-tile construction as a counterexample to the integrality/divisibility conclusion of Lemma 55 in Beeson v4; the prime-case candidate does not depend on that lemma.
- Include checked 45-tile and 57-tile boundary collars for the two $N=105$ equilateral candidates. These are partial placements, and do not settle either full tiling problem.
- Replay thirteen exact bridge examples and exercise ten verifier cases, including nine invalid-input rejection tests.
- Supply readable PDF notes and editable sources, an English and Russian overview, citation metadata, an authorship and assistance statement, and reproducibility instructions.
- Keep the full composite-count classification unresolved and document the remaining research frontier.
- Exclude historical upstream-derived code with unresolved redistribution terms from this curated current snapshot.

This entry describes the initial snapshot's contents. The dated research update below supersedes its then-open 75-tile instance. It is not a receipt that a separate remote GitHub release has been published. Previously published tags should not be silently retargeted.

## Research update — 29 September 2026

- Construct and separately verify the 75-tile theta example: target $(30,30,15)$ and tile $(2,3,4)$, with all 2,775 tile pairs checked exactly.
- Complete the fixed-tile theta spectrum: exactly $N=3t^2$ for every integer $t\ge4$, with no remaining exception at $t=5$.
- Add `data/theta-75.json`, bringing the theta certificate set to six examples; the separate odd-scale replay now checks 75, 147 and 243 tiles.
- Strengthen the necessary form in the rational theta branch to $N=bT^2$ for all primitive tiles, using two direction characters and parity, including nonsquarefree $b$.
- Establish the corresponding necessary form $N=b(b+c)K^2$ in the alpha-isosceles branch for every primitive tile.
- Give an explicit eventual construction bound for all five rational target shapes when $\Delta=b(a^2+b^2)-a^2c>0$. In particular, the eventual $W$ and beta scale divisors are $d=1$ in that range; the complementary range and small exceptions remained open at that stage (the later update below removes the range restriction for eventual existence).
- Check the eventual macrogeometry over 132 parameter pairs and the transfers over 199 parameter pairs using exact arithmetic, with the finite scope recorded separately from the universal proof.
- Record the smaller counterexample to Beeson v4 Lemma 55: $\mu=15/2$, $M=5$ in the 75-tile construction.
- Prove that the two previously constructed $N=105$ boundary collars cannot extend, by a four-placement obstruction at one inner corner in each. Include exact one-node refutations and a separate checker; this is not a global exclusion of 105.

This is a dated research update within the v0.1.0 snapshot. It does not assert that a new release tag exists, and it does not claim a complete solution of Erdős problem 634.

## Further research update — 29 September 2026

- Remove the $\Delta>0$ restriction from eventual existence for all five rational target shapes. Two annular dissections add $u$ and $v$ to theta scales; their coprimality gives all sufficiently large scales for every primitive tile.
- Prove both W/beta eventual divisors equal 1, with the explicit bound $v\lceil H_u/v\rceil+(u-1)(v-1)$. Give theta/alpha bounds and explicit seed scales for both signs of $\Delta$, making all five bounds computable from the tile parameters; seed existence is also supplied by Beeson v4, Corollary 5.
- Add exact finite macroregion checks for both annuli. These checks support the geometric formulas but are not a finite proof of the universal theorem.
- Add a compact exact refutation of the alpha21 instance: 391 certificate nodes, separately replayed as 437 expanded states and 158 dead ends. No lattice restriction, denominator cap, or edge-to-edge assumption is imposed.
- Complete the alpha spectrum for tile $(2,3,4)$, exactly $21t^2$ for $t\ge2$, and assemble the complete six-family classification for every triangular target tiled by this fixed tile.
- Give a global, composite-safe reduction of count 21 to that single refuted instance. Bonfioli and Harries had previously reported the exclusion; this is an independent checked reproduction, not a priority claim.
- Add a different 45-tile N105 collar with a separately admissible full fan at each of 18 convex inner corners. Include exact witnesses while leaving their joint compatibility, extendability, and global N105 unresolved.
- Add the universal annulus, explicit seed, alpha21, global21 arithmetic, and individual N105 fan checkers to the finite replay.

This update supersedes the earlier statement that the negative-$\Delta$ range remains unresolved for eventual existence. Small-scale exceptions across unbounded primitive parameters, and the other angle families, still prevent a complete solution of Erdős problem 634.
