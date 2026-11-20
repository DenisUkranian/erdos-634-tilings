#!/usr/bin/env python3
"""Complete geometric catalogue for the two-tree exterior-spine class.

The catalogue covers exactly contained tiles at heights 0,1,2 in R,
A+zR,A+z^2R. Counting scans integer row intervals; it does not materialize
millions of columns or solve their integer endpoint equations.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from math import gcd
from pathlib import Path
import argparse
import json


UNITS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def mul(p,q):
    x,y=p;u,v=q
    return x*u-y*v,x*v+y*u+y*v


def ceildiv(n,d):
    return -((-n)//d)


def axis(p,q):
    x,y=q[0]-p[0],q[1]-p[1]
    divisor=gcd(abs(x),abs(y))
    assert divisor
    x,y=x//divisor,y//divisor
    return (x,y) if x>0 or (x==0 and y>0) else (-x,-y)


def polygon_rows(poly):
    rows=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        u=axis(p,q)
        rows.append(((p[0],p[1],*u),1))
        rows.append(((q[0],q[1],*u),-1))
    return tuple(rows)


class SpineCatalogue:
    def __init__(self,a,b,c):
        assert a>b>0 and c*c==a*a+a*b+b*b
        self.a,self.b,self.c=a,b,c
        self.A,self.B=b*(2*a+b),a*(a+2*b)
        self.N=(a+2*b)*(2*a+b)
        self.D=c*c
        self.board=((0,0),(self.D*self.A,0),(0,self.D*self.B))
        self.templates=tuple((h,j,s) for h in range(3)
                             for j in range(6) for s in (-1,1))

    def shift(self,h):
        return self.A if h else 0

    @lru_cache(None)
    def power(self,h):
        base=(self.a,self.b) if h>=0 else (self.a+self.b,-self.b)
        answer=(1,0)
        for _ in range(abs(h)):
            answer=mul(answer,base)
        return *answer,self.c**abs(h)

    @lru_cache(None)
    def offsets(self,j,s):
        u,v=UNITS[j],UNITS[(j+s)%6]
        return ((-self.a*u[0],-self.a*u[1]),(0,0),
                (self.b*v[0],self.b*v[1]))

    @lru_cache(None)
    def inequalities(self,h,j,s):
        u,v,den=self.power(h)
        offsets=[mul((u,v),e) for e in self.offsets(j,s)]
        shift=self.shift(h)
        return ((-u,v,shift*den+min(x for x,y in offsets)),
                (-v,-u-v,min(y for x,y in offsets)),
                (self.B*u+self.A*v,-self.B*v+self.A*(u+v),
                 self.A*self.B*den-self.B*shift*den
                 -max(self.B*x+self.A*y for x,y in offsets)))

    @lru_cache(None)
    def anchor_box(self,h):
        u,v,den=self.power(-h)
        shift=self.shift(h)
        pts=[mul((u,v),(x-shift,y)) for x,y in
             ((0,0),(self.A,0),(0,self.B))]
        return (ceildiv(min(x for x,y in pts),den),
                max(x for x,y in pts)//den,
                ceildiv(min(y for x,y in pts),den),
                max(y for x,y in pts)//den)

    def row_interval(self,h,j,s,n):
        xmin,xmax,ymin,ymax=self.anchor_box(h)
        if not ymin<=n<=ymax:
            return None
        lo,hi=xmin,xmax
        for p,q,r in self.inequalities(h,j,s):
            remainder=r-q*n
            if p>0:
                hi=min(hi,remainder//p)
            elif p<0:
                lo=max(lo,ceildiv(remainder,p))
            elif remainder<0:
                return None
        return (lo,hi) if lo<=hi else None

    def anchor_rows(self,h,j,s):
        _,_,ymin,ymax=self.anchor_box(h)
        for n in range(ymin,ymax+1):
            interval=self.row_interval(h,j,s,n)
            if interval is not None:
                yield n,*interval

    def count_template(self,h,j,s):
        return sum(hi-lo+1 for _,lo,hi in self.anchor_rows(h,j,s))

    def placements(self):
        for h,j,s in self.templates:
            for n,lo,hi in self.anchor_rows(h,j,s):
                for m in range(lo,hi+1):
                    yield m,n,h,j,s

    def contains(self,tile):
        m,n,h,j,s=tile
        return (h,j,s) in self.templates and all(
            p*m+q*n<=r for p,q,r in self.inequalities(h,j,s))

    def vertices(self,tile):
        m,n,h,j,s=tile
        u,v,den=self.power(h)
        scale=self.D//den
        shift=self.shift(h)*self.D
        result=[]
        for x,y in self.offsets(j,s):
            X,Y=mul((u,v),(m+x,n+y))
            result.append((shift+scale*X,scale*Y))
        return tuple(result) if s==1 else tuple(reversed(result))

    def endpoint_rows(self,tile):
        return polygon_rows(self.vertices(tile))

    def native_anchor(self,point,h):
        """Return integer native coordinates of a point scaled by D, or None."""
        if h not in range(3):
            return None
        u,v,den=self.power(-h)
        x,y=mul((u,v),(point[0]-self.shift(h)*self.D,point[1]))
        divisor=self.D*den
        if x%divisor or y%divisor:
            return None
        return x//divisor,y//divisor

    @lru_cache(None)
    def local_rows(self,h,j,s):
        return self.endpoint_rows((0,0,h,j,s))

    def incident(self,row):
        """Every contained spine placement contributing to this exact row."""
        x,y,ux,uy=row
        found={}
        for h,j,s in self.templates:
            u,v,den=self.power(-h)
            divisor=self.D*den
            for (px,py,vx,vy),coefficient in self.local_rows(h,j,s):
                if (ux,uy)!=(vx,vy):
                    continue
                X,Y=mul((u,v),(x-px,y-py))
                if X%divisor or Y%divisor:
                    continue
                tile=X//divisor,Y//divisor,h,j,s
                if self.contains(tile):
                    assert tile not in found
                    found[tile]=coefficient
        assert len(found)<=24
        return found

    def report(self):
        records=[]
        for h,j,s in self.templates:
            rows=list(self.anchor_rows(h,j,s))
            records.append({'height':h,'rotation':j,'hand':s,
                            'placements':sum(hi-lo+1 for _,lo,hi in rows),
                            'nonempty_anchor_rows':len(rows)})
        return {'N':self.N,'tile':[self.a,self.b,self.c],
                'common_coordinate_denominator':self.D,
                'cosets':['R','A+zR','A+z^2R'],
                'height_counts':[sum(r['placements'] for r in records if r['height']==h)
                                 for h in range(3)],
                'total_placements':sum(r['placements'] for r in records),
                'templates':records}


def control_143(certificate):
    cat=SpineCatalogue(5,3,7)
    data=json.loads(certificate.read_text())
    selected=[]
    balances=Counter({r:-v for r,v in polygon_rows(cat.board)})
    area=0
    for point,h,j,s in data['tiles']:
        x,y,e=point
        q=(Fraction(x*cat.D,cat.c**e),Fraction(y*cat.D,cat.c**e))
        assert all(v.denominator==1 for v in q)
        native=cat.native_anchor(tuple(int(v) for v in q),h)
        assert native is not None
        tile=(*native,h,j,s)
        assert cat.contains(tile)
        selected.append(tile)
        poly=cat.vertices(tile)
        for i in range(3):
            p,q=poly[i],poly[(i+1)%3]
            area+=p[0]*q[1]-p[1]*q[0]
        for row,coefficient in cat.endpoint_rows(tile):
            balances[row]+=coefficient
            assert cat.incident(row).get(tile)==coefficient
    assert len(set(selected))==len(selected)==143
    assert not any(balances.values())
    assert area==cat.A*cat.B*cat.D*cat.D
    # Exhaust the much smaller control catalogue independently by boxes.
    total=0
    for h,j,s in cat.templates:
        xmin,xmax,ymin,ymax=cat.anchor_box(h)
        count=0
        for m in range(xmin,xmax+1):
            for n in range(ymin,ymax+1):
                poly=cat.vertices((m,n,h,j,s))
                if all(x>=0 and y>=0 and cat.B*x+cat.A*y<=cat.A*cat.B*cat.D
                       for x,y in poly):
                    count+=1
        assert count==cat.count_template(h,j,s)
        total+=count
    return {'certificate_N':143,'known_tiles_retained':143,
            'known_current_residuals':0,'known_doubled_area_verified':True,
            'all_template_row_counts_match_independent_box_enumeration':True,
            'complete_control_catalogue_placements':total,
            'incident_oracle_retains_every_known_tile_at_all_six_rows':True}


def find_control():
    for ancestor in Path(__file__).resolve().parents:
        for candidate in (ancestor/'global-endpoints/tiling_143.json',
                          ancestor/'repo/research/2026-11-20/semiprimes/continuation/global-endpoints/tiling_143.json'):
            if candidate.exists():
                return candidate
    raise FileNotFoundError('Pass --control pointing to tiling_143.json.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path)
    p.add_argument('--control',type=Path)
    args=p.parse_args()
    report={'scope':'Complete finite catalogue for the no-occupied-exterior-free-node class in both trees; no endpoint feasibility result.',
            'catalogues':[SpineCatalogue(*s).report() for s in
                          ((5,3,7),(33,7,37),(35,13,43))],
            'positive_control':control_143(args.control or find_control()),
            'checks':'PASS'}
    text=json.dumps(report,indent=2)+'\n'
    if args.out:
        args.out.write_text(text)
    print(text,end='')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    main()
