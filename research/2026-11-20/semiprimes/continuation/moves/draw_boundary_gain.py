"""Draw the two exact midpoint half-rhombus packings at 3431 as a small SVG."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


def picture(a=33, b=7):
    from math import sqrt
    shapes = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 322" role="img">',
              '<title>Exact midpoint boundary switch on the 3431 board</title>',
              '<desc>Two views of the same half-rhombus. Exchanging the short sides aligns the diagonals with the board and adds 33 whole tiles.</desc>',
              '<rect width="830" height="322" fill="#faf8f3"/>']
    def stroke(poly, offset):
        return ' '.join(f'{offset+200*(float(x)+0.5*float(y)):.2f},{250-100*sqrt(3)*float(y):.2f}' for x,y in poly)
    for col, (nx,ny,expected,color) in enumerate(((b,a,a*b-a,'#a9c9c4'),(a,b,a*b,'#6ca99b'))):
        offset = 47+410*col
        def point(i,j): return Fraction(i,nx),Fraction(j,ny)
        def inside(v): return a*(2*v[0]-1)>=b*(2*v[1]-1)
        lo = Fraction(a-b,2*a),0
        hi = Fraction(a+b,2*a),1
        region = [lo,(1,0),(1,1),hi]
        shapes.append(f'<polygon points="{stroke(region,offset)}" fill="#f7d9b6" stroke="#344b52" stroke-width="1"/>')
        borders=set()
        segments=defaultdict(set)
        count=0
        for i in range(nx):
            for j in range(ny):
                for middle in [point(i+1,j),point(i,j+1)]:
                    tile=[point(i,j),middle,point(i+1,j+1)]
                    if all(inside(x) for x in tile):
                        ints=[(int(x*nx),int(y*ny)) for x,y in tile]
                        if middle==point(i,j+1):
                            ints.reverse()
                        for u,v in zip(ints,ints[1:]+ints[:1]):
                            if (v,u) in borders:
                                borders.remove((v,u))
                            else:
                                borders.add((u,v))
                            (x,y),(xx,yy)=sorted((u,v))
                            kind=0 if y==yy else 1 if x==xx else 2
                            pos=y if kind==1 else x
                            axis=y if kind==0 else x if kind==1 else y-x
                            segments[kind,axis].add(pos)
                        count+=1
        assert count==expected
        chain=dict(borders)
        assert len(chain)==len(borders)
        start=next(iter(chain))
        walk=[start]
        while chain:
            nxt=chain.pop(walk[-1]); walk.append(nxt)
            if nxt==start:
                break
        assert not chain
        shapes.append(f'<polygon points="{stroke([point(*v) for v in walk],offset)}" fill="{color}"/>')
        lines=[]
        for (kind,axis),steps in sorted(segments.items()):
            coords=lambda t: (axis,t) if kind==1 else (t,axis) if kind==0 else (t,t+axis)
            while steps:
                first=min(steps); stop=first
                while stop in steps:
                    steps.remove(stop); stop+=1
                pair=[point(*coords(first)),point(*coords(stop))]
                lines.append('M'+stroke(pair,offset).replace(' ',' L'))
        shapes.append(f'<path d="{" ".join(lines)}" stroke="#28554f" stroke-width="0.7" fill="none"/>')
        shapes.append(f'<polyline points="{stroke([lo,hi],offset)}" fill="none" stroke="#9a422c" stroke-width="2.7"/>')
        shapes.append(f'<text x="{offset+25}" y="46" font-family="sans-serif" font-size="18" fill="#23383a">{("Before","After")[col]} · {count} whole tiles</text>')
    shapes.append('<text x="415" y="296" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#553629">Red line: the outer triangle boundary.  Orange: space left between whole tiles.</text>')
    shapes.append('</svg>')
    return '\n'.join(shapes)+'\n'


if __name__ == '__main__':
    Path(__file__).with_name('boundary-gain.svg').write_text(picture(), encoding='utf-8')
