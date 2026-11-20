"""Exact strict-interior point cuts; spatial bins are used only to find cuts."""
from collections import defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from math import floor, gcd


def point(x, y, d=1):
    assert d > 0
    g = gcd(gcd(abs(x), abs(y)), d)
    return x // g, y // g, d // g


def from_fractions(x, y):
    d = x.denominator * y.denominator
    return point(x.numerator * y.denominator, y.numerator * x.denominator, d)


class ExactGeometry:
    def __init__(self, c, template, add, powers):
        self.c, self.template, self.add, self.powers = c, template, add, powers
        self.cuts = []
        self.cut_set = set()
        self.mask_cache = {}

    @lru_cache(150000)
    def geometry(self, key):
        anchor, h, j, s = key
        t = self.template(h, j, s)
        v = (self.add(anchor, t[0][0]), anchor, self.add(anchor, t[3][0]))
        e = max(p[2] for p in v)
        d = self.powers[e]
        v = tuple((x * self.powers[e-k], y * self.powers[e-k]) for x,y,k in v)
        cross = lambda p,q: p[0]*q[1]-p[1]*q[0]
        area = sum(cross(v[i], v[(i+1)%3]) for i in range(3))
        assert area
        if area < 0:
            v = tuple(reversed(v))
        edges = []
        for i,(x,y) in enumerate(v):
            xx,yy = v[(i+1)%3]
            dx,dy = xx-x,yy-y
            coeff = (-dy*d, dx*d, dy*x-dx*y)
            g = gcd(gcd(abs(coeff[0]),abs(coeff[1])),abs(coeff[2]))
            edges.append(tuple(z//g for z in coeff))
        box = (min(x for x,y in v), max(x for x,y in v),
               min(y for x,y in v), max(y for x,y in v))
        return v,d,tuple(edges),box

    def contains(self, key, p):
        v,d,edges,box = self.geometry(key)
        x,y,q = p
        xx,yy = x*d,y*d
        if xx <= box[0]*q or xx >= box[1]*q or yy <= box[2]*q or yy >= box[3]*q:
            return False
        return all(A*x+B*y+C*q > 0 for A,B,C in edges)

    def centroid(self, key):
        v,d,_,_ = self.geometry(key)
        return point(sum(x for x,y in v),sum(y for x,y in v),3*d)

    def mask(self, key):
        old,mask = self.mask_cache.get(key,(0,0))
        for i in range(old,len(self.cuts)):
            if self.contains(key,self.cuts[i]):
                mask |= 1 << i
        if len(self.mask_cache)>350000:
            self.mask_cache.clear()
        self.mask_cache[key]=(len(self.cuts),mask)
        return mask

    def append(self, p):
        if p in self.cut_set:
            return None
        i=len(self.cuts)
        self.cuts.append(p)
        self.cut_set.add(p)
        return i

    def overlap_point(self, one, two):
        def vertices(key):
            v,d,_,_=self.geometry(key)
            return [(Q(x,d),Q(y,d)) for x,y in v]
        poly,wall=vertices(one),vertices(two)
        cross=lambda p,q:p[0]*q[1]-p[1]*q[0]
        sub=lambda p,q:(p[0]-q[0],p[1]-q[1])
        for i,left in enumerate(wall):
            right=wall[(i+1)%3];edge=sub(right,left)
            if not poly:return None
            out=[];start=poly[-1];fs=cross(edge,sub(start,left))
            for end in poly:
                fe=cross(edge,sub(end,left))
                if (fs>=0)!=(fe>=0):
                    t=fs/(fs-fe)
                    out.append((start[0]+t*(end[0]-start[0]),start[1]+t*(end[1]-start[1])))
                if fe>=0:out.append(end)
                start,fs=end,fe
            poly=out
        if len(poly)<3 or sum(cross(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))==0:
            return None
        p=from_fractions(sum(x for x,y in poly)/len(poly),sum(y for x,y in poly)/len(poly))
        assert self.contains(one,p) and self.contains(two,p)
        return p

    def discover(self, cols, solution, seed, maximum=12, centroid_limit=1000, pair_limit=2000):
        """Find violated cuts. Every returned point is exact and seed-feasible.

        Spatial bins and finite search limits affect only discovery, never the
        exact matrix coefficients or global reduced-cost oracle.
        """
        signed=defaultdict(float)
        positive={}
        for (key,negative),value in zip(cols,solution):
            if value>1e-8:
                signed[key]+=(-value if negative else value)
                if not negative:positive[key]=float(value)
        signed={k:w for k,w in signed.items() if abs(w)>1e-9}
        keys=sorted(positive,key=lambda k:positive[k],reverse=True)
        size=float(self.c)
        bins=defaultdict(set)
        for key in signed:
            _,d,_,box=self.geometry(key)
            # One-cell padding makes the heuristic robust to float endpoints.
            for ix in range(floor((box[0]/d)/size)-1,floor((box[1]/d)/size)+2):
                for iy in range(floor((box[2]/d)/size)-1,floor((box[3]/d)/size)+2):
                    bins[ix,iy].add(key)
        proposed={}
        def consider(p):
            if p is None or p in self.cut_set or p in proposed:return
            x,y,d=p;near=bins[floor((x/d)/size),floor((y/d)/size)]
            value=sum(signed[k] for k in near if self.contains(k,p))
            if value>1+1e-7:proposed[p]=value
        for key in keys[:centroid_limit]:consider(self.centroid(key))
        seen=set();tried=0
        for key in keys:
            if tried>=pair_limit:break
            _,d,_,box=self.geometry(key)
            near=set()
            for ix in range(floor((box[0]/d)/size),floor((box[1]/d)/size)+1):
                for iy in range(floor((box[2]/d)/size),floor((box[3]/d)/size)+1):near.update(bins[ix,iy])
            for other in sorted(near,key=lambda k:positive.get(k,0),reverse=True):
                if other==key or other not in positive:continue
                pair=tuple(sorted((key,other)))
                if pair in seen:continue
                seen.add(pair)
                _,dd,_,bb=self.geometry(other)
                if box[1]*dd<=bb[0]*d or bb[1]*d<=box[0]*dd or box[3]*dd<=bb[2]*d or bb[3]*d<=box[2]*dd:continue
                tried+=1
                consider(self.overlap_point(key,other))
                if tried>=pair_limit:break
        result=[]
        for p,value in sorted(proposed.items(),key=lambda x:x[1],reverse=True):
            # At a seed edge the strict signed indicator can jump. Keep the
            # original exact feasible seed, rather than assume genericity.
            seed_value=sum(w for key,w in seed.items() if w and self.contains(key,p))
            if seed_value<=1:
                exact_value=sum(w for key,w in signed.items() if self.contains(key,p))
                if exact_value>1+1e-7:result.append((p,exact_value,seed_value))
            if len(result)>=maximum:break
        return result,dict(centroids=min(len(keys),centroid_limit),pair_tests=tried,violations=len(proposed))
