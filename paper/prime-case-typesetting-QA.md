# Prime-case manuscript: typesetting review

29 September 2026. Version 0.1.0, draft for review.

## Deliverables

- `prime-case-candidate.tex`: standalone LaTeX source.
- `prime-case-candidate.pdf`: 15 A4 pages, 392,830 bytes.
- Title: *A candidate classification of prime triangle-tiling counts*.
- Author: Denis Paliy.

The manuscript incorporates the precise candidate statement for all prime counts, the exhaustive branch table, version-specific outside dependencies, the direct integer-scale argument, the other branch calculations, explicit existence constructions, and both complete scale-one geometric arguments. The geometric proof body from the earlier two-obstruction manuscript was preserved exactly. The contribution statement describes Denis Paliy's direction of the investigation and ChatGPT's assistance. Candidate status and the unresolved composite-count classification are stated explicitly.

## Build and visual checks

Built with pdfLaTeX (TeX Live 2023). From this directory, run twice:

```sh
pdflatex -interaction=nonstopmode -halt-on-error prime-case-candidate.tex
```

- Final build has no LaTeX warnings, undefined references, overfull boxes, or underfull boxes.
- All 15 final pages were rendered and visually inspected. The final bibliography pagination change affected pages 14 and 15; both were rendered and inspected again afterward.
- Equations, Greek symbols, tables, running headers, page numbers, and bibliography are readable and unclipped.
- The twelve-row classification table fits on one page. The four-row sine-law table is intact.
- The bibliography starts on its own page. The W appendix starts on its own page.
- All PDF fonts are embedded, with Unicode mappings. No JavaScript or interactive form is present.
- Title and author metadata are correct. No workspace paths, tool citations, or local-file URLs occur in the source.
- The source requires no external figures or bibliography files.

This is a presentation and build check, not an external mathematical review or formal verification.

## SHA-256

```text
c515027d3c386b8e18d49d24370a92233a4de925b0e6fedb3c52d47928c68f2e  prime-case-candidate.pdf
81b35348cff0f2199a5998702b88592c6ba3cc2cd0fe92c32d67866df85bd953  prime-case-candidate.tex
```
