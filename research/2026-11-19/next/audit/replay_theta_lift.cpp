// Independent point-by-point lift for the theta6 target and D=729.
// The input is the outward-rounded height-6 Q=81 mesh, followed by the
// placement table to compare. It enumerates 9x9 individual integer anchors
// in each surviving cell; the endpoint phase below uses no scanline unions.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <gmpxx.h>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
constexpr int D=729,Q=81,W=60*D+1,hblocks=(W+255)/256;
struct V { int x=0,y=0; auto operator<=>(const V&)const=default; };
V operator+(V u,V v){return {u.x+v.x,u.y+v.y};}
V operator-(V u,V v){return {u.x-v.x,u.y-v.y};}
uint32_t key(V p){return (uint32_t(p.y)<<16)+p.x;}
V point(uint32_t code){return {int(code&65535),int(code>>16)};}
V axis(V p){
 int g=gcd(abs(p.x),abs(p.y));if(p.x<0||(!p.x&&p.y<0))g=-g;
 return {p.x/g,p.y/g};
}
bool contained(V p){return p.y>=0&&p.y<=2*p.x&&p.y<=2*(W-1-p.x);}
struct End { int type; V v; bool start; };
struct Directions { vector<End> edges,wall; };
struct Bits {
 using Page=array<array<uint64_t,4>,2>;
 vector<int> slot=vector<int>(W*hblocks);
 vector<int> touched;
 vector<Page> pages;
 void clear(){for(int a:touched)slot[a]=0;touched.clear();pages.clear();}
 void add(V p,bool start){
  int a=p.y*hblocks+(p.x>>8),j=slot[a];
  if(!j){pages.push_back({});slot[a]=j=pages.size();touched.push_back(a);}
  pages[j-1][start][(p.x>>6)&3]|=1ULL<<(p.x&63);
 }
 bool has(V p,bool start)const{
  int j=slot[p.y*hblocks+(p.x>>8)];
  return j&&((pages[j-1][start][(p.x>>6)&3]>>(p.x&63))&1);
 }
};
int main(int argc,char** argv){
 if(argc!=3)return 2;
 ifstream mesh(argv[1]),expected(argv[2]);int b,q,sel,wx,wy;
 mesh>>b>>q>>sel>>wx>>wy;
 if(b!=6||q!=Q||sel!=3||wx!=60*Q+1||wy!=60*Q+1)throw runtime_error("mesh header");
 array<V,13> units;units[6]={D,0};for(int h=1;h<=6;h++){
  V u=units[5+h];int x=-u.x-4*u.y,y=2*u.x-u.y;
  if(x%3||y%3)throw runtime_error("orientation denominator");
  units[6+h]={x/3,y/3};units[6-h]={x/3,-y/3};
 }
 vector<array<V,3>> sh;for(V r:units)for(int s:{1,-1})for(int c:{-2,7}){
  int x=s*r.x,y=s*r.y;sh.push_back({V{0,0},V{5*x,5*y},V{c*x-8*y,4*x+c*y}});
 }
 vector<vector<uint32_t>> pos(sh.size());int t,y;string row;int64_t nc=0,n=0;
 while(mesh>>t>>y>>row){
  mpz_class mask(row,16);
  for(unsigned bit=mpz_scan1(mask.get_mpz_t(),0);bit<wx;bit=mpz_scan1(mask.get_mpz_t(),bit+1)){
   ++nc;for(int dy=0;dy<9;dy++)for(int dx=0;dx<9;dx++){
    V p{int(9*bit)+dx,9*y+dy};
    if(all_of(sh.at(t).begin(),sh[t].end(),[&](V v){return contained(p+v);})){pos[t].push_back(key(p));++n;}
   }
  }
 }
 cout<<"cells "<<nc<<" initial exact positions "<<n<<endl;
 map<V,Directions> dirs;
 auto register_edges=[&](array<V,3> tri,int type){
  for(int i=0;i<3;i++){
   V a=tri[i],b=tri[(i+1)%3];auto& d=dirs[axis(b-a)];auto& ends=type<0?d.wall:d.edges;
   ends.push_back({type,a,true});ends.push_back({type,b,false});
  }
 };
 for(int k=0;k<int(sh.size());k++)register_edges(sh[k],k);
 register_edges({V{0,0},V{60*D,0},V{30*D,60*D}},-1);
 Bits support;
 for(int sweep=1;;sweep++){
  int64_t prev=n;
  for(const auto& [d,g]:dirs){
   support.clear();
   for(End e:g.edges)for(uint32_t anchor:pos[e.type])support.add(point(anchor)+e.v,e.start);
   for(End e:g.wall)support.add(e.v,!e.start);
   for(End e:g.wall)if(!support.has(e.v,e.start))throw runtime_error("unsupported wall");
   for(End e:g.edges){auto& list=pos[e.type];size_t old=list.size();
    erase_if(list,[&](uint32_t k){return !support.has(point(k)+e.v,!e.start);});
    n-=old-list.size();
   }
  }
  cout<<"sweep "<<sweep<<" exact positions "<<n<<endl;
  if(n==prev)break;
 }
 int denom,count,rows;expected>>denom>>count>>rows;if(denom!=D||count!=180||rows!=n)throw runtime_error("pool header");
 vector<vector<uint32_t>> wanted(sh.size());int x;while(expected>>t>>x>>y)wanted.at(t).push_back(key({x,y}));
 for(int k=0;k<int(sh.size());k++){
  sort(pos[k].begin(),pos[k].end());sort(wanted[k].begin(),wanted[k].end());
  if(pos[k]!=wanted[k])throw runtime_error("placement set mismatch");
 }
 cout<<"All final ordered placement sets agree."<<endl;
}
