// Check all possible doubly stopped runs on the indicated polygon side.
// Build with g++ -std=c++20 -O2 check_runs.cpp -o check_runs
// Modes select the 345 quadrilateral, equilateral with side 455, or 480 quadrilateral.
// See LOCAL_OBSTRUCTION.md for the completeness argument and geometric predicates.
#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <tuple>
#include <vector>
using namespace std;
using I=long long;using W=__int128;
struct Pt{I x,y;bool operator<(Pt p)const{return tie(x,y)<tie(p.x,p.y);}bool operator==(Pt p)const{return x==p.x&&y==p.y;}};
Pt operator+(Pt p,Pt q){return {p.x+q.x,p.y+q.y};}Pt operator-(Pt p,Pt q){return {p.x-q.x,p.y-q.y};}Pt operator*(int n,Pt p){return {n*p.x,n*p.y};}
W det(Pt p,Pt q){return W(p.x)*q.y-W(p.y)*q.x;}
struct Dir{int j,h;};Dir rot(Dir d,int m,int n){return{(d.j+m+12)%6,d.h+n-m};}
int a,b,c;I D; map<Pt,Dir> vectorDirs;Pt unit[41][6];Pt uv(Dir d){if(abs(d.h)>8)abort();return unit[d.h+10][d.j];}
struct Side{int l;Dir d;Pt p;};vector<Side>walls;
void init(){
D=1;for(int i=0;i<8;i++)D*=c;
for(int h: {-1,1}){Pt p{D,0};for(int i=0;i<=8;i++){
 Pt v=p;for(int j=0;j<6;j++){unit[10+h*i][j]=v;v={-v.y,v.x+v.y};}
 if(i<8){
 I x=h==1?a:a+b,y=h==1?b:-b;
 W xx=W(x)*p.x-W(y)*p.y, yy=W(x)*p.y+W(y)*(p.x+p.y);
 if(xx%c||yy%c)abort();p={I(xx/c),I(yy/c)};
 }
}}
}
Dir direction(Pt v){auto it=vectorDirs.find(v);if(it!=vectorDirs.end())return it->second;abort();}
Dir opp(Dir d){return {(d.j+3)%6,d.h};}
bool coeff(Dir start,Dir end,int &m,int &n){for(m=0;m<=6;m++){n=m+end.h-start.h;if(n>=0&&n<=6&&(start.j+m)%6==end.j)return true;}return false;}
using Tri=array<Pt,3>;
struct Phys{Tri t;array<int,3> lengths;I lo,hi,down,up;};
bool fits(Pt p){for(auto &s:walls)if((s.l!=385||s.d.h!=1)&&det(uv(s.d),p-s.p)<0)return false;return true;}
bool sep(Tri const&t,Tri const&u){for(int i=0;i<3;i++){
 Pt dir=t[(i+1)%3]-t[i];bool pass=true;for(Pt x:u)if(det(dir,x-t[i])>0){pass=false;break;}if(pass)return true;}return false;}
bool okpair(Phys const&t,Phys const&u){if(t.hi<u.lo||u.hi<t.lo||t.up<u.down||u.up<t.down)return true;
 return (sep(t.t,u.t)||sep(u.t,t.t));}

struct Wedge{Dir lo,hi;int tag;};
vector<Phys> searchTiles;
long long visits; int cutoff;

bool isLen(int n){static vector<int> fl;if(fl.empty()){fl.resize(10001);fl[0]=1;for(int k=1;k<10001;k++)for(int z:{a,b,c})if(k>=z&&fl[k-z])fl[k]=1;}return n>=0&&n<10001&&fl[n];}
set<Pt> gridPoints; int rangeX,rangeL; bool activeLocal(Pt p){return gridPoints.count(p);}
using Ln=pair<int,W>;
struct Interval {Pt x,y;Dir d;};
struct Data {vector<Interval> edges;};
using LineTable=map<Ln,Data>;
Ln lk(Pt p,Dir d){Dir v{d.j%3,d.h};return {d.h*4+v.j,det(uv(v),p)};}
void addlines(LineTable &L,const Phys &t){for(int k=0;k<3;k++){Pt p=t.t[k],q=t.t[(k+1)%3];Dir d=direction(q-p);
 L[lk(p,d)].edges.push_back({p,q,d});
 }
 // A tile can require a split on ANY supported axis through its vertex. Index
 // its vertices separately instead of making assumptions about the two incident axes.
}
struct EdgeLayer{LineTable chosen;vector<pair<Pt,int>>chosenV;} layer;
bool lineFailure(Pt p,Dir d,int freeSide, int &bestSegment){
 auto F=uv(d);I denominator=F.x?abs(F.x):abs(F.y);int sign=((F.x?F.x:F.y)>0?1:-1);
 auto loc=[&](Pt x){return sign*(F.x?x.x-p.x:x.y-p.y);};
 auto key=lk(p,d);vector<pair<I,I>>intervals;
 auto load=[&](const LineTable &tbl){auto it=tbl.find(key);if(it==tbl.end())return;for(auto s:it->second.edges){
  bool right=s.d.j!=(d.j);if((freeSide>0)!=right)continue;
  auto x=loc(s.x),y=loc(s.y);if(max(x,y)>0)intervals.push_back(minmax(x,y));
 }};
 load(layer.chosen);
 for(auto w:walls)if(lk(w.p,w.d)==key){bool right=w.d.j==d.j;if((freeSide>0)!=right)continue;
  I x=loc(w.p),y=loc(w.p+w.l*uv(w.d));if(max(x,y)>0)intervals.push_back(minmax(x,y));}
 sort(intervals.begin(),intervals.end());I end=0;for(auto [l,h]:intervals)if(l<=end)end=max(end,h);else break;
 if(end==0)return false;
 static vector<bool>coin;if(coin.empty()){coin.resize(10000);coin[0]=1;for(int i=1;i<10000;i++)for(int l:{a,b,c})if(i>=l&&coin[i-l])coin[i]=1;}
 auto inspect=[&](const vector<pair<Pt,int>>&vx){for(auto [v,id]:vx){I f=loc(v);if(f<=0||f>end||det(F,v-p))continue;
   auto &t=searchTiles[id];bool left=false;for(Pt z:t.t)if(freeSide*det(F,z-v)>0){left=true;break;}if(!left)continue;
   if(f%denominator||f/denominator>=10000||!coin[f/denominator])return true;
   bestSegment=min(bestSegment,(int)(f/denominator));
 }return false;};
 return inspect(layer.chosenV);
}

// If opposite-bank vertices V and P both existed, the fully backed interval VP
// would have to be a concatenation of whole opposite-bank sides.
bool virtualThrough(Pt p,Dir d){
 auto F=uv(d);I den=F.x?abs(F.x):abs(F.y);int sg=(F.x?F.x:F.y)>0?1:-1;
 auto loc=[&](Pt q){return sg*(F.x?q.x-p.x:q.y-p.y);};auto key=lk(p,d);
 vector<pair<I,I>> banks;vector<I> ends;
 auto it=layer.chosen.find(key);if(it==layer.chosen.end())return false;
 for(auto w:it->second.edges){I x=loc(w.x),y=loc(w.y);if(w.d.j!=d.j)banks.push_back(minmax(x,y));else {ends.push_back(x);ends.push_back(y);}}
 // Domain boundaries are not tile vertices on the opposite bank; only use a real
 // tile as the source V. The restriction is needed only in the domain interior.
 for(auto w:walls)if(!det(uv(w.d),p-w.p))return false;
 sort(banks.begin(),banks.end());I lo=1,hi=0;bool hit=false;
 for(auto [x,y]:banks){if(y<x)abort();if(!hit&&x<=0&&y>=0){lo=x;hi=y;hit=true;}
 if(hit&&x<=hi)hi=max(hi,y);}
 if(!hit)return false;
 for(auto [x,y]:banks)if(x<=lo&&y>=lo)lo=min(lo,x);
 // A backward scan merges chains from the support already found through P.
 for(auto it=banks.rbegin();it!=banks.rend();++it)if(it->first<=lo&&it->second>=lo)lo=it->first;
 for(I v:ends)if(v>=lo&&v<=hi&&(v%den||!isLen(abs(v)/den)))return true;return false;
}
bool dfs(){
 ++visits;if(visits>cutoff||searchTiles.size()>80)throw 1;
 
 set<Pt> points;for(int k=0;k<(int)searchTiles.size();k++)for(Pt p:searchTiles[k].t)if(activeLocal(p))points.insert(p);
 for(auto s:walls)if(activeLocal(s.p))points.insert(s.p);
 layer.chosen.clear();layer.chosenV.clear();for(int id=0;id<(int)searchTiles.size();id++){addlines(layer.chosen,searchTiles[id]);for(Pt p:searchTiles[id].t)layer.chosenV.push_back({p,id});}
 vector<Phys> best;bool found=false;
 for(Pt p:points){
  vector<Wedge> occ;vector<int> near;
  auto visit=[&](int id){auto const&t=searchTiles[id];I rad=2*c*D;if(p.x<t.lo-rad||p.x>t.hi+rad||p.y<t.down-rad||p.y>t.up+rad)return;near.push_back(id);
   for(int k=0;k<3;k++)if(t.t[k]==p){occ.push_back({direction(t.t[(k+1)%3]-p),direction(t.t[(k+2)%3]-p),id});break;}
   else if(!(t.t[(k+1)%3]==p)){auto u=t.t[k],v=t.t[(k+1)%3];if(min(u,v)<p&&p<max(u,v)&&!det(v-u,p-u)){auto d=direction(v-u);occ.push_back({d,opp(d),id});break;}}
  };
  for(int id=0;id<(int)searchTiles.size();id++)visit(id);
  bool ep=false;for(int i=0;i<(int)walls.size();i++)if(walls[i].p==p){occ.push_back({opp(walls[(i+walls.size()-1)%walls.size()].d),walls[i].d,-1});ep=true;break;}
  if(!ep)for(auto s:walls)if(!(p<min(s.p,s.p+s.l*uv(s.d))) && !(max(s.p,s.p+s.l*uv(s.d))<p) && !det(uv(s.d),p-s.p)){occ.push_back({opp(s.d),s.d,-1});break;}
  set<pair<int,int>>axes;
  for(auto w:occ)for(auto d:{w.lo,w.hi}){axes.insert({d.h,d.j%3});}
  int virtualCount=0;Dir firstVirtual{};
  for(auto [h,j]:axes)for(int side:{0,3}){Dir d{j+side,h};
   if(!virtualThrough(p,d))continue;
   bool already=false;
   for(auto w:occ)if(w.lo.h==d.h&&w.lo.j==d.j&&w.hi.h==d.h&&w.hi.j==opp(d).j){already=true;break;}
   if(already)continue;
   for(int id:near){auto &t=searchTiles[id];bool touches=false;for(Pt v:t.t)if(v==p)touches=true;
    for(int k=0;k<3;k++){auto v=t.t[k],w=t.t[(k+1)%3];if(min(v,w)<p&&p<max(v,w)&&!det(w-v,p-v))touches=true;}
    if(touches)for(Pt v:t.t)if(det(uv(d),v-p)>0)return false;
   }
   if(virtualCount++ && !(d.h==firstVirtual.h&&d.j==opp(firstVirtual).j))return false;
   firstVirtual=d;occ.push_back({d,opp(d),-2});
  }
  sort(occ.begin(),occ.end(),[](auto u,auto v){auto a=uv(u.lo),b=uv(v.lo);bool A=a.y<0||(a.y==0&&a.x<0),B=b.y<0||(b.y==0&&b.x<0);if(A!=B)return A<B;return det(a,b)>0;});
  for(int k=0;k<(int)occ.size();k++){auto u=occ[k],v=occ[(k+1)%occ.size()];Dir start=u.hi,end=v.lo;if(start.j==end.j&&start.h==end.h)continue;
   int M,N;if(!coeff(start,end,M,N))return false;if(det(uv(start),uv(end))<=0&&M>=3&&N>=3)continue;
   for(int side=0;side<2;side++){vector<Phys> choices;bool high=false;int maxLength=10000;
    if(lineFailure(p,side?end:start,side?-1:1,maxLength))return false;
    for(int l:{a,b,c})for(int r:{a,b,c})if(l!=r){
     int i=0,j=0,s=a+b+c-l-r;if(s==a)i=1;else if(s==b)j=1;else i=j=2;if(i>M||j>N||(side?r:l)>maxLength||(maxLength<10000&&!isLen(maxLength-(side?r:l))))continue;
     Dir f=side?rot(end,-i,-j):start,g=side?end:rot(start,i,j);
     if(abs(f.h)>8||abs(g.h)>8){high=true;continue;}
     Pt va=p+l*uv(f),vb=p+r*uv(g);if(!fits(va)||!fits(vb))continue;
     Phys t{{p,va,vb},{l,s,r},min({p.x,va.x,vb.x}),max({p.x,va.x,vb.x}),min({p.y,va.y,vb.y}),max({p.y,va.y,vb.y})};
     bool ok=true;for(int id:near)if(!okpair(t,searchTiles[id])){ok=false;break;}if(ok)choices.push_back(t);
    }
    if(high)continue;
    if(choices.empty())return false;if(!found||choices.size()<best.size()){found=true;best=choices;}
   }
  }
 }
 if(!found)throw 1;
 for(auto t:best){searchTiles.push_back(t);if(dfs())return true;searchTiles.pop_back();}return false;
}
int main(int argc,char**argv){
if(argc!=2)return 2;int problem=atoi(argv[1]);a=35;b=13;c=43;init();
for(int h=-8;h<=8;h++)for(int j=0;j<6;j++)for(int k:{a,b,c})vectorDirs[k*uv({j,h})]={j,h};
std::vector<std::array<int,3>> shape;
if(problem==345)shape={{260,0,0},{645,2,1},{385,1,4},{315,0,4}};
else if(problem==480)shape={{455,0,0},{43,-1,2},{420,0,2},{468,0,4}};
else if(problem==455)shape={{455,0,0},{455,0,2},{455,0,4}};
else return 2;
int len=shape[0][0],width=problem==345?3:5;Pt p{0,0};
for(auto [l,h,j]:shape){Dir d{j,h};walls.push_back({l,d,p});p=p+l*uv(d);} if(p.x||p.y)abort();
int bad=0,maxv=0,cases=0;cutoff=100000;
for(int n=1;n<=width;n++)for(int off=0;off<=len-n*c;off++)for(int bits=0;bits<(1<<n);bits++)
 for(int LEFT:{a,b})for(int RIGHT:{a,b}){
 
 if((off==0&&LEFT!=a)||(off+n*c==len&&RIGHT!=a))continue;
 if(off>0&&!isLen(off-LEFT))continue;
 if(off+n*c<len&&!isLen(len-off-n*c-RIGHT))continue;
 // Entire boundary contains these c tiles plus the two indicated stops.
 bool valid=false;
 for(int A=0;A*a<=len;A++)for(int B=0;A*a+B*b<=len;B++){
 int L=len-A*a-B*b;if(L%c||L/c<n)continue;
 if(A<(off>0&&LEFT==a)+(off+n*c<len&&RIGHT==a))continue;
 if(B<(off>0&&LEFT==b)+(off+n*c<len&&RIGHT==b))continue;
 valid=true;}
 if(!valid)continue;
 rangeL=n*c;rangeX=off;cases++;
 searchTiles.clear();
 auto tile=[&](int off,int len,int r){int oth=a+b+c-len-r;int m=0,v=0;if(oth==a)m=1;else if(oth==b)v=1;else m=v=2;
  Pt x={D*off,0},y=x+len*uv({0,0}),z=x+r*uv(rot({0,0},m,v));
  Phys f{{x,y,z},{len,oth,r},min({x.x,y.x,z.x}),max({x.x,y.x,z.x}),min({x.y,y.y,z.y}),max({x.y,y.y,z.y})};
  searchTiles.push_back(f);};
 for(int j=0;j<n;j++)tile(rangeX+j*c,c,(bits>>j&1)?a:b);
 if(off>0)tile(rangeX-LEFT,LEFT,c);
 if(off+rangeL<len)tile(rangeX+rangeL,RIGHT,a+b-RIGHT);

 gridPoints.clear();
 for(int i=0;i<n;i++)for(int m:{0,1}){
 // m=0 uses the alpha corner and m=1 the beta corner of a boundary tile.
 bool west= ((bits>>i&1)==m); int ray=west?1:-1;
 Pt base{(off+(i+(west?0:1))*c)*D,0};
 Pt C{ray*c*D,0}, A=searchTiles[i].t[2]-base;
 int depth=west?n-i:i+1;
 for(int j=0;j<=depth;j++)for(int k=0;k+j<=depth;k++)
     gridPoints.insert(base+j*A+k*C);
 }
 bool ok=true;for(int j=0;j<(int)searchTiles.size();j++){
  for(Pt p:searchTiles[j].t)if(!fits(p))ok=false;
  for(int i=0;i<j;i++)if(!okpair(searchTiles[i],searchTiles[j]))ok=false;
 }
 visits=0;int ret=0;if(ok){try{if(dfs())abort();}catch(int){ret=1;}}
 cout<<n<<' '<<off<<' '<<bits<<' '<<LEFT<<' '<<RIGHT<<' '<<(ret?"OPEN":"NO")<<' '<<visits<<'\n'<<flush;
 bad+=ret;maxv=max(maxv,(int)visits);
}
cerr<<"cases "<<cases<<" open "<<bad<<" max "<<maxv<<"\n";
return bad?1:0;
}
