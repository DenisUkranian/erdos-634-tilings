#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <cstdlib>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using namespace std;
struct P{int x,y;auto operator<=>(const P&) const=default;};
P operator+(P a,P b){return {a.x+b.x,a.y+b.y};} P operator-(P a,P b){return {a.x-b.x,a.y-b.y};} P operator*(int k,P a){return {k*a.x,k*a.y};} long long cross(P a,P b){return (long long)a.x*b.y-(long long)a.y*b.x;}
struct Edge {int type,dir,length;P offset;};struct Axis{P u;vector<Edge> edges;};
using U=uint32_t;using K=uint64_t;struct Arc {int i,j,s;U mask[2];bool ext;int sup;};
#include <set>
#include "corner_fans.hpp"

int main(int ac,char**av){int N,T;cin>>N>>T;vector<P> poly(N);for(P &p:poly)cin>>p.x>>p.y;int x0=poly[0].x,x1=x0,y0=poly[0].y,y1=y0;for(P v:poly){x0=min(x0,v.x);x1=max(x1,v.x);y0=min(y0,v.y);y1=max(y1,v.y);} for(P&p:poly)p=p-P{x0,y0};int nx=x1-x0+1,ny=y1-y0+1;
 vector<array<P,3>> triangles(T);map<P,Axis> axes;
 auto edge=[&](int t,P v,P w){P d=w-v;int l=gcd(abs(d.x),abs(d.y));int sign=(d.x>0||(d.x==0&&d.y>0))?1:0;P u{d.x/l,d.y/l};if(!sign)u=P{}-u;auto &a=axes[u];a.u=u;a.edges.push_back({t,sign^(t==T),l,sign?v:w});};
 for(int t=0;t<T;t++){for(auto &p:triangles[t])cin>>p.x>>p.y;for(int j=0;j<3;j++)edge(t,triangles[t][j],triangles[t][(j+1)%3]);}
 for(int j=0;j<N;j++)edge(T,poly[j],poly[(j+1)%N]);
 vector<U> mask(nx*ny);vector<bool> inside(nx*ny);auto idx=[&](P p){return p.y*nx+p.x;};auto fits=[&](P p){return p.x>=0&&p.y>=0&&p.x<nx&&p.y<ny;};auto legal=[&](P p){return fits(p)&&inside[idx(p)];};
 for(int y=0;y<ny;y++)for(int x=0;x<nx;x++){P p{x,y};bool good=true;for(int j=0;j<N;j++)if(cross(poly[(j+1)%N]-poly[j],p-poly[j])<0){good=false;break;}inside[idx(p)]=good;}
 int C=0,R0=0,R1=0,F1=0; if(getenv("NATIVE_PHASES")){C=atoi(getenv("C"));R0=atoi(getenv("R0"));R1=atoi(getenv("R1"));F1=atoi(getenv("F1"));}
 long long avail=0;for(int y=0;y<ny;y++)for(int x=0;x<nx;x++)if(inside[y*nx+x]){P p{x,y};for(int t=0;t<T;t++)if((!C || (((p.x+x0)+(t<12?R0:R1)*(p.y+y0)-(t<12?0:F1))%C==0)) && legal(p+triangles[t][1])&&legal(p+triangles[t][2])){mask[idx(p)]|=1u<<t;avail++;}}
 cerr<<nx<<"x"<<ny<<" placements "<<avail<<"\n";bool extbad=false;

 StarFilter star(nx,ny,triangles,poly,mask,inside);
 for(int it=0;;it++){auto old=avail;
 if(!star.sweep(avail)){cerr<<"corner failed on sweep "<<it<<" remaining "<<avail<<"\n";cout<<"NO\n";return 0;}cerr<<"star "<<it<<" "<<avail<<"\n";
 for(auto &[u,ax]:axes){map<int,vector<Edge>> lengths;for(auto e:ax.edges)lengths[e.length].push_back(e);
  for(int y=0;y<ny;y++)for(int x=0;x<nx;x++){P origin{x,y};if(!inside[idx(origin)]||legal(origin-u))continue;
   vector<Arc> arcs;vector<int> common;int n=0;
   for(P p=origin;legal(p);p=p+u,n++){
    int sources=0;
    for(auto & [l,eds]:lengths){U a[2]={};int s=0;bool ext=false;
     for(auto e:eds){P q=p-e.offset;if(e.type==T){if(q==P{}){ext=true;s|=1<<e.dir;}continue;}if(!fits(q))continue;U bit=1u<<e.type;if(mask[idx(q)]&bit){s|=1<<e.dir;a[e.dir]|=bit;}}
     if(s){arcs.push_back({n,n+l,s,{a[0],a[1]},ext,0});sources|=s;}
    }if(sources==3)common.push_back(n);
   }
   if(arcs.empty())continue;
   for(size_t off=0;off<common.size();off+=64){vector<array<K,4>> path(n);for(int j=0;j<64&&off+j<common.size();j++){auto &k=path[common[off+j]];k[0]=k[1]=K(1)<<j;}
    for(const auto &a:arcs){if(a.j>=n){cerr<<"bad\n";abort();}for(int i=0;i<2;i++)if((a.s>>i)&1)path[a.j][i]|=path[a.i][i];}
    for(auto &r:path)r[2]=r[3]=r[0]&r[1];
    for(auto ar=arcs.rbegin();ar!=arcs.rend();++ar){auto &a=*ar;for(int i=0;i<2;i++)if((a.s>>i)&1){if(path[a.i][i]&path[a.j][i+2])a.sup|=1<<i;path[a.i][i+2]|=path[a.j][i+2];}}
   }
   for(const auto &a:arcs)if(a.sup!=a.s){P p=origin+a.i*u;for(const auto &e:lengths[a.j-a.i])if(!((a.sup>>e.dir)&1)){if(e.type==T){if(a.ext&&p==e.offset)extbad=true;continue;}U bit=1u<<e.type;if(a.mask[e.dir]&bit){U &m=mask[idx(p-e.offset)];if(m&bit){m^=bit;avail--;}}}}
  }
  if(extbad){cerr<<"outer failure axis "<<u.x<<","<<u.y<<" sweep "<<it<<" remaining "<<avail<<"\n";cout<<"NO\n";return 0;}
 }
 cerr<<"sweep "<<it<<" "<<avail<<"\n";if(avail==old)break;
 }
 if(ac>1){ifstream truth(av[1]);if(!truth)abort();int t,x,y,seen=0;while(truth>>t>>x>>y){P q{x-x0,y-y0};if(!fits(q)||!(mask[idx(q)]&(U(1)<<t))){cerr<<"known tile lost\n";abort();}seen++;}cerr<<"preserved "<<seen<<" prescribed tile placements\n";}
 if(ac>2){ofstream out(av[2],ios::binary);out.write((char*)&nx,sizeof(nx));out.write((char*)&ny,sizeof(ny));out.write((char*)&x0,sizeof(x0));out.write((char*)&y0,sizeof(y0));out.write((char*)mask.data(),mask.size()*sizeof(U));}
 cout<<"OPEN "<<avail<<"\n";
}
