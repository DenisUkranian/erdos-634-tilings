# Erdős 634: separate boundary workstream and the two unresolved 92 candidates

Denis Paliy, research with ChatGPT assistance — 9 October 2026.

## Coordination and status

The request was to avoid duplicating another ongoing ChatGPT conversation.
Attempts to retrieve that conversation did NOT reveal its current messages or
unfinished computations. A Library listing showed the most recent shared
saved research artifacts to be the class-14 package (last listed upload:
2026-10-09 13:18 UTC). That is a saved artifact, not evidence of what the other
conversation is currently doing. GitHub main was still 3a0ad269.

Accordingly this workstream did NOT repeat W56 or the beta92 interior search.
It independently checked the arithmetic gate for 23 and 92 and tested the
OTHER 92 realization: W with (u,v,m)=(3,4,2). Live non-duplication across the
two conversations cannot be guaranteed without a current status message.

**Neither 92, the full square class 23, nor the full problem is solved here.**
All interior searches in this package are explicitly INCOMPLETE.
The completed checks concern arithmetic and necessary boundary-support
eliminations only. No solver confidence, timeout, or incomplete tree is used
as a nonexistence proof.

## 1. Exact arithmetic gate

Using the complete branch formulae from the project at commit 3a0ad269,
`check_gate.py` enumerates all primitive Group-1 and plus/minus norm rows.
The finite bound and classical-family handling are those documented in the
prior class-14 package. The code is a prior input, not a new classification.
Heron's identity is checked for every candidate.

For N=92 the entire nonclassical overlist is:

| Branch | Primitive tile | Target sides | Residual scale |
| --- | --- | --- | --- |
| W | (12,7,16) | (128,138,56) | 2 |
| beta | (6,5,9) | (54,54,92) | 2 |
| theta | (132,23,144) | (552,552,506) | 2 |
| double-angle | (121,23,132) | (506,506,552) | 2 |

There is no classical witness. The last two rows fail the existing necessary
long-seam bounds, at u=11,v=12,b=23:

- theta requires m*b >= u*v, but 46 < 132;
- double-angle requires m*b >= u^2, but 46 < 121.

Thus, conditional on the existing exhaustive classification and the cited
long-seam theorem, **92 is realizable if and only if at least one of the first
two specific geometric instances is tileable**. A negative beta92 answer
alone would not globally exclude 92. A positive answer to either instance
would establish the global count immediately.

For N=23 the two surviving rows have the same parameter pairs at scale one.
The W row is already excluded by its 28-length side, shorter than two c=16
edges. The beta row is the prior finite fixed-tile 23 exclusion; it is not
reproved or newly claimed here. The earlier beta construction for (6,5,9)
provides every 23*m^2 with m>=3. Consequently the only possible remaining
choice for that global class is whether m=2 is admitted. It is NOT determined
by this package.

## 2. The independent W92 root split

The prior adjacent longest-edge theorem implies that the short side, of
length 56, has two consecutive c=16 edges. The equation

    12*A + 7*B + 16*C = 56,   A,B>=0, C>=2

has the unique solution (A,B,C)=(2,0,2). From the 2-alpha corner its first
edge must be c, so the complete word is

    16,16,12,12.

The endpoint-angle inventories fix the first c-edge and both a-edges;
only the chirality of the second c-edge remains. The two roots therefore
exhaust this fixed W instance. They use the same written root-split argument
as the previous W56 proof, now at v=4 rather than v=3.
`verify_support.py` reconstructs them from the target metric and cosine rule;
it also recomputes the unique length inventory. Reflections and T-junctions
are permitted. Interior coordinates are not restricted to a grid or a band.

## 3. A sound support-elimination rule

Let P be the already placed root triangles and let C be the finite dictionary
of possible whole supported boundary tiles. Whole boundary edges have integral
arclength endpoints because all tile side lengths are integers. Retain every
contained placement with a permitted endpoint angle; discard overlap with P.

The pre-existing boundary-path test asks, separately on each exterior side,
for a path from its first endpoint to its last, with the mandatory angle and
blocked-c rules. It is necessary, not sufficient.

The additional rule implemented here is:

1. Tentatively require one surviving supported tile T to belong to a completion.
2. Forbid every other supported position whose interior overlaps T, except T
   itself (one actual triangle may support two exterior sides).
3. Run the necessary path test on all exterior sides, retaining previous sound
   exclusions. If any side has no path, T has no support in any completion.
4. Permanently exclude T and iterate.

**Proof of soundness.** If a genuine tiling extended P and contained T, its
supported boundary triangles would avoid every overlap with T and would give
valid paths on every side. A failed path contradicts that assumption.
Induction over the elimination list preserves every genuine completion.
The existing blocked-c and geometric dictionary completeness are written
inputs; this is not a formal proof-assistant verification of those inputs.

This is a necessary condition only. Reaching a fixed point does not yield a
tiling, and the rule is not asserted to characterize all globally compatible
boundary choices.

## 4. Completed replay and incomplete searches

Each of the two W92 roots starts with 1554 oriented supported-edge dictionary
entries. In each root, 260 entries are forbidden directly by root overlaps.
The new rule then excludes 650 further supported tile positions; the 650
position sets coincide in the two root cases. There remain 644 unbanned
boundary entries in each case. The basic sidewise path tests still pass.

C++ GMP was used to generate the implication trace. The Python replay
uses fractions.Fraction and imports no C++ search code. It independently
reconstructs the boundary dictionary and every candidate assumption, checks
its geometry, recomputes all path failures, and applies only certified bans.
All 650 eliminations in each root were accepted. These are boundary
elimination certificates, not full refutations of W92.

The subsequent limited interior searches have the following retained reports:

| Search | Status | Nodes | Largest partial placement reported |
| --- | --- | ---:| ---:|
| W92 root 0, original boundary test | INCOMPLETE | 12928 | 82/92 |
| W92 root 1, original boundary test | INCOMPLETE | 11776 | 77/92 |
| W92 root 0, with support preprocessing | INCOMPLETE | 13056 | 82/92 |
| W92 root 1, with support preprocessing | INCOMPLETE | 11904 | 77/92 |

The partial placements and node totals are exploratory records, not tilings
or negative certificates. No complete refutation tree is provided. Search
budgets were approximately 30 and 34 seconds per root; their termination
was deliberate. No process from this workstream is running in the background.

## 5. Reproduce the completed checks

Python 3 and its standard library suffice:

    python reproduce.py

This recomputes the 23/92 arithmetic gate, applies the two documented seam
inequalities, checks the expected surviving instances, and replays both lists
of 650 boundary-support eliminations. It preserves the unresolved W92 status.
It does NOT repeat any beta92 search.

Optional exploratory C++ regeneration (GMP development library required):

    g++ -O3 -std=c++17 generate_W92_support.cpp -lgmpxx -lgmp -o search_w92
    BOUNDARY=1 W_ADJ_ROOT=0 ./search_w92 3 4 2 W 34 0 new_root0.json
    BOUNDARY=1 W_ADJ_ROOT=1 ./search_w92 3 4 2 W 34 0 new_root1.json

An INCOMPLETE output must never be used as a global negative result.

## 6. Handoff to the other conversation

The precise question to ask that workstream is:

    Are you working on beta92, W92, a general M<v theorem, or F3/14430?
    The independent gate leaves BOTH W(12,7,16) in (128,138,56) and
    beta(6,5,9) in (54,54,92) at N=92. This workstream has not decided
    either; it has checked the W boundary eliminations only.

The candidate reverse-apex manuscript is not a premise. Its own scope note
labels it proposed for independent scrutiny, not an accepted proof.
GitHub and the Library were not changed by creating this local package.

## Sources and provenance

All repository inputs are pinned to 3a0ad269f645850ed9fd01bbd76a08c9b456032e.

- research/uniform-reduction/PROOF.md: complete branch normalization and
  explicit published classification/rationality assumptions.
- docs/long-seams-density.md, Theorem 1: tb>=uv and tb>=u^2.
- research/w-global-oct7/ADJACENT_C_EDGES.md: blocked-c lemma, adjacent
  scale-two boundary word and endpoint orientations.
- research/universal-closure-oct8/group1/PROOF.md: the previously constructed
  positive beta23 square-class tail m>=3.
- User-provided Erdos634_class14_complete_2026-10-09.zip: inherited finite
  arithmetic enumerator, C++ exact corner search and Python base verifier.

The external rationality source is Beeson and Zhang,
Rationality of certain triangle tilings, arXiv:2604.01314 (2026).
Nothing here asserts a new literature priority, external review, or a complete
solution to Erdős 634.
