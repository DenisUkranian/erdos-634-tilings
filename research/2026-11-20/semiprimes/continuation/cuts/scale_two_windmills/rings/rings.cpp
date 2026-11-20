// Enumerate every cyclic sequence of individually admissible outer cells whose
// inner corners form a simple polygon, allowing reflex corners. Input is produced by ears.cpp.
// Each output row holds size k, k outer-cell indices, k signed central lengths,
// and the central area in unit tiles. See RINGS.md and replay_rings.py.
#include <algorithm>
#include <array>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
using I=long long;using W=__int128_t;
using Node=array<int,4>;
struct Point{I x,y;};
W cross(Point a,Point b,Point c){return W(b.x-a.x)*(c.y-a.y)-W(b.y-a.y)*(c.x-a.x);}
struct Edge{int u,v,la,lb;Point p;};
int main(int argc,char**argv){
 if(argc!=6)return 2;int a=atoi(argv[1]),b=atoi(argv[2]),c=atoi(argv[3]),area=atoi(argv[4]);
 ifstream in(argv[5]);I D=0,den;
 map<Node,int>lookup;vector<Node>nodes;
 auto node=[&](Node q){auto[i,did]=lookup.emplace(q,nodes.size());if(did)nodes.push_back(q);return i->second;};
 vector<Edge> rows;
 string line;while(getline(in,line)){
   if(line.empty()||line.front()=='C')continue;
   Point p;Node u,v;int la,lb;istringstream s(line);
   if(!(s>>p.x>>p.y>>den>>u[0]>>u[1]>>la>>u[2]>>u[3]>>v[0]>>v[1]>>lb>>v[2]>>v[3]))abort();
   if(D&&D!=den)abort();D=den;
   rows.push_back({node(u),node(v),la,lb,p});
 }
 int longestArm=0;for(auto const&e:rows)longestArm=max({longestArm,e.la,e.lb});
 vector<bool>coin(longestArm+1);coin[0]=true;
 for(int i=1;i<=longestArm;i++)for(int l:{a,b,c})if(i>=l&&coin[i-l])coin[i]=true;
 auto goodlen=[&](int n){return n!=0&&abs(n)<=longestArm&&coin[abs(n)];};
 if(!D)return 2;
 // Interior anchors are distinct. Increasing order also gives an acyclic
 // forward traversal before the final return to the least exterior anchor.
 set<pair<int,int>> sites;for(auto const&q:nodes)sites.insert({q[0],q[1]});
 const int K=sites.size(); const int INF=K+1;

 vector<vector<int>>out(nodes.size()),inc(nodes.size());
 vector<map<int,int>>outmap(nodes.size()),inmap(nodes.size());
 for(int i=0;i<(int)rows.size();i++){
   Edge e=rows[i];out[e.u].push_back(i);inc[e.v].push_back(i);
   if(!outmap[e.u].emplace(e.v,i).second)abort();inmap[e.v][e.u]=i;
 }
 auto order=[&](int x,int y){auto s=nodes[x],t=nodes[y];return tie(s[0],s[1])<tie(t[0],t[1]);};
 auto legal=[&](int pr,int signpr,int cu,int signcu){
  auto u=nodes[pr],v=nodes[cu];int h=u[2]-v[2],j=(u[3]+3*(signpr<0)+3-v[3]-3*(signcu<0)+12)%6;
  for(int m=j;m<=6;m+=6)if(m+h>=0&&m+h<=6&&2*m+h>0&&2*m+h<12)return true;return false;
 };

 const W unit=W(D)*D*a*b;long long visits=0,returns=0,prints=0;map<int,long long> hist;int deepest=0;
 vector<int> path,back(nodes.size(),INF),marked,frontier;

 auto intersects=[](Point a,Point b,Point c,Point d){
  if(max(a.x,b.x)<min(c.x,d.x)||max(c.x,d.x)<min(a.x,b.x)||max(a.y,b.y)<min(c.y,d.y)||max(c.y,d.y)<min(a.y,b.y))return false;
  auto sg=[](W t){return (t>0)-(t<0);};
  return sg(cross(a,b,c))*sg(cross(a,b,d))<=0&&sg(cross(c,d,a))*sg(cross(c,d,b))<=0;
 };
 auto validChain=[&](int id){
   if(path.empty())return true;auto &last=rows[path.back()];auto &next=rows[id];
   int delta=next.la-last.lb;if(!goodlen(delta))return false;
   if(path.size()==1)return true;auto &prev=rows[path[path.size()-2]];
   if(!legal(prev.v,last.la-prev.lb,last.v,delta))return false;
   Point A=last.p,B=next.p;
   if(!cross(prev.p,A,B))return false;
   for(size_t i=0;i+2<path.size();i++)if(intersects(rows[path[i]].p,rows[path[i+1]].p,A,B))return false;
   return true;
 };
 auto emit=[&](){int K=path.size();
   for(int i=0;i<K;i++){
    auto &pre=rows[path[(i+K-1)%K]],&cur=rows[path[i]],&nex=rows[path[(i+1)%K]];
    int d1=cur.la-pre.lb,d2=nex.la-cur.lb;
    if(!goodlen(d1)||!legal(cur.u,d1,cur.v,d2))return;
    if(!cross(pre.p,cur.p,nex.p))return;
    for(int j=i+2;j<K;j++){
      if(i==0&&j+1==K)continue;
      if(intersects(cur.p,nex.p,rows[path[j]].p,rows[path[(j+1)%K]].p))return;
    }
   }
   W area2=0;for(int i=1;i+1<K;i++)area2+=cross(rows[path[0]].p,rows[path[i]].p,rows[path[i+1]].p);
   if(area2<=0||area2>=area*unit||area2%unit)return;
   cout<<K<<' ';for(int i:path)cout<<i<<' ';
   for(int i=0;i<K;i++)cout<<rows[path[(i+1)%K]].la-rows[path[i]].lb<<' ';
   cout<<(long long)(area2/unit)<<'\n';++prints;++hist[K];
 };
 for(int u=0;u<(int)nodes.size();u++){
   // Shortest possible ordered return to u, ignoring the geometry of the core.
   for(int v:marked)back[v]=INF;marked.clear();frontier={u};
   for(int d=1;d<K;d++){
     vector<int> next;
     for(int w:frontier)for(int id:inc[w]){
       int v=rows[id].u;if(!order(u,v)||(d>1&&!order(v,w))||back[v]<=d)continue;
       back[v]=d;marked.push_back(v);next.push_back(v);
     }frontier.swap(next);if(frontier.empty())break;
   }
   auto dfs=[&](auto&&self,int v)->void{
    deepest=max(deepest,(int)path.size());
    if(path.size()+1>=3){
      auto it=outmap[v].find(u);if(it!=outmap[v].end()){
        ++returns;if(validChain(it->second)){
          path.push_back(it->second);emit();path.pop_back();
        }
      }
    }
    if(path.size()+1>=K)return;
    for(int id:out[v]){
      int t=rows[id].v;
      if(!order(v,t)||back[t]>K-(int)path.size()-1||!validChain(id))continue;
      ++visits;path.push_back(id);self(self,t);path.pop_back();
    }
   };
   dfs(dfs,u);
 }
 cerr<<"max path "<<deepest<<" histogram";for(auto [k,n]:hist)cerr<<" "<<k<<":"<<n;cerr<<"\n";
 cerr<<"ears "<<rows.size()<<" path nodes "<<visits<<" returns "<<returns<<" anchor bound "<<K<<" cycles "<<prints<<"\n";
}
