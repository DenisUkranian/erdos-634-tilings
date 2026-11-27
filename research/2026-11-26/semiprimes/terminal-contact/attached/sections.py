"""Exact section obstruction for the two 148-tile middle regions at 3431."""
from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path

import numpy as np

from native_owners import UNITS, add, scale
from middle_pairs import row
from terminal import det

HERE = Path(__file__).resolve().parent
a,b,c = 33,7,37


def residual(record):
    """Unit boundary chain after removing the two known owners from each cut."""
    j,k,axial,slant,w,u = record
    chain = Counter()
    for hand,heading,word in [(1,j,w),(-1,k,u)]:
        p = (0,0)
        for direction,length in row(a,b,c,hand,heading,word):
            for _ in range(length):
                q = add(p,UNITS[direction])
                edge = tuple(sorted((p,q)))
                chain[edge] += -hand if edge[0]==p else hand
                p = q
    successor = {}
    for (p,q),v in chain.items():
        if v:
            assert abs(v)==1
            if v<0:
                p,q = q,p
            assert p not in successor
            successor[p] = q
    p = min(successor)
    start = p
    vertices = []
    while p in successor:
        vertices.append(p)
        p = successor.pop(p)
    assert p==start and not successor
    assert sum(det(p,q) for p,q in zip(vertices,vertices[1:]+vertices[:1]))==a*b*(axial-slant-4)
    corners = []
    for i,p in enumerate(vertices):
        q,r = vertices[i-1],vertices[(i+1)%len(vertices)]
        if det((p[0]-q[0],p[1]-q[1]),(r[0]-p[0],r[1]-p[1])):
            corners.append(p)
    return np.array(corners,dtype=np.int64)


def multiply(p,q):
    x,y = p
    u,v = q
    return x*u-y*v,x*v+y*u+y*v


def lattice(polygon,mesh,shift):
    """Raster of legal corner sites, ordered by coordinates in the owner's mesh."""
    conjugate = mesh[0]+mesh[1],-mesh[1]
    corners = np.array([multiply(conjugate,(x-shift,y)) for x,y in polygon])
    lower = np.min(corners,axis=0)//(c*c)-a-b-1
    upper = np.max(corners,axis=0)//(c*c)+a+b+2
    i,k = np.ogrid[lower[0]:upper[0],lower[1]:upper[1]]
    x,y = multiply(mesh,(i,k))
    x = x+shift
    boundary = np.zeros(x.shape,dtype=bool)
    winding = np.zeros(x.shape,dtype=np.int8)
    for (u,v),(s,t) in zip(polygon,np.roll(polygon,-1,axis=0)):
        cross = (s-u)*(y-v)-(t-v)*(x-u)
        boundary |= ((cross==0)&(min(u,s)<=x)&(x<=max(u,s))&
                     (min(v,t)<=y)&(y<=max(v,t)))
        winding += ((v<=y)&(y<t)&(cross>0)).astype(np.int8)
        winding -= ((t<=y)&(y<v)&(cross<0)).astype(np.int8)
    inside = boundary | (winding!=0)
    return inside,np.stack((x,y),axis=-1)


def objects(polygon,mesh_hand,translate):
    """Group whole pairs and allow only singles whose long endpoints reach the other lift."""
    mesh = (c,0) if not mesh_hand else ((a,b) if mesh_hand==1 else (a+b,-b))
    inside,points = lattice(polygon,mesh,c*translate)
    i,k = np.nonzero(inside)
    q = points[i,k]
    groups = defaultdict(list)
    for j,(x,y) in enumerate(UNITS):
        for h in (-1,1):
            r,s = UNITS[(j+h)%6]
            I,K = i-a*x,k-a*y
            J,H = i+b*r,k+b*s
            u,w = points[I,K],points[J,H]
            good = inside[I,K]&inside[J,H]
            if j<3:
                mask = good & inside[I+b*r,K+b*s]
                shape = np.stack([u[mask],q[mask],w[mask],(u+w-q)[mask]],axis=1)
                groups['pairs'].append(shape)
            if mesh_hand:
                if h!=-mesh_hand:
                    continue
                mask = good & (u[:,0]%c==0) & (u[:,1]%c==0)
                assert np.all(w[mask]%c==0)
                groups['singles'].append(np.stack([u[mask],q[mask],w[mask],u[mask]],axis=1))
            else:
                coeff = (-(a if h==1 else b)*pow(b if h==1 else a,-1,c))%c
                g = ((u[:,0]//c)+coeff*(u[:,1]//c))%c
                assert np.array_equal(g,((w[:,0]//c)+coeff*(w[:,1]//c))%c)
                triangles = np.stack([u[good],q[good],w[good],u[good]],axis=1)
                for label in range(c):
                    groups[h,label].append(triangles[g[good]==label])
    return {g:np.concatenate(parts) for g,parts in groups.items()}


def rotate(points,axis):
    x,y = points[...,0],points[...,1]
    for _ in range(axis):
        x,y = -y,x+y
    return x,y


def fractions(x,y,t):
    """Edge crossings of 2x=t. A repeated corner pads triangles to four sites."""
    u,v = np.roll(x,-1,axis=-1),np.roll(y,-1,axis=-1)
    mask = (2*x<t)!=(2*u<t)
    numer = (2*y*(u-x)+(v-y)*(t-2*x))[mask]
    denom = (2*(u-x))[mask]
    div = np.gcd(numer,denom)*np.sign(denom)
    return mask,numer//div,denom//div


def reached(start,adj,lo,hi):
    seen = {start}
    todo = [start]
    while todo:
        for endpoint in adj.get(todo.pop(),()):
            if lo<=endpoint<=hi and endpoint not in seen:
                seen.add(endpoint)
                todo.append(endpoint)
    return seen


def section(polygon,shapes,axis,t):
    """Delete every crossing shape absent from all endpoint-to-endpoint interval paths."""
    x,y = rotate(polygon,axis)
    _,n,d = fractions(x,y,t)
    ends = sorted(Fraction(int(p),int(q)) for p,q in zip(n,d))
    x,y = rotate(shapes,axis)
    active = (2*x.min(axis=1)<t)&(t<2*x.max(axis=1))
    mask,n,d = fractions(x[active],y[active],t)
    assert np.all(mask.sum(axis=1)==2) and len(ends)%2==0
    intervals = []
    forward,back = defaultdict(set),defaultdict(set)
    # Intern fractions before building the endpoint graph.
    values = {(int(p),int(q)) for p,q in zip(n,d)}
    keys = {u:Fraction(*u) for u in values}
    for (u,v),(s,r) in zip(n.reshape(-1,2),d.reshape(-1,2)):
        lo,hi = sorted((keys[int(u),int(s)],keys[int(v),int(r)]))
        assert lo<hi
        forward[lo].add(hi)
        back[hi].add(lo)
        intervals.append((lo,hi))
    keep = np.zeros(len(intervals),dtype=bool)
    for lo,hi in zip(ends[::2],ends[1::2]):
        left = reached(lo,forward,lo,hi)
        if hi not in left:
            return None
        right = reached(hi,back,lo,hi)
        keep |= np.fromiter((p in left and q in right for p,q in intervals),dtype=bool)
    select = ~active
    select[active] = keep
    return shapes[select]


# Each odd numerator avoids every vertex of every candidate shape.
SECTIONS = (
    (0,79403), (1,-16131), (2,-95533),
    (0,89097), (1,-6437), (2,-91093),
    (0,98791), (1,3257), (2,-91907),
    (0,81549), (1,12951),
)


def check(record):
    corners = residual(record)
    polygon = c*corners
    B = objects(polygon,0,0)
    failures = Counter()
    indices = {-1:[],1:[]}
    for h in (-1,1):
        for t in range(c):
            child = objects(polygon,h,t)
            shapes = np.concatenate((B['pairs'],B[h,t],child['pairs'],child['singles']))
            for index,(axis,pos) in enumerate(SECTIONS):
                shapes = section(polygon,shapes,axis,pos)
                if shapes is None:
                    failures[axis,pos] += 1
                    indices[h].append(index)
                    break
            else:
                raise AssertionError((h,t))
    return dict(corners=corners.tolist(),rejected=sum(failures.values()),
                first_failing_indices_by_hand=indices,
                first_failing_slices=[[i,t,n] for (i,t),n in sorted(failures.items())])


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    rows = json.loads((HERE/'UNBOUNDED.json').read_text())['forced_two_lift_cases']
    assert len(rows)==2
    print(json.dumps([check(r) for r in rows],indent=2))
