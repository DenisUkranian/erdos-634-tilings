"""Full-board endpoint dual column generation; no orientation cutoff.

Every proposed certificate is checked on every contained placement incident to
one of its finitely many supported endpoint rows. Other placements have price 0.
"""
from pathlib import Path
import os, sys, time, math, json, pickle
from collections import Counter, defaultdict
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, hstack, vstack, eye, csr_matrix
from point_coverage import ExactGeometry
from sparse_dual import sparsify
from warm_lp import WarmLP
warm_phase=WarmLP();warm_exact=WarmLP();warm_steer=WarmLP()

a,b,c=map(int,sys.argv[1:4]);N=(a+2*b)*(2*a+b)
A,B=b*(2*a+b),a*(a+2*b)
pows=[c**e for e in range(257)]
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
def normpt(x,y,e):
 while e and x%c==0 and y%c==0:x//=c;y//=c;e-=1
 return int(x),int(y),e
def add(p,q):
 x,y,e=p;u,v,f=q;d=max(e,f)
 return normpt(x*pows[d-e]+u*pows[d-f],y*pows[d-e]+v*pows[d-f],d)
def mult(p,q):
 x,y,e=p;u,v,f=q
 return normpt(x*u-y*v,x*v+y*u+y*v,e+f)
def scale(k,p):return normpt(k*p[0],k*p[1],p[2])
@lru_cache(None)
def unit(h,j):
 if j%6:return mult(unit(h,0),(*U[j%6],0))
 if h==0:return 1,0,0
 return mult((a,b,1) if h>0 else (a+b,-b,1),unit(h-(1 if h>0 else -1),0))
coin=bytearray(max(A,B,c*c)+1);coin[0]=1
for i in range(1,len(coin)):coin[i]=any(i>=n and coin[i-n] for n in (a,b,c))
@lru_cache(250000)
def legal(p):
 x,y,e=p;d=pows[e]
 if x<0 or y<0 or B*x+A*y>A*B*d:return False
 if y==0 and (x%d or not (coin[x//d] and coin[A-x//d])):return False
 if x==0 and (y%d or not (coin[y//d] and coin[B-y//d])):return False
 if B*x+A*y==A*B*d:
  q,r=divmod(x*c*c,A*d)
  if r or not (coin[q] and coin[c*c-q]):return False
 return True
@lru_cache(None)
def template(h,j,s):
 u=scale(-a,unit(h,j));w=scale(b,unit(h,(j+s)%6));o=(0,0,0)
 return ((u,h,j%3,-s),(o,h,j%3,s),(o,h,(j+s)%3,-s),(w,h,(j+s)%3,s),(w,h+s,j%3,-s),(u,h+s,j%3,s))
@lru_cache(None)
def inverse(h,j):
 ret=[]
 for H in (h-1,h,h+1):
  for J in range(6):
   for s in (1,-1):
    for p,hh,jj,x in template(H,J,s):
     if (hh,jj)==(h,j):ret.append((scale(-1,p),H,J,s,x))
 return ret

def tile_rows(key):
 q,h,j,s=key
 return [( (add(q,off),H,J),w) for off,H,J,w in template(h,j,s)]
@lru_cache(250000)
def admissible(key):
 q,h,j,s=key;T=template(h,j,s)
 return legal(q) and legal(add(q,T[0][0])) and legal(add(q,T[3][0]))

needs=Counter()
def ext(P,Q,h,j):
 needs[P,h,j]-=1;needs[Q,h,j]+=1
ext((0,0,0),(A,0,0),0,0)
ext((A,0,0),(0,B,0),2,1)
ext((0,B,0),(0,0,0),0,1)
rows={};cols=[];tiles={};cost=[];matI=[];matJ=[];matV=[];heads=[]
def rowid(row):
 if row not in rows:rows[row]=len(rows);heads.append(needs[row])
 return rows[row]
BUILDING_SEED=True
negative_map={}
def addcol(key,negative=False):
 if not negative and key in tiles:return tiles[key]
 i=len(cols);cols.append((key,negative));cost.append(1.0 if negative else 0.0)
 if not negative:tiles[key]=i
 else:negative_map[key]=i
 for row,v in tile_rows(key):
  if BUILDING_SEED or row in rows:
   matI.append(rowid(row));matJ.append(i);matV.append(-v if negative else v)
 return i

def toP(p,den):
 e=0
 while pows[e]<den:e+=1
 assert pows[e]==den
 return normpt(*p,e)
inv={scale(a,unit(h,j)):(h,j) for h in range(-60,61) for j in range(6)}
def tkey(T):
 for i in range(3):
  for k in (1,2):
   q=T[i];p=T[(i+k)%3];r=T[(i+3-k)%3]
   au=add(q,scale(-1,p))
   if au not in inv:continue
   h,j=inv[au];bv=add(r,scale(-1,q))
   for s in (1,-1):
    if bv==scale(b,unit(h,(j+s)%6)):return q,h,j,s
 raise RuntimeError(T)
seed=Counter()
seed_path=Path(os.environ['SEED_JSON']) if os.getenv('SEED_JSON') else Path(__file__).with_name(f'seed_{N}.json')
data=json.loads(seed_path.read_text());assert data['sides']==[a,b,c];den=data['denominator']
for T,w in data['signed']:seed[tkey(tuple(toP(p,den) for p in T))]+=w
x0=[];negative_indices=[]
for T,w in seed.items():
 if not w:continue
 i=addcol(T)
 while len(x0)<len(cols):x0.append(0)
 if w>0:x0[i]=w
 else:
  j=addcol(T,True);negative_indices.append(j)
  while len(x0)<len(cols):x0.append(0)
  x0[j]=-w
assert sum(seed.values())==N
M=coo_matrix((matV,(matI,matJ)),shape=(len(rows),len(cols))).tocsc()
assert np.max(np.abs(M@np.array(x0)-np.array(heads)))==0
print('seed',N,'positive mass',sum(max(w,0) for w in seed.values()),'negative mass',sum(max(-w,0) for w in seed.values()),'rows',len(rows),'columns',len(cols),flush=True)
for row in needs:rowid(row)
BUILDING_SEED=False

def install_row(row):
 if row in rows:return
 idx=rowid(row);p,h,j=row
 for off,H,J,sg,w in inverse(h,j):
  T=(add(p,off),H,J,sg)
  if T in tiles:matI.append(idx);matJ.append(tiles[T]);matV.append(w)
  if T in negative_map:matI.append(idx);matJ.append(negative_map[T]);matV.append(-w)

start_iteration=0
state={}
if os.getenv('RESUME'):
 with open(os.environ['RESUME'],'rb') as f:state=pickle.load(f)
 assert tuple(state['sides'])==(a,b,c)
 rows=state['rows'];cols=state['cols'];cost=state['cost'];matI=state['matI'];matJ=state['matJ'];matV=state['matV'];heads=state['heads'];needs=state['needs'];tiles=state['positive_keys']
 negative_map={T:i for i,(T,negative) in enumerate(cols) if negative}
 start_iteration=state['iteration']+1
 print('RESUMED',start_iteration,'rows',len(rows),'cols',len(cols),flush=True)

coverage=ExactGeometry(c,template,add,pows)
for p in state.get('coverage_points',[]):coverage.append(tuple(p))
cutI=state.get('coverage_I',[]);cutJ=state.get('coverage_J',[]);cutV=state.get('coverage_V',[])
base_addcol=addcol
def addcol(key,negative=False):
 before=len(cols);i=base_addcol(key,negative)
 if i==before:
  mask=coverage.mask(key)
  while mask:
   bit=mask & -mask;cutI.append(bit.bit_length()-1);cutJ.append(i);cutV.append(-1 if negative else 1);mask-=bit
 return i

def install_cut(p):
 k=coverage.append(p)
 if k is None:return False
 count=0
 for i,(key,negative) in enumerate(cols):
  if coverage.contains(key,p):cutI.append(k);cutJ.append(i);cutV.append(-1 if negative else 1);count+=1
 print('installed point cut',k,'nonzeros',count,'denominator digits',len(str(p[2])),flush=True)
 return True

def point_score(key,dual):
 mask=coverage.mask(key);value=0
 while mask:
  bit=mask & -mask;value+=dual[bit.bit_length()-1];mask-=bit
 return value

def discover_cuts(solution):
 if len(coverage.cuts)>=int(os.getenv('MAX_POINT_CUTS','240')):return 0
 found,detail=coverage.discover(cols,solution,seed,
  maximum=min(int(os.getenv('CUTS_PER_ITER','12')),int(os.getenv('MAX_POINT_CUTS','240'))-len(coverage.cuts)),
  centroid_limit=int(os.getenv('CUT_CENTROIDS','1200')),pair_limit=int(os.getenv('CUT_PAIRS','2000')))
 print('point separation',detail,'new',len(found),flush=True)
 for p,value,seedvalue in found:
  assert seedvalue<=1
  install_cut(p)
 return len(found)

def checkpoint(iteration):
 state=dict(sides=(a,b,c),rows=rows,cols=cols,cost=cost,matI=matI,matJ=matJ,matV=matV,heads=heads,needs=needs,iteration=iteration,positive_keys=tiles,
  coverage_points=coverage.cuts,coverage_I=cutI,coverage_J=cutJ,coverage_V=cutV)
 dest=Path(f'checkpoint_{N}.pickle');tmp=dest.with_suffix('.tmp')
 with tmp.open('wb') as f:pickle.dump(state,f)
 tmp.replace(dest)

# Exact pricing of a finite integer endpoint certificate, including all h.
def certify(y,point_duals,iteration):
 scale0=int(os.getenv('CERT_SCALE','100000000'))
 weights={row:int(round(float(y[i])*scale0)) for row,i in rows.items() if abs(y[i])*scale0>=.5}
 cutweights=[min(0,int(round(float(v)*scale0))) for v in point_duals]
 candidates=set()
 for (p,h,j),w in weights.items():
  for off,H,J,s,_ in inverse(h,j):
   T=(add(p,off),H,J,s)
   if admissible(T):candidates.add(T)
 price={T:sum(weights.get(row,0)*v for row,v in tile_rows(T))+point_score(T,cutweights) for T in candidates}
 bound=sum(needs.get(row,0)*w for row,w in weights.items())+sum(cutweights);maxprice=max(0,max(price.values(),default=0));top_sum=sum(sorted((v for v in price.values() if v>0),reverse=True)[:N]);margin=bound-top_sum
 print('exact certificate trial',iteration,'boundary',bound,'max tile',maxprice,'top N',top_sum,'margin',margin,'support',len(weights),'priced',len(candidates),flush=True)
 if margin>0:
  out=dict(format='endpoint-current-dual-v1',sides=[a,b,c],N=N,scale=scale0,boundary=bound,max_tile=maxprice,top_N=top_sum,margin=margin,
   board=[[0,0],[A,0],[0,B]],boundary_arithmetic=True,
   rows=[dict(point=[str(__import__('fractions').Fraction(p[0],pows[p[2]])),str(__import__('fractions').Fraction(p[1],pows[p[2]]))],height=h,phase=j,weight=-w) for (p,h,j),w in weights.items()],
   point_penalties=[dict(point=[str(__import__('fractions').Fraction(x,d)),str(__import__('fractions').Fraction(y,d))],weight=-w) for (x,y,d),w in zip(coverage.cuts,cutweights) if w])
  Path(f'GLOBAL_CERT_{N}.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
  print('GLOBAL STRICT CERTIFICATE',N,margin,flush=True)
  return True
 return False

for it in range(start_iteration,int(os.getenv('ITERATIONS','10000'))):
 if it%10==0:checkpoint(it-1)
 t0=time.time();nr,nc=len(rows),len(cols)
 mat=coo_matrix((matV,(matI,matJ)),shape=(nr,nc)).tocsc()
 budget=np.array([-1.0 if neg else 1.0 for key,neg in cols])
 cutmatrix=coo_matrix((cutV,(cutI,cutJ)),shape=(len(coverage.cuts),nc)).tocsr()
 inequalities=vstack([csr_matrix(budget.reshape(1,nc)),cutmatrix],format='csr')
 inequality_rhs=np.r_[N,np.ones(len(coverage.cuts))]
 identity=eye(nr,format='csc')
 phase_matrix=hstack([mat,identity,-identity],format='csc')
 phase_cost=np.r_[cost,np.full(2*nr,float(os.getenv('ARTIFICIAL_COST','1')))]
 phase_inequalities=hstack([inequalities,csr_matrix((len(coverage.cuts)+1,2*nr))],format='csr')
 real_bounds=[(0,None if negative else (1 if admissible(T) else 0)) for T,negative in cols]
 res=warm_phase.solve(phase_cost,layout=(nr,nc,True),A_eq=phase_matrix,b_eq=heads,A_ub=phase_inequalities,b_ub=inequality_rhs,bounds=real_bounds+[(0,None)]*(2*nr),method='highs-ds',options={'threads':1,'time_limit':int(os.getenv('LP_LIMIT','60'))})
 print('warm primary',res.warm_start,'iterations',res.nit,'seconds',res.seconds,flush=True)
 if not res.success:print('LP STOP',res.message,flush=True);checkpoint(it-1);break
 artificial_mass=float(res.x[nc:].sum());res.x=res.x[:nc]
 negative_mass=sum(float(res.x[i]) for i,(T,negative) in enumerate(cols) if negative)
 y=np.array(res.eqlin.marginals);y[np.abs(y)<1e-10]=0
 budget_dual=float(res.ineqlin.marginals[0]);assert budget_dual<=1e-8
 point_duals=np.minimum(0,np.array(res.ineqlin.marginals[1:]));assert all(v<=1e-8 for v in res.ineqlin.marginals[1:])
 if res.fun<1e-8:y[:]=0;budget_dual=0.0;point_duals[:]=0
 if res.fun>1e-8 and os.getenv('SPARSE_DUAL','1')=='1' and np.count_nonzero(y)>int(os.getenv('SPARSE_THRESHOLD','2000')):
  sparse,detail=sparsify(mat,np.array(heads),inequalities,inequality_rhs,np.array(cost),
   np.array([not negative and admissible(T) for T,negative in cols]),np.array([negative for T,negative in cols]),res.fun,
   endpoint_cap=float(os.getenv('ARTIFICIAL_COST','1')),keep_fraction=float(os.getenv('SPARSE_FRACTION','0.5')),time_limit=int(os.getenv('SPARSE_LIMIT','30')))
  print('sparse pricing dual',detail,flush=True)
  if sparse is not None:
   y,duals=sparse;budget_dual=min(0,float(duals[0]));point_duals=np.minimum(0,duals[1:]);y[np.abs(y)<1e-10]=0
 support=[(r,float(y[i])) for r,i in rows.items() if y[i]]
 candidates=set()
 for (p,h,j),w in support:
  for off,H,J,s,_ in inverse(h,j):
   T=(add(p,off),H,J,s)
   if T not in tiles and admissible(T):candidates.add(T)
 prices=[(sum(y[rows[r]]*v for r,v in tile_rows(T) if r in rows)+budget_dual+point_score(T,point_duals),T) for T in candidates]
 prices.sort(reverse=True)
 bad=[(w,T) for w,T in prices if w>1e-8]
 worst=bad[0][0] if bad else 0
 print(it,'rows',nr,'cols',nc,'cuts',len(coverage.cuts),'phaseI',res.fun,'negative_mass',negative_mass,'artificial_mass',artificial_mass,'support',len(support),'priced',len(candidates),'bad',len(bad),'maxprice',worst,'budgetdual',budget_dual,'seconds',round(time.time()-t0,3),flush=True)
 if res.fun<1e-8:
  steer_cost=np.array([-1.0 if not negative and seed.get(T,0)>0 else 0.0 for T,negative in cols])
  steer_bounds=[(0,0 if negative or not admissible(T) else 1) for T,negative in cols]
  steer=None
  if os.getenv('STEER_EXACT_AREA','1')!='0':
   steer=warm_exact.solve(steer_cost,layout=(nr,nc,False),A_eq=vstack([mat,csr_matrix(budget.reshape(1,nc))],format='csr'),b_eq=np.r_[heads,N],A_ub=inequalities,b_ub=inequality_rhs,bounds=steer_bounds,method='highs-ds',options={'threads':1,'time_limit':int(os.getenv('LP_LIMIT','60'))})
   print('exact-area steering',steer.message,flush=True)
  if steer is None or not steer.success:
   steer=warm_steer.solve(steer_cost,layout=(nr,nc,False),A_eq=mat,b_eq=heads,A_ub=inequalities,b_ub=inequality_rhs,bounds=steer_bounds,method='highs-ds',options={'threads':1,'time_limit':int(os.getenv('LP_LIMIT','60'))})
  if steer.success:
   res.x=steer.x
   print('primal steering','retained seed mass',-steer.fun,'positive mass',float(budget@res.x),'seconds',round(time.time()-t0,3),flush=True)
  else:print('primal steering unavailable',steer.message,flush=True)
  newcuts=discover_cuts(res.x)
  if newcuts and os.getenv('JOINT_ROWS','1')!='1':
   checkpoint(it)
   continue
  residual=Counter()
  for i in np.flatnonzero(res.x>1e-8):
   T,neg=cols[i]
   for r,w in tile_rows(T):residual[r]+=res.x[i]*w*(-1 if neg else 1)
  badrows=sorted([(abs(w-needs.get(r,0)),r) for r,w in residual.items() if r not in rows and abs(w-needs.get(r,0))>1e-7],reverse=True)
  for r,w in needs.items():
   if w and r not in residual and r not in rows:badrows.append((abs(w),r))
  print('row generation','violations',len(badrows),'active positives',sum(res.x[i]>1e-8 for i in tiles.values()),flush=True)
  if not badrows and newcuts:
   checkpoint(it)
   continue
  if not badrows:
   selected=[(cols[i][0],float(x)) for i,x in enumerate(res.x) if x>1e-8 and not cols[i][1]]
   Path(f'positive_solution_{N}.json').write_text(json.dumps(selected,separators=(',',':'))+'\n');print('ZERO NEGATIVE COMPLETE LP',N,flush=True);break
  for w,r in badrows[:int(os.getenv('GROW','1500'))]:install_row(r)
  checkpoint(it)
  continue
 if worst* N < res.fun*.99 or not bad:
  if certify(y,point_duals,it):break
 if not bad:
  print('No float violating column but no strict exact certificate',flush=True);break
 chosen=bad[:int(os.getenv('BATCH','3000'))]
 for w,T in chosen:addcol(T)
 if os.getenv('CUT_POSITIVE_PHASE','0')=='1' and it%int(os.getenv('CUT_INTERVAL','5'))==0:discover_cuts(res.x)
 if it%10==0:checkpoint(it)
