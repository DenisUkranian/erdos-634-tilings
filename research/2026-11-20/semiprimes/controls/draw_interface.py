"""Draw the two verified banks and their detour from the 3431 partial certificate."""
from math import sqrt
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def xy(p):
    return p[0]+p[1]/2, sqrt(3)*p[1]/2


def main():
    data = json.loads((ROOT/'interface_3431.json').read_text())
    a, b, c = data['tile']
    c2 = c*c
    board = [(0,0), (a+b, -b), (a*a*(a+2*b)/c2, a*b*(a+2*b)/c2)]
    path = data['path_vertices_in_unit_lattice']
    tiles = [[(x/c2,y/c2) for x,y in tri] for tri in data['triangles']]
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="332" viewBox="0 0 920 332">',
           '<title>A partial tiling on the unit F2 triangle for 3431</title>',
           '<desc>Two banks of 42 tiles each along a nonstraight interface. The full board and the two changes of direction near the incenter are shown.</desc>',
           '<rect width="920" height="332" fill="white"/>',
           '<g font-family="system-ui, sans-serif" fill="#1a3040">',
           '<text x="20" y="29" font-size="19" font-weight="bold">3431 · a scale-one partial tiling</text>',
           '<text x="20" y="55" font-size="14">Entire board</text>',
           '<text x="595" y="55" font-size="14">Detail near the incenter</text>']
    physical = [xy(vertex) for vertex in board]
    bounds = (min(x for x,y in physical)-1, min(y for x,y in physical)-1,
              max(x for x,y in physical)+1, max(y for x,y in physical)+1)
    panels = [(20,71,550,200,bounds), (595,71,304,200,(a-3.2,-2.6,a+3.2,1.6))]
    for number, (left,top,width,height,box) in enumerate(panels):
        x0,y0,x1,y1 = box
        scale = min(width/(x1-x0),height/(y1-y0))
        def pts(vertices):
            points = []
            for vertex in vertices:
                x,y = xy(vertex)
                px = left+(width-scale*(x1-x0))/2 + (x-x0)*scale
                py = top+(height-scale*(y1-y0))/2 + (y1-y)*scale
                points.append(f'{px:.3f},{py:.3f}')
            return ' '.join(points)
        svg.append(f'<defs><clipPath id="view{number}"><rect x="{left}" y="{top}" width="{width}" height="{height}"/></clipPath></defs>')
        svg.append(f'<g clip-path="url(#view{number})">')
        svg.append(f'<polygon points="{pts(board)}" fill="#f3f5f3" stroke="#344b55" stroke-width="1.6"/>')
        for i,tri in enumerate(tiles):
            color = '#337d9e' if i%2 == 0 else '#dd9767'
            svg.append(f'<polygon points="{pts(tri)}" fill="{color}" stroke="white" stroke-width="0.35"/>')
        if number:
            svg.append(f'<polyline points="{pts([(0,0),(a,0),(a+b,-b)])}" fill="none" stroke="#697e87" stroke-dasharray="5 4" stroke-width="1"/>')
        svg.append(f'<polyline points="{pts(path)}" fill="none" stroke="#172e39" stroke-width="1.25"/>')
        svg.append('</g>')
    svg.extend(['<rect x="20" y="291" width="15" height="11" fill="#337d9e"/>',
                '<text x="42" y="301" font-size="13">42 low tiles</text>',
                '<rect x="150" y="291" width="15" height="11" fill="#dd9767"/>',
                '<text x="172" y="301" font-size="13">42 high tiles</text>',
                '<rect x="291" y="291" width="15" height="11" fill="#f3f5f3" stroke="#697e87"/>',
                '<text x="314" y="301" font-size="13">Unfilled part of the board</text>',
                '</g></svg>'])
    (ROOT/'interface_3431.svg').write_text('\n'.join(svg)+'\n')


if __name__ == '__main__':
    main()
