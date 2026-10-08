# Five-page mathematical note

`Triangle_Tilings_Mixed_Corner.tex` is the editable source for
**A mixed-direction construction for triangle tilings**, Denis Paliy,
8 October 2026, with ChatGPT assistance acknowledged on the title page.

The note contains the general sufficient F3 semigroup theorem, its five
positive regions, the 4830 example, both exact macro figures, the
uniform interval ending at 2725/1139, the Frobenius estimate, and links
to all 710 finite witnesses and supporting code. It explicitly leaves
the complete classification of Erdős 634 open. It makes no statement
about 135.

The exact SVG originals are versioned in `../f3-general/`. Generate the
two PNG renderings below before compiling twice with `pdflatex` from this
directory. PNGs are temporary build inputs rather than additional proof
data. For example:

```
inkscape ../f3-general/q480_five_regions.svg --export-type=png --export-width=2400 --export-filename=../f3-general/q480_five_regions.png
inkscape ../f3-general/f3_4830_macro.svg --export-type=png --export-width=2400 --export-filename=../f3-general/f3_4830_macro.png
```

Choose an output directory outside the repository when compiling the
PDF. The source uses Palatino text and mathematics, A4 paper, and
clickable supporting links.

The initial release was rendered with Poppler at 120 dpi and every
page was visually checked. It has five pages, no LaTeX overflow or
unresolved-reference warnings, correct clickable repository links,
and no missing glyphs, clipped text or overlapping layout elements.
