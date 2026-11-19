"""Exact vertex-star consistency for congruent (9,20,25) triangles on an orientation band.

Each row is a Python bigint representing a set of integral x-coordinates. Coordinates
represent (x+y*sqrt(-21))/D. No rounding enters geometric and angular predicates.
"""
from argparse import ArgumentParser
from collections import defaultdict
from fractions import Fraction as F
from functools import cmp_to_key
import json
from pathlib import Path
from math import isqrt

def add(p,q):return p[0]+q[0],p[1]+q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def mul(p,q):return p[0]*q[0]-21*p[1]*q[1],p[0]*q[1]+p[1]*q[0]
def sc(a,p):return a*p[0],a*p[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def norm(p):return p[0]*p[0]+21*p[1]*p[1]
def ceil(a,b):return -((-a)//b)
def angle_cmp(a,b):
    au=a[1]<0 or a[1]==0 and a[0]<0
    bu=b[1]<0 or b[1]==0 and b[0]<0
    c=cross(a,b)
    return (au>bu)-(au<bu) if au!=bu else (c<0)-(c>0)

def rx(v,x):return v<<x if x>=0 else v>>-x

class Model:
    def __init__(self,lo,hi,scale,control=False,fixed=(),use_strips=True):
        self.d=D=5**max(abs(lo),abs(hi))
        self.lo,self.hi,self.scale=lo,hi,scale
        self.star_list=[]
        self.control=control
        n=2*max(abs(lo),abs(hi))+7
        g={0:(F(1),F(0))}
        z=(F(-2,5),F(1,5))
        for h in range(1,n+1):
            g[h]=mul(g[h-1],z)
            g[-h]=(g[h][0],-g[h][1])
        def ial(p):
            x,y=p
            assert int(x)==x and int(y)==y
            return int(x),int(y)
        if control:
            raw=[(0,0),(36,0),(68,16)]
        else:
            raw=[(0,0),(236*scale,0),(118*scale,9*scale)]
        self.target=raw
        tr=[sc(D,v) for v in raw]
        self.walls=[(tr[i],tr[(i+1)%3]) for i in range(3)]
        lengths=[isqrt(norm(sub(b,a)))//D for a,b in self.walls]
        outer_u=[tuple(F(w,L*D) for w in sub(b,a)) for (a,b),L in zip(self.walls,lengths)]
        dirs=sorted({sc(s,g[j]) for h in range(lo,hi+1) for j in range(h-2,h+3) for s in (1,-1)}
                    |set(outer_u)|{sc(-1,q) for q in outer_u},key=cmp_to_key(angle_cmp))
        self.rays=R=len(dirs); self.north=R//2
        self.outer_dirs=[dirs.index(q) for q in outer_u]
        self.oy=min(y for x,y in tr)
        assert self.oy==0 and min(x for x,y in tr)==0
        self.width=W=1+max(x for x,y in tr); self.height=H=1+max(y for x,y in tr)
        self.limit=(1<<W)-1
        self.blank=[0]*H
        self.genuine=[]
        self.inc=defaultdict(list)
        self.edge=defaultdict(list)
        self.pos=[]
        self.shapes=[]
        self.verts=[]
        self.sectors=[]
        self.id={}
        self.slices=defaultdict(lambda:[0]*H)
        cornerlist=[]
        for i,(a,b) in enumerate(self.walls):
            u=self.outer_dirs[i]
            v=self.outer_dirs[(i-1)%3]
            cornerlist.append(((v+R//2)%R,u,a))
            vector=sub(b,a)
            if use_strips:
                sem=[False]*(lengths[i]+1); sem[0]=True
                for j in range(1,len(sem)):sem[j]=any(j>=n and sem[j-n] for n in (9,20,25))
            for j in range(1,lengths[i]):
                if use_strips and not (sem[j] and sem[lengths[i]-j]):continue
                a0=tuple(F(x*j,lengths[i]) for x in vector)
                if not all(v.denominator==1 for v in a0):continue
                x,y=add(a,ial(a0))
                self.slices[(u+R//2)%R,u][y]|=1<<x
        for a,b,(x,y) in cornerlist:self.slices[a,b][y]|=1<<x
        self.outer_corners=cornerlist
        self.outer_integer={}
        for i,((a,b),L) in enumerate(zip(self.walls,lengths)):
            d=sub(b,a)
            sem=[False]*(L+1);sem[0]=True
            for j in range(1,L+1):sem[j]=any(j>=n and sem[j-n] for n in (9,20,25))
            points=set()
            for j in range(L+1):
                delta=tuple(F(x*j,L) for x in d)
                if sem[j] and sem[L-j] and all(v.denominator==1 for v in delta):points.add(add(a,ial(delta)))
            self.outer_integer[i]=points
        for h in range(lo,hi+1):
            for sign in (1,-1):
                for o in (-8,17):
                    u=sc(D*sign,g[h])
                    vs=[(0,0),ial(sc(9,u)),ial(mul(u,(o,4)))]
                    key=(h,sign,o)
                    self.id[key]=k=len(self.pos); self.shapes.append(key);self.verts.append(vs)
                    edge_dirs=[]
                    for j in range(3):
                        e=sub(vs[(j+1)%3],vs[j])
                        le=isqrt(norm(e))//D
                        unit=tuple(F(c,D*le) for c in e)
                        edge_dirs.append(dirs.index(unit))
                    sec=[]
                    for j,p in enumerate(vs):
                        # Interior sector runs counterclockwise from forward edge to reverse previous edge.
                        a=edge_dirs[j]; b=(edge_dirs[(j-1)%3]+R//2)%R
                        assert 0<(b-a)%R<R//2
                        self.inc[a,b].append((k,p));sec.append((a,b,p))
                        delta=sub(vs[(j+1)%3],p)
                        le=isqrt(norm(delta))//D
                        ds=[]
                        for s in range(1,le):
                            point=tuple(F(w*s,le) for w in delta)
                            if all(w.denominator==1 for w in point):ds.append(add(p,ial(point)))
                        if ds:self.edge[a,(a+R//2)%R].append((k,ds))
                    self.sectors.append(sec)
                    values=[]
                    for y in range(H):
                        left,right=0,W-1
                        blocks=[]
                        for i,((a,b),L) in enumerate(zip(self.walls,lengths)):
                            dx,dy=sub(b,a)
                            # signed distance numerator cross(wall, anchor+v-a).
                            # All template vertices lie in target.
                            for j,(ex,ey) in enumerate(vs):
                                c=dx*(y+ey-a[1])+dy*(a[0]-ex)
                                if dy>0:right=min(right,c//dy)
                                elif dy<0:left=max(left,ceil(-c,-dy))
                                elif c<0:left=1;right=0;break
                                if not use_strips:continue
                                # A vertex on a wall must be a boundary-word joint.
                                # Off the wall, clearance is at least 81*sqrt(21)/125.
                                # A parallel interior tile side needs at least 36*sqrt(21)/25.
                                parallel=any(edge_dirs[ed]% (R//2)==self.outer_dirs[i]% (R//2) for ed in (j,(j-1)%3))
                                num,den=(36,25) if parallel else (81,125)
                                cutoff=ceil(num*L*D*D,den)
                                if dy==0:
                                    if 0<c<cutoff:left=1;right=0
                                    if c==0:blocks.append(('wall',i,ex,ey))
                                else:
                                    if dy>0:l=(c-cutoff)//dy+1;r=(c-1)//dy
                                    else:l=ceil(1-c,-dy);r=ceil(cutoff-c,-dy)-1
                                    if l<=r:blocks.append((l,r))
                                    if c%dy==0 and (c//dy+ex,y+ey) not in self.outer_integer[i]:blocks.append((c//dy,c//dy))
                        if left>right:values.append(0);continue
                        bits=((1<<(right-left+1))-1)<<left
                        for rec in blocks:
                            if len(rec)==4:
                                _,i,ex,ey=rec
                                ok=sum(1<<(px-ex) for px,py in self.outer_integer[i] if py==y+ey and px>=ex)
                                bits &=ok
                            else:
                                l,r=max(left,rec[0]),min(right,rec[1])
                                if l<=r:bits &=~(((1<<(r-l+1))-1)<<l)
                        values.append(bits)
                    self.pos.append(values)
        self.blocked=fixed
    def moves_or(self,out,source,p):
        x,y=p
        for j in range(max(0,y),min(self.height,self.height+y)):
            v=source[j-y]
            if v:out[j]|=rx(v,x)&self.limit
    def remove(self,k,x,y):
        self.pos[k][y]&=~(1<<x)
    def turn(self,stars=True):
        H=self.height;R=self.rays
        arcs={s:list(v) for s,v in self.slices.items()}
        for ab,types in self.inc.items():
            a=arcs.setdefault(ab,self.blank.copy())
            for k,p in types:self.moves_or(a,self.pos[k],p)
        if stars:
            for ab,types in self.edge.items():
                a=arcs.setdefault(ab,self.blank.copy())
                for k,offsets in types:
                    for p in offsets:self.moves_or(a,self.pos[k],p)
        adj=defaultdict(list)
        for (a,b),valid in arcs.items():adj[b].append((a,valid))
        dead=[]
        # For a chosen starting ray s, compute all viable masks for CCW paths
        # through a strict subarc. This reads previous-generation placements.
        support={}
        requests=set(self.inc)|{(a,b) for a,b,p in self.outer_corners}
        for s in sorted(set(b for a,b in requests)):
            interval={s:[self.limit]*H}
            for n in range(1,R):
                j=(s+n)%R
                options=[(interval[i],av) for i,av in adj[j] if i in interval and (j-i)%R<=n]
                if not options:continue
                val=self.blank.copy()
                for prior,available in options:
                    for y in range(H):val[y]|=prior[y]&available[y]
                interval[j]=val
            for a,b in requests:
                if b==s:support[a,b]=interval.get(a,self.blank)
        for a,b,(x,y) in self.outer_corners:
            if not ((support[a,b][y]>>x)&1):dead.append((x,y))
        new=[]
        for k,mask in enumerate(self.pos):
            rows=mask.copy()
            for a,b,(x,y) in self.sectors[k]:
                right=support[a,b]
                for j in range(H):
                    if rows[j]:rows[j]=rows[j]&rx(right[j+y],-x) if 0<=j+y<H else 0
            new.append(rows)
        self.pos=new
        return dead
    def turn_rows(self):
        # A vertex-star constraint only compares incidences at one y coordinate.
        # Retaining the old generation permits the same monotone transformation
        # as turn(), with memory for only one row of paths and arcs at a time.
        H,R=self.height,self.rays
        new=[q.copy() for q in self.pos]
        requests=set(self.inc)|{(a,b) for a,b,p in self.outer_corners}
        starts=sorted({b for a,b in requests})
        required={b:[a for a,k in requests if k==b] for b in starts}
        moves=defaultdict(list)
        for key,occur in self.inc.items():
            for k,p in occur:moves[key].append((k,*p))
        for key,occur in self.edge.items():
            for k,points in occur:
                for p in points:moves[key].append((k,*p))
        keys=set(moves)|set(self.slices)
        paths={}
        for s in starts:
            prior=set([s])
            steps=[]
            for j in [(s+n)%R for n in range(1,R)]:
                choices=[(i,(i,j)) for i in prior if (i,j) in keys]
                if choices:steps.append((j,choices));prior.add(j)
            paths[s]=steps
        dead=[]
        queries=defaultdict(list)
        for a,b,(x,y) in self.outer_corners:queries[y].append((x,a,b))
        inc=list(self.inc.items())
        for y in range(H):
            arcs={k:v[y] for k,v in self.slices.items()}
            for key,types in moves.items():
                v=0
                for k,x,d in types:
                    yy=y-d
                    if 0<=yy<H:
                        row=self.pos[k][yy]
                        if row:v|=rx(row,x)
                arcs[key]=arcs.get(key,0)|(v&self.limit)
            support={}
            for s in starts:
                reach={s:self.limit}
                for j,choices in paths[s]:
                    value=0
                    for i,ab in choices:
                        if reach[i]:value|=reach[i]&arcs[ab]
                    reach[j]=value
                for a in required[s]:support[a,s]=reach.get(a,0)
            for x,a,b in queries[y]:
                if not ((support[a,b]>>x)&1):dead.append((x,y))
            for key,types in inc:
                possible=support[key]
                for k,(x,d) in types:
                    yy=y-d
                    if 0<=yy<H and new[k][yy]:
                        new[k][yy]&=rx(possible,-x)
        self.pos=new
        return dead
    def count(self):
        return sum(v.bit_count() for s in self.pos for v in s)
    def entry(self,tri):
        for k,vs in enumerate(self.verts):
            for a in tri:
                if {add(a,p) for p in vs}==set(tri):
                    x,y=a
                    assert x>=0 and y>=0
                    yield k,x,y
    def accepts(self,entries):
        return all(self.pos[k][y]>>x&1 for k,x,y in entries)

def main():
    ap=ArgumentParser();ap.add_argument('lo',type=int);ap.add_argument('hi',type=int)
    ap.add_argument('--scale',type=int,default=2);ap.add_argument('--control',action='store_true')
    ap.add_argument('--no-strips',action='store_true'); ap.add_argument('--remove-control-corner',action='store_true')
    ap.add_argument('--trace',action='store_true');ap.add_argument('--row-wise',action='store_true')
    args=ap.parse_args()
    mod=Model(args.lo,args.hi,args.scale,args.control,use_strips=not args.no_strips)
    if args.remove_control_corner:
        assert args.control
        mod.remove(mod.id[0,1,17],0,0)
    if args.control:
        D=mod.d
        grid=[]
        for i in range(4):
            for j in range(4-i):
                a=(D*(9*i+17*j),D*4*j)
                grid.append((mod.id[0,1,17],*a))
                if i+j<3:grid.append((mod.id[0,-1,17],a[0]+26*D,a[1]+4*D))
        assert len(grid)==16
        if not args.remove_control_corner:assert mod.accepts(grid)
    record=[mod.count()];death=[]
    while True:
        death=mod.turn_rows() if args.row_wise else mod.turn()
        n=mod.count();record.append(n)
        if args.trace:print(len(record)-1,n,death,flush=True)
        if args.control and not args.remove_control_corner:assert mod.accepts(grid)
        if death or n==record[-2]:break
    print(json.dumps(dict(band=[args.lo,args.hi],scale=args.scale,control=args.control,remove_control_corner=args.remove_control_corner,
          denominator=mod.d,counts=record,missing_corners=death,exact_status='contradiction' if death else 'fixed_point'),indent=2))

if __name__=='__main__':main()
