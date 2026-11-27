"""The physical owners of a positioned native path, in the reflected chart."""
from functools import lru_cache
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from native_positions import covered, cross, overlap
from terminal import UNITS, add, scale
from two_native import turn


def board(a, b, c):
    return ((0,0), scale(c*c, (a+b,-b)), scale(a*(a+2*b), (a,b)))


def inside(p, vertices):
    return all(cross(u,v,p) >= 0 for u,v in zip(vertices, vertices[1:]+vertices[:1]))


@lru_cache(None)
def offsets(a, b, c, hand, heading):
    z = (a,b) if hand == 1 else (a+b,-b)
    v = turn(z, heading)
    steps = [scale(c,u) for u in UNITS] + [v,scale(-1,v)]
    apex = [turn(scale(a,z),i) for i in range(6)]
    apex.extend((turn((a*c,0),heading),turn((a*c,0),heading+3)))
    return steps,apex


def triangle(P, Q, offset):
    R = add(P,offset)
    return (P,Q,R) if cross(P,Q,R)>0 else (Q,P,R)


def shape(a, b, c, hand, j, word):
    trace = [(0,0)]
    owners = []
    vertices = board(a,b,c)
    steps, apex = offsets(a,b,c,hand,j)
    for t in map(int, word):
        P = trace[-1]
        Q = add(P, scale(c,steps[t]))
        tri = triangle(P,Q,apex[t])
        if not all(inside(v,vertices) for v in tri) or any(overlap(tri,prev) for prev in owners):
            return None
        trace.append(Q)
        owners.append(tri)
    if any(covered(tuple(map(sum,zip(*tri))),trace) != int((int(t)>=6)==(hand==1))
           for t,tri in zip(word,owners)):
        return None
    return tuple(trace),tuple(owners)


@lru_cache(None)
def conflict(P,Q):
    return overlap(P,Q)


@lru_cache(None)
def winding(tri,path):
    return covered(tuple(map(sum,zip(*tri))),path)


def compatible(C,T):
    path_C,tiles_C = C
    path_T,tiles_T = T
    return (all(not conflict(p,q) for p in tiles_C for q in tiles_T)
            and all(winding(p,path_C)==1 for p in tiles_T)
            and all(winding(p,path_T)==0 for p in tiles_C))
