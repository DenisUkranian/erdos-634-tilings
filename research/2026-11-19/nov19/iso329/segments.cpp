// Exact positive-length support checking, applied to an independent list of remaining placements.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <vector>
using namespace std;using I=long long;
struct P{int x,y;};
P plusp(P a,P b){return {a.x+b.x,a.y+b.y};}
P mul(P a,P b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}
P power(P a,int n){P r{1,0};while(n--)r=mul(r,a);return r;}
P times(int s,P a){return {a.x*s,a.y*s};}
struct E {I line;int phase,low,high,id,length;bool positive;};
struct R{int a,b;};
int main(int argc,char**argv){
 if(argc<2)return 1;const bool exactUniform=argc>5&&stoi(argv[5]);ifstream input(argv[1]);int L,U,count;input>>L>>U>>count;
 using Tri=array<P,3>;P eta{7,-3},bar{4,3},rho{0,1};vector<Tri> ts;
 for(int h=L;h<=U;h++)for(int swap=0;swap<2;swap++){P u=mul(power(eta,h-L),power(bar,U-h));
  for(int r=0;r<6;r++){ts.push_back({P{0,0},times(swap?7:33,u),times(swap?33:7,mul(rho,mul(rho,u)))});u=mul(rho,u);}
 }
 const int scale=(argc>2&&stoi(argv[2])==0)?0:8547;
 map<pair<int,int>,vector<E>> groups;
 auto append=[&](Tri tri,int id,array<int,3> lens){
 for(int k=0;k<3;k++){P a=tri[k],b=tri[(k+1)%3],v{b.x-a.x,b.y-a.y};
 int n=gcd(v.x,v.y);if(v.x<0||(!v.x&&v.y<0))n=-n;P d{v.x/n,v.y/n};
 int A=d.x?a.x:a.y,B=d.x?b.x:b.y;
 int step=abs(B-A)*scale/lens[k], rem=!step?0:int((I(min(A,B))*scale%step+step)%step);
 if(scale&&I(step)*lens[k]!=I(abs(B-A))*scale)throw logic_error("inexact unit");
 groups[{d.x,d.y}].push_back({I(d.x)*a.y-I(d.y)*a.x,rem,min(A,B),max(A,B),id,lens[k],id==count?A>B:A<B});}};
 for(int i=0;i<count;i++){int t,x,y;if(!(input>>t>>x>>y))throw logic_error("short input");Tri tri=ts.at(t);for(P&v:tri)v=plusp(v,{x,y});append(tri,i,t%12<6?array<int,3>{33,37,7}:array<int,3>{7,37,33});}
 P inv=mul(power(eta,-L),power(bar,U));int control=argc>4?stoi(argv[4]):0;
 if(control)append({P{0,0},times(33*control,inv),times(7*control,mul(mul(rho,rho),inv))},count,{33*control,37*control,7*control});
 else append({P{0,0},times(329,inv),mul({49,231},inv)},count,{329,259,259});
 for(auto&[d,es]:groups)sort(es.begin(),es.end(),[](E e,E f){return tie(e.line,e.phase,e.low,e.high)<tie(f.line,f.phase,f.low,f.high);});
 vector<bool> active(count+1,true); int live=count;
 for(int iter=0;;iter++){int old=live;for(auto&[d,es]:groups){size_t first=0;
 while(first<es.size()){size_t last=first+1;while(last<es.size()&&es[first].line==es[last].line&&es[first].phase==es[last].phase)last++;
  vector<R> ranges[2];for(size_t i=first;i<last;i++){E e=es[i];if(!active[e.id])continue;auto& rs=ranges[e.positive];if(rs.empty()||rs.back().b<e.low)rs.push_back({e.low,e.high});else rs.back().b=max(rs.back().b,e.high);}
  if(exactUniform){
   // On a line/phase with only one possible tile-edge length, equality of
   // interval currents requires equality at each individual interval start.
   int length=0,step=0;bool mixed=false;const E* boundary=nullptr;
   for(size_t i=first;i<last;i++)if(active[es[i].id]){
    const auto& e=es[i];if(e.id==count){boundary=&e;continue;}
    if(length&&length!=e.length){mixed=true;break;}length=e.length;step=e.high-e.low;
   }
   if(!mixed&&length){
    map<int,int> signs;for(size_t i=first;i<last;i++)if(active[es[i].id]&&es[i].id!=count)signs[es[i].low]|=1<<es[i].positive;
    if(boundary){
     if((boundary->high-boundary->low)%step){cout<<"CONFLICT incompatible whole boundary intervals at "<<boundary->line<<endl;return 0;}
     for(int x=boundary->low;x<boundary->high;x+=step){int& flags=signs[x];if(!(flags&(1<<(!boundary->positive)))){cout<<"CONFLICT missing whole length boundary interval at "<<x<<" iteration "<<iter<<endl;return 0;}flags|=1<<boundary->positive;}
    }
    for(size_t i=first;i<last;i++){auto e=es[i];if(active[e.id]&&e.id!=count&&signs[e.low]!=3){active[e.id]=false;live--;}}
   }
  }
  size_t ptr[2]={};for(size_t i=first;i<last;i++){E e=es[i];if(!active[e.id])continue;auto& rs=ranges[!e.positive];auto& j=ptr[!e.positive];
   while(j<rs.size()&&rs[j].b<=e.low)j++;
   if(j==rs.size()||rs[j].a>e.low||rs[j].b<e.high){if(e.id==count){cout<<"CONFLICT along boundary line "<<e.line<<" dir "<<d.first<<" "<<d.second<<" iteration "<<iter<<" remaining "<<live<<endl;return 0;}active[e.id]=false;live--;}
  }first=last;
 }}cout<<"iteration "<<iter<<" alive "<<live<<endl;if(old==live)break;}
 if(argc>3){ifstream reread(argv[1]);int k; reread>>k>>k>>k;ofstream out(argv[3]);out<<L<<' '<<U<<' '<<live<<'\n';for(int i=0;i<count;i++){int t,x,y;reread>>t>>x>>y;if(active[i])out<<t<<' '<<x<<' '<<y<<'\n';}}
}
