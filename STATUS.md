# Claim ledger and verification scope

**Research snapshot v0.1.0 · 29 September 2026**

This file distinguishes mathematical claims from the evidence supporting them. It records a prepared research snapshot; it does not by itself assert that a GitHub release has been published or that remote continuous integration has passed.

| Claim | Status in this work | Supporting material |
|---|---|---|
| For prime $p$, a triangle can be tiled by $p$ congruent triangles exactly when $p=2$, $p=3$ or $p\equiv1\pmod4$ | **Candidate proof**, dependent on the two geometric obstructions and the explicitly cited classification inputs; external review needed | [Complete candidate manuscript](paper/prime-case-candidate.pdf), [dependency note](docs/prime-case-dependencies.md), [geometric working text](docs/prime-case-candidate.md) |
| Scale-one obstruction for $W=(2\alpha,\beta,\alpha+\beta)$ | Proposed universal geometric theorem, internally checked; scrutiny of boundary induction and column completion requested | [Geometric text](docs/prime-case-candidate.md) |
| Scale-one obstruction for $(\beta,3\alpha,\beta)$ | Proposed universal geometric theorem, using the forced patch and the $W$ obstruction; external review needed | [Geometric text](docs/prime-case-candidate.md) |
| Fixed primitive tile $(uv,v^2-u^2,v^2)$, target $(2\alpha,\alpha,2\beta)$: exactly $N=k^2(2v^2-u^2)(3v^2-u^2)$ | Complete mathematical construction and necessity argument supplied; internally checked | [Construction PDF](paper/two-piece-construction.pdf), [full proof](docs/two-piece-construction.md) |
| $(81,115,126)$ admits a tiling by 322 copies of $(6,5,9)$ | Explicit coordinate certificate, checked by two different exact geometric methods | [Certificate](data/tiling-322.json), [separate checker](scripts/verify_322.py) |
| Additional constructions with 77 and 897 tiles | Finite exact implementation checks of the same formula | [77 certificate](data/tiling-77.json), [897 certificate](data/tiling-897.json) |
| Eventual structure of $W$ and $\beta$-isosceles scale sets | Each nonempty scale set eventually consists exactly of multiples of an integer $d\mid v$; the value of $d$ and small exceptions are not determined in general | [Scale spectra](docs/scale-spectra.md) |
| Tile $(2,3,4)$: $W$ counts $7t^2$ and $\beta$-isosceles counts $11t^2$, exactly for $t\ge2$ | Known spectrum credited to Bonfioli; included for context and constructive continuation, not claimed as new here | [Scale spectra and attribution](docs/scale-spectra.md) |
| $\theta=\alpha+\beta$ isosceles branch, $b=qh^2$ with $q$ squarefree | Independent necessary bound $qh(t-h)\ge2v$ in the parametrization of the note; no complete classification claimed | [Theta-branch argument](docs/theta-branch.md) |
| Tile $(2,3,4)$ in the $\theta$ branch | Necessary form $N=3t^2$, $t\ge4$; constructions realize every such $t$ except possibly $t=5$. Only $N=75$ remains unresolved in this fixed-tile branch | [Theta branch](docs/theta-branch.md) |
| Theta constructions with 147 and 243 tiles | Separate exact-rational intersection replays pass all 10,731 and 29,403 tile pairs, respectively, plus containment, total area and atomized edge cancellation | [Theta branch and certificates](docs/theta-branch.md) |
| Lemma 55 of Beeson v4 for tile $(2,3,4)$ | The 147-tile construction is a counterexample to its stated integrality/divisibility conclusion: $\mu=21/2$ and $M=7$, while its hypotheses hold. The prime-case candidate does not use this lemma | [Source comparison](docs/theta-branch.md) |
| Complete boundary collars for the two $N=105$ equilateral candidates | Exact partial placements for tiles $(5,21,19)$ and $(7,15,13)$; 45 and 57 tiles respectively, leaving interiors with areas equal to 60 and 48 tiles. No complete 105-tiling or global exclusion is established | [Open frontier](docs/open-frontier.md#the-remaining-n105-investigation), [collar checker](scripts/verify_n105_collars.py) |
| Complete classification of all composite counts or all counts in Erdős 634 | **Not obtained** | [Open frontier](docs/open-frontier.md) |

## Logical independence

The two-piece construction and its fixed-tile necessity argument do not use the proposed scale-one nonexistence proofs. A gap in a prime-case obstruction would therefore not invalidate the explicit 322-tile construction.

The independent theta-branch constructions and their scale-addition consequences have their own proofs and exact certificates. The lone remaining count $75$ concerns the specific tile $(2,3,4)$ and the specific theta-isosceles target shape; it is not a claim that only one count remains in Erdős problem 634 as a whole.

Indeed, 75 is already globally admissible because it is three times a square. The unresolved fixed instance has target sides $(30,30,15)$ and tile sides $(2,3,4)$.

The 322 certificate establishes one finite geometric existence claim. Reproducing it does not prove the infinite family criterion, which has its own mathematical proof, and does not validate any nonexistence theorem.

The prime-case PDF contains the new geometric obstruction arguments and the exhaustive deduction from them and the stated external results to the all-primes conclusion, including the remaining branch calculations and explicit existence constructions. The [dependency note](docs/prime-case-dependencies.md) records the outside inputs for additional review. The expanded presentation does not change the candidate status of the geometric arguments.

## Meaning of independent checks

The construction program and the 322 checker were developed separately within this project. The checker reads coordinates as data; it does not import the generator or reuse its separating-axis predicate. It uses exact polygon intersections and subdivided edge cancellation. This is implementation independence. It is not independent human refereeing.

The current work does not claim journal acceptance, external referee approval, proof-assistant formalization or established publication priority. A public source timestamp would record availability of the material, not mathematical correctness or adjudicated priority.

## Literature boundary

The construction is compared specifically with the undecided case after Theorem 14 in [Beeson, arXiv:1206.2229v4](https://arxiv.org/abs/1206.2229v4). That reference describes a state of the source, not a proof that no other researcher has found the construction.

The prime deduction records exact versions and the parts of external results that it uses. Broad historical claims from superseded or withdrawn arguments must not replace those stated dependencies.

## What remains

General composite-count classification, including scales and target families not settled by the current results, remains unresolved. Specific reductions and any separately settled subfamilies are maintained in [docs/open-frontier.md](docs/open-frontier.md). Do not infer that every count or scale not covered by the main README is either impossible or still open in the literature.
