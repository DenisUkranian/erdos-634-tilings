"""Check positive rational direction populations with the board's count and flux."""
from collections import Counter
from fractions import Fraction as Q
types=[(1,1,-1),(1,3,-1),(1,2,1),(1,4,1),(2,1,-1),(2,3,-1)]
examples={
    (33,7,37):["1551/37","511/37","637/740","13223/740","429/20","91/20"],
    (35,13,43):["2135/43","1079/43","1859/1032","30901/1032","385/24","143/24"],
}
def emit(d,h,j,s):
    j%=6
    d[h,j%3]+=s if j<3 else -s
def tile(d,a,b,c,h,j,s,mass):
    emit(d,h,j,a*mass)
    emit(d,h,j+s,b*mass)
    emit(d,h+s,j,-c*mass)
for (a,b,c),initial in examples.items():
    N=(a+2*b)*(2*a+b)
    masses=list(map(Q,initial))
    assert min(masses)>0 and sum(masses)<N
    d=Counter()
    for (h,j,s),k in zip(types,masses):tile(d,a,b,c,h,j,s,k)
    gap=N-sum(masses)
    for j in (0,3):tile(d,a,b,c,1,j,1,gap/2)
    board=Counter()
    emit(board,0,0,b*(2*a+b));emit(board,2,1,c*c);emit(board,0,4,a*(a+2*b))
    assert d==board
    print(N,"six-type mass",sum(masses),"total after adding a half-turn pair",sum(masses)+gap)
