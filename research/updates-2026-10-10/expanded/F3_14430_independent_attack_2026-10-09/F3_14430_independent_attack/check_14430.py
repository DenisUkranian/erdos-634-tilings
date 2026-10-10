#!/usr/bin/env python3
"""Exact replay of the finite witnesses accompanying the 14430 research note.

Python 3 standard library only. No numerical tolerances, external packages or
network access. This does NOT decide whether a 14430-tiling exists.
Run: python check_14430.py [optional-path-to-witnesses.json]
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path
import json
import sys

Point = tuple[F, F]
ZERO: Point = (F(0), F(0))
RHO: Point = (F(0), F(1))

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def add(p: Point, q: Point) -> Point:
    return p[0] + q[0], p[1] + q[1]

def sub(p: Point, q: Point) -> Point:
    return p[0] - q[0], p[1] - q[1]

def scale(t: F | int, p: Point) -> Point:
    return t*p[0], t*p[1]

def mul(p: Point, q: Point) -> Point:
    # rho^2=rho-1
    x,y=p; X,Y=q
    return x*X-y*Y, x*Y+y*X+y*Y

def norm(p: Point) -> F:
    return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]

def det(p: Point, q: Point) -> F:
    return p[0]*q[1]-p[1]*q[0]

def power(p: Point, n: int) -> Point:
    if n < 0:
        nn=norm(p)
        p=((p[0]+p[1])/nn, -p[1]/nn)
        n=-n
    ans=(F(1),F(0))
    while n:
        if n & 1: ans=mul(ans,p)
        p=mul(p,p)
        n//=2
    return ans

def polygon_det(poly: list[Point]) -> F:
    # Physical signed area is this number times sqrt(3)/4.
    return sum(det(p,poly[(i+1)%len(poly)]) for i,p in enumerate(poly))

def points(raw: list[list[str]]) -> list[Point]:
    return [(F(p[0]), F(p[1])) for p in raw]

def exact_sqrt(q: F) -> F:
    u,v=isqrt(q.numerator),isqrt(q.denominator)
    require(u*u==q.numerator and v*v==q.denominator, 'Non-rational edge length')
    return F(u,v)

def contained(poly: list[Point], target: list[Point], strict: bool=False) -> bool:
    for i,p in enumerate(target):
        e=sub(target[(i+1)%len(target)],p)
        for v in poly:
            cross=det(e,sub(v,p))
            if cross < 0 or (strict and cross == 0): return False
    return True

def main(path: Path) -> dict:
    data=json.loads(path.read_text(encoding='utf-8'))
    a,b,c=data['tile']; N=14430
    require((a,b,c)==(56,9,61), 'Unexpected tile')
    require(gcd(a,b)==gcd(a,c)==gcd(b,c)==1, 'Primitivity failed')
    require(a*a+a*b+b*b==c*c, 'Norm equation failed')
    require(3*(a+b)*(a+2*b)==N, 'F3 area-count formula failed')
    require(N < 4*c*c and N%(2*c*c)!=0, 'Small-area arithmetic failed')
    z=(F(a,c),F(b,c))
    target=points(data['target'])
    expected=[ZERO,(F(c*c),F(0)),scale(c*(a+2*b),power(z,3))]
    require(target==expected, 'Target coordinates differ from F3 formula')
    require(polygon_det(target)==N*a*b, 'Target area failed')
    require(sub(target[2],target[1])==scale(3*b*(a+b),mul(RHO,power(z,2))),
            'Third side direction identity failed')

    directions={mul(power(RHO,j),power(z,h)):(h,j)
                for h in range(-3,7) for j in range(6)}
    require(len(directions)==60, 'Repeated direction in tested band')

    def edge_moments(poly: list[Point]) -> dict:
        ans=defaultdict(F)
        for i,p in enumerate(poly):
            q=poly[(i+1)%len(poly)]
            v=sub(q,p); length=exact_sqrt(norm(v))
            unit=scale(1/length,v)
            require(unit in directions, 'Edge outside replay direction band')
            h,j=directions[unit]; sign=1 if j<3 else -1
            mid=scale(F(1,2),add(p,q))
            for degree,value in enumerate((F(1),mid[0],mid[1])):
                ans[h,j%3,degree]+=sign*length*value
        return dict(ans)

    target_moments=edge_moments(target)
    boundary={(h,j):v for (h,j,k),v in target_moments.items() if k==0 and v}
    require(boundary=={(0,0):3721,(2,1):1755,(3,0):-4514}, 'Boundary current failed')
    require(1755%c==47, 'Non-whole-c side residue failed')

    def base_tile(h: int, j: int, kind: str) -> list[Point]:
        require(kind in ('A','B'), 'Unknown chirality')
        aa,bb=(a,b) if kind=='A' else (b,a)
        rot=mul(power(RHO,j),power(z,h))
        return [ZERO,scale(aa,rot),scale(bb,mul(power(RHO,2),rot))]

    def signed_char(inventory: list[dict]) -> tuple[int,int]:
        D=Ds=0
        for item in inventory:
            h,j,n=item['h'],item['j'],item['count']
            w=(-1 if item['type']=='A' else 1)*((-1)**j)*n
            D+=w; Ds+=(-1)**h*w
        return D,Ds

    # An independent direct-edge replay of the small, unpositioned inventory.
    formal=defaultdict(F); formal_counts=defaultdict(int)
    for item in data['formal_inventory']:
        h,j,kind,n=item['h'],item['j'],item['type'],item['count']
        formal_counts[h]+=n
        for key,value in edge_moments(base_tile(h,j,kind)).items():
            if key[2]==0: formal[key[:2]]+=n*value
    require(sum(formal_counts.values())==N, 'Formal population failed')
    require(all(formal.get(k,0)==boundary.get(k,0) for k in set(formal)|set(boundary)),
            'Formal directional current failed')
    require(signed_char(data['formal_inventory'])==(-182,-60), 'Character totals failed')

    # Exact integer multiset with translations. Moments are derived from the
    # actual geometric edge vectors, not from the orientation-current recurrence.
    total=defaultdict(F); populations=defaultdict(int); centroid=[F(0),F(0)]
    placements=data['moment_counterexample']['placements']
    for item in placements:
        h,j,kind,n=item['h'],item['j'],item['type'],item['count']
        require(isinstance(n,int) and n>0, 'Nonpositive or noninteger multiplicity')
        vs=points(item['vertices']); base=base_tile(h,j,kind)
        require([sub(v,vs[0]) for v in vs]==base, 'Incorrect orientation metadata')
        require(sorted(norm(sub(vs[(i+1)%3],vs[i])) for i in range(3))
                ==sorted((a*a,b*b,c*c)), 'Triangle is not congruent to tile')
        require(polygon_det(vs)==a*b, 'Tile orientation/area failed')
        require(contained(vs,target), 'Contained-placement condition failed')
        populations[h]+=n
        for k,value in edge_moments(vs).items(): total[k]+=n*value
        for k in range(2): centroid[k]+=F(n,3)*sum(v[k] for v in vs)
    require(sum(populations.values())==N, 'Multiset count failed')
    require(all(total.get(k,0)==target_moments.get(k,0)
                for k in set(total)|set(target_moments)), 'Exact first edge moments failed')
    require(all(centroid[k]==F(N,3)*sum(v[k] for v in target) for k in range(2)),
            'Area-centroid condition failed')
    require(dict(populations)=={1:13969,2:461}, 'Unexpected height populations')
    require(all(n%c==(N%c if h==2 else 0) for h,n in populations.items()),
            'Population congruences failed')
    require(signed_char(placements)==(-182,-60), 'Multiset character totals failed')
    duplicate=max(item['count'] for item in placements)
    require(duplicate==4737, 'Expected explicit overlap witness not found')

    # A contained polygon of the required tail area: NOT a tiling certificate.
    hx=data['contained_hexagon']; hv=points(hx['vertices']); k=hx['h']
    require(contained(hv,target,strict=True), 'Hexagon is not strictly contained')
    require(polygon_det(hv)==2*c*c*a*b, 'Hexagon area failed')
    for j,m in enumerate(hx['successive_edge_multipliers']):
        require(sub(hv[(j+1)%6],hv[j])==scale(c*m,mul(power(z,k),power(RHO,j))),
                'Hexagon whole-c boundary failed')
    require(all(not v for (h,j,dg),v in edge_moments(hv).items() if dg==0),
            'Hexagon directional imbalance is not zero')

    # Finite arithmetic consequences used in the written proofs.
    d=a-b
    require((3721-1755-4514)//(c-d)==-182, 'D formula failed')
    require(F(3721-1755+4514,-(c+d))==-60, 'D-star formula failed')
    n2_candidates=[]
    for n2 in (34,95):
        possible=[w for w in range(-n2,n2+1) if w%c==1 and (w-n2)%2==0]
        n2_candidates.append((n2,possible))
    require(n2_candidates==[(34,[]),(95,[1])], 'n2>=95 arithmetic failed')
    require((N-95)//61+1==236, 'Occupied-height bound failed')
    gap_cases=[]
    for K in (3721,7442,11163):
        for t in range(-20,21):
            M=-47+1512*t; DD=61+6588*t; SS=-61+854*t
            if max(abs(DD),abs(SS))<=K and (DD-K)%2==0 and (SS-K)%2==0:
                require(61*(61+M)==14*DD and 61*(M-61)==108*SS,
                        'Gap character identity failed')
                gap_cases.append((K,t))
    require(gap_cases==[(3721,0),(11163,-1),(11163,0),(11163,1)],
            'Empty-height-one alternatives failed')
    require(2*a*b==1008 and a*b==504, 'Polyiamond cell counts failed')
    require(3*(a*b)>2*a*b+2, 'Connected-polyiamond imbalance bound failed')

    # Control checks use only previously reported height populations, not a
    # newly replayed full geometric certificate for N=4830.
    ctl=data['control_4830']; ac,bc,cc=ctl['tile']
    pcs={int(h):n for h,n in ctl['height_populations'].items()}
    Nc=3*(ac+bc)*(ac+2*bc)
    require(Nc==4830 and sum(pcs.values())==Nc, '4830 count control failed')
    require(all(n%cc==(Nc%cc if h==2 else 0) for h,n in pcs.items()),
            '4830 residue control failed')
    require(sum(n for h,n in pcs.items() if h%2)%2==cc%2, '4830 odd parity control failed')
    require(sum(n for h,n in pcs.items() if not h%2)%2==(2*ac+bc)%2,
            '4830 even parity control failed')

    return {
        'status':'PASS: exact finite witness replay only',
        'N_14430':'UNDECIDED',
        'tiling_certificate_produced':False,
        'nonexistence_certificate_produced':False,
        'numeric_arithmetic':'fractions.Fraction; zero floating-point tolerance',
        'boundary_heights':[0,2,3],
        'formal_inventory_populations':dict(formal_counts),
        'moment_multiset':{'count':N,'distinct_listed_placements':len(placements),
            'height_populations':dict(populations),'largest_coincident_multiplicity':duplicate,
            'is_a_tiling':False,'first_edge_moments':'PASS','area_centroid':'PASS',
            'individual_containment':'PASS','height_congruences':'PASS'},
        'contained_hexagon':{'tile_area_equivalent':7442,'whole_c_height':3,
            'strict_containment':'PASS','tiling_of_hexagon_asserted':False},
        'necessary_condition_arithmetic':{'n2_minimum':95,'occupied_heights_maximum':236,
            'derived_height_span_bound':237,'gap_one_lower_population_options':[3721,11163],
            'small_whole_c_component_cells':1008,'up_cells':504,'down_cells':504},
        'control_4830':'Population and parity consistency PASS; not a full tiling replay',
        'scope':'Universal necessity proofs are written in the note; this script checks the finite witnesses and their arithmetic, not all possible tilings.'
    }

if __name__=='__main__':
    try:
        src=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('witnesses.json')
        report=main(src)
        print(json.dumps(report,ensure_ascii=False,indent=2))
    except (ValueError,KeyError,TypeError,ArithmeticError,OSError,json.JSONDecodeError) as exc:
        print(f'FAIL: {exc}',file=sys.stderr)
        sys.exit(1)
