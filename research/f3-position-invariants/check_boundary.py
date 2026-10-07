#!/usr/bin/env python3
"""Exact one-side collar search; no claim of filling the remaining polygon."""
from fractions import Fraction as F
import json

def add(p,q): return (p[0]+q[0],p[1]+q[1])
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def mul(p,q): return (p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def conj(p): return (p[0]+p[1],-p[1])
def norm(p): return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def turn(p,q,r): return cross(sub(q,p),sub(r,p))
def inside(P,p): return all(turn(P[i],P[(i+1)%len(P)],p)>=0 for i in range(len(P)))
def overlaps(P,Q):
    for A,B in ((P,Q),(Q,P)):
        for i in range(len(A)):
            p,q=A[i],A[(i+1)%len(A)]
            if all(turn(p,q,r)<=0 for r in B): return False
    return True

def thirds(a,b,c):
    R=[(F(0),F(0)),(F(a),F(0)),(F(a),F(b))]
    out={a:set(),b:set(),c:set()}
    for i in range(3):
        for j in range(3):
            if i==j: continue
            k=3-i-j;v=sub(R[j],R[i]); nn=norm(v)
            l=next(x for x in (a,b,c) if x*x==nn)
            w=mul(sub(R[k],R[i]),conj(v));w=(w[0]*l/nn,w[1]*l/nn)
            if w[1]<0: w=conj(w)
            out[l].add(w)
    return {k:sorted(v) for k,v in out.items()}

def solve(P,L,a,b,c):
    forms=thirds(a,b,c); calls=0
    cache={}
    def options(x):
        if x in cache:return cache[x]
        answer=[]
        for l in (c,a,b):
            if x+l>L:continue
            for q in forms[l]:
                T=[(F(x),F(0)),(F(x+l),F(0)),add((F(x),F(0)),q)]
                if all(inside(P,p) for p in T):answer.append((l,T))
        cache[x]=answer;return answer
    def dfs(x,seq):
        nonlocal calls
        calls+=1
        if x==L:return seq
        for l,T in options(x):
            if any(overlaps(T,U) for _,U in seq):continue
            ans=dfs(x+l,seq+[(l,T)])
            if ans is not None:return ans
        return None
    ans=dfs(0,[])
    encode=lambda P:[[str(x),str(y)]for x,y in P]
    return {'status':'COLLAR_EXISTS' if ans else 'NO_ONE_SIDE_COLLAR',
            'scope':'only complete coverage of the side from (0,0) to (L,0)',
            'tile':[a,b,c], 'target':encode(P), 'side_length':L,'states':calls,
            'lengths': None if ans is None else [l for l,_ in ans],
            'triangles':None if ans is None else [encode(T)for _,T in ans],
            'full_gamma_tiling_proved':False}

if __name__=='__main__':
    P=[(F(0),F(0)),(F(194),F(0)),(F(506),F(143)),(F(242),F(528))]
    result=solve(P,194,24,11,31)
    ts=[[(F(x),F(y))for x,y in T]for T in result['triangles']]
    more=[]
    for j in range(1,4):
        more.append([(F(j*31),F(0)),ts[j][2],ts[j-1][2]])
    more += [[(124,0),(113,11),(89,11)],
             [(148,0),(137,11),(113,11)],
             [(172,0),(161,11),(137,11)],
             [(183,0),(159,24),(148,24)]]
    for T in more:
        if turn(*T)<0:T.reverse()
        ts.append(T)
    pairs=0
    for i,T in enumerate(ts):
        assert all(inside(P,p)for p in T)
        assert sorted(norm(sub(T[(j+1)%3],T[j]))for j in range(3))==[121,576,961]
        assert turn(*T)==264
        for U in ts[:i]:
            assert not overlaps(T,U)
            pairs+=1
    result['extended_patch_triangles']=[[[str(x),str(y)]for x,y in T]for T in ts]
    result['extended_patch_count']=len(ts)
    result['all_pair_checks']=pairs
    result['verification']='PASS: exact containment, congruence, nonoverlap'
    result['collar_status']=result['status']
    result['status']='PASS'
    result['full_Erdos634_solved']=False
    print(json.dumps(result,indent=2))
