"""Render construction blocks and export the two small, exact pentagon certificates."""
from json import dumps
from math import sqrt
from pathlib import Path

from notch_check import unit_board, verify


def render_board(a, b, c, y_offset):
    data = unit_board(a, b, c, 2, 1)
    total, holes, (_, _, remaining) = verify(data)
    assert holes == 2
    n = (a+2*b)*(2*a+b)
    output = Path(__file__).resolve().parent
    (output/f"pentagons_{n}.json").write_text(dumps(data, separators=(",",":"))+"\n")
    outer = data["target"]
    scale = 690/max(y+x/2 for x,y in outer)

    baseline = y_offset + 70 + scale*max(x for x,y in outer)*sqrt(3)/2

    def poly(points):
        return " ".join(f"{25+scale*(y+x/2):.2f},{baseline-scale*x*sqrt(3)/2:.2f}"
                        for x,y in points)

    elements = [f'<text x="25" y="{y_offset+24}" class="header">N = {n:,}</text>',
                f'<text x="25" y="{y_offset+49}" class="detail">{total-2*remaining:,} placed tiles. '
                f'Two congruent holes, each with area {remaining} tiles.</text>']
    for block in data["blocks"]:
        kind = block["kind"]
        color = {"triangle":"#c6e1e4","parallelogram":"#b3d2dc","notch":"#eb8a34"}[kind]
        elements.append(f'<polygon points="{poly(block["points"])}" fill="{color}" stroke="#40565f" '
                        'stroke-width="0.65" stroke-linejoin="round"/>')
    elements.append(f'<polygon points="{poly(outer)}" fill="none" stroke="#253f48" stroke-width="1.5"/>')
    return elements


if __name__ == "__main__":
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 710" role="img">',
             '<title>Two partial triangle tilings with congruent pentagonal holes</title>',
             '<style>text{font-family:Arial,sans-serif;fill:#263e49}.header{font-size:19px;font-weight:bold}'
             '.detail{font-size:14px}</style><rect width="750" height="710" fill="#ffffff"/>']
    parts += render_board(33,7,37,0)
    parts += render_board(35,13,43,304)
    parts.append('</svg>')
    (Path(__file__).resolve().parent/'pentagons.svg').write_text("\n".join(parts)+"\n")
