#include <array>
#include <vector>
#include <map>
#include <tuple>
#include <set>
#include <algorithm>
#include <numeric>
#include <iostream>
#include <cstdlib>
using namespace std;
using Z=long long; using W=__int128_t;
struct P { Z x,y; auto operator<=>(const P&)const=default;};
P operator+(P a,P b){return {a.x+b.x,a.y+b.y};}
P operator-(P a,P b){return {a.x-b.x,a.y-b.y};}
P operator*(Z t,P a){return {t*a.x,t*a.y};}
P rot(P a){return {-a.y,a.x+a.y};}
P mul(P a,P b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}
W cross(P a,P b){return W(a.x)*b.y-W(a.y)*b.x;}
P dir(P a){Z d=gcd(abs(a.x),abs(a.y));return {a.x/d,a.y/d};}
W norm(P d){return W(d.x)*d.x+W(d.x)*d.y+W(d.y)*d.y;}
int exact_length(P d,Z den,int upper){
 W square=norm(d);
 int lo=0,hi=upper+1;
 while(lo<hi){int mid=(lo+hi)/2;if(W(mid)*mid*den*den<square)lo=mid+1;else hi=mid;}
 return lo<=upper&&W(lo)*lo*den*den==square?lo:-1;
}
using Tri=array<P,3>;using Edge=pair<P,P>;
struct Shape { Tri t; };
int a,b,c,defects,allowedDefects,allowedRadius;
Z nodes,gridDen; P distinguishedAxis,anchorCorner;
map<P,vector<bool>> coins;
vector<P> outer;vector<Shape> chosen;
map<P,vector<Shape>> byout;
bool sep(const Tri &t,const Tri &v){
 for(int i=0;i<3;i++){P d=t[(i+1)%3]-t[i];bool ok=true;for(P q:v)if(cross(d,q-t[i])>0){ok=false;break;}if(ok)return true;}return false;
}
map<P,int> metricLength;
set<pair<P,P>> feasibleTurns;
bool polarLess(P p,P q){
 bool a=p.y>0||(p.y==0&&p.x>0),b=q.y>0||(q.y==0&&q.x>0);
 if(a!=b)return a>b;return cross(p,q)>0;
}
void buildAngleTable(){
 vector<P> rays;for(const auto &[p,shapes]:byout)rays.push_back(p);
 sort(rays.begin(),rays.end(),polarLess);
 const int count=rays.size();map<P,int> ranks;
 for(int i=0;i<count;i++)ranks[rays[i]]=i;
 for(int i=0;i<count;i++) {
  vector<bool> can(count);can[0]=true;
  for(int j=0;j<count;j++)if(can[j]){
   P p=rays[(i+j)%count];feasibleTurns.insert({rays[i],p});
   auto extend=[&](P q){int d=(ranks.at(q)-ranks.at(p)+count)%count;if(d && j+d<count)can[j+d]=true;};
   extend(-1*p);
   for(const auto &s:byout[p])extend(dir(s.t[2]));
  }
 }
}
bool admissibleGap(P lower,P upper){return lower==upper||(cross(lower,upper)>0&&feasibleTurns.count({lower,upper}));}
map<tuple<P,int,P,P>,bool> spanCache;
bool sideSpan(P ray,int L,P upperStart,P lowerEnd){
 if(!L)return admissibleGap(lowerEnd,upperStart);
 auto key=make_tuple(ray,L,upperStart,lowerEnd);auto found=spanCache.find(key);
 if(found!=spanCache.end())return found->second;
 for(const Shape &s:byout[ray]){
   int len=metricLength.at(s.t[1]);if(len>L)continue;
   P left=dir(s.t[2]),right=dir(s.t[2]-s.t[1]);
   if(admissibleGap(left,upperStart)&&sideSpan(ray,L-len,right,lowerEnd))
    return spanCache.emplace(key,true).first->second;
 }
 return spanCache.emplace(key,false).first->second;
}
bool nearby(const Tri &A,const Tri &B) {
 for(int i=0;i<3;i++){
  P p=A[i],q=A[(i+1)%3],d=q-p;
  for(auto r:B){if(min(p,q)<r&&r<max(p,q)&&cross(d,r-p)==0){
    Z dl=d.x?d.x:d.y,offset=d.x?r.x-p.x:r.y-p.y;
    if((offset*metricLength.at(d))%dl)return false;
  }}
 }return true;
}
struct Bank {P start,end;bool clampStart,clampEnd;};
bool positionAllowed(P r,const Bank &bank) {
 const P p=bank.start,q=bank.end,d=q-p;
 if(!(min(p,q)<r&&r<max(p,q))||cross(d,r-p))return true;
 auto it=coins.find(dir(d));if(it==coins.end())return false;
 if(bank.clampStart){int n=exact_length(r-p,gridDen,10000);if(n<0||!it->second[n])return false;}
 if(bank.clampEnd){int n=exact_length(q-r,gridDen,10000);if(n<0||!it->second[n])return false;}
 return true;
}
struct Box { Z xmin,xmax,ymin,ymax; };
Box bounds(Tri const &t){
 return {min({t[0].x,t[1].x,t[2].x}),max({t[0].x,t[1].x,t[2].x}),
         min({t[0].y,t[1].y,t[2].y}),max({t[0].y,t[1].y,t[2].y})};
}
bool disjoint(Box const &a,Box const&b){
 return a.xmax<b.xmin||b.xmax<a.xmin||a.ymax<b.ymin||b.ymax<a.ymin;
}
vector<Box> placedBoxes;
bool oneAxis(Tri const& t){for(int i=0;i<3;i++)if(!cross(distinguishedAxis,t[(i+1)%3]-t[i]))return true;return false;}
bool nearCorner(P p){return norm(p-anchorCorner)<=W(allowedRadius)*allowedRadius*gridDen*gridDen;}
bool onX(const Tri&t){for(int i=0;i<3;i++)if(t[i].y==0 && t[(i+1)%3].y==0)return true;return false;}
bool isDefect(Tri const&t){return !oneAxis(t)&&!onX(t)&&any_of(t.begin(),t.end(),nearCorner);}
bool good(const Shape &s,const vector<Bank>& banks){if(defects>=allowedDefects && isDefect(s.t))return false;for(int i=0;i<(int)outer.size();i++)for(auto q:s.t)if(cross(outer[(i+1)%outer.size()]-outer[i],q-outer[i])<0)return false;
 for(auto &w:banks)for(auto r:s.t)if(!positionAllowed(r,w))return false;
 Box box=bounds(s.t);for(int i=0;i<(int)chosen.size();i++){if(disjoint(box,placedBoxes[i]))continue;const auto &v=chosen[i];
  if(!sep(s.t,v.t)&&!sep(v.t,s.t))return false;
  if(!nearby(s.t,v.t)||!nearby(v.t,s.t))return false;
 }return true;}
vector<Edge> update(const vector<Edge> &old,const Tri &t){
 vector<Edge> z=old;
 for(int j=0;j<3;j++){
  P a=t[(j+1)%3],b=t[j],u=dir(b-a);if(u<P{0,0})u=-1*u;
  map<P,int> event;vector<Edge> keep;
  auto add=[&](P p,P q){event[p]++;event[q]--;};
  add(a,b);
  for(auto [p,q]:z){if(cross(q-p,u)||cross(p-a,u))keep.push_back({p,q});else add(p,q);}
  P prev{};int n=0;
  for(auto [cur,val]:event)if(val){
    if(n==1)keep.push_back({prev,cur});if(n==-1)keep.push_back({cur,prev});
    n+=val;if(abs(n)>1){cerr<<"invalid boundary";exit(3);}prev=cur;
  }
  z=move(keep);
 }
 return z;
}
bool dfs(const vector<Edge>&edges){
 ++nodes;
 if(edges.empty())return true;
 if(defects>allowedDefects)return false;map<P,vector<P>> in,out;
 for(auto [p,q]:edges){out[p].push_back(q-p);in[q].push_back(q-p);}
 for(const auto &[p,ray]:out)if(ray.size()==1&&in[p].size()==1){
  bool through=false;for(auto [x,y]:edges)if(min(x,y)<p&&p<max(x,y)&&!cross(y-x,p-x)){through=true;break;}
  if(!through){P start=dir(ray[0]),end=dir(-1*in[p][0]);if(!feasibleTurns.count({start,end}))return false;}
 }
 set<P> convex;
 for(auto &[p,r]:out){if(r.size()!=1||in[p].size()!=1||cross(in[p][0],r[0])<=0)continue;
  bool transit=false;for(auto [x,y]:edges)if(p!=x&&p!=y&&!cross(y-x,p-x)&&min(x,y)<p&&p<max(x,y)){transit=true;break;}if(!transit)convex.insert(p);
 }
 vector<Bank> banks;for(auto [p,q]:edges){bool clamped=convex.count(p)&&convex.count(q);for(int i=0;i<(int)outer.size()&&!clamped;i++){P d=outer[(i+1)%outer.size()]-outer[i];if(!cross(q-p,d)&&!cross(p-outer[i],d))clamped=true;}
  if(clamped||convex.count(p)||convex.count(q))banks.push_back({p,q,clamped||bool(convex.count(p)),clamped||bool(convex.count(q))});
  if(clamped){P d=q-p;int L=exact_length(d,gridDen,10000);P ray=dir(d);
   if(norm(d)>W(10000)*10000*gridDen*gridDen){cerr<<"length table exceeded"<<endl;exit(5);}
   if(L<0||!coins.count(ray)||!coins[ray][L])return false;
   if(convex.count(p)&&convex.count(q)&&!sideSpan(ray,L,dir(-1*in[p][0]),dir(out[q][0])))return false;
}
 }
 vector<vector<Shape>> best;bool init=false;
 vector<P> pivots(convex.begin(),convex.end());
 for(P p:pivots){if(!nearCorner(p))continue;
  P begin=dir(out[p][0]),end=dir(-1*in[p][0]);
  vector<vector<Shape>> cand;vector<Shape> fan;
  auto addfan=[&](auto &&self,P source)->void{
   if(init && cand.size()>=best.size())return;
   if(source==end){cand.push_back(fan);return;}
   for(auto s:byout[source]){
    P next=dir(s.t[2]);if(cross(next,end)<0 || (cross(next,end)==0 && next!=end) || cross(begin,next)<=0)continue;
    for(auto &q:s.t)q=q+p;if(!good(s,banks))continue;
    fan.push_back(s);self(self,next);fan.pop_back();
   }
  };
  addfan(addfan,begin);if(cand.empty())return false;if(!init||cand.size()<best.size()){init=true;best=move(cand);}
 }
 if(!init)return true;
 for(const auto &fan:best){
  auto child=edges;
  for(const auto &s:fan){
   defects+=isDefect(s.t);chosen.push_back(s);placedBoxes.push_back(bounds(s.t));child=update(child,s.t);
  }
  if(dfs(child))return true;
  for(const auto&s:fan){defects-=isDefect(s.t);chosen.pop_back();placedBoxes.pop_back();}
 }
 return false;
}
void verify(int aa,int bb,int cc,int index,int radius,int allowance){
 a=aa;b=bb;c=cc;gridDen=c*c;allowedDefects=allowance;allowedRadius=radius;
 defects=0;nodes=0;
 outer={{0,0},{gridDen*b*(2*a+b),0},{0,gridDen*a*(a+2*b)}};
 anchorCorner=outer[index];distinguishedAxis=rot({a,b});
 chosen.clear();placedBoxes.clear();byout.clear();coins.clear();metricLength.clear();feasibleTurns.clear();spanCache.clear();
 for(int height=0;height<=2;height++){
  P d{1,0};Z denominator=1;
  for(int i=0;i<height;i++){d=mul(d,{a,b});denominator*=c;}
  d=(gridDen/denominator)*d;
  for(int phase=0;phase<6;phase++,d=rot(d))for(int hand:{-1,1}){
   P v=rot(rot(d));if(hand<0)v=rot(rot(v));
   Tri t={{P{0,0},a*d,b*v}};
   if(cross(t[1],t[2])<0)swap(t[1],t[2]);
   for(int i=0;i<3;i++){
    Tri r={P{0,0},t[(i+1)%3]-t[i],t[(i+2)%3]-t[i]};
    byout[dir(r[1])].push_back({r});
   }
  }
 }
 for(auto &[ray,variants]:byout){
  vector<bool> possible(10001);possible[0]=true;
  for(const auto&sh:variants){
   const P d=sh.t[1];int len=exact_length(d,gridDen,c);
   if(len!=a&&len!=b&&len!=c)abort();metricLength[d]=len;
   for(int j=len;j<(int)possible.size();j++)possible[j]=possible[j]||possible[j-len];
  }coins[ray]=move(possible);
 }
 buildAngleTable();
 vector<Edge> edges;
 for(int i=0;i<3;i++)edges.push_back({outer[i],outer[(i+1)%3]});
 bool possible=dfs(edges);
 cout<<a<<" "<<index<<" "<<radius<<" "<<allowance<<" "<<possible<<" "<<nodes<<endl;
 if(possible)exit(1);
}
int main(){
 verify(33,7,37,0,75,3);
 verify(33,7,37,1,85,10);
 verify(35,13,43,0,140,6);
 verify(35,13,43,1,175,7);
}
