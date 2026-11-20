from path_core import *
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

def solve(a,b,c):
 units=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
 def phi(p):return (b*p[0]+(a+b)*p[1])%c
 def col(j,s,r):
  aa=phi(tb(a,units[j]));bb=phi(tb(b,units[(j+s)%6]))
  i=j%3*c;ii=(j+s)%3*c
  return [(i+r,s),(i+(r-aa)%c,-s),(ii+(r+bb)%c,s),(ii+r,-s)]
 columns=[];cost=[]
 for j in range(6):
  for r in range(c):
    columns.append(col(j,1,r));cost.append(1)
 for j in range(3):
  aa=phi(tb(a,units[j]));bb=phi(tb(b,units[(j-1)%6]))
  for r in range(c):
    columns.append(col(j,-1,r)+col(j+3,-1,(r-aa+bb)%c));cost.append(2)
 rhs=np.zeros(3*c)
 for i,n in col(0,-1,a*b%c):rhs[i]-=c*n
 entries=[(i,j,n) for j,cl in enumerate(columns) for i,n in cl]
 ii,jj,nn=zip(*entries);M=coo_matrix((nn,(ii,jj)),shape=(3*c,len(columns))).tocsc()
 res=linprog(cost,A_eq=M,b_eq=rhs,bounds=(0,None),method='highs')
 if res.success: print(a,b,c,'minimum n1=',res.fun+c,'N',(a+2*b)*(2*a+b),'ratio',(res.fun+c)/((a+2*b)*(2*a+b)),flush=True)
 else: print(a,b,c,res.message)
 return res,M,rhs,cost
if __name__=='__main__':
 for t in [(5,3,7),(33,7,37),(35,13,43),(85,11,91),(143,25,157),(161,15,169),(323,37,343),(533,27,547)]:
  solve(*t)
