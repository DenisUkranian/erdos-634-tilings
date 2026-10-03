# Claim ledger and verification scope

**Research snapshot v0.3.0 · 3 October 2026**

This ledger distinguishes mathematical claims from their evidence. The research packages are included in the repository. The exact commit and remote verification results are recorded by GitHub Actions; this ledger is not itself a CI success assertion.

| Claim | Status in this work | Supporting material |
|---|---|---|
| 120° F4 / Harries row III, a<b: every positive multiplier | Explicit four-region construction, separate internal symbolic review, 80 exact macro regressions and three independently checked complete unit-coordinate examples; a>b is not covered | [Proof and source attribution](research/group2-f4/PROOF.md), [finite report](research/group2-f4/VERIFIED_RESULTS.json) |
| Exact all-tile criterion in the stated N≡6 (mod16) sector | Written necessity and sufficiency proof, internally reviewed; all finite regressions replayed; uses established classification and the existing QP construction, not the prime candidate | [Uniform sectors](research/uniform-sectors/PROOF.md), [3 October review](docs/audits/october-theorems.md) |
| Compatible W/beta square classes: every sufficiently large multiplier is realized | Written geometric construction and norm reduction; explicit conductor C<2d for the selected squarefree representative; small scales not classified | [Square-class saturation](research/square-class-saturation/PROOF.md), [3 October review](docs/audits/october-theorems.md) |
| No triangle admits a 105-tiling | Computer-assisted proof with published classification/rationality inputs, written lemmas, and four complete exact certificates; internally replayed, no external acceptance | [Manuscript](research/n105/PROOF_N105.md), [certificate package](research/n105/), [scope](docs/n105-global.md) |
| Equilateral primitive 60°/120° spectra | Necessary S=abm, N=abm²; sufficient explicit large-m bounds, not a small-scale classification | [General spectra proof](research/general-spectra/PROOF.md) |
| 120° F1/isosceles necessary spectra | Known forms credited to Bonfioli, rederived by half-differences; large-scale sufficiency from Zhang-type constructions | [Attribution and proof](docs/general-spectra.md) |
| (45,32,67), equilateral side 12960, 116640 tiles | Exact hierarchical construction; macroregion pair intersections and all expanded tile shapes/containment checked; no claimed O(N²) tile-pair replay | [Certificate](research/general-spectra/construction_116640.json), [checker](research/general-spectra/verify_certificate.py) |
| Sharp c-relation thresholds | Complete elementary arithmetic derivation and finite regression; not certification of the geometric prime induction | [Audit](research/c-relations/audit.md) |
| For prime $p$, a triangle can be tiled by $p$ congruent triangles exactly when $p=2$, $p=3$ or $p\equiv1\pmod4$ | **Candidate proof**, dependent on the two geometric obstructions and the explicitly cited classification inputs; external review needed | [Complete candidate manuscript](paper/prime-case-candidate.pdf), [dependency note](docs/prime-case-dependencies.md), [geometric working text](docs/prime-case-candidate.md) |
| Scale-one obstruction for $W=(2\alpha,\beta,\alpha+\beta)$ | Proposed universal geometric theorem, internally checked; scrutiny of boundary induction and column completion requested | [Geometric text](docs/prime-case-candidate.md) |
| Scale-one obstruction for $(\beta,3\alpha,\beta)$ | Proposed universal geometric theorem, using the forced patch and the $W$ obstruction; external review needed | [Geometric text](docs/prime-case-candidate.md) |
| Fixed primitive tile $(uv,v^2-u^2,v^2)$, target $(2\alpha,\alpha,2\beta)$: exactly $N=k^2(2v^2-u^2)(3v^2-u^2)$ | Complete mathematical construction and necessity argument supplied; internally checked | [Construction PDF](paper/two-piece-construction.pdf), [full proof](docs/two-piece-construction.md) |
| $(81,115,126)$ admits a tiling by 322 copies of $(6,5,9)$ | Explicit coordinate certificate, checked by two different exact geometric methods | [Certificate](data/tiling-322.json), [separate checker](scripts/verify_322.py) |
| Additional constructions with 77 and 897 tiles | Finite exact implementation checks of the same formula | [77 certificate](data/tiling-77.json), [897 certificate](data/tiling-897.json) |
| All five rational target shapes for every primitive tile | Every sufficiently large arithmetically admissible scale is realizable, with no sign restriction on $\Delta$. The proof adds coprime increments $u,v$ to theta scales. Small-scale exceptions are still unclassified in general | [Universal annuli theorem](docs/universal-rational-scales.md) |
| W and beta eventual scales | Both eventual divisors are $d=1$ for **all** primitive parameters; an explicit conductor is $v\lceil H_u/v\rceil+(u-1)(v-1)$. No theta existence seed is required for this bound | [Universal annuli theorem](docs/universal-rational-scales.md) |
| Theta and alpha eventual scales | Explicit seed scales for both signs of $\Delta$ make the theta and alpha bounds computable directly from the tile parameters. Seed existence also follows from Beeson v4, Corollary 5 | [Universal theorem](docs/universal-rational-scales.md), [explicit seeds](docs/explicit-theta-seeds.md) |
| All triangular targets for the fixed tile $(2,3,4)$ | Complete six-family count classification, combining credited results, explicit constructions and the separately replayed alpha21 exclusion | [Fixed-tile theorem](docs/first-tile-classification.md) |
| No triangle admits a 21-tiling | Exhaustive classification-based reduction to one instance; a 391-node certificate is independently replayed as 437 expanded states. No prime-case candidate is used. Previously reported exclusion, independently reproduced here | [Global reduction](docs/n21-global-reduction.md), [geometric certificate proof](docs/alpha-21-obstruction.md) |
| Tile $(2,3,4)$: $W$ counts $7t^2$ and $\beta$-isosceles counts $11t^2$, exactly for $t\ge2$ | Known spectrum credited to Bonfioli; included for context and constructive continuation, not claimed as new here | [Scale spectra and attribution](docs/scale-spectra.md) |
| $\theta=\alpha+\beta$ isosceles branch for every primitive rational tile satisfying $3\alpha+2\beta=\pi$ | Two direction characters and parity give the necessary form $N=bT^2$ with integral $T$. The independent boundary argument also gives $b(T-1)\ge2v$. No complete classification for every tile is claimed | [Theta-branch argument](docs/theta-branch.md) |
| $\alpha$-isosceles branch for every primitive rational tile satisfying $3\alpha+2\beta=\pi$ | The same direction-character parity gives the necessary form $N=b(b+c)K^2$ with integral $K$, including nonsquarefree $b$; no restriction on the sign of $\Delta$ is needed for necessity | [Arithmetic proof](docs/eventual-rational-families.md) |
| Tile $(2,3,4)$ in the $\theta$ branch | Exact spectrum $N=3t^2$ for all integers $t\ge4$. The 75-tile construction completes the final missing scale | [Theta branch](docs/theta-branch.md) |
| Theta constructions with 75, 147 and 243 tiles | Separate exact-rational intersection replays pass all 2,775, 10,731 and 29,403 tile pairs, respectively, plus containment, total area and atomized edge cancellation | [Theta branch and certificates](docs/theta-branch.md) |
| Lemma 55 of Beeson v4 for tile $(2,3,4)$ | The 75-tile construction is a counterexample to its stated integrality/divisibility conclusion: $\mu=15/2$ and $M=5$, while its hypotheses hold. The prime-case candidate does not use this lemma | [Source comparison](docs/theta-branch.md) |
| Complete boundary collars for the two $N=105$ equilateral candidates | Exact partial placements for tiles $(5,21,19)$ and $(7,15,13)$; 45 and 57 tiles respectively, leaving interiors with areas equal to 60 and 48 tiles. This historical collar result alone gives no global exclusion; the later complete proof is listed above | [Current 105 result](docs/n105-global.md), [collar checker](scripts/verify_n105_collars.py) |
| Nonextendability of those two fixed $N=105$ collars | All four possible first tiles at one inner corner are blocked in each collar; two complete one-node refutations pass separate exact replay. This excludes only the named partial configurations | [Four-placement proof](docs/n105-fixed-collar-obstructions.md), [refutation checker](scripts/verify_n105_collar_refutations.py) |
| Third fixed N=105 collar | Six convex corners have no mutually compatible full fans; exact replay checks all options and six eliminations. Only this collar is excluded | [Proof](docs/n105-six-corner-obstruction.md), [checker](scripts/verify_n105_joint_fans.py) |
| Boundary of the (8,7,13) F1 target | Internally checked geometric proof: each external side has at least two length-13 edges; side 56 has two edges of each length. Not a global nonexistence proof | [Boundary proposition](docs/f1-two-longest-edges.md) |
| Complete classification of all composite counts or all counts in Erdős 634 | **Not obtained** | [Open frontier](docs/open-frontier.md) |

## Logical independence

The two-piece construction and its fixed-tile necessity argument do not use the proposed scale-one nonexistence proofs. A gap in a prime-case obstruction would therefore not invalidate the explicit 322-tile construction.

The universal annular construction and its eventual-scale theorem do not use either prime-case scale-one obstruction. The complete $(2,3,4)$ classification covers all targets for that one tile; small scales for other tiles and the separate angle families remain unresolved. The global exclusion of 21 has its own exhaustive reduction and exact refutation, also independent of the prime-case candidates.

The count 75 was already globally admissible because it is three times a square. The new result constructs the specific target $(30,30,15)$ from 75 tiles $(2,3,4)$ and completes the fixed-tile spectrum.

The 322 certificate establishes one finite geometric existence claim. Reproducing it does not prove the infinite family criterion, which has its own mathematical proof, and does not validate any nonexistence theorem.

The prime-case PDF contains the new geometric obstruction arguments and the exhaustive deduction from them and the stated external results to the all-primes conclusion, including the remaining branch calculations and explicit existence constructions. The [dependency note](docs/prime-case-dependencies.md) records the outside inputs for additional review. The expanded presentation does not change the candidate status of the geometric arguments.

## Meaning of independent checks

The construction program and the 322 checker were developed separately within this project. The checker reads coordinates as data; it does not import the generator or reuse its separating-axis predicate. It uses exact polygon intersections and subdivided edge cancellation. This is implementation independence. It is not independent human refereeing.

The current work does not claim journal acceptance, external referee approval, proof-assistant formalization or established publication priority. A public source timestamp would record availability of the material, not mathematical correctness or adjudicated priority.

## Literature boundary

The construction is compared specifically with the undecided case after Theorem 14 in [Beeson, arXiv:1206.2229v4](https://arxiv.org/abs/1206.2229v4). That reference describes a state of the source, not a proof that no other researcher has found the construction.

The prime deduction records exact versions and the parts of external results that it uses. Broad historical claims from superseded or withdrawn arguments must not replace those stated dependencies.

## What remains

General all-integer classification remains uncompleted even after the global 105 exclusion. This includes scales and target families not settled by the current results. Specific reductions and any separately settled subfamilies are maintained in [docs/open-frontier.md](docs/open-frontier.md). Do not infer that every count or scale not covered by the main README is either impossible or still open in the literature.

The precise remaining obligations are in [the full-solution roadmap](docs/full-solution-roadmap.md). The repository audit checks all tracked files and runnable finite evidence, not every universal proof in a formal system.

## Integrated continuation: uniform reduction (30 September 2026)

The [uniform-reduction note](docs/uniform-reduction.md) and its complete source, test data, and separately checked positive witnesses are included in this publication. Its results are necessary spectra, two squarefree congruence obstructions, a finite candidate overlist, and formal boundary-signature witnesses. They are not a complete all-integer classification. The N=154 search is recorded as INCOMPLETE. The root verification coordinator now also replays all supplementary tests of this module in a disposable copy. Historical reports are retained with their original preparation scope.
