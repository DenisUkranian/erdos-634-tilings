#include <array>
#include <vector>
#include <map>
#include <tuple>
#include <set>
#include <algorithm>
#include <numeric>
#include <iostream>
#include <cstdlib>
#include <cmath>
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
// A direction is an oriented primitive integer vector in the Eisenstein basis.
// All metric computations below compare integer squared norms.
W norm(P d){return W(d.x)*d.x+W(d.x)*d.y+W(d.y)*d.y;}
int exact_length(P d,Z den,int upper){
 W square=norm(d);
 int lo=0,hi=upper+1;
 while(lo<hi){int mid=(lo+hi)/2;if(W(mid)*mid*den*den<square)lo=mid+1;else hi=mid;}
 return lo<=upper&&W(lo)*lo*den*den==square?lo:-1;
}
using Tri=array<P,3>;using Edge=pair<P,P>;
struct Shape {Tri t;int h;int sign;int chir;};
int a,b,c,t,k,target,hlo,hhi,chosenN=0;
Z nodes=0,limit,gridDen;
vector<array<int,13>> inventories; array<int,13> used{},takenSigns{},takenUps{},takenDowns{};
struct Signature {array<int,13> pop,G,up,down;};
vector<Signature> signatures;
void signTake(Shape const &s,int inc){takenSigns[s.h+6]+=inc*s.sign;(s.chir>0?takenUps:takenDowns)[s.h+6]+=inc*s.sign;}
extern vector<P> outer;
void findSignatures(){
 map<P,pair<int,int>> directions;map<int,int> ext;
 for(int h=hlo-1;h<=hhi+1;h++){P u={1,0};for(int x=0;x<abs(h);x++)u=mul(u,h>0?P{a,b}:P{a+b,-b});
 for(int j=0;j<6;j++,u=rot(u))directions[dir(u)]={h,j%2?-1:1};}
 int E=0,A=0,d=a-b;
 for(int i=0;i<(int)outer.size();i++){P edge=outer[(i+1)%outer.size()]-outer[i];auto [h,sign]=directions.at(dir(edge));
 int l=exact_length(edge,gridDen,10000);if(l<=0)abort();E+=sign*l;A+=(h%2?-1:1)*sign*l;ext[h]+=sign*l;}
 if(E%(d-c)||A%(d+c))return;int sum=E/(d-c),alt=A/(d+c);
 Signature r;
 for(const auto &population:inventories){r.pop=population;r.G={};r.up={};r.down={};
 auto extend=[&](auto&&self,int h,int gsum,int galt)->void{
 if(h>hhi){if(gsum!=sum||galt!=alt)return;
  int lastup=0;for(int i=hlo-1;i<=hhi+1;i++){
    int g=i>=hlo&&i<=hhi?r.G[i+6]:0;
    int back=(d*g-ext[i]);if(back%c)return;
    int down=back/c-lastup;
    if(i+1>=hlo&&i+1<=hhi){r.down[i+7]=down;r.up[i+7]=r.G[i+7]-down;
     if(abs(r.down[i+7])+abs(r.up[i+7])>r.pop[i+7])return;}
    else if(down)return;
    lastup=i>=hlo&&i<=hhi?r.up[i+6]:0;
  }signatures.push_back(r);return;
 }
 for(int z=-r.pop[h+6];z<=r.pop[h+6];z+=2)if((d*z-ext[h])%c==0){
  r.G[h+6]=z;self(self,h+1,gsum+z,galt+(h%2?-z:z));
 }
 };extend(extend,hlo,0,0);}
}
struct PhaseLevel{
 map<Z,array<int,3>> by[2];
 array<int,3> bound[2]{};
 Z mod[2]{},root[2]{};
};
PhaseLevel phases[13];
array<array<int,2>,13> residues{};
void prepPhase(){
 int H=0;for(Z v=gridDen;v>1;v/=c)H++;
 for(int h=hlo;h<=hhi;h++)for(int side=0;side<2;side++){
  int depth=H+(side?-h:h);auto &p=phases[h+6];Z m=1,r=0;
  for(int i=0;i<depth;i++){
   Z next=m*c;bool fit=false;
   for(int j=0;j<c;j++){Z x=r+m*j;if(i==0&&x!=(side?7:37))continue;
    if((W(x)*x-x+1)%next==0){r=x;fit=true;break;}}
   if(!fit)abort();m=next;
  }p.mod[side]=m;p.root[side]=r;
  if(h==0||h==1){
   const auto &sig=signatures.at(0);int total=sig.pop[h+6],g=sig.G[h+6];
   int plus=(total+g)/2%c, minus=(total-g)/2%c;
   for(const auto &s:signatures)if((s.pop[h+6]+s.G[h+6])/2%c!=plus||(s.pop[h+6]-s.G[h+6])/2%c!=minus)abort();
   residues[h+6]={plus,minus};p.bound[side]={plus,minus,plus+minus};
  }
 }
}
array<int,3> phaseBill(array<int,3> cnt,bool core,int h){
 int x=core?residues[h+6][0]:0,y=core?residues[h+6][1]:0;
 x+=max(0,(cnt[0]-x+c-1)/c)*c;y+=max(0,(cnt[1]-y+c-1)/c)*c;
 int n=x+y;if(!core&&(n!=0||cnt[2]>0)&&n<2*c)n=2*c;
 return {x,y,n};
}
void phaseTake(const Shape &s, int inc){
 P v=s.t[0];
 for(int side=0;side<2;side++)for(int h=s.h;h>=hlo&&h<=hhi;h+=side?1:-1){
  auto &p=phases[h+6];Z m=p.mod[side];Z key=(W(v.y)*p.root[side]+v.x)%m;if(key<0)key+=m;
  bool exterior=(side?h>=0:h<=1)&&key==0;
  if(h!=s.h&&exterior)break;
  auto &count=p.by[side][key];bool core=(h==0||h==1)&&key==0;
  auto prev=phaseBill(count,core,h);count[h==s.h?int(s.sign<0):2]+=inc;auto next=phaseBill(count,core,h);
  for(int j=0;j<3;j++)p.bound[side][j]+=next[j]-prev[j];
  if(count[0]==0&&count[1]==0&&count[2]==0)p.by[side].erase(key);
  if(exterior)break;
 }
}
bool phaseAccept(const Signature &r,int h){
 int i=h+6;const auto &p=phases[i];
 for(int side=0;side<2;side++){
  const auto &b=p.bound[side];if(b[2]>r.pop[i]||b[0]>(r.pop[i]+r.G[i])/2||b[1]>(r.pop[i]-r.G[i])/2)return false;
 }return true;
}

bool possibleSigns(){
 for(auto const &r:signatures){bool ok=true;for(int h=hlo;h<=hhi&&ok;h++){
 int i=h+6,left=r.pop[i]-used[i];if(!phaseAccept(r,h)||left<0||abs(r.G[i]-takenSigns[i])>left||
 abs(r.up[i]-takenUps[i])+abs(r.down[i]-takenDowns[i])>left)ok=false;
 }if(ok)return true;}return false;
}
map<P,vector<bool>> coins;
vector<P> outer;vector<Shape> chosen;
map<P,vector<Shape>> byout,byin;
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
   extend(-1*p); // Straight corner of a tile with a through-edge.
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
bool good(const Shape &s,const vector<Bank>& banks){for(int i=0;i<(int)outer.size();i++)for(auto q:s.t)if(cross(outer[(i+1)%outer.size()]-outer[i],q-outer[i])<0)return false;
 for(auto &w:banks)for(auto r:s.t)if(!positionAllowed(r,w))return false;
 Box box=bounds(s.t);for(int i=0;i<(int)chosen.size();i++){if(disjoint(box,placedBoxes[i]))continue;const auto &v=chosen[i];
  if(!sep(s.t,v.t)&&!sep(v.t,s.t))return false;
  if(!nearby(s.t,v.t)||!nearby(v.t,s.t))return false;
 }return true;}
bool locatedSpan(P p,P q,P upper,P lower,int L,const vector<Bank>& banks){
 const P d=q-p,ray=dir(d);map<pair<int,P>,bool> memo;
 auto solve=[&](auto&&self,int start,P up)->bool{
   if(start==L)return admissibleGap(lower,up);
   auto key=make_pair(start,up);if(auto it=memo.find(key);it!=memo.end())return it->second;
   Z x=d.x*start,y=d.y*start;if(x%L||y%L)return false;P point=p+P{x/L,y/L};
   for(auto s:byout[ray]){
    int n=metricLength.at(s.t[1]);if(start+n>L)continue;
    P left=dir(s.t[2]),right=dir(s.t[2]-s.t[1]);if(!admissibleGap(left,up))continue;
    for(auto &v:s.t)v=v+point;
    if(good(s,banks)&&self(self,start+n,right))return memo.emplace(key,true).first->second;
   }
   return memo.emplace(key,false).first->second;
 };return solve(solve,0,upper);
}
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
bool integralLoops(const vector<Edge>&edges){
 map<P,int> ids;vector<int> parent,rank;vector<W> wt;
 W mod=W(gridDen)*gridDen*a*b;
 auto id=[&](P p){auto it=ids.find(p);if(it!=ids.end())return it->second;
  int i=parent.size();parent.push_back(i);rank.push_back(0);wt.push_back(0);ids[p]=i;return i;};
 auto find=[&](int p){W w=0;while(parent[p]!=p){w+=wt[p];p=parent[p];}return pair<int,W>{p,w};};
 for(auto [p,q]:edges){
  int u=id(p),v=id(q);auto [r,x]=find(u);auto [s,y]=find(v);
  W diff=(cross(p,q)+x-y)%mod;
  if(r==s){if(diff)return false;}
  else if(rank[r]<rank[s]){parent[r]=s;wt[r]=-diff;}
  else{parent[s]=r;wt[s]=diff;if(rank[r]==rank[s])rank[r]++;}
 }
 return true;
}
int shardCount=1,shardID=0,shardDepth=8,subCount=1,subID=0,thirdCount=1,thirdID=0,lastCount=1,lastID=0;
bool dfs(const vector<Edge>&edges,int level=0,unsigned hash=0){
 if(shardCount>1&&level==shardDepth&&int(hash%shardCount)!=shardID)return false;
 if(subCount>1&&level==shardDepth+6&&int(hash%subCount)!=subID)return false;
 if(thirdCount>1&&level==shardDepth+12&&int(hash%thirdCount)!=thirdID)return false;
 if(lastCount>1&&level==shardDepth+18&&int(hash%lastCount)!=lastID)return false;
 nodes++;if(nodes%50000==0)cerr<<"nodes "<<nodes<<" depth "<<chosen.size()<<"\n";if(nodes>limit){cerr<<"budget "<<nodes<<"\n";exit(2);}
#ifdef LOOP_FILTER
 if(!integralLoops(edges))return false;
#endif
 if(chosen.size()>target)abort();
 if(chosen.size()==target){if(!edges.empty())abort();cout<<"YES "<<nodes<<"\n";for(auto &tile:chosen){for(P p:tile.t)cout<<p.x<<" "<<p.y<<" ";cout<<tile.h<<"\n";}return true;}
 map<P,vector<P>> in,out;
 for(auto [p,q]:edges){out[p].push_back(q-p);in[q].push_back(q-p);}
 bool populationOK=false;for(const auto &row:inventories){bool ok=true;for(int j=0;j<13;j++)if(used[j]>row[j])ok=false;if(ok){populationOK=true;break;}}if(!populationOK)return false;
#ifdef REFLEX_FILTER
 for(const auto &[p,ray]:out)if(ray.size()==1&&in[p].size()==1){
  bool through=false;for(auto [x,y]:edges)if(min(x,y)<p&&p<max(x,y)&&!cross(y-x,p-x)){through=true;break;}
  if(!through){P start=dir(ray[0]),end=dir(-1*in[p][0]);if(!feasibleTurns.count({start,end}))return false;}
 }
#endif
#ifdef SIGN_FILTER
 if(!possibleSigns())return false;
#endif
 set<P> convex;
 for(auto &[p,r]:out){if(r.size()!=1||in[p].size()!=1||cross(in[p][0],r[0])<=0)continue;
  bool transit=false;for(auto [x,y]:edges)if(p!=x&&p!=y&&!cross(y-x,p-x)&&min(x,y)<p&&p<max(x,y)){transit=true;break;}if(!transit)convex.insert(p);
 }
 vector<Bank> banks;for(auto [p,q]:edges){bool clamped=convex.count(p)&&convex.count(q);for(int i=0;i<(int)outer.size()&&!clamped;i++){P d=outer[(i+1)%outer.size()]-outer[i];if(!cross(q-p,d)&&!cross(p-outer[i],d))clamped=true;}
  if(clamped||convex.count(p)||convex.count(q))banks.push_back({p,q,clamped||bool(convex.count(p)),clamped||bool(convex.count(q))});
  if(clamped){P d=q-p;int L=exact_length(d,gridDen,10000);P ray=dir(d);
   if(norm(d)>W(10000)*10000*gridDen*gridDen){cerr<<"length table exceeded"<<endl;exit(5);}
   if(L<0||!coins.count(ray)||!coins[ray][L])return false;
#ifdef SPAN_FILTER
   if(convex.count(p)&&convex.count(q)&&!sideSpan(ray,L,dir(-1*in[p][0]),dir(out[q][0])))return false;
#endif
}
 }
#ifdef LOCATED_SPANS
 for(auto [p,q]:edges)if(convex.count(p)&&convex.count(q)){
  int L=exact_length(q-p,gridDen,10000);
  if(L<0||!locatedSpan(p,q,dir(-1*in[p][0]),dir(out[q][0]),L,banks))return false;
 }
#endif
 vector<vector<Shape>> best;bool init=false;
 vector<P> pivots(convex.begin(),convex.end());
#ifdef REVERSE_TIES
 reverse(pivots.begin(),pivots.end());
#endif
 for(P p:pivots){
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
#ifdef LEFT_SIDE_FIRST
 if(init){vector<vector<Shape>> left;bool have=false;
  for(auto [p,q]:edges)if(p.x==0&&q.x==0){P d=q-p;int L=exact_length(d,gridDen,10000);
   vector<vector<Shape>> options;
   for(auto s:byout[dir(d)]){
    int n=metricLength.at(s.t[1]);if(n>L||!coins[dir(d)][L-n])continue;
    for(auto&v:s.t)v=v+p;if(good(s,banks))options.push_back({s});
   }
   if(options.empty())return false;if(!have||options.size()<left.size()){have=true;left=move(options);}
  }if(have)best=move(left);
 }
#endif
#ifdef BANK_PROBES
 if(init&&best.size()>1){
 for(auto [p,q]:edges){
  if(!convex.count(p)||!convex.count(q))continue;
  P d=q-p,ray=dir(d),upper=dir(-1*in[p][0]),lower=dir(out[q][0]);
  int L=exact_length(d,gridDen,10000);if(L<=0)return false;
  for(int m:{L/2,L/3,2*L/3}){
   vector<vector<Shape>> options;
   for(int x=max(0,m-c+1);x<=m&&options.size()<best.size();x++){
    if(!coins[ray][x]||d.x*x%L||d.y*x%L)continue;
    P anchor=p+P{d.x*x/L,d.y*x/L};
    for(auto s:byout[ray]){int len=metricLength.at(s.t[1]);
     if(x+len<=m||x+len>L||!coins[ray][L-x-len])continue;
     P left=dir(s.t[2]),right=dir(s.t[2]-s.t[1]);
     if(!sideSpan(ray,x,upper,left)||!sideSpan(ray,L-x-len,right,lower))continue;
     for(auto &v:s.t)v=v+anchor;if(good(s,banks))options.push_back({s});
    }
   }
   if(options.empty())return false;
   if(options.size()<best.size())best=move(options);
   if(best.size()==1)break;
  }
  if(best.size()==1)break;
 }}
#endif
 if(!init){cerr<<"singular state; no decision\n";exit(4);}
 int branch=0;for(const auto &fan:best){auto child=edges;for(const auto &s:fan){chosen.push_back(s);placedBoxes.push_back(bounds(s.t));used[s.h+6]++;signTake(s,1);phaseTake(s,1);child=update(child,s.t);}unsigned childHash=hash;int childLevel=level;if(shardCount>1 && level<shardDepth+(subCount>1?6:0)+(thirdCount>1?6:0)+(lastCount>1?6:0) && best.size()>1){
   childHash=hash*16777619u+(unsigned)branch+1u;childLevel++;
 }branch++;if(dfs(child,childLevel,childHash))return true;for(auto &s:fan){chosen.pop_back();placedBoxes.pop_back();used[s.h+6]--;signTake(s,-1);phaseTake(s,-1);}}
 return false;
}
int main(int ac,char**av){
 if(ac!=9&&ac!=10&&ac!=11&&ac!=12)return 1;a=atoi(av[1]);b=atoi(av[2]);c=atoi(av[3]);t=atoi(av[4]);k=atoi(av[5]);hlo=atoi(av[6]);hhi=atoi(av[7]);limit=atoll(av[8]);target=t*t-k*k;
 if(hlo< -6||hhi>6||hhi<hlo)return 3;int pow=max({1,-hlo,hhi});Z den=1;for(int i=0;i<pow;i++)den*=c;
 gridDen=den;
 int l=ac==12?atoi(av[11]):0;int jrow=ac>=11?atoi(av[10]):1;int step=ac>=10?atoi(av[9]):(c-a)/2;P X={0,step*c*den},Y={0,(step*c+t*b)*den},W={Z(t*a-k*c)*den,(step*c+t*b)*den};
 P D=X+P{t*a*den-k*a*a*(den/c),t*b*den-k*a*b*(den/c)},V={a*b*(den/c),b*b*(den/c)-c*den};
 outer={{0,(step-jrow)*c*den},Y,W,D,D+jrow*V};
 target=t*t-k*k+2*jrow*(a-step)+jrow*jrow;
 if(l){if(step!=jrow)return 3;P P0={0,0},T={a*a*b*(den/c),a*b*b*(den/c)},U={b*(a+b)*(den/c),-a*b*(den/c)};
 outer={P0,Y,W,D+l*U,T+l*U,P0+P{l*c*den,0}};target+=l*(2*b-l+2*step);
 }
 if(jrow==0)outer.pop_back();
 if(k==0 && jrow==0)outer={{0,0},{t*a*den,0},{-t*b*den,t*b*den}};
 int sides=outer.size();__int128 ar=0;for(int i=0;i<sides;i++)ar+=cross(outer[i],outer[(i+1)%sides]);if(ar<0){reverse(outer.begin(),outer.end());ar=-ar;}if(ar!=__int128(target)*den*den*a*b)abort();
 for(int i=0;i<sides;i++)for(auto p:outer)if(cross(outer[(i+1)%sides]-outer[i],p-outer[i])<0)abort();
 for(int h=hlo;h<=hhi;h++){
  P d={1,0};Z n=1;for(int i=0;i<abs(h);i++){d=mul(d,h>0?P{a,b}:P{a+b,-b});n*=c;}d=(den/n)*d;
  for(int j=0;j<6;j++,d=rot(d))for(int sign:{-1,1}){
   P f=rot(rot(d));if(sign<0)f=rot(rot(f));
   Tri s={P{0,0},a*d,b*f};if(cross(s[1],s[2])<0)swap(s[1],s[2]);
   for(int i=0;i<3;i++){Tri row{P{0,0},s[(i+1)%3]-s[i],s[(i+2)%3]-s[i]};byout[dir(row[1])].push_back({row,h,j%2?-sign:sign,-sign});byin[dir(row[2])].push_back({row,h,j%2?-sign:sign,-sign});}
  }
 }
 for(auto &[ray,vec]:byout){
  vector<bool> dp(10001);dp[0]=true;for(auto &s:vec){P d=s.t[1];int l=exact_length(d,den,c);if(l!=a&&l!=b&&l!=c)abort();metricLength[d]=l;metricLength[-1*d]=l;
   for(int j=l;j<(int)dp.size();j++)if(dp[j-l])dp[j]=true;
  }coins[ray]=move(dp);
 }
 #if defined(REFLEX_FILTER) || defined(SPAN_FILTER) || defined(LOCATED_SPANS) || defined(BANK_PROBES)
 buildAngleTable();
#endif
 array<int,13> rr{};
 auto inv=[&](auto &&self,int h,int remaining)->void{if(h>hhi){if(!remaining)inventories.push_back(rr);return;}
   int res=h==0?t*t%c:h==1?(2*jrow*(a-step)+jrow*jrow+l*(2*b-l+2*step)-k*k%c+c)%c:0;
   for(int n=res;n<=remaining;n+=c){if(h!=0&&h!=1&&n==c)continue;rr[h+6]=n;self(self,h+1,remaining-n);}
 };inv(inv,hlo,target);
 #ifdef SIGN_FILTER
 findSignatures();if(signatures.empty()){cout<<"NO no signatures\n";return 0;}prepPhase();
#endif
 vector<Edge> edges;for(int i=0;i<(int)outer.size();i++)edges.push_back({outer[i],outer[(i+1)%outer.size()]});
 #ifdef SEED_P250
 if(a!=35||b!=13||c!=43||target!=250||step!=8||l!=0)return 6;
 Tri ytile={P{0,0},P{0,-a*den},P{b*den,0}};
#ifdef SEED_P250_OTHER_Y
 ytile={P{0,0},P{(a+b)*den,-a*den},P{b*den,0}};
#endif
 bool found=false;for(auto sh:byout[dir(ytile[1])])if(sh.t==ytile){
   if(found)abort();found=true;for(auto&v:sh.t)v=v+Y;chosen.push_back(sh);
   placedBoxes.push_back(bounds(sh.t));used[sh.h+6]++;signTake(sh,1);edges=update(edges,sh.t);
 }if(!found)abort();
#ifdef SEED_P250_D
 P Dp=D+V,G={a*b*(den/c),b*b*(den/c)};
 Tri needed={P{0,0},-1*V,-1*G};if(cross(needed[1],needed[2])<0)swap(needed[1],needed[2]);
 found=false;for(auto sh:byout[dir(needed[1])])if(sh.t==needed){
 if(found)abort();found=true;for(auto &v:sh.t)v=v+Dp;chosen.push_back(sh);placedBoxes.push_back(bounds(sh.t));
 used[sh.h+6]++;signTake(sh,1);edges=update(edges,sh.t);
 }if(!found)abort();
#endif
#endif
 if(auto count=getenv("PACK_SHARDS")){shardCount=atoi(count);shardID=atoi(getenv("PACK_SHARD_ID"));if(shardCount<1||shardID<0||shardID>=shardCount)return 7;}
 if(auto cnt=getenv("PACK_SUBSHARDS")){subCount=atoi(cnt);subID=atoi(getenv("PACK_SUBSHARD_ID"));if(subCount<1||subID<0||subID>=subCount)return 7;}
 if(auto cnt=getenv("PACK_THIRD_SHARDS")){thirdCount=atoi(cnt);thirdID=atoi(getenv("PACK_THIRD_ID"));if(thirdCount<1||thirdID<0||thirdID>=thirdCount)return 7;}
 if(auto cnt=getenv("PACK_LAST_SHARDS")){lastCount=atoi(cnt);lastID=atoi(getenv("PACK_LAST_ID"));if(lastCount<1||lastID<0||lastID>=lastCount)return 7;}
 if(!dfs(edges)){if(lastCount>1)cout<<"NO(last "<<lastID<<" of "<<lastCount<<", third "<<thirdID<<" of "<<thirdCount<<", subshard "<<subID<<" of "<<subCount<<", shard "<<shardID<<" of "<<shardCount<<") ";else if(thirdCount>1)cout<<"NO(third "<<thirdID<<" of "<<thirdCount<<", subshard "<<subID<<" of "<<subCount<<", shard "<<shardID<<" of "<<shardCount<<") ";else if(subCount>1)cout<<"NO(subshard "<<subID<<" of "<<subCount<<", shard "<<shardID<<" of "<<shardCount<<") ";else if(shardCount>1)cout<<"NO(shard "<<shardID<<" of "<<shardCount<<") ";else cout<<"NO(in palette) ";cout<<nodes<<"\n";}
}

