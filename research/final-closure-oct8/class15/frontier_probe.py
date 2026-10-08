#!/usr/bin/env python3
'''Budgeted exact convex-frontier search for three surviving class-15 families.
Derived from scripts/search_alpha21.py, retaining its exact exhaustive branching.
INCOMPLETE is never a refutation. Boundary coverage is not grid restricted.
'''
from pathlib import Path
import importlib.util,sys,argparse
from fractions import Fraction as F
from math import isqrt
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('front',ROOT/'scripts/search_alpha21.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
p=argparse.ArgumentParser();p.add_argument('kind',choices=['theta4','theta56','double49','e120']);p.add_argument('m',type=int);p.add_argument('--seconds',type=int,default=30);p.add_argument('--max-nodes',type=int,default=100000);p.add_argument('--output',required=True);p.add_argument('--boundary-pruning',action='store_true');args=p.parse_args()
u,v=(1,4) if args.kind=='theta4' else (7,8)
if args.kind=='e120':
 D=3;a,b,c=3,5,7;angles=(('alpha',(F(13,14),F(3,14)),(b,c)),('beta',(F(11,14),F(5,14)),(a,c)),('gamma',(-F(1,2),F(1,2)),(a,b)));base=15*args.m
elif args.kind.startswith('theta'):
 D=4*v*v-u*u;a,b,c=u*v,v*v-u*u,v*v
 angles=(('alpha',(1-F(u*u,2*v*v),F(u,2*v*v)),(b,c)),('beta',(F(u*(3*v*v-u*u),2*v**3),F(b,2*v**3)),(a,c)),('gamma',(-F(u,2*v),F(1,2*v)),(a,b)))
 base=b*u*args.m
else:
 D=4*u*u-v*v;a,b,c=u*u,v*v-u*u,u*v
 angles=(('alpha',(F(v,2*u),F(1,2*u)),(b,c)),('beta',(F(3*v,2*u)-F(v**3,2*u**3),F(b,2*u**3)),(a,c)),('gamma',(F(v*v-2*u*u,2*u*u),F(v,2*u*u)),(a,b)))
 base=b*v*args.m

g.dot=lambda a,b:a[0]*b[0]+D*a[1]*b[1]
g.compose=lambda a,b:(a[0]*b[0]-D*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
g.rotate=lambda a,r:g.compose(a,r)
g.ANGLES=angles;g.FANS={(F(1),F(0)):(0,0,0)};todo=[(F(1),F(0))]
while todo:
 r=todo.pop()
 for i,(_,angle,_) in enumerate(angles):
  q=g.compose(r,angle)
  if q[1]>0 and q not in g.FANS:
   inv=list(g.FANS[r]);inv[i]+=1;g.FANS[q]=tuple(inv);todo.append(q)
g.OUTER=(g.P(0,0),g.P(base,0),g.P(F(base,2),F((15 if args.kind=='e120' else b)*args.m,2)))
g.AREA2=F(a*b)*angles[2][1][1]
# Optional necessary whole-boundary arithmetic. Never a sufficiency test.
if args.boundary_pruning:
    original_possibilities=g.possibilities
    def boundary_possible(placed):
        for A,B in g.edges(g.OUTER):
            length=g.length(g.sub(B,A));unit=g.mul(g.sub(B,A),1/length)
            occupied=[];c_count=0
            for tri in placed:
                for p in tri:
                    if g.on(p,A,B) and g.dot(g.sub(p,A),unit).denominator!=1:
                        return False
                for p,q in g.edges(tri):
                    if g.on(p,A,B) and g.on(q,A,B):
                        x,y=sorted((g.dot(g.sub(p,A),unit),g.dot(g.sub(q,A),unit)))
                        occupied.append((x,y))
                        if y-x==c:c_count+=1
            occupied.sort();end=F(0);gaps=[]
            for x,y in occupied:
                if x>end:gaps.append(x-end)
                end=y
            if end<length:gaps.append(length-end)
            c_max=0
            for gap in gaps:
                if gap.denominator!=1:return False
                n=int(gap);choices=[C for C in range(n//c+1)
                    if any((n-c*C-b*B)%a==0 for B in range((n-c*C)//b+1))]
                if not choices:return False
                c_max+=max(choices)
            # Two longest edges lemma used only for the proved obtuse cases.
            if c_count+c_max<2:return False
        return True
    def pruned(sector,placed):
        return [row for row in original_possibilities(sector,placed)
                if boundary_possible(placed+[row[-1]])]
    g.possibilities=pruned

# Patch only N and metadata, reuse the frozen source main verbatim.
source=(ROOT/'scripts/search_alpha21.py').read_text().split('def main():',1)[1].split("if __name__=='__main__':",1)[0]
source='def main():'+source
source=source.replace('len(placed)==21','len(placed)==N').replace("'depth':21","'depth':N").replace("'D':15,'tile_sides':[2,3,4]","'D':D,'tile_sides':TILE_SIDES")
g.N=15*args.m*args.m;g.D=D;g.TILE_SIDES=[a,b,c]
assert sum(g.det(a,b) for a,b in g.edges(g.OUTER))==g.N*g.AREA2
exec(source,g.__dict__)
sys.argv=[sys.argv[0],'--seconds',str(args.seconds),'--max-nodes',str(args.max_nodes),'--output',args.output]
g.main()
