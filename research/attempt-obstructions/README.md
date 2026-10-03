# A checked limit of a proposed seam argument

[THETA_CHORD.md](THETA_CHORD.md) and `check_corner_chord.py` give an exact
five-tile partial configuration and a chord. It refutes a proposed scalar
width cutoff, including the width of the actual unfilled region. It is
neither a complete triangular tiling nor an actual tiled a/c seam, and it
does not show that an additional swapped tile can be placed.

Run ordinary Python without optimization:

```
python check_corner_chord.py
```

The checker uses rational arithmetic and an exact isolating interval for
one square root. Its labeled decimal ratio is descriptive only. The
report is written to `corner_chord_certificate.json`; the root replay
runs it in a disposable copy.
