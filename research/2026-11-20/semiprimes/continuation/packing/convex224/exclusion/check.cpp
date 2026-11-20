#include <algorithm>
#include <array>
#include <bit>
#include <compare>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <deque>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;using K=uint64_t;using Z=long long;constexpr int a=35,b=13,c=43,D=1849;
struct P{int x,y;auto operator<=>(const P&)const=default;};P operator+(P x,P y){return {x.x+y.x,x.y+y.y};}P operator-(P x,P y){return {x.x-y.x,x.y-y.y};}P operator*(int n,P p){return {p.x*n,p.y*n};}P rot(P p){return {-p.y,p.x+p.y};}Z cr(P x,P y){return Z(x.x)*y.y-Z(x.y)*y.x;}
K key(P p){return (K(uint32_t(p.x))<<32)|uint32_t(p.y);}
P unit(int h,int j){P p={D,0};for(int k=0;k<abs(h);k++){int u=h>0?35:48,v=h>0?13:-13;Z x=(Z(p.x)*u-Z(p.y)*v)/43,y=(Z(p.x)*v+Z(p.y)*(u+v))/43;p={int(x),int(y)};}for(int t=0;t<(j+6)%6;t++)p=rot(p);return p;}
struct R{int h,j;auto operator<=>(const R&)const=default;};R ray(int h,int j){return {h,(j+12)%6};}R rev(R r){return ray(r.h,r.j+3);}
array<P,4> board={P{0,0},P{143*D,0},P{195*D,140*D},P{-4095*43,15120*43}};
R walls[4]={{0,0},{-1,1},{1,2},{1,4}};
struct T{P p,q;R u,v;int i,j,chir;};
struct Grid{int h;P o;array<T,36> t;};
struct Node{P p;array<K,3> mask{};int side=-1,corner=-1;bool queued=false;};
struct State{array<K,3> m{};int lo=-1,hi=-1;bool operator==(const State&)const=default;};
struct SH{size_t operator()(const State&s)const{K h=s.lo*59+s.hi+4321;for(auto x:s.m)h=(h^x)*11995408973635179863ULL;return h^(h>>32);}};
vector<Grid> grids;vector<Node> nodes;unordered_map<K,int> ids;map<R,int> rid;vector<R> rays;int nr;deque<int> queue1;
unordered_map<State,array<K,3>,SH> cache1;
bool in(P p){for(int i=0;i<4;i++)if(cr(board[(i+1)%4]-board[i],p-board[i])<0)return false;return true;}
int vertex(P p){auto [it,fresh]=ids.emplace(key(p),nodes.size());if(fresh){Node n;n.p=p;for(int i=0;i<4;i++)if(p==board[i])n.corner=i;for(int i=0;i<4;i++)if(cr(board[(i+1)%4]-board[i],p-board[i])==0)n.side=i;nodes.push_back(n);}return it->second;}
void push(int i){if(!nodes[i].queued){nodes[i].queued=true;queue1.push_back(i);}}
void addGrid(int h,P o){
 for(const auto&g:grids)if(g.h==h&&g.o==o)return;
 Grid g;g.h=h;g.o=o;
 for(int j=0;j<6;j++)for(int ch:{1,-1}){
  P v[3]={{0,0},a*unit(h,j),b*unit(h,j+2*ch)};R e[3]={ray(h,j),ray(h-ch,j+3),ray(h,j+2*ch+3)};
  if(ch<0){swap(v[1],v[2]);R f[3]={rev(e[2]),rev(e[1]),rev(e[0])};copy(f,f+3,e);}
  for(int i=0;i<3;i++){int k=(2*j+(ch<0))*3+i;g.t[k]={v[(i+1)%3]-v[i],v[(i+2)%3]-v[i],e[i],rev(e[(i+2)%3]),i,j,ch};}
 }
 grids.push_back(g);
}
void setup(){
 int gi=0;set<R> dirs;for(R v:walls){dirs.insert(v);dirs.insert(rev(v));}
 for(auto &g:grids){
  P ex=unit(g.h,0),ey=rot(ex);Z det=cr(ex,ey);int lx=10000,hx=-10000,ly=10000,hy=-10000;
  for(P p:board){int x=cr(p-g.o,ey)/det,y=cr(ex,p-g.o)/det;lx=min(lx,x-1);hx=max(hx,x+1);ly=min(ly,y-1);hy=max(hy,y+1);}
  for(auto&t:g.t){dirs.insert(t.u);dirs.insert(t.v);}
  for(int i=lx;i<=hx;i++)for(int j=ly;j<=hy;j++){P p=g.o+i*ex+j*ey;if(!in(p))continue;K m=0;for(int t=0;t<36;t+=3){auto&s=g.t[t];P q=p+s.p,r=p+s.q;
   if(in(q)&&in(r)){nodes[vertex(q)].mask[gi]|=K(1)<<(t+1);nodes[vertex(r)].mask[gi]|=K(1)<<(t+2);m|=K(1)<<t;}
  }if(m)nodes[vertex(p)].mask[gi]|=m;
  }gi++;
 }
 // Exact ray order: use physical integer vectors at common denominator D*c for the possible long heights ±3.
 auto vec=[](R r){Z x=1,y=0;for(int n=0;n<abs(r.h);n++){int a=r.h>0?35:48,b=r.h>0?13:-13;Z X=x*a-y*b,Y=x*b+y*(a+b);x=X;y=Y;}for(int i=0;i<r.j;i++){Z z=-y;y=x+y;x=z;}return pair<Z,Z>(x,y);};
 rays.assign(dirs.begin(),dirs.end());sort(rays.begin(),rays.end(),[&](R u,R v){auto[x,y]=vec(u);auto[w,z]=vec(v);bool p=y>0||(y==0&&x>0),q=z>0||(z==0&&w>0);if(p!=q)return p>q;return x*z-y*w>0;});nr=rays.size();for(int i=0;i<nr;i++)rid[rays[i]]=i;
 for(auto p:board)vertex(p);
 for(int i=0;i<(int)nodes.size();i++)push(i);
}
struct Arc{int a,b,g,t;};
array<K,3> support(const State &s){
 if(auto it=cache1.find(s);it!=cache1.end())return it->second;
 vector<vector<Arc>> arcs(nr);for(int g=0;g<(int)grids.size();g++)for(K mm=s.m[g];mm;mm&=mm-1){
  int t=countr_zero(mm);auto &sh=grids[g].t[t];int i=rid.at(sh.u),j=rid.at(sh.v);arcs[i].push_back({i,j,g,t});
 }
 array<K,3> keep{};
 auto walk=[&](int start,int len){
  bool can[100]{},back[100]{};can[0]=true;
  for(int i=0;i<len;i++)if(can[i])for(auto e:arcs[(start+i)%nr]){int j=i+(e.b-e.a+nr)%nr;if(j<=len)can[j]=true;}
  if(!can[len])return;back[len]=true;
  for(int i=len-1;i>=0;i--)for(auto e:arcs[(start+i)%nr]){int j=i+(e.b-e.a+nr)%nr;if(j<=len&&back[j]){back[i]=true;if(can[i])keep[e.g]|=K(1)<<e.t;}}
 };
 if(s.lo<0){for(int src=0;src<nr;src++)if(!arcs[src].empty()){walk(src,nr/2);walk(src,nr);}}
 else walk(s.lo,(s.hi-s.lo+nr)%nr);
 if(cache1.size()<500000)cache1.emplace(s,keep);return keep;
}
int run(){
 while(!queue1.empty()){
  int i=queue1.front();queue1.pop_front();auto&n=nodes[i];n.queued=false;State s;s.m=n.mask;
  if(n.side>=0){
    int j=n.corner>=0?n.corner:n.side;
    s.lo=rid.at(walls[j]);s.hi=rid.at(rev(walls[n.corner>=0?(j+3)%4:j]));
  }
  auto keep=support(s);
  if(n.corner>=0&&!(keep[0]|keep[1]|keep[2]))return 0;
  for(int g=0;g<(int)grids.size();g++)for(K m=n.mask[g]&~keep[g];m;m&=m-1){
   int t=countr_zero(m);auto &sh=grids[g].t[t];int suf=t%3;
   int u=ids.at(key(n.p+sh.p)),v=ids.at(key(n.p+sh.q));nodes[u].mask[g]&=~(K(1)<<(t/3*3+(suf+1)%3));nodes[v].mask[g]&=~(K(1)<<(t/3*3+(suf+2)%3));push(u);push(v);
  }n.mask=keep;
 }
 int n=0;for(auto &p:nodes)for(K m:p.mask)n+=popcount(m);return n/3;
}
int main(int ac,char**av){
 if(ac!=4)return 2;
 int mode=atoi(av[1]);
 if(mode==9){
   board={P{0,0},P{35*D,0},P{22*D,13*D},P{-13*D,13*D}};
   walls[0]={0,0};walls[1]={0,2};walls[2]={0,3};walls[3]={0,5};
   mode=0;
 }

 for(int r=atoi(av[2]);r<=atoi(av[ac>3?3:2]);r++){
 grids.clear();nodes.clear();ids.clear();rid.clear();rays.clear();queue1.clear();

 addGrid(0,{0,0});addGrid(1,{0,0});
 if(mode==0&&r)addGrid(1,{r*D,0});
 if(mode==1&&r)addGrid(0,r*unit(1,0));
 if(mode==2)addGrid(-1,{r*D,0});
 if(mode==3||mode==4)addGrid(2,r*unit(1,0));
 if(mode==5)addGrid(-2,P{143*D,0}+r*unit(-1,0));
 setup();int n=run();cout<<mode<<" "<<r<<" "<<n<<endl;
}}
