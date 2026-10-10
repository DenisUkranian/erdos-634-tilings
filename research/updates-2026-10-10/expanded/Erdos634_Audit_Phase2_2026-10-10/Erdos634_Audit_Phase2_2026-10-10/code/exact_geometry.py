"""New small rational geometry kernel for the Phase-2 audit.
No project generator/checker is imported. Closed convex polygons, exact area.
"""
from fractions import Fraction as F

def p(x,y): return (F(x),F(y))
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def mul(k,a):return k*a[0],k*a[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def side(a,b,c):return det(sub(b,a),sub(c,a))
def signed2(poly):
 return sum(det(a,b) for a,b in zip(poly,poly[1:]+poly[:1]))
def clean(poly):
 out=[]
 for x in poly:
  if not out or x!=out[-1]:out.append(x)
 if len(out)>1 and out[0]==out[-1]:out.pop()
 return out
def ccw(poly):
 poly=clean(list(poly))
 return poly if signed2(poly)>=0 else poly[::-1]
def inside_convex(poly,point):
 poly=ccw(poly)
 return all(side(a,b,point)>=0 for a,b in zip(poly,poly[1:]+poly[:1]))
def clip(subject,window):
 """Sutherland-Hodgman: return exact convex intersection polygon."""
 out=ccw(subject)
 for a,b in zip(ccw(window),ccw(window)[1:]+ccw(window)[:1]):
  inp=out;out=[]
  if not inp:break
  prev=inp[-1];sp=side(a,b,prev)
  for cur in inp:
   sc=side(a,b,cur)
   if (sp<0<=sc) or (sc<0<=sp):
    lam=sp/(sp-sc);out.append(add(prev,mul(lam,sub(cur,prev))))
   if sc>=0:out.append(cur)
   prev,sp=cur,sc
  out=clean(out)
 return out
def intersect_area2(a,b):return abs(signed2(clip(a,b)))
def box(poly):return (min(x for x,y in poly),max(x for x,y in poly),min(y for x,y in poly),max(y for x,y in poly))
def boxes_overlap(a,b):return a[0]<b[1] and b[0]<a[1] and a[2]<b[3] and b[2]<a[3]
def point_in_open_edge(x,a,b):
 return side(a,b,x)==0 and x!=a and x!=b and min(a,b)<x<max(a,b)
