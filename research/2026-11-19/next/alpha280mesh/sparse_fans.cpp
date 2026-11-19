// Exact vertex fans and complete facing-edge chains in a supplied finite pool.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;
struct P{int x,y;auto operator<=>(const P&)const=default;};
P operator+(P a,P b){return{a.x+b.x,a.y+b.y};}
P operator-(P a,P b){return{a.x-b.x,a.y-b.y};}
P operator*(int n,P a){return{n*a.x,n*a.y};}
P primitive(P a){int n=gcd(a.x,a.y);return{a.x/n,a.y/n};}
long long det(P a,P b){return (long long)a.x*b.y-(long long)a.y*b.x;}
bool angular(P a,P b){auto half=[](P x){return x.y<0||(x.y==0&&x.x<0);};if(half(a)!=half(b))return half(a)<half(b);return det(a,b)>0;}
uint64_t point(P p){return (uint64_t(uint32_t(p.x))<<32)|uint32_t(p.y);}
struct EdgeKey{uint64_t p;int r;bool operator==(const EdgeKey&)const=default;};
struct EdgeHash{size_t operator()(const EdgeKey& e)const{uint64_t x=e.p+0x9e3779b97f4a7c15ULL*(1+e.r);x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);}};
struct Shape{P v[3],unit[3];int len[3],ray[3],arc[3];};
struct Pose{int k;P p;};
struct Fan{vector<int> arcs,good;};
int main(int argc,char** argv){
 if(argc<2||argc>4)return 2;
 ifstream pool(argv[1]),in(string(argv[1])+".shapes");int D,N,n,dd,nn,ns;pool>>D>>N>>n;in>>dd>>nn>>ns;
 if(!pool||!in||D!=dd||N!=nn||!(N==180||N==280||N==320))return 2;
 int L=9*D,base=N==180?60:N==280?140:80,ht=N==280?40:base;
 P outer[]={{0,0},{base*L,0},{base*L/2,ht*L}};
 vector<Shape> shapes(ns);
 vector<P> rays;
 for(auto& s:shapes){
  s.v[0]={0,0};for(int i:{1,2}){in>>s.v[i].x>>s.v[i].y;s.v[i]=9*s.v[i];}
  assert(det(s.v[1],s.v[2])==20LL*L*L);
  for(int j=0;j<3;j++){
   P v=s.v[(j+1)%3]-s.v[j];
   for(int l:{5,6,9})if((long long)v.x*v.x+2LL*v.y*v.y==(long long)l*l*L*L)s.len[j]=l;
   assert(s.len[j]>0&&v.x%s.len[j]==0&&v.y%s.len[j]==0);
   s.unit[j]={v.x/s.len[j],v.y/s.len[j]};rays.push_back(primitive(v));rays.push_back(primitive(-1*v));
  }
 }
 for(int i=0;i<3;i++){P v=primitive(outer[(i+1)%3]-outer[i]);rays.push_back(v);rays.push_back(-1*v);}
 sort(rays.begin(),rays.end(),angular);rays.erase(unique(rays.begin(),rays.end()),rays.end());int R=rays.size();assert(R<=60&&R%2==0);
 map<P,int> ranks;for(int i=0;i<R;i++)ranks[rays[i]]=i;
 auto opp=[&](int r){return (r+R/2)%R;};auto arc=[&](int a,int b){return R*a+b;};
 for(auto& s:shapes){for(int j=0;j<3;j++)s.ray[j]=ranks.at(primitive(s.unit[j]));for(int j=0;j<3;j++)s.arc[j]=arc(s.ray[j],opp(s.ray[(j+2)%3]));}
 int wall[3],ca[3];for(int j=0;j<3;j++)wall[j]=ranks.at(primitive(outer[(j+1)%3]-outer[j]));for(int j=0;j<3;j++)ca[j]=arc(opp(wall[(j+2)%3]),wall[j]);
 vector<Pose> placements(n);
 for(auto& p:placements){pool>>p.k>>p.p.x>>p.p.y;p.p=9*p.p;}assert(pool);
 for(int step=0;step<200;step++){
  unordered_map<uint64_t,Fan> fans;fans.reserve(2*placements.size());
  unordered_map<EdgeKey,unsigned,EdgeHash> along;along.reserve(3*placements.size());
  for(int j=0;j<3;j++)fans[point(outer[j])].arcs.push_back(ca[j]);
  for(auto p:placements){
   auto& s=shapes[p.k];for(int j=0;j<3;j++){
    fans[point(p.p+s.v[j])].arcs.push_back(s.arc[j]);
    along[{point(p.p+s.v[(j+1)%3]),opp(s.ray[j])}]|=1U<<s.len[j];
   }
  }
  for(auto p:placements){
   auto& s=shapes[p.k];for(int j=0;j<3;j++){int r=s.ray[j];int a=arc(r,opp(r));P start=p.p+s.v[j];
    for(int l=1;l<s.len[j];l++){auto it=fans.find(point(start+l*s.unit[j]));if(it!=fans.end())it->second.arcs.push_back(a);}
   }
  }
  for(auto& [id,f]:fans){
   P p{(int)(id>>32),(int)id};bool corner=false;
   for(P v:outer)if(p==v)corner=true;
   if(!corner)for(int j=0;j<3;j++)if(det(outer[(j+1)%3]-outer[j],p-outer[j])==0)f.arcs.push_back(arc(opp(wall[j]),wall[j]));
   sort(f.arcs.begin(),f.arcs.end());f.arcs.erase(unique(f.arcs.begin(),f.arcs.end()),f.arcs.end());
   uint64_t outgoing[60]={};
   for(int a:f.arcs)outgoing[a/R]|=uint64_t(1)<<(a%R);
   for(int a:f.arcs){
    int from=a%R,to=a/R,len=(to-from+R)%R;
    uint64_t reachable=1;
    for(int k=0;k<len;k++)if((reachable>>k)&1){
     int r=(from+k)%R;uint64_t opts=outgoing[r];
     while(opts){int dest=__builtin_ctzll(opts);opts&=opts-1;int d=(dest-from+R)%R;
      if(k<d&&d<=len)reachable|=uint64_t(1)<<d;}
    }
    if((reachable>>len)&1)f.good.push_back(a);
   }
  }
  for(int j=0;j<3;j++){auto& g=fans.at(point(outer[j])).good;if(!binary_search(g.begin(),g.end(),ca[j])){cout<<"missing target corner "<<j<<" at pass "<<step<<endl;return 0;}}
  vector<Pose> keep;keep.reserve(placements.size());
  for(auto p:placements){
   bool ok=true;auto& s=shapes[p.k];
   for(int j=0;j<3&&ok;j++){
    P start=p.p+s.v[j],end=p.p+s.v[(j+1)%3];auto& g=fans.at(point(start)).good;
    if(!binary_search(g.begin(),g.end(),s.arc[j])){ok=false;break;}
    bool on=false;for(int w=0;w<3;w++){P v=outer[(w+1)%3]-outer[w];if(det(v,start-outer[w])==0&&det(v,end-outer[w])==0)on=true;}
    if(on)continue;
    unsigned reachable=0;bool covered=false;
    for(int k=-8;k<s.len[j]&&!covered;k++){
     if(k>0 && ((reachable>>k)&1)==0)continue;
     auto it=along.find({point(start+k*s.unit[j]),s.ray[j]});if(it==along.end())continue;
     auto ways=it->second;while(ways){
      int l=__builtin_ctz(ways);ways&=ways-1;
      if(k+l<=0)continue;if(k+l>=s.len[j])covered=true;else reachable|=1U<<(k+l);
     }
    }
    if(!covered)ok=false;
   }
   if(ok)keep.push_back(p);
  }
  cout<<"pass "<<step+1<<" incoming "<<placements.size()<<" surviving "<<keep.size()<<endl;
  if(placements.size()==keep.size()){
   if(argc>=3){
    ofstream out(argv[2]);out<<D<<" "<<N<<" "<<keep.size()<<"\n";
    for(auto p:keep)out<<p.k<<" "<<p.p.x/9<<" "<<p.p.y/9<<"\n";
   }return 0;
  }
  placements.swap(keep);
 }
 cout<<"pass-limit"<<endl;
}
