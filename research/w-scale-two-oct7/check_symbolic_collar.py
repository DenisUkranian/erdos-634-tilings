#!/usr/bin/env python3
"""Universal exact nine-tile collar; coefficients are in v-3, not samples."""
from pathlib import Path
from itertools import permutations
import argparse,importlib.util,json
P=Path(__file__).resolve().parents[1]/'elliptic-sectors'/'check_alpha_maps.py'
spec=importlib.util.spec_from_file_location('rat_poly',P);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
R=M.RationalFunction

def z(x):return x if isinstance(x,R) else R(x)
def val(x):x=z(x);return x.n[0]/x.d[0]
def eq(x,y):return not any((z(x)-y).n)
def nonnegative(x):
 x=z(x)
 if not any(x.n):return True
 return (all(a>=0 for a in x.n) and all(a>=0 for a in x.d) and x.d[0]>0) or (all(a<=0 for a in x.n) and all(a<=0 for a in x.d) and x.d[0]<0)
def add(P,Q):return tuple(x+y for x,y in zip(P,Q))
def sub(P,Q):return tuple(x-y for x,y in zip(P,Q))
def mul(P,k):return tuple(x*k for x in P)
def cross(P,Q):return P[0]*Q[1]-P[1]*Q[0]
def orient(P,Q,S):return cross(sub(Q,P),sub(S,P))
def ccw(T):return T if val(orient(*T))>0 else (T[0],T[2],T[1])
def edges(T):return zip(T,T[1:]+T[:1])

def verify():
 v=R((3,1));u=v-1;a=u*v;b=2*v-1;c=v*v;Q=b+c;D=4*v*v-u*u
 C=(R(0),R(0));A=(2*(a+c),R(0));O=((2*v**4-4*v*v*u*u+u**4)/v,u*Q/v)
 r=b*Q/(2*c);h=b*u/(2*c);s=b*(b-c)/(2*a);k=b/(2*v)
 R0=(r,h);R1=(c+r,h);S0=(2*c+s,k);S1=(2*c+a+s,k)
 J1=(c,R(0));J2=(2*c,R(0));J3=(2*c+a,R(0))
 P=mul(O,1/(2*v));W=add(A,mul(sub(O,A),b/(2*u*Q)));U=add(J2,mul(sub(R1,J2),c/a))
 target=ccw((C,A,O))
 def norm(P):return P[0]**2+D*P[1]**2
 assert eq(norm(sub(A,C)),(2*v*b)**2)
 assert eq(norm(sub(O,C)),(2*v**3)**2)
 assert eq(norm(sub(O,A)),(2*u*Q)**2)
 assert eq(orient(*target),4*Q*b*u/2)
 tiles=list(map(ccw,[(C,J1,R0),(J1,J2,R1),(J2,J3,S0),(J3,A,S1),
                    (C,R0,P),(A,S1,W),(J1,R0,R1),(J3,S0,S1),(J2,S0,U)]))
 for i,T in enumerate(tiles):
  assert eq(orient(*T),b*u/2),('area',i)
  squared=[(p[0]-q[0])**2+D*(p[1]-q[1])**2 for p,q in edges(T)]
  assert any(all(eq(x,y) for x,y in zip(squared,perm)) for perm in permutations([a*a,b*b,c*c])),('metric',i)
  for p,q in edges(target):
   for V in T:assert nonnegative(orient(p,q,V)),('containment',i)
 separators=[]
 for i in range(9):
  for j in range(i):
   axes=[]
   for ti,tj in [(i,j),(j,i)]:
    for ei,(p,q) in enumerate(edges(tiles[ti])):
     if all(nonnegative(-orient(p,q,V)) for V in tiles[tj]):axes.append((ti,ei))
   assert axes,('separation',i,j)
   separators.append({'pair':[i,j],'separating_tile_edge':list(axes[0])})
 return {'status':'PASS','range':'all real v>=3, hence every integer v>=3',
         'proof_method':'exact rational identities and nonnegative coefficients in v-3',
         'tiles':9,'all_pair_checks':36,'tile_area_det':'b*u/2','separators':separators,
         'claim':'The ccaa side has an actual nine-tile collar completing all its five boundary fans.',
         'whole_target_tiled':False,'W_scale_two_decided':False,'full_Erdos634_solved':False}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--report',type=Path)
 args=parser.parse_args()
 report=verify()
 if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='separators'},indent=2))
