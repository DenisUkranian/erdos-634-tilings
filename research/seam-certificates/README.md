# Exact seam certificates

The [proof note](../../docs/exact-seam-certificates.md) establishes integer
atomic lengths and a forest of contacts between original tile sides in a
convex integer-sided tiling. For a proposed combinatorial disk, tree leaf
elimination determines all contact lengths; exact angle and topology checks
give the general existence certificate described in the note.

`verify_seams.py` is a **finite replay of the retained 322-tile example**,
not an implementation of the general abstract-disk checker or a search for
new tilings. It uses only Python's standard library and imports no
construction code. The input is [`data/tiling-322.json`](../../data/tiling-322.json).

From the repository root, run:

```sh
python research/seam-certificates/verify_seams.py
```

Default execution only prints JSON. To regenerate the retained report:

```sh
python research/seam-certificates/verify_seams.py --report research/seam-certificates/verification.json
```

The module also exposes a read-only `verify()` function returning the report
dictionary. `--output` is an alias of `--report`. Running with `python -O`
is rejected because assertions are part
of verification. Paths to the input are resolved from the script location;
an explicitly supplied report path is resolved from the working directory.

The replay splits every original tile side at **all genuine tile vertices**
on that side, including T-junctions. It permits ordinary cross-points at
tile corners. It checks positive integral atomic lengths, boundary versus
interior incidences, opposite-bank contacts, the side-contact forest, and
recovery of every interior atom solely from whole-side lengths by integer
leaf elimination. It also checks the angle-count/Euler identities and
linear bounds from the note by counting actual vertices and incidences.

The retained [report](verification.json) records 450 trees, 474 interior
atoms, 42 boundary atoms, and 24 T-junctions. All recovered lengths match
the input coordinates. The three target corners are included in the 42
boundary vertices; the other 129 interior vertices have no straight-through
tile.

Global containment, positive-area nonoverlap, and coverage are dependencies
on the existing geometric certificate, rather than conclusions of this seam
replay. The existing checker is:

```sh
python scripts/verify_322.py
```

The report therefore explicitly distinguishes this finite replay from a
complete abstract-disk verifier. Neither the replay nor the general
certificate theorem solves the unbounded global classification required
by Erdős 634.
