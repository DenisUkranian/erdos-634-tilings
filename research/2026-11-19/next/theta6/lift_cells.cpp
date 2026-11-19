// Exact translation endpoint consistency over enumerated (x,sqrt(2)*y) lattice shapes.
#include <algorithm>
#include <gmpxx.h>
#include <cassert>
#include <array>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using I = long long;
struct V { int x,y; };
V operator+(V a,V b){return {a.x+b.x,a.y+b.y};}
V operator-(V a,V b){return {a.x-b.x,a.y-b.y};}
V operator*(V a,V b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}
V scale(int n,V v){return {n*v.x,n*v.y};}
V power(V v,int n){V r{1,0};while(n-->0)r=r*v;return r;}
I det(V a,V b){return I(a.x)*b.y-I(a.y)*b.x;}
I down(I a,I b){if(b<=0)throw logic_error("denominator");return a>=0?a/b:-((-a+b-1)/b);}
struct Run{int lo,hi;};
using Runs=vector<Run>;
using Strip=vector<Runs>;
using Triangle=array<V,3>;
struct End{int shape; V offset; bool start;};
struct Corner{V p;bool start;};
struct Dir{vector<End> ends;vector<Corner> corners;};
int main(int argc,char**argv){
 if(argc!=5 && argc!=6)return 1;
 const bool write_pool = argc==5;
 if(!write_pool && string(argv[5])!="--count-only")return 1;
 int denom=stoi(argv[1]),num=stoi(argv[2]),cap=300;
 if(denom<1||denom>100000||(num!=180 && num!=280))return 2;
 ifstream maskfile(argv[4]);
 int bound,mesh,target,wcells,hcells;
 if(!(maskfile>>bound>>mesh>>target>>wcells>>hcells))return 2;
 if(target!=(num==180 ? 3 : 2))return 2;
 int base=num==180 ? 60 : 140, ht=num==180 ? 60 : 40;
 Triangle outer={V{0,0},V{base*denom,0},V{base/2*denom,ht*denom}};
 vector<Triangle> shapes;
 map<int,V> rotations;
 rotations[0]={denom,0};
 for(int i=1;i<=bound;++i){
   V old=rotations[i-1];int x=-old.x-4*old.y,y=2*old.x-old.y;
   if(x%3||y%3)return 2;
   rotations[i]={x/3,y/3};rotations[-i]={x/3,-y/3};
 }
 for(int h=-bound;h<=bound;h++)for(int sign:{1,-1})for(int adj:{-2,7}){
   V u=scale(sign,rotations[h]);
   shapes.push_back({V{0,0},scale(5,u),V{adj*u.x-8*u.y,4*u.x+adj*u.y}});
 }
 vector<map<int,Runs>> coarse(shapes.size());
 int tpl,ry;string bits;
 while(maskfile>>tpl>>ry>>bits){
   if(tpl<0||tpl>=int(shapes.size())||ry<0||ry>=hcells)return 2;
   mpz_class mask(bits,16);Runs& row=coarse[tpl][ry];
   for(auto x=mpz_scan1(mask.get_mpz_t(),0);x<(unsigned)wcells;){
     auto e=mpz_scan0(mask.get_mpz_t(),x);
     int l=(x*denom+mesh-1)/mesh,r=(e*denom+mesh-1)/mesh-1;
     if(l<=r)row.push_back({l,r});
     x=mpz_scan1(mask.get_mpz_t(),e);
   }
 }
 if(write_pool){
  ofstream f(string(argv[3])+".shapes");f<<denom<<" "<<num<<" "<<shapes.size()<<"\n";
  for(auto t:shapes)f<<t[1].x<<" "<<t[1].y<<" "<<t[2].x<<" "<<t[2].y<<"\n";
 }
 map<pair<int,int>,Dir> dirs;
 auto axis=[](V p){int n=gcd(p.x,p.y);if(p.x<0||(!p.x&&p.y<0))n=-n;return make_pair(p.x/n,p.y/n);};
 auto edges=[&](Triangle shape,auto record){
  for(int j=0;j<3;j++){V a=shape[j],b=shape[(j+1)%3]; Dir& d=dirs[axis(b-a)];record(d,a,true);record(d,b,false);}
 };
 for(int t=0;t<int(shapes.size());t++)edges(shapes[t],[&](Dir& d,V v,bool start){d.ends.push_back({t,v,start});});
 edges(outer,[](Dir& d,V v,bool start){d.corners.push_back({v,start});});
 int bottom=min({outer[0].y,outer[1].y,outer[2].y}),top=max({outer[0].y,outer[1].y,outer[2].y}),H=top-bottom+1;
 vector<Strip> state(shapes.size(),Strip(H)); I population=0;
 // For each shape, translate the target's three supporting halfplanes inward
 // by the worst of its three vertices; all integer anchors form one run on each row.
 for(int t=0;t<int(shapes.size());t++){
  array<I,3> minimum;
  for(int e=0;e<3;e++){
   V p=outer[e],d=outer[(e+1)%3]-p; I c=det(d,p);
   minimum[e]=max({c-det(d,shapes[t][0]),c-det(d,shapes[t][1]),c-det(d,shapes[t][2])});
  }
  for(int y=bottom;y<=top;y++){
   I a=-(1LL<<40),b=1LL<<40;
   for(int e=0;e<3;e++){V d=outer[(e+1)%3]-outer[e]; I k=I(d.x)*y-minimum[e];
    if(d.y>0)b=min(b,down(k,d.y));else if(d.y<0)a=max(a,-down(k,-d.y));else if(k<0){a=1;b=0;break;}
   }
   if(a>b)continue;
   auto row=coarse[t].find((I)y*mesh/denom);
   if(row==coarse[t].end())continue;
   for(Run r:row->second){
    int lo=max((I)r.lo,a),hi=min((I)r.hi,b);
    if(lo<=hi){state[t][y-bottom].push_back({lo,hi});population+=hi-lo+1;}
   }
  }
 }
 cout<<"initial "<<population<<" templates "<<shapes.size()<<" scanlines "<<H<<endl;
 for(int iter=1;iter<=cap;iter++){
  I previous=population, fragments=0;
  for(auto& [direction,dir]:dirs){
   array<Strip,2> available{Strip(H),Strip(H)};Runs gathered;
   for(int side=0;side<2;side++)for(int y=bottom;y<=top;y++){
    gathered.clear();
    for(End e:dir.ends)if(e.start==bool(side)){
     int k=y-e.offset.y-bottom;if(k<0||k>=H)continue;
     for(Run r:state[e.shape][k])gathered.push_back({r.lo+e.offset.x,r.hi+e.offset.x});
    }
    // The exterior supplies the *opposite* incidence required by its signed boundary equation.
    for(Corner c:dir.corners)if(c.p.y==y&&c.start!=bool(side))gathered.push_back({c.p.x,c.p.x});
    sort(gathered.begin(),gathered.end(),[](Run a,Run b){return a.lo<b.lo;});
    Runs& out=available[side][y-bottom];
    for(Run r:gathered){
     if(out.empty()||out.back().hi+1<r.lo)out.push_back(r);
     else out.back().hi=max(out.back().hi,r.hi);
    }
   }
   for(Corner c:dir.corners){
    bool found=false;for(Run r:available[c.start][c.p.y-bottom])if(r.lo<=c.p.x&&c.p.x<=r.hi){found=true;break;}
    if(!found){cout<<"CONFLICT iteration "<<iter<<" at "<<c.p.x<<" "<<c.p.y<<" direction "<<direction.first<<" "<<direction.second<<" sign "<<c.start<<endl;return 0;}
   }
   Runs newruns;
   for(End e:dir.ends)for(int k=0;k<H;k++){
    Runs& runs=state[e.shape][k];if(runs.empty())continue;
    int y=k+e.offset.y;if(y<0||y>=H)throw logic_error("containment");
    Runs const& allow=available[!e.start][y];newruns.clear();size_t a=0,b=0;
    while(a<runs.size()&&b<allow.size()){
     Run u=runs[a],v{allow[b].lo-e.offset.x,allow[b].hi-e.offset.x};
     int l=max(u.lo,v.lo),h=min(u.hi,v.hi);if(l<=h)newruns.push_back({l,h});
     if(u.hi<=v.hi)a++;if(u.hi>=v.hi)b++;
    }
    for(Run r:runs)population-=r.hi-r.lo+1;
    for(Run r:newruns)population+=r.hi-r.lo+1;
    runs.swap(newruns);
   }
  }
  for(auto& grid:state)for(auto& runs:grid)fragments+=runs.size();
  cout<<"iteration "<<iter<<" candidates "<<population<<" intervals "<<fragments<<endl;
  if(population==previous){
   cout<<"STABLE"<<endl;
   if(write_pool){
    ofstream save(argv[3]);save<<denom<<' '<<num<<' '<<population<<'\n';
    for(size_t t=0;t<shapes.size();t++)for(int k=0;k<H;k++)for(Run r:state[t][k])
     for(int x=r.lo;x<=r.hi;x++)save<<t<<' '<<x<<' '<<bottom+k<<'\n';
   }return 0;
  }
 }
 cout<<"UNRESOLVED: iteration limit"<<endl;
}
