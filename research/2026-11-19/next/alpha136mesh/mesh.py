"""Conservative vertex-star test on real square cells for any finite orientation band."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"beta"))
from vertex_stars import (F,add,sub,sc,angle_cmp,cmp_to_key,isqrt,ceil,rx,defaultdict)
def mul(p,q):return p[0]*q[0]-35*p[1]*q[1],p[0]*q[1]+p[1]*q[0]
def norm(p):return p[0]*p[0]+35*p[1]*p[1]
from argparse import ArgumentParser
import json
def cells(v):
    x,y=v
    xs=sorted({x.numerator//x.denominator,ceil(x.numerator,x.denominator)})
    ys=sorted({y.numerator//y.denominator,ceil(y.numerator,y.denominator)})
    return [(a,b) for a in xs for b in ys]
def fl(v):return tuple(a.numerator//a.denominator for a in v)
class Mesh:
    def __init__(self,B,Q,scale=2,freeze=None,clearance=True):
        self.freeze=freeze
        self.B=B;self.Q=Q
        power={0:(F(1),F(0))}
        for k in range(1,max(B+2,3)+1):
            power[k]=mul(power[k-1],(F(-1,6),F(1,6)));power[-k]=(power[k][0],-power[k][1])
        rays=sorted({sc(s,v) for v in power.values() for s in (1,-1)},key=cmp_to_key(angle_cmp))
        R=self.R=len(rays)
        tr=[(0,0),(136,0),(68,4)]
        walls=[];bins=[]
        sem=[False]*(136+1);sem[0]=True
        for j in range(1,len(sem)):sem[j]=any(j>=v and sem[j-v] for v in (3,8,9))
        D=Q
        self.w=W=1+136*Q;self.h=H=1+4*Q
        self.lim=(1<<W)-1
        self.outer=defaultdict(dict);self.corners=[]
        for j in range(3):
            a=tr[j];b=tr[(j+1)%3];delta=sub(b,a)
            l=isqrt(norm(delta));u=sc(F(1,l),delta);r=rays.index(u)
            walls.append((a,delta,l,r))
            ps=[add(sc(Q,a),sc(Q*i,u)) for i in range(l+1) if sem[i] and sem[l-i]]
            bins.append(ps)
            z=self.outer[(r+R//2)%R,r]
            for p in ps[1:-1]:
                x,y=fl(p); z[y]=z.get(y,0)|(1<<x)
        for i,((a,d,l,r),pwall) in enumerate(zip(walls,[walls[-1]]+walls[:-1])):
            x,y=sc(Q,a);ab=(pwall[3]+R//2)%R,r
            self.outer[ab][y]=self.outer[ab].get(y,0)|(1<<x)
            self.corners.append((*ab,x,y))
        self.inc=defaultdict(list);self.gluing=defaultdict(list);self.pos=[];self.shapes=[]
        for h in range(-B,B+1):
            for s in (1,-1):
                u=sc(s,power[h])
                for o in (-1,17):
                    k=len(self.pos)
                    self.shapes.append((h,s,o))
                    vs=[(F(0),F(0)),sc(8*Q,u),sc(Q,mul(u,(F(o,2),F(1,2))))]
                    ed=[sub(vs[(j+1)%3],vs[j]) for j in range(3)]
                    ls=[8,9 if o==-1 else 3,3 if o==-1 else 9]
                    rs=[rays.index(sc(F(1,l*Q),v)) for v,l in zip(ed,ls)]
                    for j,v in enumerate(vs):
                        ab=rs[j],(rs[(j+2)%3]+R//2)%R
                        self.inc[ab].append((k,cells(v)))
                        offs=set()
                        for m in range(1,ls[j]):
                            offs.update(cells(add(v,sc(F(m,ls[j]),ed[j]))))
                        self.gluing[rs[j],(rs[j]+R//2)%R].append((k,offs))
                    constraints=[]
                    for i,(a,(dx,dy),l,rwall) in enumerate(walls):
                        for j,v in enumerate(vs):
                            x,y=v
                            parallel=any(e%(R//2)==rwall%(R//2) for e in (rs[j],rs[(j+2)%3]))
                            distance_bound=(F(4,9) if parallel else F(1,6))*l*Q if clearance else 0
                            # Need actual cross >= clearance at some actual anchor in the cell,
                            # or a vertex at an admissible boundary joint.
                            allowance=max(0,dx)+max(0,-dy)
                            c=dx*(y-Q*a[1])-dy*(x-Q*a[0])+allowance-distance_bound
                            flo=c.numerator//c.denominator
                            discrete=defaultdict(int)
                            for p in bins[i]:
                                bx,by=fl(sub(p,v))
                                if 0<=bx<W and 0<=by<H:discrete[by]|=1<<bx
                            constraints.append((dx,dy,flo,discrete))
                    p=[]
                    for y in range(H):
                        value=self.lim
                        for dx,dy,c,discrete in constraints:
                            n=dx*y+c
                            if dy>0:
                                r=min(W-1,n//dy);v=0 if r<0 else (1<<(r+1))-1
                            elif dy<0:
                                l=max(0,ceil(-n,-dy));v=0 if l>=W else self.lim^((1<<l)-1)
                            else:v=self.lim if n>=0 else 0
                            value&=v|discrete[y]
                            if not value:break
                        p.append(value)
                    self.pos.append(p)
        self.moves=defaultdict(list)
        for typ in (self.inc,self.gluing):
            for key,parts in typ.items():
                for k,delta in parts:
                    self.moves[key].extend((k,x,y) for x,y in delta)
        keys=set(self.moves)|set(self.outer)
        self.requests=set(self.inc)|{(a,b) for a,b,x,y in self.corners}
        starts=sorted({b for a,b in self.requests})
        self.required={b:[a for a,k in self.requests if k==b] for b in starts}
        self.paths={}
        for s in starts:
            earlier=set([s]);steps=[]
            for j in [(s+n)%R for n in range(1,R)]:
                choices=[(i,(i,j)) for i in earlier if (i,j) in keys]
                if choices:steps.append((j,choices));earlier.add(j)
            self.paths[s]=steps
        self.queries=defaultdict(list)
        for a,b,x,y in self.corners:self.queries[y].append((x,a,b))
    def count(self):return sum(v.bit_count() for row in self.pos for v in row)
    def turn(self):
        # Modified backward mapping uses a union of floor/ceiling shifts for
        # each individual corner before intersecting the three corners.
        H,R=self.h,self.R
        inc=list(self.inc.items())
        # Group offsets by (shape, vertical shift) to reuse a bitmask.
        moves={}
        for key,entries in self.moves.items():
            groups=defaultdict(list)
            for k,x,y in entries:groups[k,y].append(x)
            moves[key]=[(k,y,xs) for (k,y),xs in groups.items()]
        sup={ab:[0]*H for ab in self.inc}
        dead=[]
        for y in range(H):
            av={k:v.get(y,0) for k,v in self.outer.items()}
            for key,types in moves.items():
                v=0
                for k,d,xs in types:
                    yy=y-d
                    if 0<=yy<H:
                        row=self.pos[k][yy]
                        if row:
                            for x in xs:v|=rx(row,x)
                av[key]=av.get(key,0)|(v&self.lim)
            for s,steps in self.paths.items():
                reach={s:self.lim}
                for j,choices in steps:
                    v=0
                    for i,ab in choices:
                        if reach[i]:v|=reach[i]&av[ab]
                    reach[j]=v
                for a in self.required[s]:
                    if (a,s) in sup:sup[a,s][y]=reach.get(a,0)
                for x,a,b in self.queries[y]:
                    if b==s and not (reach.get(a,0)>>x&1):dead.append((x,y))
        new=[a.copy() for a in self.pos]
        for ab,items in inc:
            ok=sup[ab]
            for k,offsets in items:
                if self.freeze is not None and abs(self.shapes[k][0])>self.freeze:continue
                newk=new[k]
                for y,row in enumerate(newk):
                    if row:
                        v=0
                        for x,d in offsets:
                            yy=y+d
                            if 0<=yy<H:v|=rx(ok[yy],-x)
                        newk[y]&=v
        self.pos=new
        return dead

if __name__=='__main__':
    p=ArgumentParser();p.add_argument('bound',type=int);p.add_argument('mesh',type=int)
    p.add_argument('--scale',type=int,default=2);p.add_argument('--steps',type=int,default=1000)
    p.add_argument('--freeze-outside',type=int);p.add_argument('--no-clearance',action='store_true')
    args=p.parse_args()
    m=Mesh(args.bound,args.mesh,args.scale,args.freeze_outside,not args.no_clearance);counts=[m.count()]
    print(0,counts[-1],flush=True)
    end='pass-limit'
    dead=[]
    for i in range(1,args.steps+1):
        dead=m.turn();counts.append(m.count());print(i,counts[-1],dead,flush=True)
        if dead:end='contradiction';break
        if counts[-1]==counts[-2]:end='fixed-point';break
    print(json.dumps({'abs_bound':args.bound,'mesh':args.mesh,'scale':args.scale,'status':end,'no_clearance':args.no_clearance,'freeze_outside':args.freeze_outside,'counts':counts,'dead':dead}))

    for h in range(-args.bound,args.bound+1):
        total=sum(v.bit_count() for rs in m.pos[4*(h+args.bound):4*(h+args.bound+1)] for v in rs)
        print("height",h,total)
