"""Replay candidate windmill sections with exact integer and rational arithmetic."""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache
from pathlib import Path
import json
import subprocess
import sys
import tempfile

folder = Path(__file__).resolve().parent

def polygon_key(edges):
    mirror = [(l,-h,(3-j)%6) for l,h,j in reversed(edges)]
    keys = []
    for cycle in (list(edges),mirror):
        for i,(_,h,j) in enumerate(cycle):
            keys.append(tuple((n,k-h,(p-j)%6) for n,k,p in cycle[i:]+cycle[:i]))
    return min(keys)

def angle(previous, current):
    _,ph,pj=previous
    _,h,j=current
    return next(((m,m+ph-h) for m in range((pj+3-j)%6,7,6)
                 if 0<=m+ph-h<=6 and 0<2*m+ph-h<12),None)

def arc(board,start,end):
    i,t=start
    j,u=end
    if i==j and t<u:
        return [(u-t,*board[i][1:])]
    boundary=[(board[i][0]-t,*board[i][1:])]
    i=(i+1)%len(board)
    while i!=j:
        boundary.append(board[i]);i=(i+1)%len(board)
    if u:boundary.append((u,*board[j][1:]))
    return boundary

def analyze(a,b,c,board,rows):
    @cache
    def unit(h,j):
        x,y=1,0
        u,v=(Fraction(a,c),Fraction(b,c)) if h>=0 else (Fraction(a+b,c),Fraction(-b,c))
        for _ in range(abs(h)):
            x,y=x*u-y*v,x*v+y*(u+v)
        for _ in range(j%6):x,y=-y,x+y
        return x,y
    @cache
    def area(shape):
        x=y= A=0
        for length,h,j in shape:
            u,v=unit(h,j);dx,dy=u*length,v*length
            A+=x*dy-y*dx;x+=dx;y+=dy
        assert (x,y)==(0,0)
        return Fraction(A,a*b)
    @cache
    def cmax(length):
        return max((z for z in range(length//c+1) for x in range((length-z*c)//a+1)
                    if (length-z*c-x*a)%b==0),default=-1)
    K={33:3,35:5}[a]
    def stopped(shape):
        angles=[angle(shape[i-1],s) for i,s in enumerate(shape)]
        for i,(l,_,_) in enumerate(shape):
            ends=angles[i],angles[(i+1)%len(shape)]
            if any(min(v)>=2 for v in ends):continue
            if cmax(l)>K:continue
            for col,wall in ((0,b),(1,a)):
                if (max(v[col] for v in ends)<=1 and
                    min(shape[i-1][0],shape[(i+1)%len(shape)][0])>K*wall):return True
        return False
    @cache
    def ear(s,t,l,ll):
        shape=arc(board,s[:2],t[:2])+[(ll,*t[2:]),(l,s[2],(s[3]+3)%6)]
        if all(angle(shape[i-1],side) is not None for i,side in enumerate(shape)):
            return polygon_key(shape)
    edges=defaultdict(dict);incoming=defaultdict(set)
    for line in rows:
        if line.startswith('C'):continue
        _,_,_,i,t,l,h,j,k,u,m,g,q=map(int,line.split())
        s=(i,t,h,j);v=(k,u,g,q)
        assert v not in edges[s]
        edges[s][v]=(l,m);incoming[v].add(s)
    result=set();board_area=area(board)
    for u,neighbors in edges.items():
        for v,e in neighbors.items():
            if v[:2]<=u[:2] or v not in edges:continue
            for w in edges[v].keys() & incoming[u]:
                if w[:2]<=v[:2]:continue
                f=edges[v][w];k=edges[w][u]
                lengths=(f[0]-e[1],k[0]-f[1],e[0]-k[1]);axes=(v,w,u)
                if any(cmax(abs(l))<0 or not l for l in lengths):continue
                core=tuple((abs(l),p[2],(p[3]+3*(l<0))%6) for p,l in zip(axes,lengths))
                if any(angle(core[i-1],s) is None for i,s in enumerate(core)):continue
                mass=area(core)
                if mass.denominator!=1 or not 0<mass<board_area:continue
                cells=[ear(u,v,*e),ear(v,w,*f),ear(w,u,*k)]
                if None in cells:continue
                shape=tuple(sorted(cells+[polygon_key(core)],key=lambda z:(area(z),z)))
                if sum(map(area,shape))==board_area:result.add(shape)
    live=[r for r in result if not any(stopped(cell) for cell in r)]
    print('Unit tile',a,b,c,'board area',board_area,'layouts up to cell shapes',len(result),'after stopped-run check',len(live),flush=True)
    return sorted(live),len(result)

def replay(executable,a,b,c,board,shards=1):
    data=' '.join(map(str,(a,b,c,len(board),4)))+'\n'+''.join('%d %d %d\n'%row for row in board)
    with tempfile.TemporaryFile(mode='w+t') as output:
        for i in range(shards):
            subprocess.run([executable,str(shards),str(i)],input=data,text=True,stdout=output,check=True)
        output.seek(0)
        return analyze(a,b,c,board,output)

if __name__=='__main__':
    with tempfile.TemporaryDirectory() as tmp:
        exe=str(Path(tmp)/'ears');subprocess.run(['c++','-std=c++17','-O3',str(folder/'ears.cpp'),'-o',exe],check=True)
        for a,b,c,total,count in [(33,7,37,35,0),(35,13,43,137,3)]:
            side=2*a*b
            live,n=replay(exe,a,b,c,((side,0,0),(side,0,2),(side,0,4)),4)
            assert n==total and len(live)==count
            for row in live:print(row)

        a,b,c=33,7,37
        control=((4*b,0,0),(4*a,0,1),(4*c,-1,4))
        live,n=replay(exe,a,b,c,control,1)
        assert live and n>=1

        if '--boards' in sys.argv:
            for a,b,c,total,count in [(33,7,37,111,18),(35,13,43,200,67)]:
                board=((b*(2*a+b),0,0),(c*c,2,1),(a*(a+2*b),0,4))
                live,n=replay(exe,a,b,c,board,16)
                assert (n,len(live))==(total,count)
                saved=json.loads((folder/f"board_{(a+2*b)*(2*a+b)}.json").read_text())
                shapes={tuple(tuple(tuple(edge) for edge in cell) for cell in row["shapes"]) for row in saved}
                assert set(live)==shapes
